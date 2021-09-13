def get_rendement_brut(achat, revenus, charges):
    num = 100 * revenus["loyer_cc"] * 12
    den = 1000 * (achat["montant"] + charges["notaire"])
    return round(num / den, 2)


def get_rendement_net(achat, revenus, charges):
    rev = revenus["loyer_cc"] * 12
    cha = 1000 * (charges["copropriete"] + charges["taxe_fonciere"])
    num = 100 * (rev - cha)
    den = 1000 * (achat["montant"] + charges["notaire"])
    return round(num / den, 2)


def get_rendement_net_net():
    return 0
