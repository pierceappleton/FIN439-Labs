"""Lab 14 portfolio risk engine. Returns and volatilities use decimal units."""
import math

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
