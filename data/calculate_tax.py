import json

def calculate_federal_tax(gross_income, filing_status="single", brackets_path="federal_tax_brackets_2026.json"):
    """
    Estimate federal income tax owed using marginal brackets.
    gross_income: annual salary before deductions
    filing_status: "single" or "married_filing_jointly"
    Returns: dict with taxable_income, tax_owed, effective_rate, marginal_rate
    """
    with open(brackets_path) as f:
        data = json.load(f)

    standard_deduction = data["standard_deduction"][filing_status]
    taxable_income = max(0, gross_income - standard_deduction)

    brackets = data["brackets"][filing_status]
    tax_owed = 0.0
    lower_bound = 0
    marginal_rate = 0

    for bracket in brackets:
        rate = bracket["rate"]
        upper_bound = bracket["up_to"]

        if upper_bound is None:
            taxed_amount = max(0, taxable_income - lower_bound)
        else:
            taxed_amount = max(0, min(taxable_income, upper_bound) - lower_bound)

        if taxed_amount > 0:
            tax_owed += taxed_amount * rate
            marginal_rate = rate

        if upper_bound is not None and taxable_income <= upper_bound:
            break

        lower_bound = upper_bound if upper_bound is not None else lower_bound

    effective_rate = (tax_owed / gross_income) if gross_income > 0 else 0

    return {
        "gross_income": gross_income,
        "standard_deduction": standard_deduction,
        "taxable_income": taxable_income,
        "tax_owed": round(tax_owed, 2),
        "effective_rate": round(effective_rate, 4),
        "marginal_rate": marginal_rate,
    }


if __name__ == "__main__":
    # quick sanity checks against the known examples from search results
    result = calculate_federal_tax(65000, "single")
    print("Single, $65,000 salary:", result)

    result2 = calculate_federal_tax(150000, "married_filing_jointly")
    print("MFJ, $150,000 salary:", result2)
