# Lab 08 Context From Previous FIN439 Labs

Use this file as the handoff context before completing Lab 08. The target company throughout the prior work is Palantir Technologies Inc. (`PLTR`).

## Current Target And Prior Call

- Target: Palantir Technologies Inc.
- Ticker: `PLTR`
- Current research stance from Lab 04 and Lab 06: `watch-defer`.
- Reason: Palantir shows strong operating momentum, especially around AIP and U.S. commercial growth, but the prior work still needs stronger valuation discipline and peer evidence before supporting an initiate decision.

## Key Filing And Company Context

- Primary company filing used earlier: Palantir 2025 Form 10-K, accession `0001321655-26-000011`, filed `2026-02-17`, reporting period ended `2025-12-31`.
- SEC filing link used in prior labs: https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm
- Business model summary from prior labs: Palantir provides software platforms for government and commercial customers. Earlier filings described Gotham, Foundry, Apollo, and AIP as principal platforms for integrating data, decisions, and operations at scale.
- Report currency: USD.
- Diluted share convention used earlier: weighted-average diluted shares used in computing diluted EPS.
- Prior diluted shares input: `2,565.197` million for FY2025.
- Prior cash input: `$1,423.796` million as of 2025-12-31.
- Prior debt input: `$0.000` million, because the 2025 10-K indicated no outstanding debt balances under the credit facility at year-end.

## Lab 06 DCF Inputs And Results

- Model date / valuation date used in Lab 06: `2026-09-10`.
- Units: USD millions except per-share amounts and share count.
- Starting FCFF: `2,100.591` million, calculated from FY2025 operating cash flow less purchases of property and equipment.
- Five-year FCFF growth path: `119%, 100%, 80%, 60%, 40%`.
- WACC: `10%`.
- Terminal growth: `3%`.
- Cash: `$1,423.796` million.
- Debt: `$0.000` million.
- Diluted shares: `2,565.197` million.
- Base-case DCF value per diluted share: `$158.1618`.
- Market price used for the reverse DCF: `$169.53` for `PLTR`, observed on `2026-09-10`.
- Sensitivity grid from Lab 06:

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 163.88 | 188.27 | 222.42 |
| 10% | 140.52 | 158.16 | 181.68 |
| 11% | 122.45 | 135.69 | 152.70 |

- Lab 06 conditional call: `watch-defer`. Initiate only if the price falls below the base-case value per share, roughly below `$158`, or if sourced evidence supports the growth path demanded by the current price.

## Lab 07 Comparable-Company Calculator Context

Lab 07 built a P/E comparable-company calculator for the Asbury case. The reusable file is:

- `../lab-07/lab07_comps.py`

Important calculator behavior:

- Edit `TARGET` and `PEERS` at the top of the file.
- It uses price per share and GAAP diluted EPS only.
- It excludes the target if accidentally listed as a peer.
- It ignores peers with non-positive or missing price/EPS for P/E calculations.
- It prints peer P/E calculations, the median peer P/E, an implied target range or single-peer reference, and leave-one-out sensitivity.
- It does not use a cash/debt bridge.

Lab 07 saved command:

```powershell
python lab07_comps.py
```

Lab 07 Asbury known check:

- AutoNation P/E: `10.037825x`.
- Group 1 Automotive P/E: `11.450149x`.
- Peer median P/E: `10.743987x`.
- Asbury peer-implied range: `$215.81-$246.18`.
- Asbury median-implied price: `$231.00`.
- Removing GPI left a single-peer reference of `$215.81`.

## Lab 08 Starting Judgment

For Lab 08, do not mechanically reuse Asbury. The new task is to build and defend a peer P/E comparison for Palantir and compare it with the Week 3 / Lab 06 DCF result.

Initial peer policy to test and revise only with explanation:

> A useful peer for Palantir should be a listed operating company that sells enterprise software or data/AI platforms with recurring or durable customer relationships, meaningful commercial or government enterprise exposure, and positive annual reported diluted EPS available before the `2026-09-10` comparison date. Differences to qualify include cloud/SaaS delivery model, customer mix, growth maturity, margin structure, government exposure, and whether the company is mainly infrastructure software, analytics software, cybersecurity, or application software. Exclude companies that are not operating companies, have materially different economics, lack positive annual reported diluted EPS, report incompatible share/currency bases that cannot be reconciled, or cannot be supported by opened primary/company sources.

Evidence that should reject or qualify a candidate:

- Reject if the source does not support a real business-model overlap with Palantir.
- Reject or mark unresolved if annual diluted EPS public by `2026-09-10` cannot be verified.
- Qualify if the company is comparable as enterprise software but differs materially in growth, government exposure, product scope, profitability, or maturity.
- Keep excluded candidates in the source table with the reason.

## Sources To Reopen

- Palantir 2025 Form 10-K: https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm
- Palantir Investor Relations, Q2 2026 materials from `2026-08-03`: https://investors.palantir.com/news-details/2026/Palantir-Reports-
- Nasdaq market activity starting page: https://www.nasdaq.com/market-activity/stocks
- SEC company search: https://www.sec.gov/edgar/search/

## Lab 08 Output Needed

The final Lab 08 work should include:

- Explicit target, comparison date, and peer policy before selection.
- Two sourced candidate decisions: `use`, `qualify`, or `exclude`.
- Target and peer prices on the same trading date.
- Annual reported diluted EPS, fiscal year-end, publication date, and source locator.
- Calculator output for Palantir using only candidates marked `use` or `qualify`.
- Hand check of one admitted peer's price divided by EPS.
- Leave-one-out prediction and calculator result.
- DCF vs peer P/E comparison table.
- Skeptical AI criticism with `accept`, `reject`, or `unresolved` judgment.
- Final action: `initiate`, `watch-defer`, or `do not initiate`, with the evidence that would change the decision.
