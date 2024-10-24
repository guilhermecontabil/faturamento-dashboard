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

# Dados de Impostos (incluindo o DCTFWEB e outros impostos)
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
    'DCTFWEB': [
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

# Layout da página no Streamlit
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

# Título e Introdução
st.title("🌐 Dashboard Financeiro 2024")
st.markdown("""
### Visão consolidada das finanças da empresa para 2024
Apresentamos uma visão detalhada dos **valores realizados** para vendas, compras e folha de pagamento, junto com uma análise das categorias de impostos.
""")

# Seção de Métricas Principais
st.header('📊 Resumo Financeiro')
total_vendas = df_faturamento['Vendas'].sum()
total_compras = df_faturamento['Compras'].sum()
total_folha = df_faturamento['Folha_Liquida'].sum()
total_das = df_impostos['DAS_Simples'].sum()
total_fgts = df_impostos['FGTS'].sum()
total_dctfweb = df_impostos['DCTFWEB'].sum()
total_issqn = df_impostos['ISSQN'].sum()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
col1.metric(label='Vendas Totais (Realizado)', value=formatar_moeda(total_vendas))
col2.metric(label='Compras Totais (Realizado)', value=formatar_moeda(total_compras))
col3.metric(label='Folha Líquida Total (Realizado)', value=formatar_moeda(total_folha))
col4.metric(label='DAS Simples Total', value=formatar_moeda(total_das))

# Gráfico de Vendas vs Compras
st.header('📈 Comparação de Vendas e Compras (Realizado)')
fig1 = px.line(df_faturamento, x='Data', y=['Vendas', 'Compras'], title='Valores Realizados de Vendas e Compras', markers=True)
fig1.update_layout(yaxis_title='Valor (R$)', xaxis_title='Mês/Ano', legend_title_text='Categoria')
st.plotly_chart(fig1, use_container_width=True)

# Focar no total de impostos e compras em relação às receitas
st.header('📉 Comparação de Receitas com Despesas')

# Criando uma coluna que mostra o total de despesas (compras + folha + impostos)
df_comparacao['Despesas_Totais'] = df_comparacao['Compras'] + df_comparacao['Folha_Liquida'] + df_comparacao['DAS_Simples'] + df_comparacao['FGTS'] + df_comparacao['DCTFWEB'] + df_comparacao['ISSQN']
df_comparacao['Resultado'] = df_comparacao['Vendas'] - df_comparacao['Despesas_Totais']

# Gráfico de barras comparando Receita e Despesas
st.header('💡 Receita vs Despesas Totais (Compras + Folha + Impostos)')
fig3 = go.Figure()

# Receita
fig3.add_trace(go.Bar(
    x=df_comparacao['Data'],
    y=df_comparacao['Vendas'],
    name='Vendas (Receita)',
    marker_color='rgb(26, 118, 255)'
))

# Despesas Totais
fig3.add_trace(go.Bar(
    x=df_comparacao['Data'],
    y=df_comparacao['Despesas_Totais'],
    name='Despesas Totais',
    marker_color='rgb(255, 99, 71)'
))

fig3.update_layout(barmode='group', xaxis_tickangle=-45, title="Receita vs Despesas")
st.plotly_chart(fig3, use_container_width=True)

# Análise de Resultado
st.header('🔍 Análise de Resultados')

# Exibindo a tabela com os resultados mensais
df_resultado = df_comparacao[['Data', 'Vendas', 'Despesas_Totais', 'Resultado']]
df_resultado['Resultado_Status'] = df_resultado['Resultado'].apply(lambda x: 'Positivo' if x >= 0 else 'Negativo')

st.markdown("""
Abaixo está a análise de resultados mensais, mostrando se as receitas foram suficientes para cobrir as despesas. 
Um **resultado positivo** indica que as receitas superaram as despesas, enquanto um **resultado negativo** indica um déficit.
""")
st.dataframe(df_resultado.style.format({'Vendas': 'R$ {:,.2f}', 'Despesas_Totais': 'R$ {:,.2f}', 'Resultado': 'R$ {:,.2f}'}))

# Gráfico de linha para visualizar o saldo mensal (resultado)
st.header('📊 Resultado Mensal (Saldo)')
fig4 = px.line(df_resultado, x='Data', y='Resultado', title='Resultado Mensal (Receitas - Despesas)', markers=True)
fig4.update_layout(yaxis_title='Saldo (R$)', xaxis_title='Mês/Ano')
st.plotly_chart(fig4, use_container_width=True)

# Conclusão Final
st.header('📈 Conclusão')
st.markdown("""
Nesta análise, foi possível identificar se a empresa teve um resultado positivo ou negativo em cada mês.
Os gráficos e tabelas indicam como as receitas e despesas totais se comportaram, ajudando a identificar eventuais déficits.
Essa informação pode ser usada para tomar decisões estratégicas visando otimizar o fluxo de caixa e melhorar a lucratividade.
""")
