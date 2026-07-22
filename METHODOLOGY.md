# Methodology notes

## Why the data years don't all match (FY2024 vs. 2026)

This project mixes two different kinds of government data, and they update
on different schedules — that's expected, not an oversight.

**Tax brackets — current year (2026)**

Federal and state income tax brackets are pulled for 2026, the current tax
year. This is deliberate: the calculator answers "what would I owe on this
salary today," so it needs to use the rates actually in effect right now.
The IRS and most states adjust brackets annually for inflation, so using
last year's brackets would give a slightly wrong answer for someone
checking their real 2026 paycheck math.

**Spending breakdowns — most recent completed fiscal year (FY2024)**

Federal spending by category (CBPP/CBO) and state spending by category
(NASBO) are both FY2024, the most recent year with finalized actual
spending. Government spending reports lag — FY2025 and FY2026 numbers
either aren't fully closed out yet or aren't available in the same
structured, category-level format. Using FY2024 actuals is more accurate
than using a FY2025/2026 projection or estimate.

**The result:** this app tells you "based on what you'd owe in taxes this
year, here's how that kind of money was actually spent last year" — which
is a reasonable and honest way to frame it, but worth being explicit about
rather than letting someone assume everything is from the same year.

## A note on the state spending comparison

An earlier version of this project used the *national average* spending
mix for every state (e.g. "Medicaid is 29.8% of spending" applied
identically to Illinois, Texas, and California). That would have made the
state comparison feature misleading, since two states could show identical
spending pies despite genuinely different budget priorities.

This was caught and fixed by extracting NASBO's actual per-state table
(Table 5 of the 2024 State Expenditure Report) instead, so each state's
spending percentages are genuinely its own.

## What this app is and isn't

- It **is** a good-faith estimate using real, sourced government data.
- It **is not** tax advice, and doesn't account for credits, itemized
  deductions, pre-tax retirement contributions, FICA/payroll tax, or local
  (city/county) taxes.
- "No state income tax" (e.g. Texas, Florida, Washington) does not mean a
  state collects no revenue from residents — those states typically rely
  more heavily on sales tax, property tax, or business taxes instead. See
  `DATA_SOURCES.md` for the full source list.