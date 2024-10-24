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

# Dados de Impostos
dados_impostos = {
    'Periodo': [
        '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09'
    ],
    'Historico': [
        'IRPJ', 'Cofins', 'ICMS', 'ISS', 'IRPJ', 'Cofins', 'ICMS', 'ISS', 'IRPJ'
    ],
    'Valor_Pagar': [
        2021.90, 1468.94, 283.65, 6806.03, 14.25, 2457.80, 3405.67, 3987.55, 1821.75
    ]
}

# Criando DataFrames
df_faturamento = pd.DataFrame(dados_faturamento)
df_impostos = pd.DataFrame(dados_impostos)

# Convertendo a coluna "Data" para o tipo datetime
df_faturamento['Data'] = pd.to_datetime(df_faturamento['Data'])
df_impostos['Periodo'] = pd.to_datetime(df_impostos['Periodo'], format='%Y-%m')

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

col1, col2, col3, col4 = st.columns(4)
col1.metric(label='Total Vendas (Jan-Set)', value=formatar_moeda(total_vendas))
col2.metric(label='Total Compras (Jan-Set)', value=formatar_moeda(total_compras))
col3.metric(label='Folha Líquida (Jan-Set)', value=formatar_moeda(total_folha))
col4.metric(label='Total Impostos (Jan-Set)', value=formatar_moeda(total_impostos))

# Revenue vs Purchases Chart
st.header('Vendas vs Compras (Mensal)')
faturamento_monthly = df_faturamento.groupby(df_faturamento['Data'].dt.to_period('M')).agg({'Compras': 'sum', 'Vendas': 'sum'}).reset_index()
faturamento_monthly['Data'] = faturamento_monthly['Data'].dt.to_timestamp()

# Map months to Portuguese manually
month_map = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
    7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}
faturamento_monthly['Data'] = faturamento_monthly['Data'].apply(lambda x: f"{month_map[x.month]} de {x.year}")

fig1 = px.line(faturamento_monthly, x='Data', y=['Compras', 'Vendas'], title='Compras e Vendas ao longo do tempo', markers=True)
fig1.update_layout(yaxis_title='Valor (R$)', xaxis_title='Mês', legend_title_text='Categoria')
st.plotly_chart(fig1, use_container_width=True)

# Tax Payments by Type
st.header('Pagamentos de Impostos (Detalhado)')
df_impostos['Periodo'] = df_impostos['Periodo'].apply(lambda x: f"{month_map[x.month]} de {x.year}")
fig2 = px.bar(df_impostos, x='Periodo', y='Valor_Pagar', color='Historico', title='Pagamentos de Impostos por Tipo', labels={'Valor_Pagar': 'Valor (R$)'})
fig2.update_layout(barmode='stack', xaxis_title='Mês', yaxis_title='Total Pago (R$)')
st.plotly_chart(fig2, use_container_width=True)

# Detailed Tables (Optional Section)
with st.expander('Ver Tabelas Detalhadas'):
    st.subheader('Dados de Faturamento')
    df_faturamento['Data'] = df_faturamento['Data'].dt.strftime('%d/%m/%Y')
    st.dataframe(df_faturamento.style.format({'Compras': 'R$ {:,.2f}', 'Vendas': 'R$ {:,.2f}', 'Folha_Liquida': 'R$ {:,.2f}'}))
    st.subheader('Dados de Impostos')
    st.dataframe(df_impostos.style.format({'Valor_Pagar': 'R$ {:,.2f}'}))

# Summary & Conclusion
st.header('Resumo e Conclusão')
st.markdown("""
Podemos observar que as vendas tiveram um comportamento de crescimento variável ao longo dos meses, enquanto os custos com compras e folha líquida permaneceram relativamente constantes. O total de impostos pagos apresenta uma boa visão dos principais custos tributários, que podem ser utilizados para planejar ações fiscais e otimizar o fluxo de caixa.

A partir deste dashboard, os stakeholders da empresa podem identificar padrões, áreas de alta despesa, e oportunidades de otimização financeira. 
""")

# Footer
st.markdown("Criado com ❤️ utilizando Python e Streamlit para uma análise financeira clara e poderosa.")