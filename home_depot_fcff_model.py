"""Home Depot linked pro-forma and provisional FCFF/WACC DCF.

Standard library only. USD millions except per-share values.
Educational AI finance class work; not professional financial advice.
"""
from copy import deepcopy
import sys

YEARS = [2026, 2027, 2028, 2029, 2030]
TOLERANCE = 0.000001

# Reported FY2025, before normalization. 10-K pp. 39, 40, 43; Notes 3-5.
REPORTED = {
    "revenue":164683., "cogs":109818., "gross_profit":54865., "sga":30702.,
    "presented_da":3273., "ebit":20890., "interest_other":-124.,
    "interest":2412., "pretax":18602., "tax":4446., "net_income":14156.,
    "cfo":16325., "cfi":-8980., "cff":-7714., "cash_change":-369.,
    "fx":99., "cash_begin":1659., "cash":1389., "ppe_depreciation":3514.,
    "intangible_amortization":607., "capex":3679., "acquisitions":5410.,
    "receivables":5597., "inventory":25817., "other_current_assets":1588.,
    "ppe":28021., "lease_assets":9204., "goodwill":22344.,
    "intangibles":10329., "other_noncurrent_assets":806., "total_assets":105095.,
    "commercial_paper":4464., "accounts_payable":11491., "accrued_salaries":2529.,
    "sales_taxes":508., "deferred_revenue":2575., "income_taxes_payable":114.,
    "current_debt":4967., "current_lease_liability":1418., "other_accrued":4358.,
    "noncurrent_debt":46341., "noncurrent_lease_liability":8160.,
    "deferred_taxes":2845., "other_long_term_liabilities":2512.,
    "equity":12813., "total_liabilities_equity":105095.,
}

BASE_INPUTS = {
    "growth":[0.025]*5, "gross_margin":[0.334]*5, "sga_gp":[0.560]*5,
    "presented_da_ppe":3273/28021, "ppe_depreciation_ppe":3514/28021,
    "amortization_intangibles":607/10329, "capex":[4000.]*5,
    "tax_rate":4446/18602, "receivables_revenue":5597/164683,
    "inventory_days":25817/109818*365, "oca_revenue":1588/164683,
    "ap_inventory":11491/25817, "salaries_revenue":2529/164683,
    "sales_tax_revenue":508/164683, "deferred_revenue_ratio":2575/164683,
    "income_tax_payable_revenue":114/164683, "other_accrued_revenue":4358/164683,
    "minimum_cash":1500., "cp_limit":11000., "cp_rate":0.037,
    "debt_rate":0.046, "debt_repayments":[4684.,3625.,3115.,3852.,2072.],
    "quarterly_dividend":2.33, "dividend_growth":0.025, "shares":999.689626,
    "wacc":0.08198434559001862, "terminal_growth":0.025,
}

VALUATION = {
    "price":319.77, "rf":0.0479, "erp":0.0414, "beta":1.00,
    "debt_cost":0.04395038097692053, "tax_rate":0.24663299663299662,
    "shares":999.689626, "reported_cash":2085., "excess_cash":0.,
    "cp":4248., "current_debt":4697., "noncurrent_debt":43951.,
    "finance_lease_current":303., "finance_lease_noncurrent":2791.,
    "operating_lease_current":1516., "operating_lease_noncurrent":8155.,
    "notes_fair_value":39859., "notes_carrying":44905.,
}

def near_zero(x): return abs(x) <= TOLERANCE

def bridge_debt():
    return VALUATION["cp"] + VALUATION["current_debt"] + VALUATION["noncurrent_debt"]

def calculate_wacc():
    b = VALUATION
    ke = b["rf"] + b["beta"] * b["erp"]
    equity = b["price"] * b["shares"]
    other_debt = b["current_debt"] + b["noncurrent_debt"] - b["notes_carrying"]
    debt = b["notes_fair_value"] + other_debt + b["cp"]
    ew = equity / (equity + debt); dw = 1 - ew
    return ew*ke + dw*b["debt_cost"]*(1-b["tax_rate"]), ke, equity, debt, ew, dw

def historical_checks():
    h = REPORTED
    assets = sum(h[k] for k in ("cash","receivables","inventory","other_current_assets",
        "ppe","lease_assets","goodwill","intangibles","other_noncurrent_assets"))
    le = sum(h[k] for k in ("commercial_paper","accounts_payable","accrued_salaries",
        "sales_taxes","deferred_revenue","income_taxes_payable","current_debt",
        "current_lease_liability","other_accrued","noncurrent_debt",
        "noncurrent_lease_liability","deferred_taxes","other_long_term_liabilities","equity"))
    return {
        "Gross profit from components":h["gross_profit"]-(h["revenue"]-h["cogs"]),
        "Operating income from components":h["ebit"]-(h["gross_profit"]-h["sga"]-h["presented_da"]),
        "Pretax income from components":h["pretax"]-(h["ebit"]-h["interest"]-h["interest_other"]),
        "Net income from components":h["net_income"]-(h["pretax"]-h["tax"]),
        "D&A from separate addbacks":h["ppe_depreciation"]+h["intangible_amortization"]-4121,
        "Individual assets sum":assets-h["total_assets"],
        "Individual liabilities and equity sum":le-h["total_liabilities_equity"],
        "Balance sheet equation":h["total_assets"]-h["total_liabilities_equity"],
        "CFO + CFI + CFF":h["cfo"]+h["cfi"]+h["cff"]-h["cash_change"],
        "Cash rollforward including FX":h["cash"]-(h["cash_begin"]+h["cash_change"]+h["fx"]),
        "Long-term debt components":h["current_debt"]+h["noncurrent_debt"]-51308,
        "Financing debt components":h["commercial_paper"]+h["current_debt"]+h["noncurrent_debt"]-55772,
    }

def opening_state(): return deepcopy(REPORTED)

def operating_nwc(s):
    return (s["receivables"]+s["inventory"]+s["other_current_assets"]
        -s["accounts_payable"]-s["accrued_salaries"]-s["sales_taxes"]
        -s["deferred_revenue"]-s["income_taxes_payable"]-s["other_accrued"])

def run_forecast(i):
    names = ("Revenue","Operating income","PP&E depreciation","Intangible amortization",
        "Total D&A","Operating NWC","Change in operating NWC","FCFF","Cash",
        "Receivables","Inventory","Other current assets","PP&E","Lease assets",
        "Goodwill","Intangibles","Other noncurrent assets","Total assets",
        "Accounts payable","Term debt","Commercial paper","Lease liabilities",
        "Equity","Liabilities and equity","Operating cash flow","Investing cash flow",
        "Financing cash flow","Net cash change","Cash-flow-to-cash gap","Balance-sheet gap")
    rows = {n:[] for n in names}; s = opening_state()
    for x, year in enumerate(YEARS):
        opening_cash=s["cash"]; old_nwc=operating_nwc(s)
        revenue=s["revenue"]*(1+i["growth"][x]); gp=revenue*i["gross_margin"][x]
        cogs=revenue-gp; sga=gp*i["sga_gp"][x]
        presented_da=s["ppe"]*i["presented_da_ppe"]
        depreciation=s["ppe"]*i["ppe_depreciation_ppe"]
        amortization=s["intangibles"]*i["amortization_intangibles"]
        total_da=depreciation+amortization; ebit=gp-sga-presented_da
        interest=s["current_debt"]*0 + (s["current_debt"]+s["noncurrent_debt"])*i["debt_rate"]+s["commercial_paper"]*i["cp_rate"]
        pretax=ebit-interest; tax=max(0,pretax)*i["tax_rate"]; ni=pretax-tax
        p={
            "receivables":revenue*i["receivables_revenue"],
            "inventory":cogs*i["inventory_days"]/365,
            "other_current_assets":revenue*i["oca_revenue"],
            "accrued_salaries":revenue*i["salaries_revenue"],
            "sales_taxes":revenue*i["sales_tax_revenue"],
            "deferred_revenue":revenue*i["deferred_revenue_ratio"],
            "income_taxes_payable":revenue*i["income_tax_payable_revenue"],
            "other_accrued":revenue*i["other_accrued_revenue"],
        }
        p["accounts_payable"]=p["inventory"]*i["ap_inventory"]
        new_nwc=operating_nwc(p); dnwc=new_nwc-old_nwc
        ppe=s["ppe"]+i["capex"][x]-depreciation
        intangibles=max(0,s["intangibles"]-amortization)
        repayment=min(i["debt_repayments"][x],s["current_debt"]+s["noncurrent_debt"])
        term_debt=s["current_debt"]+s["noncurrent_debt"]-repayment
        dividend=i["quarterly_dividend"]*4*(1+i["dividend_growth"])**x*i["shares"]
        equity=s["equity"]+ni-dividend
        fcff=ebit*(1-i["tax_rate"])+total_da-i["capex"][x]-dnwc
        ocf=ni+total_da-dnwc; investing=-i["capex"][x]; financing_pre=-repayment-dividend
        cp=s["commercial_paper"]; cash_pre=opening_cash+ocf+investing+financing_pre
        if cash_pre<i["minimum_cash"]: cp+=min(i["minimum_cash"]-cash_pre,i["cp_limit"]-cp)
        else: cp-=min(cash_pre-i["minimum_cash"],cp)
        financing=financing_pre+cp-s["commercial_paper"]
        cash_change=ocf+investing+financing; cash=opening_cash+cash_change
        lease_liab=s["current_lease_liability"]+s["noncurrent_lease_liability"]
        other_lt=s["deferred_taxes"]+s["other_long_term_liabilities"]
        assets=sum((cash,p["receivables"],p["inventory"],p["other_current_assets"],ppe,
            s["lease_assets"],s["goodwill"],intangibles,s["other_noncurrent_assets"]))
        le=sum((cp,p["accounts_payable"],p["accrued_salaries"],p["sales_taxes"],
            p["deferred_revenue"],p["income_taxes_payable"],p["other_accrued"],term_debt,
            lease_liab,other_lt,equity))
        cash_gap=cash-(opening_cash+cash_change); bs_gap=assets-le
        if not near_zero(cash_gap): raise ValueError(f"{year} cash-flow-to-cash gap {cash_gap:.6f}")
        if not near_zero(bs_gap): raise ValueError(f"{year} balance-sheet gap {bs_gap:.6f}")
        if cash<i["minimum_cash"]-TOLERANCE: raise ValueError(f"{year} minimum-cash failure")
        vals=(revenue,ebit,depreciation,amortization,total_da,new_nwc,dnwc,fcff,cash,
            p["receivables"],p["inventory"],p["other_current_assets"],ppe,s["lease_assets"],
            s["goodwill"],intangibles,s["other_noncurrent_assets"],assets,p["accounts_payable"],
            term_debt,cp,lease_liab,equity,le,ocf,investing,financing,cash_change,cash_gap,bs_gap)
        for n,v in zip(names,vals): rows[n].append(v)
        s.update(p); s.update({"revenue":revenue,"cash":cash,"ppe":ppe,"intangibles":intangibles,
            "commercial_paper":cp,"current_debt":0.,"noncurrent_debt":term_debt,"equity":equity})
    return rows

def value_fcff(fcff,wacc,g,cash=None,debt=None,shares=None):
    if g>=wacc: return None
    debt=bridge_debt() if debt is None else debt
    cash=VALUATION["excess_cash"] if cash is None else cash
    shares=VALUATION["shares"] if shares is None else shares
    if shares<=0: return None
    explicit=sum(v/(1+wacc)**t for t,v in enumerate(fcff,1))
    tv=fcff[-1]*(1+g)/(wacc-g); tvpv=tv/(1+wacc)**5; ev=explicit+tvpv
    equity=ev+cash-debt
    return {"explicit_pv":explicit,"terminal_pv":tvpv,"enterprise_value":ev,"cash":cash,
        "debt":debt,"equity_value":equity,"value_per_share":equity/shares,"terminal_share":tvpv/ev}

def prow(label, values): print(f"{label:<34}"+"".join(f"{v:>13,.1f}" for v in values))

def record(name, passed, tests):
    tests[name]=bool(passed); print(f"{name}: {'PASS' if passed else 'FAIL'}")

def main():
    tests={}; hc=historical_checks()
    print("FY2025 REPORTED FILING RECONCILIATION")
    for n,gap in hc.items(): print(f"{n}: {'PASS' if near_zero(gap) else 'FAIL'} (gap {gap:.6f})")
    tests["Historical reconciliation"]=all(near_zero(g) for g in hc.values())
    print("\nNORMALIZATION: reported FY2025 unchanged; unresolved adjustments remain separate.")
    wacc,ke,me,md,ew,dw=calculate_wacc()
    print("\nSEPTEMBER 1, 2026 WACC (PROVISIONAL)")
    print(f"Cost of equity {ke:.4%}; market equity ${me:,.1f}; market debt ${md:,.1f}")
    print(f"Weights {ew:.4%}/{dw:.4%}; calculated WACC {wacc:.4%}")
    record("Calculated WACC equals BASE_INPUTS['wacc']",abs(wacc-BASE_INPUTS["wacc"])<=TOLERANCE,tests)
    f=run_forecast(deepcopy(BASE_INPUTS))
    print("\nLINKED FIVE-YEAR PRO-FORMA AND FCFF")
    print(f"{'USD millions':<34}"+"".join(f"{y:>13}" for y in YEARS))
    for n in ("Revenue","Operating income","PP&E depreciation","Intangible amortization",
        "Total D&A","Operating NWC","Change in operating NWC","FCFF","Cash","Receivables",
        "Inventory","PP&E","Goodwill","Intangibles","Lease assets","Total assets",
        "Liabilities and equity","Operating cash flow","Investing cash flow","Financing cash flow",
        "Cash-flow-to-cash gap","Balance-sheet gap"): prow(n,f[n])
    v=value_fcff(f["FCFF"],BASE_INPUTS["wacc"],BASE_INPUTS["terminal_growth"])
    print("\nCURRENT REBUILT RESULT — PROVISIONAL")
    for label,key in (("Enterprise value","enterprise_value"),("Excess cash","cash"),
        ("Financing debt","debt"),("Equity value","equity_value")):
        print(f"{label}: ${v[key]:,.1f} million")
    print(f"Value per diluted share: ${v['value_per_share']:.2f}")
    print(f"Terminal-value share: {v['terminal_share']:.1%}")
    old_basis=value_fcff(f["FCFF"],.088,.025,1389.,55772.,995.)
    share_step=value_fcff(f["FCFF"],.088,.025,1389.,55772.,VALUATION["shares"])
    debt_step=value_fcff(f["FCFF"],.088,.025,1389.,bridge_debt(),VALUATION["shares"])
    cash_step=value_fcff(f["FCFF"],.088,.025,0.,bridge_debt(),VALUATION["shares"])
    print("\nRECONCILIATION FROM DOCUMENTED PART 1 RESULT")
    print("Archived Part 1 result (not reproduced): $207.85")
    waterfall=(("Current schedules at old valuation basis",old_basis),
        ("Valuation-date diluted shares",share_step),("Latest public debt",debt_step),
        ("Zero excess-cash convention",cash_step),("Calculated provisional WACC",v))
    prior=207.85
    for label,result in waterfall:
        current=result["value_per_share"]
        print(f"{label:<42}${current:>8.2f}  change {current-prior:+.2f}")
        prior=current
    print("\nVALIDATION SUMMARY")
    record("Forecast balance sheet balances",all(near_zero(x) for x in f["Balance-sheet gap"]),tests)
    record("Forecast cash flow ties to cash",all(near_zero(x) for x in f["Cash-flow-to-cash gap"]),tests)
    neg=deepcopy(f["FCFF"]); neg[0]=-100.; zero=deepcopy(neg); zero[0]=0.
    delta=value_fcff(zero,wacc,.025)["enterprise_value"]-value_fcff(neg,wacc,.025)["enterprise_value"]
    record("Signed negative FCFF reduces value",near_zero(delta-100/(1+wacc)),tests)
    low=value_fcff(f["FCFF"],wacc,.025,debt=50000)["equity_value"]
    high=value_fcff(f["FCFF"],wacc,.025,debt=51000)["equity_value"]
    record("Debt increase reduces equity dollar for dollar",near_zero((low-high)-1000),tests)
    record("DCF monotonicity",value_fcff(f["FCFF"],.072,.025)["value_per_share"]>value_fcff(f["FCFF"],.092,.025)["value_per_share"] and value_fcff(f["FCFF"],wacc,.03)["value_per_share"]>value_fcff(f["FCFF"],wacc,.02)["value_per_share"],tests)
    record("Enterprise-to-equity bridge",near_zero(v["equity_value"]-(v["enterprise_value"]+v["cash"]-v["debt"])),tests)
    leases=VALUATION["finance_lease_current"]+VALUATION["finance_lease_noncurrent"]
    record("Finance leases included once",leases==3094 and v["debt"]==bridge_debt(),tests)
    print("\nUNRESOLVED: dated beta; marginal debt cost/tax; excess-cash evidence; exact diluted")
    print("shares; detailed operating-lease rollforward; forecast and normalization evidence.")
    print("Created for an AI finance class. This is not professional financial advice.")
    failed=[n for n,p in tests.items() if not p]
    if failed:
        print("FAILED REQUIRED VALIDATIONS:",", ".join(failed)); return 1
    return 0

if __name__=="__main__": sys.exit(main())
