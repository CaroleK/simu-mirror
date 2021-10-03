from lib.utils import load_config

config = load_config()


def get_yearly_tax(cf_table, impots, revenus, achat):
    if impots["regime"] == "Micro-Foncier":
        return calculate_tax_micro_foncier(cf_table, impots)
    elif impots["regime"] == "Foncier Réel":
        return calculate_tax_foncier_reel(cf_table, impots, achat)
    elif impots["regime"] == "Micro-BIC":
        return calculate_tax_micro_bic(cf_table, impots, revenus)
    elif impots["regime"] == "BIC Réel (LMNP)":
        return calculate_tax_bic_reel(cf_table)


def calculate_tax_micro_foncier(cf_table, impots):
    base_imposable = cf_table['Loyer HC'] * 0.7
    charges_deductibles = 0
    cf_table = _add_tax_column(cf_table, impots, base_imposable, charges_deductibles)
    return cf_table


def calculate_tax_foncier_reel(cf_table, impots, achat):

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

    # Impots
    if impots['cosse_ancien']:
        deduction = config['cosse']['deduction'][impots["cosse_ancien_convention"]][achat["zone"]]
        base_imposable = cf_table['Loyer HC'] * (1 - deduction) + charges_deductibles
    else:
        base_imposable = cf_table['Loyer HC'] + charges_deductibles
    cf_table = _add_tax_column(cf_table, impots, base_imposable, charges_deductibles)
    # TODO: Prendre en compte le déficit foncier et la répercussion sur les années suivantes si dépassement du seuil de 10700€ (p.369)

    return cf_table


def calculate_tax_micro_bic(cf_table, impots, revenus):
    loyer_cc = cf_table['Loyer HC'] + revenus["loyer_charges"] * 12 * (1 - revenus["vacance_locative"] / 12)
    base_imposable = loyer_cc * 0.5
    charges_deductibles = 0
    cf_table = _add_tax_column(cf_table, impots, base_imposable, charges_deductibles)
    return cf_table


def calculate_tax_bic_reel(cf_table):
    cf_table['Impôts'] = 0
    return cf_table


def _add_tax_column(cf_table, impots, base_imposable, charges_deductibles):
    total_impots = - _get_tax_rate(impots) * base_imposable
    cf_table['(Charges déductibles)'] = - charges_deductibles
    cf_table['(Base imposable)'] = base_imposable
    cf_table['Impôts'] = total_impots.map(lambda x: min(x, 0))
    cf_table.loc[0, 'Impôts'] = 0
    return cf_table


def _get_tax_rate(impots):
    return (impots['tmi'] + impots["prelevements_sociaux"]) / 100


def get_cosse_ancien_max_loyer(impots, achat):
    plafond = config['cosse']['plafond'][impots["cosse_ancien_convention"]][achat["zone"]]
    return int(achat["surface"] * plafond)