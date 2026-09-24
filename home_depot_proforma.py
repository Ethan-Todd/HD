YEARS = [2026, 2027, 2028, 2029, 2030]

# Forecast assumptions
REVENUE_GROWTH = [0.025, 0.025, 0.025, 0.025, 0.025]
GROSS_MARGIN = 0.334
SGA_AS_PERCENT_OF_GROSS_PROFIT = [0.56, 0.56, 0.56, 0.56, 0.56]
DEPRECIATION_AS_PERCENT_OF_OPENING_PPE = 0.122
ANNUAL_IMPAIRMENT = 0.0
ANNUAL_CAPITAL_SPENDING = [4000.0, 4000.0, 4000.0, 4000.0, 4000.0]
TAX_RATE = 0.24
INVENTORY_DAYS = 85.8
ACCOUNTS_PAYABLE_AS_PERCENT_OF_INVENTORY = 0.478
OTHER_WORKING_CAPITAL_AS_PERCENT_OF_REVENUE_CHANGE = 0.008
MINIMUM_CASH = 1500.0
REVOLVER_LIMIT = 11000.0
REVOLVER_RATE = 0.037
DEBT_REPAYMENTS = [4684.0, 3625.0, 3115.0, 3852.0, 2072.0]
TERM_DEBT_RATE = 0.046
QUARTERLY_DIVIDEND_PER_SHARE = 2.33
DIVIDEND_GROWTH = 0.025
ANNUAL_SHARE_BUYBACK = [0.0, 0.0, 0.0, 0.0, 0.0]
COST_OF_EQUITY = 0.09
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 995.0

# Opening balance sheet at February 1, 2026, and FY2025 revenue; USD millions
OPENING_REVENUE = 164683.0
OPENING_CASH = 1389.0
OPENING_INVENTORY = 25817.0
OPENING_PPE = 28021.0
OPENING_OTHER_ASSETS = 49868.0
OPENING_ACCOUNTS_PAYABLE = 11491.0
OPENING_TERM_DEBT = 51308.0
OPENING_REVOLVER = 4464.0
OPENING_OTHER_LIABILITIES = 25019.0
OPENING_EQUITY = 12813.0


def assert_balanced(year, assets, liabilities_and_equity, cash):
    gap = assets - liabilities_and_equity
    if abs(gap) > 0.000001:
        raise ValueError(f"{year} balance-sheet check failed; gap = {gap:.6f}")
    if cash < MINIMUM_CASH - 0.000001:
        shortfall = MINIMUM_CASH - cash
        raise ValueError(f"{year} minimum-cash check failed; gap = {shortfall:.6f}")


def print_table(title, rows):
    label_width = max(len(label) for label, _ in rows)
    print(f"\n{title}")
    print(f"{'USD millions':<{label_width}}" + "".join(f"{year:>12}" for year in YEARS))
    for label, values in rows:
        print(f"{label:<{label_width}}" + "".join(f"{value:>12.1f}" for value in values))


income_statement = {
    "Revenue": [],
    "Gross profit": [],
    "SG&A": [],
    "Depreciation": [],
    "Impairment": [],
    "Operating income": [],
    "Interest expense": [],
    "Pretax income": [],
    "Tax": [],
    "Net income": [],
}

balance_sheet = {
    "Cash": [],
    "Inventory": [],
    "PP&E": [],
    "Other assets": [],
    "Total assets": [],
    "Accounts payable": [],
    "Term debt": [],
    "Revolver / commercial paper": [],
    "Other liabilities": [],
    "Equity": [],
    "Liabilities and equity": [],
}

cash_flow_statement = {
    "Net income": [],
    "Depreciation": [],
    "Impairment": [],
    "Capital spending": [],
    "Change in inventory": [],
    "Change in other working capital": [],
    "Change in accounts payable": [],
    "Debt repayment": [],
    "FCFE": [],
    "Dividends": [],
    "Share buyback": [],
    "Change in revolver": [],
    "Ending cash": [],
}

checks = {
    "Assets - liabilities - equity": [],
    "Cash above minimum": [],
}

prior_revenue = OPENING_REVENUE
opening_cash = OPENING_CASH
opening_inventory = OPENING_INVENTORY
opening_ppe = OPENING_PPE
opening_other_assets = OPENING_OTHER_ASSETS
opening_accounts_payable = OPENING_ACCOUNTS_PAYABLE
opening_term_debt = OPENING_TERM_DEBT
opening_revolver = OPENING_REVOLVER
opening_other_liabilities = OPENING_OTHER_LIABILITIES
opening_equity = OPENING_EQUITY

for index, year in enumerate(YEARS):
    revenue = prior_revenue * (1.0 + REVENUE_GROWTH[index])
    change_in_revenue = revenue - prior_revenue
    gross_profit = revenue * GROSS_MARGIN
    cost_of_sales = revenue - gross_profit
    sga = gross_profit * SGA_AS_PERCENT_OF_GROSS_PROFIT[index]
    depreciation = opening_ppe * DEPRECIATION_AS_PERCENT_OF_OPENING_PPE
    impairment = ANNUAL_IMPAIRMENT
    operating_income = gross_profit - sga - depreciation - impairment
    interest_expense = (
        opening_term_debt * TERM_DEBT_RATE
        + opening_revolver * REVOLVER_RATE
    )
    pretax_income = operating_income - interest_expense
    tax = max(0.0, pretax_income) * TAX_RATE
    net_income = pretax_income - tax

    inventory = cost_of_sales * INVENTORY_DAYS / 365.0
    accounts_payable = inventory * ACCOUNTS_PAYABLE_AS_PERCENT_OF_INVENTORY
    ppe = opening_ppe + ANNUAL_CAPITAL_SPENDING[index] - depreciation
    change_in_other_working_capital = (
        OTHER_WORKING_CAPITAL_AS_PERCENT_OF_REVENUE_CHANGE * change_in_revenue
    )
    other_assets = opening_other_assets + change_in_other_working_capital - impairment
    debt_repayment = min(DEBT_REPAYMENTS[index], opening_term_debt)
    term_debt = opening_term_debt - debt_repayment
    other_liabilities = opening_other_liabilities

    dividend_per_share = QUARTERLY_DIVIDEND_PER_SHARE * 4.0 * (1.0 + DIVIDEND_GROWTH) ** index
    dividends = dividend_per_share * SHARES_OUTSTANDING
    share_buyback = ANNUAL_SHARE_BUYBACK[index]
    equity = opening_equity + net_income - dividends - share_buyback

    change_in_inventory = inventory - opening_inventory
    change_in_accounts_payable = accounts_payable - opening_accounts_payable
    fcfe = (
        net_income
        + depreciation
        + impairment
        - ANNUAL_CAPITAL_SPENDING[index]
        - change_in_inventory
        - change_in_other_working_capital
        + change_in_accounts_payable
        - debt_repayment
    )

    cash_before_revolver = opening_cash + fcfe - dividends - share_buyback
    revolver = opening_revolver
    if cash_before_revolver < MINIMUM_CASH:
        draw = min(MINIMUM_CASH - cash_before_revolver, REVOLVER_LIMIT - opening_revolver)
        revolver += draw
    else:
        repayment = min(cash_before_revolver - MINIMUM_CASH, opening_revolver)
        revolver -= repayment

    change_in_revolver = revolver - opening_revolver
    cash = cash_before_revolver + change_in_revolver

    total_assets = cash + inventory + ppe + other_assets
    liabilities_and_equity = (
        accounts_payable
        + term_debt
        + revolver
        + other_liabilities
        + equity
    )
    balance_gap = total_assets - liabilities_and_equity
    assert_balanced(year, total_assets, liabilities_and_equity, cash)

    for label, value in (
        ("Revenue", revenue), ("Gross profit", gross_profit), ("SG&A", sga),
        ("Depreciation", depreciation), ("Impairment", impairment),
        ("Operating income", operating_income), ("Interest expense", interest_expense),
        ("Pretax income", pretax_income), ("Tax", tax), ("Net income", net_income),
    ):
        income_statement[label].append(value)

    for label, value in (
        ("Cash", cash), ("Inventory", inventory), ("PP&E", ppe),
        ("Other assets", other_assets), ("Total assets", total_assets),
        ("Accounts payable", accounts_payable), ("Term debt", term_debt),
        ("Revolver / commercial paper", revolver),
        ("Other liabilities", other_liabilities), ("Equity", equity),
        ("Liabilities and equity", liabilities_and_equity),
    ):
        balance_sheet[label].append(value)

    for label, value in (
        ("Net income", net_income), ("Depreciation", depreciation),
        ("Impairment", impairment), ("Capital spending", -ANNUAL_CAPITAL_SPENDING[index]),
        ("Change in inventory", -change_in_inventory),
        ("Change in other working capital", -change_in_other_working_capital),
        ("Change in accounts payable", change_in_accounts_payable),
        ("Debt repayment", -debt_repayment), ("FCFE", fcfe),
        ("Dividends", -dividends), ("Share buyback", -share_buyback),
        ("Change in revolver", change_in_revolver), ("Ending cash", cash),
    ):
        cash_flow_statement[label].append(value)

    checks["Assets - liabilities - equity"].append(balance_gap)
    checks["Cash above minimum"].append(cash - MINIMUM_CASH)

    prior_revenue = revenue
    opening_cash = cash
    opening_inventory = inventory
    opening_ppe = ppe
    opening_other_assets = other_assets
    opening_accounts_payable = accounts_payable
    opening_term_debt = term_debt
    opening_revolver = revolver
    opening_other_liabilities = other_liabilities
    opening_equity = equity

print_table("Income statement", list(income_statement.items()))
print_table("Balance sheet", list(balance_sheet.items()))
print_table("Cash flow statement", list(cash_flow_statement.items()))
print_table("Checks", list(checks.items()))

if COST_OF_EQUITY <= TERMINAL_GROWTH:
    raise ValueError("Terminal growth must be less than the cost of equity.")

for year, fcfe in zip(YEARS, cash_flow_statement["FCFE"]):
    if fcfe < 0.0:
        print(f"Negative FCFE: {year} (${fcfe:.1f} million)")

present_value_of_positive_fcfe = sum(
    max(0.0, fcfe) / (1.0 + COST_OF_EQUITY) ** year_number
    for year_number, fcfe in enumerate(cash_flow_statement["FCFE"], start=1)
)
normalized_2030_fcfe = cash_flow_statement["FCFE"][-1] + DEBT_REPAYMENTS[-1]
if normalized_2030_fcfe <= 0.0:
    raise ValueError(
        "No terminal value: a negative sustainable cash flow cannot support "
        "a meaningful Gordon-growth value."
    )

terminal_value = (
    normalized_2030_fcfe
    * (1.0 + TERMINAL_GROWTH)
    / (COST_OF_EQUITY - TERMINAL_GROWTH)
)
present_value_of_terminal_value = terminal_value / (1.0 + COST_OF_EQUITY) ** 5
equity_value = present_value_of_positive_fcfe + present_value_of_terminal_value
share_of_value_after_2030 = present_value_of_terminal_value / equity_value
value_per_share = equity_value / SHARES_OUTSTANDING

print("\nValuation")
print(f"Equity value: ${equity_value:.2f} million")
print(f"Share of value after 2030: {share_of_value_after_2030:.2%}")
print(f"Value per share: ${value_per_share:.2f}")
print(
    f"The ${value_per_share:.2f} value comes from the forecast operating margins, "
    "working-capital needs, capital spending, debt repayments, and the 9.0% cost of equity."
)
print(
    "It would change most if revenue growth, SG&A efficiency, the cost of equity, "
    "terminal growth, or the assumed refinancing of debt changed."
)
print("\nCreated for an AI finance class. This is not professional financial advice.")
