# Architecture Audit and Priority Gaps

## How the existing files connect

| Artifact | Current role | Connection problem |
|---|---|---|
| Edition A | Initial thesis, decision frame, filing facts, unknowns, and research plan | Must remain unchanged; its synthetic bridge, human partner question, and receipt fields are visibly incomplete and cannot be fabricated now. |
| Lab 3 / acquisition research | Builds the acquisition thesis and watch/defer logic | Strong qualitative thread, but acquisition-level FCFF and ROIC remain undisclosed and unresolved. |
| `home_depot_dcf_inputs.md` | Sources the starting FCFF, WACC, terminal growth, cash, debt, shares, and market price | Uses a September 10 forecast/WACC and September 9 price rather than the September 1 valuation date. Debt omits short-term commercial paper. |
| `dcf.py` | Stand-alone FCFF-growth DCF, WACC-growth grid, and reverse DCF | Forecast FCFF is grown directly from one historical FCFF number rather than produced by the three-statement operating model. |
| `home_depot_proforma.py` | Five-year linked statements and operating sensitivities | Produces FCFE and discounts it at cost of equity; the assignment requires FCFF discounted at WACC. |
| `comps.py` / `comps.md` | Peer P/E equity-value cross-check | Has an equity-value multiple but lacks the required consistent enterprise-value multiple. |
| Sensitivity files | Gross-margin and SG&A cases with visible checks | Cases apply to the FCFE architecture, not yet to the required FCFF/WACC DCF; the saved “locked” record must not be represented as AI-off unless independently documented. |

## Highest-priority gaps

1. **Historical base year and debt are inconsistent across engines.** The DCF subtracts $51,308 million of long-term debt but omits $4,464 million of short-term commercial paper. The pro-forma carries both. Before any valuation, the bridge must use one explicit debt perimeter.
2. **The three-statement forecast does not feed the required DCF.** The stand-alone DCF grows historical FCFF mechanically, while the pro-forma values FCFE. The rebuilt model must calculate FCFF from projected operating statements and pass it directly into the WACC engine.
3. **Base-year reconciliation is incomplete.** The existing aggregate opening balance sheet balances, but it does not print a filing-to-model reconciliation. Income-statement D&A ($3,273 million) and total cash-flow D&A/addbacks ($4,121 million) are different definitions and must not be used interchangeably.
4. **Normalization and basis changes are not cataloged.** FY2025 includes a full year of SRS, a partial year of GMS, acquired-intangible amortization, and acquisition-driven revenue. FY2024 had 53 weeks. These contaminate simple historical growth and margin comparisons.
5. **Cash and share conventions are unresolved.** The DCF adds all $1,389 million of cash as non-operating, while the pro-forma assumes a $1,500 million minimum cash balance without evidence. The project also needs a valuation-date reconciliation of weighted-average diluted shares versus period-end/current shares.
6. **WACC support is incomplete and date-mismatched.** The 8.8% estimate lacks a fully visible September 1 component build and conflicts with later dates in the DCF input file.
7. **Peer evidence is incomplete for the required architecture.** P/E is present; a consistently defined enterprise-value multiple and its debt/cash bridge are not.
8. **Required downside and validation evidence is incomplete.** Existing sensitivities are useful but are not a named recommendation-changing downside case. No fresh-environment cold-run record, highest-risk failure test, complete bridge check, or dated market-fact manifest exists in the current bundle.
9. **The output is still point-oriented.** The final committee decision must use a defensible range with conditions and reversal/monitoring triggers, not one DCF number or a mechanical average.

## Material choices to defend in the rebuild

- Treat short-term commercial paper as debt in the enterprise-to-equity bridge.
- Include current and noncurrent long-term debt, including finance-lease obligations already included in Note 5 total long-term debt.
- Exclude operating-lease liabilities from the preliminary debt bridge while lease costs remain in operating expenses; changing that treatment requires a matching operating-profit and multiple adjustment.
- Keep interest, debt repayment, dividends, and buybacks out of FCFF. They remain financing-statement items, not operating FCFF drivers.
- Calculate FCFF as NOPAT plus total noncash D&A minus capital expenditure minus investment in operating working capital, with acquisition cash payments excluded from recurring capital expenditure.
- Preserve signed cash flows. Negative FCFF reduces value; it is not floored at zero.
- Use reported history first, then state each normalization separately rather than silently rewriting the filing.

