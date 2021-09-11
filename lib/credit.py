from immo_tools import calculator


def get_loan_schedule(credit):

    # Get loan schedule
    loan = calculator.build_loan(
        duration=credit["duree"]*12,
        amount=credit["montant"]*1000,
        year_rate=credit["taux_interet"],
        insurance_rate=credit["taux_assurance"],
        build_summary=True,
        duration_unit='month')
    schedule = loan.summary

    # Formatting
    schedule = loan.summary.groupby('annees').agg({
        'refunded_cap': 'sum',
        'interset': 'sum',
        'assur tot': 'sum'
    }).reset_index()
    schedule.columns = ['Année', 'Capital', 'Intérêt', 'Assurance Crédit']
    schedule = schedule.set_index('Année')
    for col in schedule.columns:
        schedule[col] = - round(schedule[col], 0)

    return schedule


