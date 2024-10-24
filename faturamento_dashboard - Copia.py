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
        '2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01',
        '2024-05-01', '2024-06-01', '2024-07-01', '2024-08-01', '2024-09-01'
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

# Dados de Impostos
dados_impostos = {
    'Periodo': [
        '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
        '2024-07', '2024-08', '2024-09'
    ],
    'DAS_Simples': [
        6806.03, 9021.59, 10990.54, 3594.41, 6007.22, 7688.00,
        9800.00, 11200.00, 8200.00
    ],
    'Outros_Impostos': [
        3774.49, 3163.71, 3744.60, 4075.97, 4989.19, 5901.58,
        5046.25, 3774.49, 3163.71
    ]
}

# Criando DataFrames
df_faturamento = pd.DataFrame(dados_faturamento)
df_impostos = pd.DataFrame(dados_impostos)

# Convertendo a coluna "Data" para o tipo datetime e formatando para mês/ano
df_faturamento['Data'] = pd.to_datetime(df_faturamento['Data'], errors='coerce').dt.to_period('M').dt.strftime('%m/%Y')
df_impostos['Periodo'] = pd.to_datetime(df_impostos['Periodo'], format='%Y-%m').dt.to_period('M').dt.strftime('%m/%Y')

# Unindo os dados de faturamento e impostos
df_comparacao = pd.merge(df_faturamento, df_impostos, left_on='Data', right_on='Periodo', how='left')
df_comparacao['Proporcao_DAS_Receita'] = (df_comparacao['DAS_Simples'] / df_comparacao['Vendas']) * 100

# Layout da página no Streamlit
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

# Título e Introdução
st.title("Dashboard Financeiro 2024")
st.markdown("""
Uma visão abrangente das finanças da empresa para o período de janeiro a setembro de 2024. 
Essa dashboard oferece insights rápidos sobre receitas, despesas e custos com impostos, auxiliando no planejamento estratégico e análise financeira.
""")

# Seção de Métricas Principais
st.header('Principais Métricas Financeiras')
total_vendas = df_faturamento['Vendas'].sum()
total_compras = df_faturamento['Compras'].sum()
total_folha = df_faturamento['Folha_Liquida'].sum()
total_das = df_impostos['DAS_Simples'].sum()
total_outros_impostos = df_impostos['Outros_Impostos'].sum()
total_impostos = total_das + total_outros_impostos

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label='Total Vendas (Jan-Set)', value=formatar_moeda(total_vendas))
col2.metric(label='Total Compras (Jan-Set)', value=formatar_moeda(total_compras))
col3.metric(label='Folha Líquida (Jan-Set)', value=formatar_moeda(total_folha))
col4.metric(label='Total Impostos (Jan-Set)', value=formatar_moeda(total_impostos))
col5.metric(label='Total DAS Simples (Jan-Set)', value=formatar_moeda(total_das))

# Gráfico Vendas vs Compras
st.header('Vendas vs Compras (Mensal)')
fig1 = px.line(df_faturamento, x='Data', y=['Vendas', 'Compras'], title='Vendas e Compras Mensais', markers=True)
fig1.update_layout(yaxis_title='Valor (R$)', xaxis_title='Mês/Ano', legend_title_text='Categoria')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico Receita vs DAS Simples
st.header('Comparação entre Receita do Mês e DAS Simples')
fig2 = px.bar(df_comparacao, x='Data', y=['Vendas', 'DAS_Simples'], barmode='group', title='Receita vs DAS Simples', labels={'value': 'Valor (R$)', 'variable': 'Categoria'})
fig2.update_layout(xaxis_title='Mês/Ano', yaxis_title='Valor (R$)')
st.plotly_chart(fig2, use_container_width=True)

# Gráfico Outros Impostos
st.header('Outros Impostos Pagos (Mensal)')
fig3 = px.bar(df_comparacao, x='Data', y='Outros_Impostos', title='Outros Impostos Pagos Mensalmente', labels={'Outros_Impostos': 'Valor Pago (R$)'})
fig3.update_layout(xaxis_title='Mês/Ano', yaxis_title='Total Pago (R$)')
st.plotly_chart(fig3, use_container_width=True)

# Tabelas Detalhadas
st.header('Tabelas Detalhadas')
st.subheader('Dados de Faturamento, Compras e Folha')
st.dataframe(df_faturamento.style.format({'Compras': 'R$ {:,.2f}', 'Vendas': 'R$ {:,.2f}', 'Folha_Liquida': 'R$ {:,.2f}'}))

st.subheader('Dados de Impostos - DAS Simples e Outros Impostos')
st.dataframe(df_impostos.style.format({'DAS_Simples': 'R$ {:,.2f}', 'Outros_Impostos': 'R$ {:,.2f}'}))

# Resumo e Conclusão
st.header('Resumo e Conclusão')
st.markdown("""
O dashboard mostra que a empresa teve uma variação significativa nas vendas ao longo dos meses, enquanto os impostos, incluindo o DAS Simples, tiveram um impacto considerável nas finanças. 
Esses dados são fundamentais para otimizar o planejamento tributário e a gestão do fluxo de caixa.
""")