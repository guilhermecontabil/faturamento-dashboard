# Parte 1 - Configurações Iniciais e Métricas Principais

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale

# Função para formatar moeda no padrão brasileiro
def formatar_moeda(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# Configurando locale para português brasileiro
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Configurações de layout da página
st.set_page_config(layout='wide', page_title='Dashboard Financeiro 2024', page_icon=':bar_chart:')

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
# Continuando a Parte 2 - Gráfico de Linha com Resultado Mensal

# Gráfico de linha para visualizar o saldo mensal (resultado)
st.header('📊 Resultado Mensal (Saldo)')
fig3 = px.line(df_resultado, x='Data', y='Resultado', title='Resultado Mensal (Receitas - Despesas)', markers=True)
fig3.update_layout(yaxis_title='Saldo (R$)', xaxis_title='Mês/Ano')
st.plotly_chart(fig3, use_container_width=True)

# Valores Totais de Uso e Consumo e Ativo
despesa_uso_consumo = 15000.00  # Valor total no período de despesas de uso e consumo
despesa_ativo = 25000.00  # Valor total no período de despesas com ativo

# Atualizando as despesas totais com esses valores
df_comparacao['Despesas_Totais_Completas'] = df_comparacao['Despesas_Totais'] + (despesa_uso_consumo / len(df_comparacao)) + (despesa_ativo / len(df_comparacao))

# Seção de Destaque para Uso e Consumo e Ativo
st.header('📦 Despesas de Uso e Consumo e Ativo (Valor Total)')
st.markdown(f"""
As despesas de **uso e consumo** somam um total de **{formatar_moeda(despesa_uso_consumo)}** e as despesas com **ativos** somam **{formatar_moeda(despesa_ativo)}** no período.
Esses valores estão inclusos na demonstração das **despesas totais** e **resultado**.
""")

# Exibindo a tabela atualizada com as novas despesas
df_resultado_completo = df_comparacao[['Data', 'Vendas', 'Despesas_Totais_Completas', 'Resultado']]
df_resultado_completo['Resultado_Status'] = df_resultado_completo['Resultado'].apply(lambda x: 'Positivo' if x >= 0 else 'Negativo')

st.dataframe(df_resultado_completo.style.format({
    'Vendas': 'R$ {:,.2f}',
    'Despesas_Totais_Completas': 'R$ {:,.2f}',
    'Resultado': 'R$ {:,.2f}'
}))

# Atualizando gráfico com despesas totais completas
st.header('📊 Resultado Mensal (Incluindo Uso e Consumo e Ativo)')
fig4 = px.line(df_resultado_completo, x='Data', y='Resultado', title='Resultado Mensal Completo (Receitas - Despesas Totais)', markers=True)
fig4.update_layout(yaxis_title='Saldo (R$)', xaxis_title='Mês/Ano')
st.plotly_chart(fig4, use_container_width=True)
# Parte 3 - Tabelas Detalhadas e Conclusão

# Meses em português para o DataFrame
df_comparacao['Data'] = pd.to_datetime(df_comparacao['Data'], format='%Y-%m').dt.strftime('%b/%Y')

# Tabelas de Impostos
st.header('📄 Tabelas Detalhadas de Impostos e Receitas')
st.subheader('Dados de Impostos por Categoria')
st.dataframe(df_impostos.style.format({
    'DAS_Simples': 'R$ {:,.2f}',
    'FGTS': 'R$ {:,.2f}',
    'DCTFWEB': 'R$ {:,.2f}',
    'ISSQN': 'R$ {:,.2f}'
}))

# Tabelas de Receitas, Despesas e Salários
st.subheader('Receitas, Despesas e Folha de Pagamento')
st.dataframe(df_faturamento.style.format({
    'Compras': 'R$ {:,.2f}',
    'Vendas': 'R$ {:,.2f}',
    'Folha_Liquida': 'R$ {:,.2f}'
}))

# Conclusão Final
st.header('📈 Conclusão Geral')
st.markdown(f"""
Com a inclusão das despesas de **uso e consumo** no valor de **{formatar_moeda(despesa_uso_consumo)}** e as despesas de **ativo** no valor de **{formatar_moeda(despesa_ativo)}**, 
foi possível realizar uma análise completa do fluxo de caixa da empresa. As tabelas detalhadas, juntamente com os gráficos, permitem uma avaliação clara do saldo mensal e do impacto total das despesas sobre as receitas.
Essa visão consolidada é essencial para tomar decisões estratégicas e ajustar o planejamento financeiro da empresa.
""")
