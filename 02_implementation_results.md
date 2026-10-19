# Current Rebuild — Implementation Results

Generated from the saved `home_depot_fcff_model.py` run. Educational AI finance class work; not professional financial advice.

## Result status

The **current reproducible result is $234.31 per diluted share and is provisional**. The earlier $207.85 was a Part 1 assumption-set output; the current explicit-schedule script does not reproduce it, so it is not used as the current result.

## Changes made in the current version

- WACC validation compares `calculated_wacc` directly with `BASE_INPUTS["wacc"]`.
- `value_fcff()` subtracts its resolved `debt` argument. A $1,000 million debt increase is tested to reduce equity value by exactly $1,000 million.
- Operating working capital is scheduled using receivables, inventory, other current assets, accounts payable, accrued salaries, sales taxes, deferred revenue, income taxes payable, and other accrued expenses.
- PP&E, goodwill, intangibles, operating-lease assets, and other noncurrent assets have separate schedules.
- PP&E depreciation and intangible amortization are separate. Their sum is the FCFF cash-flow addback; PP&E and intangibles roll forward by their corresponding amounts.
- Historical assets and liabilities/equity are summed from individual filing lines.
- Historical cash reconciles from separately reported CFO, CFI, CFF, and FX.
- Every required failed validation contributes to exit status 1; runtime accounting errors also exit unsuccessfully.

## Current visible output

USD millions except per-share values.

| Line | 2026E | 2027E | 2028E | 2029E | 2030E |
|---|---:|---:|---:|---:|---:|
| Revenue | 168,800.1 | 173,020.1 | 177,345.6 | 181,779.2 | 186,323.7 |
| Operating income | 21,533.9 | 22,097.3 | 22,683.3 | 23,291.4 | 23,921.3 |
| PP&E depreciation | 3,514.0 | 3,574.9 | 3,628.3 | 3,674.9 | 3,715.6 |
| Intangible amortization | 607.0 | 571.3 | 537.8 | 506.2 | 476.4 |
| Operating NWC | 11,694.1 | 11,986.4 | 12,286.1 | 12,593.2 | 12,908.1 |
| FCFF | 16,241.1 | 16,669.8 | 17,128.2 | 17,598.5 | 18,081.2 |
| Cash | 1,500.0 | 1,500.0 | 1,634.4 | 3,951.2 | 8,414.7 |
| Total assets | 105,876.5 | 106,575.1 | 107,409.4 | 110,432.8 | 115,614.1 |
| Liabilities and equity | 105,876.5 | 106,575.1 | 107,409.4 | 110,432.8 | 115,614.1 |
| Balance-sheet gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Cash-flow-to-cash gap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Current valuation

| Item | Result |
|---|---:|
| Calculated WACC | 8.1984% |
| Enterprise value | $287,132.2 million |
| Excess-cash addback | $0.0 million |
| Financing debt | $(52,896.0) million |
| Equity value | $234,236.2 million |
| Diluted shares | 999.689626 million |
| Value per diluted share | **$234.31** |
| Terminal-value share | 76.4% |

## End-to-end validation

| Required check | Result |
|---|---|
| Historical income-statement reconciliation | PASS |
| Individual FY2025 assets sum to reported total | PASS |
| Individual FY2025 liabilities and equity sum to reported total | PASS |
| CFO + CFI + CFF equals reported pre-FX cash change | PASS |
| Beginning cash + pre-FX change + FX equals ending cash | PASS |
| Calculated WACC equals stored WACC | PASS |
| Forecast balance sheet balances every year | PASS |
| Forecast cash flow ties to cash every year | PASS |
| Signed negative FCFF reduces value | PASS |
| Debt increase reduces equity dollar for dollar | PASS |
| WACC/terminal-growth monotonicity | PASS |
| Enterprise-to-equity bridge | PASS |
| Finance leases included exactly once | PASS |
| Exact saved script exit status | **0** |

## Unresolved evidence

- Beta lacks a reproducible return regression ending August 31, 2026 or a dated September 1 snapshot.
- Debt cost and tax rate remain historical effective proxies rather than marginal inputs.
- Excess cash remains zero because the filing does not identify an excess amount.
- Diluted shares combine August 18 actual shares with the latest disclosed award dilution.
- Operating-lease assets and liabilities are held flat because a complete forecast rollforward is unavailable.
- Forecast assumptions and numeric base-year normalizations still require evidence and challenge records.

Run:

```bash
./.venv/bin/python home_depot_project_1_rebuild/home_depot_fcff_model.py
```
