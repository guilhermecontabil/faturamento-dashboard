import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Dados embutidos no código, baseados no arquivo fornecido
# (Os dados são apenas para simulação e análise do dashboard)
dados = {
    'Período': ['01/2024', '02/2024', '03/2024', '04/2024', '05/2024', '06/2024', '07/2024', '08/2024', '09/2024'],
    'Darf DctfWeb': [2021.90, 1682.27, 1702.63, 1715.30, 1779.19, 1800.00, 1820.00, 1850.00, 1900.00],
    'DAS': [6806.03, 9021.59, 10990.54, 3594.41, 6007.22, 6500.00, 6700.00, 7000.00, 7200.00],
    'FGTS': [1468.94, 1224.44, 1141.97, 1310.92, 1389.34, 1400.00, 1450.00, 1500.00, 1550.00],
    'Contribuição Assistencial': [283.65, 226.58, 228.81, 259.75, 228.44, 230.00, 235.00, 240.00, 245.00],
    'ISSQN Retido': [14.25, 10.40, 11.60, 7.68, 13.02, 13.50, 14.00, 15.00, 16.00],
    'COMPRAS': [105160.60, 107065.02, 64392.80, 120088.99, 124917.39, 130000.00, 135000.00, 140000.00, 145000.00],
    'Vendas': [79964.37, 105745.62, 127695.82, 41245.16, 69917.40, 75000.00, 80000.00, 85000.00, 90000.00],
    'FOLHA LIQUIDA': [11614.67, 11459.96, 11220.51, 11982.91, 12607.28, 13000.00, 13500.00, 14000.00, 14500.00]
}

# Criando DataFrame
fin_data = pd.DataFrame(dados)
fin_data['Período'] = pd.to_datetime(fin_data['Período'], format='%m/%Y').dt.strftime('%m/%Y')

# Calculando despesas totais
fin_data['Despesas Totais'] = fin_data[['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuição Assistencial', 'ISSQN Retido', 'COMPRAS', 'FOLHA LIQUIDA']].sum(axis=1)

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
    st.markdown(
        "<div style='display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;'>"
        "<div style='background-color: #f8f9fa; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); flex: 1; min-width: 200px; text-align: center;'>"
        f"<h4>Total Vendas</h4><h3>R$ {fin_data['Vendas'].sum():,.2f}</h3>"
        "</div>"
        "<div style='background-color: #f8f9fa; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); flex: 1; min-width: 200px; text-align: center;'>"
        f"<h4>Total Compras</h4><h3>R$ {fin_data['COMPRAS'].sum():,.2f}</h3>"
        "</div>"
        "<div style='background-color: #f8f9fa; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); flex: 1; min-width: 200px; text-align: center;'>"
        f"<h4>Total Salários</h4><h3>R$ {fin_data['FOLHA LIQUIDA'].sum():,.2f}</h3>"
        "</div>"
        "<div style='background-color: #f8f9fa; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); flex: 1; min-width: 200px; text-align: center;'>"
        f"<h4>Total DAS</h4><h3>R$ {fin_data['DAS'].sum():,.2f}</h3>"
        "</div>"
        "<div style='background-color: #f8f9fa; padding: 20px; border-radius: 15px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); flex: 1; min-width: 200px; text-align: center;'>"
        f"<h4>Total DCTFWeb</h4><h3>R$ {fin_data['Darf DctfWeb'].sum():,.2f}</h3>"
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )

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
    fin_data, x='Período', y='Lucro/Prejuízo',
    labels={"Lucro/Prejuízo": "Valores em R$", "Período": "Mês/Ano"},
    title="Análise de Lucro/Prejuízo Mensal"
)
grafico_lucro_prejuizo.update_layout(template="plotly", title_font_size=20)
st.plotly_chart(grafico_lucro_prejuizo, use_container_width=True)

# Tabela Interativa para Consulta
st.markdown("### Tabela Interativa para Consulta de Dados Financeiros")
# Adicionando linha de totalização na tabela
fin_data_display = fin_data.copy()
colunas_monetarias = ['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuição Assistencial', 'ISSQN Retido', 'COMPRAS', 'Vendas', 'FOLHA LIQUIDA', 'Despesas Totais', 'Lucro/Prejuízo']
for coluna in colunas_monetarias:
    fin_data_display[coluna] = fin_data_display[coluna].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Adicionando uma linha de totais na tabela
totais = {
    'Período': 'Totais',
    'Darf DctfWeb': f"R$ {fin_data['Darf DctfWeb'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'DAS': f"R$ {fin_data['DAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'FGTS': f"R$ {fin_data['FGTS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Contribuição Assistencial': f"R$ {fin_data['Contribuição Assistencial'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'ISSQN Retido': f"R$ {fin_data['ISSQN Retido'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'COMPRAS': f"R$ {fin_data['COMPRAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Vendas': f"R$ {fin_data['Vendas'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'FOLHA LIQUIDA': f"R$ {fin_data['FOLHA LIQUIDA'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Despesas Totais': f"R$ {fin_data['Despesas Totais'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Lucro/Prejuízo': f"R$ {fin_data['Lucro/Prejuízo'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
}
fin_data_display = pd.concat([fin_data_display, pd.DataFrame([totais])], ignore_index=True)

st.dataframe(fin_data_display)

# Outras Despesas Não Registradas na Planilha
st.markdown("### Outras Despesas Não Registradas na Planilha")
st.markdown("Essas despesas não estão incluídas nas demonstrações acima.")
st.markdown("- COMPRA ATIVO: R$ 78.390,94")
st.markdown("- MAT USO CONSUMO: R$ 31.785,62")

# Comentário final
st.markdown(
    "<div style='text-align: center; font-size: 24px;'>Confie nos números e impulsione o crescimento da sua empresa!</div>", unsafe_allow_html=True
)
