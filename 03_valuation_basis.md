# Part 2 — Current Valuation Basis

Educational AI finance class work; not professional financial advice. Edition A and original files are unchanged.

**Status: complete for implementation; provisional for evidence.** The code and accounting mechanics are implemented and validated. The result remains provisional because several load-bearing inputs still use estimates or proxies.

## 1. One valuation date

**September 1, 2026** is used for the decision, HD closing price, risk-free rate, ERP, and market capitalization. The latest company filing public by then was the Q2 FY2026 10-Q filed August 25, with an August 2 balance sheet and an exact August 18 outstanding-share disclosure.

| Input | Value | Date | Evidence |
|---|---:|---|---|
| HD closing price | $319.77 | September 1, 2026 | [Yahoo historical prices](https://ca.finance.yahoo.com/quote/HD/history/) |
| Latest filing | Q2 FY2026 10-Q | Filed August 25, 2026 | [SEC filing](https://www.sec.gov/Archives/edgar/data/354950/000162828026058715/hd-20260802.htm) |
| Balance-sheet date | August 2, 2026 | Latest public by valuation date | Q2 10-Q, p. 1 |

## 2. Sourced WACC

| Component | Value | Definition/calculation | Date | Status |
|---|---:|---|---|---|
| Risk-free rate | 4.79% | 10-year Treasury par yield | September 1, 2026 | Resolved: [U.S. Treasury](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value=202609&type=daily_treasury_yield_curve) |
| Equity-risk premium | 4.14% | Trailing-12-month adjusted-payout implied ERP | September 1, 2026 | Selected convention: [Damodaran](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm) |
| Levered beta | 1.00 | Five-year monthly provider beta | Not captured exactly on September 1 | **Unresolved dated evidence** |
| Cost of equity | 8.93% | 4.79% + 1.00 × 4.14% | September 1 basis | Provisional because beta is unresolved |
| Pre-tax debt cost | 4.3950% | $1,194 × 2 ÷ average financing debt | Latest six months | **Historical effective proxy, not marginal cost** |
| Tax rate | 24.6633% | $2,637 ÷ $10,692 | Six months ended August 2 | **Effective proxy, not necessarily marginal** |
| Market equity | $319,670.8m | $319.77 × 999.689626m | September 1 basis | Calculated |
| Market debt | $47,850.0m | Senior notes at fair value + other debt + commercial paper | August 2 | Filing-based calculation |
| Equity/debt weights | 86.9803% / 13.0197% | Market-value weights | September 1 basis | Calculated |

`WACC = 86.9803% × 8.93% + 13.0197% × 4.3950% × (1 − 24.6633%) = 8.1984%`

The code compares this calculated result directly with `BASE_INPUTS["wacc"]`. WACC and the resulting valuation remain **provisional** until the beta and marginal debt/tax evidence are resolved.

## 3. Enterprise-to-equity bridge and leases

| Item | USD millions |
|---|---:|
| Enterprise value | 287,132.2 |
| Excess-cash addback | 0.0 |
| Commercial paper | (4,248.0) |
| Current long-term debt | (4,697.0) |
| Noncurrent long-term debt | (43,951.0) |
| Equity value | **234,236.2** |

- Finance leases are $303 million current plus $2,791 million noncurrent. They are already classified inside long-term debt and are included once—never separately re-added.
- Operating leases are $1,516 million current plus $8,155 million noncurrent. They are excluded from financing debt because lease expense remains in EBIT and FCFF. Capitalizing them would require corresponding EBIT, FCFF, and comparable-multiple adjustments.
- Reported cash is $2,085 million. The base adds zero because the filing does not identify an excess amount. Adding all cash would be a sensitivity, not a sourced base assumption.

## 4. Diluted shares

| Measure | Millions | Use |
|---|---:|---|
| FY2025 weighted-average diluted shares | 995.000000 | Historical EPS only |
| Common shares outstanding August 18 | 997.689626 | Latest exact point-in-time disclosure |
| Latest reported incremental award dilution | 2.000000 | Q2 Note 8 proxy |
| Valuation-date diluted estimate | **999.689626** | Per-share valuation denominator |

This is more appropriate than the historical weighted-average EPS denominator, but remains approximate because award dilution and share activity through September 1 are not fully disclosed.

## 5. Separate normalization proposals

Reported FY2025 remains unchanged. No unresolved adjustment is embedded.

| Issue | Proposed treatment | Double-count protection | Status |
|---|---|---|---|
| SRS | Retain owned business; use organic/comparable evidence for growth | Do not remove SRS revenue and also reduce consolidated growth for the same effect | Profit split unresolved |
| GMS | Retain reported partial period; investigate a full-year run rate | Any run-rate addition must replace growth already attributed to GMS | Numeric adjustment unresolved |
| Mingledorff’s | Reflect latest balance sheet; separately investigate forward contribution | Do not treat purchase price as recurring capex or add earnings twice | Contribution unresolved |
| FY2024 53rd week | Normalize historical comparison, not FY2025 reported results | Do not combine 52/53 scaling with another adjustment to the same sales | Exact effect unresolved |
| Acquisition amortization | Keep in reported case; any adjusted case must also adjust tax and asset schedules | Never add back through both EBIT and D&A | No adjustment selected |
| FY2024 legal benefit | Adjust FY2024 comparison only if amount is sourced | Do not alter FY2025 for a prior-year benefit | Amount unresolved |
| Acquisition payments | Exclude from recurring capex | Do not deduct in both FCFF and equity bridge | Classification resolved |

## 6. Reconciliation from $207.85

The $207.85 result is an archived Part 1 result, not reproducible by the current explicit-schedule model. The first line isolates the schedule-architecture difference; later lines change one valuation-basis item at a time while holding the current FCFF forecast fixed.

| Sequential step | Value/share | Change |
|---|---:|---:|
| Archived Part 1 documented result | $207.85 | — |
| Current explicit schedules at old 8.8%/cash/debt/shares basis | $206.34 | −$1.51 |
| Valuation-date diluted shares | $205.37 | −$0.97 |
| Latest public financing debt | $208.24 | +$2.88 |
| Zero excess-cash convention | $206.86 | −$1.39 |
| Provisional 8.1984% WACC | **$234.31** | **+$27.45** |

The WACC change is the main cause of the valuation increase. Before changing WACC, the schedule, share, debt, and cash changes move the documented $207.85 to $206.86, a net decrease of $0.99. Reducing WACC from 8.8% to 8.1984% then increases value by $27.45 to $234.31.

## Facts versus proxies

| Type | Items |
|---|---|
| Dated facts | September 1 price and Treasury yield; August 2 cash, debt and lease balances; August 18 shares outstanding; Q2 reported interest, pretax income and tax provision |
| Calculated from dated facts | Market equity and debt, capital weights, historical effective debt cost, effective tax rate, enterprise-to-equity bridge |
| Estimated proxies/judgments | 1.00 beta, historical effective debt cost as marginal cost proxy, effective tax rate as marginal tax proxy, two million incremental dilution, zero excess cash, terminal growth and operating forecast drivers |

## Validation

Historical component sums, reported cash subtotals, forecast balance sheets, forecast cash ties, signed FCFF, debt dollar-for-dollar behavior, DCF monotonicity, the EV-equity bridge, finance-lease treatment, and direct WACC comparison all pass. A deliberate WACC mismatch produces `FAIL` and exit status 1; the clean saved script exits 0.

### Assignment requirements still outstanding

- Evidence-backed low/base/high operating cases and a named downside case
- Completed assumption-challenge record with evidence that would change each load-bearing input
- One consistent enterprise-value comparable multiple, with peer-definition checks
- Reverse DCF or market-implied expectation tied to the current engine
- Highest-risk failure test and documented fresh-environment cold run
- Final valuation range, conditional committee action, monitoring and reversal triggers
- Final memo/deck, recordings, corrected transcripts, manifest and access checks

## Still unresolved before final valuation conclusions

- Dated beta or reproducible beta regression through August 31, 2026
- Marginal debt cost and marginal tax rate
- Evidence for any excess cash
- Award-level valuation-date dilution
- Detailed operating-lease rollforward
- Evidence-backed forecast ranges and numeric normalization adjustments

The next phase is the requested evidence-backed low/base/high scenarios and enterprise-value comparable analysis. The final memo is intentionally deferred until those are complete.
