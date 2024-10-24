import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Função para formatar moeda no padrão brasileiro
def formatar_moeda(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Função para traduzir os meses para português manualmente
def traduzir_mes(mes_ano_str):
    meses_traducao = {
        'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'Mai', 'Jun': 'Jun',
        'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set', 'Oct': 'Out', 'Nov': 'Nov', 'Dec': 'Dez'
    }
    mes_abrev = mes_ano_str[:3]  # Pegando a abreviação do mês
    ano = mes_ano_str[4:]  # Pegando o ano
    return f"{meses_traducao.get(mes_abrev, mes_abrev)}/{ano}"

# Configurações de layout da página
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

# Dados embutidos diretamente no código (extraídos da sua planilha)
data = {
    'Data': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09'],
    'Compras': [105160.60, 107065.02, 64392.80, 120088.99, 124917.39, 89430.32, 115399.63, 81134.93, 72725.11],
    'Vendas': [79964.37, 105745.62, 127695.82, 41245.16, 69917.40, 105804.46, 151307.07, 112968.77, 142545.12],
    'Folha_Liquida': [11614.67, 11459.96, 11220.51, 11982.91, 12607.28, 11809.55, 12145.88, 12400.17, 13012.31],
    'Compra_Ativo': [0, 0, 0, 0, 0, 0, 0, 0, 0],  # Sem valores mensais, então zeramos
    'Mat_Uso_Consumo': [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Sem valores mensais, então zeramos
}

df_faturamento_cleaned = pd.DataFrame(data)

# Total de uso e consumo e ativo (apenas total no período)
despesa_uso_consumo = 15000.00  # Exemplo de total fornecido
despesa_ativo = 25000.00  # Exemplo de total fornecido

# Criando DataFrame de comparação (somente comparações mensais)
df_faturamento = pd.DataFrame({
    'Data': pd.to_datetime(df_faturamento_cleaned['Data'], format='%Y-%m'),
    'Compras': df_faturamento_cleaned['Compras'],
    'Vendas': df_faturamento_cleaned['Vendas'],
    'Folha_Liquida': df_faturamento_cleaned['Folha_Liquida']
})

# Criando colunas para as comparações mensais (sem incluir uso e consumo/ativo)
df_faturamento['Despesas_Totais'] = df_faturamento['Compras'] + df_faturamento['Folha_Liquida']
df_faturamento['Resultado'] = df_faturamento['Vendas'] - df_faturamento['Despesas_Totais']

# Título e Introdução
st.title("🌐 Dashboard Financeiro 2024")
st.markdown("""
### Visão consolidada das finanças da empresa para 2024
Análise de **vendas**, **compras**, **folha de pagamento** no período.
As despesas totais **não incluem** os valores de uso e consumo e ativo, que serão destacados separadamente.
""")

# Seção de Métricas Principais
st.header('📊 Resumo Financeiro')
total_vendas = df_faturamento['Vendas'].sum()
total_compras = df_faturamento['Compras'].sum()
total_folha = df_faturamento['Folha_Liquida'].sum()

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric(label='Vendas Totais (Realizado)', value=formatar_moeda(total_vendas))
col2.metric(label='Compras Totais (Realizado)', value=formatar_moeda(total_compras))
col3.metric(label='Folha Líquida Total (Realizado)', value=formatar_moeda(total_folha))

# Gráfico de Vendas vs Compras
st.header('📈 Comparação de Vendas e Compras (Realizado)')
fig1 = px.line(df_faturamento, x='Data', y=['Vendas', 'Compras'], title='Vendas e Compras Mensais', markers=True)
fig1.update_layout(yaxis_title='Valor (R$)', xaxis_title='Mês/Ano', legend_title_text='Categoria')
st.plotly_chart(fig1, use_container_width=True)

# Gráfico de barras comparando Receita e Despesas Totais (excluindo uso e consumo e ativo)
st.header('💡 Receita vs Despesas Totais (Compras + Folha de Pagamento)')
fig2 = go.Figure()

# Receita
fig2.add_trace(go.Bar(
    x=df_faturamento['Data'],
    y=df_faturamento['Vendas'],
    name='Vendas (Receita)',
    marker_color='rgb(26, 118, 255)'
))

# Despesas Totais (Compras + Folha)
fig2.add_trace(go.Bar(
    x=df_faturamento['Data'],
    y=df_faturamento['Despesas_Totais'],
    name='Despesas Totais',
    marker_color='rgb(255, 99, 71)'
))

fig2.update_layout(barmode='group', xaxis_tickangle=-45, title="Receita vs Despesas Totais (Sem Uso e Consumo/Ativo)")
st.plotly_chart(fig2, use_container_width=True)

# Análise de Resultados Mensais
st.header('🔍 Análise de Resultados Mensais')
df_faturamento['Resultado_Status'] = df_faturamento['Resultado'].apply(lambda x: 'Positivo' if x >= 0 else 'Negativo')

st.dataframe(df_faturamento.style.format({
    'Vendas': 'R$ {:,.2f}',
    'Despesas_Totais': 'R$ {:,.2f}',
    'Resultado': 'R$ {:,.2f}'
}))

# Gráfico de linha para visualizar o saldo mensal (resultado)
st.header('📊 Resultado Mensal (Saldo)')
fig3 = px.line(df_faturamento, x='Data', y='Resultado', title='Resultado Mensal (Receitas - Despesas)', markers=True)
fig3.update_layout(yaxis_title='Saldo (R$)', xaxis_title='Mês/Ano')
st.plotly_chart(fig3, use_container_width=True)

# Exibindo os valores de Uso e Consumo e Ativo no final (sem incluir nas comparações)
st.header('📦 Despesas de Uso e Consumo e Ativo (Valor Total)')
st.markdown(f"""
**Despesas de Uso e Consumo:** {formatar_moeda(despesa_uso_consumo)} (Valor total no período).
**Despesas com Ativo:** {formatar_moeda(despesa_ativo)} (Valor total no período).

Esses valores **não estão incluídos** nas comparações mensais acima, pois são totais do período.
""")

# Conclusão
st.header('📈 Conclusão Geral')
st.markdown(f"""
As comparações mensais de receita e despesas incluem **vendas, compras e folha de pagamento**, enquanto as despesas de **uso e consumo** e **ativo** são valores totais e estão destacados separadamente.
Essa visão clara permite avaliar o impacto das despesas operacionais e financeiras da empresa ao longo do tempo.
""")
