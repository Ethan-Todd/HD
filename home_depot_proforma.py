from copy import deepcopy


YEARS = [2026, 2027, 2028, 2029, 2030]

# Independent base inputs. Every run gets a fresh deep copy.
BASE_INPUTS = {
    "revenue_growth": [0.025] * 5,
    "gross_margin": [0.334] * 5,
    "sga_ratio": [0.560] * 5,
    "depreciation_ratio": 0.122,
    "impairment": [0.0] * 5,
    "capex": [4000.0] * 5,
    "tax_rate": 0.24,
    "inventory_days": 85.8,
    "accounts_payable_ratio": 0.478,
    "other_working_capital_ratio": 0.008,
    "minimum_cash": 1500.0,
    "revolver_limit": 11000.0,
    "revolver_rate": 0.037,
    "debt_repayments": [4684.0, 3625.0, 3115.0, 3852.0, 2072.0],
    "term_debt_rate": 0.046,
    "quarterly_dividend": 2.33,
    "dividend_growth": 0.025,
    "buybacks": [0.0] * 5,
    "cost_of_equity": 0.09,
    "terminal_growth": 0.025,
    "shares": 995.0,
}

# Locked one-at-a-time sensitivity ranges.
SENSITIVITY_DRIVERS = {
    "Gross margin": {
        "key": "gross_margin",
        "unit": "% of revenue",
        "years": "FY2026E-FY2030E",
        "Lower": [0.329] * 5,
        "Base": [0.334] * 5,
        "Higher": [0.339] * 5,
    },
    "SG&A efficiency": {
        "key": "sga_ratio",
        "unit": "% of gross profit (lower is more efficient)",
        "years": "FY2026E-FY2030E",
        "Lower": [0.540] * 5,
        "Base": [0.560] * 5,
        "Higher": [0.580] * 5,
    },
}

# Edit this pair to print full statements for another sensitivity case.
TRACE_RUN = ("SG&A efficiency", "Lower")
VALIDATION_TOLERANCE = 0.000001

# Opening balance sheet at February 1, 2026, and FY2025 revenue; USD millions.
OPENING = {
    "revenue": 164683.0,
    "cash": 1389.0,
    "inventory": 25817.0,
    "ppe": 28021.0,
    "other_assets": 49868.0,
    "accounts_payable": 11491.0,
    "term_debt": 51308.0,
    "revolver": 4464.0,
    "other_liabilities": 25019.0,
    "equity": 12813.0,
}


def blank_table(names):
    return {name: [] for name in names}


def assert_balanced(year, assets, liabilities_and_equity, cash, minimum_cash):
    gap = assets - liabilities_and_equity
    if abs(gap) > 0.000001:
        raise ValueError(f"{year} balance-sheet check failed; gap = {gap:.6f}")
    if cash < minimum_cash - 0.000001:
        raise ValueError(
            f"{year} minimum-cash check failed; gap = {minimum_cash - cash:.6f}"
        )


def run_model(inputs):
    income = blank_table([
        "Revenue", "Gross profit", "SG&A", "Depreciation", "Impairment",
        "Operating income", "Interest expense", "Pretax income", "Tax", "Net income",
    ])
    balance = blank_table([
        "Cash", "Inventory", "PP&E", "Other assets", "Total assets",
        "Accounts payable", "Term debt", "Revolver / commercial paper",
        "Other liabilities", "Equity", "Liabilities and equity",
    ])
    cash_flow = blank_table([
        "Net income", "Depreciation", "Impairment", "Capital spending",
        "Change in inventory", "Change in other working capital",
        "Change in accounts payable", "Debt repayment", "FCFE", "Dividends",
        "Share buyback", "Change in revolver", "Ending cash",
    ])
    checks = blank_table(["Assets - liabilities - equity", "Cash above minimum"])

    prior_revenue = OPENING["revenue"]
    opening_cash = OPENING["cash"]
    opening_inventory = OPENING["inventory"]
    opening_ppe = OPENING["ppe"]
    opening_other_assets = OPENING["other_assets"]
    opening_ap = OPENING["accounts_payable"]
    opening_debt = OPENING["term_debt"]
    opening_revolver = OPENING["revolver"]
    opening_other_liabilities = OPENING["other_liabilities"]
    opening_equity = OPENING["equity"]

    try:
        for i, year in enumerate(YEARS):
            revenue = prior_revenue * (1.0 + inputs["revenue_growth"][i])
            revenue_change = revenue - prior_revenue
            gross_profit = revenue * inputs["gross_margin"][i]
            cost_of_sales = revenue - gross_profit
            sga = gross_profit * inputs["sga_ratio"][i]
            depreciation = opening_ppe * inputs["depreciation_ratio"]
            impairment = inputs["impairment"][i]
            operating_income = gross_profit - sga - depreciation - impairment
            interest = (
                opening_debt * inputs["term_debt_rate"]
                + opening_revolver * inputs["revolver_rate"]
            )
            pretax = operating_income - interest
            tax = max(0.0, pretax) * inputs["tax_rate"]
            net_income = pretax - tax

            inventory = cost_of_sales * inputs["inventory_days"] / 365.0
            accounts_payable = inventory * inputs["accounts_payable_ratio"]
            ppe = opening_ppe + inputs["capex"][i] - depreciation
            other_wc_change = inputs["other_working_capital_ratio"] * revenue_change
            other_assets = opening_other_assets + other_wc_change - impairment
            debt_repayment = min(inputs["debt_repayments"][i], opening_debt)
            debt = opening_debt - debt_repayment
            other_liabilities = opening_other_liabilities

            dividend_per_share = (
                inputs["quarterly_dividend"] * 4.0
                * (1.0 + inputs["dividend_growth"]) ** i
            )
            dividends = dividend_per_share * inputs["shares"]
            buyback = inputs["buybacks"][i]
            equity = opening_equity + net_income - dividends - buyback

            inventory_change = inventory - opening_inventory
            ap_change = accounts_payable - opening_ap
            fcfe = (
                net_income + depreciation + impairment - inputs["capex"][i]
                - inventory_change - other_wc_change + ap_change - debt_repayment
            )

            cash_before_revolver = opening_cash + fcfe - dividends - buyback
            revolver = opening_revolver
            if cash_before_revolver < inputs["minimum_cash"]:
                draw = min(
                    inputs["minimum_cash"] - cash_before_revolver,
                    inputs["revolver_limit"] - opening_revolver,
                )
                revolver += draw
            else:
                repayment = min(
                    cash_before_revolver - inputs["minimum_cash"], opening_revolver
                )
                revolver -= repayment
            revolver_change = revolver - opening_revolver
            cash = cash_before_revolver + revolver_change

            total_assets = cash + inventory + ppe + other_assets
            liabilities_and_equity = (
                accounts_payable + debt + revolver + other_liabilities + equity
            )
            gap = total_assets - liabilities_and_equity
            assert_balanced(
                year, total_assets, liabilities_and_equity, cash, inputs["minimum_cash"]
            )

            income_values = [
                revenue, gross_profit, sga, depreciation, impairment,
                operating_income, interest, pretax, tax, net_income,
            ]
            for name, value in zip(income, income_values):
                income[name].append(value)

            balance_values = [
                cash, inventory, ppe, other_assets, total_assets, accounts_payable,
                debt, revolver, other_liabilities, equity, liabilities_and_equity,
            ]
            for name, value in zip(balance, balance_values):
                balance[name].append(value)

            cash_flow_values = [
                net_income, depreciation, impairment, -inputs["capex"][i],
                -inventory_change, -other_wc_change, ap_change, -debt_repayment,
                fcfe, -dividends, -buyback, revolver_change, cash,
            ]
            for name, value in zip(cash_flow, cash_flow_values):
                cash_flow[name].append(value)

            checks["Assets - liabilities - equity"].append(gap)
            checks["Cash above minimum"].append(cash - inputs["minimum_cash"])

            prior_revenue = revenue
            opening_cash = cash
            opening_inventory = inventory
            opening_ppe = ppe
            opening_other_assets = other_assets
            opening_ap = accounts_payable
            opening_debt = debt
            opening_revolver = revolver
            opening_other_liabilities = other_liabilities
            opening_equity = equity
    except ValueError as error:
        return {"valid": False, "error": str(error), "inputs": deepcopy(inputs)}

    valuation_valid = inputs["cost_of_equity"] > inputs["terminal_growth"]
    valuation_error = ""
    equity_value = None
    terminal_share = None
    value_per_share = None
    if valuation_valid:
        normalized_fcfe = cash_flow["FCFE"][-1] + inputs["debt_repayments"][-1]
        if normalized_fcfe <= 0.0:
            valuation_valid = False
            valuation_error = "Nonpositive sustainable FCFE cannot support terminal value."
        else:
            explicit_pv = sum(
                max(0.0, value) / (1.0 + inputs["cost_of_equity"]) ** period
                for period, value in enumerate(cash_flow["FCFE"], start=1)
            )
            terminal_value = (
                normalized_fcfe * (1.0 + inputs["terminal_growth"])
                / (inputs["cost_of_equity"] - inputs["terminal_growth"])
            )
            terminal_pv = terminal_value / (1.0 + inputs["cost_of_equity"]) ** 5
            equity_value = explicit_pv + terminal_pv
            terminal_share = terminal_pv / equity_value
            value_per_share = equity_value / inputs["shares"]
    else:
        valuation_error = "Terminal growth must be below cost of equity."

    return {
        "valid": True,
        "valuation_valid": valuation_valid,
        "valuation_error": valuation_error,
        "inputs": deepcopy(inputs),
        "income": income,
        "balance": balance,
        "cash_flow": cash_flow,
        "checks": checks,
        "equity_value": equity_value,
        "terminal_share": terminal_share,
        "value_per_share": value_per_share,
        "final_operating_profit": income["Operating income"][-1],
        "final_fcfe": cash_flow["FCFE"][-1],
    }


def print_table(title, rows):
    width = max(len(name) for name in rows)
    print(f"\n{title}")
    print(f"{'USD millions':<{width}}" + "".join(f"{year:>12}" for year in YEARS))
    for name, values in rows.items():
        print(f"{name:<{width}}" + "".join(f"{value:>12.1f}" for value in values))


def print_full_result(title, result):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")
    if not result["valid"]:
        print(f"INVALID RUN: {result['error']}")
        return
    print_table("Income statement", result["income"])
    print_table("Balance sheet", result["balance"])
    print_table("Cash flow statement", result["cash_flow"])
    print_table("Checks", result["checks"])
    print("\nValuation")
    if result["valuation_valid"]:
        print(f"Equity value: ${result['equity_value']:.2f} million")
        print(f"Share of value after 2030: {result['terminal_share']:.2%}")
        print(f"Value per share: ${result['value_per_share']:.2f}")
    else:
        print(f"Value per share: unavailable — {result['valuation_error']}")


def input_path(values):
    return ", ".join(f"{year} {value:.1%}" for year, value in zip(YEARS, values))


def signed(value, decimals, dollar=True):
    prefix = "$" if dollar else ""
    return f"{prefix}{value:+,.{decimals}f}"


base_result = run_model(deepcopy(BASE_INPUTS))
print_full_result("BASE CASE — INITIAL RUN", base_result)

results = {}
for driver, specification in SENSITIVITY_DRIVERS.items():
    results[driver] = {}
    for case in ("Lower", "Base", "Higher"):
        fresh_inputs = deepcopy(BASE_INPUTS)
        fresh_inputs[specification["key"]] = deepcopy(specification[case])
        result = run_model(fresh_inputs)
        changed_keys = [
            key for key in BASE_INPUTS if fresh_inputs[key] != BASE_INPUTS[key]
        ]
        expected_keys = [] if case == "Base" else [specification["key"]]
        result["changed_keys"] = changed_keys
        result["input_change_check"] = changed_keys == expected_keys
        results[driver][case] = result

print(f"\n{'=' * 78}\nONE-AT-A-TIME SENSITIVITY ANALYSIS\n{'=' * 78}")
for driver, specification in SENSITIVITY_DRIVERS.items():
    print(f"\n{driver}")
    print(f"Unit: {specification['unit']} | Affected years: {specification['years']}")
    for case in ("Lower", "Base", "Higher"):
        print(f"  {case} input: {input_path(specification[case])}")
    print(
        f"{'Case':<9}{'2030 operating profit':>24}{'Change':>14}"
        f"{'2030 FCFE':>18}{'Change':>14}{'Value/share':>16}{'Change':>12}  Status"
    )
    base = results[driver]["Base"]
    valid = []
    for case in ("Lower", "Base", "Higher"):
        result = results[driver][case]
        if not result["valid"]:
            print(f"{case:<9}{'—':>98}  INVALID: {result['error']}")
            continue
        valid.append(result)
        op_change = result["final_operating_profit"] - base["final_operating_profit"]
        fcfe_change = result["final_fcfe"] - base["final_fcfe"]
        if result["valuation_valid"] and base["valuation_valid"]:
            value_text = f"${result['value_per_share']:,.2f}"
            value_change = signed(result["value_per_share"] - base["value_per_share"], 2)
            status = "valid"
        else:
            value_text = "unavailable"
            value_change = "—"
            status = result["valuation_error"]
        print(
            f"{case:<9}${result['final_operating_profit']:>22,.1f}"
            f"{signed(op_change, 1):>14}  ${result['final_fcfe']:>16,.1f}"
            f"{signed(fcfe_change, 1):>14}{value_text:>16}{value_change:>12}  {status}"
        )
        max_gap = max(abs(value) for value in result["checks"]["Assets - liabilities - equity"])
        minimum_headroom = min(result["checks"]["Cash above minimum"])
        print(
            f"  Checks — maximum absolute balance gap: ${max_gap:.1f} million; "
            f"minimum cash headroom: ${minimum_headroom:.1f} million; "
            f"independent-input audit: {'PASS' if result['input_change_check'] else 'FAIL'}"
        )
    if valid:
        op_values = [result["final_operating_profit"] for result in valid]
        fcfe_values = [result["final_fcfe"] for result in valid]
        valued = [result for result in valid if result["valuation_valid"]]
        print(f"Output span — 2030 operating profit: ${max(op_values) - min(op_values):,.1f} million")
        print(f"Output span — 2030 FCFE: ${max(fcfe_values) - min(fcfe_values):,.1f} million")
        if valued:
            values = [result["value_per_share"] for result in valued]
            print(f"Output span — value per share: ${max(values) - min(values):,.2f} per diluted share")
        else:
            print("Output span — value per share: unavailable; no valid valuations.")

trace_driver, trace_case = TRACE_RUN
print_full_result(
    f"TRACE — {trace_driver}, {trace_case}", results[trace_driver][trace_case]
)

# Restore base independent inputs and rerun the linked model last.
restored_result = run_model(deepcopy(BASE_INPUTS))
print_full_result("BASE CASE — RESTORED FINAL RUN", restored_result)
restored = (
    base_result["valid"] and restored_result["valid"]
    and abs(base_result["final_operating_profit"] - restored_result["final_operating_profit"]) < VALIDATION_TOLERANCE
    and abs(base_result["final_fcfe"] - restored_result["final_fcfe"]) < VALIDATION_TOLERANCE
    and abs(base_result["value_per_share"] - restored_result["value_per_share"]) < VALIDATION_TOLERANCE
)
all_input_checks = all(
    result["input_change_check"]
    for driver_results in results.values()
    for result in driver_results.values()
)
all_accounting_checks = all(
    result["valid"]
    and max(abs(value) for value in result["checks"]["Assets - liabilities - equity"])
        < VALIDATION_TOLERANCE
    and min(result["checks"]["Cash above minimum"]) >= -VALIDATION_TOLERANCE
    for driver_results in results.values()
    for result in driver_results.values()
)
print("\nValidation summary")
print(f"Tolerance: {VALIDATION_TOLERANCE:.6f} USD million / USD per share")
print(f"Base before-and-after match: {'PASS' if restored else 'FAIL'}")
print(f"One-independent-input-only audit: {'PASS' if all_input_checks else 'FAIL'}")
print(f"Accounting checks on every usable run: {'PASS' if all_accounting_checks else 'FAIL'}")
print("Change-from-base formula: changed output minus matching base output")
print("\nCreated for an AI finance class. This is not professional financial advice.")
