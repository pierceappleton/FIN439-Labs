# FIN439 Lab 08 - Palantir P/E Triangulation

Company: Palantir Technologies Inc.  
Ticker: `PLTR`  
Comparison date: `2026-09-10`  
Valuation object: value per diluted share using annual reported GAAP diluted EPS and same-date stock prices.

## Starting Peer Policy

A useful peer for Palantir should be a listed operating company that sells enterprise software or data/AI platforms with recurring or durable customer relationships, meaningful commercial or government enterprise exposure, and positive annual reported diluted EPS available before the `2026-09-10` comparison date. Differences to qualify include cloud/SaaS delivery model, customer mix, growth maturity, margin structure, government exposure, and whether the company is mainly infrastructure software, analytics software, cybersecurity, or application software. Exclude companies that are not operating companies, have materially different economics, lack positive annual reported diluted EPS, report incompatible share/currency bases that cannot be reconciled, or cannot be supported by opened primary/company sources.

I would reject a candidate if the opened source does not support real enterprise software or data/AI overlap with Palantir, if annual diluted EPS public by `2026-09-10` cannot be verified, if the same-date price cannot be traced consistently with the target, or if the business model is too different for a P/E multiple to say anything useful.

## Lab 07 Calculator Check

I reran the saved Lab 07 command:

```powershell
python "..\Lab 07\lab07_comps.py"
```

The Asbury calculator still works. It printed AutoNation P/E of `10.037825x`, Group 1 Automotive P/E of `11.450149x`, peer median P/E of `10.743987x`, Asbury peer-implied range of `$215.81-$246.18`, and median-implied price of `$231.00`. Removing `GPI` left a single-peer reference estimate of `$215.81`.

## Target Evidence

Palantir's 2025 Form 10-K, filed February 17, 2026, says the company builds software that helps organizations integrate data, decisions, and operations at scale, and describes Gotham, Foundry, Apollo, and AIP as principal platforms. The same filing reports 2025 diluted EPS of `$0.63` and diluted weighted-average shares of `2,565.197` million. Source: SEC Form 10-K, accession `0001321655-26-000011`, business section and Note 12, `https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm`.

For the P/E calculator I used the `2026-09-10` close of `$165.86` from FinanceCharts' PLTR historical price table. This differs from the Lab 06 reverse-DCF market price note of `$169.53`, which appears in current historical tables as the `2026-09-09` close. I kept the Lab 06 DCF value unchanged, but used the same `2026-09-10` price convention for target and peers in this Lab 08 P/E comparison. Price source: `https://www.financecharts.com/compare/PLTR/summary/price`.

## Candidate Decisions

| Candidate | Business evidence | Important difference from Palantir | Annual diluted EPS public by 2026-09-10 | Price used | Decision |
|---|---|---|---:|---:|---|
| Microsoft (`MSFT`) | Microsoft says it develops software, services, devices, and solutions, including cloud-based solutions with AI, software, services, platforms, and content. Its 2026 Form 10-K also describes Microsoft 365 Commercial, Dynamics, Azure, GitHub, and cloud/AI services for enterprise customers. Source: Microsoft 2026 Form 10-K, Item 1 Business, `https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm`. | Much larger, more diversified, and more mature than Palantir; includes consumer, devices, gaming, LinkedIn, advertising, and hyperscale cloud infrastructure. | `$17.95`, fiscal year ended `2026-06-30`, 10-K signed/filed `2026-07-29`. | `$492.44` close on `2026-09-10`, FinanceCharts MSFT historical price table, `https://www.financecharts.com/stocks/MSFT/summary/price`. | `qualify` |
| Salesforce (`CRM`) | Salesforce says it is a global CRM technology leader helping organizations become agentic enterprises, bringing humans, agents, applications, and data together on a trusted unified platform. It sells worldwide primarily on a subscription basis. Source: Salesforce 2026 Form 10-K, Item 1 Business, `https://www.sec.gov/Archives/edgar/data/1108524/000110852426000060/crm-20260131.htm`. | More application/CRM and customer-workflow focused than Palantir, with less direct government/intelligence exposure and a more mature SaaS subscription profile. | `$7.80`, fiscal year ended `2026-01-31`, 10-K filed `2026-03-02`. | `$243.00` close on `2026-09-10`, FinanceCharts CRM historical price table, `https://www.financecharts.com/stocks/CRM/summary/price`. | `qualify` |

I admitted both companies only as qualified peers. They satisfy the listed operating-company, enterprise software, positive annual EPS, and traceable price tests, but neither is a clean Palantir twin.

## Calculator Output

I copied and adapted the Lab 07 calculator as `lab08_palantir_comps.py`, then ran:

```powershell
python lab08_palantir_comps.py
```

Output:

```text
Lab 08: Palantir P/E Comparable-Company Calculator
==========================================================
Comparison inputs
Target: Palantir Technologies (PLTR)
  Price: $165.86
  Annual GAAP diluted EPS: $0.63
Peers:
  Microsoft (MSFT), qualified candidate peer: price $492.44, EPS $17.95
  Salesforce (CRM), qualified candidate peer: price $243.00, EPS $7.80

Peer P/E calculations
  MSFT: 27.433983x
  CRM: 31.153846x

Palantir implied valuation
  Peer median P/E: 29.293915x
  Peer-implied range: $17.28-$19.63
  Median-implied price: $18.46

Leave-one-out sensitivity
  Remove MSFT: remaining median-implied price $19.63; change from full-peer estimate $1.17
  Remove CRM: remaining median-implied price $17.28; change from full-peer estimate -$1.17
```

The peer P/E result is dramatically below Palantir's own `2026-09-10` market price because Palantir's annual GAAP EPS is still small relative to its price. The result does not mean Microsoft or Salesforce are perfect peers; it shows that mature profitable enterprise software P/E multiples do not support Palantir's current price when applied to Palantir's latest annual diluted EPS.

## Validation

Hand check for Salesforce:

`$243.00 / $7.80 = 31.153846x`, matching the calculator's `CRM` P/E.

Before reading the leave-one-out output, I expected removing Salesforce to lower the reference estimate because Salesforce has the higher peer P/E. The calculator confirms this: removing `CRM` leaves Microsoft only and drops the estimate to `$17.28`, a change of `-$1.17` from the full two-peer median. Removing Microsoft leaves Salesforce only and raises the estimate to `$19.63`, a change of `$1.17`.

## DCF Comparison

| Method | Palantir result and date | Main assumption or limitation |
|---|---|---|
| Week 3 / Lab 06 DCF | `$158.1618` per diluted share on `2026-09-10` | Forecast FCFF growth path, WACC, terminal growth, and terminal value dependence |
| Peer P/E | `$17.28-$19.63` peer-implied range, with `$18.46` median-implied price using `2026-09-10` prices and latest annual GAAP diluted EPS | Peer choices are only qualified, not exact; P/E penalizes Palantir because annual GAAP EPS lags the market's expected growth; same-date price source differs from the Lab 06 price note |

I do not average these methods. The DCF capitalizes a forward FCFF growth path, while the P/E comparison applies mature profitable software multiples to reported annual diluted EPS. The large gap is the main point of the triangulation.

## AI Criticism Checked Against Sources

Prompt used:

> Review my valuation comparison as a skeptical colleague. Identify the weakest supported assumption and any mismatch in company, date, valuation object or earnings definition. Do not invent a missing range or average the methods. Ask one question that could change my decision. I will check your criticism against my sources before revising my call.

| Criticism | Judgment | Source-checked reason |
|---|---|---|
| The weakest supported assumption is that Microsoft and Salesforce are close enough peers for Palantir. | `accept` | Their SEC business descriptions support enterprise software and AI/data overlap, but the filings also show much broader, more mature platforms than Palantir. That is why both are marked `qualify`, not clean `use`. |
| There is a date mismatch because Lab 06 recorded `$169.53` for PLTR on `2026-09-10`, while the P/E table uses `$165.86`. | `accept` | FinanceCharts and StockAnalysis show `$165.86` for `2026-09-10` and `$169.53` for `2026-09-09`; I therefore use one consistent `2026-09-10` price source for Lab 08 and preserve the Lab 06 DCF value separately. |
| The earnings definition may be too backward-looking for a company whose price reflects expected AI growth. | `accept` | The calculator intentionally uses annual reported GAAP diluted EPS. Palantir's 2025 10-K reports positive diluted EPS of `$0.63`, but that base is small relative to the stock price. A forward EPS method would be a different assignment. |
| One question that could change the decision: can Palantir convert AIP demand into annual GAAP EPS fast enough to make its own P/E converge toward qualified peer multiples? | `unresolved` | The current opened sources prove strong business momentum and positive EPS, but they do not prove a multi-year GAAP EPS path sufficient to bridge the gap. Future annual filings and guidance would resolve it. |

## Final Reflection And Call

Microsoft and Salesforce were admitted as qualified peers because opened SEC filings support enterprise software, cloud, data, AI, and durable customer relationships, and both had positive annual diluted EPS public before `2026-09-10`. They remain qualified rather than clean peers because Microsoft is far more diversified and Salesforce is more CRM/application-SaaS focused, while Palantir has a distinct data/operations platform and government heritage.

The peer comparison adds valuation discipline to the DCF. The DCF can support a much higher value only by forecasting very high FCFF growth and accepting terminal-value dependence. The P/E method asks what Palantir would be worth if reported annual EPS were valued like mature profitable enterprise software peers, and that answer is far below both the DCF and the market price.

The two methods differ because they use different valuation objects: forward FCFF potential versus current annual GAAP diluted EPS. The result is not cleanly comparable as an average, but it is comparable as a warning. Current reported EPS does not defend the stock price at qualified peer P/E multiples.

Final call: `watch-defer`.

I withhold an initiate call. The defensible P/E range from the admitted peer set is `$17.28-$19.63`, but I would not use it as a standalone price target because the peers are only qualified and the method is backward-looking for Palantir. Evidence that would change the decision would include sourced proof that Palantir can grow GAAP diluted EPS and free cash flow fast enough for the DCF growth path to become less speculative, or a market price falling below the Lab 06 base-case value of about `$158` while operating momentum remains intact.
