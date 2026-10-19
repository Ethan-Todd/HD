# Source Accessibility and Consistency Audit

Checked October 19, 2026. “Accessible” means the cited page opened during this audit; it does not guarantee future access.

## Accessibility and date checks

| Evidence | Date/period used | Accessibility result | Finding/action |
|---|---|---|---|
| Home Depot FY2025 10-K, accession 0001628280-26-019436 | Year ended Feb. 1, 2026; filed **Mar. 18, 2026** | SEC HTML accessible | Corrected two Mar. 11 references in `04_part3_assumption_challenge_record.md` to Mar. 18 |
| Home Depot Q2 FY2026 10-Q, accession 0001628280-26-058715 | Balance sheet Aug. 2; shares Aug. 18; filed Aug. 25, 2026 | SEC HTML accessible | Dates are correctly distinguished; latest filing public before Sep. 1 |
| Home Depot Q2 release/guidance | Published Aug. 18, 2026 | IR page accessible | FY2026 total sales 2.5%–4.5%, comps 0%–2%, gross margin ~33.1%, capex ~2.5% of sales |
| U.S. Treasury daily curve | Sep. 1, 2026 | Treasury page accessible | 10-year column shows 4.79%; definition remains 10-year par yield |
| Damodaran ERP | Sep. 1, 2026 value used: 4.14% | [Damodaran's official home page](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm?trk=public_post_reshare-text) directly states “Implied ERP on September 1, 2026 = 4.14% (Trailing 12 month, adjusted payout)” | **Resolved dated ERP observation.** Damodaran's calculation used a 4.75% Treasury rate; the model independently uses the Treasury's 4.79% 10-year par yield, so that convention difference remains disclosed rather than silently blended |
| HD Sep. 1 close | $319.77 | Nasdaq's official historical-data page opened but displayed “Data currently not available”; independent historical tables from [Yahoo](https://es.finance.yahoo.com/quote/HD/history/), [Investing.com](https://mx.investing.com/equities/home-depot-historical-data), and [ChartExchange](https://chartexchange.com/symbol/nyse-hd/historical/) agree on the amount | Amount/date cross-verified; **exchange-quality saved evidence remains incomplete** |
| LOW Sep. 1 close | $200.05 | [Yahoo historical prices](https://finance.yahoo.com/quote/LOW/history/) supports the amount; Nasdaq's historical archive was unavailable during the audit | Amount/date cross-verified; **exchange-quality saved evidence remains incomplete** |
| TSCO Sep. 1 close | $34.71 | [Yahoo historical prices](https://ca.finance.yahoo.com/quote/TSCO/history/) and [Investing.com](https://www.investing.com/equities/tractor-supply-company-historical-data) agree | Amount/date cross-verified; **exchange-quality saved evidence remains incomplete** |
| Lowe's Q2 10-Q | July 31 balance sheet; Aug. 25 shares; filed before Sep. 1 | SEC HTML accessible | Shares, cash and debt definitions trace to filing |
| Tractor Supply Q2 10-Q | June 27 balance sheet; July 25 shares; filed Aug. 6 | SEC HTML accessible | Shares, cash, debt, finance leases and product mix trace to filing |
| Local Week 3 training CSVs | Published course files | Accessible locally | Inputs and answer key copied exactly into benchmark code; all outputs pass |

## Multiple and definition consistency

| Item | Consistency check | Result |
|---|---|---|
| P/E | Same-date Sep. 1 prices; latest annual positive reported GAAP diluted EPS; target excluded from peer set | PASS |
| EV/EBITDA | Same-date price × latest public actual shares; latest public cash/debt; annual GAAP operating income + presented D&A | PASS with mixed-date/trailing limitation disclosed |
| Finance leases | Included once in financing debt for target and peers | PASS |
| Operating leases | Excluded from debt and no lease capitalization adjustment to EBITDA for all companies | PASS as a consistent convention; economic limitation disclosed |
| Excess cash | Zero in HD DCF and peer-implied HD bridge | PASS consistency; underlying amount unresolved |
| Share basis | DCF uses estimated valuation-date diluted shares; P/E uses reported annual diluted EPS; EV numerator uses latest actual shares | Definitions are explicitly different for valid reasons; exact HD dilution remains unresolved |
| Currency | All target and peers are U.S. issuers and calculations are USD | PASS |
| Earnings periods | Latest annual reported GAAP results public by Sep. 1; no quarterly EPS substituted | PASS |
| Price date | Sep. 1, 2026 for HD, LOW and TSCO | PASS amount consistency; source-quality gap remains |
| Method aggregation | DCF, P/E and EV/EBITDA are shown separately | PASS; no mechanical average |

## Saved-output/document consistency

- Part 2 `$234.31` and Part 3 base `$234.00` are both valid for their labelled operating input sets; `09_part4_decision_and_evidence_map.md` reconciles the $0.31 change.
- `05_part3_visible_output.txt`, README and comparable file agree on $220.99–$253.91, $319.77 market, $240.00 P/E reference and $217.21 EV/EBITDA reference.
- `08_locked_changed_input_record.md` uses the Part 3 base $234.00, not the Part 2 $234.31, and records the 1.5% terminal-growth result of $199.38.
- The peer-policy labels agree: Lowe's “use,” Tractor Supply “qualify,” Menards “exclude.”
- The current WACC is consistently 8.1984%/8.20% rounded and remains provisional.
- Final memo, recordings and transcripts do not yet exist, so cross-artifact consistency cannot be checked for them.

## Open corrections before freezing submission

1. Save exchange-quality or Nasdaq historical-price evidence for all three Sep. 1 closes if the archive becomes available; current amounts are cross-verified only with third-party tables.
2. Preserve a PDF/screenshot of the official dated ERP statement for the frozen evidence package and explain the 4.75% ERP-source Treasury input versus the independently selected 4.79% Treasury par yield.
3. Resolve or sensitivity-test exact award dilution, excess cash, marginal debt cost/tax and operating-lease rollforward.
4. After final artifacts exist, compare every displayed valuation, date, unit and recommendation across them.

Educational AI finance class work; not professional financial advice.
