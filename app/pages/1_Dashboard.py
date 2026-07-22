import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from calculations import calculate_state_tax, load_json, list_states

st.set_page_config(page_title="Dashboard — Itemized", page_icon="📊", layout="wide")

# ---- theme to match the rest of the app ----
INK, INK2, PAPER, MUTED, AMBER, MINT = "#0E1620", "#141F2A", "#E9EDF1", "#8A97A6", "#E8A33D", "#6FE7C8"
PALETTE = [AMBER, MINT, "#7FA8E8", "#E86F9E", "#B98CE8", "#8AE85E", "#E8C05E"]

st.markdown(f"""
<style>
    .stApp {{ background-color: {INK}; }}
    * {{ font-family: 'JetBrains Mono', 'Courier New', monospace !important; }}
</style>
""", unsafe_allow_html=True)

def style_fig(fig, height=420):
    fig.update_layout(
        paper_bgcolor=INK, plot_bgcolor=INK,
        font=dict(color=PAPER, family="JetBrains Mono, monospace", size=12),
        margin=dict(l=10, r=10, t=50, b=10),
        height=height,
    )
    return fig

st.title("📊 National dashboard")
st.caption("Where tax dollars go, across all 50 states — real government data, not estimates.")

# ---------------- Row 1: federal spending + state tax map ----------------
col1, col2 = st.columns([1, 1.4])

with col1:
    fed = load_json("federal_spending_fy2024.json")
    labels = [c["label"] for c in fed["categories"]]
    values = [c["percent"] for c in fed["categories"]]
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.45,
        marker=dict(colors=PALETTE, line=dict(color=INK, width=2)),
        textinfo="percent", textfont=dict(color=INK, size=12),
    )])
    fig.update_layout(
        title="Federal spending by category (FY2024)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, font=dict(size=10)),
    )
    st.plotly_chart(style_fig(fig, 480), use_container_width=True)

with col2:
    salary_map = st.slider("Salary for map ($)", 30000, 250000, 85000, step=5000, key="map_salary")
    state_data = load_json("state_income_tax_all50.json")
    codes, names, taxes, rates = [], [], [], []
    for code in state_data["states"]:
        if code == "DC":
            continue
        result = calculate_state_tax(salary_map, code)
        codes.append(code)
        names.append(result["state_name"])
        taxes.append(result["tax_owed"])
        rates.append(result["effective_rate"] * 100)

    fig2 = go.Figure(data=go.Choropleth(
        locations=codes, z=taxes, locationmode="USA-states",
        colorscale=[[0, INK2], [0.5, "#B98C5E"], [1, AMBER]],
        marker_line_color=INK, marker_line_width=1,
        text=names, colorbar_title="Tax ($)",
    ))
    fig2.update_layout(
        title=f"State income tax owed on a ${salary_map:,} salary",
        geo=dict(scope="usa", bgcolor=INK, lakecolor=INK, showlakes=True),
    )
    st.plotly_chart(style_fig(fig2, 480), use_container_width=True)

st.divider()

# ---------------- Row 2: state spending comparison ----------------
st.subheader("Compare how two states spend their tax dollars")

states = list_states()
c1, c2 = st.columns(2)
with c1:
    state_a = st.selectbox("State A", [c for c, _ in states], format_func=lambda c: dict(states)[c],
                            index=[c for c, _ in states].index("IL") if "IL" in dict(states) else 0)
with c2:
    state_b = st.selectbox("State B", [c for c, _ in states], format_func=lambda c: dict(states)[c],
                            index=[c for c, _ in states].index("TX") if "TX" in dict(states) else 1)

spending = load_json("state_spending_by_state.json")
cat_labels = {
    "k12_education": "K-12 Education", "higher_education": "Higher Education",
    "public_assistance": "Public Assistance", "medicaid": "Medicaid",
    "corrections": "Corrections", "transportation": "Transportation", "all_other": "All Other",
}
order = spending["category_order"]

if state_a in spending["states"] and state_b in spending["states"]:
    a_vals = [spending["states"][state_a][k] for k in order]
    b_vals = [spending["states"][state_b][k] for k in order]
    cat_names = [cat_labels[k] for k in order]

    fig3 = go.Figure(data=[
        go.Bar(name=dict(states)[state_a], x=cat_names, y=a_vals, marker_color=AMBER),
        go.Bar(name=dict(states)[state_b], x=cat_names, y=b_vals, marker_color=MINT),
    ])
    fig3.update_layout(
        barmode="group", title=f"{dict(states)[state_a]} vs {dict(states)[state_b]} — spending mix (% of total)",
        yaxis_title="% of state spending",
        legend=dict(orientation="h", yanchor="bottom", y=1.05),
    )
    st.plotly_chart(style_fig(fig3, 420), use_container_width=True)
else:
    st.info("Spending category data isn't available for one of these selections.")

st.caption(
    "Sources: CBPP/CBO (federal spending, FY2024) · Tax Foundation (state income tax, 2026) · "
    "NASBO 2024 State Expenditure Report (state spending mix)."
)
