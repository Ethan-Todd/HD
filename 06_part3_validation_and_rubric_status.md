# Part 3 — Validation and Rubric Status

## Automated results completed

The exact saved commands exited successfully on October 19, 2026:

```bash
./.venv/bin/python home_depot_project_1_rebuild/home_depot_fcff_model.py
./.venv/bin/python home_depot_project_1_rebuild/part3_analysis.py
```

Passed: FY2025 statement arithmetic and component sums; historical CFO + CFI + CFF and cash including FX; every scenario's forecast balance and cash tie; direct WACC comparison; enterprise-to-equity bridge; finance leases included once; debt dollar-for-dollar; signed negative FCFF; terminal boundary; WACC/growth monotonicity; independent-copy base rerun.

## Highest-risk claim tests

| Claim | Test and result | Limitation |
|---|---|---|
| Lower WACC caused the Part 2 increase | Sequential reconciliation passed: WACC step was +$27.45/share, the dominant change | WACC evidence remains provisional |
| Debt is not double-counted | CP + current debt + noncurrent debt; finance leases included once; $1,000m more debt lowered equity $1,000m | Market/carrying-value date convention remains |
| Scenarios are linked statements | Full model reran from fresh copies; balance and cash ties passed in all cases | Magnitudes remain forecasts |
| Negative FCFF is not hidden | Synthetic negative first-year FCFF remained signed in valuation | Test is not a forecast of an HD loss |
| Terminal boundary fails safely | Terminal growth equal to WACC returned invalid | Does not validate selected growth |

## Assignment evidence still outstanding

| Requirement | Status | What remains |
|---|---|---|
| Published training-case known-answer | **Outstanding** | Run and preserve the exact published Project 1 benchmark; ordinary HD execution is not a substitute |
| Independent source/definition check | **Partly complete** | SEC inputs were checked; student must designate the submitted load-bearing check in the frozen record |
| Pre-run directional test | **Outstanding human evidence** | Must be authored AI-off before execution |
| Locked Changed-Input Record | **Outstanding** | Human prediction, timestamp/commit, old/new units, expected/actual direction, decision effect, reconciliation |
| AI-output check | **Outstanding for frozen submission** | Independently test one actual AI claim and record accept/correct/qualify/reject plus exposed tool/model/version and date |
| Highest-risk failure test | **Code complete; demonstration outstanding** | Explain the chosen test in Video 2 |
| Recorded cold run | **Outstanding** | Current successful execution is not a recorded fresh-environment cold run |
| Edition A receipt | **Not created here** | Preserve the actual Brightspace receipt; Edition A file remains unchanged |
| Memo/deck, recordings, transcripts | **Deferred** | Complete after Part 3 review |

## Rubric-mapped checklist

| Rubric criterion | Completed | Remaining gap |
|---|---|---|
| Problem definition and decision usefulness | Buy-side user, no-position decision, HD, Sep. 1, 2026, USD/diluted basis, conditional watch-defer | Final Edition B and committee artifact |
| Data integrity and traceability | SEC base/debt/shares; dated guidance; challenge record | Beta, marginal debt cost/tax, dilution, excess cash, leases, scenario decomposition |
| Financial soundness and judgment | Linked statements → signed FCFF → WACC DCF; causal cases; EV and equity comps kept separate | Better WACC evidence and peer depth |
| Technical execution and usability | Standard-library scripts, failure status, visible output, deterministic rerun | Environment file and fresh-user cold run |
| Validation, sensitivity, reproducibility | Accounting/bridge/sign/boundary/monotonicity tests, grid, reverse DCF | Benchmark, Locked Record, frozen AI check, recorded cold run |
| Professional communication | README, source-linked record, visible output, limitations, action/triggers | Final artifacts and manifest |

## Provisional interpretation

The operating-case DCF range is **$220.99–$253.91** per diluted share versus the **$319.77** September 1 close. Peer references are **$240.00** from median P/E and **$217.21** from median EV/EBITDA; they are not averaged because the two-peer set is fragile and Tractor Supply is only qualified.

Provisional action: **watch-defer**. Initiation requires a price inside the supported range without deteriorating fundamentals, or sourced evidence supporting stronger organic growth and operating leverage; worse transactions, project demand, margins, or integration would move the action toward do-not-initiate.

The modeled downside does **not** change the current action: its $220.99 value widens the shortfall to market and makes immediate initiation less supportable. A still more severe sourced downside could change the action to do-not-initiate, but that case has not been invented here.

Educational AI finance class work; not professional financial advice.
