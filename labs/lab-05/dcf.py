"""Five-year FCFF DCF model for FIN 439 Lab 05.

Run ``python dcf.py`` for the lab training case. Run ``python dcf.py --live``
to refresh factual inputs from Yahoo Finance for the ticker below.
"""

import sys

# Editable inputs, in USD millions except rates and per-share output.
TICKER = "PLTR"
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0


def discount(value, year, rate):
    return value / ((1 + rate) ** year)


def validate_inputs():
    """Fail early with a useful message when an editable input is invalid."""
    if not GROWTH_RATES:
        raise ValueError("GROWTH_RATES must contain at least one forecast year.")
    if STARTING_FCFF < 0:
        raise ValueError("STARTING_FCFF cannot be negative.")
    if WACC <= -1:
        raise ValueError("WACC must be greater than -100%.")
    if TERMINAL_GROWTH >= WACC:
        raise ValueError("terminal growth must be less than WACC.")
    if DILUTED_SHARES <= 0:
        raise ValueError("DILUTED_SHARES must be greater than zero.")


def load_live_inputs():
    """Replace factual inputs with the latest annual Yahoo Finance values."""
    from finance import FinanceDataError, fetch_financials

    global STARTING_FCFF, CASH, DEBT, DILUTED_SHARES
    try:
        data = fetch_financials(TICKER)
    except FinanceDataError as error:
        print(f"Error: {error}")
        return None

    STARTING_FCFF = data["starting_fcff"]
    CASH = data["cash"]
    DEBT = data["debt"]
    DILUTED_SHARES = data["diluted_shares"]
    return data


def main():
    live_data = None
    if "--live" in sys.argv[1:]:
        live_data = load_live_inputs()
        if live_data is None:
            return

    try:
        validate_inputs()
    except ValueError as error:
        print(f"Error: {error}")
        return

    fcff_values = []
    fcff = STARTING_FCFF
    for growth_rate in GROWTH_RATES:
        fcff *= 1 + growth_rate
        fcff_values.append(fcff)

    pv_explicit_fcff = sum(
        discount(fcff, year, WACC)
        for year, fcff in enumerate(fcff_values, start=1)
    )
    forecast_years = len(fcff_values)
    terminal_value = (
        fcff_values[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    )
    pv_terminal_value = discount(terminal_value, forecast_years, WACC)
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + CASH - DEBT
    value_per_share = equity_value / DILUTED_SHARES
    pv_tv_share_of_ev = pv_terminal_value / enterprise_value

    for year, fcff in enumerate(fcff_values, start=1):
        print(f"FCFF Year {year}: {fcff:,.4f}")
    print(f"PV of explicit FCFF: {pv_explicit_fcff:,.4f}")
    print(f"Terminal value, Year {forecast_years}: {terminal_value:,.4f}")
    print(f"PV of terminal value: {pv_terminal_value:,.4f}")
    print(f"Enterprise value: {enterprise_value:,.4f}")
    print(f"Equity value: {equity_value:,.4f}")
    print(f"Value per share: {value_per_share:,.4f}")
    print(f"PV of TV / enterprise value: {pv_tv_share_of_ev:,.4f}")

    if live_data is not None:
        print(f"Yahoo Finance price ({live_data['ticker']}): {live_data['price']:,.4f}")
        print(f"Yahoo Finance data date: {live_data['as_of']}")
        print("Note: growth rates, WACC, and terminal growth remain editable assumptions.")


if __name__ == "__main__":
    main()