"""FIN 439 Lab 06 DCF model.

Run ``python dcf.py`` to print the base DCF, sensitivity grid, and reverse DCF.
Amounts are in USD millions except rates and per-share output.
"""

# Original training inputs block:
# STARTING_FCFF = 100.0
# GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
# WACC = 0.10
# TERMINAL_GROWTH = 0.03
# CASH = 50.0
# DEBT = 300.0
# DILUTED_SHARES = 50.0
# TARGET_SHARE_PRICE = 30.00
# REVERSE_SHIFT_LOWER = -0.05
# REVERSE_SHIFT_UPPER = 0.10

COMPANY = "Palantir Technologies Inc. (PLTR)"
STARTING_FCFF = 2100.591
GROWTH_RATES = [1.19, 1.00, 0.80, 0.60, 0.40]
WACC = 0.10
TERMINAL_GROWTH = 0.03
CASH = 1423.796
DEBT = 0.0
DILUTED_SHARES = 2565.197

WACC_VALUES = [0.09, 0.10, 0.11]
TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 169.53
REVERSE_SHIFT_LOWER = -0.05
REVERSE_SHIFT_UPPER = 0.10


def discount(value, year, rate):
    return value / ((1 + rate) ** year)


def validate_inputs(wacc, terminal_growth, growth_rates):
    if not growth_rates:
        raise ValueError("GROWTH_RATES must contain at least one forecast year.")
    if STARTING_FCFF < 0:
        raise ValueError("STARTING_FCFF cannot be negative.")
    if wacc <= -1:
        raise ValueError("WACC must be greater than -100%.")
    if terminal_growth >= wacc:
        raise ValueError("terminal growth must be less than WACC.")
    if DILUTED_SHARES <= 0:
        raise ValueError("DILUTED_SHARES must be greater than zero.")
    for growth_rate in growth_rates:
        if growth_rate <= -1:
            raise ValueError("annual growth rates must stay above -100%.")


def calculate_dcf(wacc, terminal_growth, growth_rates):
    validate_inputs(wacc, terminal_growth, growth_rates)

    fcff_values = []
    fcff = STARTING_FCFF
    for growth_rate in growth_rates:
        fcff *= 1 + growth_rate
        fcff_values.append(fcff)

    pv_explicit_fcff = sum(
        discount(fcff, year, wacc)
        for year, fcff in enumerate(fcff_values, start=1)
    )
    forecast_years = len(fcff_values)
    terminal_value = (
        fcff_values[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    )
    pv_terminal_value = discount(terminal_value, forecast_years, wacc)
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + CASH - DEBT
    value_per_share = equity_value / DILUTED_SHARES
    pv_tv_share_of_ev = pv_terminal_value / enterprise_value

    return {
        "fcff_values": fcff_values,
        "pv_explicit_fcff": pv_explicit_fcff,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
        "pv_tv_share_of_ev": pv_tv_share_of_ev,
    }


def print_base_case(result):
    for year, fcff in enumerate(result["fcff_values"], start=1):
        print(f"FCFF Year {year}: {fcff:,.4f}")
    print(f"PV of explicit FCFF: {result['pv_explicit_fcff']:,.4f}")
    print(f"Terminal value, Year {len(result['fcff_values'])}: {result['terminal_value']:,.4f}")
    print(f"PV of terminal value: {result['pv_terminal_value']:,.4f}")
    print(f"Enterprise value: {result['enterprise_value']:,.4f}")
    print(f"Equity value: {result['equity_value']:,.4f}")
    print(f"Value per share: {result['value_per_share']:,.4f}")
    print(f"PV of TV / enterprise value: {result['pv_tv_share_of_ev']:,.4f}")


def print_sensitivity_grid():
    print()
    print("Sensitivity Grid: value per diluted share")
    header = "WACC \\ Terminal growth"
    print(f"{header:<24}" + "".join(f"{tg:>12.0%}" for tg in TERMINAL_GROWTH_VALUES))
    for wacc in WACC_VALUES:
        row = f"{wacc:<24.0%}"
        for terminal_growth in TERMINAL_GROWTH_VALUES:
            if terminal_growth >= wacc:
                cell = "invalid"
            else:
                value = calculate_dcf(wacc, terminal_growth, GROWTH_RATES)[
                    "value_per_share"
                ]
                cell = f"{value:,.2f}"
            row += f"{cell:>12}"
        print(row)


def shifted_growth_rates(shift):
    growth_rates = [growth_rate + shift for growth_rate in GROWTH_RATES]
    if any(growth_rate <= -1 for growth_rate in growth_rates):
        raise ValueError("shift pushes an annual growth rate to -100% or below.")
    return growth_rates


def solve_reverse_dcf():
    lower_growth_rates = shifted_growth_rates(REVERSE_SHIFT_LOWER)
    upper_growth_rates = shifted_growth_rates(REVERSE_SHIFT_UPPER)
    lower_value = calculate_dcf(WACC, TERMINAL_GROWTH, lower_growth_rates)[
        "value_per_share"
    ]
    upper_value = calculate_dcf(WACC, TERMINAL_GROWTH, upper_growth_rates)[
        "value_per_share"
    ]

    target = TARGET_SHARE_PRICE
    if not (min(lower_value, upper_value) < target < max(lower_value, upper_value)):
        return None, lower_value, upper_value

    low = REVERSE_SHIFT_LOWER
    high = REVERSE_SHIFT_UPPER
    increasing = upper_value > lower_value
    for _ in range(100):
        mid = (low + high) / 2
        mid_value = calculate_dcf(WACC, TERMINAL_GROWTH, shifted_growth_rates(mid))[
            "value_per_share"
        ]
        if abs(mid_value - target) < 0.0001:
            return mid, lower_value, upper_value
        if (mid_value < target) == increasing:
            low = mid
        else:
            high = mid

    solved_shift = (low + high) / 2
    if solved_shift in (REVERSE_SHIFT_LOWER, REVERSE_SHIFT_UPPER):
        return None, lower_value, upper_value
    return solved_shift, lower_value, upper_value


def print_reverse_dcf():
    print()
    print("Reverse DCF")
    try:
        solved_shift, lower_value, upper_value = solve_reverse_dcf()
    except ValueError as error:
        print(f"No solution: {error}")
        return

    print(f"Target share price: ${TARGET_SHARE_PRICE:,.2f}")
    if solved_shift is None:
        print(
            "No solution in bracket: "
            f"{REVERSE_SHIFT_LOWER:.2%} gives ${lower_value:,.2f}; "
            f"{REVERSE_SHIFT_UPPER:.2%} gives ${upper_value:,.2f}."
        )
    else:
        print(f"Solved uniform growth shift: {solved_shift:.2%}")
    print(
        "Inputs held fixed: "
        f"starting FCFF ${STARTING_FCFF:,.3f} million; "
        f"growth rates {[f'{growth_rate:.0%}' for growth_rate in GROWTH_RATES]}; "
        f"WACC {WACC:.0%}; terminal growth {TERMINAL_GROWTH:.0%}; "
        f"cash ${CASH:,.3f} million; debt ${DEBT:,.3f} million; "
        f"diluted shares {DILUTED_SHARES:,.3f} million."
    )


def main():
    print(f"Base DCF: {COMPANY}")
    print()
    base_case = calculate_dcf(WACC, TERMINAL_GROWTH, GROWTH_RATES)
    print_base_case(base_case)
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
