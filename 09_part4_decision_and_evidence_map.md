# Part 4 — Decision Explanation and Evidence Map

## Why the action is watch/defer

The committee holds no Home Depot position. The September 1, 2026 close of **$319.77** is above the operating-scenario DCF range of **$220.99–$253.91**, the **$240.00** P/E reference, and the **$217.21** EV/EBITDA reference. Because the operating cases and two-peer comparisons are still affected by provisional WACC, dilution, cash, and peer evidence, the analysis supports neither immediate initiation nor a falsely certain “overvalued” claim; it supports watching for a better entry price or evidence of stronger organic growth and operating leverage.

The downside case produces **$220.99**, widening the shortfall to market. It does not change watch/defer by itself because the current action already avoids initiation. For an entry decision, it raises the required margin of safety: a price decline is not sufficient if the decline is accompanied by operating evidence that moves the forecast toward or below the downside path.

## Operating range versus WACC sensitivity

- **Operating-scenario range ($220.99–$253.91):** linked downside/base/upside business paths. Organic demand, acquisition/new-unit contribution, gross margin, SG&A efficiency, and capex move together for stated economic reasons. WACC and terminal growth stay fixed. This is the provisional decision range.
- **WACC–terminal-growth sensitivity ($177.82–$330.03 across the displayed grid):** a valuation-boundary table applied to the base FCFF path. It changes discount/terminal assumptions without changing operations. Its corners are not probabilities or additional operating cases and are not substituted for the decision range.

At the lowest displayed WACC and highest terminal growth, sensitivity reaches $330.03, above market. That does not justify initiation because the 7.20% WACC and 3.0% terminal growth combination has not been established as the evidence-backed base.

## Reconciliation: $234.31 Part 2 to $234.00 Part 3 base

WACC, terminal growth, bridge debt, excess cash, and diluted shares are unchanged. The difference is a sequential operating-assumption update:

| Sequential step | Value/share | Change from prior step |
|---|---:|---:|
| Part 2 operating inputs | $234.308875 | — |
| Part 3 total-growth path | $237.390142 | +$3.081267 |
| Part 3 gross-margin path | $237.075506 | −$0.314636 |
| Part 3 SG&A/gross-profit path | $236.877042 | −$0.198464 |
| Part 3 capex path | **$233.996269** | −$2.880773 |

Net change: **−$0.312606 per share**, displayed as $234.31 to $234.00. The higher guidance-aligned 2026 growth adds value, but the 33.1% near-term gross margin, slight SG&A deleverage, and $4.2bn annual capex more than offset it.

## Published training-case benchmark identified

The required files were available locally at `course-materials/lessons/week-03/starter/dcf_case.csv` and `dcf_expected_output.csv`; no user-supplied answer key was needed.

Inputs: starting FCFF **$100m**; annual growth **8%, 6%, 5%, 4%, 3%**; WACC **10%**; terminal growth **3%**; non-operating cash **$50m**; debt **$300m**; diluted shares **50m**. Convention: annual year-end FCFF, five explicit years, Gordon terminal value at Year 5, discounted five years.

Expected answers: Year 1–5 FCFF **108.000000, 114.480000, 120.204000, 125.012160, 128.762525**; explicit FCFF PV **448.440817**; terminal value at Year 5 **1,894.648579**; terminal-value PV **1,176.427703**; enterprise value **1,624.868520**; common equity value **1,374.868520**; value/share **27.497370**; terminal-value share **0.724014**. The saved benchmark reproduces all twelve within the published tolerances.

## Assignment and rubric evidence map

| Requirement | Evidence file or record | Status |
|---|---|---|
| Decision user, no-position action, target/security | `README.md`; this file | Complete |
| Horizon, valuation date, currency, diluted-share basis, exclusions | `README.md`; `03_valuation_basis.md` | Complete; exact dilution remains provisional |
| Unchanged Edition A | `edition_a_unchanged.md`; matching SHA-1 recorded in work log | File preserved; **Brightspace receipt still required** |
| Edition B and A-to-B evidence table | `16_edition_b_draft.md` | Working draft complete; **not frozen** |
| FY2025 reported base reconciles to filing | `01_base_year_reconciliation.md`; `home_depot_fcff_model.py` | Complete mechanically; 10-K date corrected to Mar. 18 |
| Facts, normalizations, forecasts, outputs distinguished | `04_part3_assumption_challenge_record.md` | Complete structure; unresolved items remain labelled |
| Separate reported base and normalizations | `03_valuation_basis.md`; `04_part3_assumption_challenge_record.md` | Complete policy; several numeric normalizations unresolved and not embedded |
| Five-year linked statements and personalized drivers | `home_depot_fcff_model.py`; `02_implementation_results.md` | Complete implementation |
| Balance sheet, cash tie, base-year checks fail loudly | `home_depot_fcff_model.py`; `02_implementation_results.md` | Complete automated checks |
| Five-year signed FCFF/WACC DCF | `home_depot_fcff_model.py`; `05_part3_visible_output.txt` | Complete; WACC evidence provisional |
| EV-to-equity/per-share bridge and leases | `03_valuation_basis.md`; model validation | Complete mechanics; excess cash/dilution unresolved |
| Low/base/high causal operating cases | `part3_analysis.py`; `05_part3_visible_output.txt` | Complete |
| Downside capable of testing action | `05_part3_visible_output.txt`; this file | Complete test; downside did not change action |
| WACC–growth sensitivity and boundary checks | `part3_analysis.py`; `05_part3_visible_output.txt` | Complete |
| Terminal-value share | `05_part3_visible_output.txt` | Complete |
| Reverse DCF and held-fixed inputs | `05_part3_visible_output.txt` | Complete |
| Assumption-challenge record for load-bearing drivers | `04_part3_assumption_challenge_record.md` | Complete structure; evidence gaps explicitly unresolved |
| Peer policy set before results | `07_comparable_valuation.md` | Complete |
| Equity-value multiple | `07_comparable_valuation.md` | Complete: trailing GAAP P/E |
| Enterprise-value multiple | `07_comparable_valuation.md` | Complete: trailing GAAP EV/EBITDA |
| Dates, periods, debt/cash and lease convention | `07_comparable_valuation.md`; `13_source_consistency_audit.md` | Dated ERP resolved; price amounts cross-verified; exchange-quality price evidence remains incomplete |
| Relevant transaction evidence | No defensible transaction set selected | Not used; no unsupported transaction multiple invented |
| Explain method disagreement; do not average | `07_comparable_valuation.md`; this file | Complete |
| Provisional range, conditional action, monitoring/reversal | `05_part3_visible_output.txt`; this file | Complete, provisional |
| Published known-answer reconciliation | `benchmark_validation.py`; `14_training_benchmark_output.txt` | Complete: all twelve outputs pass |
| Independent load-bearing source/definition check | `11_ai_output_check.md`; `13_source_consistency_audit.md` | Complete for peer qualification and debt/lease definitions |
| Human AI-off changed-input prediction and precommit | `08_locked_changed_input_record.md`; commit `46e3d77…` | Complete for terminal-growth test |
| Credited partner challenge | `20_partner_challenge_status.md`; placeholder in preserved Edition A | **Incomplete; no challenge or credit invented** |
| Blank procedure for another changed-input test | `10_locked_changed_input_blank.md` | Prepared; intentionally blank |
| Highest-risk failure test | model/Part 3 terminal boundary, debt, sign and monotonicity tests | Code complete; **Video 2 demonstration incomplete** |
| Actual AI output independently checked | `11_ai_output_check.md` | Complete working record; frozen PDF/video still incomplete |
| Fresh-environment instructions | `12_cold_run_instructions.md`; `requirements.txt` | Prepared |
| Recorded cold run | No recording yet | **Incomplete** |
| Visible executed output | `05_part3_visible_output.txt`; `14_training_benchmark_output.txt` | Complete |
| README/repository map and run commands | `README.md` | Complete working version |
| Research-Evolution PDF | `edition_a_unchanged.md`; `16_edition_b_draft.md` | Draft components prepared; **PDF incomplete/not frozen** |
| Validation-and-AI-Use frozen PDF | Markdown records only | **Incomplete** |
| Decision memo/deck | `17_decision_memo_draft.md` | Working draft prepared; **PDF incomplete/not frozen** |
| Videos 1–3 and corrected transcripts | `18_video_outlines.md` | Outlines prepared; **recordings/transcripts incomplete** |
| Brightspace manifest, URLs, access check | `19_submission_manifest.csv` | Twelve rows prepared; **URLs/access/frozen IDs incomplete** |

### Rubric mapping

| Criterion | Primary current evidence | Main remaining risk |
|---|---|---|
| Problem definition and decision usefulness | `README.md`, this file, Edition A, working Edition B/memo | Freeze final committee artifacts |
| Data integrity and traceability | files `01`, `03`, `04`, `07`, `13` | WACC proxies, price-source quality, dilution/excess cash |
| Financial soundness and judgment | model, files `05`, `07`, this file | provisional WACC and narrow peers |
| Technical execution and usability | three Python scripts, visible outputs, README | actual fresh-environment cold run |
| Validation, sensitivity, reproducibility | files `08`, `10`, `11`, `12`, `14` | frozen validation PDF and recorded demonstration |
| Professional communication | organized Markdown, visible results, working memo/video plans | frozen memo, recordings, corrected transcripts, completed manifest |

Educational AI finance class work; not professional financial advice.
