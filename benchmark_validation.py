"""Published Week 3 synthetic FCFF DCF known-answer reconciliation."""
from pathlib import Path
import sys

INPUTS = {
    "starting_fcff": 100.0,
    "growth": [0.08, 0.06, 0.05, 0.04, 0.03],
    "wacc": 0.10,
    "terminal_growth": 0.03,
    "cash": 50.0,
    "debt": 300.0,
    "shares": 50.0,
}

EXPECTED = {
    "FCFF Year 1": (108.000000, 0.01),
    "FCFF Year 2": (114.480000, 0.01),
    "FCFF Year 3": (120.204000, 0.01),
    "FCFF Year 4": (125.012160, 0.01),
    "FCFF Year 5": (128.762525, 0.01),
    "PV explicit FCFF": (448.440817, 0.01),
    "Terminal value Year 5": (1894.648579, 0.01),
    "PV terminal value": (1176.427703, 0.01),
    "Enterprise value": (1624.868520, 0.01),
    "Common equity value": (1374.868520, 0.01),
    "Value per diluted share": (27.497370, 0.01),
    "Terminal value share": (0.724014, 0.0002),
}


def calculate():
    if INPUTS["terminal_growth"] >= INPUTS["wacc"]:
        raise ValueError("terminal growth must be less than WACC")
    fcff = []
    current = INPUTS["starting_fcff"]
    for growth in INPUTS["growth"]:
        current *= 1.0 + growth
        fcff.append(current)
    explicit = sum(value / (1.0 + INPUTS["wacc"]) ** year for year, value in enumerate(fcff, 1))
    terminal = fcff[-1] * (1.0 + INPUTS["terminal_growth"]) / (INPUTS["wacc"] - INPUTS["terminal_growth"])
    pv_terminal = terminal / (1.0 + INPUTS["wacc"]) ** 5
    enterprise = explicit + pv_terminal
    equity = enterprise + INPUTS["cash"] - INPUTS["debt"]
    return {
        **{f"FCFF Year {year}": value for year, value in enumerate(fcff, 1)},
        "PV explicit FCFF": explicit,
        "Terminal value Year 5": terminal,
        "PV terminal value": pv_terminal,
        "Enterprise value": enterprise,
        "Common equity value": equity,
        "Value per diluted share": equity / INPUTS["shares"],
        "Terminal value share": pv_terminal / enterprise,
    }


def main():
    actual = calculate()
    lines = [
        "PUBLISHED WEEK 3 TRAINING-CASE RECONCILIATION",
        "Source: course-materials/lessons/week-03/starter/dcf_case.csv and dcf_expected_output.csv",
        "Convention: USD millions; year-end FCFF; five years; Gordon terminal value at Year 5",
        "",
        f"{'Output':<29}{'Actual':>15}{'Expected':>15}{'Difference':>15}{'Result':>10}",
    ]
    failed = []
    for label, (expected, tolerance) in EXPECTED.items():
        difference = actual[label] - expected
        passed = abs(difference) <= tolerance
        if not passed:
            failed.append(label)
        lines.append(f"{label:<29}{actual[label]:>15.6f}{expected:>15.6f}{difference:>15.6f}{'PASS' if passed else 'FAIL':>10}")
    lines.append("")
    lines.append(f"Overall: {'PASS' if not failed else 'FAIL'}")
    text = "\n".join(lines) + "\n"
    print(text, end="")
    Path(__file__).with_name("14_training_benchmark_output.txt").write_text(text, encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
