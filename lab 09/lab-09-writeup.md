# Lab 09: Pro-Forma Build, ABG (Asbury Automotive Group)

Pierce Appleton  
Partner: Ethan Heeres, ethane@purdue.edu  
AI partner: Codex CLI  
Date: September 24, 2026

## The question

What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?

## What I built

- `proforma.py` builds the income statement first, then the balance sheet.
- It calculates free cash flow to equity (FCFE), then computes cash last with a revolver if cash would fall below the minimum.
- It prints the full cash flow build from net income to ending cash.
- It checks five things each year: balance sheet balance, cash tie, PP&E roll-forward, debt roll-forward, and the cash floor.
- Valuation refuses to run unless all five checks pass for every projected year.
- It guards terminal growth so the growth rate cannot equal or exceed the cost of equity.
- It values equity from five years of FCFE plus a terminal value.

## Assumptions

| Name | Value | Label | Reason |
|---|---:|---|---|
| organic_growth | 1.8% | judgment | Same-store revenue grew 1.2%; acquisitions excluded. |
| gross_margin | 17.05% | judgment | 2025 margin held flat; the shortage-era premium is gone. |
| sga_gp | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | judgment | The Herb Chambers integration raises costs in 2026, then partial recovery toward the 2024 level. |
| depreciation_ratio | 2.68% of opening PP&E | history | 2025 depreciation divided by opening PP&E. |
| impairment | $120M | judgment | Below the 3-year average of 136; recurring and non-cash. |
| capex | $250M | guidance | Management's 2026 figure. Holding it 5 years is judgment. 1H 2026 ran about $339M annualized. |
| tax_rate | 25.5% | judgment | Between the 3-year average of 25.2% and the 2025 rate of 25.7%. |
| inventory_days | 52.2 | history | 2025 inventory days. |
| floor_plan_inventory_ratio | about 95% | history | 2025 floor plan debt divided by inventory. |
| other_working_capital_ratio | 0.8% of revenue change | judgment | Other working capital moves with revenue. |
| MIN_CASH | $25M | judgment | Small cash floor. |
| REVOLVER_LIMIT | $850M | judgment | Safety net, unused in the base case. |
| revolver_rate | 6.0% | judgment | Safety net, unused in the base case. |
| debt_repayment | $150M | judgment | Steady annual paydown assumption. |
| buyback | $150M | judgment | Actuals were 260, 185, 100. |
| floor_plan_rate | 4.67% | history | 2025 interest divided by opening floor plan balance. |
| term_debt_rate | 5.44% | history | 2025 interest divided by opening term debt balance. |
| cost_of_equity | 10.0% | judgment | Starting convention; measured beta comes later. |
| terminal_growth | 2.5% | judgment | Must stay below cost of equity. |
| shares_outstanding | 17.951349M | fact | June 2026 10-Q, 40.1M issued less 22.15M treasury. |

## Known-answer match

| Line | FY2026E target | FY2026E mine | FY2030E target | FY2030E mine | Match |
|---|---:|---:|---:|---:|---|
| Revenue | 18,323.0 | 18,323.0 | 19,678.3 | 19,678.3 | Yes |
| Operating income | 844.2 | 844.2 | 971.4 | 971.4 | Yes |
| Net income | 413.6 | 413.6 | 527.5 | 527.5 | Yes |
| FCFE | 211.4 | 211.4 | 342.3 | 342.3 | Yes |
| Cash year end | 101.8 | 101.8 | 719.8 | 719.8 | Yes |
| Assets minus liabilities minus equity | 0.0 | 0.0 | 0.0 | 0.0 | Yes |

Value per share: target $291.75 vs mine $291.75.  
Share of value after 2030: target about 80% vs mine 79.8%.

Learning demonstration, not investment advice.

## Swap and break

Exact error line from the temporary copy:

```text
ValueError: FY2026E Balance check failed with gap -61.441437
```

It is -61.4 because forcing 2026 cash to 40.4 removes the 2026 increase in cash, so the balance sheet shows that year's cash change with the sign flipped.

## Floor plan

- It is inventory loans from manufacturers' finance arms and banks.
- It rises with inventory, charges interest on the opening balance, and is counted as operating inside FCFE.
- Removing it takes away the inventory financing source, which sends cash to about -1.1 billion.
- Exact error line from the temporary copy: `ValueError: FY2026E Cash floor check failed: ending cash -1112.04 is 1137.04 below the 25.0 floor`
- The balance sheet still balanced, gap 0.0, while cash went to about -$1.1 billion, which is why the cash check exists alongside the balance check. A model can tie and still be wrong.

## Reflection

(a) The model computes cash last because every other projected line creates or uses cash first.  
(b) The -61.4 tells me the balance sheet is off by exactly the missing 2026 cash increase before I open a single cell.

## Files

- [proforma.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/lab%2009/proforma.py)
- [lab-09-writeup.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/lab%2009/lab-09-writeup.md)
