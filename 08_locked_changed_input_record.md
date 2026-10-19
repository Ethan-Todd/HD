# Locked Changed-Input Record

## Pre-run record — frozen before execution

- Recorded at: **2026-10-19 18:18:31 EDT**
- Model: Home Depot Part 3 linked pro-forma and FCFF/WACC DCF
- Model files and pre-run SHA-1 versions:
  - `home_depot_fcff_model.py`: `7e3b3fd9165435e1de8c56d14bdfbb3582cdb953`
  - `part3_analysis.py`: `b7ad6536d81d415fa5d8aedf8911529cb934c6ee`
- Case tested: Part 3 base operating case
- Independent input changed: terminal growth rate
- Old value: **2.5% per year**
- New value: **1.5% per year**
- Unit: **annual percentage rate**, a decrease of **1.0 percentage point**
- Held fixed: five-year operating-case assumptions and resulting FCFF, WACC, excess cash, financing debt, diluted shares, discount timing, and every other independent input
- Student prediction, preserved exactly: **I expect value per share to fall a little like around 3%.**

The actual result, comparison, validation, and recommendation effect are intentionally omitted from this pre-run section until after the committed prediction is executed.

## Pre-run commit

- Commit: `46e3d779148b70b78a9ea9bde56ff9a9c7674c03`
- Commit timestamp: **2026-10-19T18:18:48-04:00**
- Commit message: `Lock terminal-growth changed-input prediction`

## Post-run result

| Measure | Base case | Changed case | Changed minus base |
|---|---:|---:|---:|
| Terminal growth | 2.5% per year | 1.5% per year | −1.0 percentage point |
| DCF value per diluted share | $234.00 | $199.38 | −$34.62 |
| Percentage change in value per share | — | — | −14.80% |
| Enterprise value | $286,819.6m | $252,209.8m | −$34,609.8m |
| Terminal-value share of enterprise value | 76.57% | 73.36% | −3.22 percentage points |

Unrounded values used in the comparison were $233.996269 and $199.375697 per share. The changed value minus the base value was −$34.620572; divided by the unrounded base value, the change was −14.795352%.

## Validation results

- Only the terminal-growth valuation input changed: **PASS**.
- Five-year FCFF remained identical between cases: **PASS**.
- Forecast balance sheet balanced in every base-case year: **PASS**.
- Forecast cash flow tied to balance-sheet cash in every base-case year: **PASS**.
- Directional check—lower terminal growth lowers value: **PASS**.
- Terminal growth remained below WACC in both cases: **PASS**.
- Initial execution attempt: **did not run the model** because `./.venv/bin/python` was called from the rebuild subfolder, where that relative path does not exist. The rerun used the working Python environment one directory above; this was an execution-path correction, not a model or input change.

## Prediction comparison and decision effect

Original prediction, unchanged: **I expect value per share to fall a little like around 3%.**

The predicted direction was correct, but the predicted magnitude was not: the actual decline was 14.80%, about 11.80 percentage points larger than the predicted approximate 3% decline. The main explanation is terminal-value concentration: 76.57% of base enterprise value came from cash flows after 2030, so reducing perpetual growth by one percentage point materially reduced the largest valuation component.

The provisional recommendation remains **watch-defer**. The changed $199.38 value and the base $234.00 value are both below the September 1, 2026 market price of $319.77, so the change increases the modeled valuation gap but does not cross a recommendation boundary. It reinforces terminal growth as a research and monitoring priority rather than establishing mispricing by itself.

Educational AI finance class work; not professional financial advice.
