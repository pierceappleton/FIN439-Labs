# Lab 07 Project Context — Carry-Forward Notes from Prior Labs

Use this file with `lab-07-instructions.md`. Lab 07 practices P/E comparable-company valuation on the Asbury case first, but the reason it matters for the project is that Lab 08 will apply the same method to your own company: **Palantir Technologies Inc. (`PLTR`)**.

## Current Project Position

Your FIN439 project company is **Palantir Technologies Inc. (`PLTR`)**.

The working investment call from prior labs is **watch-defer**. That means Palantir stays on the research list, but the existing evidence does not yet support an initiate-buy decision. The operating story is strong; the valuation evidence still needs discipline.

Useful one-sentence version:

> Palantir has strong company-reported evidence of AIP and U.S. commercial momentum, but the current project should not become a buy call unless valuation work shows the market price is reasonable for the growth being assumed.

## What Prior Labs Already Established

### Lab 03 / Project 1 Baseline

- Company: Palantir Technologies Inc. (`PLTR`)
- Valuation date: `2025-12-31`
- Primary filing: Palantir 2025 Form 10-K
- SEC accession: `0001321655-26-000011`
- Filing date: `2026-02-17`
- Reporting period: fiscal year ended `2025-12-31`
- Currency: USD
- Filing units: thousands
- Current view: **watch-defer**

Key filing facts carried forward:

| Item | Prior-lab value | Why it matters |
| --- | ---: | --- |
| Cash and cash equivalents | `$1,423,796` thousand | Used in DCF enterprise-to-equity bridge |
| Debt | `$0` | No borrowings outstanding under credit facility |
| 2025 diluted shares | `2,565,197` thousand shares | Used for DCF per-share value and EPS/share-count context |
| 2025 revenue | `$4,475,446` thousand | Main growth evidence |
| 2024 revenue | `$2,865,507` thousand | Base for revenue growth comparison |
| 2025 operating cash flow | `$2,134,473` thousand | Starting point for FCFF logic |

The original unresolved question was whether Palantir should be valued mainly through growth, profitability, or cash generation. Lab 06 answered part of that by building a DCF around FCFF growth, but Lab 07 adds a market-comparison lens.

### Lab 04 Company Research

Lab 04 strengthened the company story but kept the call at **watch-defer**.

Business description to remember:

- Palantir builds software for integrating data, decisions, and operations at scale.
- Its major platforms are **Gotham**, **Foundry**, **Apollo**, and **AIP**.
- AIP is central to the current growth story because it connects organizations to large language models, AI agents, automations, governance, and production workflows.

Evidence of operating momentum from the Q2 2026 release:

| Evidence | Value |
| --- | ---: |
| Q2 2026 total revenue growth | `93%` year over year |
| Q2 2026 U.S. commercial revenue growth | `149%` year over year |
| Q2 2026 U.S. commercial revenue | `$764 million` |
| Q2 2026 U.S. commercial total contract value | `$2.132 billion`, up `153%` year over year |
| FY2026 revenue guidance | `$8.150 billion` to `$8.158 billion` |

The key gap Lab 04 identified was valuation. The report did not yet have a sourced DCF, multiple comparison, or independent risk evidence strong enough to support a buy call.

### Lab 05 Context

Lab 05 framed the next step as converting the research packet into a valuation argument. It said the most useful next valuation work would be:

1. A sourced valuation multiple comparison against relevant peers.
2. A DCF or scenario table tied to revenue growth, margin trajectory, free cash flow, and share dilution.
3. Independent risk evidence that challenges management's framing.
4. A clear decision rule for changing the call from watch-defer to initiate or do not initiate.

Lab 07 directly supports item 1 by practicing a P/E comparable-company method.

### Lab 06 DCF Result

Lab 06 built and verified a DCF for Palantir.

Important DCF inputs:

| Input | Value used | Notes |
| --- | ---: | --- |
| Starting FCFF | `$2,100.591 million` | 2025 operating cash flow minus capex; after-tax interest treated as zero because debt was zero |
| Explicit FCFF growth | `119%, 100%, 80%, 60%, 40%` | Forecast path informed by 2026 guidance and recent growth, then tapered |
| WACC | `10%` | Assignment estimate |
| Terminal growth | `3%` | Long-run nominal economy assumption |
| Cash | `$1,423.796 million` | From 2025 10-K |
| Debt | `$0.000 million` | From 2025 10-K debt note |
| Diluted shares | `2,565.197 million` | 2025 diluted weighted-average shares |
| Market price used | `$169.53` | Observed on 2026-09-10 |

DCF outputs to remember:

| Output | Result |
| --- | ---: |
| Base-case value per diluted share | `$158.16` |
| Market price used in reverse DCF | `$169.53` |
| Base value / market price | about `0.93x` |
| Reverse DCF uniform growth shift | `+2.58 percentage points` |
| PV of terminal value / enterprise value | `83.83%` |

Sensitivity grid from Lab 06, value per diluted share:

| WACC \ terminal growth | 2% | 3% | 4% |
| --- | ---: | ---: | ---: |
| 9% | `$163.88` | `$188.27` | `$222.42` |
| 10% | `$140.52` | `$158.16` | `$181.68` |
| 11% | `$122.45` | `$135.69` | `$152.70` |

Lab 06 bottom line:

- The DCF value was close enough to the market price to pass the assignment reasonableness check.
- The biggest concern was the growth path, because Palantir's recent AIP momentum is very strong but extending extremely high FCFF growth for five years puts a lot of value into the terminal value.
- The conditional call stayed **watch-defer**: initiate only if price falls below the base-case value, or if sourced evidence supports the growth path demanded by the current market price.

## What Lab 07 Adds

Lab 07 is about learning how a **P/E comparable-company analysis** works before applying it to Palantir.

A P/E multiple asks:

> How much is the market paying for one dollar of a company's earnings?

The Lab 07 Asbury case uses P/E to estimate what Asbury's share price might be if its EPS were valued at peer-company P/E multiples.

For your project, the equivalent future question will be:

> What would PLTR's share price imply if its EPS were valued at comparable software / AI infrastructure companies' P/E multiples?

## How This Differs from the Lab 06 DCF

Keep these methods separate:

| DCF from Lab 06 | P/E comps from Lab 07 |
| --- | --- |
| Values the company from forecast free cash flow | Values the company by comparing market prices to earnings |
| Uses WACC, terminal growth, cash, debt, and share count | Uses peer price per share and EPS |
| Produces an intrinsic-value estimate based on assumptions | Produces a market-implied comparison range |
| Sensitive to long-term growth and discount rate | Sensitive to peer selection and earnings quality |

Important rule from Lab 07:

> Never bridge P/E with cash/debt.

That means the Lab 06 cash/debt bridge belongs to the DCF. For a P/E exercise, use price per share and EPS. Do not add cash or subtract debt from the P/E-implied share price.

## Questions to Answer During Lab 07

When practicing on Asbury, focus on the logic you will need later for PLTR:

1. What business features make a peer truly comparable?
2. Does the peer have similar growth prospects, profitability, and risk?
3. Are earnings positive and meaningful?
4. Are earnings unusually high or low because of one-time items?
5. Does a lower P/E mean undervaluation, or could it reflect lower growth or higher risk?
6. What happens to the implied value range when one peer is removed?

## Palantir-Specific Issues for Later Peer Selection

Do not choose peers just because they are large technology companies. For PLTR, a stronger peer argument should consider:

- Enterprise software business model
- AI / data platform exposure
- Government and commercial customer mix
- Revenue growth rate
- Free cash flow margin and profitability
- Stock-based compensation and dilution
- Whether GAAP EPS is positive and stable enough for P/E to mean anything
- Whether the peer's growth/risk profile is close enough to Palantir's

Potentially relevant peer categories to research later:

- Enterprise software / data analytics platforms
- AI infrastructure or AI-enabled software companies
- High-growth profitable software companies
- Government-exposed software or defense-technology companies

Do not decide the peer set from this file alone. Lab 08 should use fresh, sourced evidence.

## Partner Explanation for Lab 07

Use this short explanation before AI help:

> My DCF says Palantir is worth about `$158.16` per share in the base case versus a `$169.53` observed price, so the market price needs only a modest positive growth shift to fit my model. But the DCF depends heavily on aggressive FCFF growth and terminal value. Lab 07 adds a peer-multiple check: instead of forecasting cash flows directly, it asks what price would be implied if a company's EPS were valued like comparable companies' EPS. The hard part is not the math; it is choosing peers that are comparable in business, growth, profitability, and risk.

## Lab 07 Deliverable Reminder

For today's Asbury checkout, you need to be able to explain:

- What P/E measures.
- Why a lower P/E is not automatically better.
- Why AutoNation and Group 1 are used, qualified, or excluded in the Asbury case.
- How the peer median P/E creates an implied price.
- Why removing the higher-multiple peer changes the implied estimate and removes the range when only one peer remains.

For your Palantir project, save the lesson:

> Comparable-company valuation is only as good as the peer policy. The calculation is easy; the judgment is in whether the companies actually deserve to be compared.

## Existing Source Trail to Reuse Later

Local files already created:

- `labs/lab-03/Project1_EditionA_Palantir.md`
- `labs/lab-04/Lab04_Company_Research_Report_Palantir.md`
- `labs/lab-04/sources.md`
- `labs/lab-05/Lab05_Palantir_Context.md`
- `labs/lab-06/lab06_dcf.md`
- `labs/lab-06/dcf.py`

Core sources already identified:

- Palantir 2025 Form 10-K, SEC accession `0001321655-26-000011`, filed `2026-02-17`
- Palantir 2024 Form 10-K, filed `2025-02-18`
- Palantir 2023 Form 10-K, filed `2024-02-20`
- Palantir Q2 2026 earnings release, dated `2026-08-03`
- Palantir Investor Relations Events page for the Q2 2026 earnings event
- Investing.com PLTR market data used in Lab 06 for the `$169.53` observed price on `2026-09-10`

This file is a working class note, not investment advice.
