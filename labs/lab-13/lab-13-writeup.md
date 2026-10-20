# Lab 13 — Portfolio Mandate Defense

Pierce Appleton | October 20, 2026

AI-assisted implementation and analysis. Responses below for the instruction's independent exercises are proposed answers to review and rewrite independently; they do not document an AI-closed exercise, quiz response, or partner exchange.

## D — Question and conclusion

Which portfolios does Meridian Foundation's mandate permit, and what must the CIO answer before anyone optimizes?

A passes every checkable rule; B fails three; C fails one. Passing those checks is necessary but does not establish suitability: expected real returns, turnover, and the undefined loss promise still need attention.

## R — Statement types and IPS mapping

An investment policy statement (IPS) records a client's objectives, constraints, governance, and evaluation rules. It guides portfolio construction and gives the committee a standard for monitoring it. A target describes what success means; a constraint limits which choices are allowed.

| Statement | Primary type | Reason and policy implication |
|---|---|---|
| S1: seven-year horizon; annual rebalancing | Hard constraint / operating policy | Specifies investment horizon and rebalance schedule; static weights alone cannot show compliance over time. |
| S2: CPI + 4%, net of costs, rolling five years | Objective | A performance target, not a guaranteed outcome; requires CPI, costs and realized multi-year returns to evaluate. |
| S3: $0.75M quarterly; 12 months in cash or daily-liquid government securities | Hard constraint | Four payouts require $3M, or 3% of the $100M portfolio, in eligible holdings. |
| S4: 60% global equity / 40% U.S. IG bonds | Preference / evaluation benchmark | Defines the reference for performance, not a command to hold those exact weights; exact replication would violate S3. |
| S5: long-only, no borrowing, shorts or derivatives | Hard constraint | Nonnegative weights totaling 100% check a fully invested portfolio using the permitted holdings; the holdings list contains no derivatives. |
| S6: no single issuer above 8% | Hard constraint | Aggregate each company's securities; cash, Treasuries and diversified funds are exempt under the case's explicit rule. |
| S7: turnover at most 25% without committee approval | Hard constraint with approval exception | Requires starting holdings, trades and a turnover convention; cannot be tested from one target allocation. |
| S8: at least 90% redeemable within five business days | Hard constraint | Sum the holdings whose redemption period is at most five days. |
| S9: no calendar-year loss greater than 10% | Unverifiable promise as written | No risk measure, measurement basis or breach response is defined; print “requires CIO clarification,” never a pass. |
| S10: no stated preferences or pilot optimization goal | Missing | No extra sector, ESG, tax or home-bias constraint is authorized; the optimization criterion remains unspecified. |

S4 is the most ambiguous classification: a benchmark can appear alongside objectives in an IPS, but it does not impose exact weights. S9 sounds like a hard limit, yet treating a future realized loss as guaranteed would create false certainty.

## I / V — Checker and verification

Run from the repository root:

```text
python labs/lab-13/mandate.py
python labs/lab-14/verify_labs.py
```

All weights are percentages. Reserve minimum = 4 × $0.75M / $100M × 100 = **3.0%**. Issuer aggregation adds Acme's stock and bonds before comparing with 8%.

| Measurement | A | B | C | D | E (Lab 14) |
|---|---:|---:|---:|---:|---:|
| Sum of weights | 100.0 pass | 100.0 pass | 100.0 pass | 100.0 pass | 100.0 pass |
| Lowest weight | 0.0 pass | 0.0 pass | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve eligible ≥ 3% | 14.0 pass | 1.0 FAIL | 2.0 FAIL | 100.0 pass | 0.0 FAIL |
| Liquid within five days ≥ 90% | 100.0 pass | 85.0 FAIL | 100.0 pass | 100.0 pass | 100.0 pass |
| Largest company ≤ 8% | 0.0 pass | 9.0 FAIL | 8.0 pass | 0.0 pass | 0.0 pass |
| Failed checkable rules | 0 | 3 | 1 | 0 | 1 |

For all candidates, calendar-year loss **requires CIO clarification**. “Passes every checkable rule” refers to these five checks, not every IPS statement.

The mutation probe copies A, sets cash to −2% and equity to 64%, and reruns the checker: sum 100%, lowest −2%, reserve 10%, liquidity 100%, largest company 0%. Only long-only fails. The saved A inputs remain restored.

## E — Attack and proposed judgment

D is **100% Treasury bills**, using only allowed holdings. It passes all five checks because it is fully invested, long-only, wholly liquid, reserve eligible, and exempt from the company limit.

Proposed two-sentence judgment: The objection holds because a feasible allocation can still fail the client's return objective. S2 decides the objection: Lab 14's course-authored bill return is 3.5%, below the 6.5% nominal proxy for CPI + 4%, even before costs.

S4 also makes D a poor benchmark match, but tracking error is not an explicit rejection rule. A skeptical colleague should cite S2, and ask why the checker never claims to verify that objective.

## Proposed CIO question

What should the pilot optimize: the lowest volatility that meets the return target, or the highest expected return within an agreed risk budget?

An answer choosing minimum volatility would favor the least risky feasible mix that just meets the target. Choosing maximum return within a risk budget would generally permit more equity exposure; that is a different portfolio design, not a cosmetic change to the same optimization. S9 still needs a separate operational definition before either design can be approved.

Quiz prompt to answer before requesting an explanation: **Why must the checker add Acme's 5% bonds and 4% stock before applying the 8% limit to candidate B?** No student answer is recorded yet.

## Reflection draft

A portfolio can pass the checker and still be wrong because the checker only sees static feasibility. It cannot establish net rolling-five-year performance, annual turnover, future loss, or the CIO's preferred risk-return tradeoff. S9 was the least clear type: a statement phrased as an absolute limit cannot be honestly implemented without defining the metric and breach action.

## Project 2 — Proposed fictional client mandate

This is an editable practice mandate, not a claim about my personal finances or an actual client.

- Client: a fictional $100M education foundation reserve; seven-year horizon; annual rebalancing.
- Objective: CPI + 4% annualized net of costs over rolling five-year periods. Use CPI 2.5% only as a labeled modeling estimate, giving a 6.5% expected nominal target before an explicit cost allowance.
- Constraints: long-only, fully invested, no borrowing or derivatives; at least 3% in Treasury-bill or daily-liquid government holdings; at least 90% redeemable within five business days; 8% aggregate company issuer cap with Meridian's exemptions; turnover ≤25% annually absent approval.
- Proposed optimization: minimize volatility subject to the agreed expected return and constraints. No guaranteed 10% loss ceiling is asserted.
- Client question: which probabilistic loss measure and breach response should govern the pilot? A tight loss-probability limit could force more reserves or reveal that the target is infeasible.

## Checkout

- [mandate.py](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-13/mandate.py)
- [This writeup](https://github.com/pierceappleton/FIN439-Labs/blob/main/labs/lab-13/lab-13-writeup.md)
