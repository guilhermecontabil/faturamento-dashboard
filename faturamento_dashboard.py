import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Dados embutidos no código, baseados no arquivo fornecido
# (Os dados são apenas para simulação e análise do dashboard)
dados = {
    'Período': ['01/2024', '02/2024', '03/2024', '04/2024', '05/2024'],
    'Darf DctfWeb': [2021.90, 1682.27, 1702.63, 1715.30, 1779.19],
    'DAS': [6806.03, 9021.59, 10990.54, 3594.41, 6007.22],
    'FGTS': [1468.94, 1224.44, 1141.97, 1310.92, 1389.34],
    'Contribuição Assistencial': [283.65, 226.58, 228.81, 259.75, 228.44],
    'ISSQN Retido': [14.25, 10.40, 11.60, 7.68, 13.02],
    'COMPRAS': [105160.60, 107065.02, 64392.80, 120088.99, 124917.39],
    'Vendas': [79964.37, 105745.62, 127695.82, 41245.16, 69917.40],
    'FOLHA LIQUIDA': [11614.67, 11459.96, 11220.51, 11982.91, 12607.28]
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

# Resumo Geral no topo (como cartões)
receita_total = fin_data['Vendas'].sum()
despesas_totais = fin_data['Despesas Totais'].sum()
lucro_prejuizo_total = receita_total - despesas_totais

col1, col2, col3 = st.columns(3)
col1.metric(label="Receita Total", value=f"R$ {receita_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col2.metric(label="Despesas Totais", value=f"R$ {despesas_totais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col3.metric(label="Lucro/Prejuízo Total", value=f"R$ {lucro_prejuizo_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Cartões adicionais para Vendas, Compras, Salários, DAS e DCTFWeb
total_vendas = fin_data['Vendas'].sum()
total_compras = fin_data['COMPRAS'].sum()
total_salarios = fin_data['FOLHA LIQUIDA'].sum()
total_das = fin_data['DAS'].sum()
total_dctfweb = fin_data['Darf DctfWeb'].sum()

col4, col5, col6, col7, col8 = st.columns(5)
col4.metric(label="Total Vendas", value=f"R$ {total_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col5.metric(label="Total Compras", value=f"R$ {total_compras:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col6.metric(label="Total Salários", value=f"R$ {total_salarios:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col7.metric(label="Total DAS", value=f"R$ {total_das:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col8.metric(label="Total DCTFWeb", value=f"R$ {total_dctfweb:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

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
# Formatando os valores monetários para Real Brasileiro (R$)
fin_data_display = fin_data.copy()
colunas_monetarias = ['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuição Assistencial', 'ISSQN Retido', 'COMPRAS', 'Vendas', 'FOLHA LIQUIDA', 'Despesas Totais', 'Lucro/Prejuízo']
for coluna in colunas_monetarias:
    fin_data_display[coluna] = fin_data_display[coluna].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

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
