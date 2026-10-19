"""Part 3 scenarios, comparable valuation, and decision tests.

Standard library only. USD millions except per-share values.
Educational AI finance class work; not professional financial advice.
"""
from copy import deepcopy
from pathlib import Path
import sys

import home_depot_fcff_model as model

OUT = []


def emit(line=""):
    OUT.append(line)
    print(line)


def scenario_inputs(organic, acquisition, gross_margin, sga_gp, capex):
    inputs = deepcopy(model.BASE_INPUTS)
    inputs["growth"] = [a + b for a, b in zip(organic, acquisition)]
    inputs["gross_margin"] = list(gross_margin)
    inputs["sga_gp"] = list(sga_gp)
    inputs["capex"] = list(capex)
    return inputs


SCENARIOS = {
    "Downside": {
        "organic": [0.000, 0.005, 0.015, 0.020, 0.020],
        "acquisition": [0.025, 0.005, 0.000, 0.000, 0.000],
        "gross_margin": [0.331, 0.330, 0.330, 0.331, 0.332],
        "sga_gp": [0.570, 0.570, 0.565, 0.560, 0.560],
        "capex": [4200.0, 4200.0, 4100.0, 4100.0, 4100.0],
        "cause": "Housing affordability keeps big projects weak; fixed-cost deleverage and input costs pressure margins while committed capability spending continues.",
    },
    "Base": {
        "organic": [0.010, 0.020, 0.025, 0.025, 0.025],
        "acquisition": [0.025, 0.005, 0.000, 0.000, 0.000],
        "gross_margin": [0.331, 0.332, 0.333, 0.334, 0.334],
        "sga_gp": [0.565, 0.560, 0.560, 0.560, 0.560],
        "capex": [4200.0, 4200.0, 4200.0, 4200.0, 4200.0],
        "cause": "FY2026 uses the midpoint of total-sales and comparable-sales guidance; acquired/new capacity fades as organic repair-and-remodel demand normalizes.",
    },
    "Upside": {
        "organic": [0.020, 0.030, 0.030, 0.030, 0.030],
        "acquisition": [0.025, 0.005, 0.000, 0.000, 0.000],
        "gross_margin": [0.331, 0.333, 0.335, 0.336, 0.336],
        "sga_gp": [0.555, 0.550, 0.545, 0.545, 0.545],
        "capex": [4300.0, 4400.0, 4400.0, 4400.0, 4400.0],
        "cause": "Stronger project demand raises volume and utilization; acquisition integration and operating leverage improve margins while higher reinvestment supports growth.",
    },
}


PEERS = {
    "Lowe's": {
        "status": "use", "price": 200.05, "shares": 561.054019,
        "eps": 11.85, "ebit": 10153.0, "da": 1941.0,
        "cash": 3172.0, "debt": 2352.0 + 35204.0,
    },
    "Tractor Supply": {
        "status": "qualify", "price": 34.71, "shares": 521.040137,
        "eps": 2.06, "ebit": 1467.389, "da": 494.011,
        "cash": 231.588, "debt": 2153.826 + 10.315 + 42.933,
    },
}


def median(values):
    values = sorted(values)
    n = len(values)
    return values[n // 2] if n % 2 else (values[n // 2 - 1] + values[n // 2]) / 2


def solve_growth_shift(base_inputs, target, lower=-0.05, upper=0.10):
    if any(g + lower <= -1 or g + upper <= -1 for g in base_inputs["growth"]):
        return None, "invalid bracket: annual growth would be -100% or below"

    def price(shift):
        inputs = deepcopy(base_inputs)
        inputs["growth"] = [g + shift for g in inputs["growth"]]
        forecast = model.run_forecast(inputs)
        return model.value_fcff(forecast["FCFF"], inputs["wacc"], inputs["terminal_growth"])["value_per_share"]

    lo_value, hi_value = price(lower), price(upper)
    if not min(lo_value, hi_value) <= target <= max(lo_value, hi_value):
        return None, f"no solution in bracket ({lo_value:.2f} to {hi_value:.2f})"
    lo, hi = lower, upper
    increasing = hi_value > lo_value
    for _ in range(100):
        mid = (lo + hi) / 2
        value = price(mid)
        if abs(value - target) < 0.0001:
            return mid, "solved"
        if (value < target) == increasing:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2, "solved"


def run():
    tests = {}
    results = {}
    emit("HOME DEPOT PART 3 — SCENARIOS, COMPARABLES, AND DECISION TESTING")
    emit("Valuation date: September 1, 2026 | USD millions | diluted-share basis")
    emit("Evidence cutoff: information public by September 1, 2026")

    emit("\nCAUSAL OPERATING CASES")
    for name, case in SCENARIOS.items():
        inputs = scenario_inputs(case["organic"], case["acquisition"], case["gross_margin"], case["sga_gp"], case["capex"])
        forecast = model.run_forecast(inputs)
        value = model.value_fcff(forecast["FCFF"], inputs["wacc"], inputs["terminal_growth"])
        results[name] = (inputs, forecast, value)
        balance_ok = all(model.near_zero(x) for x in forecast["Balance-sheet gap"])
        cash_ok = all(model.near_zero(x) for x in forecast["Cash-flow-to-cash gap"])
        tests[f"{name} balance sheet"] = balance_ok
        tests[f"{name} cash tie"] = cash_ok
        emit(f"\n{name.upper()}")
        emit("Cause: " + case["cause"])
        emit("Year                         " + " ".join(f"{y:>10}" for y in model.YEARS))
        for label, values, kind in (
            ("Organic growth", case["organic"], "pct"),
            ("Acquisition/new contribution", case["acquisition"], "pct"),
            ("Total revenue growth", inputs["growth"], "pct"),
            ("Gross margin", inputs["gross_margin"], "pct"),
            ("SG&A / gross profit", inputs["sga_gp"], "pct"),
        ):
            emit(f"{label:<29}" + " ".join(f"{v:>9.1%}" for v in values))
        emit(f"{'Capital spending ($m)':<29}" + " ".join(f"{v:>10,.1f}" for v in inputs["capex"]))
        emit(f"{'FCFF ($m)':<29}" + " ".join(f"{v:>10,.1f}" for v in forecast["FCFF"]))
        emit(f"Enterprise value: ${value['enterprise_value']:,.1f}; excess cash: ${value['cash']:,.1f}; debt: ${value['debt']:,.1f}")
        emit(f"Equity value: ${value['equity_value']:,.1f}; value/share: ${value['value_per_share']:.2f}; terminal share: {value['terminal_share']:.1%}")
        emit(f"Checks: balance {'PASS' if balance_ok else 'FAIL'}; cash tie {'PASS' if cash_ok else 'FAIL'}")

    base_inputs, base_forecast, base_value = results["Base"]
    emit("\nWACC–TERMINAL-GROWTH SENSITIVITY ($/diluted share)")
    waccs = [base_inputs["wacc"] - 0.01, base_inputs["wacc"], base_inputs["wacc"] + 0.01]
    growths = [0.020, 0.025, 0.030]
    emit("WACC \\ terminal growth" + "".join(f"{g:>12.1%}" for g in growths))
    sensitivity = []
    for wacc in waccs:
        cells = []
        for growth in growths:
            value = model.value_fcff(base_forecast["FCFF"], wacc, growth)
            cells.append("invalid" if value is None else f"${value['value_per_share']:.2f}")
        sensitivity.append(cells)
        emit(f"{wacc:>21.2%}" + "".join(f"{cell:>12}" for cell in cells))
    tests["Sensitivity monotonicity"] = (
        float(sensitivity[0][1][1:]) > float(sensitivity[1][1][1:]) > float(sensitivity[2][1][1:])
        and float(sensitivity[1][2][1:]) > float(sensitivity[1][1][1:]) > float(sensitivity[1][0][1:])
    )

    emit("\nREVERSE DCF")
    shift, status = solve_growth_shift(base_inputs, model.VALUATION["price"])
    if shift is None:
        emit(f"Target ${model.VALUATION['price']:.2f}: {status}")
    else:
        emit(f"Uniform shift to all five total revenue-growth rates: {shift:+.2%}")
        emit(f"Target share price: ${model.VALUATION['price']:.2f} on September 1, 2026")
        emit("Held fixed: gross margin, SG&A/gross profit, D&A rates, capex, working-capital ratios, tax rate, WACC, terminal growth, bridge debt, excess cash, and diluted shares.")

    emit("\nCOMPARABLE VALUATION — POLICY PRESERVED")
    emit("Policy: listed operating companies with substantial home-improvement/construction/repair/maintenance retail or omnichannel exposure; qualify material customer-mix differences; positive consistent annual GAAP earnings required for P/E.")
    pe_values, ev_ebitda_values = [], []
    for name, p in PEERS.items():
        market_cap = p["price"] * p["shares"]
        ev = market_cap + p["debt"] - p["cash"]
        pe = p["price"] / p["eps"]
        ev_ebitda = ev / (p["ebit"] + p["da"])
        pe_values.append(pe); ev_ebitda_values.append(ev_ebitda)
        emit(f"{name} ({p['status']}): P/E {pe:.6f}x; EV/EBITDA {ev_ebitda:.6f}x; market cap ${market_cap:,.1f}; EV ${ev:,.1f}")
    median_pe, median_ev_ebitda = median(pe_values), median(ev_ebitda_values)
    hd_eps = 14.23  # FY2025 reported GAAP diluted EPS; do not reconstruct with rounded shares.
    hd_ebitda = model.REPORTED["ebit"] + model.REPORTED["presented_da"]
    pe_price = median_pe * hd_eps
    implied_ev = median_ev_ebitda * hd_ebitda
    ev_price = (implied_ev + model.VALUATION["excess_cash"] - model.bridge_debt()) / model.VALUATION["shares"]
    emit(f"Peer median P/E: {median_pe:.6f}x; HD implied price: ${pe_price:.2f}")
    emit(f"Peer median EV/EBITDA: {median_ev_ebitda:.6f}x; HD implied EV: ${implied_ev:,.1f}; implied price: ${ev_price:.2f}")
    emit("Convention: market cap uses September 1 close and latest public actual shares; debt and cash use latest quarter public by that date; finance leases are included in financing debt, operating leases are excluded for all companies; EBITDA is latest annual GAAP operating income plus separately presented D&A.")
    emit("Limitation: Tractor Supply is a qualified, not close, peer because rural-lifestyle/consumable demand differs from project-heavy home improvement; two peers make both medians fragile. Latest-quarter balance sheets and annual EBITDA/EPS mix dates by design and are not forward multiples.")

    emit("\nDECISION TEST")
    low = results["Downside"][2]["value_per_share"]
    high = results["Upside"][2]["value_per_share"]
    emit(f"Operating-case DCF range: ${low:.2f}–${high:.2f}; base ${base_value['value_per_share']:.2f}; market ${model.VALUATION['price']:.2f}.")
    emit(f"Comparable references: P/E ${pe_price:.2f}; EV/EBITDA ${ev_price:.2f}. These are not averaged with DCF.")
    emit("Provisional action: WATCH-DEFER. Initiate only if price falls into the evidence-supported range without deterioration in demand/margins, or if sourced results justify materially stronger organic growth and operating leverage than the base case.")
    emit("Downside result: it does not change the current watch-defer action; at $220.99 it widens the valuation shortfall and makes an immediate initiation less supportable.")
    emit("Monitor: U.S. comparable sales and transactions, big-ticket/project demand, gross margin, SG&A leverage, acquisition integration, inventory days, capex, and market-based WACC inputs.")
    emit("Reversal trigger: sustained comparable-sales growth near or above the upside path with margin expansion would strengthen the case; recessionary demand and margin pressure matching or exceeding downside would support do-not-initiate.")
    emit("WACC caveat: the base 8.20% remains provisional because beta and marginal debt-cost evidence are unresolved; the sensitivity table shows this uncertainty can move value materially.")

    emit("\nAUTOMATED VALIDATION")
    tests["Base rerun deterministic"] = model.run_forecast(deepcopy(base_inputs))["FCFF"] == base_forecast["FCFF"]
    tests["Debt dollar-for-dollar"] = model.near_zero(
        model.value_fcff(base_forecast["FCFF"], base_inputs["wacc"], base_inputs["terminal_growth"], debt=50000)["equity_value"]
        - model.value_fcff(base_forecast["FCFF"], base_inputs["wacc"], base_inputs["terminal_growth"], debt=51000)["equity_value"] - 1000
    )
    tests["Terminal boundary rejected"] = model.value_fcff(base_forecast["FCFF"], 0.025, 0.025) is None
    negative = deepcopy(base_forecast["FCFF"]); negative[0] = -100.0
    tests["Negative FCFF retained"] = negative[0] < 0 and model.value_fcff(negative, base_inputs["wacc"], base_inputs["terminal_growth"]) is not None
    for name, passed in tests.items():
        emit(f"{name}: {'PASS' if passed else 'FAIL'}")

    output = Path(__file__).with_name("05_part3_visible_output.txt")
    output.write_text("\n".join(OUT) + "\n", encoding="utf-8")
    failed = [name for name, passed in tests.items() if not passed]
    if failed:
        emit("FAILED REQUIRED AUTOMATED VALIDATIONS: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run())
