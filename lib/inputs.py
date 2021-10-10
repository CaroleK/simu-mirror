import streamlit as st
from lib.utils import load_toml
from lib.impots import get_cosse_ancien_max_loyer

config = load_toml("config")
notes = load_toml("notes")


def get_achat_inputs(achat):
    achat["montant"] = st.sidebar.number_input(
        "Montant de l'achat (k€)",
        value=config['achat']['montant'],
        min_value=0,
    )
    achat["zone"] = st.sidebar.selectbox(
        "Zone",
        options=config['achat']['zone'],
    )
    achat["surface"] = st.sidebar.number_input(
        "Surface (m2)",
        value=config['achat']['surface'],
        min_value=10,
    )
    achat["surface_annexes"] = st.sidebar.number_input(
        "Surface annexes (m2)",
        value=config['achat']['surface_annexes'],
        min_value=0,
    )
    return achat


def get_credit_inputs(credit):
    credit["montant"] = st.sidebar.number_input(
        "Montant emprunté (k€)",
        value=config['credit']['montant'],
        min_value=0,
    )
    credit["duree"] = st.sidebar.number_input(
        "Durée (années)",
        value=config['credit']['duree'],
        min_value=5
    )
    credit["taux_interet"] = st.sidebar.number_input(
        "Taux d'intérêt (%)",
        value=config['credit']['taux_interet'],
        min_value=0.0,
        format="%.2f",
    )
    credit["taux_assurance"] = st.sidebar.number_input(
        "Taux d'assurance (%)",
        value=config['credit']['taux_assurance'],
        min_value=0.0,
        format="%.3f",
    )
    return credit


def get_impots_inputs(impots):
    impots["regime"] = st.sidebar.selectbox(
        "Régime",
        options=config['fiscalite']['regime'],
    )
    impots["cosse_ancien"] = st.sidebar.checkbox("Régime Cosse Ancien") if impots["regime"] == 'Foncier Réel' else False
    if impots["cosse_ancien"]:
        impots["cosse_ancien_convention"] = st.sidebar.selectbox(
            "Convention (Cosse Ancien)",
            options=config['cosse']['types'],
        )
    impots["tmi"] = st.sidebar.selectbox(
        "TMI (%)",
        options=config['fiscalite']['tmi'],
    )
    impots["prelevements_sociaux"] = config['fiscalite']['prelevements_sociaux']
    return impots


def get_revenus_inputs(revenus, impots, achat):
    revenus["loyer_hc"] = st.sidebar.number_input(
        "Loyer mensuel HC (€)",
        value=get_cosse_ancien_max_loyer(impots, achat) if impots["cosse_ancien"] else config['revenus']['loyer_hc'],
        min_value=0,
        max_value=get_cosse_ancien_max_loyer(impots, achat) if impots["cosse_ancien"] else 10000,
    )
    revenus["loyer_charges"] = st.sidebar.number_input(
        "Charges mensuelles (€)",
        value=config['revenus']['loyer_charges'],
        min_value=0,
    )
    revenus["loyer_cc"] = revenus["loyer_hc"] + revenus["loyer_charges"]
    revenus["vacance_locative"] = st.sidebar.number_input(
        "Vacance locative (mois/an)",
        value=config['revenus']['vacance_locative_mois_par_an'],
        min_value=0.0,
        format="%.2f",
        help=notes['sidebar']['vacance_locative'],
    )
    return revenus


def get_charges_inputs(charges, impots, achat):

    with st.sidebar.expander("Charges initiales", expanded=False):
        charges["notaire"] = st.number_input(
            "Notaire (k€)",
            value=config['charges']['taux_notaire'] * achat["montant"],
            min_value=0.0,
            help=notes['sidebar']['notaire'],
        )
        charges["agence"] = st.number_input(
            "Agence (k€)",
            value=config['charges']['agence'],
            min_value=0.0,
            format="%.2f",
        )
        charges["dossier_bancaire"] = st.number_input(
            "Dossier bancaire (k€)",
            value=config['charges']['dossier_bancaire'],
            min_value=0.0,
            format="%.2f",
        )
        charges["garantie_financement"] = st.number_input(
            "Garantie de financement (k€)",
            value=config['charges']['garantie_financement'],
            min_value=0.0,
            format="%.2f",
        )
        charges["courtier"] = st.number_input(
            "Courtier (k€)",
            value=config['charges']['courtier'],
            min_value=0.0,
            format="%.2f",
        )

    with st.sidebar.expander("Aménagement", expanded=False):
        charges["travaux"] = st.number_input(
            "Travaux (k€)",
            value=config['charges']['travaux'],
            min_value=0.0,
            format="%.2f",
        )
        charges["achat_mobilier"] = st.number_input(
            "Achat mobilier (k€)",
            value=config['charges']['achat_mobilier'],
            min_value=0.0,
            format="%.2f",
        )

    with st.sidebar.expander("Assurances", expanded=False):
        charges["assurance_pno"] = st.number_input(
            "Assurance habitation PNO (k€)",
            value=config['charges']['assurance_pno'],
            min_value=0.0,
            format="%.2f",
        )
        charges["assurance_loyer_impaye"] = st.number_input(
            "Assurance loyer impayé (k€)",
            value=config['charges']['assurance_loyer_impaye'],
            min_value=0.0,
            format="%.2f",
        )

    with st.sidebar.expander("Charges récurrentes", expanded=False):
        charges["taxe_fonciere"] = st.number_input(
            "Taxe foncière (k€)",
            value=config['charges']['taxe_fonciere'],
            min_value=0.0,
            format="%.2f",
        )
        charges["copropriete"] = st.number_input(
            "Charges de copropriété (k€)",
            value=config['charges']['copropriete'],
            min_value=0.0,
            format="%.2f",
        )

    if impots["regime"] in ['Micro-BIC', 'BIC Réel (LMNP)']:
        with st.sidebar.expander("Charges location meublée", expanded=False):
            charges["taxe_cfe"] = st.number_input(
                "Taxe CFE (k€)",
                value=config['charges']['taxe_cfe'],
                min_value=0.0,
                format="%.2f",
            )
            charges["comptable_cga"] = st.number_input(
                "Frais de comptabilité + CGA (k€)",
                value=config['charges']['comptable_cga'],
                min_value=0.0,
                format="%.2f",
            )
    else:
        charges["taxe_cfe"] = 0
        charges["comptable_cga"] = 0

    return charges
