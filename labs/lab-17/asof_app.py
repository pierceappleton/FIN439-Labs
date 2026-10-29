"""Compare current FRED observations with an ALFRED point-in-time vintage."""
from datetime import date, datetime
from io import StringIO
import re

import pandas as pd
import requests
import streamlit as st

SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


def parse_csv(response):
    response.raise_for_status()
    frame = pd.read_csv(StringIO(response.text), na_values=["."])
    if len(frame.columns) != 2 or frame.empty:
        raise ValueError("The download did not contain a single series of observations.")
    dates = pd.to_datetime(frame.iloc[:, 0], errors="coerce")
    values = pd.to_numeric(frame.iloc[:, 1], errors="coerce")
    if dates.isna().any() or dates.duplicated().any():
        raise ValueError("The download contains invalid or duplicate observation dates.")
    return pd.Series(values.to_numpy(), index=dates, name="value").dropna().sort_index()


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id):
    """Retrieve and cache FRED's current CSV and the actual download time."""
    response = requests.get("https://fred.stlouisfed.org/graph/fredgraph.csv",
                            params={"id": series_id}, timeout=30)
    return parse_csv(response), datetime.now()


@st.cache_data(ttl=3600, show_spinner=False)
def download_asof(series_id, vintage_date):
    """Retrieve the ALFRED snapshot for the requested vintage, not current FRED."""
    response = requests.get("https://alfred.stlouisfed.org/graph/alfredgraph.csv",
                            params={"id": series_id, "vintage_date": vintage_date.isoformat()},
                            timeout=30)
    return parse_csv(response), datetime.now()


def compare(today, vintage):
    """Count nonmissing later observations and changed values on common dates."""
    if vintage.empty:
        return None, None
    common = today.to_frame("today").join(vintage.to_frame("vintage"), how="inner")
    return int((today.index > vintage.index.max()).sum()), int((common.today != common.vintage).sum())


def last(series):
    return (None, None) if series.empty else (series.index[-1].date(), float(series.iloc[-1]))


def main():
    st.set_page_config(page_title="Rates: point-in-time audit", layout="wide")
    st.title("Rates: point-in-time audit")
    st.caption("Data from [FRED](https://fred.stlouisfed.org/) and [ALFRED](https://alfred.stlouisfed.org/), Federal Reserve Bank of St. Louis; download times shown below. Built with AI help; a learning demonstration, not investment advice.")
    selected = st.sidebar.multiselect("Series", list(SERIES), default=list(SERIES),
                                      format_func=lambda x: f"{x} — {SERIES[x]}")
    extra = st.sidebar.text_input("Add another FRED series ID", value="GS10").strip().upper()
    start = st.sidebar.date_input("Start date", date(2020, 1, 1))
    asof_date = st.sidebar.date_input("As known on", date.today(), max_value=date.today())
    if extra and extra not in selected:
        selected.append(extra)
    if not selected:
        st.info("Select a series or enter an ID.")
        return
    rows, downloads = [], []
    for series_id in selected:
        st.subheader(f"{series_id} — {SERIES.get(series_id, 'Custom series')}")
        if not re.fullmatch(r"[A-Z0-9_]+", series_id):
            st.error("Invalid series ID. Use letters, numbers, and underscores.")
            continue
        try:
            current, downloaded_current = download_today(series_id)
            vintage, downloaded_vintage = download_asof(series_id, asof_date)
            # A future observation cannot be known on the decision date.
            vintage = vintage[vintage.index <= pd.Timestamp(asof_date)]
            if current.empty:
                raise ValueError("No nonmissing observations returned for this ID.")
            visible = current[current.index >= pd.Timestamp(start)]
            if visible.empty:
                st.info("No current observations on or after the start date.")
            else:
                st.line_chart(visible.rename("Current value"))
            old_date, old_value = last(vintage)
            new_date, new_value = last(current)
            st.write(f"Last observation known on {asof_date}: {old_date or 'none'}")
            late, revised = compare(current, vintage)
            rows.append({"Series": f"https://fred.stlouisfed.org/series/{series_id}",
                         "Last measured as known": old_date, "Value as known": old_value,
                         "Last measured today": new_date, "Value today": new_value,
                         "Values after last known": late, "Common dates revised": revised})
            downloads.append(f"{series_id}: FRED {downloaded_current:%Y-%m-%d %H:%M}; ALFRED {downloaded_vintage:%Y-%m-%d %H:%M}")
        except (requests.RequestException, ValueError, pd.errors.ParserError) as exc:
            st.error(f"Could not load {series_id}: {exc}")
    if rows:
        st.subheader("Current versus as-known observations")
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch",
                     column_config={"Series": st.column_config.LinkColumn("FRED series", display_text=r"https://fred\.stlouisfed\.org/series/(.*)")})
        st.caption("Counts use all available history, not only the chart's start date. Revised compares nonmissing values on matching observation dates; later observations count nonmissing current values after the vintage's last date. An empty vintage has unavailable counts, not zero.")
        st.caption("Downloaded (local time; cached for up to one hour): " + " | ".join(downloads))


if __name__ == "__main__":
    main()
