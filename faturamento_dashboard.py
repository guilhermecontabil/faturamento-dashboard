import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Dados fornecidos pelo arquivo Excel atualizado (de Janeiro/2024 a Setembro/2024)
dados = {
    'Período': ['01/2024', '02/2024', '03/2024', '04/2024', '05/2024', '06/2024', '07/2024', '08/2024', '09/2024'],
    'Darf DctfWeb': [2021.90, 1682.27, 1702.63, 1715.30, 1779.19, 1934.75, 2436.78, 2586.50, 2676.25],
    'DAS': [6806.03, 9021.59, 10990.54, 3594.41, 6007.22, 9074.02, 13103.30, 9876.06, 12417.05],
    'FGTS': [1468.94, 1224.44, 1141.97, 1310.92, 1389.34, 1455.73, 1692.25, 2018.08, 1752.26],
    'Contribuicao_Assistencial': [283.65, 226.58, 228.81, 259.75, 228.44, 244.08, 275.39, 352.60, 383.91],
    'ISSQN Retido': [14.25, 10.40, 11.60, 7.68, 13.02, 11.29, 16.82, 12.40, 14.27],
    'COMPRAS': [105160.60, 107065.02, 64392.80, 120088.99, 124917.39, 89307.32, 115399.63, 105061.49, 72725.11],
    'Vendas': [79964.37, 105745.62, 127695.82, 41245.16, 69917.40, 105804.46, 151307.07, 112968.77, 142545.12],
    'Folha_Liquida': [11614.67, 11459.96, 11220.51, 11982.91, 12607.28, 14409.63, 12659.46, 19565.77, 16131.06]
}

# Criando DataFrame
fin_data = pd.DataFrame(dados)
fin_data['Período'] = pd.to_datetime(fin_data['Período'], format='%m/%Y').dt.strftime('%m/%Y')

# Calculando despesas totais
fin_data['Despesas Totais'] = fin_data[['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuicao_Assistencial', 'ISSQN Retido', 'COMPRAS', 'Folha_Liquida']].sum(axis=1)

# Calculando lucro/prejuízo
fin_data['Lucro/Prejuízo'] = fin_data['Vendas'] - fin_data['Despesas Totais']

# Configurando a página do Streamlit
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("Dashboard Financeiro")
st.markdown("### Visão Geral das Receitas, Despesas e Lucros")

# Período da Análise
st.markdown(f"Período da análise: {fin_data['Período'].min()} a {fin_data['Período'].max()}")

# Resumo Geral no topo usando cards estilizados
with st.container():
    st.markdown("#### Resumo Financeiro Geral")
    st.markdown(
        "<style>"
        "div[data-testid='metric-container'] {"
        "    background-color: #f0f2f6;"
        "    border: 1px solid #e1e1e1;"
        "    padding: 10px;"
        "    border-radius: 10px;"
        "    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);"
        "    margin-bottom: 10px;"
        "}"
        "div[data-testid='metric-container'] > div {"
        "    overflow-wrap: break-word;"
        "    font-family: 'Arial', sans-serif;"
        "    font-weight: bold;"
        "}"
        "</style>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="large")
    col1.metric(label="Receita Total", value=f"R$ {fin_data['Vendas'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col2.metric(label="Despesas Totais", value=f"R$ {fin_data['Despesas Totais'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col3.metric(label="Lucro/Prejuízo Total", value=f"R$ {fin_data['Lucro/Prejuízo'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Indicadores Detalhados em Seção Separada e Estilizada
st.markdown("#### Indicadores Detalhados")
with st.container():
    col4, col5, col6, col7, col8 = st.columns(5, gap="large")
    col4.metric(label="Total Vendas", value=f"R$ {fin_data['Vendas'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col5.metric(label="Total Compras", value=f"R$ {fin_data['COMPRAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col6.metric(label="Total Salários", value=f"R$ {fin_data['Folha_Liquida'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col7.metric(label="Total DAS", value=f"R$ {fin_data['DAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col8.metric(label="Total DCTFWeb", value=f"R$ {fin_data['Darf DctfWeb'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Receita x Compras
grafico_receita_compras = px.line(
    fin_data, x='Período', y=['Vendas', 'COMPRAS'],
    labels={"value": "Valores em R$", "Período": "Mês/Ano"},
    title="Comparativo de Receitas vs Compras"
)
grafico_receita_compras.update_layout(template="plotly_dark", title_font_size=20)
st.plotly_chart(grafico_receita_compras, use_container_width=True)

# Receita x Imposto DAS
grafico_receita_das = px.bar(
    fin_data, x='Período', y=['Vendas', 'DAS'],
    barmode='group',
    labels={"value": "Valores em R$", "Período": "Mês/Ano"},
    title="Receitas vs DAS (Imposto)"
)
grafico_receita_das.update_layout(template="plotly_white", title_font_size=20)
st.plotly_chart(grafico_receita_das, use_container_width=True)

# Receita Total vs Despesas Totais
grafico_receita_despesas = go.Figure()
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Vendas'],
                                              mode='lines+markers', name='Receita Total',
                                              line=dict(width=3)))
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Despesas Totais'],
                                              mode='lines+markers', name='Despesas Totais',
                                              line=dict(width=3, dash='dash')))
grafico_receita_despesas.update_layout(
    title="Receita Total vs Despesas Totais",
    xaxis_title="Mês/Ano",
    yaxis_title="Valores em R$",
    template="plotly_dark",
    title_font_size=20
)
st.plotly_chart(grafico_receita_despesas, use_container_width=True)

# Gráfico sugestivo: Análise de Lucro/Prejuízo
grafico_lucro_prejuizo = px.area(
    fin_data, x='Período', y='Lucro/Preju
