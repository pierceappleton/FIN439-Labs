"""Run: python -m streamlit run labs/lab-15/app.py."""
import hashlib
import importlib
import io
from pathlib import Path
import sys

import streamlit as st

ENGINE = Path(__file__).resolve().parents[1] / "lab-14"
sys.path.insert(0, str(ENGINE))
import portfolio

# Reload on rerun so editing the engine's correlation table updates this page.
p = importlib.reload(portfolio)
st.set_page_config(page_title="Portfolio stability", layout="wide")
st.title("Portfolio stability lab")
st.caption("Built with AI help, a learning demonstration, not investment advice.")
st.write("Find the lowest-volatility mix meeting your return objective and reserve rule.")

objective = st.sidebar.number_input("Objective (%)", value=6.5, step=0.1) / 100
minimum = st.sidebar.number_input("Reserve minimum (%)", 0.0, 100.0, 3.0, 1.0) / 100
upload = st.sidebar.file_uploader("Monthly adjusted prices CSV", type="csv")
use_example = st.sidebar.checkbox("Use saved Project 2 prices", value=False)
last_36 = st.sidebar.toggle("Last 36 monthly returns", value=False)
raw = upload.getvalue() if upload is not None else (
    (ENGINE / "prices.csv").read_bytes() if use_example else None)

try:
    if raw is None:
        loaded, loaded_corr = p.SLEEVES, p.CORRELATIONS
        active, active_corr = loaded, loaded_corr
        source_key = "Meridian"
        defaults = p.RESERVE_ELIGIBLE
        st.subheader("Meridian training inputs")
        st.caption("Course-authored estimates; no market-price calibration.")
        if last_36:
            st.info("The 36-month switch applies to price data. Upload a CSV or select saved prices.")
    else:
        text = raw.decode("utf-8-sig")
        loaded, loaded_corr, full_meta = p.estimate_from_csv(io.StringIO(text))
        active, active_corr, meta = p.estimate_from_csv(io.StringIO(text), last_36)
        source_key = hashlib.sha256(raw).hexdigest()[:12]
        defaults = {"BIL", "IEF"}
        st.subheader("Uploaded prices" if upload is not None else "Project 2 saved prices")
        st.caption(f"Historical arithmetic return estimates, not forecasts. "
                   f"{meta['returns']} monthly returns from {meta['prices']} prices; "
                   f"price window {meta['start']} to {meta['end']}. "
                   "Annual mean = monthly mean × 12; sample volatility annualized by √12.")

    st.write("Edit annual expected return estimates and select reserve-eligible assets.")
    edited, eligible = [], set()
    for name, mean, vol in active:
        left, right = st.columns([3, 2])
        estimate = left.number_input(f"{name} return estimate (%)", value=mean * 100,
                                     step=0.1, key=f"return-{source_key}-{last_36}-{name}")
        if right.checkbox(f"{name} reserve eligible", value=name in defaults,
                          key=f"reserve-{source_key}-{name}"):
            eligible.add(name)
        edited.append((name, estimate / 100, vol))

    baseline = p.search(loaded, loaded_corr, objective, minimum, eligible)
    current = p.search(edited, active_corr, objective, minimum, eligible)

    def show_result(title, result):
        st.subheader(title)
        if result is None:
            st.warning("no mix meets the objective")
            st.caption("No feasible mix on the 5-point grid under the selected reserve rule.")
            return
        st.table([{"Asset": s[0], "Weight (%)": f"{w * 100:.2f}"}
                  for s, w in zip(loaded, result["weights"])])
        st.metric("Expected return estimate", f"{result['expected_return']:.2%}")
        st.metric("Annual volatility estimate", f"{result['volatility']:.2%}")
        st.metric("Reserve-eligible weight", f"{result['reserve']:.2%}")

    left, right = st.columns(2)
    with left:
        show_result("As loaded · all months", baseline)
    with right:
        show_result("Current estimates / selected window", current)
    change = p.largest_weight_change(baseline, current)
    if change is None:
        st.info("Largest weight change: undefined because at least one run is infeasible.")
    else:
        st.metric("Largest weight change (percentage points)", f"{change:.2f}")
    st.caption("Long-only, fully invested, 5-point steps. Minimum volatility on this grid; "
               "other mandate provisions such as turnover, costs and future losses need separate review. "
               "Both columns use the selected objective and reserve rule.")
except (ValueError, UnicodeError) as error:
    st.error(f"Input error: {error}")
