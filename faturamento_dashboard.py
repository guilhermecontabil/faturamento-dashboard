import streamlit as st
import pandas as pd
import plotly.express as px

# Função para formatar moeda no padrão brasileiro
def formatar_moeda(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Dados do Faturamento
data = {
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
    ]
}

# Criando o DataFrame
df = pd.DataFrame(data)

# Convertendo a coluna "Data" para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Criando uma coluna formatada para exibição com o mês e o ano em português
meses_traducao = {
    'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'Mai',
    'Jun': 'Jun', 'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set', 'Oct': 'Out',
    'Nov': 'Nov', 'Dec': 'Dez'
}
df['Data_Exibicao'] = df['Data'].dt.strftime('%b %Y').replace(meses_traducao, regex=True)

# Definindo cores para os gráficos
cores = ['silver', 'green']  # 'silver' para Compras e 'green' para Vendas

# Título do Dashboard
st.title('Dashboard Interativo - Faturamento da Empresa')

# Seção 1: Compras ao longo do tempo
st.header('Compras ao Longo do Tempo')
fig_compras = px.line(df, x='Data_Exibicao', y='Compras', title='Compras Mensais', markers=True, color_discrete_sequence=['silver'])
st.plotly_chart(fig_compras)

# Seção 2: Vendas ao longo do tempo
st.header('Vendas ao Longo do Tempo')
fig_vendas = px.line(df, x='Data_Exibicao', y='Vendas', title='Vendas Mensais', markers=True, color_discrete_sequence=['green'])
st.plotly_chart(fig_vendas)

# Seção 3: Comparação entre Compras e Vendas
st.header('Comparação de Compras e Vendas')
fig_comparacao = px.bar(df, x='Data_Exibicao', y=['Compras', 'Vendas'], barmode='group', title='Compras vs Vendas', color_discrete_sequence=cores)
st.plotly_chart(fig_comparacao)

# Seção 4: Resumo Estatístico Explicado
st.header('Resumo Estatístico Explicado')

# Resumo Estatístico Original
st.subheader("Dados Resumidos:")
st.write(df.describe())

# Explicação das Métricas
st.subheader("Explicação das Métricas Estatísticas:")
st.markdown("""
- **count**: Número de registros (quantidade de entradas de dados).
- **mean**: Média dos valores.
- **std**: Desvio padrão, mostra o quanto os valores variam em relação à média.
- **min**: Valor mínimo da série de dados.
- **25%**: Primeiro quartil, 25% dos valores são menores ou iguais a este valor.
- **50%**: Mediana, metade dos valores são menores ou iguais a este valor.
- **75%**: Terceiro quartil, 75% dos valores são menores ou iguais a este valor.
- **max**: Valor máximo da série de dados.
""")

# Seção 5: Análise de Desempenho
st.header('Análise de Desempenho')
total_compras = df['Compras'].sum()
total_vendas = df['Vendas'].sum()

# Formatando os valores como moeda brasileira
total_compras_formatado = formatar_moeda(total_compras)
total_vendas_formatado = formatar_moeda(total_vendas)

st.metric("Total de Compras", total_compras_formatado)
st.metric("Total de Vendas", total_vendas_formatado)

if total_vendas > total_compras:
    st.success("Parabéns! O total de vendas é maior do que o total de compras.")
else:
    st.warning("Atenção: As vendas são menores que as compras.")

# Seção 6: Adicionar Filtro por Data (Opcional)
st.header('Filtrar por Data')
start_date = st.date_input('Data Inicial', df['Data'].min())
end_date = st.date_input('Data Final', df['Data'].max())

if start_date <= end_date:
    filtered_df = df[(df['Data'] >= start_date) & (df['Data'] <= end_date)]
    st.write("Dados Filtrados:")

    # Aplicar formatação ao DataFrame filtrado
    filtered_df_formatado = filtered_df.copy()
    filtered_df_formatado['Compras'] = filtered_df_formatado['Compras'].apply(formatar_moeda)
    filtered_df_formatado['Vendas'] = filtered_df_formatado['Vendas'].apply(formatar_moeda)
    st.write(filtered_df_formatado[['Data_Exibicao', 'Compras', 'Vendas']])

    # Atualizar Gráficos com Filtro
    st.subheader('Gráficos Atualizados')
    fig_compras_filtered = px.line(filtered_df, x='Data_Exibicao', y='Compras', title='Compras Mensais Filtradas', markers=True, color_discrete_sequence=['silver'])
    st.plotly_chart(fig_compras_filtered)

    fig_vendas_filtered = px.line(filtered_df, x='Data_Exibicao', y='Vendas', title='Vendas Mensais Filtradas', markers=True, color_discrete_sequence=['green'])
    st.plotly_chart(fig_vendas_filtered)

    fig_comparacao_filtered = px.bar(filtered_df, x='Data_Exibicao', y=['Compras', 'Vendas'], barmode='group', title='Compras vs Vendas (Filtrado)', color_discrete_sequence=cores)
    st.plotly_chart(fig_comparacao_filtered)
else:
    st.error('A data final deve ser posterior à data inicial.')