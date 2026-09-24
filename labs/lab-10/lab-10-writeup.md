# Lab 10: Pro-Forma, Palantir Through the Engine

Pierce Appleton  
Partner: Ethan Heeres, ethane@purdue.edu  
AI partner: Claude Code (resumed from the Lab 09 ABG model)  
Date: September 24, 2026

## D: The question

> What are five years of your company's statements worth, built from assumptions you can defend?

Company: **Palantir Technologies Inc. (`PLTR`)**, the same company as Labs 03, 04, 06 and 08.

**The line that makes Palantir different:** customers pay Palantir before the work is done. Deferred revenue plus customer deposits ("contract liabilities") were $812M at the end of 2025. That money funds Palantir's receivables the same way floor plan funded ABG's inventory. In my model it replaces the floor plan row. It grows at 18.15% of revenue and adds about $0.67 to $0.71B of cash each year. The second difference is stock-based compensation. It was 15% of 2025 revenue, and the cash flow statement adds it back, so the valuation has to take it out again.

## R: History, three years

All figures are USD millions from Palantir's consolidated statements. Each 10-K reports the balance sheet for the current and prior year, and the income statement for three years. I took each year from the 10-K for that year.

| Line | FY2023 | FY2024 | FY2025 | Source |
|---|---:|---:|---:|---|
| Revenue | 2,225.0 | 2,865.5 | 4,475.4 | Consolidated Statements of Operations, 10-K for each year |
| Gross profit | 1,793.9 | 2,299.5 | 3,686.3 | Statements of Operations |
| SG&A (sales & marketing + G&A) | 1,269.3 | 1,481.2 | 1,714.6 | Statements of Operations: 745.0 + 524.3; 887.8 + 593.5; 1,056.9 + 657.7 |
| R&D (not in the ABG grid; Palantir-specific) | 404.6 | 507.9 | 557.7 | Statements of Operations |
| Net income attributable to common | 209.8 | 462.2 | 1,625.0 | Statements of Operations |
| Inventory | none | none | none | Balance sheets carry no inventory line (software company). Receivables used instead: 364.8, 575.0, 1,042.1 |
| PP&E, net | 47.8 | 39.6 | 52.0 | Consolidated Balance Sheets |
| Shareholders' equity (Palantir's) | 3,475.6 | 5,003.3 | 7,387.3 | Consolidated Balance Sheets; total equity incl. NCI 3,561.0 / 5,094.4 / 7,488.0 |
| Contract liabilities (the named line) | 486.3 | 566.4 | 812.3 | Balance sheets: deferred revenue + customer deposits, current and noncurrent; ties to the revenue note |
| Stock-based compensation | 475.9 | 691.6 | 684.0 | Consolidated Statements of Cash Flows |

Filings:

- FY2025 10-K, accession 0001321655-26-000011, filed 2026-02-17: https://www.sec.gov/Archives/edgar/data/1321655/000132165526000011/pltr-20251231.htm
- FY2024 10-K, accession 0001321655-25-000022, filed 2025-02-18: https://www.sec.gov/Archives/edgar/data/1321655/000132165525000022/pltr-20241231.htm
- FY2023 10-K, accession 0001321655-24-000022, filed 2024-02-20: https://www.sec.gov/Archives/edgar/data/1321655/000132165524000022/pltr-20231231.htm

**Two numbers confirmed by hand** in the filing itself, not from a data feed:

- [ ] FY2025 revenue $4,475,446 thousand. FY2025 10-K, Consolidated Statements of Operations, p. 86.
- [ ] FY2023 PP&E, net $47,758 thousand. FY2024 10-K, Consolidated Balance Sheets, prior-year column. It also appears in the FY2023 10-K as the current-year figure.

**Unresolved:** the cash flow statement's "Depreciation and amortization" (26.1 / 31.6 / 33.4) includes amortization of acquired intangibles. The PP&E note says depreciation of property and equipment was "not material" and does not give the split. My depreciation ratio uses the total, so it slightly overstates PP&E depreciation. That makes almost no difference at this size.

### Ratios

| Ratio | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Gross margin | 80.6% | 80.2% | 82.4% |
| SG&A ÷ gross profit | 70.8% | 64.4% | 46.5% |
| R&D ÷ revenue | 18.2% | 17.7% | 12.5% |
| Inventory days | n/a | n/a | n/a |
| Receivable days (replaces inventory days) | 59.8 | 73.2 | 85.0 |
| Depreciation ÷ opening PP&E | 48.2% | 66.1% | 66.0% |
| Capex, from the filing | 15.1 | 12.6 | 33.9 |
| Capex, data provider field (Yahoo Finance `annualCapitalExpenditure`) | 15.11 | 12.63 | 33.88 |
| Tax rate (provision ÷ pretax) | 8.3% | 4.3% | 1.4% |
| Contract liabilities ÷ revenue | 21.9% | 19.8% | 18.1% |
| SBC ÷ revenue | 21.4% | 24.1% | 15.3% |
| **Reported revenue growth** | 16.7% | 28.8% | 56.2% |
| **Growth from existing customers** (MD&A, Palantir's closest thing to same-store) | 11.0% | 21.2% | 41.8% |
| U.S. commercial revenue growth (MD&A) | 36.4%* | 54% | 109% |

\*The FY2023 10-K gives U.S. commercial revenue of $457.1M vs. $335.1M. The growth rate is my calculation.

The existing-customer figures come from the MD&A revenue paragraph in each 10-K. That paragraph gives the dollar increase from customers that existed at the prior year-end: government $129.4M + commercial $79.6M in 2023, $280.7M + $190.7M in 2024, and $774.0M + $425.2M in 2025. I divided each total by prior-year revenue. The provider's capex matches the filing to the dollar. That makes sense because Yahoo pulls this field straight from the XBRL tag.

### Assumption set

| Assumption | Value | Label | Reason |
|---|---|---|---|
| Revenue growth 2026 | 82.2% | guidance | This equals the $8.154B midpoint of the $8.150–8.158B full-year guide in the Q2 2026 release (Aug 3, 2026). |
| Revenue growth 2027–2030 | 45% / 32% / 25% / 20% | judgment | Total remaining deal value doubled to $11.2B, so demand is there. But each point of growth takes more dollars as revenue gets bigger. I cut growth about a third each year. |
| Gross margin | 82.0% | judgment | 2025 reached 82.4% after two years near 80.5%. I held it just under 2025 because AIP runs more compute for customers, and hosting sits in cost of revenue. |
| SG&A ÷ gross profit | 38% / 35% / 33% / 32% / 31% | judgment | This ratio fell from 71% to 46% in two years. Most 2025 growth came from customers Palantir already had, and selling to existing customers costs less than winning new ones. |
| R&D ÷ revenue | 11.0% | judgment | It fell from 18% to 12.5%. The four platforms already exist, so R&D rises in dollars but keeps shrinking as a share. |
| SBC ÷ revenue (memo; already inside the expense lines) | 10% / 9.5% / 9% / 8.5% / 8% | judgment | SBC dollars were flat in 2025 while revenue grew 56%. I assume the dollars keep rising, but slower than revenue. |
| Depreciation ÷ opening PP&E | 66.0% | history | 2025 D&A ÷ 2024 PP&E, consistent with the three-year asset lives in the policy note. |
| Capex ÷ revenue | 0.70% | history | The three-year average is 0.63%, and 2025 was 0.76%. |
| Tax rate | 5% / 10% / 18% / 21% / 21% | judgment | Palantir paid 1.4% in 2025 because it holds $2.6B of tax-effected NOLs behind a full valuation allowance. At over $3B of pretax income a year, those run out around 2028, and the rate moves to the 21% federal rate. |
| Receivable days | 80 | judgment | Days rose from 60 to 85, mostly from big contracts billed near year-end. I assume slightly better collections, not a full reversal. |
| **Contract liabilities ÷ revenue (the named line, replaces floor plan)** | 18.15% | history | 2025 year-end ratio. It has drifted down from 21.9%, so holding it flat is the one risk I'd flag. |
| Other working capital ÷ Δrevenue | 0.0% | judgment | None. Other assets ($629M) and other liabilities ($600M) nearly cancel, so I don't grow them. |
| Interest yield on cash and securities | 3.5% | judgment | 2025 earned 4.38% on the opening balance. Short-term rates are lower in 2026. |
| Buyback | $100M a year | judgment | Actuals were $0, $64M and $75M. The $1B program from August 2023 is mostly unused. |
| Cash floor | $1,500M | judgment | This is about the 2025 year-end cash before securities, roughly two months of 2026 operating costs. |
| Revolver limit | $500M | history | The 2025 10-K reports a $500M facility, undrawn, maturing March 2027. I assume it gets renewed. |
| Revolver rate | 6.0% | judgment | Safety net only, never drawn in the base case. |
| Cost of equity | 11.0% | judgment | Same as my Lab 06 DCF. The stock's beta is high. |
| Terminal growth | 3.0% | judgment | Long-run nominal economy, same as Lab 06. It must stay below the cost of equity, and the code refuses otherwise. |
| Shares | 2,565.197M | fact | Diluted weighted-average shares from the FY2025 10-K, the same count I used in Labs 03, 06 and 08. |

**Negative FCFE?** No. Palantir's FCFE is positive in every projected year, so the negative-FCFE branch never runs. The code still guards it: a negative year is not valued, and a negative terminal cash flow raises an error. A perpetuity of an outflow has no value.

## I: Palantir through the engine

File: [pltr_proforma.py](pltr_proforma.py). This is the Lab 09 ABG engine with Palantir's opening balance sheet (Dec 31, 2025) and the assumptions above. Changes from ABG:

| ABG line | Palantir line | Why |
|---|---|---|
| Inventory (days of COGS) | Receivables (days of revenue) | No inventory; receivables are the working-capital asset |
| Floor plan (% of inventory) | Contract liabilities (% of revenue) | Customer prepayments finance working capital |
| Term debt + repayment | Debt = 0 | No debt outstanding at Dec 31, 2025 |
| Impairment | none | No recurring impairment in the three years |
| Cash | Cash + marketable securities ($1,423.8 + $5,753.2) | Palantir manages the two as one liquidity pool, and it earns interest income |
| none | SBC added back in the cash flow, credited to equity | This follows the 10-K cash flow statement. An equity roll-forward check was added. |

Opening balance sheet ($M): cash and securities 7,177.0 + receivables 1,042.1 + PP&E 52.0 + other assets 629.3 = **8,900.4 total assets**. On the other side, contract liabilities 812.3 + other liabilities 600.1 + debt 0 + total equity 7,488.0 = **8,900.4**. This ties to the 10-K total.

Run: `python pltr_proforma.py`

| $M | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---:|---:|---:|---:|---:|
| Revenue | 8,154.3 | 11,823.7 | 15,607.3 | 19,509.1 | 23,410.9 |
| Operating income | 3,214.4 | 4,952.1 | 6,786.5 | 8,635.9 | 10,547.8 |
| Net income | 3,292.3 | 4,806.1 | 6,045.4 | 7,483.5 | 9,238.8 |
| Increase in contract liabilities | 667.7 | 666.0 | 686.7 | 708.2 | 708.2 |
| FCFE | 4,007.4 | 5,757.6 | 7,269.6 | 8,954.5 | 10,923.6 |
| Valuation FCFE (less after-tax interest income and SBC) | 2,953.4 | 4,285.2 | 5,384.4 | 6,635.1 | 8,144.7 |
| Ending cash and securities | 11,084.5 | 16,742.0 | 23,911.6 | 32,766.2 | 43,589.8 |
| Assets − liabilities − equity | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

**How the valuation handles the two Palantir-specific issues.** First, interest income: I take after-tax interest income out of FCFE and add the opening $7,177M of cash and securities once at the end. Leaving it in would count the cash pile twice. Second, SBC: I subtract it from FCFE. Paying employees in shares costs owners through dilution just as paying them in cash would. I also subtract the $100.7M noncontrolling interest.

**Refusal test.** On a temporary copy, I cut the contract liability increase out of FCFE and left the balance sheet alone. The model refused:

```text
ValueError: FY2026E Balance check failed with gap -667.680186
```

The gap is −667.7, exactly the 2026 increase in contract liabilities. The balance sheet carries the liability, but the cash it brought in never reached the cash line. The real file was not changed.

## V: Check block and price

```text
FY2026E Balance: OK, gap 0.0      FY2026E Cash floor: OK, gap 9,584.5
FY2027E Balance: OK, gap 0.0      FY2027E Cash floor: OK, gap 15,242.0
FY2028E Balance: OK, gap 0.0      FY2028E Cash floor: OK, gap 22,411.6
FY2029E Balance: OK, gap 0.0      FY2029E Cash floor: OK, gap 31,266.2
FY2030E Balance: OK, gap 0.0      FY2030E Cash floor: OK, gap 42,089.8
```

Cash tie, PP&E roll-forward, debt roll-forward and equity roll-forward also print `OK, gap 0.0` in every year (full block in the program output). Cash never approaches the $1.5B floor, so **the revolver is never drawn**. Palantir generates more cash than it spends in every year.

Valuation output:

```text
PV of 2026-2030 valuation FCFE: 19,279.9
PV of terminal value: 62,231.3
+ Opening cash and securities: 7,177.0
- Noncontrolling interest: 100.7
Equity value: 88,587.5
Share of value after 2030: 70.2%
Value per share: $34.53
```

**Price:** $192.59, the PLTR regular-session close on 2026-09-24 (Yahoo Finance chart data).

**The model says $34.53 per share. The market says $192.59, on the same 2,565.197M diluted shares.** That is $88.6B of equity against about $494B of market value. What does the market expect after 2030 that my 3% terminal growth leaves out, given that revenue is still growing 20% in the fifth year?

For scale: holding everything else fixed, growth of 60/45/35/30% in 2027–2030 moves the value to $46.15, and 5% terminal growth moves it to $43.25. Neither closes the gap. I will take these assumptions apart one at a time in Part 2.

Learning demonstration, not investment advice.

## E: Fresh eyes (partner review)

*To be completed in class with Ethan. Record his exact attack and my two-sentence answer here.*

**Ethan's attack on my table:** "Why ________, and what would change it?"

**My answer (two sentences):**

> _[answer here]_

**My attack on Ethan's table:** _[his company, the judgment label I attacked, and my exact question]_

**His answer:** _[record it]_

## Organic growth: learned on my own

1. **What it is.** Organic growth is revenue growth from the business a company already had, with acquisitions stripped out. For a dealer that means same-store sales. For Palantir it means growth from customers it already had.
2. **How Palantir discloses it.** Palantir doesn't use the words "organic" or "same-store." Each 10-K's MD&A splits the revenue increase by segment and states how much came from customers that existed at the prior year-end ($1,199.2M of the $1,610M increase in 2025). None of the three MD&A revenue paragraphs credits any growth to an acquisition, so reported growth is effectively organic. The existing-customer split separates expansion within current accounts from new-customer wins.
3. **Why the video carries 1.8% for ABG when reported growth was 4.7%.** ABG's reported growth included revenue from dealerships it bought, mainly the Herb Chambers acquisition. Bought revenue happens once, and you pay for it separately. It does not keep compounding from the stores ABG already owned. Same-store growth was 1.2%, so 1.8% is a judgment built on the organic number, not the acquisition-boosted one.

## Reflect (for my partner conversation)

1. **The label I'd defend longest:** contract liabilities at 18.15% of revenue. It comes straight from the 2025 balance sheet, it is how Palantir's billing works, and removing it cuts 2026 FCFE from $4.0B to $2.5B. That shows the line matters.
2. **The number that surprised me:** the 1.4% tax rate on $1.66B of pretax income in 2025. Palantir still carries $2.6B of tax-effected NOLs from its loss years, and that shield is why near-term earnings run far above what a 21% rate would leave.

## Files

- [pltr_proforma.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-10/pltr_proforma.py)
- [lab-10-writeup.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-10/lab-10-writeup.md)
