# Lab 14 — Portfolio Baselines

Pierce Appleton | October 20, 2026

AI-assisted code and analysis using the supplied course-authored training values, not market estimates. Reflection and explain-back material below is preparation for independent review; no partner session or AI-closed work is claimed.

## D — Question and answer

What does each simple portfolio earn and risk, and does any meet the Meridian mandate?

None of the three meets both the 6.5% expected-return proxy and the 3% reserve rule. The benchmark earns enough in expectation but has no eligible reserve. Equal weight and inverse volatility have ample reserves but miss the return objective. Expected returns are not guarantees or proof of realized net rolling-five-year performance.

## R — Inputs

| Sleeve | Expected return | Volatility |
|---|---:|---:|
| Treasury bills | 3.5% | 0.5% |
| Treasury 10-year note | 4.3% | 7.0% |
| Investment-grade bond fund | 5.0% | 6.0% |
| Global equity index fund | 8.0% | 16.0% |

| Correlation | Bills | 10-year | IG | Equity |
|---|---:|---:|---:|---:|
| Bills | 1.00 | 0.10 | 0.05 | 0.00 |
| 10-year | 0.10 | 1.00 | 0.80 | −0.10 |
| IG | 0.05 | 0.80 | 1.00 | 0.25 |
| Equity | 0.00 | −0.10 | 0.25 | 1.00 |

Objective = CPI estimate 2.5% + 4% = 6.5%. Bills and the 10-year note are reserve eligible. Calculations use decimal returns, volatilities and weights; the mandate checker uses percent weights.

## I / V — Results and evidence

```text
python labs/lab-14/portfolio.py
python labs/lab-13/mandate.py
python labs/lab-14/verify_labs.py
```

| Portfolio | Bills / 10-year / IG / equity (%) | Return (%) | Volatility (%) | Reserve (%) | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80 | 10.46 | 0.0 | yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20 | 5.21 | 50.0 | no |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77 | 1.05 | 90.3 | no |

All known answers match. Inverse-volatility displayed weights sum to 99.9% because of rounding; computations use full-precision weights summing to 100%.

The verification script exercises both labs' known answers and the required probes:

- Change IG–equity correlation to 0.50 in both cells: benchmark volatility rises to **11.00%**.
- Set it to 1.3: the engine refuses with a clear bounds message; −1.3 is refused too.
- Change only one cell: the engine refuses the asymmetric table.
- Lab 13 candidate E is 40% IG fund / 60% equity; its eligible reserve is **0.0%**, below 3.0%, and it fails exactly one checkable rule.

Probes use copies of the inputs, so the saved correlation remains 0.25. The engine checks correlation bounds, symmetry, dimensions, diagonal and finite inputs; it does not provide a general positive-semidefinite matrix certification.

## Diversification and hand calculation

Diversification combines assets whose returns do not move together perfectly. A correlation below +1 reduces the cross term relative to perfectly correlated assets, lowering risk relative to the weighted-average volatility. It does not guarantee risk below that of each individual asset: the benchmark remains riskier than its 6% bond sleeve.

Covariance(i,j) = correlation(i,j) × volatility(i) × volatility(j).

Portfolio variance = Σᵢ Σⱼ weight(i) × weight(j) × covariance(i,j).

For the benchmark:

```text
Expected return = 0.4 × 0.05 + 0.6 × 0.08 = 0.068 = 6.80%
Variance = (0.4 × 0.06)^2 + (0.6 × 0.16)^2
           + 2 × 0.4 × 0.6 × 0.06 × 0.16 × 0.25
         = 0.000576 + 0.009216 + 0.001152 = 0.010944
Volatility = sqrt(0.010944) = 0.1046136 = 10.46%
```

At correlation 0.50, the cross term doubles to 0.002304; variance becomes 0.012096 and volatility 10.9982%, displayed as 11.00%. Omitting covariance gives sqrt(0.009792) = 9.90%, the known incorrect answer. At correlation +1 the benchmark's volatility would be 12.00%.

## Code explanation preparation

In `portfolio_volatility`, the dimension check makes each weight correspond to one covariance row and column. The outer loop selects sleeve i; the inner loop selects sleeve j. Each pair contributes `weights[i] * weights[j] * covariance[i][j]` to variance. Off-diagonal pairs appear twice, matching the factor of two in the hand calculation. The square root converts variance back to volatility. A materially negative variance is refused; a tiny floating-point negative is clamped to zero.

Quiz prompt to answer before reading the explanation above: **Why must the sum include both (IG, equity) and (equity, IG), and why would dropping those terms give 9.90%?** No student answer is recorded yet.

## Reflection draft

Inverse volatility favors bills because 1/0.005 = 200, compared with about 14.29 for notes, 16.67 for IG bonds and 6.25 for equity. Normalizing gives bills about 84.3%. This weighting uses each asset's standalone volatility, not the full covariance matrix, so it is not a solved minimum-variance portfolio.

I would show the CIO the benchmark first: it frames the client's own comparison standard and immediately exposes the reserve conflict. Then I would show the other baselines to demonstrate how lower volatility trades away the expected return target. The next step requires an agreed optimization objective and a defined interpretation of S9.

## Before Thursday — proposed fund universe

For the fictional Project 2 mandate drafted in Lab 13, the instruction's four practice funds map naturally to the four roles:

| Ticker | Fund name (Yahoo) | Role | Price source / download date |
|---|---|---|---|
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | Cash / reserve proxy | [Yahoo Finance](https://finance.yahoo.com/quote/BIL/history/), monthly Adj Close; 2026-10-20 |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds | [Yahoo Finance](https://finance.yahoo.com/quote/IEF/history/), monthly Adj Close; 2026-10-20 |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade fixed income | [Yahoo Finance](https://finance.yahoo.com/quote/LQD/history/), monthly Adj Close; 2026-10-20 |
| VT | Vanguard Total World Stock Index Fund ETF Shares | Broad global equity | [Yahoo Finance](https://finance.yahoo.com/quote/VT/history/), monthly Adj Close; 2026-10-20 |

These are the instruction's practice examples, not personalized recommendations. They are a proposed universe for review. [prices.csv](prices.csv) contains **60 monthly adjusted closes per fund, October 2021–September 2026**, oldest month first, with Date followed by BIL, IEF, LQD and VT. Dates label the month (first of month), not the date of the final trading session. The incomplete October 2026 month is excluded.

Actual prices were retrieved from Yahoo Finance's chart endpoint, using its `adjclose` field rather than unadjusted close. Adjusted history accounts for distributions and splits and may be revised by the provider. [prices-sources.json](prices-sources.json) records the exact source URL, field, fund name, download date and count for each ticker. The downloader rejects missing, duplicate or invalid observations and requires all 60 months for every ticker before writing the CSV.

To reproduce the fixed window with internet access:

```text
python labs/lab-14/download_prices.py
```

This real-price file is for the next lab; the Lab 14 risk engine continues to use the supplied training inputs.

## Checkout

- [portfolio.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-14/portfolio.py)
- [This writeup](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-14/lab-14-writeup.md)
- [Verification script](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-14/verify_labs.py)
- [Mandate checker including candidate E](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-13/mandate.py)
- [Monthly adjusted prices](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-14/prices.csv)
