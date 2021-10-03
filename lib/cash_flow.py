from lib.credit import get_loan_schedule
from lib.impots import get_yearly_tax
from lib.rendement import get_charges_credit_annuelles
import pandas as pd


def get_yearly_cf_table(credit, charges, revenus, achat, impots):

    # Loan schedule
    cf_table = get_loan_schedule(credit)

    # Charges
    cf_table['Assurance Autre'] = - charges['assurance_pno'] * 1000 - charges["assurance_loyer_impaye"] * 1000
    cf_table['Taxe Foncière'] = - charges['taxe_fonciere'] * 1000
    cf_table['Charges Copro'] = - charges["copropriete"] * 1000
    cf_table['Charges Vacance'] = - revenus["loyer_charges"] * revenus["vacance_locative"]  # Charges locatives payées en cas de vacance
    # TODO: Ajouter CFE si location meublée
    cf_table = get_initial_charges(cf_table, credit, achat, charges)
    charges_cols = list(cf_table.columns)

    # Revenus
    cf_table['Loyer HC'] = revenus["loyer_hc"] * 12 * (1 - revenus["vacance_locative"] / 12)
    cf_table.loc[0, 'Loyer HC'] = 0

    # Impots
    cf_table['TOTAL avant impôts'] = cf_table['Loyer HC'] + cf_table[charges_cols].sum(axis=1)
    cf_table = get_yearly_tax(cf_table, impots, revenus, achat)
    cf_table['TOTAL après impôts'] = cf_table['TOTAL avant impôts'] + cf_table['Impôts']

    # Total
    cf_table = cf_table.reset_index()
    cf_table['Année'] = cf_table['Année'].astype(str)
    cf_table = cf_table.set_index('Année')
    total = pd.DataFrame(cf_table.sum(axis=0)).T
    total.index = ['TOTAL']
    cf_table = pd.concat([cf_table, total], axis=0)

    return cf_table


def get_simplified_yearly_cf_table(credit, charges, revenus, achat, impots):

    cf_table = get_yearly_cf_table(credit, charges, revenus, achat, impots)

    # Charges diverses
    cf_table['Frais divers'] = cf_table['Assurance Autre'] + cf_table['Taxe Foncière'] + cf_table['Charges Copro']+ cf_table['Charges Vacance']

    # Charges crédit
    cf_table['Charges crédit'] = cf_table['Capital'] + cf_table['Intérêt'] + cf_table['Assurance Crédit']
    cf_table.loc['0', 'Charges crédit'] += cf_table.loc['0', 'Frais initiaux']

    cf_table['TOTAL'] = cf_table['Loyer HC'] + cf_table['Frais divers'] + cf_table['Impôts'] + cf_table['Charges crédit']
    cf_table = cf_table [['Loyer HC', 'Frais divers', 'Impôts', 'Charges crédit', 'TOTAL']]

    # Total
    cf_table = cf_table.drop('TOTAL', axis=0)
    total = pd.DataFrame(cf_table.sum(axis=0)).T
    total.index = ['TOTAL']
    cf_table = pd.concat([cf_table, total], axis=0)

    return cf_table


def get_initial_charges(cf_table, credit, achat, charges):
    cf_table.loc[0, "Capital"] = credit["montant"] * 1000
    frais_initiaux = [
        achat["montant"],
        charges["notaire"],
        charges["agence"],
        charges["dossier_bancaire"],
        charges["garantie_financement"],
        charges["courtier"],
        charges["travaux"],
        charges["achat_mobilier"],
        charges["TVA"]
    ]
    cf_table.loc[0, "Frais initiaux"] = - sum(frais_initiaux) * 1000
    return cf_table.sort_index().fillna(0)