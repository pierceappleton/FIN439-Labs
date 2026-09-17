"""Lab 08 P/E comparable-company calculator for Palantir.

Edit TARGET and PEERS to reuse the calculator for another company. The
calculation uses price per share and GAAP diluted EPS only; it does not bridge
P/E-implied prices with cash or debt.
"""

from statistics import median


TARGET = {
    "ticker": "PLTR",
    "name": "Palantir Technologies",
    "role": "target",
    "price": 165.86,
    "eps": 0.63,
}

PEERS = [
    {
        "ticker": "MSFT",
        "name": "Microsoft",
        "role": "qualified candidate peer",
        "price": 492.44,
        "eps": 17.95,
    },
    {
        "ticker": "CRM",
        "name": "Salesforce",
        "role": "qualified candidate peer",
        "price": 243.00,
        "eps": 7.80,
    },
]


def is_positive_number(value):
    return isinstance(value, (int, float)) and value > 0


def money(value):
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def multiple(value):
    return f"{value:.6f}x"


def display_money(value):
    if not is_positive_number(value):
        return "not meaningful"
    return money(value)


def display_eps(value):
    if not is_positive_number(value):
        return "not meaningful"
    return f"${value:.2f}"


def clean_peers(target, peers):
    """Deduplicate peers by ticker, excluding the target if included."""
    seen = set()
    cleaned = []
    target_ticker = target["ticker"].strip().upper()

    for peer in peers:
        ticker = peer["ticker"].strip().upper()
        if ticker == target_ticker or ticker in seen:
            continue
        seen.add(ticker)
        cleaned.append(peer)

    return cleaned


def pe_ratio(company):
    price = company.get("price")
    eps = company.get("eps")
    if not is_positive_number(price) or not is_positive_number(eps):
        return None
    return price / eps


def valid_peer_multiples(peers):
    results = []
    for peer in peers:
        ratio = pe_ratio(peer)
        if ratio is not None:
            results.append((peer, ratio))
    return results


def implied_prices(target_eps, ratios):
    if not is_positive_number(target_eps):
        return None
    return {
        "min": min(ratios) * target_eps,
        "median": median(ratios) * target_eps,
        "max": max(ratios) * target_eps,
    }


def print_inputs(target, peers):
    print("Lab 08: Palantir P/E Comparable-Company Calculator")
    print("=" * 58)
    print("Comparison inputs")
    print(f"Target: {target['name']} ({target['ticker']})")
    print(f"  Price: {display_money(target.get('price'))}")
    print(f"  Annual GAAP diluted EPS: {display_eps(target.get('eps'))}")
    print("Peers:")
    for peer in peers:
        print(
            f"  {peer['name']} ({peer['ticker']}), {peer['role']}: "
            f"price {display_money(peer.get('price'))}, "
            f"EPS {display_eps(peer.get('eps'))}"
        )
    print()


def print_peer_table(peers):
    print("Peer P/E calculations")
    valid_results = []
    for peer in peers:
        ratio = pe_ratio(peer)
        if ratio is None:
            print(f"  {peer['ticker']}: not meaningful")
        else:
            valid_results.append((peer, ratio))
            print(f"  {peer['ticker']}: {multiple(ratio)}")
    print()
    return valid_results


def print_implied_valuation(target, valid_results):
    print("Palantir implied valuation")
    if not valid_results:
        print("  No usable peers.")
        print()
        return None

    ratios = [ratio for _, ratio in valid_results]
    prices = implied_prices(target["eps"], ratios)
    if prices is None:
        print("  Target EPS is not meaningful, so implied prices are not meaningful.")
        print()
        return None

    median_ratio = median(ratios)
    print(f"  Peer median P/E: {multiple(median_ratio)}")

    if len(valid_results) == 1:
        print(f"  Reference estimate: {money(prices['median'])}")
    else:
        print(f"  Peer-implied range: {money(prices['min'])}-{money(prices['max'])}")
        print(f"  Median-implied price: {money(prices['median'])}")
    print()
    return prices["median"]


def print_leave_one_out(target, peers, full_estimate):
    print("Leave-one-out sensitivity")
    if full_estimate is None:
        print("  Full-peer estimate is not meaningful, so changes are not meaningful.")
        return

    for removed in peers:
        remaining = [peer for peer in peers if peer["ticker"] != removed["ticker"]]
        remaining_results = valid_peer_multiples(remaining)
        if not remaining_results:
            print(f"  Remove {removed['ticker']}: no estimate")
            continue

        ratios = [ratio for _, ratio in remaining_results]
        prices = implied_prices(target["eps"], ratios)
        if prices is None:
            print(f"  Remove {removed['ticker']}: not meaningful")
            continue

        estimate = prices["median"]
        change = estimate - full_estimate
        print(
            f"  Remove {removed['ticker']}: remaining median-implied price "
            f"{money(estimate)}; change from full-peer estimate {money(change)}"
        )


def main():
    peers = clean_peers(TARGET, PEERS)
    print_inputs(TARGET, peers)
    valid_results = print_peer_table(peers)
    full_estimate = print_implied_valuation(TARGET, valid_results)
    print_leave_one_out(TARGET, peers, full_estimate)


if __name__ == "__main__":
    main()
