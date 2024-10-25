import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Dados fornecidos pelo arquivo Excel atualizado (de Janeiro/2024 a Setembro/2024)
dados = {
    'Período': ['01/2024', '02/2024', '03/2024', '04/2024', '05/2024', '06/2024', '07/2024', '08/2024', '09/2024'],
    'Darf DctfWeb': [2021.90, 1682.27, 1702.63, 1715.30, 1779.19, 1934.75, 2436.78, 2586.50, 2676.25],
    'DAS': [6806.03, 9021.59, 10990.54, 3594.41, 6007.22, 9074.02, 13103.30, 9876.06, 12417.05],
    'FGTS': [1468.94, 1224.44, 1141.97, 1310.92, 1389.34, 1455.73, 1692.25, 2018.08, 1752.26],
    'Contribuicao_Assistencial': [283.65, 226.58, 228.81, 259.75, 228.44, 244.08, 275.39, 352.60, 383.91],
    'ISSQN Retido': [14.25, 10.40, 11.60, 7.68, 13.02, 11.29, 16.82, 12.40, 14.27],
    'COMPRAS': [105160.60, 107065.02, 64392.80, 120088.99, 124917.39, 89307.32, 115399.63, 105061.49, 72725.11],
    'Vendas': [79964.37, 105745.62, 127695.82, 41245.16, 69917.40, 105804.46, 151307.07, 112968.77, 142545.12],
    'Folha_Liquida': [11614.67, 11459.96, 11220.51, 11982.91, 12607.28, 14409.63, 12659.46, 19565.77, 16131.06]
}

# Criando DataFrame
fin_data = pd.DataFrame(dados)
fin_data['Período'] = pd.to_datetime(fin_data['Período'], format='%m/%Y').dt.strftime('%m/%Y')

# Calculando despesas totais
fin_data['Despesas Totais'] = fin_data[['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuicao_Assistencial', 'ISSQN Retido', 'COMPRAS', 'Folha_Liquida']].sum(axis=1)

# Calculando lucro/prejuízo
fin_data['Lucro/Prejuízo'] = fin_data['Vendas'] - fin_data['Despesas Totais']

# Configurando a página do Streamlit
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

# Estilo customizado para o fundo da página e estilo neon
page_bg_img = '''
<style>
body {
    background-color: #0f0e17;
    color: #ffffff;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Título do dashboard
st.markdown("<h1 style='text-align: center; color: #a7f3d0;'>Dashboard Financeiro Neon</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ff8a65;'>Visão Geral das Receitas, Despesas e Lucros</h3>", unsafe_allow_html=True)

# Período da Análise
st.markdown(f"<h4 style='text-align: center; color: #f4d06f;'>Período da análise: {fin_data['Período'].min()} a {fin_data['Período'].max()}</h4>", unsafe_allow_html=True)

# Resumo Geral no topo usando cards estilizados com gradientes neon
with st.container():
    st.markdown("#### Resumo Financeiro Geral")
    st.markdown(
        "<style>"
        "div[data-testid='metric-container'] {"
        "    background: linear-gradient(135deg, #ff4b5c, #ff8a65);"
        "    border: 1px solid #ff8a65;"
        "    padding: 15px;"
        "    border-radius: 15px;"
        "    box-shadow: 0px 0px 20px #ff8a65;"
        "    margin-bottom: 15px;"
        "    color: white;"
        "}"
        "div[data-testid='metric-container'] > div {"
        "    overflow-wrap: break-word;"
        "    font-family: 'Arial', sans-serif;"
        "    font-weight: bold;"
        "}"
        "</style>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="large")
    col1.metric(label="💰 Receita Total", value=f"R$ {fin_data['Vendas'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col2.metric(label="💸 Despesas Totais", value=f"R$ {fin_data['Despesas Totais'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col3.metric(label="📊 Lucro/Prejuízo Total", value=f"R$ {fin_data['Lucro/Prejuízo'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Indicadores Detalhados em Seção Separada e Estilizada com tema Neon
st.markdown("#### Indicadores Detalhados")
with st.container():
    col4, col5, col6, col7, col8 = st.columns(5, gap="large")
    col4.metric(label="📈 Total Vendas", value=f"R$ {fin_data['Vendas'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col5.metric(label="🛒 Total Compras", value=f"R$ {fin_data['COMPRAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col6.metric(label="👥 Total Salários", value=f"R$ {fin_data['Folha_Liquida'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col7.metric(label="💵 Total DAS", value=f"R$ {fin_data['DAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    col8.metric(label="📑 Total DCTFWeb", value=f"R$ {fin_data['Darf DctfWeb'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Receita x Compras
grafico_receita_compras = px.line(
    fin_data, x='Período', y=['Vendas', 'COMPRAS'],
    labels={"value": "Valores em R$", "Período": "Mês/Ano"},
    title="Comparativo de Receitas vs Compras",
    color_discrete_sequence=['#ff8a65', '#42a5f5']
)
grafico_receita_compras.update_layout(template="plotly_dark", title_font_size=20)
st.plotly_chart(grafico_receita_compras, use_container_width=True)

# Receita x Imposto DAS
grafico_receita_das = px.bar(
    fin_data, x='Período', y=['Vendas', 'DAS'],
    barmode='group',
    labels={"value": "Valores em R$", "Período": "Mês/Ano"},
    title="Receitas vs DAS (Imposto)",
    color_discrete_sequence=['#f4d06f', '#13c4a3']
)
grafico_receita_das.update_layout(template="plotly_dark", title_font_size=20)
st.plotly_chart(grafico_receita_das, use_container_width=True)

# Receita Total vs Despesas Totais
grafico_receita_despesas = go.Figure()
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Vendas'],
                                              mode='lines+markers', name='Receita Total',
                                              line=dict(width=3, color='#ff4b5c')))
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Despesas Totais'],
                                              mode='lines+markers', name='Despesas Totais',
                                              line=dict(width=3, dash='dash', color='#13c4a3')))
grafico_receita_despesas.update_layout(
    title="Receita Total vs Despesas Totais",
    xaxis_title="Mês/Ano",
    yaxis_title="Valores em R$",
    template="plotly_dark",
    title_font_size=20
)
st.plotly_chart(grafico_receita_despesas, use_container_width=True)

# Gráfico sugestivo: Análise de Lucro/Prejuízo
grafico_lucro_prejuizo = px.area(
    fin_data, x='Período', y='Lucro/Prejuízo',
    labels={"Lucro/Prejuízo": "Valores em R$", "Período": "Mês/Ano"},
    title="Análise de Lucro/Prejuízo Mensal",
    color_discrete_sequence=['#a7f3d0']
)
grafico_lucro_prejuizo.update_layout(template="plotly_dark", title_font_size=20)
st.plotly_chart(grafico_lucro_prejuizo, use_container_width=True)

# Tabela Interativa para Consulta
st.markdown("### Tabela Interativa para Consulta de Dados Financeiros")
# Adicionando linha de totalização na tabela
fin_data_display = fin_data.copy()
colunas_monetarias = ['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuicao_Assistencial', 'ISSQN Retido', 'COMPRAS', 'Vendas', 'Folha_Liquida', 'Despesas Totais', 'Lucro/Prejuízo']
for coluna in colunas_monetarias:
    fin_data_display[coluna] = fin_data_display[coluna].apply(lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Adicionando uma linha de totais na tabela
totais = {
    'Período': 'Totais',
    'Darf DctfWeb': f"R$ {fin_data['Darf DctfWeb'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'DAS': f"R$ {fin_data['DAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'FGTS': f"R$ {fin_data['FGTS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Contribuicao_Assistencial': f"R$ {fin_data['Contribuicao_Assistencial'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'ISSQN Retido': f"R$ {fin_data['ISSQN Retido'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'COMPRAS': f"R$ {fin_data['COMPRAS'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Vendas': f"R$ {fin_data['Vendas'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Folha_Liquida': f"R$ {fin_data['Folha_Liquida'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Despesas Totais': f"R$ {fin_data['Despesas Totais'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    'Lucro/Prejuízo': f"R$ {fin_data['Lucro/Prejuízo'].sum():,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
}
fin_data_display = pd.concat([fin_data_display, pd.DataFrame([totais])], ignore_index=True)

st.dataframe(fin_data_display)

# Outras Despesas Não Registradas na Planilha
st.markdown("### Outras Despesas Não Registradas na Planilha")
st.markdown("Essas despesas não estão incluídas nas demonstrações acima.")
st.markdown("- COMPRA ATIVO: R$ 78.390,94")
st.markdown("- MAT USO CONSUMO: R$ 31.785,62")

# Comentário final
st.markdown(
    "<div style='text-align: center; font-size: 24px; color: #a7f3d0;'>Confie nos números e impulsione o crescimento da sua empresa!</div>", unsafe_allow_html=True
)
