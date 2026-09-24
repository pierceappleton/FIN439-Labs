"""Small, dependency-free Yahoo Finance data client for the FIN 439 DCF.

Yahoo Finance is an unofficial public data source. The returned fundamentals
are annual reported values and are converted from USD to USD millions.
"""

from datetime import datetime, timedelta, timezone
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://query2.finance.yahoo.com"
USER_AGENT = "FIN439-DCF/1.0 (educational use)"


class FinanceDataError(RuntimeError):
    """Raised when Yahoo Finance data cannot be retrieved or parsed."""


def _get_json(url):
    request = Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except Exception as error:
        raise FinanceDataError(f"Yahoo Finance request failed: {error}") from error


def _latest_value(timeseries, field):
    values = timeseries.get(field, [])
    if not values:
        raise FinanceDataError(f"Yahoo Finance did not return {field}.")
    latest = values[-1]
    try:
        return latest["reportedValue"]["raw"], latest["asOfDate"]
    except (KeyError, TypeError) as error:
        raise FinanceDataError(f"Yahoo Finance returned an invalid {field} value.") from error


def _annual_value(ticker, field, period1, period2):
    params = {
        "symbol": ticker,
        "period1": int(period1.timestamp()),
        "period2": int(period2.timestamp()),
        "type": field,
    }
    url = f"{BASE_URL}/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}?{urlencode(params)}"
    response = _get_json(url)
    try:
        timeseries = response["timeseries"]["result"][0]
    except (KeyError, IndexError, TypeError) as error:
        raise FinanceDataError(f"Yahoo Finance returned no fundamentals for {ticker}.") from error
    return _latest_value(timeseries, field)


def fetch_financials(ticker="PLTR"):
    """Return current market data and latest annual DCF inputs for *ticker*."""
    ticker = ticker.upper().strip()
    if not ticker:
        raise FinanceDataError("Ticker cannot be blank.")

    chart_url = f"{BASE_URL}/v8/finance/chart/{ticker}?{urlencode({'range': '1d', 'interval': '1d'})}"
    chart = _get_json(chart_url)
    try:
        meta = chart["chart"]["result"][0]["meta"]
        price = meta.get("regularMarketPrice")
        if price is None:
            raise KeyError("regularMarketPrice")
    except (KeyError, IndexError, TypeError) as error:
        raise FinanceDataError(f"Yahoo Finance returned no current price for {ticker}.") from error

    period2 = datetime.now(timezone.utc)
    period1 = period2 - timedelta(days=365 * 5)
    fcff, as_of = _annual_value(ticker, "annualFreeCashFlow", period1, period2)
    cash, _ = _annual_value(ticker, "annualCashAndCashEquivalents", period1, period2)
    debt, _ = _annual_value(ticker, "annualTotalDebt", period1, period2)
    shares, _ = _annual_value(ticker, "annualDilutedAverageShares", period1, period2)

    return {
        "ticker": ticker,
        "price": float(price),
        "as_of": as_of,
        "starting_fcff": fcff / 1_000_000,
        "cash": cash / 1_000_000,
        "debt": debt / 1_000_000,
        "diluted_shares": shares / 1_000_000,
    }