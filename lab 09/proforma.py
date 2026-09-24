"""FIN439 Lab 09 pro forma model for Asbury Automotive Group (ABG).

All values are in USD millions except per-share output.
"""

from collections import OrderedDict


YEARS = [2026, 2027, 2028, 2029, 2030]

MIN_CASH = (25.0, "judgment", "cash floor kept as a small operating cushion")
REVOLVER_LIMIT = (
    850.0,
    "judgment",
    "safety net, unused in the base case",
)

OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    # Other assets is the grouped residual line and likely absorbs the 0.2 filing rounding difference; confirm against the 2025 10-K balance sheet.
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
    "revolver": 0.0,
}

ASSUMPTIONS = {
    "organic_growth": (
        0.018,
        "judgment",
        "same-store revenue grew 1.2%; acquisitions excluded",
    ),
    "gross_margin": (
        0.1705,
        "judgment",
        "2025 margin held flat; the shortage-era premium is gone",
    ),
    "sga_gp": (
        {
            2026: 0.665,
            2027: 0.655,
            2028: 0.645,
            2029: 0.645,
            2030: 0.645,
        },
        "judgment",
        "Herb Chambers integration raises costs in 2026, then partial recovery toward the 2024 level",
    ),
    "depreciation_ratio": (
        82.4 / 3_070.4,
        "history",
        "2025 depreciation divided by opening PP&E",
    ),
    "impairment": (
        120.0,
        "judgment",
        "below the 3-year average of 136; recurring and non-cash",
    ),
    "capex": (
        250.0,
        "guidance",
        "management's 2026 figure; holding it 5 years is judgment and 1H 2026 ran about 339 annualized",
    ),
    "tax_rate": (
        0.255,
        "judgment",
        "between the 3-year average of 25.2% and the 2025 rate of 25.7%",
    ),
    "inventory_days": (
        2_135.8 / (17_999.0 - 3_071.7) * 365.0,
        "history",
        "2025 inventory days",
    ),
    "floor_plan_inventory_ratio": (
        2_027.0 / 2_135.8,
        "history",
        "2025 floor plan debt divided by inventory",
    ),
    "other_working_capital_ratio": (
        0.008,
        "judgment",
        "other working capital moves at 0.8% of the revenue change",
    ),
    "revolver_rate": (
        0.060,
        "judgment",
        "safety net, unused in the base case",
    ),
    "debt_repayment": (
        150.0,
        "judgment",
        "steady annual paydown assumption",
    ),
    "buyback": (
        150.0,
        "judgment",
        "actuals were 260, 185, 100",
    ),
    "floor_plan_rate": (
        0.0467,
        "history",
        "2025 interest divided by opening floor plan balance",
    ),
    "term_debt_rate": (
        0.0544,
        "history",
        "2025 interest divided by opening term debt balance",
    ),
    "cost_of_equity": (
        0.100,
        "judgment",
        "starting convention; measured beta comes later",
    ),
    "terminal_growth": (
        0.025,
        "judgment",
        "must stay below cost of equity",
    ),
    "shares_outstanding": (
        17.951349,
        "fact",
        "June 2026 10-Q, 40.1M issued less 22.15M treasury",
    ),
}


def assumption_value(name):
    return ASSUMPTIONS[name][0]


def assumption_rows():
    rows = [
        ("MIN_CASH", MIN_CASH),
        ("REVOLVER_LIMIT", REVOLVER_LIMIT),
    ]
    rows.extend(ASSUMPTIONS.items())
    return rows


def format_assumption_value(name, value):
    if name == "sga_gp":
        return " / ".join(f"{year}: {rate:.1%}" for year, rate in value.items())
    if name == "shares_outstanding":
        return f"{value:.6f}M"
    if name in {"impairment", "capex", "debt_repayment", "buyback", "MIN_CASH"}:
        return f"${value:.1f}M"
    if name == "REVOLVER_LIMIT":
        return f"${value:.1f}M"
    if name == "inventory_days":
        return f"{value:.1f} days"
    if name in {
        "organic_growth",
        "gross_margin",
        "depreciation_ratio",
        "tax_rate",
        "floor_plan_inventory_ratio",
        "other_working_capital_ratio",
        "revolver_rate",
        "floor_plan_rate",
        "term_debt_rate",
        "cost_of_equity",
        "terminal_growth",
    }:
        return f"{value:.2%}"
    return str(value)


def build_model():
    """Project the model year by year in the order required by the lab."""
    results = OrderedDict()
    opening = dict(OPENING)

    for year in YEARS:
        revenue = opening["revenue"] * (1.0 + assumption_value("organic_growth"))
        gross_profit = revenue * assumption_value("gross_margin")
        sga = gross_profit * assumption_value("sga_gp")[year]
        depreciation = opening["ppe"] * assumption_value("depreciation_ratio")
        impairment = assumption_value("impairment")
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (
            opening["floor_plan"] * assumption_value("floor_plan_rate")
            + opening["term_debt"] * assumption_value("term_debt_rate")
            + opening["revolver"] * assumption_value("revolver_rate")
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * assumption_value("tax_rate")
        net_income = pretax_income - tax

        inventory = (
            (revenue - gross_profit) * assumption_value("inventory_days") / 365.0
        )
        floor_plan = inventory * assumption_value("floor_plan_inventory_ratio")
        ppe = opening["ppe"] + assumption_value("capex") - depreciation
        change_revenue = revenue - opening["revenue"]
        change_other_working_capital = (
            assumption_value("other_working_capital_ratio") * change_revenue
        )
        other_assets = opening["other_assets"] + change_other_working_capital - impairment
        debt_repayment = assumption_value("debt_repayment")
        buyback = assumption_value("buyback")
        term_debt = opening["term_debt"] - debt_repayment
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - buyback

        change_inventory = inventory - opening["inventory"]
        change_floor_plan = floor_plan - opening["floor_plan"]
        fcfe = (
            net_income
            + depreciation
            + impairment
            - assumption_value("capex")
            - change_inventory
            - change_other_working_capital
            + change_floor_plan
            - debt_repayment
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

        assets = cash + inventory + ppe + other_assets
        liabilities_and_equity = (
            floor_plan + term_debt + revolver + other_liabilities + equity
        )
        balance_gap = assets - liabilities_and_equity

        results[year] = {
            "Revenue": revenue,
            "Gross Profit": gross_profit,
            "SG&A": sga,
            "Depreciation": depreciation,
            "Impairment": impairment,
            "Operating Income": operating_income,
            "Interest": interest,
            "Pretax Income": pretax_income,
            "Tax": tax,
            "Net Income": net_income,
            "Inventory": inventory,
            "Floor Plan Debt": floor_plan,
            "PP&E": ppe,
            "Other Assets": other_assets,
            "Term Debt": term_debt,
            "Other Liabilities": other_liabilities,
            "Equity": equity,
            "Opening Cash": opening["cash"],
            "Opening PP&E": opening["ppe"],
            "Opening Term Debt": opening["term_debt"],
            "Opening Revolver": opening["revolver"],
            "Capex": assumption_value("capex"),
            "Increase in Inventory": change_inventory,
            "Increase in Other Working Capital": change_other_working_capital,
            "Increase in Floor Plan": change_floor_plan,
            "Debt Repayment": debt_repayment,
            "FCFE": fcfe,
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
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "floor_plan": floor_plan,
            "term_debt": term_debt,
            "other_liabilities": other_liabilities,
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
            row["Opening PP&E"] + assumption_value("capex") - row["Depreciation"]
        )
        term_debt_gap = row["Term Debt"] - (
            row["Opening Term Debt"] - row["Debt Repayment"]
        )
        revolver_gap = row["Ending Revolver"] - (
            row["Opening Revolver"] + row["Revolver Draw"] - row["Revolver Repayment"]
        )
        debt_gap = term_debt_gap + revolver_gap
        cash_floor_gap = row["Ending Cash"] - MIN_CASH[0]

        checks[year] = [
            ("Balance", balance_gap, abs(balance_gap) <= 0.05),
            ("Cash tie", cash_tie_gap, abs(cash_tie_gap) <= 0.05),
            ("PP&E roll-forward", ppe_gap, abs(ppe_gap) <= 0.05),
            ("Debt roll-forward", debt_gap, abs(term_debt_gap) <= 0.05 and abs(revolver_gap) <= 0.05),
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

    for year, row in results.items():
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


def assert_balanced(results):
    check_model(results)


def value_equity(results):
    check_model(results)
    cost_of_equity = assumption_value("cost_of_equity")
    terminal_growth = assumption_value("terminal_growth")
    if terminal_growth >= cost_of_equity:
        raise ValueError(
            f"Terminal growth ({terminal_growth:.1%}) must be below cost of equity ({cost_of_equity:.1%}): "
            "a growing perpetuity above the required return is not a valuation."
        )

    pv_fcfe = 0.0
    for period, year in enumerate(YEARS, start=1):
        pv_fcfe += results[year]["FCFE"] / ((1.0 + cost_of_equity) ** period)

    terminal_fcfe = results[2030]["FCFE"] + assumption_value("debt_repayment")
    terminal_value = (
        terminal_fcfe
        * (1.0 + terminal_growth)
        / (cost_of_equity - terminal_growth)
    )
    pv_terminal_value = terminal_value / ((1.0 + cost_of_equity) ** len(YEARS))
    equity_value = pv_fcfe + pv_terminal_value
    value_per_share = equity_value / assumption_value("shares_outstanding")
    terminal_share = pv_terminal_value / equity_value

    return {
        "PV FCFE": pv_fcfe,
        "Terminal Value": terminal_value,
        "PV Terminal Value": pv_terminal_value,
        "Equity Value": equity_value,
        "Share of Value After 2030": terminal_share,
        "Value Per Share": value_per_share,
    }


def print_table(title, results, lines):
    print(title)
    print("-" * len(title))
    header = f"{'Metric':<24}" + "".join(f"{year:>12}" for year in YEARS)
    print(header)
    for label, key in lines:
        values = "".join(f"{results[year][key]:>12.1f}" for year in YEARS)
        print(f"{label:<24}{values}")
    print()


def print_assumptions():
    print("Assumptions")
    print("-----------")
    print(f"{'Name':<32}{'Value':<92}{'Label':<12}Reason")
    for name, assumption in assumption_rows():
        value, label, reason = assumption
        formatted_value = format_assumption_value(name, value)
        print(f"{name:<32}{formatted_value:<92}{label:<12}{reason}")
    print()


def format_gap(gap):
    if abs(gap) <= 0.0000005:
        gap = 0.0
    return f"{gap:.1f}"


def print_checks(results):
    check_model(results, print_results=True)


def print_valuation(valuation):
    print("Valuation")
    print("---------")
    print(f"Equity value: {valuation['Equity Value']:.1f}")
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
            ("Depreciation", "Depreciation"),
            ("Impairment", "Impairment"),
            ("Operating Income", "Operating Income"),
            ("Interest", "Interest"),
            ("Pretax Income", "Pretax Income"),
            ("Tax", "Tax"),
            ("Net Income", "Net Income"),
        ],
    )
    print_table(
        "Balance Sheet",
        results,
        [
            ("Cash", "Ending Cash"),
            ("Inventory", "Inventory"),
            ("PP&E", "PP&E"),
            ("Other Assets", "Other Assets"),
            ("Floor Plan Debt", "Floor Plan Debt"),
            ("Term Debt", "Term Debt"),
            ("Revolver", "Ending Revolver"),
            ("Other Liabilities", "Other Liabilities"),
            ("Equity", "Equity"),
        ],
    )
    print_table(
        "Cash Flow",
        results,
        [
            ("Net Income", "Net Income"),
            ("+ Depreciation", "Depreciation"),
            ("+ Impairment", "Impairment"),
            ("- Capex", "Capex"),
            ("- Increase in Inventory", "Increase in Inventory"),
            ("- Increase in Other WC", "Increase in Other Working Capital"),
            ("+ Increase in Floor Plan", "Increase in Floor Plan"),
            ("- Debt Repayment", "Debt Repayment"),
            ("FCFE", "FCFE"),
            ("- Buyback", "Buyback"),
            ("+ Revolver Draw", "Revolver Draw"),
            ("- Revolver Repayment", "Revolver Repayment"),
            ("Net Change in Cash", "Net Change in Cash"),
            ("Opening Cash", "Opening Cash"),
            ("Ending Cash", "Ending Cash"),
        ],
    )
    print_checks(results)
    valuation = value_equity(results)
    print_valuation(valuation)


if __name__ == "__main__":
    main()
