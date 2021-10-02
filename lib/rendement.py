def get_rendement_brut(achat, revenus, charges):
    num = revenus["loyer_cc"] * 12
    den = 1000 * (achat["montant"] + charges["notaire"])
    return round(100 * num / den, 2)


def get_rendement_net(achat, revenus, charges):
    rev = revenus["loyer_cc"] * 12
    cha = 1000 * (charges["copropriete"] + charges["taxe_fonciere"])
    num = rev - cha
    den = 1000 * (achat["montant"] + charges["notaire"])
    return round(100 * num / den, 2)


def get_rendement_net_net():
    return 0


def get_part_de_ma_poche(cf_table, prix_revente):
    total_paid = cf_table['TOTAL après impôts'].sum()
    return round(100 * total_paid / prix_revente, 2)