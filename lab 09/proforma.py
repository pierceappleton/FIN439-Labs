"""FIN439 Lab 09 pro forma model for Asbury Automotive Group (ABG).

All values are in USD millions except per-share output.
"""

from collections import OrderedDict


YEARS = [2026, 2027, 2028, 2029, 2030]

MIN_CASH = 25.0
REVOLVER_LIMIT = 850.0

OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
    "revolver": 0.0,
}

ASSUMPTIONS = {
    "organic_growth": 0.018,
    "gross_margin": 0.1705,
    "sga_gp": {
        2026: 0.665,
        2027: 0.655,
        2028: 0.645,
        2029: 0.645,
        2030: 0.645,
    },
    "depreciation_ratio": 82.4 / 3_070.4,
    "impairment": 120.0,
    "capex": 250.0,
    "tax_rate": 0.255,
    "inventory_days": 2_135.8 / (17_999.0 - 3_071.7) * 365.0,
    "floor_plan_inventory_ratio": 2_027.0 / 2_135.8,
    "other_working_capital_ratio": 0.008,
    "revolver_rate": 0.060,
    "debt_repayment": 150.0,
    "buyback": 150.0,
    "floor_plan_rate": 0.0467,
    "term_debt_rate": 0.0544,
    "cost_of_equity": 0.100,
    "terminal_growth": 0.025,
    "shares_outstanding": 17.951349,
}


def build_model():
    """Project the model year by year in the order required by the lab."""
    results = OrderedDict()
    opening = dict(OPENING)

    for year in YEARS:
        revenue = opening["revenue"] * (1.0 + ASSUMPTIONS["organic_growth"])
        gross_profit = revenue * ASSUMPTIONS["gross_margin"]
        sga = gross_profit * ASSUMPTIONS["sga_gp"][year]
        depreciation = opening["ppe"] * ASSUMPTIONS["depreciation_ratio"]
        impairment = ASSUMPTIONS["impairment"]
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (
            opening["floor_plan"] * ASSUMPTIONS["floor_plan_rate"]
            + opening["term_debt"] * ASSUMPTIONS["term_debt_rate"]
            + opening["revolver"] * ASSUMPTIONS["revolver_rate"]
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * ASSUMPTIONS["tax_rate"]
        net_income = pretax_income - tax

        inventory = (
            (revenue - gross_profit) * ASSUMPTIONS["inventory_days"] / 365.0
        )
        floor_plan = inventory * ASSUMPTIONS["floor_plan_inventory_ratio"]
        ppe = opening["ppe"] + ASSUMPTIONS["capex"] - depreciation
        change_revenue = revenue - opening["revenue"]
        change_other_working_capital = (
            ASSUMPTIONS["other_working_capital_ratio"] * change_revenue
        )
        other_assets = opening["other_assets"] + change_other_working_capital - impairment
        term_debt = opening["term_debt"] - ASSUMPTIONS["debt_repayment"]
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - ASSUMPTIONS["buyback"]

        change_inventory = inventory - opening["inventory"]
        change_floor_plan = floor_plan - opening["floor_plan"]
        fcfe = (
            net_income
            + depreciation
            + impairment
            - ASSUMPTIONS["capex"]
            - change_inventory
            - change_other_working_capital
            + change_floor_plan
            - ASSUMPTIONS["debt_repayment"]
        )

        cash_before_revolver = opening["cash"] + fcfe - ASSUMPTIONS["buyback"]
        revolver = opening["revolver"]
        cash = cash_before_revolver
        revolver_draw = 0.0
        revolver_repayment = 0.0

        if cash < MIN_CASH:
            needed = MIN_CASH - cash
            availability = REVOLVER_LIMIT - revolver
            revolver_draw = min(needed, availability)
            revolver += revolver_draw
            cash += revolver_draw
        elif cash > MIN_CASH and revolver > 0.0:
            excess_cash = cash - MIN_CASH
            revolver_repayment = min(excess_cash, revolver)
            revolver -= revolver_repayment
            cash -= revolver_repayment

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
            "FCFE": fcfe,
            "Cash Before Revolver": cash_before_revolver,
            "Revolver Draw": revolver_draw,
            "Revolver Repayment": revolver_repayment,
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


def assert_balanced(results):
    """Raise if any projected year is out of balance or below minimum cash."""
    for year, row in results.items():
        year_label = f"FY{year}E"
        gap = row["Balance Gap"]
        if abs(gap) > 0.05:
            raise ValueError(f"{year_label} balance sheet gap is {gap:.6f}")
        if row["Ending Cash"] < MIN_CASH - 1e-9:
            raise ValueError(
                f"{year_label} ending cash is {row['Ending Cash']:.6f}, below {MIN_CASH:.1f}"
            )


def value_equity(results):
    cost_of_equity = ASSUMPTIONS["cost_of_equity"]
    terminal_growth = ASSUMPTIONS["terminal_growth"]

    pv_fcfe = 0.0
    for period, year in enumerate(YEARS, start=1):
        pv_fcfe += results[year]["FCFE"] / ((1.0 + cost_of_equity) ** period)

    terminal_fcfe = results[2030]["FCFE"] + ASSUMPTIONS["debt_repayment"]
    terminal_value = (
        terminal_fcfe
        * (1.0 + terminal_growth)
        / (cost_of_equity - terminal_growth)
    )
    pv_terminal_value = terminal_value / ((1.0 + cost_of_equity) ** len(YEARS))
    equity_value = pv_fcfe + pv_terminal_value
    value_per_share = equity_value / ASSUMPTIONS["shares_outstanding"]
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


def print_checks(results):
    print("Balance Checks")
    print("--------------")
    for year in YEARS:
        row = results[year]
        print(
            f"{year}: Assets {row['Assets']:.1f}; "
            f"Liabilities + Equity {row['Liabilities + Equity']:.1f}; "
            f"Assets - Liabilities - Equity {row['Balance Gap']:.1f}; "
            f"Ending Cash {row['Ending Cash']:.1f}"
        )
    print()


def print_valuation(valuation):
    print("Valuation")
    print("---------")
    print(f"Equity value: {valuation['Equity Value']:.1f}")
    print(f"Share of value after 2030: {valuation['Share of Value After 2030']:.1%}")
    print(f"Value per share: ${valuation['Value Per Share']:.2f}")


def main():
    results = build_model()
    assert_balanced(results)
    valuation = value_equity(results)

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
            ("FCFE", "FCFE"),
            ("Cash Before Revolver", "Cash Before Revolver"),
            ("Revolver Draw", "Revolver Draw"),
            ("Revolver Repayment", "Revolver Repayment"),
            ("Ending Cash", "Ending Cash"),
        ],
    )
    print_checks(results)
    print_valuation(valuation)


if __name__ == "__main__":
    main()
