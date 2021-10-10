import pandas as pd
from lib.utils import load_toml

config = load_toml("config")


def get_yearly_tax(cf_table, impots, revenus, achat, charges, credit):
    if impots["regime"] == "Micro-Foncier":
        return calculate_tax_micro_foncier(cf_table, impots, credit)
    elif impots["regime"] == "Foncier Réel":
        return calculate_tax_foncier_reel(cf_table, impots, achat, credit)
    elif impots["regime"] == "Micro-BIC":
        return calculate_tax_micro_bic(cf_table, impots, revenus, credit)
    elif impots["regime"] == "BIC Réel (LMNP)":
        return calculate_tax_bic_reel(cf_table, revenus, charges, achat, impots, credit)


def calculate_tax_micro_foncier(cf_table, impots, credit):
    base_imposable = cf_table['Loyer HC'] * 0.7
    charges_deductibles, amortissements = 0, 0
    cf_table = _add_tax_column(cf_table, impots, base_imposable, charges_deductibles, amortissements, credit)
    return cf_table


def calculate_tax_foncier_reel(cf_table, impots, achat, credit):

    # Charges déductibles
    charges_deductibles = cf_table['Intérêt'].copy()
    charges_deductibles += cf_table['Taxe Foncière'].copy()  # TODO: Ajustement TEOM (p.366)
    charges_deductibles += cf_table['Assurance Crédit'].copy()
    charges_deductibles += cf_table['Assurance Autre'].copy()
    charges_deductibles += cf_table['Charges Copro'].copy() * 0.5  # TODO: Affiner l'hypothèse de la proportion des charges déductibles (p.366-367)
    charges_deductibles += cf_table['Charges Vacance'].copy()  # Montant des charges locatives payées au titre d'une période de vacances entre 2 locations (p.365)
    charges_deductibles -= 20  # Montant forfaitaire par local (p.363)
    charges_deductibles.loc[0] = 0
    # TODO: Ajouter les frais d'inscription hypothécaire et les frais de constitution du dossier auprès de la banque (p.368)

    # Amortissements
    amortissements = 0

    # Impots
    if impots['cosse_ancien']:
        deduction = config['cosse']['deduction'][impots["cosse_ancien_convention"]][achat["zone"]]
        base_imposable = cf_table['Loyer HC'] * (1 - deduction) + charges_deductibles
    else:
        base_imposable = cf_table['Loyer HC'] + charges_deductibles
    cf_table = _add_tax_column(cf_table, impots, base_imposable, charges_deductibles, amortissements, credit)
    # TODO: Prendre en compte le déficit foncier et la répercussion sur les années suivantes si dépassement du seuil de 10700€ (p.369)

    return cf_table


def calculate_tax_micro_bic(cf_table, impots, revenus, credit):
    loyer_cc = cf_table['Loyer HC'] + revenus["loyer_charges"] * 12 * (1 - revenus["vacance_locative"] / 12)
    base_imposable = loyer_cc * 0.5
    charges_deductibles, amortissements = 0, 0
    cf_table = _add_tax_column(cf_table, impots, base_imposable, charges_deductibles, amortissements, credit)
    return cf_table


def calculate_tax_bic_reel(cf_table, revenus, charges, achat, impots, credit):

    # Charges déductibles
    charges_deductibles = cf_table['Intérêt'].copy()
    charges_deductibles += cf_table['Taxe CFE'].copy()
    charges_deductibles += cf_table['Comptable + CGA'].copy() / 3  # Les deux autres tiers sont directement déduits des impôts (exemple p.453)
    charges_deductibles += cf_table['Taxe Foncière'].copy()  # TODO: Ajustement TEOM (p.366)
    charges_deductibles += cf_table['Assurance Crédit'].copy()
    charges_deductibles += cf_table['Assurance Autre'].copy()
    charges_deductibles += cf_table['Charges Copro'].copy()  # En totalité, sauf partie "Provisions pour loi ALUR" (p.442) # TODO: Voir si ça représente beaucoup ou si on peut garder 100%
    charges_deductibles -= revenus["loyer_charges"] * 12  # TODO: Vérifier que toutes les charges du locataire sont bien déductibles chaque mois
    charges_deductibles.loc[1] -= charges["notaire"] * 1000
    charges_deductibles.loc[1] -= charges["agence"] * 1000
    charges_deductibles.loc[1] -= charges["dossier_bancaire"] * 1000
    charges_deductibles.loc[1] -= charges["garantie_financement"] * 1000
    charges_deductibles.loc[1] -= charges["courtier"] * 1000
    charges_deductibles.loc[1] -= charges["achat_mobilier"] * 1000  # TODO: Prendre en compte les cas où l'achat de mobilier est pris en amortissements et non en charges
    charges_deductibles.loc[1] -= charges["travaux"] * 1000  # TODO: Prendre en compte les cas où l'achat de mobilier est pris en amortissements et non en charges
    charges_deductibles.loc[0] = 0

    # Amortissements
    # TODO: Hypothèse d'un amortissement linéaire de 1/30 de la valeur du bien chaque année, à affiner.
    # TODO: Ajouter les autres amortissements (travaux, achat de mobilier).
    amortissements = pd.Series(index=cf_table.index, data=achat['montant'] * 0.85 * 1000 / 30)  # Amortissement annuel du bien (voir exemple p.453)
    amortissements.loc[0] = 0

    # Impots
    loyer_cc = cf_table['Loyer HC'] + revenus["loyer_charges"] * 12 * (1 - revenus["vacance_locative"] / 12)
    loyer_cc.loc[0] = 0
    base_imposable = loyer_cc + charges_deductibles - amortissements
    cf_table = _add_tax_column(cf_table, impots, base_imposable, charges_deductibles, amortissements, credit)

    return cf_table


def _add_tax_column(cf_table, impots, base_imposable, charges_deductibles, amortissements, credit):

    # Réduction
    if impots["regime"] in ['Micro-BIC', 'BIC Réel (LMNP)']:
        reduction_impots = cf_table['Comptable + CGA'].copy() * (2/3)  # Le tiers restant est dans les charges déductibles (exemple p.453)
    else:
        reduction_impots = 0

    # Calculs intermédiaires
    cf_table["(Réduction d'impôts)"] = abs(reduction_impots)
    cf_table['(Amortissements)'] = amortissements
    cf_table['(Charges déductibles)'] = abs(charges_deductibles)
    cf_table['(Base imposable)'] = base_imposable
    cf_table = _calculate_report(cf_table, credit)

    # Impôts finaux
    total_impots = - _get_tax_rate(impots) * cf_table['(BI post report)'] - reduction_impots
    cf_table['Impôts'] = total_impots.map(lambda x: min(x, 0))
    cf_table.loc[0, 'Impôts'] = 0

    return cf_table


def _get_tax_rate(impots):
    return (impots['tmi'] + impots["prelevements_sociaux"]) / 100


def _calculate_report(cf_table, credit):
    cf_table['(Réserve)'] = 0
    cf_table['(BI post report)'] = 0
    for year in range(1, credit['duree'] + 1):
        BI_minus_report = cf_table.loc[year, '(Base imposable)'] + cf_table.loc[year - 1, '(Réserve)']
        cf_table.loc[year, '(Réserve)'] = min(BI_minus_report, 0)
        cf_table.loc[year, '(BI post report)'] = max(BI_minus_report, 0)
    return cf_table


def get_cosse_ancien_max_loyer(impots, achat):
    plafond = config['cosse']['plafond'][impots["cosse_ancien_convention"]][achat["zone"]]
    return int(achat["surface"] * plafond)
