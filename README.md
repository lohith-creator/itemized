# Itemized — Where Your Tax Dollars Go

A Streamlit app that turns a salary into an itemized "receipt" showing
exactly where federal and state tax dollars are spent, using real
government data (not made-up percentages).

## Run it

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## How it works

1. You enter a salary, filing status, and pick a state from the dropdown.
2. `calculations.py` estimates your federal tax bill using real 2026 IRS
   marginal brackets, and your state tax bill using that state's actual
   income tax structure (flat, graduated, or none).
3. Each tax bill is split into spending categories using real government
   data: federal spending by function (CBPP/CBO), and state spending by
   function (NASBO's 2024 State Expenditure Report — genuine per-state
   percentages, not a national average applied to everyone).

## Data sources (all in `data/`)

- `federal_spending_fy2024.json` — federal budget by category, FY2024
- `federal_tax_brackets_2026.json` — IRS brackets + standard deduction, 2026
- `state_income_tax_all50.json` — all 50 states' income tax structure
- `state_spending_by_state.json` — real per-state spending mix, NASBO FY2024

## Extending it

- `calculations.py` has no Streamlit dependency, so it's independently
  testable — run it directly or write unit tests against it.
- Married-filing-jointly state brackets aren't included yet (single-filer
  brackets are used for all state calculations); federal already supports
  both filing statuses.
- The federal "all other" spending category is a lumped bucket — CBPP's
  underlying data breaks it into education, transportation, science,
  law enforcement, and international if you want finer categories later.
- Consider caching the JSON loads with `@st.cache_data` if load time
  becomes noticeable — not needed yet given how small these files are.

## Not tax advice

This gives a good-faith estimate for illustration. It doesn't account for
credits, itemized deductions, pre-tax retirement contributions, FICA, or
local taxes.
