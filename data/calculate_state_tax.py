import json

def calculate_state_tax(gross_income, state_code, data_path="state_income_tax_all50.json"):
    """
    Estimate state income tax owed (single filer, no deductions applied -
    state standard deductions vary too much to generalize; treating gross
    income as taxable income for this first pass).
    """
    with open(data_path) as f:
        data = json.load(f)

    state = data["states"].get(state_code.upper())
    if not state:
        raise ValueError(f"Unknown state code: {state_code}")

    structure = state["structure"]

    if structure == "none":
        return {"state": state["name"], "structure": "none", "tax_owed": 0.0, "effective_rate": 0.0}

    if structure == "flat":
        tax_owed = gross_income * state["rate"]
        return {
            "state": state["name"],
            "structure": "flat",
            "tax_owed": round(tax_owed, 2),
            "effective_rate": state["rate"],
        }

    if structure == "special":
        # e.g. Washington - wage income untaxed
        return {"state": state["name"], "structure": "special", "tax_owed": 0.0,
                "effective_rate": 0.0, "notes": state.get("notes")}

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

        effective_rate = tax_owed / gross_income if gross_income > 0 else 0
        return {
            "state": state["name"],
            "structure": "graduated",
            "tax_owed": round(tax_owed, 2),
            "effective_rate": round(effective_rate, 4),
        }

    raise ValueError(f"Unknown structure: {structure}")


if __name__ == "__main__":
    for code in ["IL", "TX", "CA", "WA", "NY"]:
        print(f"$85,000 salary in {code}:", calculate_state_tax(85000, code))
