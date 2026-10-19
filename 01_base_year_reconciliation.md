# FY2025 Base-Year and Debt Reconciliation

Primary source: Home Depot Form 10-K for the 52 weeks ended February 1, 2026, filed March 18, 2026. Units are USD millions except per-share data.

## Reported income statement

| Line | FY2025 reported | Model use |
|---|---:|---|
| Net sales | 164,683 | Base-year revenue |
| Cost of sales | 109,818 | Historical gross-margin and working-capital analysis |
| Gross profit | 54,865 | Reconciles to net sales less cost of sales |
| SG&A | 30,702 | Operating-expense history |
| Depreciation and amortization presented as operating expense | 3,273 | Reconciles reported operating income |
| Operating income | 20,890 | 54,865 − 30,702 − 3,273 |
| Interest income and other, net | (124) | Keep separate from operating income and the preliminary debt cost |
| Interest expense | 2,412 | Financing expense; excluded from FCFF but used to check debt cost |
| Pretax income | 18,602 | Reported |
| Income-tax provision | 4,446 | Reported |
| Effective tax rate | 23.9007% | 4,446 ÷ 18,602; preliminary normalized tax-rate anchor |
| Net earnings | 14,156 | Reported |
| Diluted weighted-average shares | 995 | Historical EPS denominator, not automatically the valuation-date denominator |
| Diluted EPS | 14.23 | Reported |

## Cash-flow definitions that must remain distinct

| Line | FY2025 reported | Treatment |
|---|---:|---|
| Cash from operations | 16,325 | Historical cash-flow fact, not a substitute for forecast operating drivers |
| Depreciation and amortization excluding intangible amortization | 3,514 | Noncash addback disclosed in the cash-flow reconciliation |
| Intangible-asset amortization | 607 | Separate noncash addback |
| Total cash-flow D&A/addback | 4,121 | 3,514 + 607; preliminary FCFF addback history |
| Capital expenditures | 3,679 | Recurring investment line; acquisition payments are excluded |
| Payments for acquired businesses | 5,410 | Investing cash flow, but not recurring capex in FCFF |

The $3,273 million income-statement D&A line and $4,121 million total cash-flow D&A/addback are not interchangeable. Some depreciation is embedded in other operating lines, including cost of sales. The rebuilt model must reconcile operating income using the income-statement presentation while adding back total noncash D&A when calculating FCFF.

## Reported balance sheet

| Assets | FY2025 |
|---|---:|
| Cash and cash equivalents | 1,389 |
| Receivables, net | 5,597 |
| Merchandise inventories | 25,817 |
| Other current assets | 1,588 |
| Net PP&E | 28,021 |
| Operating-lease right-of-use assets | 9,204 |
| Goodwill | 22,344 |
| Intangible assets, net | 10,329 |
| Other assets | 806 |
| **Total assets** | **105,095** |

| Liabilities and equity | FY2025 |
|---|---:|
| Short-term debt / commercial paper | 4,464 |
| Accounts payable | 11,491 |
| Accrued salaries | 2,529 |
| Sales taxes payable | 508 |
| Deferred revenue | 2,575 |
| Income taxes payable | 114 |
| Current installments of long-term debt | 4,967 |
| Current operating-lease liabilities | 1,418 |
| Other accrued expenses | 4,358 |
| Long-term debt, excluding current installments | 46,341 |
| Long-term operating-lease liabilities | 8,160 |
| Deferred income taxes | 2,845 |
| Other long-term liabilities | 2,512 |
| Stockholders' equity | 12,813 |
| **Total liabilities and equity** | **105,095** |

Base-year balance check: **$105,095 − $105,095 = $0**.

## Debt perimeter

| Debt component | Amount | Preliminary bridge treatment |
|---|---:|---|
| Short-term debt / commercial paper | 4,464 | Include as financing debt |
| Current installments of long-term debt | 4,967 | Included in Note 5 total long-term debt |
| Long-term debt, excluding current installments | 46,341 | Included in Note 5 total long-term debt |
| **Note 5 total long-term debt** | **51,308** | Include; contains current installments and finance-lease obligations |
| **Total financing debt** | **55,772** | 4,464 + 51,308 |
| Cash and cash equivalents | (1,389) | Preliminary conventional cash addback; operating/excess-cash treatment remains a challenge item |
| **Preliminary net debt** | **54,383** | 55,772 − 1,389 |

The original `dcf.py` subtracts only $51,308 million. It therefore omits $4,464 million of short-term debt and overstates equity value by $4,464 million, or approximately $4.49 per share using 995 million shares, before considering any other model changes.

Operating-lease liabilities total $9,578 million and are excluded from this preliminary debt perimeter because lease costs remain inside operating expenses. If leases are later capitalized in the valuation or peer multiple, EBIT/EBITDA and enterprise value must be adjusted consistently to avoid double counting.

## Historical FCFF cross-check

Using the reported effective tax rate:

`FCFF = CFO + interest expense × (1 − tax rate) − capex`

`FCFF = 16,325 + 2,412 × (1 − 23.9007%) − 3,679 = 14,481.5`

The original DCF uses $14,443.4 million, which implies a different tax rate. The rebuild will not carry either number forward mechanically; forecast FCFF will be generated from projected operating statements. This historical calculation is retained as a definition check.

## Base-year contamination catalog

| Item | Classification | Why it matters | Current status |
|---|---|---|---|
| SRS acquisition | Basis change | FY2025 includes a full year of SRS while FY2024 includes only a partial year | Disclosed; exact organic/acquired profit split unresolved |
| GMS acquisition | Basis change | FY2025 includes GMS only after September 4, 2025 | Disclosed; stand-alone operating profit and FCFF unresolved |
| FY2024 53rd week | Calendar difference | Distorts FY2025-versus-FY2024 reported growth | Disclosed; normalized comparison not yet computed |
| Acquired-intangible amortization | Acquisition-related noncash expense | Affects reported operating income and comparability | Amounts exist in disclosures; normalization policy not yet selected |
| Fiscal 2024 legal-related benefit | One-time comparison item | Makes FY2025 SG&A growth look worse against a benefited prior year | Disclosed; amount and normalization unresolved |
| Acquisition payments | Nonrecurring investing item | Must not be classified as recurring capex in FCFF | Separated from capital expenditures |

No unresolved item above is silently normalized. Each requires evidence and an explicit policy before Edition B is finalized.

