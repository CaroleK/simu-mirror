def get_loyer_cc_annuel_moyen(revenus):
    return revenus["loyer_hc"] * 12 * (1 - revenus["vacance_locative"] / 12)


def get_frais_initiaux(cf_table):
    return - cf_table.loc['0', 'Frais initiaux']


def get_charges_annuelles(charges, cf_table):
    charges_recurrentes = [
        "copropriete",
        "taxe_fonciere",
        "assurance_pno",
        "assurance_loyer_impaye"
    ]
    charges_rendement = 1000 * sum([charges[i] for i in charges_recurrentes])
    charges_vacance_locative = - cf_table.loc['1', 'Charges Vacance']
    return charges_rendement + charges_vacance_locative


def get_charges_credit_annuelles(cf_table, credit):
    interet = - cf_table.loc['TOTAL', 'Intérêt'] / credit["duree"]
    capital = cf_table.loc['0', 'Capital'] / credit["duree"]
    assurance = - cf_table.loc['1', 'Assurance Crédit']
    return interet + capital + assurance


def get_impot_annuel_moyen(cf_table, credit):
    return - cf_table.loc['TOTAL', 'Impôts'] / credit["duree"]


def get_rendement_brut(revenus, cf_table):
    num = get_loyer_cc_annuel_moyen(revenus)
    den = get_frais_initiaux(cf_table)
    return round(100 * num / den, 2)


def get_rendement_net(revenus, charges, cf_table):
    loyer_cc_annuel_moyen = get_loyer_cc_annuel_moyen(revenus)
    charges_annuelles = get_charges_annuelles(charges, cf_table)
    num = loyer_cc_annuel_moyen - charges_annuelles
    den = get_frais_initiaux(cf_table)
    return round(100 * num / den, 2)


def get_rendement_net_net(revenus, charges, credit, cf_table):
    loyer_cc_annuel_moyen = get_loyer_cc_annuel_moyen(revenus)
    charges_annuelles = get_charges_annuelles(charges, cf_table)
    impot_annuel_moyen = get_impot_annuel_moyen(cf_table, credit)
    num = loyer_cc_annuel_moyen - charges_annuelles - impot_annuel_moyen
    den = get_frais_initiaux(cf_table)
    return round(100 * num / den, 2)


def get_rendement_net_net_net(revenus, charges, credit, cf_table):
    loyer_cc_annuel_moyen = get_loyer_cc_annuel_moyen(revenus)
    charges_annuelles = get_charges_annuelles(charges, cf_table)
    charges_credit_annuelles = get_charges_credit_annuelles(cf_table, credit)
    impot_annuel_moyen = get_impot_annuel_moyen(cf_table, credit)
    num = loyer_cc_annuel_moyen - charges_annuelles - impot_annuel_moyen - charges_credit_annuelles
    den = get_frais_initiaux(cf_table)
    return round(100 * num / den, 2)
    
def get_part_de_ma_poche(cf_table, prix_revente):
    total_paid = cf_table['TOTAL après impôts'].sum()
    return round(100 * total_paid / prix_revente, 2)
