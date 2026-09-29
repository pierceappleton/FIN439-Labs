# Lab 11: Pro-Forma Sensitivity — Palantir Technologies (PLTR)

Pierce Appleton  
Partner: Ethan Heeres  
Date: September 29, 2026  
Model: [Lab 10 pro forma](../lab-10/pltr_proforma.py)  
Run: `python pltr_sensitivity.py`

## D — Question

Which assumptions drive Palantir's forecast and value, and what explains their effects?

## R — Drivers and locked changed-input record

I selected two independent operating inputs from the Lab 10 assumption table:

| Driver | Base | Lower | Higher | Units / affected years | Range reason |
|---|---|---|---|---|---|
| Revenue growth | 82.2%, 45%, 32%, 25%, 20% | 72.2%, 35%, 22%, 15%, 10% | 92.2%, 55%, 42%, 35%, 30% | % of prior-year revenue, 2026–2030 | ±10 percentage points tests execution around the judgment path while preserving its taper. |
| Gross margin | 82.0% | 79.0% | 85.0% | % of revenue, 2026–2030 | Brackets recent 80.2%–82.4% history plus a modest compute-cost upside/downside case. |

The ranges are labeled judgments, not probabilities. The model uses FCFE consistently; value per share is shown because the Lab 10 terminal FCFE remains positive and its accounting checks pass.

**Locked prediction, recorded before the runs:**

- Timestamp: September 29, 2026, before `python pltr_sensitivity.py`.
- Revenue growth: base path → minus/plus 10 percentage points in every forecast year. I predicted lower growth would reduce 2030 operating profit, FCFE, and value per share, with the largest effect of roughly $5–6B on operating profit and FCFE across the full span.
- Gross margin: 82% → 79% / 85%. I predicted lower margin would reduce all three outputs, with a smaller effect than revenue growth because margin changes apply to revenue but do not change the revenue path.
- Partner unit check: Ethan checked that growth is percentage points, margin is percent of revenue, and only one independent input changes per run.

## I/V — Sensitivity evidence

All figures below are USD millions except value per share. Parentheses are signed changes from that driver's own base run. Every run reset all other independent assumptions to the Lab 10 base; linked statements recalculated.

| Driver | Case | Actual input | 2030 operating profit | 2030 FCFE | Value/share | Checks |
|---|---|---|---:|---:|---:|---|
| Revenue growth | Lower | 72.2% / 35% / 22% / 15% / 10% | $7,223.8 (-3,324.0) | $7,708.7 (-3,214.9) | $25.57 (-8.96) | PASS |
| Revenue growth | Base | 82.2% / 45% / 32% / 25% / 20% | $10,547.8 (+0.0) | $10,923.6 (+0.0) | $34.53 (+0.00) | PASS |
| Revenue growth | Higher | 92.2% / 55% / 42% / 35% / 30% | $14,987.8 (+4,440.0) | $15,174.7 (+4,251.1) | $46.27 (+11.74) | PASS |
| Gross margin | Lower | 79.0% | $10,063.2 (-484.6) | $10,514.3 (-409.3) | $33.04 (-1.50) | PASS |
| Gross margin | Base | 82.0% | $10,547.8 (+0.0) | $10,923.6 (+0.0) | $34.53 (+0.00) | PASS |
| Gross margin | Higher | 85.0% | $11,032.4 (+484.6) | $11,332.8 (+409.3) | $36.03 (+1.50) | PASS |

Output spans over these tested ranges:

| Driver | Operating profit span | FCFE span | Value/share span |
|---|---:|---:|---:|
| Revenue growth | $7,764.0M | $7,466.0M | $20.70 |
| Gross margin | $969.2M | $818.5M | $3.00 |

The restored base rerun matched Lab 10: 2030 operating profit $10,547.8M, 2030 FCFE $10,923.6M, and $34.53 per share; all checks passed. The selected result can be traced through revenue → gross profit → operating income → net income/FCFE → valuation FCFE → terminal value.

## E — Driver conclusion and partner evidence

Over these ranges, revenue growth is the larger driver of operating profit, FCFE, and value per share. The ranking is range-dependent: the growth test moves five yearly inputs by 10 percentage points, while the margin test moves one percentage assumption by 3 points each way. That is why this is a conclusion about the tested ranges, not a universal claim that growth is always more important.

Mechanism: higher revenue growth compounds the revenue base every year. It increases gross profit, operating income, net income, and working-capital cash flows; the resulting valuation FCFE also raises the terminal value. Higher gross margin keeps the same revenue path but changes gross profit directly, so its effect is more limited.

**Partner exchange 2.** Ethan checked the revenue-growth higher case against the base: $14,987.8M − $10,547.8M = $4,440.0M, verified that gross margin and all other assumptions stayed at base, and asked me to trace the statement link. My answer: the higher growth path compounds into a larger revenue base, then gross profit and operating income rise; the cash-flow and terminal-value effects explain the higher FCFE and value. Prediction: direction was correct, but the effect was larger than my locked $5–6B estimate. The actual spans were $7,764.0M for operating profit and $7,466.0M for FCFE, because the growth shift compounds on a bigger revenue base each year (2030 revenue $33,226.7M higher case vs. $23,410.9M base).

**Partner exchange 3.** Ethan asked whether growth “wins” only because its range is wider. I answered yes, the ranking is conditional on the chosen ranges; a fairer comparison would equalize economic ranges or use elasticity in a follow-up. I asked Ethan which of his company's inputs changed both its operating result and cash conversion, and recorded his response in my class notes.

## Learn on your own

1. One-at-a-time sensitivity changes one independent input while resetting every other independent assumption to base, then compares the linked model outputs at lower, base, and higher values.
2. The chosen input range can determine the ranking: a wider or more aggressive range creates a larger output span even if the input is not intrinsically more important.
3. A sensitivity table is not a forecast probability. It shows conditional model outputs under selected scenarios; it does not assign likelihoods or say which case will occur.

## Reflection

Revenue growth mattered most over my tested ranges. The surprising result was how large the growth effect became: a 10-percentage-point path shift produced a $20.70 per-share span because the change compounds across five years and affects the terminal value.

## Files

- [Sensitivity code](pltr_sensitivity.py)
- [Lab 10 model](../lab-10/pltr_proforma.py)
- [This write-up](lab-11-writeup.md)
