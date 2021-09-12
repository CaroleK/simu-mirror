import streamlit as st
from lib.cash_flow import get_yearly_cf_table
from lib.visualisation import (
    plot_yearly_cash_flow,
    plot_cumulated_cash_flow,
    display_global_cash_flow,
    display_rendement,
)

achat, credit, impots, revenus, charges = dict(), dict(), dict(), dict(), dict()

st.sidebar.title("1. Achat")
achat["montant"] = st.sidebar.number_input("Montant de l'achat (k€)", 200)
achat["zone"] = st.sidebar.selectbox("Zone", ['A1', 'A2', 'B1', 'B2', 'C'])
achat["surface"] = st.sidebar.number_input("Surface (m2)", 40)
achat["surface_annexes"] = st.sidebar.number_input("Surface annexes (m2)", 0)

st.sidebar.title("2. Crédit")
credit["montant"] = st.sidebar.number_input("Montant emprunté (k€)", 180)
credit["duree"] = st.sidebar.number_input("Durée (années)", 20)
credit["taux_interet"] = st.sidebar.number_input("Taux d'intérêt (%)", 1.2)
credit["taux_assurance"] = st.sidebar.number_input("Taux d'assurance (%)", 0.02)

st.sidebar.title("3. Fiscalité")
impots["regime"] = st.sidebar.selectbox("Régime", ['Micro-Foncier', 'Foncier Réel', 'Micro-BIC', 'BIC Réel (LMNP)'])
impots["tmi"] = st.sidebar.number_input("TMI (%)", 30)

st.sidebar.title("4. Revenus")
revenus["loyer_hc"] = st.sidebar.number_input("Loyer mensuel HC (€)", 1600)
revenus["loyer_charges"] = st.sidebar.number_input("Charges mensuelles (€)", 200)
revenus["loyer_cc"] = revenus["loyer_hc"] + revenus["loyer_charges"]
revenus["vacance_locative"] = st.sidebar.number_input("Vacance locative (mois/an)", 0.5)

st.sidebar.title("5. Charges")
with st.sidebar.expander("Charges initiales", expanded=False):
    charges["notaire"] = st.number_input("Notaire (k€)", 0.075*achat["montant"])
    charges["agence"] = st.number_input("Agence (k€)", 1)
    charges["dossier_bancaire"] = st.number_input("Dossier bancaire (k€)", 0.5)
    charges["garantie_financement"] = st.number_input("Garantie de financement (k€)", 0.5)
    charges["courtier"] = st.number_input("Courtier (k€)", 1)
with st.sidebar.expander("Aménagement", expanded=False):
    charges["travaux"] = st.number_input("Travaux (k€)", 1)
    charges["achat_mobilier"] = st.number_input("Achat mobilier (k€)", 1.5)
with st.sidebar.expander("Assurances", expanded=False):
    charges["assurance_pno"] = st.number_input("Assurance habitation PNO (k€)", 0.2)
    charges["assurance_loyer_impaye"] = st.number_input("Assurance loyer impayé (k€)", 0.2)
with st.sidebar.expander("Charges récurrentes", expanded=False):
    charges["taxe_fonciere"] = st.number_input("Taxe foncière (k€)", 1)
    charges["copropriete"] = st.number_input("Charges de copropriété (k€)", 0.5)

st.title("1. Rendement")
display_rendement()

st.title("2. Cash Flow")
cf_table = get_yearly_cf_table(credit, charges, revenus, achat, impots)
display_global_cash_flow(cf_table, credit)
st.dataframe(cf_table.style.format("{:.0f}"))
st.plotly_chart(plot_yearly_cash_flow(cf_table, credit))
st.plotly_chart(plot_cumulated_cash_flow(cf_table))
