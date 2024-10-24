import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurações básicas da página
st.set_page_config(
    page_title="Dashboard Financeira",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carregar os dados já processados
df_faturamento = pd.read_csv('faturamento_compras.csv')  # Substitua pelos seus dados
df_impostos = pd.read_csv('impostos.csv')  # Substitua pelos seus dados

# Título da Dashboard
st.title("💼 Dashboard Financeira - 2024")

# Métricas Resumo
st.header("📊 Resumo Financeiro Mensal")
col1, col2, col3, col4 = st.columns(4)

# Métricas simples como cards
with col1:
    st.metric("Vendas Totais", f"R$ {df_faturamento['Vendas'].sum():,.2f}")
with col2:
    st.metric("Compras Totais", f"R$ {df_faturamento['Compras'].sum():,.2f}")
with col3:
    st.metric("Folha Líquida Total", f"R$ {df_faturamento['Folha Líquida'].sum():,.2f}")
with col4:
    st.metric("Impostos Pagos", f"R$ {df_impostos.sum().sum():,.2f}")

# Gráficos de Tendência
st.header("📈 Gráficos de Tendência")

# Gráfico de Vendas e Compras ao longo do tempo
fig_vendas_compras = px.line(df_faturamento, x='Data', y=['Vendas', 'Compras'], 
                             title="Vendas e Compras Mensais", 
                             labels={'value': 'Valor (R$)', 'Data': 'Mês'})
st.plotly_chart(fig_vendas_compras, use_container_width=True)

# Gráfico de Impostos por Categoria
st.header("💸 Impostos Pagos por Categoria")
fig_impostos = go.Figure()

for imposto in df_impostos.columns[1:]:
    fig_impostos.add_trace(go.Bar(x=df_impostos['Periodo'], y=df_impostos[imposto], name=imposto))

fig_impostos.update_layout(barmode='stack', title='Impostos Pagos de Janeiro a Setembro de 2024',
                           xaxis_title='Período', yaxis_title='Valor (R$)')
st.plotly_chart(fig_impostos, use_container_width=True)

# Proporção de Despesas e Receitas
st.header("⚖️ Proporção entre Vendas, Compras, Folha e Impostos")

totais = {
    'Vendas': df_faturamento['Vendas'].sum(),
    'Compras': df_faturamento['Compras'].sum(),
    'Folha Líquida': df_faturamento['Folha Líquida'].sum(),
    'Impostos': df_impostos.sum().sum()
}

fig_pizza = px.pie(names=totais.keys(), values=totais.values(), title='Proporção Financeira')

st.plotly_chart(fig_pizza, use_container_width=True)

# Filtro de detalhes por mês
st.sidebar.header("Filtros Interativos")
mes_selecionado = st.sidebar.selectbox("Selecione o mês", df_faturamento['Data'].unique())

# Filtra os dados
dados_filtrados = df_faturamento[df_faturamento['Data'] == mes_selecionado]
st.sidebar.write("Dados do mês selecionado:", dados_filtrados)
