# Lab 16 — Provenance Gate

Decision date: **March 31, 2026**.

## Question

On the day you would have traded, what did this data actually say — and how much of what you see now came later?

## Run

From the repository root:

```sh
python labs/lab-16/asof.py
```

The script uses only the Python standard library. The table and decision date are editable at the top. All outputs are calculated from those inputs.

## Verification against the known answer

| Rule, applied in order | Count | Row numbers |
| --- | ---: | --- |
| Quarantine missing ticker | 1 | 11 |
| Remove exact duplicate | 1 | 7 |
| Remove publications after decision date | 3 | 3, 8, 10 |
| Replace older vintage | 1 | 2 |
| Remaining as-of panel | 6 | 1, 4, 5, 6, 9, 12 |

The row number is an identifier, so it is excluded when comparing records for an exact duplicate.

| Ticker | As-of signal | Naive signal |
| --- | --- | --- |
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

Return is `(latest price / previous month's price - 1) * 100`. The naive calculation still removes missing tickers and duplicates and selects the latest vintage, but ignores the publication cutoff.

The March 31 funnel, panel, and all signals match the supplied answer. An automated check with **April 15, 2026** confirmed that every as-of signal equals its naive signal. The saved decision date remains March 31. The automated check was completed locally. I also completed the partner swap and later-date test in class.

## Rule 4 explanation

`latest = {}` creates a dictionary holding the selected row for each ticker and measured month. For every eligible row, `key = (row[1], row[2])` groups it by ticker and month. The eligibility step has already excluded publications after the decision date.

`if key not in latest or row[3] > latest[key][3]` selects a row if the group is new or its publication date is later than the stored row's date. ISO dates in YYYY-MM-DD format sort in calendar order. If an older row is already stored, its row number goes into the older-vintage removal list. `latest[key] = row` stores the replacement. Otherwise, the incoming row is older and its row number is recorded as removed.

For AAA February, row 2 is initially stored, then row 4 replaces it because March 25 is later than March 10 and still on or before March 31. The return therefore uses 103, not 104.

## Sanity check

Yield is `(100 / price - 1) * 100`.

| Row | Fund | Month | Price | Yield | Breaks in the training table |
| --- | --- | --- | ---: | ---: | --- |
| 1 | AAA | January | 101 | -0.99% | Negative yield |
| 4 | AAA | February | 103 | -2.91% | Negative yield |
| 5 | BBB | January | 98 | +2.04% | Nothing |
| 6 | BBB | February | 97 | +3.09% | Nothing |
| 9 | CCC | January | 110 | -9.09% | Negative yield; priced above BBB and AAA |
| 12 | CCC | February | 111 | -9.91% | Negative yield; priced above BBB and AAA |

The provenance gate verifies when records were available. It does not check economic plausibility. Under this lab's assumptions, a fifth rule would quarantine prices above 100 (negative yields), catching rows 1, 4, 9, and 12. A separate cross-rating check would flag violations of AAA > BBB > CCC for the same month and maturity.

## Learn and reflect

Look-ahead bias occurs when a historical decision uses information published after that decision. Event time is the month measured; publication time is when the value becomes available. A revision changes a previously published value and has its own publication date.

AAA's naive +5.83% uses March's price of 109, published April 10, divided by February's revised price of 103. On March 31, March's price was unavailable. The latest knowable comparison was February versus January: 103 / 101 - 1 = +1.98%. The +5.83% therefore makes AAA appear stronger using future information.

Rule 3 matters most for preventing future information from entering the March 31 decision: it excludes rows 3, 8, and 10. Rule 4 is also essential because it replaces AAA's February 104 with the knowable revision of 103; failing to do that produces the incorrect +2.97%.

A backtest using the naive column would claim AAA gained 5.83%, BBB lost 5.15%, and CCC gained 1.82% over their respective latest monthly comparisons. Those figures incorporate publications unavailable on March 31, and the months differ across tickers. They are not a tradable March 31 information set.

## Personal checkout completed

I completed the in-class activities: explained rule 4 aloud, answered a partner's question from the code, ran the partner's file with April 15 and undid the change, and completed the AI quiz.
