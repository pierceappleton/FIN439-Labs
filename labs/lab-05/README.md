# FIN439 Lab 05 - DCF Build

This folder contains my FIN439 Lab 05 work for building and checking a five-year FCFF discounted cash flow model.

## Lab Question

What is one share of the company worth on a five-year FCFF DCF, and what growth does today's price already assume?

## Files

| File | Purpose |
|---|---|
| `dcf.py` | Main five-year FCFF DCF model. Uses editable assumptions at the top of the file and prints the required labelled output lines. |
| `finance.py` | Small standard-library Yahoo Finance helper used by `dcf.py --live` to pull current factual inputs for `PLTR`. |
| `Lab05_Task_Instructions.md` | Clean copy of the Session 5 lab task and known-answer checklist. |
| `Lab05_Palantir_Context.md` | Context from earlier FIN439 Palantir research and how Lab 05 connects to the valuation work. |

## How to Run

From this folder, run:

```powershell
python dcf.py
```

The training case uses these editable assumptions:

- Starting FCFF: `100.0` USD millions
- Growth rates: `0.08`, `0.06`, `0.05`, `0.04`, `0.03`
- WACC: `0.10`
- Terminal growth: `0.03`
- Cash: `50.0` USD millions
- Debt: `300.0` USD millions
- Diluted shares: `50.0` million

## Known Answer Check

The training run should produce these key results:

- Value per share: `27.4974`
- PV of terminal value / enterprise value: `0.7240`

The script was checked against the lab's known-answer table. The terminal value is discounted five years because the Gordon-growth terminal value is measured at the end of Year 5, not at the end of Year 6.

## Optional Live Run

The script also supports an optional live-data mode:

```powershell
python dcf.py --live
```

That mode refreshes factual inputs for `PLTR` from Yahoo Finance while leaving growth rates, WACC, and terminal growth as editable assumptions. Yahoo Finance is an unofficial public data source, so any final submission should still tie company-specific facts back to primary or assignment-approved sources.

## Current Research Context

My prior FIN439 Palantir work supports a `watch-defer` call. The company has strong operating momentum in the research packet, but the investment case still needs stronger valuation discipline, independent risk evidence, and price-implied growth analysis before moving to an initiate-buy conclusion.
