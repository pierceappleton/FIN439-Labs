# Lab 07: Asbury P/E Comparable-Company Analysis

Date: September 15, 2026

Price-to-earnings (P/E) measures how much the market is paying for one dollar of a company's earnings. It is calculated as price per share divided by diluted earnings per share. In this lab, the peer P/E multiples are applied to Asbury's EPS to estimate what Asbury's share price would be if the market valued its earnings like the selected peers' earnings.

A lower P/E does not automatically mean a better investment. It may signal undervaluation, but it can also reflect slower growth, weaker margins, higher risk, unusual earnings, or lower confidence in future performance. P/E is most useful when the companies have similar businesses, earnings quality, growth prospects, and risk.

## Peer Policy

| Company | Decision | Reason |
| --- | --- | --- |
| AutoNation (AN) | Use, with qualification | AutoNation is a large franchised automotive retailer with dealership operations and service/parts economics that make its price and EPS relevant for comparison. It should still be qualified because company mix, store footprint, brand exposure, and growth profile may differ from Asbury. |
| Group 1 Automotive (GPI) | Use, with qualification | Group 1 is also a franchised automotive retailer with dealership and service/parts operations, so the comparison is based on business economics rather than a broad industry label alone. It remains qualified because its scale, market mix, and earnings drivers may not match Asbury exactly. |

## Frozen Case Inputs

| Company / role | December 31, 2024 closing price | FY2024 total GAAP diluted EPS |
| --- | ---: | ---: |
| Asbury Automotive (ABG), target | $243.03 | $21.50 |
| AutoNation (AN), candidate peer | $169.84 | $16.92 |
| Group 1 Automotive (GPI), qualified candidate peer | $421.48 | $36.81 |

## Calculated Peer P/E

| Peer | Calculation | P/E |
| --- | ---: | ---: |
| AutoNation (AN) | $169.84 / $16.92 | 10.037825x |
| Group 1 Automotive (GPI) | $421.48 / $36.81 | 11.450149x |
| Peer median | Median of AN and GPI | 10.743987x |

## Implied Asbury Price

Using Asbury's FY2024 diluted EPS of $21.50:

| Measure | Implied price |
| --- | ---: |
| Low peer P/E estimate | $215.81 |
| Median peer P/E estimate | $231.00 |
| High peer P/E estimate | $246.18 |

The peer-implied range is **$215.81-$246.18**, with Asbury at the peer median equal to **$231.00**.

## Leave-One-Out Result

Removing Group 1 leaves AutoNation as the only valid peer. The remaining median-implied price is therefore AutoNation's single-peer reference estimate of **$215.81**, not a range. The change from the full two-peer median estimate is **-$15.18**, because removing the higher-multiple peer lowers the remaining peer multiple.

## Validation

The script output matches the expected case checks within normal rounding:

| Check | Expected | Script result |
| --- | ---: | ---: |
| AutoNation P/E | 10.037825x | 10.037825x |
| Group 1 P/E | 11.450149x | 11.450149x |
| Peer median P/E | 10.743987x | 10.743987x |
| Asbury peer-implied range | $215.81-$246.18 | $215.81-$246.18 |
| Asbury at peer median | $231.00 | $231.00 |
| Remove GPI: remaining AN estimate | $215.81 | $215.81 |
| Change from two-peer midpoint | -$15.18 | -$15.18 |

## Reflection Versus the Prior Palantir DCF

The prior Palantir DCF used forecast FCFF, WACC, terminal growth, cash, debt, and shares to estimate intrinsic value. This P/E comparable-company method uses price per share and EPS to create a market-implied comparison. The two methods should stay separate: P/E does not use a cash/debt bridge. In the comps method, the main judgment is peer selection, because the calculation is only meaningful if the peers have comparable businesses, growth prospects, profitability, and risk.

