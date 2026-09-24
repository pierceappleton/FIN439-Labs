# FIN439 Lab 06 DCF - Palantir Technologies Inc. (`PLTR`)

Company: Palantir Technologies Inc.  
Ticker: `PLTR`  
Model date: 2026-09-10  
Units: USD millions except per-share amounts and share count, which is in millions.

## Sourced Input Table

| Input | Value used | Unit | As-of date | Locator/source | Status |
|---|---:|---|---|---|---|
| Starting FCFF | 2,100.591 | USD millions | 2025-12-31 | Palantir 2025 Form 10-K, consolidated cash flow statement: net cash provided by operating activities of $2,134.473 million less purchases of property and equipment of $33.882 million. I used after-tax interest of $0 because the filing shows no outstanding debt under the credit facility. SEC filing: https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm | Sourced |
| Growth, years 1-5 | 119%, 100%, 80%, 60%, 40% | annual FCFF growth rates | Forecast from 2026-2030 | Year 1 ties 2025 FCFF to Palantir's FY2026 adjusted free cash flow guidance midpoint of about $4.6 billion. Later years are forecast taper assumptions informed by Q2 2026 revenue growth of 93%, U.S. commercial revenue growth of 149%, and management's FY2026 guidance. Palantir Q2 2026 release: https://investors.palantir.com/news-details/2026/Palantir-Reports- | Sourced forecast / assumption |
| WACC | 10% | discount rate | 2026-09-10 | Assignment estimate: cost of equity about 11%, after-tax cost of debt about 4.5%, 85/15 capital structure, rounded WACC about 10%. | Sourced from lab instruction method |
| Terminal growth | 3% | perpetual growth rate | 2026-09-10 | Long-run nominal economy assumption, not a company-specific growth forecast. | Assumption |
| Cash | 1,423.796 | USD millions | 2025-12-31 | Palantir 2025 Form 10-K balance sheet cash and cash equivalents. SEC filing: https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm | Sourced |
| Debt | 0.000 | USD millions | 2025-12-31 | Palantir 2025 Form 10-K debt note: no outstanding debt balances under the 2014 Credit Facility at December 31, 2025. | Sourced |
| Diluted shares | 2,565.197 | millions | 2025 fiscal year | Palantir 2025 Form 10-K EPS note: diluted weighted-average shares used in computing EPS. | Sourced |

No unresolved rows were left as training placeholders. The five-year growth path is still a forecast, not a reported fact.

## Stock Price

Today's price used for the reverse DCF target: **$169.53** for `PLTR`, observed on 2026-09-10 from Investing.com market data, which showed the latest regular-session price/close as $169.53 and after-hours price of $169.80 at 20:40:43. Source: https://www.investing.com/equities/palantir-technologies-inc-historical-data

## Model Output Summary

Base-case value per diluted share: **$158.1618**.

Twelve printed lines from the company run:

```text
FCFF Year 1: 4,600.2943
FCFF Year 2: 9,200.5886
FCFF Year 3: 16,561.0594
FCFF Year 4: 26,497.6951
FCFF Year 5: 37,096.7732
PV of explicit FCFF: 65,360.9068
Terminal value, Year 5: 545,852.5193
PV of terminal value: 338,931.4685
Enterprise value: 404,292.3752
Equity value: 405,716.1712
Value per share: 158.1618
PV of TV / enterprise value: 0.8383
```

Sensitivity grid, dollars per diluted share:

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 163.88 | 188.27 | 222.42 |
| 10% | 140.52 | 158.16 | 181.68 |
| 11% | 122.45 | 135.69 | 152.70 |

Reverse DCF result:

- Target price: **$169.53**
- Solved uniform growth shift: **+2.58 percentage points**
- Inputs held fixed: starting FCFF, WACC, terminal growth, cash, debt, and diluted shares.

## Reasonableness Check

The base-case value of $158.16 is about 0.93x the $169.53 price used, so it is within the assignment's 0.5x to 2.0x reasonableness range. I would still distrust the growth path most because Palantir's recent AIP momentum is very strong, but extending extremely high FCFF growth rates for five years puts a lot of value into the terminal value.

## Conditional Call

Watch-defer. Initiate if the price falls below my base-case value per share, such as below about $158, or if there is sourced evidence that Palantir can sustain the growth path the current price demands. Otherwise keep it on the research list without initiating. Monitor: U.S. commercial revenue growth and adjusted free cash flow margin next quarter.

## Temperature Check

What works: the lab makes the valuation pressure visible instead of stopping at a company story.

What confuses: deciding how aggressive the five-year growth path should be when one-year guidance and recent growth are both unusually high.

One change: I would add a required downside case so the base case does not carry all the judgment.

## Verification Notes

Before switching to Palantir, I verified the training case:

- Base value per share: $27.4974
- Sensitivity grid matched the expected values: 28.60, 32.94, 39.02 / 24.36, 27.50, 31.69 / 21.06, 23.41, 26.44.
- Reverse DCF solved at about +1.78 percentage points for a $30.00 target.

Final verification command:

```bash
python dcf.py
```

The final company version printed all three required blocks cleanly: base DCF, sensitivity grid, and reverse DCF.
