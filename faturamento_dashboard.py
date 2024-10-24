import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Função para formatar moeda no padrão brasileiro
def formatar_moeda(valor):
    return f'R$ {valor:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

# Configurações de layout da página
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

# Dados de Faturamento e Compras
faturamento_data = {
    'Data': df_faturamento_cleaned['Data'],
    'Compras': df_faturamento_cleaned['Compras'],
    'Vendas': df_faturamento_cleaned['Vendas'],
    'Folha_Liquida': df_faturamento_cleaned['Folha_Liquida']
}

# Criando DataFrame para análise financeira
df_faturamento = pd.DataFrame(faturamento_data)

# Total de uso e consumo e ativo (apenas total no período)
despesa_uso_consumo = df_faturamento_cleaned['Mat_Uso_Consumo'].sum()  # Total no período
despesa_ativo = df_faturamento_cleaned['Compra_Ativo'].sum()  # Total no período

# Criando colunas para as comparações mensais (sem incluir uso e consumo/ativo)
df_faturamento['Despesas_Totais'] = df_faturamento['Compras'] + df_faturamento['Folha_Liquida']

# Adicionando valores de impostos ao DataFrame de faturamento
df_impostos_mes = df_impostos_cleaned.groupby(df_impostos_cleaned['Periodo'].dt.to_period('M')).sum().reset_index()
df_impostos_mes['Periodo'] = df_impostos_mes['Periodo'].dt.strftime('%m/%Y')

df_faturamento = df_faturamento.merge(df_impostos_mes, how='left', left_on=df_faturamento['Data'].dt.strftime('%m/%Y'), right_on='Periodo')
df_faturamento['Despesas_Totais_Completas'] = df_faturamento['Despesas_Totais'] + df_faturamento['Valor_Pagar']
df_faturamento['Resultado'] = df_faturamento['Vendas'] - df_faturamento['Despesas_Totais_Completas']

# Título e Introdução
st.title("\U0001F310 Dashboard Financeiro 2024")
st.markdown("""
### Visão consolidada das finanças da empresa para 2024
Análise de **vendas**, **compras**, **folha de pagamento**, e **impostos** no período.
As despesas totais **não incluem** os valores de uso e consumo e ativo, que serão destacados separadamente.
""")

# Seção de Métricas Principais
st.header('\U0001F4CA Resumo Financeiro')
total_vendas = df_faturamento['Vendas'].sum()
total_compras = df_faturamento['Compras'].sum()
total_folha = df_faturamento['Folha_Liquida'].sum()
total_impostos = df_faturamento['Valor_Pagar'].sum()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
col1.metric(label='Vendas Totais (Realizado)', value=formatar_moeda(total_vendas))
col2.metric(label='Compras Totais (Realizado)', value=formatar_moeda(total_compras))
col3.metric(label='Folha Líquida Total (Realizado)', value=formatar_moeda(total_folha))
col4.metric(label='Impostos Totais (Realizado)', value=formatar_moeda(total_impostos))

# Gráfico de Vendas vs Compras
st.header('\U0001F4C8 Comparação de Vendas e Compras (Realizado)')
fig1 = px.line(df_faturamento, x='Data', y=['Vendas', 'Compras'], title='Vendas e Compras Mensais', markers=True)
fig1.update_layout(yaxis_title='Valor (R$)', xaxis_title='Mês/Ano', legend_title_text='Categoria')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de barras comparando Receita e Despesas Totais (incluindo impostos)
st.header('\U0001F4C9 Receita vs Despesas Totais (Compras + Folha de Pagamento + Impostos)')
fig2 = go.Figure()

# Receita
fig2.add_trace(go.Bar(
    x=df_faturamento['Data'],
    y=df_faturamento['Vendas'],
    name='Vendas (Receita)',
    marker_color='rgb(26, 118, 255)'
))

# Despesas Totais (Compras + Folha + Impostos)
fig2.add_trace(go.Bar(
    x=df_faturamento['Data'],
    y=df_faturamento['Despesas_Totais_Completas'],
    name='Despesas Totais',
    marker_color='rgb(255, 99, 71)'
))

fig2.update_layout(barmode='group', xaxis_tickangle=-45, title="Receita vs Despesas Totais (Incluindo Impostos)")
st.plotly_chart(fig2, use_container_width=True)

# Gráfico comparando Receita vs DAS
st.header('\U0001F4B8 Comparativo Receita vs DAS')
df_faturamento['DAS'] = df_impostos_cleaned[df_impostos_cleaned['Historico'].str.contains('DAS', case=False)].groupby(df_impostos_cleaned['Periodo'].dt.to_period('M')).sum().reset_index()['Valor_Pagar']
fig3 = go.Figure()

# Receita
fig3.add_trace(go.Bar(
    x=df_faturamento['Data'],
    y=df_faturamento['Vendas'],
    name='Vendas (Receita)',
    marker_color='rgb(26, 118, 255)'
))

# DAS
fig3.add_trace(go.Bar(
    x=df_faturamento['Data'],
    y=df_faturamento['DAS'],
    name='DAS (Simples Nacional)',
    marker_color='rgb(255, 165, 0)'
))

fig3.update_layout(barmode='group', xaxis_tickangle=-45, title="Receita vs DAS")
st.plotly_chart(fig3, use_container_width=True)

# Análise de Resultados Mensais
st.header('\U0001F50D Análise de Resultados Mensais')
df_faturamento['Resultado_Status'] = df_faturamento['Resultado'].apply(lambda x: 'Positivo' if x >= 0 else 'Negativo')

st.dataframe(df_faturamento.style.format({
    'Vendas': 'R$ {:,.2f}',
    'Despesas_Totais_Completas': 'R$ {:,.2f}',
    'Resultado': 'R$ {:,.2f}'
}))

# Gráfico de linha para visualizar o saldo mensal (resultado)
st.header('\U0001F4C8 Resultado Mensal (Saldo)')
fig4 = px.line(df_faturamento, x='Data', y='Resultado', title='Resultado Mensal (Receitas - Despesas)', markers=True)
fig4.update_layout(yaxis_title='Saldo (R$)', xaxis_title='Mês/Ano')
st.plotly_chart(fig4, use_container_width=True)

# Exibindo os valores de Uso e Consumo e Ativo no final (sem incluir nas comparações)
st.header('\U0001F4E6 Despesas de Uso e Consumo e Ativo (Valor Total)')
st.markdown(f"""
**Despesas de Uso e Consumo:** {formatar_moeda(despesa_uso_consumo)} (Valor total no período).
**Despesas com Ativo:** {formatar_moeda(despesa_ativo)} (Valor total no período).

Esses valores **não estão incluídos** nas comparações mensais acima, pois são totais do período.
""")

# Conclusão
st.header('\U0001F4C1 Conclusão Geral')
st.markdown(f"""
As comparações mensais de receita e despesas incluem **vendas, compras, folha de pagamento e impostos**, enquanto as despesas de **uso e consumo** e **ativo** são valores totais e estão destacados separadamente.
Essa visão clara permite avaliar o impacto das despesas operacionais e financeiras da empresa ao longo do tempo.
""")