import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load data (use your files here)
faturamento_file = 'Faturamento e Compras 01a092024.xlsx'
impostos_file = 'RelacaoImpostos01a092024.xlsx'

# Load and clean the Faturamento data
faturamento_df = pd.read_excel(faturamento_file, sheet_name='Faturamento', header=3)
faturamento_df.columns = ['Data', 'Compras', 'Vendas', 'Folha_Liquida', 'Compra_Ativo', 'Mat_Uso_Consumo']
faturamento_df['Data'] = pd.to_datetime(faturamento_df['Data'], errors='coerce')
faturamento_df.dropna(subset=['Data'], inplace=True)

# Load and clean the Impostos data
impostos_df = pd.read_excel(impostos_file, sheet_name='RelacaoImpostos')
impostos_df.columns = ['Ignored', 'Periodo', 'Codigo', 'Historico', 'Valor_Pagar']
impostos_df['Periodo'] = pd.to_datetime(impostos_df['Periodo'], errors='coerce')
impostos_df.dropna(subset=['Periodo'], inplace=True)
impostos_df_grouped = impostos_df.groupby([impostos_df['Periodo'].dt.to_period('M'), 'Historico'])['Valor_Pagar'].sum().reset_index()
impostos_df_grouped['Periodo'] = impostos_df_grouped['Periodo'].dt.to_timestamp()

# Streamlit layout
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

# Title and introduction
st.title("Dashboard Financeiro 2024")
st.markdown("""
Uma visão abrangente das finanças da empresa para o período de janeiro a setembro de 2024. O dashboard visa fornecer insights rápidos sobre receitas, despesas e custos relacionados a impostos, garantindo uma visão clara e poderosa do status da empresa.
""")

# Metrics Section
st.header('Principais Métricas Financeiras')
total_vendas = faturamento_df['Vendas'].sum()
total_compras = faturamento_df['Compras'].sum()
total_folha = faturamento_df['Folha_Liquida'].sum()
total_impostos = impostos_df['Valor_Pagar'].sum()

# Format values to Brazilian Real manually
col1, col2, col3, col4 = st.columns(4)
col1.metric(label='Total Vendas (Jan-Set)', value=f"R$ {total_vendas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col2.metric(label='Total Compras (Jan-Set)', value=f"R$ {total_compras:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col3.metric(label='Folha Líquida (Jan-Set)', value=f"R$ {total_folha:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
col4.metric(label='Total Impostos (Jan-Set)', value=f"R$ {total_impostos:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Revenue vs Purchases Chart
st.header('Vendas vs Compras (Mensal)')
faturamento_monthly = faturamento_df.groupby(faturamento_df['Data'].dt.to_period('M')).agg({'Compras': 'sum', 'Vendas': 'sum'}).reset_index()
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
impostos_df_grouped['Periodo'] = impostos_df_grouped['Periodo'].apply(lambda x: f"{month_map[x.month]} de {x.year}")
fig2 = px.bar(impostos_df_grouped, x='Periodo', y='Valor_Pagar', color='Historico', title='Pagamentos de Impostos por Tipo', labels={'Valor_Pagar': 'Valor (R$)'})
fig2.update_layout(barmode='stack', xaxis_title='Mês', yaxis_title='Total Pago (R$)')
st.plotly_chart(fig2, use_container_width=True)

# Detailed Tables (Optional Section)
with st.expander('Ver Tabelas Detalhadas'):
    st.subheader('Dados de Faturamento')
    faturamento_df['Data'] = faturamento_df['Data'].dt.strftime('%d/%m/%Y')
    st.dataframe(faturamento_df.style.format({'Compras': 'R$ {:,.2f}', 'Vendas': 'R$ {:,.2f}', 'Folha_Liquida': 'R$ {:,.2f}', 'Compra_Ativo': 'R$ {:,.2f}', 'Mat_Uso_Consumo': 'R$ {:,.2f}'}))
    st.subheader('Dados de Impostos')
    st.dataframe(impostos_df_grouped.style.format({'Total_Valor_Pagar': 'R$ {:,.2f}'}))

# Summary & Conclusion
st.header('Resumo e Conclusão')
st.markdown("""
Podemos observar que as vendas tiveram um comportamento de crescimento variável ao longo dos meses, enquanto os custos com compras e folha líquida permaneceram relativamente constantes. O total de impostos pagos apresenta uma boa visão dos principais custos tributários, que podem ser utilizados para planejar ações fiscais e otimizar o fluxo de caixa.

A partir deste dashboard, os stakeholders da empresa podem identificar padrões, áreas de alta despesa, e oportunidades de otimização financeira. 
""")

# Footer
st.markdown("Criado com ❤️ utilizando Python e Streamlit para uma análise financeira clara e poderosa.")