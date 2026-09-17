# FIN439 Lab 08 - Palantir Peer P/E Valuation

Company: Palantir Technologies Inc. (`PLTR`)  
Valuation date: `2026-09-10`  
Prior Lab 06 DCF value: `$158.1618` per diluted share  
Observed market price from Lab 06 prompt: `$169.53`  
Valuation object: value per diluted share using annual reported GAAP diluted EPS and same-date or nearest defensible share prices.

## Starting Peer Policy

A useful peer for Palantir should be a publicly listed operating company with enterprise software, data, AI, analytics, cloud platform, observability, security, or workflow economics; durable customer relationships; and positive annual reported diluted EPS available before `2026-09-10`. I exclude candidates with non-positive annual GAAP diluted EPS because a P/E multiple is not meaningful when the denominator is zero or negative. I also reject or qualify companies when the business model is too application-specific, too broad, or when the stock price and EPS basis cannot be matched.

The candidate set requested for this lab was `SNOW`, `DDOG`, `AI`, `CRM`, and `NOW`. From that set, I selected `DDOG` and `NOW` as the two most defensible P/E peers. `SNOW` is a strong business-model candidate but fails the positive EPS screen. `AI` has the clearest enterprise AI label but also fails the positive EPS screen. `CRM` has positive EPS, but I rank it behind `DDOG` and `NOW` because it is more application/CRM-suite oriented, while Datadog and ServiceNow are closer to enterprise platform, AI, workflow, operations, security, and data infrastructure economics.

## Lab 07 Calculator Check

I reran the saved Lab 07 calculator before adapting it:

```powershell
python "labs\lab-07\lab07_comps.py"
```

The Asbury calculation still works. It printed:

```text
AN: 10.037825x
GPI: 11.450149x
Peer median P/E: 10.743987x
Peer-implied range: $215.81-$246.18
Median-implied price: $231.00
Remove AN: remaining median-implied price $246.18; change from full-peer estimate $15.18
Remove GPI: remaining median-implied price $215.81; change from full-peer estimate -$15.18
```

## Palantir Target Inputs

Palantir's 2025 Form 10-K, filed February 17, 2026, says Palantir builds software that helps organizations integrate data, decisions, and operations at scale and describes Gotham, Foundry, Apollo, and AIP as principal platforms. The same filing reports annual diluted EPS of `$0.63` for 2025. Source: Palantir Technologies Inc. 2025 Form 10-K, filed `2026-02-17`, `https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm`.

For consistency with the assignment target block, the calculator uses Palantir's observed market price of `$169.53`. The target price is shown for context; the peer-implied valuation is calculated by applying peer P/E multiples to Palantir's annual diluted EPS of `$0.63`.

## Candidate Screen

| Candidate | Business-model fit | Annual reported diluted EPS | Same-date / nearest price | Decision |
|---|---|---:|---:|---|
| Snowflake (`SNOW`) | Strong fit as an AI Data Cloud platform for consolidating data, applying AI, building data applications, and sharing data products. | `$(3.95)` for fiscal year ended `2026-01-31`; Form 10-K filed `2026-03-20`. | `$329.72` on `2026-09-10`, FinanceCharts. | `exclude`: negative GAAP diluted EPS makes P/E not meaningful. |
| Datadog (`DDOG`) | Strong fit as an AI-powered observability and security SaaS platform for cloud applications, infrastructure monitoring, log management, cloud security, and service management. | `$0.31` Class A diluted EPS for fiscal year ended `2025-12-31`; Form 10-K filed `2026-02-18`. | `$221.72` on `2026-09-10`, Investing.com historical table. | `qualify`: selected, but tiny EPS makes the P/E very sensitive. |
| C3.ai (`AI`) | Conceptual fit as enterprise AI application software. | `$(3.35)` GAAP net loss per share for fiscal year ended `2026-04-30`; Form 10-K filed `2026-06-24`. | `$10.47` on `2026-09-10`, Investing.com / StockAnalysis. | `exclude`: negative GAAP diluted EPS makes P/E not meaningful. |
| Salesforce (`CRM`) | Positive-EPS enterprise software company with AI, data, applications, and subscription software economics. | `$7.80` for fiscal year ended `2026-01-31`; Form 10-K filed `2026-03-02`. | `$243.00` on `2026-09-10`, FinanceCharts. | `qualify but not selected`: positive EPS, but less close than DDOG/NOW because CRM is more front-office application-suite focused. |
| ServiceNow (`NOW`) | Strong fit as an AI platform for enterprise workflows, connecting people, processes, and data across public and private organizations. | `$1.67` diluted EPS for fiscal year ended `2025-12-31`; Form 10-K filed `2026-01-29`. | `$131.17` on `2026-09-10`, StockAnalysis historical table. | `qualify`: selected. |

Source locators:

- Snowflake 2026 Form 10-K: `https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm`; price: `https://www.financecharts.com/stocks/SNOW/summary/price`
- Datadog 2025 Form 10-K: `https://www.sec.gov/Archives/edgar/data/1561550/000162828026008819/ddog-20251231.htm`; price: `https://www.investing.com/equities/datadog-inc-historical-data`
- C3.ai fiscal 2026 Form 10-K: `https://www.sec.gov/Archives/edgar/data/1577526/000157752626000078/ai-20260430.htm`; price: `https://www.investing.com/equities/c3-ai-inc-historical-data`
- Salesforce fiscal 2026 Form 10-K: `https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm`; price: `https://www.financecharts.com/stocks/CRM/summary/price`
- ServiceNow 2025 Form 10-K: `https://www.sec.gov/Archives/edgar/data/1373715/000137371526000007/now-20251231.htm`; price: `https://stockanalysis.com/stocks/now/history/`

## Selected Peer P/E Calculations

| Peer | Price | Annual diluted EPS | P/E calculation | P/E |
|---|---:|---:|---:|---:|
| Datadog (`DDOG`) | `$221.72` | `$0.31` | `$221.72 / $0.31` | `715.225806x` |
| ServiceNow (`NOW`) | `$131.17` | `$1.67` | `$131.17 / $1.67` | `78.544910x` |
| Peer median |  |  | Median of `DDOG` and `NOW` | `396.885358x` |

Applied to Palantir's annual diluted EPS of `$0.63`:

| Measure | Implied PLTR share value |
|---|---:|
| Low peer estimate: ServiceNow P/E x PLTR EPS | `$49.48` |
| High peer estimate: Datadog P/E x PLTR EPS | `$450.59` |
| Median peer estimate | `$250.04` |

## Calculator Output

I adapted the Lab 07 calculator as `labs/lab-08/lab08_palantir_comps.py` and ran:

```powershell
python "labs\lab-08\lab08_palantir_comps.py"
```

Output:

```text
Lab 08: Palantir P/E Comparable-Company Calculator
==========================================================
Comparison inputs
Target: Palantir Technologies (PLTR)
  Price: $169.53
  Annual GAAP diluted EPS: $0.63
Peers:
  Datadog (DDOG), qualified candidate peer: price $221.72, EPS $0.31
  ServiceNow (NOW), qualified candidate peer: price $131.17, EPS $1.67

Peer P/E calculations
  DDOG: 715.225806x
  NOW: 78.544910x

Palantir implied valuation
  Peer median P/E: 396.885358x
  Peer-implied range: $49.48-$450.59
  Median-implied price: $250.04

Leave-one-out sensitivity
  Remove DDOG: remaining median-implied price $49.48; change from full-peer estimate -$200.55
  Remove NOW: remaining median-implied price $450.59; change from full-peer estimate $200.55
```

## Hand Check

Manual check for ServiceNow:

`$131.17 / $1.67 = 78.544910x`

Then applying that single-peer multiple to Palantir:

`78.544910 x $0.63 = $49.48`

This matches the calculator's `NOW` P/E and the leave-one-out result when Datadog is removed.

## Leave-One-Out Test

Before running the leave-one-out test, I expected removing Datadog to collapse the estimate because Datadog has a very high P/E caused by small positive GAAP EPS. The calculator confirms this: removing `DDOG` leaves only ServiceNow and drops the estimate from `$250.04` to `$49.48`, a change of `-$200.55`.

Removing `NOW` leaves only Datadog and raises the estimate from `$250.04` to `$450.59`, a change of `$200.55`. This is the key sensitivity result: the peer-implied median is not stable because the two admitted peers have very different GAAP EPS maturity.

## Skeptical AI Review Checked Against Sources

| Check | Result | Source-tied judgment |
|---|---|---|
| Company fit | `accept limitation` | Datadog and ServiceNow are defensible enterprise software / AI platform peers, but neither is a perfect Palantir match. Datadog is observability/security for cloud applications; ServiceNow is workflow automation and AI governance across enterprise processes. Palantir is data/operations software with heavy government exposure. |
| Date match | `accept` | Peer prices use `2026-09-10` historical closes. The target market price is the assignment's observed `$169.53`; it is used for comparison, not to calculate peer-implied value. |
| Valuation object | `accept` | The calculator estimates value per diluted share by multiplying Palantir diluted EPS by peer P/E. It does not value enterprise value and does not bridge cash or debt. |
| Earnings definition | `accept with DDOG caveat` | The inputs are annual reported GAAP diluted EPS. Datadog reports Class A diluted EPS of `$0.31` and Class B diluted EPS of `$0.32`; I use Class A because the public quote is for Class A stock. |
| Non-positive EPS failure modes | `accept` | Snowflake and C3.ai are excluded even though they have business-model relevance, because their annual GAAP diluted EPS is negative. Using them would create non-meaningful P/E multiples. |
| Weakest assumption | `unresolved` | The biggest weakness is treating Datadog's high P/E as transferable to Palantir. Datadog's multiple is mechanically large because annual GAAP EPS is small, so the peer range is wide and should be interpreted as a sensitivity warning, not a precise target. |

One question that could change the decision: can Palantir demonstrate enough annual GAAP EPS expansion that a peer P/E comparison no longer depends on a small-denominator, high-multiple peer like Datadog?

## DCF Comparison

| Method | Palantir result and date | Main assumption or limitation |
|---|---|---|
| Week 3 / Lab 06 DCF | `$158.1618` per diluted share on `2026-09-10` | Forecast FCFF growth path, WACC, terminal growth, and terminal value dependence |
| Peer P/E | `$49.48-$450.59` peer-implied range, with `$250.04` median-implied price using selected peers and annual reported diluted EPS | Peer selection, same-date prices, annual GAAP EPS basis, and the instability created by Datadog's small positive EPS |

The DCF and peer P/E do not converge cleanly. The DCF value of `$158.1618` is below the assignment market price of `$169.53`. The P/E median of `$250.04` is above both, but the range is so wide that the median is not strong standalone evidence. ServiceNow alone implies only `$49.48`, while Datadog alone implies `$450.59`.

I would not mechanically average the DCF and P/E outputs. The DCF is a forward-looking FCFF model. The P/E method is a market multiple applied to current annual GAAP diluted EPS. In this lab, the P/E method mainly shows that the conclusion is highly sensitive to which profitable enterprise software peer is admitted and how mature that peer's GAAP earnings base is.

## Final Call

Final call: `watch-defer`.

I do not change the prior call because the peer evidence is informative but not stable enough to override the DCF. Datadog and ServiceNow are the best two candidates from the requested list after applying the positive EPS screen, but their multiples produce a very wide implied range. I would become more constructive if Palantir's reported GAAP diluted EPS grows enough that the peer P/E result becomes less dependent on high-multiple, small-denominator peers, or if the market price falls below the Lab 06 DCF value while operating evidence remains strong.