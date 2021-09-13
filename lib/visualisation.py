import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from lib.rendement import get_rendement_brut, get_rendement_net, get_rendement_net_net


def plot_yearly_cash_flow(cf_table, credit):
    fig = go.Figure()
    x_range = list(range(0, credit["duree"] + 1))
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


def display_cash_flow(cf_table, credit):
    col1, col2, col3 = st.columns(3)
    col1.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Cash Flow sur {credit['duree']} ans</p>",
        unsafe_allow_html=True,
    )
    col1.write(f"{int(cf_table.loc['TOTAL', 'TOTAL après impôts'])} €")
    col2.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Cash Flow / an moyen</p>",
        unsafe_allow_html=True,
    )
    col2.write(f"{int((int(cf_table.loc['TOTAL', 'TOTAL après impôts']) - int(cf_table.loc['0', 'TOTAL après impôts'])) / credit['duree']) } €")
    col3.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Apport initial</p>",
        unsafe_allow_html=True,
    )
    col3.write(f"{int(- cf_table.loc['0', 'TOTAL après impôts'])} €")
    st.write("")


def display_rendement(achat, revenus, charges):
    col1, col2, col3 = st.columns(3)
    col1.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Rendement brut</p>",
        unsafe_allow_html=True,
    )
    col1.write(f"{get_rendement_brut(achat, revenus, charges)}%")
    col2.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Rendement net</p>",
        unsafe_allow_html=True,
    )
    col2.write(f"{get_rendement_net(achat, revenus, charges)}%")
    col3.markdown(
        f"<p style='color: #ff0066; "
        f"font-weight: bold; font-size: 20px;'> Rendement net-net</p>",
        unsafe_allow_html=True,
    )
    col3.write(f"{get_rendement_net_net()}%")
    st.write("")
