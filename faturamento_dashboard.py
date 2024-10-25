import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Dados fornecidos (de Janeiro/2024 a Setembro/2024)
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
fin_data['Despesas Totais'] = fin_data[['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuicao_Assistencial',
                                        'ISSQN Retido', 'COMPRAS', 'Folha_Liquida']].sum(axis=1)

# Calculando lucro/prejuízo
fin_data['Lucro/Prejuízo'] = fin_data['Vendas'] - fin_data['Despesas Totais']

# Configurando a página do Streamlit
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

# Estilo customizado
st.markdown('''
<style>
body, .stApp {
    background-color: #4A5658;
    color: #ffffff;
    font-family: 'Ubuntu', sans-serif;
}
h1, h2, h3, h4 {
    text-align: center;
    color: #A8AFB0;
}
.metric-card {
    background: linear-gradient(135deg, #757575, #C5C5C5);
    color: #000000;
}
</style>
''', unsafe_allow_html=True)

# Função para formatar valores monetários
def format_currency(value):
    is_negative = value < 0
    value = abs(value)
    formatted = f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    if is_negative:
        formatted = f"({formatted})"
    return formatted

# Função para criar um cartão métrico personalizado
def metric_card(title, value):
    st.markdown(f'''
    <div class="metric-card" style="
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
    ">
        <h3>{title}</h3>
        <p style="font-size: 24px; font-weight: bold;">{value}</p>
    </div>
    ''', unsafe_allow_html=True)

# Título do dashboard
st.markdown("# Dashboard Financeiro")
st.markdown("### Visão Geral das Receitas, Despesas e Lucros")
st.markdown(f"#### Período da análise: {fin_data['Período'].min()} a {fin_data['Período'].max()}")

# Resumo Geral no topo usando cartões personalizados
st.markdown("#### Resumo Financeiro Geral")
col1, col2, col3 = st.columns(3)
with col1:
    metric_card("💰 Receita Total", format_currency(fin_data['Vendas'].sum()))
with col2:
    metric_card("💸 Despesas Totais", format_currency(fin_data['Despesas Totais'].sum()))
with col3:
    metric_card("📊 Lucro/Prejuízo Total", format_currency(fin_data['Lucro/Prejuízo'].sum()))

# Indicadores Detalhados em Seção Separada
st.markdown("#### Indicadores Detalhados")
col4, col5, col6, col7, col8 = st.columns(5)
with col4:
    metric_card("📈 Total Vendas", format_currency(fin_data['Vendas'].sum()))
with col5:
    metric_card("🛒 Total Compras", format_currency(fin_data['COMPRAS'].sum()))
with col6:
    metric_card("👥 Total Salários", format_currency(fin_data['Folha_Liquida'].sum()))
with col7:
    metric_card("💵 Total DAS", format_currency(fin_data['DAS'].sum()))
with col8:
    metric_card("📑 Total DCTFWeb", format_currency(fin_data['Darf DctfWeb'].sum()))

# Gráficos
grafico_tema = 'plotly_dark'
cores_graficos = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# Receita x Compras
grafico_receita_compras = go.Figure()
grafico_receita_compras.add_trace(go.Scatter(
    x=fin_data['Período'], y=fin_data['Vendas'],
    mode='lines+markers',
    name='Vendas',
    line=dict(width=3, color=cores_graficos[0]),
    marker=dict(size=8, color=cores_graficos[0], opacity=0.8)
))
grafico_receita_compras.add_trace(go.Scatter(
    x=fin_data['Período'], y=fin_data['COMPRAS'],
    mode='lines+markers',
    name='Compras',
    line=dict(width=3, color=cores_graficos[1]),
    marker=dict(size=8, color=cores_graficos[1], opacity=0.8)
))
grafico_receita_compras.update_layout(
    title="Comparativo de Receitas vs Compras",
    xaxis_title="Mês/Ano",
    yaxis_title="Valores em R$",
    template=grafico_tema,
    title_font_size=20,
    font=dict(color='#ffffff'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(grafico_receita_compras, use_container_width=True)

# Receita x Imposto DAS
# Definindo cores específicas para evitar confusão
cores_graficos_das = ['#1f77b4', '#2ca02c']  # Azul e verde

grafico_receita_das = px.bar(
    fin_data, x='Período', y=['Vendas', 'DAS'],
    barmode='group',
    labels={"value": "Valores em R$", "Período": "Mês/Ano"},
    title="Receitas vs DAS (Imposto)",
    color_discrete_sequence=cores_graficos_das
)
grafico_receita_das.update_layout(template=grafico_tema, title_font_size=20, font=dict(color='#ffffff'))
st.plotly_chart(grafico_receita_das, use_container_width=True)

# Receita Total vs Despesas Totais
grafico_receita_despesas = go.Figure()
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Vendas'],
                                              mode='lines+markers', name='Receita Total',
                                              line=dict(width=3, color=cores_graficos[2])))
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Despesas Totais'],
                                              mode='lines+markers', name='Despesas Totais',
                                              line=dict(width=3, dash='dash', color=cores_graficos[3])))
grafico_receita_despesas.update_layout(
    title="Receita Total vs Despesas Totais",
    xaxis_title="Mês/Ano",
    yaxis_title="Valores em R$",
    template=grafico_tema,
    title_font_size=20,
    font=dict(color='#ffffff')
)
st.plotly_chart(grafico_receita_despesas, use_container_width=True)

# Gráfico sugestivo: Análise de Lucro/Prejuízo
grafico_lucro_prejuizo = px.area(
    fin_data, x='Período', y='Lucro/Prejuízo',
    labels={"Lucro/Prejuízo": "Valores em R$", "Período": "Mês/Ano"},
    title="Análise de Lucro/Prejuízo Mensal",
    color_discrete_sequence=[cores_graficos[0]]
)
grafico_lucro_prejuizo.update_layout(
    template=grafico_tema,
    title_font_size=20,
    font=dict(color='#ffffff')
)
st.plotly_chart(grafico_lucro_prejuizo, use_container_width=True)

# Tabela Interativa para Consulta
st.markdown("### Tabela Interativa para Consulta de Dados Financeiros")
fin_data_display = fin_data.copy()
colunas_monetarias = ['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuicao_Assistencial',
                      'ISSQN Retido', 'COMPRAS', 'Vendas', 'Folha_Liquida',
                      'Despesas Totais', 'Lucro/Prejuízo']
for coluna in colunas_monetarias:
    fin_data_display[coluna] = fin_data_display[coluna].apply(format_currency)

# Adicionando uma linha de totais na tabela
totais = {
    'Período': 'Totais',
    'Darf DctfWeb': format_currency(fin_data['Darf DctfWeb'].sum()),
    'DAS': format_currency(fin_data['DAS'].sum()),
    'FGTS': format_currency(fin_data['FGTS'].sum()),
    'Contribuicao_Assistencial': format_currency(fin_data['Contribuicao_Assistencial'].sum()),
    'ISSQN Retido': format_currency(fin_data['ISSQN Retido'].sum()),
    'COMPRAS': format_currency(fin_data['COMPRAS'].sum()),
    'Vendas': format_currency(fin_data['Vendas'].sum()),
    'Folha_Liquida': format_currency(fin_data['Folha_Liquida'].sum()),
    'Despesas Totais': format_currency(fin_data['Despesas Totais'].sum()),
    'Lucro/Prejuízo': format_currency(fin_data['Lucro/Prejuízo'].sum())
}
fin_data_display = pd.concat([fin_data_display, pd.DataFrame([totais])], ignore_index=True)

st.dataframe(fin_data_display)

# Outras Despesas Não Registradas na Planilha
st.markdown("### Outras Despesas Não Registradas na Planilha")
st.write("Essas despesas não estão incluídas nas demonstrações acima.")
st.write("- COMPRA ATIVO: R$ 78.390,94")
st.write("- MAT USO CONSUMO: R$ 31.785,62")
