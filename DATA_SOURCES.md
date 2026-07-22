# Data sources

Every number in this project traces back to a real, public source. No estimates were invented to fill gaps — where a gap existed (e.g. per-state spending mix), it was flagged and either sourced properly or left out.

## Federal spending by category

**Source:** Center on Budget and Policy Priorities (CBPP), using Congressional Budget Office (CBO) account-level expenditure data
**Link:** https://www.cbpp.org/research/federal-budget/where-do-our-federal-tax-dollars-go
**Fiscal year:** 2024
**What it provides:** Federal spending broken into functional categories (health insurance, Social Security, defense, interest on debt, veterans benefits, economic security programs) as a percentage of the $6.9 trillion federal budget.

## Federal income tax brackets

**Source:** IRS Revenue Procedure 2025-32, as summarized by Tax Foundation
**Link:** https://taxfoundation.org/data/all/federal/2026-tax-brackets/
**Tax year:** 2026
**What it provides:** Marginal tax brackets and standard deduction amounts for single and married-filing-jointly filers.

## State income tax rates (all 50 states + DC)

**Source:** Tax Foundation, State Individual Income Tax Rates and Brackets
**Link:** https://taxfoundation.org/data/all/state/state-income-tax-rates-2026/
**As of:** February 2026
**What it provides:** Each state's tax structure (flat, graduated, or none) and full bracket schedule for single filers.

## State spending by category (all 50 states)

**Source:** NASBO (National Association of State Budget Officers), 2024 State Expenditure Report, Table 5
**Link:** https://higherlogicdownload.s3.amazonaws.com/NASBO/9d2d2db1-c943-4f1b-b750-0fca152d64c2/UploadedImages/SER%20Archive/2024_SER/2024_State_Expenditure_Report_S.pdf
**Fiscal year:** 2024
**What it provides:** Real, state-by-state spending percentages across K-12 education, higher education, public assistance, Medicaid, corrections, transportation, and all other categories — sourced from all fund types (general, federal, other state funds, bonds) combined. This is the piece that makes the state comparison meaningful: each state's spending mix is genuinely its own, not a national average applied uniformly.

## A note on rigor

An earlier draft of this project used a national average spending mix for every state, which would have made the state comparison feature misleading — different tax bills, identical spending pie. That gap was caught, flagged explicitly, and fixed by extracting NASBO's actual per-state table rather than shipping an approximation.
