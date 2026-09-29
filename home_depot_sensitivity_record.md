# Home Depot Locked Changed-Input Record

Locked before sensitivity runs: **2026-09-29 17:32:21 EDT**

Model: `home_depot_proforma.py`  
Currency and scale: **USD millions**, except value per share in **USD per diluted share**.  
Cash-flow definition: **FCFE before discretionary revolver/commercial-paper paydown**, consistent with the model's printed FCFE line.  
Testing rule: change one independent driver at a time and hold every other input fixed.

## Driver ranges

| Driver | Lower | Base | Higher | Units | Affected years | Range reason |
|---|---:|---:|---:|---|---|---|
| Gross margin | 32.9% each year | 33.4% each year | 33.9% each year | Gross profit as a percentage of revenue; lower/higher are −0.5/+0.5 percentage-point shifts from base | FY2026E–FY2030E | Labelled judgment around Home Depot's stable historical gross margins of 33.38%, 33.42%, and 33.32%. The wider half-point range tests merchandise mix, shrink, tariffs, and supply-chain execution. |
| SG&A efficiency | 54.0% each year | 56.0% each year | 58.0% each year | SG&A as a percentage of gross profit; lower/higher are −2.0/+2.0 percentage-point shifts from base | FY2026E–FY2030E | Labelled judgment informed by Home Depot's ratios of 52.19%, 53.93%, and 55.96% in FY2023–FY2025. The range tests partial expense recovery versus further cost deleverage; a lower ratio is more efficient. |

## Outputs used for every run

| Output | Definition | Units |
|---|---|---|
| Final-year operating profit | FY2030E operating income | USD millions |
| Final-year free cash flow | FY2030E FCFE before discretionary revolver/commercial-paper paydown | USD millions |
| Value per share | FCFE equity value divided by 995 million diluted shares | USD per diluted share |

Current base outputs are FY2030E operating profit **$23,727.7 million**, FY2030E FCFE **$13,946.2 million**, and value per share **$208.88**.

## Locked predictions

### Gross margin

**Old → low:** 33.4% → 32.9% for FY2026E–FY2030E, a **−0.5 percentage-point shift in every year**. I expect FY2030E operating profit to fall by roughly $400 million, FY2030E FCFE to fall by roughly $300 million before working-capital effects, and value per share to decline by roughly $4–$6 because less of every revenue dollar becomes gross profit.

**Old → high:** 33.4% → 33.9% for FY2026E–FY2030E, a **+0.5 percentage-point shift in every year**. I expect FY2030E operating profit to rise by roughly $400 million, FY2030E FCFE to rise by roughly $300 million before working-capital effects, and value per share to increase by roughly $4–$6 because more of every revenue dollar becomes gross profit.

### SG&A efficiency

**Old → low:** 56.0% → 54.0% of gross profit for FY2026E–FY2030E, a **−2.0 percentage-point shift in every year**. Because a lower ratio is more efficient, I expect FY2030E operating profit to rise by roughly $1.2 billion, FY2030E FCFE to rise by roughly $0.9 billion after tax, and value per share to increase by roughly $12–$15.

**Old → high:** 56.0% → 58.0% of gross profit for FY2026E–FY2030E, a **+2.0 percentage-point shift in every year**. Because a higher ratio consumes more gross profit, I expect FY2030E operating profit to fall by roughly $1.2 billion, FY2030E FCFE to fall by roughly $0.9 billion after tax, and value per share to decline by roughly $12–$15.

## Partner check before running

- Confirm gross-margin changes are **percentage-point shifts**, not percent changes.
- Confirm SG&A-efficiency changes are **percentage-point shifts**, not percent changes, and that lower means more efficient.
- Confirm each run changes only gross margin **or** SG&A efficiency, never both.
- Confirm all money outputs are USD millions except value per share.
- Confirm the same FY2030E outputs and FCFE definition are recorded for every run.

Created for an AI finance class. This is not professional financial advice.

## Actual changed result and trace

Selected run: **SG&A efficiency — Lower**. The only changed independent input is SG&A as a percentage of gross profit: **56.0% → 54.0% in FY2026E–FY2030E**, a decrease of 2.0 percentage points each year. Lower is more efficient. The program's exact input comparison reports `changed_keys = ["sga_ratio"]`; revenue growth remains 2.5%, gross margin remains 33.4%, and every other independent input equals the base set.

| Output | Base | Changed result | Recomputed change |
|---|---:|---:|---:|
| FY2030E operating profit | $23,727.7M | $24,972.3M | $24,972.3M − $23,727.7M = **+$1,244.6M** |
| FY2030E FCFE | $13,946.2M | $14,894.0M | $14,894.0M − $13,946.2M = **+$947.8M** |
| Value per diluted share | $208.88 | $222.24 | $222.24 − $208.88 = **+$13.36** |

Accounting checks for the changed run: the maximum absolute assets-minus-liabilities-minus-equity gap is **$0.0M**, and cash stays at or above the $1,500.0M floor in every year. The run is valid.

Statement trace: FY2030E revenue and gross profit remain unchanged at $186,323.7M and $62,232.1M. Applying 54.0% instead of 56.0% lowers FY2030E SG&A by $1,244.6M, so operating profit rises by the same $1,244.6M; the higher after-tax earnings then flow into FCFE and equity value while the linked debt, interest, cash, and revolver balances recalculate.

## Prediction check

The locked prediction was approximately **+$1.2B** of FY2030E operating profit, **+$0.9B** of FY2030E FCFE, and **+$12 to +$15 per share**. Actual changes were +$1.2446B, +$0.9478B, and +$13.36 per share, so the direction was correct and value per share fell inside the predicted range; the small differences from the rounded operating-profit and FCFE estimates arose from using exact linked values and recalculating interest and financing balances.

## Valuation conclusion and research priority

The result does **not** change the provisional valuation conclusion: even the more efficient 54.0% SG&A case produces $222.24 per share, above the $208.88 base but below the market-price comparison used in the analysis. It does change the emphasis of the research priority: SG&A execution deserves closer attention because its $27.87 full sensitivity span is larger than the $9.51 gross-margin span.

## Partner-model check and role swap

Partner model check: **unresolved — the partner's file or printed run has not been provided.** When acting as listener, verify the partner's changed output minus base calculation, confirm that exactly one independent input differs from base, inspect the accounting checks, and ask: **“Can you trace the changed driver through gross profit or SG&A, operating income, taxes, FCFE, and value per share?”** Record any correction only after inspecting that evidence; none is asserted without the partner's model.
