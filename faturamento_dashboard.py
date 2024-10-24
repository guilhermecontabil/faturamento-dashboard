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

# Dicionário para tradução de meses
meses_traducao = {
    'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'Mai',
    'Jun': 'Jun', 'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set', 'Oct': 'Out',
    'Nov': 'Nov', 'Dec': 'Dez'
}

# Convertendo a coluna "Data" para o tipo datetime e formatando para mês/ano
df['Data'] = pd.to_datetime(df['Data']).dt.strftime('%b %Y')  # Primeiro formata para 'Jan 2024', etc.
df['Data'] = df['Data'].replace(meses_traducao, regex=True)  # Depois traduz os meses para português

# Definindo cores para os gráficos
cores = ['silver', 'green']  # 'silver' para Compras e 'green' para Vendas

# Título do Dashboard
st.title('Dashboard Interativo - Faturamento da Empresa')

# Seção 1: Compras ao longo do tempo
st.header('Compras ao Longo do Tempo')
fig_compras = px.line(df, x='Data', y='Compras', title='Compras Mensais', markers=True, color_discrete_sequence=['silver'])
st.plotly_chart(fig_compras)

# Seção 2: Vendas ao longo do tempo
st.header('Vendas ao Longo do Tempo')
fig_vendas = px.line(df, x='Data', y='Vendas', title='Vendas Mensais', markers=True, color_discrete_sequence=['green'])
st.plotly_chart(fig_vendas)

# Seção 3: Comparação entre Compras e Vendas
st.header('Comparação de Compras e Vendas')
fig_comparacao = px.bar(df, x='Data', y=['Compras', 'Vendas'], barmode='group', title='Compras vs Vendas', color_discrete_sequence=cores)
st.plotly_chart(fig_comparacao)

# Seção 4: Resumo Estatístico
st.header('Resumo Estatístico')

# Criar uma cópia do DataFrame para formatação
df_formatado = df.copy()

# Aplicar a função de formatação a cada coluna numérica
df_formatado['Compras'] = df_formatado['Compras'].apply(formatar_moeda)
df_formatado['Vendas'] = df_formatado['Vendas'].apply(formatar_moeda)

# Mostrar o DataFrame formatado no dashboard
st.write(df_formatado)

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
start_date = st.date_input('Data Inicial', pd.to_datetime(df['Data']).min())
end_date = st.date_input('Data Final', pd.to_datetime(df['Data']).max())

if start_date <= end_date:
    filtered_df = df[(pd.to_datetime(df['Data']) >= pd.to_datetime(start_date)) & (pd.to_datetime(df['Data']) <= pd.to_datetime(end_date))]
    st.write("Dados Filtrados:")

    # Aplicar formatação ao DataFrame filtrado
    filtered_df_formatado = filtered_df.copy()
    filtered_df_formatado['Compras'] = filtered_df_formatado['Compras'].apply(formatar_moeda)
    filtered_df_formatado['Vendas'] = filtered_df_formatado['Vendas'].apply(formatar_moeda)
    st.write(filtered_df_formatado)

    # Atualizar Gráficos com Filtro
    st.subheader('Gráficos Atualizados')
    fig_compras_filtered = px.line(filtered_df, x='Data', y='Compras', title='Compras Mensais Filtradas', markers=True, color_discrete_sequence=['silver'])
    st.plotly_chart(fig_compras_filtered)

    fig_vendas_filtered = px.line(filtered_df, x='Data', y='Vendas', title='Vendas Mensais Filtradas', markers=True, color_discrete_sequence=['green'])
    st.plotly_chart(fig_vendas_filtered)

    fig_comparacao_filtered = px.bar(filtered_df, x='Data', y=['Compras', 'Vendas'], barmode='group', title='Compras vs Vendas (Filtrado)', color_discrete_sequence=cores)
    st.plotly_chart(fig_comparacao_filtered)
else:
    st.error('A data final deve ser posterior à data inicial.')