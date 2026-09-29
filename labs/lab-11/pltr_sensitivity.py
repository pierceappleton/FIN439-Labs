"""Lab 11 one-at-a-time sensitivity analysis for the Lab 10 PLTR pro forma."""

from copy import deepcopy
import importlib.util
from pathlib import Path

SOURCE = Path(__file__).parents[1] / "lab-10" / "pltr_proforma.py"
spec = importlib.util.spec_from_file_location("pltr_proforma", SOURCE)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

BASE = deepcopy(model.ASSUMPTIONS)
DRIVERS = {
    "revenue_growth": {
        "label": "Revenue growth",
        "units": "percent of prior-year revenue; percentage-point shift",
        "lower": {2026: 0.722, 2027: 0.350, 2028: 0.220, 2029: 0.150, 2030: 0.100},
        "base": {2026: 0.822, 2027: 0.450, 2028: 0.320, 2029: 0.250, 2030: 0.200},
        "higher": {2026: 0.922, 2027: 0.550, 2028: 0.420, 2029: 0.350, 2030: 0.300},
        "range_reason": "A +/-10 percentage-point path tests execution below/above the Lab 10 judgment while preserving the same taper shape.",
    },
    "gross_margin": {
        "label": "Gross margin",
        "units": "percent of revenue",
        "lower": 0.790,
        "base": 0.820,
        "higher": 0.850,
        "range_reason": "79%-85% brackets the recent 80.2%-82.4% history and a modest compute-cost upside/downside case.",
    },
}


def run(driver, case, value):
    model.ASSUMPTIONS.clear()
    model.ASSUMPTIONS.update(deepcopy(BASE))
    if driver is not None:
        model.ASSUMPTIONS[driver] = (deepcopy(value), "Lab 11 sensitivity", DRIVERS[driver]["range_reason"])
    results = model.build_model()
    checks = model.model_checks(results)
    valid = all(ok for rows in checks.values() for _, _, ok in rows)
    valuation = None
    error = ""
    if valid:
        try:
            valuation = model.value_equity(results)
        except ValueError as exc:
            error = str(exc)
    final = results[model.YEARS[-1]]
    return {
        "driver": driver, "case": case, "input": deepcopy(value), "valid": valid,
        "operating_profit": final["Operating Income"], "fcfe": final["FCFE"],
        "value_per_share": None if valuation is None else valuation["Value Per Share"],
        "results": results, "checks": checks, "valuation_error": error,
    }


def fmt_input(driver, value):
    if isinstance(value, dict):
        return "/".join(f"{value[y]:.1%}" for y in model.YEARS)
    return f"{value:.1%}"


def span(rows, key):
    values = [r[key] for r in rows if r[key] is not None]
    return max(values) - min(values) if values else None


def print_trace(r):
    year = model.YEARS[-1]
    row = r["results"][year]
    print(f"\nTrace: {DRIVERS[r['driver']]['label']} {r['case']} case, FY{year}E (USD millions)")
    for key in ("Revenue", "Gross Profit", "SG&A", "R&D", "Depreciation", "Operating Income",
                "Interest Income", "Pretax Income", "Tax", "Net Income", "SBC (memo, inside opex)",
                "Increase in Receivables", "Increase in Contract Liabilities", "FCFE", "Valuation FCFE"):
        print(f"  {key:<34}{row[key]:>12,.1f}")


def main():
    first_base = run(None, "base", None)
    all_runs = []
    for driver, definition in DRIVERS.items():
        for case in ("lower", "base", "higher"):
            all_runs.append(run(driver, case, definition[case]))

    bases = {r["driver"] + "_base": r for r in all_runs if r["case"] == "base"}
    print("LAB 11 PLTR ONE-AT-A-TIME SENSITIVITY | USD millions except per share")
    print("Only the named independent input changes; all other assumptions reset to Lab 10 base before each run.")
    print("Driver | Case | Actual input | Operating profit 2030 | FCFE 2030 | Value/share | Checks")
    print("---|---|---|---:|---:|---:|---")
    for r in all_runs:
        base = bases[r["driver"] + "_base"]
        op_change = r["operating_profit"] - base["operating_profit"]
        fcfe_change = r["fcfe"] - base["fcfe"]
        v_change = None if r["value_per_share"] is None else r["value_per_share"] - base["value_per_share"]
        value_text = "n/a" if r["value_per_share"] is None else f"${r['value_per_share']:.2f} ({v_change:+.2f})"
        print(f"{DRIVERS[r['driver']]['label']} | {r['case']} | {fmt_input(r['driver'], r['input'])} | ${r['operating_profit']:,.1f} ({op_change:+,.1f}) | ${r['fcfe']:,.1f} ({fcfe_change:+,.1f}) | {value_text} | {'PASS' if r['valid'] else 'INVALID'}")
    print("\nOutput spans (maximum minus minimum across lower/base/higher):")
    for driver in DRIVERS:
        rows = [r for r in all_runs if r["driver"] == driver and r["valid"]]
        vps = span(rows, "value_per_share")
        vps_text = "n/a" if vps is None else f"${vps:,.2f}"
        print(f"{DRIVERS[driver]['label']}: operating profit ${span(rows, 'operating_profit'):,.1f}; FCFE ${span(rows, 'fcfe'):,.1f}; value/share {vps_text}")

    print_trace(next(r for r in all_runs if r["driver"] == "revenue_growth" and r["case"] == "higher"))
    print_trace(first_base | {"driver": "revenue_growth", "case": "base"})

    restored = run(None, "base", None)
    inputs_match = model.ASSUMPTIONS == BASE
    tolerance = 0.01
    outputs_match = all(
        abs(restored[k] - first_base[k]) <= tolerance
        for k in ("operating_profit", "fcfe", "value_per_share")
    )
    print("\nRestored base vs. first base run (tolerance 0.01):")
    print(f"  Operating profit 2030: ${first_base['operating_profit']:,.1f} -> ${restored['operating_profit']:,.1f}")
    print(f"  FCFE 2030:             ${first_base['fcfe']:,.1f} -> ${restored['fcfe']:,.1f}")
    print(f"  Value/share:           ${first_base['value_per_share']:.2f} -> ${restored['value_per_share']:.2f}")
    print("Restored base check:", "PASS" if inputs_match and outputs_match and restored["valid"] else "INVESTIGATE")


if __name__ == "__main__":
    main()
