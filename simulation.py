import streamlit as st
from lib.cash_flow import get_yearly_cf_table, get_simplified_yearly_cf_table
from lib.utils import load_toml
from lib.visualisation import (
    plot_yearly_cash_flow,
    plot_cumulated_cash_flow,
    display_cash_flow,
    display_rendement,
    plot_cash_flow_waterfall,
)
from lib.inputs import (
    get_achat_inputs,
    get_credit_inputs,
    get_impots_inputs,
    get_revenus_inputs,
    get_charges_inputs,
)

notes = load_toml("notes")

# Inputs

achat, credit, impots, revenus, charges = dict(), dict(), dict(), dict(), dict()

st.sidebar.title("1. Achat")
achat = get_achat_inputs(achat)

st.sidebar.title("2. Crédit")
credit = get_credit_inputs(credit)

st.sidebar.title("3. Fiscalité")
impots = get_impots_inputs(impots)

st.sidebar.title("4. Revenus")
revenus = get_revenus_inputs(revenus, impots, achat)

st.sidebar.title("5. Charges")
charges = get_charges_inputs(charges, impots, achat)


# Calculation & Visualization

cf_table = get_yearly_cf_table(credit, charges, revenus, achat, impots)
simplified_cf_table = get_simplified_yearly_cf_table(credit, charges, revenus, achat, impots)

st.title("1. Rendement")
with st.expander("Notes", expanded=False):
    st.write(notes['main']['rendement'])
display_rendement(revenus, charges, credit, cf_table, impots)

st.title("2. Cash Flow")
st.plotly_chart(plot_cash_flow_waterfall(cf_table, charges, revenus, credit, impots))
display_cash_flow(cf_table, credit, achat)
st.dataframe(simplified_cf_table.style.format("{:.0f}"))
with st.expander("Détails", expanded=False):
    st.dataframe(cf_table.style.format("{:.0f}"))
st.plotly_chart(plot_yearly_cash_flow(cf_table, credit))
st.plotly_chart(plot_cumulated_cash_flow(cf_table))
