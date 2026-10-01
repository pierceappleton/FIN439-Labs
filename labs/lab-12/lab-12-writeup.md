# Lab 12: Present and Review the Full Analysis — Palantir Technologies (PLTR)

Pierce Appleton  
Partner: Ethan Heeres  
Date: October 1, 2026  
Role (A/B): _[fill in class]_

No new computation in this lab. Everything below points to work and output already in the repo. Part 1 is my presentation route, prepared before class. Parts 2–4 get filled in during class with AI closed.

## D — The question

> How did I get from choosing this company to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?

**Current conclusion (open with this):** watch-defer. My Lab 10 pro forma gives $34.53 per diluted share (FCFE, 11% cost of equity, 3% terminal growth, 2,565.197M diluted shares, USD). The PLTR close on 2026-09-24 was $192.59. My model only gets near the price if revenue grows much faster for much longer than my base path. Lab 11 showed revenue growth is the input that moves value the most. Over the ranges I tested, though, it still doesn't get anywhere close to the price.

## Files to have open

| Stop | File | Run |
|---|---|---|
| Selection | [Lab 03 Edition A](../lab-03/Project1_EditionA_Palantir.md) | none |
| Evidence | [Lab 04 report](../lab-04/Lab04_Company_Research_Report_Palantir.md), [research/pltr report](../../research/pltr/Palantir_2026-09-03_report.md), [sources](../../research/pltr/sources.md) | none |
| Pro forma | [Lab 10 writeup](../lab-10/lab-10-writeup.md), [pltr_proforma.py](../lab-10/pltr_proforma.py) | `python pltr_proforma.py` |
| Valuation | [Lab 06 DCF](../lab-06/lab06_dcf.md), [Lab 08 peer P/E](../lab-08/lab08_palantir_pe_triangulation.md) | `python dcf.py`, `python lab08_palantir_comps.py` |
| Sensitivity | [Lab 11 writeup](../lab-11/lab-11-writeup.md), [pltr_sensitivity.py](../lab-11/pltr_sensitivity.py) | `python pltr_sensitivity.py` |

I re-ran `pltr_sensitivity.py` before class. The restored base still matches Lab 10 ($10,547.8M 2030 operating profit, $10,923.6M 2030 FCFE, $34.53/share), and every check passes.

## Part 1 — Presentation route (15 minutes)

### 1. Target selection (~2 min)

- **Why Palantir:** it's a large, liquid U.S. company with clean SEC filings, no debt, and a business that changed fast. It went from a government-origin data platform to a commercial AI story through AIP. That gives me a real question to test: is the growth durable enough to justify the price?
- **Why it's suitable to analyze:** zero debt makes the enterprise-to-equity bridge simple (cash minus $0 debt). The 10-K gives clean diluted shares (2,565.197M), and three years of statements are easy to source.
- **Initial view (Lab 03, valuation date 2025-12-31):** watch-defer. At that point I didn't know whether the right framing was growth, profitability, or cash generation (Lab 03 "Unknowns").

### 2. Company and evidence (~2 min)

- **How it earns money:** software platforms (Gotham, Foundry, Apollo, AIP) sold to government and commercial customers. Customers often pay before the work is delivered, so contract liabilities were $812.3M at FY2025 year-end. (FY2025 10-K, Item 1 p. 11; balance sheet)
- **Facts that matter most, with source, period and units:**
  - FY2025 revenue $4,475,446 thousand, up from $2,865,507 thousand (+56.2%). FY2025 10-K, Statements of Operations p. 86, USD thousands.
  - $1,199.2M of the $1,610M 2025 revenue increase came from existing customers. FY2025 10-K MD&A, USD millions.
  - FY2026 revenue guidance $8.150–8.158B; Q2 2026 revenue +93% y/y, U.S. commercial +149%. Q2 2026 release, 2026-08-03.
  - Cash $1,423.8M plus marketable securities $5,753.2M; debt $0. FY2025 10-K balance sheet and debt note, at 2025-12-31.
  - SBC $684.0M (15.3% of revenue); tax rate 1.4% because of NOLs behind a valuation allowance. FY2025 10-K cash flow statement and tax note.
- **Gap I'll admit:** most of my growth evidence is company-reported. Lab 04 noted I have no independent analyst source challenging management's framing.

### 3. My pro forma (~3 min)

- **History → assumptions** (Lab 10 table): 2026 growth 82.2% = guidance midpoint (labeled guidance). 2027–2030 tapers 45/32/25/20% (judgment: each point of growth costs more dollars as the base gets bigger). Gross margin 82% (judgment: just under the 2025 82.4% because AIP compute sits in cost of revenue).
- **Company-specific drivers:**
  - Contract liabilities at 18.15% of revenue replace ABG's floor plan. Customer prepayments fund working capital, adding about $0.67–0.71B of cash each year.
  - SBC is subtracted from valuation FCFE because dilution is a real cost to owners.
  - Tax steps from 5% up to 21% as the NOLs run out around 2028.
- **Linked statements and checks:** opening balance sheet ties to the 10-K ($8,900.4M = $8,900.4M). Balance, cash tie, PP&E, debt and equity roll-forwards all print `OK, gap 0.0` every year. The refusal test (removing the contract-liability increase from FCFE) broke the balance by exactly −667.7. The revolver is never drawn.

### 4. Valuation (~3 min)

Every value below is in USD per diluted share, on 2,565.197M diluted shares.

| Method | Date | Result | Key assumptions | Main limitation |
|---|---|---:|---|---|
| Lab 06 FCFF DCF | 2026-09-10 | $158.16 | FCFF growth 119/100/80/60/40%, WACC 10%, g 3%, + cash $1,423.8M − debt $0 | Growth path set on FCFF directly; SBC not deducted; 83.8% of EV is terminal value |
| Lab 06 reverse DCF | 2026-09-10 | price $169.53 needs a +2.58pp uniform growth shift | starting FCFF, WACC, g, cash, debt, shares held fixed | Only solves a uniform shift on an already aggressive path |
| Lab 08 peer P/E | 2026-09-10 | $49.48–$450.59, median $250.04 | DDOG 715.2x, NOW 78.5x × PLTR GAAP diluted EPS $0.63 | Two peers; DDOG's tiny EPS makes the range useless as a point estimate. SNOW and AI were excluded because P/E isn't meaningful with negative EPS |
| Lab 10 FCFE pro forma | 2026-09-24 | $34.53 | Revenue-driven statements, cost of equity 11%, g 3%, SBC deducted, + cash and securities $7,177.0M − NCI $100.7M | 70.2% of value comes after 2030; growth is still 20% in year five when 3% terminal growth kicks in |
| Market price | 2026-09-24 | $192.59 | Yahoo Finance regular-session close | none |

- **Why the methods disagree (and why I won't average them):**
  - Lab 06 forecast FCFF to grow about 18x in five years and ignored SBC.
  - Lab 10 builds cash flow up from revenue and margins, then subtracts SBC and interest income. That's a much lower cash-flow path.
  - P/E prices current GAAP EPS off two peers with very different earnings maturity.
  - These are different questions, not noisy estimates of one number. Lab 10 is the method I can trace line by line, so it's my anchor.
- **Reverse-DCF limitation:** I have only run a reverse DCF on the Lab 06 FCFF model. I haven't run one on the Lab 10 pro forma. The scale tests in Lab 10 (60/45/35/30% growth → $46.15; 5% terminal growth → $43.25) show neither assumption alone closes the gap to $192.59. That reverse DCF is unresolved work, not a result.

### 5. Sensitivity and drivers (~3 min)

Base vs. higher revenue growth, computed in Lab 11 and shown live from `pltr_sensitivity.py`:

| Step | Base | Higher (+10pp every year) | Change |
|---|---:|---:|---:|
| Input: growth 2026–2030 | 82.2/45/32/25/20% | 92.2/55/42/35/30% | +10pp |
| 2030 revenue ($M) | 23,410.9 | 33,226.7 | +9,815.8 |
| 2030 gross profit ($M) | 19,196.9 | 27,245.9 | +8,049.0 |
| 2030 operating income ($M) | 10,547.8 | 14,987.8 | +4,440.0 |
| 2030 net income ($M) | 9,238.8 | 12,881.2 | +3,642.4 |
| 2030 FCFE ($M) | 10,923.6 | 15,174.7 | +4,251.1 |
| 2030 valuation FCFE ($M) | 8,144.7 | 11,475.7 | +3,331.0 |
| Value per share | $34.53 | $46.27 | +$11.74 |

- **Causal path:** input → revenue compounds on a bigger base each year → gross profit → operating income (opex scales partly with gross profit and revenue) → net income → FCFE. Working capital partly offsets: receivables +$1,680.6M against contract liabilities +$1,391.6M in 2030. Then SBC is subtracted to get valuation FCFE, and the larger 2030 cash flow feeds the terminal value.
- **Ranking:** over the tested ranges, revenue growth ($20.70/share span) beats gross margin ($3.00 span). The ranges aren't equal, though: ±10pp on five yearly inputs vs. ±3pp on one margin. So the ranking describes my ranges, not a universal law.
- **What it doesn't establish:** these are conditional scenarios, not probabilities. Even the higher-growth case ($46.27) is about a quarter of the $192.59 price.
- **Impact vs. uncertainty:** the $20.70 span measures *impact*: how much value moves if growth lands at either edge of my range. It says nothing about how *likely* those edges are. Growth is also the more uncertain input (2025 growth was 56%, Q2 2026 was 93%, my 2030 base is 20%), but that's a separate judgment from the table, not something the table proves.
- **Prediction miss:** I predicted a $5–6B span and got $7.8B, because the change compounds.

### 6. Interpretation (~2 min)

- **Conditional recommendation:** watch-defer, not initiate. This is a learning exercise, not investment advice. On my traceable model, the price implies growth well beyond my higher case, sustained past 2030. I'd become more constructive if:
  - the price fell toward a value my model supports, or
  - evidence showed growth staying above roughly 30% after 2027 with SBC continuing to fall as a share of revenue.
- **What would change it toward "do not initiate":** U.S. commercial growth slowing sharply, contract liabilities ÷ revenue continuing to drift down (21.9% → 18.1%), or SBC dollars re-accelerating.
- **How my view changed:**
  - In Lab 03 I didn't know which framing mattered.
  - In Lab 06 my DCF ($158) sat close to the price.
  - Building the statements in Lab 10 showed the earlier DCF was carrying an unsupported cash-flow path and leaving out SBC.
  - The call stayed watch-defer, but my confidence in *why* is much higher.
- **Evidence to investigate next:** a reverse DCF on the Lab 10 pro forma (what growth path or terminal growth equates to $192.59?), and a growth range scaled to match the margin range so the driver ranking is fair.

## Part 2 — As presenter: questions received

_Fill in during class. Write Ethan's actual questions and my actual answers. If I can't answer, write the gap and how I'd resolve it. Don't fill gaps with AI._

| Area | Ethan's question | My answer, or the specific unresolved gap and how to resolve it |
|---|---|---|
| Selection and evidence | | |
| Model and valuation | | |
| Sensitivity and interpretation | | |
| Follow-up | | |

**Evidence checked together** (source opened or calculation traced): _[what, and whether it supported the claim]_

**Ethan's explain-back** (conclusion / main driver / biggest limitation): _[record; note any correction I made]_

**Strength Ethan identified:** _[ ]_  
**Improvement Ethan suggested:** _[ ]_

## Part 3 — As reviewer: Ethan's company

Company: _[ ]_

Questions to adapt once I've heard his actual numbers. They have to use his company, assumptions and results:

- **Selection and evidence:** why this company over the others you considered? Which filing and page supports your most important revenue or margin fact, and what units is it in?
- **Model and valuation:** walk me from your biggest judgment assumption to value per share. Why do your DCF and peer result disagree, and which one do you trust more?
- **Sensitivity and interpretation:** if you gave your second driver the same-sized range as your first, would the ranking flip? What sourced evidence would move your call?

| Area | Question I asked | His answer | Follow-up / gap |
|---|---|---|---|
| Selection and evidence | | | |
| Model and valuation | | | |
| Sensitivity and interpretation | | | |

**Source or calculation I checked:** _[what I opened or traced, input → output]_  
**Result:** _[supported / not supported / partly, with numbers]_

**My explain-back:**
- Valuation conclusion: _[ ]_
- Main driver: _[ ]_
- Biggest limitation: _[ ]_
- His correction, if any: _[ ]_

**Strength (evidence-backed):** _[ ]_  
**Improvement (specific, next step):** _[ ]_

## Part 4 — Keep, revise, investigate

_Finalize after both rounds. The candidates below are what I expect going in. Update them based on what the review actually raised._

| Decision | Item | Reason |
|---|---|---|
| Keep | Lab 10 pro forma as the valuation anchor | Linked statements, passing checks, and a refusal test; every number traces to the 10-K or a labeled assumption |
| Keep | Watch-defer call | The base and the higher-growth case are both far below the $192.59 price |
| Revise | Lab 06 FCFF DCF framing | It set the growth path on FCFF directly and didn't deduct SBC. Either retire it or present it as a market-implied scenario |
| Investigate | Reverse DCF on the Lab 10 model | I don't yet know what growth or terminal path the price implies in my own model |
| Investigate | Equal-range sensitivity | The current ranking depends on unequal ranges |
| Investigate | Independent source on AIP demand durability | Growth evidence is mostly company-reported (Lab 04 gap) |

**Does the review change my conclusion or research priority?** _[State yes/no and why. If it doesn't change, explain why the evidence still holds. Don't claim a model fix I haven't run.]_

## Reflect

**The question that made me reconsider something:** _[ ]_  
**What I now understand better about Palantir:** _[ ]_

## Files

GitHub links for checkout:

- [lab-12-writeup.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-12/lab-12-writeup.md)
- Lab 11: [pltr_sensitivity.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-11/pltr_sensitivity.py), [lab-11-writeup.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-11/lab-11-writeup.md)
- Lab 10: [pltr_proforma.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-10/pltr_proforma.py), [lab-10-writeup.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-10/lab-10-writeup.md)
- Lab 08: [lab08_palantir_comps.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-08/lab08_palantir_comps.py), [lab08_palantir_pe_triangulation.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-08/lab08_palantir_pe_triangulation.md)
- Lab 06: [dcf.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-06/dcf.py), [lab06_dcf.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-06/lab06_dcf.md)
- Lab 04: [Lab04_Company_Research_Report_Palantir.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-04/Lab04_Company_Research_Report_Palantir.md)
- Lab 03: [Project1_EditionA_Palantir.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-03/Project1_EditionA_Palantir.md)
- Research: [Palantir_2026-09-03_report.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/research/pltr/Palantir_2026-09-03_report.md), [sources.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/research/pltr/sources.md)
