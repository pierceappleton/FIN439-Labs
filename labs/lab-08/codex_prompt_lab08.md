# Prompt For VS Code Codex - Complete FIN439 Lab 08 And Push To GitHub

You are working in the FIN439 course folder. Complete Lab 08 for Palantir Technologies Inc. (`PLTR`) using the prior lab context and the Lab 07 P/E calculator. Work carefully from opened sources, not unsourced AI assertions.

## Files To Use First

1. Read `Lab 08/lab08_previous_lab_context.md`.
2. Read `Lab 07/lab07_comps.py` and `Lab 07/lab07_asbury_comps_writeup.md`.
3. Read `Lab 06/lab06_dcf.md` for the Week 3 / Lab 06 DCF result and valuation date.
4. Create Lab 08 working files inside `Lab 08/`, including:
   - `lab08_palantir_pe_triangulation.md`
   - `lab08_palantir_comps.py` copied/adapted from the Lab 07 calculator

## Assignment Goal

Build and defend a peer P/E comparison for Palantir and compare it with the prior DCF. The key question is:

> What would Palantir's share be worth at defensible peer P/E multiples, and how does that compare with the discounted cash flow valuation?

Use the Lab 06 comparison date unless the sources force a better same-date choice:

- Comparison / DCF date: `2026-09-10`
- Prior DCF base-case value: `$158.1618` per diluted share
- Prior market price used in Lab 06: `$169.53` for PLTR on `2026-09-10`
- Prior DCF call: `watch-defer`

## Required Process

### 1. Reconfirm The Lab 07 Calculator

From `Lab 07`, rerun:

```powershell
python lab07_comps.py
```

Record in the Lab 08 markdown that the saved Asbury calculation still works. Include the key output values, especially the peer-implied range and median price.

### 2. Write Palantir's Starting Policy Before Peer Selection

In `lab08_palantir_pe_triangulation.md`, write the target, comparison date, valuation object, and initial peer policy before selecting peers.

Use this starting policy unless you find a sourced reason to revise it:

> A useful peer for Palantir should be a listed operating company that sells enterprise software or data/AI platforms with recurring or durable customer relationships, meaningful commercial or government enterprise exposure, and positive annual reported diluted EPS available before the `2026-09-10` comparison date. Differences to qualify include cloud/SaaS delivery model, customer mix, growth maturity, margin structure, government exposure, and whether the company is mainly infrastructure software, analytics software, cybersecurity, or application software. Exclude companies that are not operating companies, have materially different economics, lack positive annual reported diluted EPS, report incompatible share/currency bases that cannot be reconciled, or cannot be supported by opened primary/company sources.

Also write what evidence would make you reject a candidate.

### 3. Research At Most Two Candidate Peers

Suggest and investigate at most two listed operating-company candidates. For each candidate, use opened sources and record:

- Candidate name and ticker.
- Source supporting its business model, preferably Form 10-K Business section or annual report Business section.
- One important difference from Palantir.
- Latest annual reported diluted EPS public by `2026-09-10`.
- Fiscal period / fiscal year-end.
- Publication date of annual results or filing.
- Same-date stock price source for `2026-09-10` or the nearest defensible trading date used consistently for target and peers.
- Decision: `use`, `qualify`, or `exclude`.
- Your business reason and source locator.

Start from:

- SEC company search: https://www.sec.gov/edgar/search/
- Company investor relations annual results pages or annual report pages.
- Nasdaq historical data or quote pages for prices: https://www.nasdaq.com/market-activity/stocks

Potential candidates to investigate, only if they satisfy the policy through opened sources, may include enterprise software/data/AI/cybersecurity firms such as `SNOW`, `DDOG`, `CRWD`, `MDB`, `NOW`, `CRM`, `ORCL`, or `MSFT`. Do not use a company merely because it is familiar or shares a broad technology label. Use no more than two candidates in the final investigation table.

Important: If Palantir or a candidate has zero or negative annual reported diluted EPS, cite it and explain why P/E is not meaningful for that company. Do not force a positive P/E or switch valuation methods.

### 4. Adapt The Calculator

Copy `Lab 07/lab07_comps.py` to `Lab 08/lab08_palantir_comps.py` and adapt it for Palantir.

Requirements:

- Keep the code simple and close to the Lab 07 version.
- Change labels from Asbury to Palantir / Lab 08.
- Put Palantir in `TARGET` with the sourced same-date price and annual reported diluted EPS.
- Put only peers marked `use` or `qualify` in `PEERS`.
- Do not include excluded candidates in the calculator inputs.
- Keep non-positive EPS handling, since unusable P/E is an acceptable Lab 08 result.
- Run:

```powershell
python lab08_palantir_comps.py
```

Record the output in the markdown.

### 5. Validate

In the markdown:

- Hand-check one admitted peer's P/E as price divided by annual reported diluted EPS.
- Predict what removing one admitted peer should do.
- Run or read the leave-one-out output from the calculator and explain the change.
- If only one usable peer remains, explain that it produces a reference estimate and removing it leaves no estimate.
- If Palantir's own annual EPS or the peer set makes P/E unusable, explain the sourced limitation and what evidence would resolve it.

### 6. Compare With DCF

Include this table and fill it with your sourced results:

| Method | Palantir result and date | Main assumption or limitation |
|---|---|---|
| Week 3 / Lab 06 DCF | `$158.1618` per diluted share on `2026-09-10` | Forecast FCFF growth path, WACC, terminal growth, and terminal value dependence |
| Peer P/E | Range, reference estimate, or why unusable | Peer choices, business comparability, same-date prices, and annual reported diluted EPS basis |

Do not average the DCF and peer P/E results.

### 7. Skeptical AI Criticism Section

Add a section titled `AI Criticism Checked Against Sources`. Use this prompt against the completed draft, then judge the criticism yourself:

> Review my valuation comparison as a skeptical colleague. Identify the weakest supported assumption and any mismatch in company, date, valuation object or earnings definition. Do not invent a missing range or average the methods. Ask one question that could change my decision. I will check your criticism against my sources before revising my call.

In the markdown, record each criticism as `accept`, `reject`, or `unresolved`, with a short reason tied to the sources.

### 8. Final Reflection And Call

End with a direct conclusion:

- Explain why the chosen peers were admitted or qualified.
- Explain what the peer comparison adds to the DCF.
- Explain why the peer result and DCF differ or cannot be compared cleanly.
- State one of: `initiate`, `watch-defer`, or `do not initiate`.
- State the defensible range or explain why you withhold one.
- State what evidence would change the decision.

The default prior call is `watch-defer`; change it only if the new peer evidence supports the change.

## Quality Bar

Before finishing, check the Lab 08 rubric:

- Problem/decision: company, valuation date, and peer policy explicit before selection.
- Data/evidence: two candidate decisions supported by opened sources; price and earnings bases traced.
- Validation: hand arithmetic and changed-peer result checked, or unusable P/E diagnosed from sources.
- Financial judgment: DCF comparison, defensible range or justified withholding, and conditional action.
- Explanation/transfer: own causal explanation and source-checked judgment of AI criticism.

## GitHub Push

After the markdown and Python file are complete and checked:

1. Run the calculator and save the relevant output in the markdown.
2. Run `git status` from the FIN439 root.
3. Stage only the Lab 08 files you created or edited.
4. Commit with a message like:

```powershell
git commit -m "Add Lab 08 valuation triangulation"
```

5. Push to GitHub:

```powershell
git push
```

6. In the final response, provide the GitHub links or, if remote link construction is not possible, list the committed file paths and commit hash so the links can be opened from the repository.
