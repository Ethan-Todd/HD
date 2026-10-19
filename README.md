# Home Depot Project 1 Rebuild

This folder is a separate rebuild. Edition A and every original project file outside this folder remain unchanged.

## Current model

- Part 2 status: **complete for implementation; provisional for evidence**
- Valuation date: **September 1, 2026**
- Security: Home Depot common stock (NYSE: HD)
- Currency: USD; statements in USD millions
- Architecture: reported FY2025 → explicit five-year statements → signed FCFF → provisional WACC DCF → enterprise-to-equity bridge
- Current reproducible result: **$234.31 per diluted share, provisional**
- Current script: `home_depot_fcff_model.py`
- Exact command from the FIN 439 folder:

```bash
./.venv/bin/python home_depot_project_1_rebuild/home_depot_fcff_model.py
```

Part 3 command:

```bash
./.venv/bin/python home_depot_project_1_rebuild/part3_analysis.py
```

That script refreshes `05_part3_visible_output.txt`, so the dated inputs and results can be reviewed without running code.

## File map

| File | Purpose |
|---|---|
| `edition_a_unchanged.md` | Unchanged supervised baseline; never repaired retroactively |
| `00_architecture_audit.md` | Initial architecture and gap review |
| `01_base_year_reconciliation.md` | Filing-based FY2025 and debt reconciliation |
| `02_implementation_results.md` | Current visible output and validation record |
| `03_valuation_basis.md` | Part 2 valuation-date, WACC, bridge, shares, and normalization research; its earlier numeric run is superseded by the current explicit-schedule run |
| `04_part3_assumption_challenge_record.md` | Source-dated inputs, classifications, challenges, and evidence that would change them |
| `home_depot_fcff_model.py` | Only current executable rebuild model |
| `part3_analysis.py` | Scenarios, sensitivity, reverse DCF, P/E and EV/EBITDA comparables, and decision tests |
| `05_part3_visible_output.txt` | Executed Part 3 output visible without running code |
| `06_part3_validation_and_rubric_status.md` | Passed tests, outstanding evidence, and rubric map |
| `07_comparable_valuation.md` | Preserved peer policy, dated inputs, P/E and EV/EBITDA definitions, lease convention, results and limits |
| `08_locked_changed_input_record.md` | Frozen pre-run terminal-growth prediction, precommit, actual result, validation and decision effect |
| `09_part4_decision_and_evidence_map.md` | Watch/defer explanation, range distinctions, base-value reconciliation and complete requirement map |
| `10_locked_changed_input_blank.md` | Blank AI-off template and precommit instructions for any additional changed-input test |
| `11_ai_output_check.md` | Actual AI peer suggestion independently checked and qualified |
| `12_cold_run_instructions.md` | Fresh-environment commands and uncompleted recording checklist |
| `13_source_consistency_audit.md` | Source accessibility, dates, definitions and cross-file consistency audit |
| `benchmark_validation.py` | Published Week 3 twelve-output known-answer test |
| `14_training_benchmark_output.txt` | Visible passing benchmark result |
| `15_validation_and_ai_use_working.md` | Consolidated working validation/AI-use record; not yet a frozen PDF |
| `requirements.txt` | Standard-library-only environment declaration |

## Part 1 versus Part 2

- **Part 1:** established the reported FY2025 base, identified the omitted commercial paper, and linked operating forecasts to FCFF. The earlier $207.85 output belonged to that earlier assumption set and is not the current result.
- **Part 2/current:** uses a September 1 valuation basis, explicit working-capital and long-lived-asset schedules, latest public debt/share inputs, and the transparent but still provisional 8.1984% WACC. It produces $234.31.

The WACC change from 8.8% to 8.1984% is the main cause of the increase: it adds $27.45 per share in the sequential reconciliation. The schedule, share, debt, and cash changes net to a $0.99 decrease from $207.85 to $206.86 before the WACC change.

## Part 3 provisional decision

- Operating-case DCF range: **$220.99–$253.91 per diluted share**; scenario base **$234.00**.
- September 1, 2026 close: **$319.77**.
- Comparable references: **$240.00** from trailing GAAP P/E and **$217.21** from trailing GAAP EV/EBITDA. They are not averaged.
- Reverse DCF: **+6.23 percentage points** added uniformly to all five explicit total-growth rates reaches market price with printed inputs fixed.
- Action: **watch-defer**, conditional on price or evidence. WACC remains provisional.

The scenario base differs slightly from Part 2 because FY2026 now uses the midpoint of August 18 guidance and capex/margins are aligned to that evidence. Part 2 remains the architecture checkpoint; Part 3 is the decision-testing layer.

## Integrity boundaries

- Reported FY2025 is reproduced before any normalization.
- No unsupported numeric normalization is embedded.
- Failed required validations make the script exit unsuccessfully.
- Beta, marginal debt cost/tax, excess cash, exact diluted shares, the operating-lease rollforward, and several forecast drivers remain unresolved or provisional.
- No Edition A history, AI-off prediction, partner feedback, timestamp, or validation record has been invented.

Educational AI finance class work; not professional financial advice.
