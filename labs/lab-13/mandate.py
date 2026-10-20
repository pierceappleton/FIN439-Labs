"""Meridian mandate checker. Weights and percentage thresholds use percent units."""
import math

# name: (issuer, business days to redeem, reserve eligible)
HOLDINGS = {
    "Cash": ("none", 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}
CANDIDATES = {
    "A": dict(zip(HOLDINGS, (2, 2, 10, 60, 26, 0, 0, 0))),
    "B": dict(zip(HOLDINGS, (1, 0, 0, 55, 20, 15, 5, 4))),
    "C": dict(zip(HOLDINGS, (1, 1, 0, 70, 20, 0, 0, 8))),
    "D": {"Treasury bills": 100},
    "E": {"Investment-grade bond fund": 40, "Global equity index fund": 60},
}
RESERVE_SIZE = 100.0  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MINIMUM_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def reserve_minimum():
    if RESERVE_SIZE <= 0:
        raise ValueError("Reserve size must be positive.")
    return 100 * QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE


def reserve_weight(weights):
    return sum(w for name, w in weights.items() if HOLDINGS[name][2])


def liquid_weight(weights):
    return sum(w for name, w in weights.items() if HOLDINGS[name][1] <= LIQUIDITY_WINDOW)


def largest_company(weights):
    totals = {}
    for name, weight in weights.items():
        issuer = HOLDINGS[name][0]
        if issuer not in EXEMPT_ISSUERS:
            totals[issuer] = totals.get(issuer, 0.0) + weight
    return max([0.0, *totals.values()])


def check_candidate(weights):
    if not weights or any(name not in HOLDINGS for name in weights):
        raise ValueError("Candidate must contain known holdings.")
    if any(not math.isfinite(w) for w in weights.values()):
        raise ValueError("Weights must be finite.")
    total = sum(weights.values())
    lowest = min(weights.get(name, 0.0) for name in HOLDINGS)
    reserve = reserve_weight(weights)
    liquid = liquid_weight(weights)
    company = largest_company(weights)
    return [
        ("Weights sum to 100", total, math.isclose(total, 100, rel_tol=0, abs_tol=1e-9)),
        ("Long-only (lowest weight)", lowest, lowest >= 0),
        (f"Reserve >= {reserve_minimum():.1f}%", reserve, reserve >= reserve_minimum()),
        (f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.1f}%", liquid, liquid >= MINIMUM_LIQUID_SHARE),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", company, company <= ISSUER_LIMIT),
    ]


def main():
    print(f"Reserve minimum: {reserve_minimum():.1f}%")
    for name, weights in CANDIDATES.items():
        print(f"\nCandidate {name}")
        results = check_candidate(weights)
        for rule, value, passed in results:
            print(f"  {rule}: {value:.1f}% {'pass' if passed else 'FAIL'}")
        print("  Calendar-year loss: requires CIO clarification")
        failures = sum(not passed for _, _, passed in results)
        print("  passes every checkable rule" if failures == 0 else f"  fails {failures} rule(s)")


if __name__ == "__main__":
    main()
