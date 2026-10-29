# Lab 17 — Point-in-Time Audit

**Question:** Was each number in the series knowable on the day I would have traded on it — and may Project 2 use it?

## Run

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m streamlit run labs/lab-17/asof_app.py
```

If the environment is not installed, run `python -m pip install -r labs/lab-17/requirements.txt` and then `python -m streamlit run labs/lab-17/asof_app.py`. The app retrieves live CSVs without a key. It caches each download for an hour; the timestamps under the table show when the cached data was actually downloaded. Enter a series ID in the sidebar. Counts cover the complete downloaded history, not just the chart window. Revisions compare nonmissing observations on matching measurement dates; a later count measures nonmissing current observations after the last observation in the historical snapshot. Neither count is a publication timestamp.

## Known-answer checks

Live downloads tested October 29, 2026, using the app's download and comparison functions:

| Series | As known October 5, 2026: last measurement | Value |
| --- | --- | ---: |
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | October 2, 2026 | 5.28 |
| MORTGAGE30US | October 1, 2026 | 7.28 |

PAYEMS as known January 15, 2025: December 2024 **159,536** thousand; the current December 2024 observation was **158,316**. The app counted **381** changed values on common, nonmissing dates. These were computed from separate FRED and ALFRED downloads; they may change with future revisions.

## Data card — GS10

GS10 is the selected monthly series. The earlier prework choice could not be recovered from the lab files, so GS10 was selected for this audit. It is relevant to a portfolio with Treasury and investment-grade bond exposure because yields affect bond valuations.

- **Source:** Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates, via [FRED GS10](https://fred.stlouisfed.org/series/GS10) and [ALFRED GS10](https://alfred.stlouisfed.org/series?seid=GS10).
- **Measure:** monthly average of business-day market yields on U.S. Treasury securities at 10-year constant maturity, quoted on an investment basis.
- **Units and frequency:** percent per year, monthly, not seasonally adjusted.
- **Publication lag:** after the month ends. The September 30 ALFRED vintage ended in August, whereas the October 29 vintage included September. FRED’s page-level “Updated” stamp is not an observation-specific publication timestamp. Actual release dates and times vary; a date alone cannot establish availability before an intraday trade.
- **Revisions:** FRED states that all data are subject to revision. Comparing the September 30 and current snapshots found **zero** changes on shared nonmissing dates; that observation does not prove revisions are impossible in other periods.
- **Download date:** October 29, 2026. Current data and historical snapshots were downloaded from FRED and ALFRED by the app functions; the source page was also viewed on that date.

| Month measured | Current FRED value, percent |
| --- | ---: |
| July 2026 | 4.60 |
| August 2026 | 4.68 |
| September 2026 | 4.99 |

The three values were checked against the FRED page and personally confirmed by the student on October 29, 2026. As of September 30 the last available observation was August, 4.68; as of October 29 it was September, 4.99. One current observation came after the last one known September 30, with zero revisions on matching nonmissing dates.

### Fresh eyes — partner review with Rusheel

Rusheel and I discussed these questions together. Rusheel identified **publication date** as the field he trusted least. He noticed that a FRED page can show an old observation alongside a much later “Updated” stamp, so that stamp describes a page or series refresh rather than the publication time of that individual value. Our earlier use of the stamp as direct evidence of a one-month lag was coincidental. The ALFRED vintage comparison supplies the relevant date-level evidence. Units are explicit on FRED (“Percent, Not Seasonally Adjusted”), while zero revisions in this comparison does not prove revisions can never occur.

1. **What does `vintage_date` do, and why does a backtest need it?** It asks ALFRED for the series as it appeared on that date. This helps prevent a backtest from using later revisions or observations that had not yet been published. The date-based snapshot alone does not establish availability at a particular intraday trading time. Look-ahead bias can affect results in either direction.
2. **Publication-date attack: GS10 labels September as September 1. Why can't we use its September value at the September 30 close?** September 1 labels the measurement period, not the publication date. The September 30 ALFRED snapshot ends with August at 4.68%, while the later snapshot includes September at 4.99%. That establishes the September value was absent from the September 30 information set; the FRED “Updated” stamp alone does not establish its release time.
3. **Does zero revisions between September 30 and October 29 prove GS10 is never revised?** No. It only shows no changed values on common nonmissing dates in that particular comparison. FRED notes that all data are subject to revision; other vintages or dates could differ.

## Project 2 call

**Quarantine** until the backtest uses the ALFRED vintage available by each decision date and a conservative release-time rule. Admit it after the decision schedule and publication timing are documented and validated; for an intraday decision, use the prior known value unless actual release time has passed. Today's history alone cannot establish when any historical value became available.

## Explain and reflect

`download_asof` is cached by series ID and vintage date for one hour. It requests the ALFRED CSV with those two parameters, applies a timeout, checks and parses the response, and returns the values and download time. The parser converts observation dates and numerical values, treats `.` as missing, and drops missing values; the app also excludes any observation dated after the as-known date. The vintage date selects a historical snapshot, not a current FRED download.

A data card records a series' source, meaning, units, frequency, publication timing, revision behavior, and retrieval date. Measurement date, publication date/time, and vintage together prevent treating a later release or revision as if it were known earlier. “Cleaned the data” does not record those fields or allow another person to reproduce the decision-date information set.

GS10's monthly value appears after its measurement month: the September 30 snapshot did not contain September, which appeared in the October 29 snapshot. A backtest that used the September value at September's close would use information from the future and could overstate how well a strategy timed or predicted bond movements; the direction and size of any performance effect require an actual backtest.

## Remaining personal checkout

- Complete the Brightspace quiz and submit GitHub links for this writeup and `asof_app.py` using the published GitHub links.
