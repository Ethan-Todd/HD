YEARS = [2026, 2027, 2028, 2029, 2030]

# Forecast assumptions
ORGANIC_REVENUE_GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_AS_PERCENT_OF_GROSS_PROFIT = [0.665, 0.655, 0.645, 0.645, 0.645]
DEPRECIATION_AS_PERCENT_OF_OPENING_PPE = 82.4 / 3070.4
ANNUAL_IMPAIRMENT = 120.0
ANNUAL_CAPITAL_SPENDING = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365.0
FLOOR_PLAN_AS_PERCENT_OF_INVENTORY = 2027.0 / 2135.8
OTHER_WORKING_CAPITAL_AS_PERCENT_OF_REVENUE_CHANGE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
ANNUAL_DEBT_REPAYMENT = 150.0
ANNUAL_SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

# Opening balance sheet and income-statement base, USD millions
OPENING_REVENUE = 17999.0
OPENING_INVENTORY = 2135.8
OPENING_PPE = 3070.4
OPENING_OTHER_ASSETS = 6371.6
OPENING_CASH = 40.4
OPENING_FLOOR_PLAN = 2027.0
OPENING_TERM_DEBT = 3572.0
OPENING_OTHER_LIABILITIES = 2127.5
OPENING_EQUITY = 3891.7
OPENING_REVOLVER = 0.0


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
    "Floor plan": [],
    "Term debt": [],
    "Revolver": [],
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
    "Change in floor plan": [],
    "Debt repayment": [],
    "FCFE": [],
    "Share buyback": [],
    "Change in revolver": [],
    "Ending cash": [],
}

checks = {
    "Assets - liabilities - equity": [],
    "Cash above minimum": [],
}

prior_revenue = OPENING_REVENUE
opening_inventory = OPENING_INVENTORY
opening_ppe = OPENING_PPE
opening_other_assets = OPENING_OTHER_ASSETS
opening_cash = OPENING_CASH
opening_floor_plan = OPENING_FLOOR_PLAN
opening_term_debt = OPENING_TERM_DEBT
opening_other_liabilities = OPENING_OTHER_LIABILITIES
opening_equity = OPENING_EQUITY
opening_revolver = OPENING_REVOLVER

for index, year in enumerate(YEARS):
    revenue = prior_revenue * (1.0 + ORGANIC_REVENUE_GROWTH)
    change_in_revenue = revenue - prior_revenue
    gross_profit = revenue * GROSS_MARGIN
    sga = gross_profit * SGA_AS_PERCENT_OF_GROSS_PROFIT[index]
    depreciation = opening_ppe * DEPRECIATION_AS_PERCENT_OF_OPENING_PPE
    impairment = ANNUAL_IMPAIRMENT
    operating_income = gross_profit - sga - depreciation - impairment
    interest_expense = (
        opening_floor_plan * FLOOR_PLAN_RATE
        + opening_term_debt * TERM_DEBT_RATE
        + opening_revolver * REVOLVER_RATE
    )
    pretax_income = operating_income - interest_expense
    tax = max(0.0, pretax_income) * TAX_RATE
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365.0
    floor_plan = inventory * FLOOR_PLAN_AS_PERCENT_OF_INVENTORY
    ppe = opening_ppe + ANNUAL_CAPITAL_SPENDING - depreciation
    change_in_other_working_capital = (
        OTHER_WORKING_CAPITAL_AS_PERCENT_OF_REVENUE_CHANGE * change_in_revenue
    )
    other_assets = (
        opening_other_assets + change_in_other_working_capital - impairment
    )
    debt_repayment = min(ANNUAL_DEBT_REPAYMENT, opening_term_debt)
    term_debt = opening_term_debt - debt_repayment
    other_liabilities = opening_other_liabilities
    share_buyback = min(ANNUAL_SHARE_BUYBACK, opening_equity + net_income)
    equity = opening_equity + net_income - share_buyback

    change_in_inventory = inventory - opening_inventory
    change_in_floor_plan = floor_plan - opening_floor_plan
    fcfe = (
        net_income
        + depreciation
        + impairment
        - ANNUAL_CAPITAL_SPENDING
        - change_in_inventory
        - change_in_other_working_capital
        + change_in_floor_plan
        - debt_repayment
    )

    cash_before_revolver = opening_cash + fcfe - share_buyback
    revolver = opening_revolver

    if cash_before_revolver < MINIMUM_CASH:
        revolver_draw = min(MINIMUM_CASH - cash_before_revolver, REVOLVER_LIMIT - opening_revolver)
        revolver += revolver_draw
    else:
        revolver_repayment = min(cash_before_revolver - MINIMUM_CASH, opening_revolver)
        revolver -= revolver_repayment

    change_in_revolver = revolver - opening_revolver
    cash = cash_before_revolver + change_in_revolver

    total_assets = cash + inventory + ppe + other_assets
    liabilities_and_equity = (
        floor_plan + term_debt + revolver + other_liabilities + equity
    )
    balance_gap = total_assets - liabilities_and_equity

    assert_balanced(year, total_assets, liabilities_and_equity, cash)

    income_statement["Revenue"].append(revenue)
    income_statement["Gross profit"].append(gross_profit)
    income_statement["SG&A"].append(sga)
    income_statement["Depreciation"].append(depreciation)
    income_statement["Impairment"].append(impairment)
    income_statement["Operating income"].append(operating_income)
    income_statement["Interest expense"].append(interest_expense)
    income_statement["Pretax income"].append(pretax_income)
    income_statement["Tax"].append(tax)
    income_statement["Net income"].append(net_income)

    balance_sheet["Cash"].append(cash)
    balance_sheet["Inventory"].append(inventory)
    balance_sheet["PP&E"].append(ppe)
    balance_sheet["Other assets"].append(other_assets)
    balance_sheet["Total assets"].append(total_assets)
    balance_sheet["Floor plan"].append(floor_plan)
    balance_sheet["Term debt"].append(term_debt)
    balance_sheet["Revolver"].append(revolver)
    balance_sheet["Other liabilities"].append(other_liabilities)
    balance_sheet["Equity"].append(equity)
    balance_sheet["Liabilities and equity"].append(liabilities_and_equity)

    cash_flow_statement["Net income"].append(net_income)
    cash_flow_statement["Depreciation"].append(depreciation)
    cash_flow_statement["Impairment"].append(impairment)
    cash_flow_statement["Capital spending"].append(-ANNUAL_CAPITAL_SPENDING)
    cash_flow_statement["Change in inventory"].append(-change_in_inventory)
    cash_flow_statement["Change in other working capital"].append(
        -change_in_other_working_capital
    )
    cash_flow_statement["Change in floor plan"].append(change_in_floor_plan)
    cash_flow_statement["Debt repayment"].append(-debt_repayment)
    cash_flow_statement["FCFE"].append(fcfe)
    cash_flow_statement["Share buyback"].append(-share_buyback)
    cash_flow_statement["Change in revolver"].append(change_in_revolver)
    cash_flow_statement["Ending cash"].append(cash)

    checks["Assets - liabilities - equity"].append(balance_gap)
    checks["Cash above minimum"].append(cash - MINIMUM_CASH)

    prior_revenue = revenue
    opening_inventory = inventory
    opening_ppe = ppe
    opening_other_assets = other_assets
    opening_cash = cash
    opening_floor_plan = floor_plan
    opening_term_debt = term_debt
    opening_other_liabilities = other_liabilities
    opening_equity = equity
    opening_revolver = revolver

print_table("Income statement", list(income_statement.items()))
print_table("Balance sheet", list(balance_sheet.items()))
print_table("Cash flow statement", list(cash_flow_statement.items()))
print_table("Checks", list(checks.items()))

if COST_OF_EQUITY <= TERMINAL_GROWTH:
    raise ValueError("Terminal growth must be less than the cost of equity.")

present_value_of_fcfe = sum(
    fcfe / (1.0 + COST_OF_EQUITY) ** year_number
    for year_number, fcfe in enumerate(cash_flow_statement["FCFE"], start=1)
)
normalized_2030_fcfe = (
    cash_flow_statement["FCFE"][-1]
    + min(ANNUAL_DEBT_REPAYMENT, balance_sheet["Term debt"][-2])
)
terminal_value = (
    normalized_2030_fcfe
    * (1.0 + TERMINAL_GROWTH)
    / (COST_OF_EQUITY - TERMINAL_GROWTH)
)
present_value_of_terminal_value = terminal_value / (1.0 + COST_OF_EQUITY) ** 5
equity_value = present_value_of_fcfe + present_value_of_terminal_value
share_of_value_after_2030 = present_value_of_terminal_value / equity_value
value_per_share = equity_value / SHARES_OUTSTANDING

print("\nValuation")
print(f"Equity value: ${equity_value:.2f} million")
print(f"Share of value after 2030: {share_of_value_after_2030:.2%}")
print(f"Value per share: ${value_per_share:.2f}")
print("\nCreated for an AI finance class. This is not professional financial advice.")
