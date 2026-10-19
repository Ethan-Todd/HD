# Validation and AI Use — Working Record

This is the working Markdown source, not the final frozen submission PDF.

## Decision, version and boundary

- Decision: whether a buy-side committee with no current Home Depot position should initiate, watch/defer, or not initiate.
- Current action: provisional **watch/defer**.
- Valuation date and evidence cutoff: **September 1, 2026**.
- Currency/share basis: USD millions and estimated valuation-date diluted shares.
- Development environment: Python 3.14.7, Darwin arm64; model uses the standard library only.
- Core-model SHA-1: `7e3b3fd9165435e1de8c56d14bdfbb3582cdb953`.
- Part 3 SHA-1: `b7ad6536d81d415fa5d8aedf8911529cb934c6ee`.
- Benchmark SHA-1: `ebf92452822103c519dcb709d48b86c66226985c`.

## Data and convention ledger

The complete load-bearing ledger is `04_part3_assumption_challenge_record.md`. Source accessibility and definition checks are in `13_source_consistency_audit.md`. The official September 1 ERP observation is now directly cited. Unresolved beta, marginal debt cost/tax, exact dilution, excess cash, operating-lease rollforward, the ERP-source/model risk-free-rate convention difference, and exchange-quality price evidence remain visible.

## Validation register

| Claim/output | Failure mode | Test and expected result | Actual result | Disposition | Evidence |
|---|---|---|---|---|---|
| DCF formulas reproduce course convention | Formula/timing/bridge error | Twelve published training outputs within stated tolerances | All twelve PASS | Accept implementation | `benchmark_validation.py`; `14_training_benchmark_output.txt` |
| FY2025 reported base is intact | Components omitted or mixed with normalization | Statement component sums and cash rollforward equal reported totals | PASS | Accept mechanics | `home_depot_fcff_model.py`; `02_implementation_results.md` |
| Forecast statements articulate | Cash plug hides imbalance | BS gap and cash tie equal zero in all years/cases | PASS | Accept mechanics | model; `05_part3_visible_output.txt` |
| FCFF keeps its sign | Negative cash flow is floored | Synthetic −$100m first-year FCFF reduces EV by its discounted amount | PASS | Accept mechanics | model validation output |
| Debt bridge is responsive | Function ignores argument or double counts lease debt | $1,000m debt increase lowers equity $1,000m; finance leases included once | PASS | Accept mechanics | model validation output; `03_valuation_basis.md` |
| DCF boundary and direction | g ≥ WACC valued; monotonicity reversed | Reject g = WACC; value falls as WACC rises and rises as g rises | PASS | Accept mechanics | core and Part 3 output |
| Changed-input ownership | Prediction recorded after result | Human wording saved and committed before terminal-growth run | PASS | Accept record | `08_locked_changed_input_record.md`; commit `46e3d77…` |
| Terminal-growth prediction magnitude | Human expected ~3% decline | Compare exact base/changed values | Actual −14.80%; direction right, magnitude wrong | Correct interpretation | `08_locked_changed_input_record.md` |
| AI peer suggestion | Industry label hides economic mismatch | Check TSCO product mix in SEC filing | TSCO materially rural/consumable | Qualify, not close peer | `11_ai_output_check.md` |
| Reproducibility | Works only in development environment | Recorded clean clone and three-script run | Unrecorded fresh clone of published merge passed all three scripts; required recording not performed | **Mechanics pass; recorded evidence incomplete** | `12_cold_run_instructions.md` |
| Credited partner challenge | AI or author invents peer feedback | Preserve the partner's exact question, identity/credit, response and disposition | Edition A still contains a placeholder; no separate completed record located | **Incomplete—do not claim credit** | `edition_a_unchanged.md` |

## Locked Changed-Input Record

The completed record is `08_locked_changed_input_record.md`. It contains the exact human sentence, pre-run timestamp/commit, 2.5% → 1.5% annual terminal-growth change, fixed inputs, actual −$34.62/−14.80% result, validation, mismatch diagnosis and unchanged watch/defer action. `10_locked_changed_input_blank.md` is an unused blank AI-off template and is not evidence of another completed test.

## Named AI-use register

| Tool/model surface | Date | Material task/output | Independent check | Disposition | Decision effect |
|---|---|---|---|---|---|
| Codex, GPT-5; no finer version exposed | Oct. 19, 2026 | Carried Tractor Supply as a potential HD peer | SEC Q2 product mix | Qualify rather than accept as close peer | Makes peer median a fragile reference; no mechanical average; action unchanged |

Full detail is in `11_ai_output_check.md`. Before freezing the PDF, confirm the exposed product label shown in the submitted interface and correct it if the interface shows a different version; do not guess.

## Limitations, monitoring and reversal

- Watch comps, transactions, big-ticket/project demand, gross margin, SG&A leverage, acquisition integration, inventory days, capex and market-based WACC inputs.
- Initiate only if price enters the evidence-supported range without deteriorating fundamentals, or sourced results support a stronger path.
- Move toward do-not-initiate if operating evidence meets/exceeds downside deterioration or the valuation bridge/checks fail.
- The displayed WACC sensitivity is a boundary test, not the operating decision range.

## Not complete

- recorded cold run and Video 2 demonstration;
- frozen Validation-and-AI-Use PDF;
- frozen capture of the directly cited dated ERP statement and exchange-quality prices;
- credited partner challenge record;
- Edition B and Research-Evolution PDF;
- memo/deck, Videos 1–3, transcripts, manifest and access checks.

Educational AI finance class work; not professional financial advice.
