import pandas as pd


def get_yearly_tax(cf_table, impots, charges, revenus, credit):
    if impots["regime"] == "Micro-Foncier":
        return calculate_tax_micro_foncier(cf_table, impots)
    elif impots["regime"] == "Foncier Réel":
        return calculate_tax_foncier_reel(cf_table, impots)
    elif impots["regime"] == "Micro-BIC":
        return calculate_tax_micro_bic(cf_table, impots, revenus)
    elif impots["regime"] == "BIC Réel (LMNP)":
        return calculate_tax_bic_reel(cf_table)


def calculate_tax_micro_foncier(cf_table, impots):
    base_imposable = cf_table['Loyer HC'] * 0.7
    cf_table = _add_tax_column(cf_table, impots, base_imposable)
    return cf_table


def calculate_tax_foncier_reel(cf_table, impots):

    # Charges déductibles
    charges_deductibles = cf_table['Intérêt']
    charges_deductibles += cf_table['Taxe Foncière']  # TODO: Ajustement TEOM (p.366)
    charges_deductibles += cf_table['Assurance Crédit']
    charges_deductibles += cf_table['Assurance Autre']
    charges_deductibles += cf_table['Charges Copro'] * 0.5  # TODO: Affiner l'hypothèse de la proportion des charges déductibles (p.366-367)
    charges_deductibles += cf_table['Charges Vacance']  # Montant des charges locatives payées au titre d'une période de vacances entre 2 locations (p.365)
    charges_deductibles -= 20  # Montant forfaitaire par local (p.363)
    # TODO: Ajouter les frais d'inscription hypothécaire et les frais de constitution du dossier auprès de la banque (p.368)

    # Impots
    base_imposable = cf_table['Loyer HC'] + charges_deductibles
    cf_table = _add_tax_column(cf_table, impots, base_imposable)
    # TODO: Prendre en compte le déficit foncier et la répercussion sur les années suivantes si dépassement du seuil de 10700€ (p.369)

    return cf_table


def calculate_tax_micro_bic(cf_table, impots, revenus):
    loyer_cc = cf_table['Loyer HC'] + revenus["loyer_charges"] * 12 * (1 - revenus["vacance_locative"] / 12)
    base_imposable = loyer_cc * 0.5
    cf_table = _add_tax_column(cf_table, impots, base_imposable)
    return cf_table


def calculate_tax_bic_reel(cf_table):
    cf_table['Impôts'] = 0
    return cf_table


def _add_tax_column(cf_table, impots, base_imposable):
    total_impots = - _get_tax_rate(impots) * base_imposable
    cf_table['Impôts'] = total_impots.map(lambda x: min(x, 0))
    cf_table.loc[0, 'Impôts'] = 0
    return cf_table


def _get_tax_rate(impots):
    return (impots['tmi'] + impots["prelevements_sociaux"]) / 100
