import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from lib.rendement import get_rendement_brut, get_rendement_net, get_rendement_net_net, get_rendement_net_net_net, get_loyer_cc_annuel_moyen, get_charges_annuelles, get_charges_credit_annuelles, get_impot_annuel_moyen


def plot_yearly_cash_flow(cf_table, credit):
    fig = go.Figure()
    x_range = list(range(0, int(credit["duree"]) + 1))
    fig.add_trace(
        go.Bar(
            y=cf_table['TOTAL avant impôts'],
            x=x_range,
            name="Avant impôts",
            text="CF avant impôts",
            hoverinfo="y+text",
            marker=dict(line=dict(width=2)),
        )
    )
    fig.add_trace(
        go.Bar(
            y=cf_table['TOTAL après impôts'],
            x=x_range,
            name="Après impôts",
            text="CF après impôts",
            hoverinfo="y+text",
            marker=dict(line=dict(width=2)),
        )
    )
    fig.update_layout(
        showlegend=True,
        barmode="overlay",
        title_text="Cash Flow par an",
        title_x=0.5,
        title_y=0.85,
        xaxis_title="Année",
    )
    return fig


def plot_cumulated_cash_flow(cf_table):
    df_plot = cf_table.reset_index()
    df_plot['Cash Flow cumulé'] = df_plot['TOTAL après impôts'].cumsum()
    df_plot = df_plot.loc[df_plot['index'] != 'TOTAL']
    fig = px.line(df_plot, x="index", y="Cash Flow cumulé")
    fig.update_layout(
        showlegend=True,
        barmode="overlay",
        title_text="Cash Flow cumulé",
        title_x=0.5,
        title_y=1,
        xaxis_title="Année",
        yaxis_zeroline=True,
        yaxis_zerolinecolor='#d62728',
        yaxis_zerolinewidth=1,
    )
    return fig


def display_cash_flow(cf_table, credit, achat):
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> CF sur {credit['duree']} ans</p>",
        unsafe_allow_html=True,
    )
    col1.write(f"{int(cf_table.loc['TOTAL', 'TOTAL après impôts'])} €")
    col2.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> CF / an moyen</p>",
        unsafe_allow_html=True,
    )
    col2.write(f"{int((cf_table.loc['TOTAL', 'TOTAL après impôts'] - cf_table.loc['0', 'TOTAL après impôts']) / credit['duree']) } €")
    col3.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Apport initial</p>",
        unsafe_allow_html=True,
    )
    col3.write(f"{int(- cf_table.loc['0', 'TOTAL après impôts'])} €")
    col4.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Gain sur {credit['duree']} ans</p>",
        unsafe_allow_html=True,
    )
    col4.write(f"{int(cf_table.loc['TOTAL', 'TOTAL après impôts'] + achat['montant'] * 1000)} €")
    st.write("")


def display_rendement(revenus, charges, credit, cf_table, impots):
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Brut</p>",
        unsafe_allow_html=True,
    )
    col1.write(f"{get_rendement_brut(revenus, cf_table)}%")
    col2.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Net</p>",
        unsafe_allow_html=True,
    )
    col2.write(f"{get_rendement_net(revenus, charges, cf_table, impots, credit)}%")
    col3.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Net-net</p>",
        unsafe_allow_html=True,
    )
    col3.write(f"{get_rendement_net_net(revenus, charges, credit, cf_table, impots)}%")
    col4.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Net-net-net</p>",
        unsafe_allow_html=True,
    )
    col4.write(f"{get_rendement_net_net_net(revenus, charges, credit, cf_table, impots)}%")
    st.write("")


def plot_cash_flow_waterfall(cf_table, charges, revenus, credit, impots):

    # Calcul des différents composants
    loyer_cc_annuel_moyen = get_loyer_cc_annuel_moyen(revenus)
    charges_annuelles = - get_charges_annuelles(charges, cf_table, impots, credit)
    charges_credit_annuelles = - get_charges_credit_annuelles(cf_table, credit)
    impot_annuel_moyen = - get_impot_annuel_moyen(cf_table, credit)
    cf_annuel = loyer_cc_annuel_moyen + charges_annuelles + impot_annuel_moyen + charges_credit_annuelles

    # Waterfall
    names = ['Loyer HC', 'Charges', 'Impôts', 'Remboursement Crédit', 'CF annuel']
    values = [loyer_cc_annuel_moyen, charges_annuelles, impot_annuel_moyen, charges_credit_annuelles, cf_annuel]
    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative"] * 4 + ["total"],
            x=names,
            y=values,
            textposition="auto",
            text=["+" + str(int(x)) if x > 0 else "" + str(int(x)) for x in values],
            decreasing={"marker": {"color": "#ff0066"}},
            increasing={"marker": {"color": "#002244"}},
            totals={"marker": {"color": "#66cccc"}},
        )
    )
    fig.update_yaxes(title_text="Cash Flow (€)")
    fig.update_layout(
        title="Cash Flow annuel moyen",
        title_x=0.5,
        title_y=0.85,
    )
    return fig
