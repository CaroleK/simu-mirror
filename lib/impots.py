import pandas as pd


def get_yearly_tax(cf_table, impots, charges, revenus, credit):
    if impots["regime"] == "Micro-Foncier":
        return calculate_tax_micro_foncier(cf_table, impots, revenus)
    elif impots["regime"] == "Foncier Réel":
        return calculate_tax_foncier_reel(cf_table)
    elif impots["regime"] == "Micro-BIC":
        return calculate_tax_micro_bic(cf_table)
    elif impots["regime"] == "BIC Réel (LMNP)":
        return calculate_tax_bic_reel(cf_table)


def calculate_tax_micro_foncier(cf_table, impots, revenus):
    taux = impots['tmi'] / 100 + 0.172
    base_imposable = cf_table['TOTAL avant impôts'] - 0.3 * revenus['loyer_hc'] * 12
    cf_table['Impôts'] = - taux * base_imposable
    cf_table.loc[0, 'Impôts'] = 0
    return cf_table


def calculate_tax_foncier_reel(cf_table):
    cf_table['Impôts'] = 0
    return cf_table


def calculate_tax_micro_bic(cf_table):
    cf_table['Impôts'] = 0
    return cf_table


def calculate_tax_bic_reel(cf_table):
    cf_table['Impôts'] = 0
    return cf_table