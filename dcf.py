STARTING_FCFF = 14443.4224  # USD millions; FY ended February 1, 2026
GROWTH_RATES = [0.045, 0.04, 0.04, 0.035, 0.035]  # forecast
WACC = 0.088  # estimate as of September 10, 2026
TERMINAL_GROWTH = 0.025  # long-run economic growth assumption
NON_OPERATING_CASH = 1389.0  # USD millions; February 1, 2026
DEBT = 51308.0  # USD millions; February 1, 2026
DILUTED_SHARES = 995.0  # millions; FY2025 weighted average

# Additional editable controls
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTH_RATES = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 310.45
REVERSE_DCF_LOWER_SHIFT = -0.05
REVERSE_DCF_UPPER_SHIFT = 0.10


if TERMINAL_GROWTH >= WACC:
    raise SystemExit("Error: terminal growth must be less than WACC.")

fcff_by_year = []
fcff = STARTING_FCFF

for growth_rate in GROWTH_RATES:
    fcff *= 1.0 + growth_rate
    fcff_by_year.append(fcff)

present_value_explicit_fcff = sum(
    yearly_fcff / (1.0 + WACC) ** year
    for year, yearly_fcff in enumerate(fcff_by_year, start=1)
)

terminal_value_year_5 = (
    fcff_by_year[-1]
    * (1.0 + TERMINAL_GROWTH)
    / (WACC - TERMINAL_GROWTH)
)
present_value_terminal_value = terminal_value_year_5 / (1.0 + WACC) ** 5
enterprise_value = present_value_explicit_fcff + present_value_terminal_value
equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
value_per_diluted_share = equity_value / DILUTED_SHARES
terminal_value_share_of_enterprise_value = (
    present_value_terminal_value / enterprise_value
)

for year, yearly_fcff in enumerate(fcff_by_year, start=1):
    print(f"FCFF Year {year}: {yearly_fcff:.4f}")

print(f"Present value of five explicit FCFF: {present_value_explicit_fcff:.4f}")
print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
print(f"Present value of terminal value: {present_value_terminal_value:.4f}")
print(f"Enterprise value: {enterprise_value:.4f}")
print(f"Equity value: {equity_value:.4f}")
print(f"Value per diluted share: {value_per_diluted_share:.4f}")
print(
    "Present value of terminal value as share of enterprise value: "
    f"{terminal_value_share_of_enterprise_value:.4f}"
)


def calculate_value_per_share(wacc, terminal_growth, growth_rates):
    projected_fcff = []
    current_fcff = STARTING_FCFF

    for growth_rate in growth_rates:
        current_fcff *= 1.0 + growth_rate
        projected_fcff.append(current_fcff)

    explicit_value = sum(
        yearly_fcff / (1.0 + wacc) ** year
        for year, yearly_fcff in enumerate(projected_fcff, start=1)
    )
    terminal_value = (
        projected_fcff[-1]
        * (1.0 + terminal_growth)
        / (wacc - terminal_growth)
    )
    discounted_terminal_value = terminal_value / (1.0 + wacc) ** 5
    calculated_enterprise_value = explicit_value + discounted_terminal_value
    calculated_equity_value = (
        calculated_enterprise_value + NON_OPERATING_CASH - DEBT
    )
    return calculated_equity_value / DILUTED_SHARES


print("\nHome Depot sensitivity grid: value per diluted share")
header = "WACC \\ Terminal" + "".join(
    f"{terminal_growth:>12.2%}"
    for terminal_growth in SENSITIVITY_TERMINAL_GROWTH_RATES
)
print(header)

for sensitivity_wacc in SENSITIVITY_WACCS:
    row = f"{sensitivity_wacc:>15.2%}"
    for sensitivity_terminal_growth in SENSITIVITY_TERMINAL_GROWTH_RATES:
        if sensitivity_terminal_growth >= sensitivity_wacc:
            cell = "invalid"
        else:
            cell = f"{calculate_value_per_share(sensitivity_wacc, sensitivity_terminal_growth, GROWTH_RATES):.4f}"
        row += f"{cell:>12}"
    print(row)


print("\nHome Depot reverse DCF: uniform shift to all five explicit growth rates")
print(f"Target share price: {TARGET_SHARE_PRICE:.4f}")

lower_growth_rates = [
    growth_rate + REVERSE_DCF_LOWER_SHIFT for growth_rate in GROWTH_RATES
]
upper_growth_rates = [
    growth_rate + REVERSE_DCF_UPPER_SHIFT for growth_rate in GROWTH_RATES
]

if min(lower_growth_rates + upper_growth_rates) <= -1.0:
    print("Solved growth-rate shift: invalid bracket")
    print("Reason: the bracket pushes an annual growth rate to -100% or below.")
else:
    lower_value = calculate_value_per_share(
        WACC, TERMINAL_GROWTH, lower_growth_rates
    )
    upper_value = calculate_value_per_share(
        WACC, TERMINAL_GROWTH, upper_growth_rates
    )

    if not min(lower_value, upper_value) <= TARGET_SHARE_PRICE <= max(
        lower_value, upper_value
    ):
        print("Solved growth-rate shift: no solution in bracket")
    else:
        lower_shift = REVERSE_DCF_LOWER_SHIFT
        upper_shift = REVERSE_DCF_UPPER_SHIFT

        for _ in range(100):
            midpoint_shift = (lower_shift + upper_shift) / 2.0
            midpoint_growth_rates = [
                growth_rate + midpoint_shift for growth_rate in GROWTH_RATES
            ]
            midpoint_value = calculate_value_per_share(
                WACC, TERMINAL_GROWTH, midpoint_growth_rates
            )

            if midpoint_value < TARGET_SHARE_PRICE:
                lower_shift = midpoint_shift
            else:
                upper_shift = midpoint_shift

        solved_shift = (lower_shift + upper_shift) / 2.0
        print(
            f"Solved growth-rate shift: {solved_shift:.4f} "
            f"({solved_shift:.4%})"
        )

print(
    "Inputs held fixed: "
    f"starting FCFF={STARTING_FCFF:.4f}, "
    f"WACC={WACC:.4f}, terminal growth={TERMINAL_GROWTH:.4f}, "
    f"cash={NON_OPERATING_CASH:.4f}, debt={DEBT:.4f}, "
    f"diluted shares={DILUTED_SHARES:.4f}"
)
print("Interpretation: conditional market-implied shift, not proof of mispricing.")
