# Lab 06 Instructions

Paste this into Codex in your VS Code terminal:

```text
You are working in my course/work folder in VS Code. Complete Lab 06 end to end, verify the output, and push the final result to GitHub.

Goal: produce a completed DCF assignment with sourced inputs, a working `dcf.py`, a markdown writeup, verified terminal output, and final changes committed and pushed.

Follow this workflow carefully:

1. Reopen and rerun

- Confirm you are in the correct Course/Work folder.
- Open a terminal.
- Run:

```bash
python dcf.py
```

- The existing training case should print Tuesday's twelve known numbers.
- If it does not, debug until the original twelve-line output matches the known answer before changing anything else.

2. Source five input rows

Use SEC EDGAR for my assigned company:

- Find the company.
- Open the latest 10-K.
- Use Ctrl+F/search for the relevant statement or note headings.
- Collect exactly these inputs:

| Input | Training value | Source expectation |
|---|---:|---|
| Starting FCFF | 100 | Cash flow statement: operating cash flow + after-tax interest - capex |
| Growth, Years 1-5 | 8%, 6%, 5%, 4%, 3% | Item 7 MD&A plus recent history; this is a forecast |
| WACC | 10% | Do not copy it; estimate it |
| Terminal growth | 3% | Long-run economy, not the company |
| Cash, debt, shares | 50, 300, 50 | Balance sheet; debt note; EPS note diluted weighted-average shares |

For every row, record:

- value
- unit
- as-of date
- locator/source
- whether it is sourced or unresolved

Also collect today's stock price with date and time. This is the reverse DCF target.

If a row cannot be sourced, leave it unresolved and keep the training value as a placeholder. Clearly mark it as a placeholder.

Use this WACC estimate unless better sourced logic is available:

- Equity cost: 4.5% + 1.3 x 5% = about 11%
- Debt cost: 6% x (1 - 0.25) = 4.5%
- Capital structure: 85/15
- WACC: about 10%

If FCFF is negative, do not simply grow the loss mechanically. Use an explicit five-year path.

3. Create the markdown writeup

Create a new markdown file, with any clear name ending in `.md`, for example:

```text
lab06_dcf.md
```

Include:

- the sourced input table
- today's stock price with date and time
- unresolved rows, if any
- your company's value per share
- reasonableness check
- grid and reverse DCF result
- conditional call
- one thing to monitor
- temperature check response

4. Update `dcf.py`

Paste code directly over `dcf.py`. Do not create a second script.

Preserve the original training inputs block and the twelve printed lines exactly as they are so the known answer still matches after the update.

Then add:

Sensitivity grid:

- editable WACC list at the top, starting with:

```python
WACC_VALUES = [0.09, 0.10, 0.11]
```

- editable terminal growth list at the top, starting with:

```python
TERMINAL_GROWTH_VALUES = [0.02, 0.03, 0.04]
```

- print value per diluted share for every combination
- hold every other input fixed
- mark any cell invalid if terminal growth >= WACC
- print the grid as a readable terminal table underneath the original twelve lines

Reverse DCF:

- editable target share price at the top, starting with:

```python
TARGET_SHARE_PRICE = 30.00
```

- solve for one number: a uniform shift added to all five explicit growth rates
- use bisection between editable lower and upper bounds at the top:

```python
REVERSE_SHIFT_LOWER = -0.05
REVERSE_SHIFT_UPPER = 0.10
```

- refuse any bracket that pushes an annual growth rate to -100% or below
- if the target cannot be reached inside the bounds, report no solution in that bracket
- never return a bound as if it were the answer
- print:
  - solved shift
  - target price
  - list of inputs held fixed

One command must show all three blocks:

```bash
python dcf.py
```

The three blocks are:

1. original twelve lines
2. sensitivity grid
3. reverse DCF

5. Verify training case first

Set inputs to the training case:

- Starting FCFF: 100
- Growth: 8%, 6%, 5%, 4%, 3%
- WACC: 10%
- Terminal growth: 3%
- Cash: 50
- Debt: 300
- Shares: 50
- Target price: 30.00

Run:

```bash
python dcf.py
```

Expected sensitivity grid for training case, dollars per share:

| WACC \ terminal growth | 2% | 3% | 4% |
|---|---:|---:|---:|
| 9% | 28.60 | 32.94 | 39.02 |
| 10% | 24.36 | 27.50 | 31.69 |
| 11% | 21.06 | 23.41 | 26.44 |

Expected reverse DCF:

- target: $30.00
- solved uniform growth shift: about +1.78 percentage points

If the grid or shift does not match closely, fix the model before moving on.

6. Run my company

Replace the input block with my company's inputs.

- If a row is unresolved, keep the training value and mark it as a placeholder in the markdown.
- Set target price equal to today's stock price.
- Run:

```bash
python dcf.py
```

Record:

- twelve printed lines
- sensitivity grid
- reverse DCF shift
- inputs held fixed

7. Reasonableness check

Compare my value per share to today's price.

- If value is within 0.5x to 2x of today's price, say so.
- If outside that range, do not adjust the model.
- Instead, name the input you distrust most and explain why.

8. Conditional call

Write a conditional call in this form:

```text
Initiate if ...; otherwise ...
Monitor: ...
```

Example style:

```text
Watch-defer. Initiate if the growth the price demands drops below my forecast path, such as a price below about $27.50, or if there is a sourced reason to raise my growth path two points. Monitor: operating margin next quarter.
```

Do not claim the reverse DCF proves mispricing. Report the growth shift with what was held fixed.

9. Temperature check

Add a short anonymous-style response:

- what works
- what confuses
- one change

10. Final verification

Run:

```bash
python dcf.py
```

Make sure:

- the training version matched before company inputs were entered
- current company output prints cleanly
- no traceback
- markdown is complete
- unresolved inputs are clearly labeled
- one command still prints all required model blocks

11. GitHub checkout

Use git to inspect, commit, and push.

Run:

```bash
git status
git diff
```

Commit only the relevant Lab 06 files. Do not revert unrelated user changes.

Then commit with a clear message, for example:

```bash
git add dcf.py lab06_dcf.md
git commit -m "Complete Lab 06 DCF analysis"
git push
```

If the push fails because the branch needs upstream configuration, set the upstream for the current branch and push.

Final response to me should include:

- files changed
- verification command run
- final value per share
- today's price used
- reverse DCF shift
- GitHub push status
```
