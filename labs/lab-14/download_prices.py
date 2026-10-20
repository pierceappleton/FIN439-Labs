"""Download the instruction's practice fund universe; standard library only.

Fixed window: October 2021 through September 2026 (60 completed months).
Yahoo's monthly timestamps label the month; values are monthly adjusted closes.
"""
import csv
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import urllib.parse
import urllib.request

TICKERS = ("BIL", "IEF", "LQD", "VT")
START = datetime(2021, 10, 1, tzinfo=timezone.utc)
END = datetime(2026, 10, 1, tzinfo=timezone.utc)  # Exclusive; omit partial October.
DOWNLOAD_DATE = "2026-10-20"  # Task's client date.


def fetch(ticker):
    query = urllib.parse.urlencode({"period1": int(START.timestamp()),
                                    "period2": int(END.timestamp()),
                                    "interval": "1mo", "events": "div,splits"})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?{query}"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = json.load(response)
    if raw["chart"].get("error"):
        raise ValueError(f"{ticker}: {raw['chart']['error']}")
    result = raw["chart"]["result"][0]
    adjusted = result["indicators"]["adjclose"][0]["adjclose"]
    values = {}
    for timestamp, price in zip(result["timestamp"], adjusted, strict=True):
        month = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m")
        if not "2021-10" <= month <= "2026-09":
            continue
        if price is None or not math.isfinite(price) or price <= 0:
            raise ValueError(f"{ticker}: missing or invalid adjusted close for {month}")
        if month in values:
            raise ValueError(f"{ticker}: duplicate month {month}")
        values[month] = price
    expected = {f"{year:04d}-{month:02d}" for year in range(2021, 2027)
                for month in range(1, 13) if "2021-10" <= f"{year:04d}-{month:02d}" <= "2026-09"}
    if set(values) != expected:
        raise ValueError(f"{ticker}: incomplete five-year window; missing {sorted(expected - values.keys())}")
    return values, {"ticker": ticker, "fund_name": result["meta"].get("longName"),
                    "source": url, "download_date": DOWNLOAD_DATE,
                    "field": "indicators.adjclose[0].adjclose", "observations": len(values)}


def main():
    series, metadata = {}, []
    for ticker in TICKERS:
        series[ticker], source = fetch(ticker)
        metadata.append(source)
        print(f"{ticker}: {source['fund_name']}; {len(series[ticker])} monthly adjusted closes")
    folder = Path(__file__).resolve().parent
    with (folder / "prices.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Date", *TICKERS])
        for month in sorted(series[TICKERS[0]]):
            writer.writerow([month + "-01", *(format(series[t][month], ".10f") for t in TICKERS)])
    (folder / "prices-sources.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
