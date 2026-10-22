"""Lab 14 portfolio risk engine. Returns and volatilities use decimal units."""
import math
import csv
import statistics
from datetime import date

SLEEVES = (
    ("Treasury bills", 0.035, 0.005),
    ("Treasury 10-year note", 0.043, 0.070),
    ("Investment-grade bond fund", 0.050, 0.060),
    ("Global equity index fund", 0.080, 0.160),
)
CORRELATIONS = (
    (1.00, 0.10, 0.05, 0.00),
    (0.10, 1.00, 0.80, -0.10),
    (0.05, 0.80, 1.00, 0.25),
    (0.00, -0.10, 0.25, 1.00),
)
OBJECTIVE_RETURN = 0.065  # CPI estimate 2.5% + 4% objective.
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_inputs(sleeves, correlations):
    n = len(sleeves)
    if not n or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be square and match the sleeves.")
    for name, expected_return, volatility in sleeves:
        if not math.isfinite(expected_return) or not math.isfinite(volatility) or volatility <= 0:
            raise ValueError(f"{name}: return must be finite and volatility positive and finite.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation [{i}][{j}] must be between -1 and 1.")
            if not math.isclose(value, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError("Correlation table must be symmetric.")
        if not math.isclose(correlations[i][i], 1.0, rel_tol=0, abs_tol=1e-12):
            raise ValueError("Correlation diagonal must equal 1.")


def covariance_matrix(sleeves, correlations):
    validate_inputs(sleeves, correlations)
    return [[correlations[i][j] * sleeves[i][2] * sleeves[j][2]
             for j in range(len(sleeves))] for i in range(len(sleeves))]


def equal_weights(sleeves):
    return [1 / len(sleeves)] * len(sleeves)


def inverse_volatility_weights(sleeves):
    inverse = [1 / sleeve[2] for sleeve in sleeves]
    return [value / sum(inverse) for value in inverse]


def expected_return(weights, sleeves):
    return sum(weight * sleeve[1] for weight, sleeve in zip(weights, sleeves, strict=True))


def portfolio_volatility(weights, covariance):
    if len(covariance) != len(weights) or any(len(row) != len(weights) for row in covariance):
        raise ValueError("Covariance dimensions must match weights.")
    # Both (i,j) and (j,i) are included, so cross-asset covariance counts twice.
    variance = sum(weights[i] * weights[j] * covariance[i][j]
                   for i in range(len(weights)) for j in range(len(weights)))
    if variance < -1e-12:
        raise ValueError("Negative portfolio variance: check the correlation inputs.")
    return math.sqrt(max(variance, 0.0))


def reserve_weight(weights, sleeves):
    return sum(w for w, sleeve in zip(weights, sleeves, strict=True)
               if sleeve[0] in RESERVE_ELIGIBLE)


def meets_objective(value, objective):
    return value >= objective


def portfolios(sleeves):
    benchmark = {"Investment-grade bond fund": 0.4, "Global equity index fund": 0.6}
    return {"Benchmark": [benchmark.get(s[0], 0.0) for s in sleeves],
            "Equal weight": equal_weights(sleeves),
            "Inverse volatility": inverse_volatility_weights(sleeves)}


def weight_grid(n, units=20):
    """Yield every fully invested long-only allocation in five-point steps."""
    if n == 1:
        yield (units / 20,)
    else:
        for first in range(units + 1):
            for rest in weight_grid(n - 1, units - first):
                yield (first / 20,) + rest


def search(sleeves, correlations, objective=OBJECTIVE_RETURN,
           reserve_minimum=0.03, reserve_eligible=None):
    """Return the minimum-volatility feasible grid mix, or None.

    Equal-risk ties retain the first allocation in deterministic grid order.
    Reserve eligibility is supplied by name, so uploaded tickers work too.
    """
    if not 3 <= len(sleeves) <= 6:
        raise ValueError("Search requires three to six assets.")
    if not math.isfinite(objective) or not 0 <= reserve_minimum <= 1:
        raise ValueError("Objective must be finite and reserve minimum between 0 and 1.")
    eligible = RESERVE_ELIGIBLE if reserve_eligible is None else set(reserve_eligible)
    covariance = covariance_matrix(sleeves, correlations)
    best = None
    for weights in weight_grid(len(sleeves)):
        value = expected_return(weights, sleeves)
        reserve = sum(w for w, s in zip(weights, sleeves) if s[0] in eligible)
        if value + 1e-12 < objective or reserve + 1e-12 < reserve_minimum:
            continue
        risk = portfolio_volatility(weights, covariance)
        if best is None or risk < best["volatility"] - 1e-12:
            best = dict(weights=weights, expected_return=value,
                        volatility=risk, reserve=reserve)
    return best


def estimate_from_csv(source, last_36=False):
    """Estimate annual arithmetic means, sample volatilities and correlations.

    Last 36 means 36 monthly returns, using 37 prices. Never fill missing data.
    Accept a text file-like object or path. Return inputs plus window metadata.
    """
    if hasattr(source, "read"):
        rows = list(csv.reader(source))
    else:
        with open(source, encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
    if not rows or not 4 <= len(rows[0]) <= 7:
        raise ValueError("CSV needs date first and three to six ticker columns.")
    names = [s.strip() for s in rows[0][1:]]
    if len(set(names)) != len(names) or not all(names):
        raise ValueError("Ticker names must be nonempty and unique.")
    dates, prices = [], []
    for row in rows[1:]:
        if len(row) != len(names) + 1:
            raise ValueError("Each CSV row must contain one date and all prices.")
        try:
            day = date.fromisoformat(row[0])
            values = [float(x) for x in row[1:]]
        except ValueError as error:
            raise ValueError("Use ISO dates YYYY-MM-DD and numeric adjusted prices.") from error
        if any(not math.isfinite(x) or x <= 0 for x in values):
            raise ValueError("Prices must be positive and finite.")
        if dates and day.year * 12 + day.month != dates[-1].year * 12 + dates[-1].month + 1:
            raise ValueError("Prices must be oldest first with consecutive, unique months.")
        dates.append(day)
        prices.append(values)
    if len(prices) < (37 if last_36 else 3):
        raise ValueError("Need 37 prices for 36 returns, or at least 3 for all months.")
    if last_36:
        prices, dates = prices[-37:], dates[-37:]
    returns = [[prices[t][i] / prices[t-1][i] - 1 for t in range(1, len(prices))]
               for i in range(len(names))]
    if any(statistics.stdev(series) <= 0 for series in returns):
        raise ValueError("Each asset needs nonzero sample volatility.")
    sleeves = tuple((name, statistics.mean(series) * 12,
                     statistics.stdev(series) * math.sqrt(12))
                    for name, series in zip(names, returns))
    correlations = [[1.0 if i == j else max(-1.0, min(1.0, statistics.correlation(a, b)))
                     for j, b in enumerate(returns)] for i, a in enumerate(returns)]
    return sleeves, correlations, dict(prices=len(prices), returns=len(prices)-1,
                                      start=dates[0].isoformat(), end=dates[-1].isoformat())


def largest_weight_change(first, second):
    """Percentage points, undefined if either search is infeasible."""
    if first is None or second is None:
        return None
    return 100 * max(abs(a-b) for a, b in zip(first["weights"], second["weights"], strict=True))


def main():
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    print(f"Objective: {OBJECTIVE_RETURN:.2%} (CPI estimate 2.5% + 4%)")
    for name, weights in portfolios(SLEEVES).items():
        print(f"\n{name}")
        for sleeve, weight in zip(SLEEVES, weights, strict=True):
            print(f"  {sleeve[0]}: {weight:.1%}")
        value = expected_return(weights, SLEEVES)
        print(f"  Expected return: {value:.2%}")
        print(f"  Volatility: {portfolio_volatility(weights, covariance):.2%}")
        print(f"  Reserve-eligible: {reserve_weight(weights, SLEEVES):.1%}")
        print(f"  Meets objective: {'yes' if meets_objective(value, OBJECTIVE_RETURN) else 'no'}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        raise SystemExit(f"Input error: {error}") from error
