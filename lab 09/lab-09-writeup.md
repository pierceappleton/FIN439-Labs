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
- It checks that assets minus liabilities minus equity equals zero and that cash is above the floor.
- It values equity from five years of FCFE plus a terminal value.

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

## Swap and break

Exact error line from the temporary copy:

```text
ValueError: FY2026E balance sheet gap is -61.441437
```

It is -61.4 because forcing 2026 cash to 40.4 removes the 2026 increase in cash, so the balance sheet shows that year's cash change with the sign flipped.

## Floor plan

- It is inventory loans from manufacturers' finance arms and banks.
- It rises with inventory, charges interest on the opening balance, and is counted as operating inside FCFE.
- Removing it takes away the inventory financing source, which sends cash to about -1.1 billion.

## Reflection

(a) The model computes cash last because every other projected line creates or uses cash first.  
(b) The -61.4 tells me the balance sheet is off by exactly the missing 2026 cash increase before I open a single cell.

## Files

- [proforma.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/lab%2009/proforma.py)
- [lab-09-writeup.md](https://github.com/pierceappleton/FIN439-Labs/blob/main/lab%2009/lab-09-writeup.md)