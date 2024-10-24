import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Função para formatar moeda no padrão brasileiro
def formatar_moeda(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Dados de Faturamento e Compras (substituindo a necessidade de arquivos externos)
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

# Dados de Impostos (incluindo o DAS e outros impostos)
dados_impostos = {
    'Periodo': [
        '2024-01', '2024-01', '2024-01', '2024-01', '2024-02', '2024-02', '2024-02', '2024-02', '2024-03',
        '2024-03', '2024-03', '2024-04', '2024-04', '2024-04', '2024-05', '2024-05', '2024-06', '2024-06',
        '2024-06', '2024-07', '2024-07', '2024-08', '2024-08', '2024-09'
    ],
    'Historico': [
        'DAS - Doc de Arrecadação do Simples Nacional', 'FGTS', 'Darf DctfWeb', 'Contribuição Assistencial',
        'DAS - Doc de Arrecadação do Simples Nacional', 'FGTS', 'Darf DctfWeb', 'Contribuição Assistencial',
        'DAS - Doc de Arrecadação do Simples Nacional', 'FGTS', 'ISSQN Retido', 'DAS - Doc de Arrecadação do Simples Nacional',
        'ISSQN Retido', 'Darf DctfWeb', 'DAS - Doc de Arrecadação do Simples Nacional', 'FGTS',
        'DAS - Doc de Arrecadação do Simples Nacional', 'ISSQN Retido', 'Contribuição Assistencial',
        'DAS - Doc de Arrecadação do Simples Nacional', 'FGTS', 'DAS - Doc de Arrecadação do Simples Nacional',
        'ISSQN Retido', 'DAS - Doc de Arrecadação do Simples Nacional'
    ],
    'Valor_Pagar': [
        6806.03, 1468.94, 2021.90, 283.65, 9021.59, 1754.43, 2457.80, 226.58,
        10990.54, 1800.00, 340.00, 3594.41, 120.00, 1980.00, 6007.22, 1600.00,
        7688.00, 130.00, 220.00, 9800.00, 1700.00, 11200.00, 140.00, 8200.00
    ]
}

# Criando DataFrames
df_faturamento = pd.DataFrame(dados_faturamento)
df_impostos = pd.DataFrame(dados_impostos)

# Convertendo a coluna "Data" para o tipo datetime e formatando para mês/ano
df_faturamento['Data'] = pd.to_datetime(df_faturamento['Data'], errors='coerce').dt.to_period('M').dt.strftime('%m/%Y')
df_impostos['Periodo'] = pd.to_datetime(df_impostos['Periodo'], format='%Y-%m').dt.to_period('M').dt.strftime('%m/%Y')

# Filtrando os registros de impostos relacionados ao DAS
df_das = df_impostos[df_impostos['Historico'].str.contains('DAS', case=False, na=False)].copy()

# Ajustar o período para o primeiro dia do mês para alinhamento com os dados de faturamento
df_das['Periodo_Mes'] = df_das['Periodo']

# Agrupando por mês para obter o total do DAS pago em cada mês
df_das_mensal = df_das.groupby('Periodo_Mes')['Valor_Pagar'].sum().reset_index()
df_das_mensal.columns = ['Data', 'DAS_Simples']

# Unindo com o dataframe de faturamento para realizar a comparação entre receita e DAS pago
df_comparacao = pd.merge(df_faturamento, df_das_mensal, left_on='Data', right_on='Data', how='left')

# Preencher valores NaN do DAS como zero, onde não houve pagamento registrado
df_comparacao['DAS_Simples'].fillna(0, inplace=True)

# Calculando a proporção de DAS sobre Vendas (Receita)
df_comparacao['Proporcao_DAS_Receita'] = (df_comparacao['DAS_Simples'] / df_comparacao['Vendas']) * 100

# Agrupando os outros impostos por tipo e por mês
df_outros_impostos = df_impostos[~df_impostos['Historico'].str.contains('DAS', case=False, na=False)].copy()
df_outros_impostos['Periodo_Mes'] = df_outros_impostos['Periodo']
df_outros_impostos_mensal = df_outros_impostos.groupby(['Periodo_Mes', 'Historico'])['Valor_Pagar'].sum().reset_index()
df_outros_impostos_mensal.columns = ['Data', 'Historico', 'Valor_Pago']

# Streamlit layout
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

# Title and introduction
st.title("Dashboard Financeiro 2024")
st.markdown("""
Uma visão abrangente das finanças da empresa para o período de janeiro a setembro de 2024. O dashboard visa fornecer insights rápidos sobre receitas, despesas e custos relacionados a impostos, garantindo uma visão clara e poderosa do status da empresa.
""")

# Metrics Section
st.header('Principais Métricas Financeiras')
total_vendas = df_faturamento['Vendas'].sum()
total_compras = df_faturamento['Compras'].sum()
total_folha = df_faturamento['Folha_Liquida'].sum()
total_impostos = df_impostos['Valor_Pagar'].sum()

total_das = df_das_mensal['DAS_Simples'].sum()
total_outros_impostos = total_impostos - total_das

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label='Total Vendas (Jan-Set)', value=formatar_moeda(total_vendas))
col2.metric(label='Total Compras (Jan-Set)', value=formatar_moeda(total_compras))
col3.metric(label='Folha Líquida (Jan-Set)', value=formatar_moeda(total_folha))
col4.metric(label='Total Impostos (Jan-Set)', value=formatar_moeda(total_impostos))
col5.metric(label='Total DAS Simples (Jan-Set)', value=formatar_moeda(total_das))

# Revenue vs Purchases Chart
st.header('Vendas vs Compras (Mensal)')
faturamento_monthly = df_faturamento.groupby(df_faturamento['Data']).agg({'Compras': 'sum', 'Vendas': 'sum'}).reset_index()

fig1 = px.line(faturamento_monthly, x='Data', y=['Compras', 'Vendas'], title='Compras e Vendas ao longo do tempo', markers=True)
fig1.update_layout(yaxis_title='Valor (R$)', xaxis_title='Mês/Ano', legend_title_text='Categoria')
st.plotly_chart(fig1, use_container_width=True)

# DAS vs Receita Chart
st.header('Comparação entre Receita do Mês e DAS Simples')
fig2 = px.bar(df_comparacao, x='Data', y=['Vendas', 'DAS_Simples'], barmode='group', title='Receita vs DAS Simples', labels={'value': 'Valor (R$)', 'variable': 'Categoria'})
fig2.update_layout(xaxis_title='Mês/Ano', yaxis_title='Valor (R$)')
st.plotly_chart(fig2, use_container_width=True)

# Outros Impostos
st.header('Outros Impostos Pagos (Mensal por Tipo)')
fig3 = px.bar(df_outros_impostos_mensal, x='Data', y='Valor_Pago', color='Historico', title='Outros Impostos por Tipo', labels={'Valor_Pago': 'Valor (R$)'})
fig3.update_layout(barmode='stack', xaxis_title='Mês/Ano', yaxis_title='Total Pago (R$)')
st.plotly_chart(fig3, use_container_width=True)

# Detailed Tables Section
st.header('Tabelas Detalhadas')

st.subheader('Dados de Faturamento/Compras/Folha')
st.dataframe(df_faturamento.style.format({'Compras': 'R$ {:,.2f}', 'Vendas': 'R$ {:,.2f}', 'Folha_Liquida': 'R$ {:,.2f}'}))

st.subheader('Dados de Impostos - DAS Simples e Outros Impostos')
st.dataframe(df_impostos.style.format({'Valor_Pagar': 'R$ {:,.2f}'}))

st.subheader('Outros Impostos por Mês e Tipo')
st.dataframe(df_outros_impostos_mensal.style.format({'Valor_Pago': 'R$ {:,.2f}'}))

# Summary & Conclusion
st.header('Resumo e Conclusão')
st.markdown("""
Podemos observar que as vendas tiveram um comportamento de crescimento variável ao longo dos meses, enquanto os custos com compras e folha líquida permaneceram relativamente constantes. O total de impostos pagos apresenta uma boa visão dos principais custos tributários, que podem ser utilizados para planejar ações fiscais e otimizar o fluxo de caixa.

A partir deste dashboard, os stakeholders da empresa podem identificar padrões, áreas de alta despesa, e oportunidades de otimização financeira. 
""")

# Footer
st.markdown("Criado com ❤️ utilizando Python e Streamlit para uma análise financeira clara e poderosa.")