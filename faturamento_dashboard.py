import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Função para formatar moeda no padrão brasileiro
def formatar_moeda(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Dados de Faturamento e Compras
dados_faturamento = {
    'Data': [
        '2024-01', '2024-02', '2024-03', '2024-04',
        '2024-05', '2024-06', '2024-07', '2024-08', '2024-09'
    ],
    'Compras': [
        105160.60, 107065.02, 64392.80, 120088.99,
        124917.39, 89430.32, 115399.63, 81134.93, 72725.11
    ],
    'Vendas': [
        79964.37, 105745.62, 127695.82, 41245.16,
        69917.40, 105804.46, 151307.07, 112968.77, 142545.12
    ],
    'Folha_Liquida': [
        11614.67, 11459.96, 11220.51, 11982.91,
        12607.28, 11809.55, 12145.88, 12400.17, 13012.31
    ]
}

# Dados de Impostos separados por categoria
dados_impostos = {
    'Periodo': [
        '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
        '2024-07', '2024-08', '2024-09'
    ],
    'DAS_Simples': [
        6806.03, 9021.59, 10990.54, 3594.41, 6007.22, 7688.00,
        9800.00, 11200.00, 8200.00
    ],
    'FGTS': [
        1468.94, 1224.44, 1141.97, 1310.92, 1389.34, 1576.45,
        1650.78, 1487.36, 1412.00
    ],
    'Darf': [
        2021.90, 1682.27, 1702.63, 1715.30, 1779.19, 1855.00,
        1915.43, 1745.00, 1600.50
    ],
    'ISSQN': [
        283.65, 226.58, 228.81, 259.75, 228.44, 290.60,
        314.35, 276.90, 245.80
    ]
}

# Criando DataFrames
df_faturamento = pd.DataFrame(dados_faturamento)
df_impostos = pd.DataFrame(dados_impostos)

# Unindo os dados de faturamento e impostos
df_comparacao = pd.merge(df_faturamento, df_impostos, left_on='Data', right_on='Periodo', how='left')
df_comparacao['Proporcao_DAS_Receita'] = (df_comparacao['DAS_Simples'] / df_comparacao['Vendas']) * 100

# Layout da página no Streamlit
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

# Título e Introdução
st.title("🌐 Dashboard Financeiro 2024")
st.markdown("""
### Visão consolidada das finanças da empresa para 2024
Essa dashboard apresenta uma análise detalhada de **vendas**, **compras**, **folha de pagamento** e as diferentes categorias de impostos.
""")

# Seção de Métricas Principais
st.header('📊 Resumo Financeiro')
total_vendas = df_faturamento['Vendas'].sum()
total_compras = df_faturamento['Compras'].sum()
total_folha = df_faturamento['Folha_Liquida'].sum()
total_das = df_impostos['DAS_Simples'].sum()
total_fgts = df_impostos['FGTS'].sum()
total_darf = df_impostos['Darf'].sum()
total_issqn = df_impostos['ISSQN'].sum()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
col1.metric(label='Vendas Totais', value=formatar_moeda(total_vendas))
col2.metric(label='Compras Totais', value=formatar_moeda(total_compras))
col3.metric(label='Folha Líquida Total', value=formatar_moeda(total_folha))
col4.metric(label='DAS Simples (Total)', value=formatar_moeda(total_das))

# Gráfico de Vendas vs Compras
st.header('📈 Tendência de Vendas e Compras')
fig1 = px.line(df_faturamento, x='Data', y=['Vendas', 'Compras'], title='Vendas e Compras Mensais', markers=True)
fig1.update_layout(yaxis_title='Valor (R$)', xaxis_title='Mês/Ano', legend_title_text='Categoria')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico Receita vs DAS Simples
st.header('💡 Receita vs DAS Simples')
fig2 = go.Figure()

# Receita
fig2.add_trace(go.Bar(
    x=df_comparacao['Data'],
    y=df_comparacao['Vendas'],
    name='Vendas',
    marker_color='rgb(26, 118, 255)'
))

# DAS Simples
fig2.add_trace(go.Bar(
    x=df_comparacao['Data'],
    y=df_comparacao['DAS_Simples'],
    name='DAS Simples',
    marker_color='rgb(55, 83, 109)'
))

fig2.update_layout(barmode='group', xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

# Gráfico de Proporção de DAS sobre Vendas
st.header('⚖️ Proporção de DAS Simples sobre Vendas')
fig3 = px.pie(df_comparacao, names='Data', values='Proporcao_DAS_Receita', title='Proporção de DAS sobre Vendas (%)')
st.plotly_chart(fig3, use_container_width=True)

# Gráficos para cada categoria de imposto
st.header('📊 Impostos Detalhados')

# Gráfico de FGTS
st.subheader('FGTS Mensal')
fig_fgts = px.bar(df_impostos, x='Periodo', y='FGTS', title='FGTS Mensal')
st.plotly_chart(fig_fgts, use_container_width=True)

# Gráfico de DARF
st.subheader('DARF Mensal')
fig_darf = px.bar(df_impostos, x='Periodo', y='Darf', title='DARF Mensal')
st.plotly_chart(fig_darf, use_container_width=True)

# Gráfico de ISSQN
st.subheader('ISSQN Mensal')
fig_issqn = px.bar(df_impostos, x='Periodo', y='ISSQN', title='ISSQN Mensal')
st.plotly_chart(fig_issqn, use_container_width=True)

# Tabelas Detalhadas
st.header('📄 Tabelas Detalhadas')

# Tabela Faturamento e Compras
st.subheader('Dados de Faturamento, Compras e Folha')
st.dataframe(df_faturamento.style.format({
    'Compras': 'R$ {:,.2f}',
    'Vendas': 'R$ {:,.2f}',
    'Folha_Liquida': 'R$ {:,.2f}'
}))

# Tabela de Impostos por Categoria
st.subheader('Dados de Impostos por Categoria')
st.dataframe(df_impostos.style.format({
    'DAS_Simples': 'R$ {:,.2f}',
    'FGTS': 'R$ {:,.2f}',
    'Darf': 'R$ {:,.2f}',
    'ISSQN': 'R$ {:,.2f}'
}))

# Resumo Final
st.header('📈 Conclusão')
st.markdown("""
A análise detalha as tendências de **vendas e compras**, além de exibir as informações separadas por **categorias de impostos** como **DAS Simples**, **FGTS**, **DARF** e **ISSQN**. Isso proporciona uma visão clara para tomada de decisões estratégicas.
""")
