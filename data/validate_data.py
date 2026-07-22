"""
Validates the integrity of every dataset in this project.
Run this after touching any JSON file in data/ to catch mistakes early.

Usage:
    python3 data/validate_data.py
"""
import json
import sys
from pathlib import Path

DATA_DIR = Path(__file__).parent
errors = []
checks_run = 0


def load(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def check(condition, message):
    global checks_run
    checks_run += 1
    if not condition:
        errors.append(message)


def validate_federal_spending():
    data = load("federal_spending_fy2024.json")
    total = sum(c["percent"] for c in data["categories"])
    check(abs(total - 100) < 0.5, f"Federal spending categories sum to {total}%, expected ~100%")
    for c in data["categories"]:
        check("label" in c and "percent" in c, f"Federal category missing fields: {c}")
        check(0 <= c["percent"] <= 100, f"Federal category '{c['label']}' has invalid percent: {c['percent']}")


def validate_federal_brackets():
    data = load("federal_tax_brackets_2026.json")
    for status in ["single", "married_filing_jointly"]:
        brackets = data["brackets"][status]
        check(brackets[-1]["up_to"] is None, f"{status}: last bracket should have no upper bound")
        rates = [b["rate"] for b in brackets]
        check(rates == sorted(rates), f"{status}: bracket rates are not ascending: {rates}")
        thresholds = [b["up_to"] for b in brackets[:-1]]
        check(thresholds == sorted(thresholds), f"{status}: bracket thresholds are not ascending")
    check(data["standard_deduction"]["married_filing_jointly"] == 2 * data["standard_deduction"]["single"],
          "MFJ standard deduction is not exactly 2x single (may be intentional - verify against source)")


def validate_state_income_tax():
    data = load("state_income_tax_all50.json")
    states = data["states"]
    check(len(states) == 51, f"Expected 51 entries (50 states + DC), found {len(states)}")

    no_tax_states = [c for c, s in states.items() if s["structure"] == "none"]
    check(len(no_tax_states) == 8, f"Expected 8 no-income-tax states, found {len(no_tax_states)}: {no_tax_states}")

    for code, state in states.items():
        if state["structure"] == "graduated":
            brackets = state["brackets"]
            rates = [b["rate"] for b in brackets]
            check(rates == sorted(rates), f"{code}: graduated bracket rates not ascending: {rates}")
            overs = [b["over"] for b in brackets]
            check(overs == sorted(overs), f"{code}: graduated bracket thresholds not ascending")
        elif state["structure"] == "flat":
            check(0 <= state["rate"] <= 0.15, f"{code}: flat rate looks out of range: {state['rate']}")


def validate_state_spending():
    data = load("state_spending_by_state.json")
    states = data["states"]
    order = data["category_order"]

    check(len(states) == 51, f"Expected 51 entries (50 states + average), found {len(states)}")

    for code, s in states.items():
        total = sum(s[k] for k in order)
        check(abs(total - 100) < 0.5, f"{code}: spending categories sum to {total}%, expected ~100%")
        for k in order:
            check(0 <= s[k] <= 100, f"{code}: category '{k}' has invalid percent: {s[k]}")


def validate_cross_references():
    income_tax_codes = set(load("state_income_tax_all50.json")["states"].keys())
    spending_codes = set(load("state_spending_by_state.json")["states"].keys()) - {"ALL_STATES_AVERAGE"}
    missing_from_income = spending_codes - income_tax_codes
    check(not missing_from_income,
          f"States in spending data but missing from income tax data: {missing_from_income}")


if __name__ == "__main__":
    validate_federal_spending()
    validate_federal_brackets()
    validate_state_income_tax()
    validate_state_spending()
    validate_cross_references()

    print(f"Ran {checks_run} checks across 4 datasets.")
    if errors:
        print(f"\n{len(errors)} FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("All checks passed.")
        sys.exit(0)