"""FIN439 Lab 10 pro forma model for Palantir Technologies (PLTR).

Built from the Lab 09 ABG engine with Palantir's opening balance sheet and assumptions.
All values are in USD millions except per-share output.

What changed from ABG:
- Floor plan is replaced by contract liabilities (deferred revenue plus customer deposits).
  Customers prepay, so this line finances working capital the way floor plan did for ABG.
- Inventory is replaced by accounts receivable (Palantir has no inventory).
- Stock-based compensation is a non-cash expense that is added back in the cash flow and
  credited to equity, then deducted again in the valuation because it is a real cost to owners.
- Cash and marketable securities are one line and earn interest income. Interest income is
  removed from valuation FCFE, and the opening balance is added back once at the end.
- There is no term debt and no impairment line.
"""

from collections import OrderedDict


YEARS = [2026, 2027, 2028, 2029, 2030]

MIN_CASH = (
    1_500.0,
    "judgment",
    "about 2025 year-end cash excluding securities; roughly two months of 2026 costs",
)
REVOLVER_LIMIT = (
    500.0,
    "history",
    "2025 10-K: $500M facility, undrawn, matures March 2027; assumed renewed",
)

OPENING = {
    "revenue": 4_475.446,
    # Cash and cash equivalents 1,423.796 + marketable securities 5,753.247
    "cash": 7_177.043,
    "receivables": 1_042.065,
    "ppe": 51.960,
    # Prepaid and other current 139.066 + operating lease ROU 200.105 + other assets 290.153
    "other_assets": 629.324,
    # Deferred revenue 408.963 + customer deposits 357.066 + deferred revenue noncurrent 46.216
    # + customer deposits noncurrent 0.018
    "contract_liabilities": 812.263,
    # Accounts payable 8.064 + accrued 355.624 + lease liabilities 45.864 + 183.474
    # + other noncurrent 7.092
    "other_liabilities": 600.118,
    "debt": 0.0,
    # Total equity including noncontrolling interests of 100.743
    "equity": 7_488.011,
    "revolver": 0.0,
}

NONCONTROLLING_INTEREST = 100.743

ASSUMPTIONS = {
    "revenue_growth": (
        {2026: 0.822, 2027: 0.45, 2028: 0.32, 2029: 0.25, 2030: 0.20},
        "guidance/judgment",
        "2026 is the $8.154B guidance midpoint from the Q2 2026 release (guidance); "
        "2027-2030 is my taper as the base gets bigger (judgment)",
    ),
    "gross_margin": (
        0.820,
        "judgment",
        "2025 was 82.4%, 2023-2024 about 80.5%; I shaved a little because AI compute "
        "hosting costs grow with usage",
    ),
    "sga_gp": (
        {2026: 0.38, 2027: 0.35, 2028: 0.33, 2029: 0.32, 2030: 0.31},
        "judgment",
        "fell from 70.8% to 64.4% to 46.5% in three years; sales costs grow slower than "
        "gross profit because existing customers drove most 2025 growth",
    ),
    "rnd_revenue": (
        0.11,
        "judgment",
        "18.2%, 17.7%, 12.5% of revenue; the platforms are already built, so R&D keeps "
        "falling as a share but not as fast as 2025",
    ),
    "sbc_revenue": (
        {2026: 0.10, 2027: 0.095, 2028: 0.09, 2029: 0.085, 2030: 0.08},
        "judgment",
        "21.4%, 24.1%, 15.3% of revenue; dollars were flat in 2025 while revenue grew 56%, "
        "so the share keeps falling",
    ),
    "depreciation_ratio": (
        26.145 / 39.638,
        "history",
        "2025 depreciation and amortization divided by opening PP&E (three-year asset lives)",
    ),
    "capex_revenue": (
        0.007,
        "history",
        "0.68%, 0.44%, 0.76% of revenue; about the 3-year average",
    ),
    "tax_rate": (
        {2026: 0.05, 2027: 0.10, 2028: 0.18, 2029: 0.21, 2030: 0.21},
        "judgment",
        "8.3%, 4.3%, 1.4% effective; $2.6B of tax-effected NOLs under a full valuation "
        "allowance run out as pretax income passes $3B a year, then 21% federal",
    ),
    "receivable_days": (
        80.0,
        "judgment",
        "59.8, 73.2, 85.0 days; I assume collections improve slightly from 2025 year-end",
    ),
    "contract_liability_revenue": (
        812.263 / 4_475.446,
        "history",
        "2025 contract liabilities divided by 2025 revenue (21.9%, 19.8%, 18.1% history)",
    ),
    "other_working_capital_ratio": (
        0.0,
        "judgment",
        "none: other assets 629 and other liabilities 600 nearly offset, so net other "
        "working capital does not grow with revenue",
    ),
    "interest_yield": (
        0.035,
        "judgment",
        "2025 was 4.38% (229.2 on 5,230 opening cash and securities); lower rates in 2026",
    ),
    "revolver_rate": (
        0.060,
        "judgment",
        "safety net, unused in the base case",
    ),
    "buyback": (
        100.0,
        "judgment",
        "actuals were 0, 64, 75; a $1B program authorized August 2023 is still open",
    ),
    "cost_of_equity": (
        0.110,
        "judgment",
        "same 11% cost of equity I used in the Lab 06 DCF; high-beta stock",
    ),
    "terminal_growth": (
        0.030,
        "judgment",
        "long-run nominal economy, same as Lab 06; must stay below cost of equity",
    ),
    "shares_outstanding": (
        2_565.197,
        "fact",
        "2025 10-K diluted weighted-average shares, same count as Labs 03, 06, 08",
    ),
}


def assumption_value(name):
    return ASSUMPTIONS[name][0]


def yearly(name, year):
    value = assumption_value(name)
    return value[year] if isinstance(value, dict) else value


def assumption_rows():
    rows = [
        ("MIN_CASH", MIN_CASH),
        ("REVOLVER_LIMIT", REVOLVER_LIMIT),
    ]
    rows.extend(ASSUMPTIONS.items())
    return rows


def format_assumption_value(name, value):
    if isinstance(value, dict):
        return " / ".join(f"{rate:.1%}" for rate in value.values())
    if name == "shares_outstanding":
        return f"{value:,.3f}M"
    if name in {"buyback", "MIN_CASH", "REVOLVER_LIMIT"}:
        return f"${value:,.1f}M"
    if name == "receivable_days":
        return f"{value:.1f} days"
    return f"{value:.2%}"


def build_model():
    """Project the model year by year: income statement, balance sheet, then cash last."""
    results = OrderedDict()
    opening = dict(OPENING)

    for year in YEARS:
        revenue = opening["revenue"] * (1.0 + yearly("revenue_growth", year))
        gross_profit = revenue * assumption_value("gross_margin")
        sga = gross_profit * yearly("sga_gp", year)
        rnd = revenue * assumption_value("rnd_revenue")
        depreciation = opening["ppe"] * assumption_value("depreciation_ratio")
        # SBC sits inside cost of revenue, SG&A and R&D in the 10-K. It is shown here as a
        # memo line only, so it is not deducted a second time.
        sbc = revenue * yearly("sbc_revenue", year)
        operating_income = gross_profit - sga - rnd - depreciation
        interest_income = opening["cash"] * assumption_value("interest_yield")
        interest_expense = opening["revolver"] * assumption_value("revolver_rate")
        pretax_income = operating_income + interest_income - interest_expense
        tax = max(0.0, pretax_income) * yearly("tax_rate", year)
        net_income = pretax_income - tax

        receivables = revenue * assumption_value("receivable_days") / 365.0
        contract_liabilities = revenue * assumption_value("contract_liability_revenue")
        capex = revenue * assumption_value("capex_revenue")
        ppe = opening["ppe"] + capex - depreciation
        change_revenue = revenue - opening["revenue"]
        change_other_working_capital = (
            assumption_value("other_working_capital_ratio") * change_revenue
        )
        other_assets = opening["other_assets"] + change_other_working_capital
        other_liabilities = opening["other_liabilities"]
        debt = opening["debt"]
        buyback = assumption_value("buyback")
        equity = opening["equity"] + net_income + sbc - buyback

        change_receivables = receivables - opening["receivables"]
        change_contract_liabilities = (
            contract_liabilities - opening["contract_liabilities"]
        )
        fcfe = (
            net_income
            + depreciation
            + sbc
            - capex
            - change_receivables
            - change_other_working_capital
            + change_contract_liabilities
        )

        cash_before_revolver = opening["cash"] + fcfe - buyback
        revolver = opening["revolver"]
        cash = cash_before_revolver
        revolver_draw = 0.0
        revolver_repayment = 0.0

        if cash < MIN_CASH[0]:
            needed = MIN_CASH[0] - cash
            availability = REVOLVER_LIMIT[0] - revolver
            revolver_draw = min(needed, availability)
            revolver += revolver_draw
            cash += revolver_draw
        elif cash > MIN_CASH[0] and revolver > 0.0:
            excess_cash = cash - MIN_CASH[0]
            revolver_repayment = min(excess_cash, revolver)
            revolver -= revolver_repayment
            cash -= revolver_repayment

        net_change_cash = fcfe - buyback + revolver_draw - revolver_repayment

        assets = cash + receivables + ppe + other_assets
        liabilities_and_equity = (
            contract_liabilities + other_liabilities + debt + revolver + equity
        )
        balance_gap = assets - liabilities_and_equity

        # Valuation cash flow: take out interest earned on the cash pile (the opening pile is
        # added once at the end) and charge SBC as the cost of paying staff in shares.
        after_tax_interest_income = interest_income * (1.0 - yearly("tax_rate", year))
        valuation_fcfe = fcfe - after_tax_interest_income - sbc

        results[year] = {
            "Revenue": revenue,
            "Gross Profit": gross_profit,
            "SG&A": sga,
            "R&D": rnd,
            "Depreciation": depreciation,
            "Operating Income": operating_income,
            "Interest Income": interest_income,
            "Interest Expense": interest_expense,
            "Pretax Income": pretax_income,
            "Tax": tax,
            "Net Income": net_income,
            "SBC (memo, inside opex)": sbc,
            "Receivables": receivables,
            "Contract Liabilities": contract_liabilities,
            "PP&E": ppe,
            "Other Assets": other_assets,
            "Debt": debt,
            "Other Liabilities": other_liabilities,
            "Equity": equity,
            "Opening Cash": opening["cash"],
            "Opening PP&E": opening["ppe"],
            "Opening Debt": opening["debt"],
            "Opening Revolver": opening["revolver"],
            "Opening Equity": opening["equity"],
            "Capex": capex,
            "Increase in Receivables": change_receivables,
            "Increase in Other Working Capital": change_other_working_capital,
            "Increase in Contract Liabilities": change_contract_liabilities,
            "FCFE": fcfe,
            "After-tax Interest Income": after_tax_interest_income,
            "Valuation FCFE": valuation_fcfe,
            "Buyback": buyback,
            "Cash Before Revolver": cash_before_revolver,
            "Revolver Draw": revolver_draw,
            "Revolver Repayment": revolver_repayment,
            "Net Change in Cash": net_change_cash,
            "Ending Cash": cash,
            "Ending Revolver": revolver,
            "Assets": assets,
            "Liabilities + Equity": liabilities_and_equity,
            "Balance Gap": balance_gap,
        }

        opening = {
            "revenue": revenue,
            "cash": cash,
            "receivables": receivables,
            "ppe": ppe,
            "other_assets": other_assets,
            "contract_liabilities": contract_liabilities,
            "other_liabilities": other_liabilities,
            "debt": debt,
            "equity": equity,
            "revolver": revolver,
        }

    return results


def model_checks(results):
    checks = OrderedDict()
    for year, row in results.items():
        balance_gap = row["Assets"] - row["Liabilities + Equity"]
        cash_change = (
            row["FCFE"]
            - row["Buyback"]
            + row["Revolver Draw"]
            - row["Revolver Repayment"]
        )
        cash_tie_gap = row["Ending Cash"] - (row["Opening Cash"] + cash_change)
        ppe_gap = row["PP&E"] - (
            row["Opening PP&E"] + row["Capex"] - row["Depreciation"]
        )
        revolver_gap = row["Ending Revolver"] - (
            row["Opening Revolver"] + row["Revolver Draw"] - row["Revolver Repayment"]
        )
        debt_gap = (row["Debt"] - row["Opening Debt"]) + revolver_gap
        equity_gap = row["Equity"] - (
            row["Opening Equity"]
            + row["Net Income"]
            + row["SBC (memo, inside opex)"]
            - row["Buyback"]
        )
        cash_floor_gap = row["Ending Cash"] - MIN_CASH[0]

        checks[year] = [
            ("Balance", balance_gap, abs(balance_gap) <= 0.05),
            ("Cash tie", cash_tie_gap, abs(cash_tie_gap) <= 0.05),
            ("PP&E roll-forward", ppe_gap, abs(ppe_gap) <= 0.05),
            ("Debt roll-forward", debt_gap, abs(debt_gap) <= 0.05),
            ("Equity roll-forward", equity_gap, abs(equity_gap) <= 0.05),
            ("Cash floor", cash_floor_gap, cash_floor_gap >= -0.05),
        ]
    return checks


def check_model(results, print_results=False):
    """Raise if any projected year fails a model check."""
    checks = model_checks(results)
    failures = []

    if print_results:
        print("Model Checks")
        print("------------")

    for year in results:
        year_label = f"FY{year}E"
        for check_name, gap, ok in checks[year]:
            if print_results:
                status = "OK" if ok else "FAIL"
                print(f"{year_label} {check_name}: {status}, gap {format_gap(gap)}")
            if not ok:
                failures.append((year, year_label, check_name, gap))

    if print_results:
        print()

    if failures:
        year, year_label, check_name, gap = failures[0]
        if check_name == "Cash floor":
            ending_cash = results[year]["Ending Cash"]
            raise ValueError(
                f"{year_label} Cash floor check failed: ending cash {ending_cash:.2f} is {abs(gap):.2f} below the {MIN_CASH[0]:.1f} floor"
            )
        raise ValueError(f"{year_label} {check_name} check failed with gap {gap:.6f}")


def value_equity(results):
    check_model(results)
    cost_of_equity = assumption_value("cost_of_equity")
    terminal_growth = assumption_value("terminal_growth")
    if terminal_growth >= cost_of_equity:
        raise ValueError(
            f"Terminal growth ({terminal_growth:.1%}) must be below cost of equity ({cost_of_equity:.1%}): "
            "a growing perpetuity above the required return is not a valuation."
        )

    negative_years = [year for year in YEARS if results[year]["Valuation FCFE"] < 0.0]
    if negative_years:
        print(f"Negative FCFE in {negative_years}: only positive years are valued.")

    pv_fcfe = 0.0
    for period, year in enumerate(YEARS, start=1):
        cash_flow = max(0.0, results[year]["Valuation FCFE"])
        pv_fcfe += cash_flow / ((1.0 + cost_of_equity) ** period)

    terminal_fcfe = results[YEARS[-1]]["Valuation FCFE"]
    if terminal_fcfe <= 0.0:
        raise ValueError(
            "Terminal FCFE is negative: a perpetuity of a cash outflow is not a value."
        )
    terminal_value = (
        terminal_fcfe
        * (1.0 + terminal_growth)
        / (cost_of_equity - terminal_growth)
    )
    pv_terminal_value = terminal_value / ((1.0 + cost_of_equity) ** len(YEARS))
    opening_cash = OPENING["cash"]
    equity_value = pv_fcfe + pv_terminal_value + opening_cash - NONCONTROLLING_INTEREST
    value_per_share = equity_value / assumption_value("shares_outstanding")
    terminal_share = pv_terminal_value / equity_value

    return {
        "PV FCFE": pv_fcfe,
        "Terminal Value": terminal_value,
        "PV Terminal Value": pv_terminal_value,
        "Opening Cash and Securities": opening_cash,
        "Noncontrolling Interest": NONCONTROLLING_INTEREST,
        "Equity Value": equity_value,
        "Share of Value After 2030": terminal_share,
        "Value Per Share": value_per_share,
    }


def print_table(title, results, lines):
    print(title)
    print("-" * len(title))
    header = f"{'Metric':<30}" + "".join(f"{year:>12}" for year in YEARS)
    print(header)
    for label, key in lines:
        values = "".join(f"{results[year][key]:>12,.1f}" for year in YEARS)
        print(f"{label:<30}{values}")
    print()


def print_assumptions():
    print("Assumptions")
    print("-----------")
    print(f"{'Name':<30}{'Value':<40}{'Label':<20}Reason")
    for name, assumption in assumption_rows():
        value, label, reason = assumption
        formatted_value = format_assumption_value(name, value)
        print(f"{name:<30}{formatted_value:<40}{label:<20}{reason}")
    print()


def format_gap(gap):
    if abs(gap) <= 0.0000005:
        gap = 0.0
    return f"{gap:,.1f}"


def print_checks(results):
    check_model(results, print_results=True)


def print_valuation(valuation):
    print("Valuation")
    print("---------")
    print(f"PV of 2026-2030 valuation FCFE: {valuation['PV FCFE']:,.1f}")
    print(f"PV of terminal value: {valuation['PV Terminal Value']:,.1f}")
    print(f"+ Opening cash and securities: {valuation['Opening Cash and Securities']:,.1f}")
    print(f"- Noncontrolling interest: {valuation['Noncontrolling Interest']:,.1f}")
    print(f"Equity value: {valuation['Equity Value']:,.1f}")
    print(f"Share of value after 2030: {valuation['Share of Value After 2030']:.1%}")
    print(f"Value per share: ${valuation['Value Per Share']:.2f}")


def main():
    results = build_model()

    print_assumptions()
    print_table(
        "Income Statement",
        results,
        [
            ("Revenue", "Revenue"),
            ("Gross Profit", "Gross Profit"),
            ("SG&A", "SG&A"),
            ("R&D", "R&D"),
            ("Depreciation", "Depreciation"),
            ("Operating Income", "Operating Income"),
            ("Interest Income", "Interest Income"),
            ("Interest Expense", "Interest Expense"),
            ("Pretax Income", "Pretax Income"),
            ("Tax", "Tax"),
            ("Net Income", "Net Income"),
            ("SBC (memo, inside opex)", "SBC (memo, inside opex)"),
        ],
    )
    print_table(
        "Balance Sheet",
        results,
        [
            ("Cash and Securities", "Ending Cash"),
            ("Receivables", "Receivables"),
            ("PP&E", "PP&E"),
            ("Other Assets", "Other Assets"),
            ("Contract Liabilities", "Contract Liabilities"),
            ("Other Liabilities", "Other Liabilities"),
            ("Debt", "Debt"),
            ("Revolver", "Ending Revolver"),
            ("Equity", "Equity"),
            ("Assets", "Assets"),
            ("Liabilities + Equity", "Liabilities + Equity"),
        ],
    )
    print_table(
        "Cash Flow",
        results,
        [
            ("Net Income", "Net Income"),
            ("+ Depreciation", "Depreciation"),
            ("+ SBC", "SBC (memo, inside opex)"),
            ("- Capex", "Capex"),
            ("- Increase in Receivables", "Increase in Receivables"),
            ("- Increase in Other WC", "Increase in Other Working Capital"),
            ("+ Increase in Contract Liab.", "Increase in Contract Liabilities"),
            ("FCFE", "FCFE"),
            ("- Buyback", "Buyback"),
            ("+ Revolver Draw", "Revolver Draw"),
            ("- Revolver Repayment", "Revolver Repayment"),
            ("Net Change in Cash", "Net Change in Cash"),
            ("Opening Cash", "Opening Cash"),
            ("Ending Cash", "Ending Cash"),
        ],
    )
    print_table(
        "Valuation FCFE",
        results,
        [
            ("FCFE", "FCFE"),
            ("- After-tax Interest Income", "After-tax Interest Income"),
            ("- SBC", "SBC (memo, inside opex)"),
            ("Valuation FCFE", "Valuation FCFE"),
        ],
    )
    print_checks(results)
    valuation = value_equity(results)
    print_valuation(valuation)


if __name__ == "__main__":
    main()
