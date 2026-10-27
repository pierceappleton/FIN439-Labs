"""Lab 16: a point-in-time provenance gate. Run with python asof.py."""
from datetime import date

# Editable inputs: row number, ticker, month measured, published on, price.
DECISION_DATE = "2026-03-31"
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def filter_rows(table, decision_date=None):
    """Apply the rules in order. None means ignore the publication cutoff."""
    removed = {"No ticker": [], "Exact duplicate": [],
               "Published after decision date": [], "Older vintage": []}
    rows = []
    for row in table:
        if not row[1].strip():
            removed["No ticker"].append(row[0])
        else:
            rows.append(row)

    unique, seen = [], set()
    for row in rows:
        # Row number identifies the record; it is not part of its data.
        if row[1:] in seen:
            removed["Exact duplicate"].append(row[0])
        else:
            seen.add(row[1:])
            unique.append(row)

    eligible = []
    for row in unique:
        if decision_date is not None and date.fromisoformat(row[3]) > decision_date:
            removed["Published after decision date"].append(row[0])
        else:
            eligible.append(row)

    # For each ticker and measured month, select the latest eligible publication.
    latest = {}
    for row in eligible:
        key = (row[1], row[2])
        if key not in latest or row[3] > latest[key][3]:
            if key in latest:
                removed["Older vintage"].append(latest[key][0])
            latest[key] = row
        else:
            removed["Older vintage"].append(row[0])
    return sorted(latest.values(), key=lambda row: (row[1], row[2])), removed


def signals(panel):
    by_ticker = {}
    for row in panel:
        by_ticker.setdefault(row[1], []).append(row)
    result = {}
    for ticker, rows in sorted(by_ticker.items()):
        rows.sort(key=lambda row: row[2])
        if len(rows) < 2:
            result[ticker] = None
            continue
        previous, latest = rows[-2:]
        # Require the immediately preceding calendar month, not merely any prior row.
        year, month = map(int, latest[2].split("-"))
        previous_month = f"{year - 1 if month == 1 else year:04d}-{12 if month == 1 else month - 1:02d}"
        if previous[2] != previous_month or previous[4] == 0:
            result[ticker] = None
        else:
            result[ticker] = (latest[2], (latest[4] / previous[4] - 1) * 100)
    return result


def main():
    cutoff = date.fromisoformat(DECISION_DATE)
    panel, removed = filter_rows(TABLE, cutoff)
    naive_panel, _ = filter_rows(TABLE)
    print(f"Decision date: {cutoff}\nRow funnel:")
    for rule, numbers in removed.items():
        print(f"  {rule}: {len(numbers)} removed; rows {', '.join(map(str, sorted(numbers))) or 'none'}")
    print("\nAs-of panel (row, ticker, month, published, price):")
    for row in panel:
        print(f"  {row[0]:>2}  {row[1]:<6} {row[2]}  {row[3]}  {row[4]:.1f}")
    asof, naive = signals(panel), signals(naive_panel)
    print("\nSignals:")
    for ticker in sorted(set(asof) | set(naive)):
        def format_signal(signal):
            return "unavailable (need consecutive months and a nonzero prior price)" if signal is None else f"{signal[1]:+.2f}% ({signal[0]})"
        print(f"  {ticker}: as-of {format_signal(asof.get(ticker))}; naive {format_signal(naive.get(ticker))}")


if __name__ == "__main__":
    main()
