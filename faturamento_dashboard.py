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
fin_data['Período'] = pd.to_datetime(fin_data['Período'], format='%m/%Y')

# Calculando despesas totais
fin_data['Despesas Totais'] = fin_data[['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuição Assistencial', 'ISSQN Retido', 'COMPRAS', 'FOLHA LIQUIDA']].sum(axis=1)

# Calculando lucro/prejuízo
fin_data['Lucro/Prejuízo'] = fin_data['Vendas'] - fin_data['Despesas Totais']

# Configurando a página do Streamlit
st.set_page_config(page_title="Dashboard Financeiro Futurista", layout="wide")
st.title("🚀 Dashboard Financeiro Futurista ")
st.markdown("### Demonstração moderna e intuitiva das Receitas, Despesas e Lucros")

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
st.dataframe(fin_data)

# Resumo Geral
receita_total = fin_data['Vendas'].sum()
despesas_totais = fin_data['Despesas Totais'].sum()
lucro_prejuizo_total = receita_total - despesas_totais

st.markdown("### Resumo Financeiro Geral")
st.metric(label="Receita Total", value=f"R$ {receita_total:,.2f}")
st.metric(label="Despesas Totais", value=f"R$ {despesas_totais:,.2f}")
st.metric(label="Lucro/Prejuízo Total", value=f"R$ {lucro_prejuizo_total:,.2f}")

# Comentário final
st.markdown(
    "<div style='text-align: center; font-size: 24px;'>Este é apenas o começo do futuro financeiro da sua empresa!" \
    " Confie nos números e impulsione seu crescimento! 🌟</div>", unsafe_allow_html=True
)
