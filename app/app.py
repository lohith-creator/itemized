import streamlit as st
from calculations import (
    calculate_federal_tax,
    calculate_state_tax,
    federal_receipt,
    state_receipt,
    list_states,
)

st.set_page_config(page_title="Itemized — Where Your Tax Dollars Go", page_icon="🧾", layout="centered")

# ---- styling: monospace receipt look, matching the portfolio's dark/amber theme ----
st.markdown("""
<style>
    .stApp { background-color: #0E1620; }
    * { font-family: 'JetBrains Mono', 'Courier New', monospace !important; }
    .receipt-line {
        display: flex; justify-content: space-between;
        padding: 4px 0; border-bottom: 1px dotted #263241;
        color: #E9EDF1; font-size: 14px;
    }
    .receipt-total {
        display: flex; justify-content: space-between;
        padding: 10px 0; margin-top: 8px; border-top: 2px solid #E8A33D;
        color: #E8A33D; font-weight: bold; font-size: 16px;
    }
    .receipt-header {
        text-align: center; color: #8A97A6; font-size: 12px;
        letter-spacing: 2px; margin-bottom: 12px; text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧾 Itemized")
st.caption("See exactly where your tax dollars go — down to the category.")

col1, col2, col3 = st.columns([1.2, 1, 1])
with col1:
    salary = st.number_input("Annual salary ($)", min_value=0, value=75000, step=1000)
with col2:
    filing_status = st.selectbox("Filing status", ["single", "married_filing_jointly"],
                                  format_func=lambda x: "Single" if x == "single" else "Married filing jointly")
with col3:
    states = list_states()
    state_code = st.selectbox("State", [c for c, _ in states],
                               format_func=lambda c: dict(states)[c],
                               index=[c for c, _ in states].index("IL") if "IL" in dict(states) else 0)

if salary <= 0:
    st.info("Enter a salary above to generate your receipt.")
    st.stop()

federal = calculate_federal_tax(salary, filing_status)
state = calculate_state_tax(salary, state_code)
fed_lines = sorted(federal_receipt(federal["tax_owed"]), key=lambda x: -x["amount"])
state_lines = sorted(state_receipt(state["tax_owed"], state_code), key=lambda x: -x["amount"])

total_tax = federal["tax_owed"] + state["tax_owed"]

# ---- summary strip ----
s1, s2, s3 = st.columns(3)
s1.metric("Federal tax", f"${federal['tax_owed']:,.0f}", f"{federal['effective_rate']*100:.1f}% effective")
s2.metric(f"{state['state_name']} tax", f"${state['tax_owed']:,.0f}",
          f"{state['effective_rate']*100:.1f}% effective" if state['tax_owed'] > 0 else "no income tax")
s3.metric("Total tax", f"${total_tax:,.0f}", f"per day: ${total_tax/365:,.2f}")

st.divider()

# ---- federal receipt ----
st.markdown('<div class="receipt-header">— FEDERAL RECEIPT — FY2024 —</div>', unsafe_allow_html=True)
for line in fed_lines:
    st.markdown(
        f'<div class="receipt-line"><span>{line["label"]} ({line["percent"]}%)</span>'
        f'<span>${line["amount"]:,.2f}</span></div>',
        unsafe_allow_html=True,
    )
st.markdown(
    f'<div class="receipt-total"><span>FEDERAL TOTAL</span><span>${federal["tax_owed"]:,.2f}</span></div>',
    unsafe_allow_html=True,
)

st.write("")

# ---- state receipt ----
if state["tax_owed"] > 0:
    st.markdown(f'<div class="receipt-header">— {state["state_name"].upper()} RECEIPT — FY2024 —</div>', unsafe_allow_html=True)
    for line in state_lines:
        st.markdown(
            f'<div class="receipt-line"><span>{line["label"]} ({line["percent"]}%)</span>'
            f'<span>${line["amount"]:,.2f}</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        f'<div class="receipt-total"><span>{state["state_name"].upper()} TOTAL</span>'
        f'<span>${state["tax_owed"]:,.2f}</span></div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(f'<div class="receipt-header">— {state["state_name"].upper()} —</div>', unsafe_allow_html=True)
    notes = state.get("notes")
    st.info(f"{state['state_name']} has no tax on wage income." + (f" {notes}" if notes else ""))

st.divider()
st.caption(
    "Federal figures: CBPP, using CBO data (FY2024). State income tax: Tax Foundation (2026). "
    "State spending shares: NASBO 2024 State Expenditure Report, Table 5. "
    "This is an estimate for illustration — not tax advice."
)
