"""
Core calculation logic for the Tax Receipt app.
Pure functions, no Streamlit dependency, so they're independently testable.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def calculate_federal_tax(gross_income, filing_status="single"):
    data = load_json("federal_tax_brackets_2026.json")
    standard_deduction = data["standard_deduction"][filing_status]
    taxable_income = max(0, gross_income - standard_deduction)

    brackets = data["brackets"][filing_status]
    tax_owed = 0.0
    lower_bound = 0
    marginal_rate = 0

    for bracket in brackets:
        rate = bracket["rate"]
        upper_bound = bracket["up_to"]
        taxed_amount = (max(0, min(taxable_income, upper_bound) - lower_bound)
                         if upper_bound is not None
                         else max(0, taxable_income - lower_bound))
        if taxed_amount > 0:
            tax_owed += taxed_amount * rate
            marginal_rate = rate
        if upper_bound is not None and taxable_income <= upper_bound:
            break
        lower_bound = upper_bound if upper_bound is not None else lower_bound

    return {
        "taxable_income": taxable_income,
        "standard_deduction": standard_deduction,
        "tax_owed": round(tax_owed, 2),
        "effective_rate": round(tax_owed / gross_income, 4) if gross_income else 0,
        "marginal_rate": marginal_rate,
    }


def calculate_state_tax(gross_income, state_code):
    data = load_json("state_income_tax_all50.json")
    state = data["states"][state_code]
    structure = state["structure"]

    if structure == "none":
        return {"state_name": state["name"], "tax_owed": 0.0, "effective_rate": 0.0}

    if structure == "flat":
        tax_owed = gross_income * state["rate"]
        return {"state_name": state["name"], "tax_owed": round(tax_owed, 2), "effective_rate": state["rate"]}

    if structure == "special":
        return {"state_name": state["name"], "tax_owed": 0.0, "effective_rate": 0.0, "notes": state.get("notes")}

    if structure == "graduated":
        brackets = state["brackets"]
        tax_owed = 0.0
        for i, bracket in enumerate(brackets):
            lower = bracket["over"]
            upper = brackets[i + 1]["over"] if i + 1 < len(brackets) else None
            if gross_income <= lower:
                break
            taxed_amount = (min(gross_income, upper) if upper else gross_income) - lower
            tax_owed += taxed_amount * bracket["rate"]
        return {
            "state_name": state["name"],
            "tax_owed": round(tax_owed, 2),
            "effective_rate": round(tax_owed / gross_income, 4) if gross_income else 0,
        }


def federal_receipt(federal_tax_owed):
    """Split the federal tax bill into category dollar amounts."""
    data = load_json("federal_spending_fy2024.json")
    lines = []
    for cat in data["categories"]:
        lines.append({
            "label": cat["label"],
            "percent": cat["percent"],
            "amount": round(federal_tax_owed * cat["percent"] / 100, 2),
        })
    return lines


def state_receipt(state_tax_owed, state_code):
    """Split the state tax bill into category dollar amounts using real per-state NASBO shares."""
    data = load_json("state_spending_by_state.json")
    state_data = data["states"].get(state_code)
    if not state_data:
        return []
    labels = {
        "k12_education": "K-12 Education",
        "higher_education": "Higher Education",
        "public_assistance": "Public Assistance",
        "medicaid": "Medicaid",
        "corrections": "Corrections",
        "transportation": "Transportation",
        "all_other": "All Other (admin, environment, housing, etc.)",
    }
    lines = []
    for key in data["category_order"]:
        percent = state_data[key]
        lines.append({
            "label": labels[key],
            "percent": percent,
            "amount": round(state_tax_owed * percent / 100, 2),
        })
    return lines


def list_states():
    data = load_json("state_income_tax_all50.json")
    return sorted(
        [(code, s["name"]) for code, s in data["states"].items()],
        key=lambda x: x[1],
    )
