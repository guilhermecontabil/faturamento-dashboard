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
fin_data['Despesas Totais'] = fin_data[['Darf DctfWeb', 'DAS', 'FGTS', 'Contribuicao_Assistencial',
                                        'ISSQN Retido', 'COMPRAS', 'Folha_Liquida']].sum(axis=1)

# Calculando lucro/prejuízo
fin_data['Lucro/Prejuízo'] = fin_data['Vendas'] - fin_data['Despesas Totais']

# Configurando a página do Streamlit
st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

# Estilo customizado com fundo gradiente do escuro para o claro
st.markdown('''
<style>
.stApp {
    background: linear-gradient(180deg, #1f1f1f, #f0f2f6);
    color: #ffffff;
}
h1, h2, h3, h4 {
    text-align: center;
    color: #ffffff;
}
</style>
''', unsafe_allow_html=True)

# Função para formatar valores monetários
def format_currency(value):
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Função para criar um cartão métrico personalizado
def metric_card(title, value, background, text_color):
    st.markdown(f'''
    <div style="
        background-color: {background};
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: {text_color};
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
    metric_card("💰 Receita Total", format_currency(fin_data['Vendas'].sum()), background="#2196f3", text_color="#ffffff")
with col2:
    metric_card("💸 Despesas Totais", format_currency(fin_data['Despesas Totais'].sum()), background="#f44336", text_color="#ffffff")
with col3:
    metric_card("📊 Lucro/Prejuízo Total", format_currency(fin_data['Lucro/Prejuízo'].sum()), background="#4caf50", text_color="#ffffff")

# Indicadores Detalhados em Seção Separada
st.markdown("#### Indicadores Detalhados")
col4, col5, col6, col7, col8 = st.columns(5)
with col4:
    metric_card("📈 Total Vendas", format_currency(fin_data['Vendas'].sum()), background="#03a9f4", text_color="#ffffff")
with col5:
    metric_card("🛒 Total Compras", format_currency(fin_data['COMPRAS'].sum()), background="#ff9800", text_color="#ffffff")
with col6:
    metric_card("👥 Total Salários", format_currency(fin_data['Folha_Liquida'].sum()), background="#9c27b0", text_color="#ffffff")
with col7:
    metric_card("💵 Total DAS", format_currency(fin_data['DAS'].sum()), background="#009688", text_color="#ffffff")
with col8:
    metric_card("📑 Total DCTFWeb", format_currency(fin_data['Darf DctfWeb'].sum()), background="#795548", text_color="#ffffff")

# Receita x Compras
grafico_receita_compras = go.Figure()
grafico_receita_compras.add_trace(go.Scatter(
    x=fin_data['Período'], y=fin_data['Vendas'],
    mode='lines+markers',
    name='Vendas',
    line=dict(width=3, color='#1f77b4'),
    marker=dict(size=8, color='#1f77b4', opacity=0.8)
))
grafico_receita_compras.add_trace(go.Scatter(
    x=fin_data['Período'], y=fin_data['COMPRAS'],
    mode='lines+markers',
    name='Compras',
    line=dict(width=3, color='#ff7f0e'),
    marker=dict(size=8, color='#ff7f0e', opacity=0.8)
))
grafico_receita_compras.update_layout(
    title="Comparativo de Receitas vs Compras",
    xaxis_title="Mês/Ano",
    yaxis_title="Valores em R$",
    template="plotly_dark",
    title_font_size=20,
    font=dict(color='#ffffff'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(grafico_receita_compras, use_container_width=True)

# Receita x Imposto DAS
grafico_receita_das = px.bar(
    fin_data, x='Período', y=['Vendas', 'DAS'],
    barmode='group',
    labels={"value": "Valores em R$", "Período": "Mês/Ano"},
    title="Receitas vs DAS (Imposto)",
    color_discrete_sequence=['#2196f3', '#f44336']
)
grafico_receita_das.update_layout(template="plotly_dark", title_font_size=20)
st.plotly_chart(grafico_receita_das, use_container_width=True)

# Receita Total vs Despesas Totais
grafico_receita_despesas = go.Figure()
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Vendas'],
                                              mode='lines+markers', name='Receita Total',
                                              line=dict(width=3, color='#4caf50')))
grafico_receita_despesas.add_trace(go.Scatter(x=fin_data['Período'], y=fin_data['Despesas Totais'],
                                              mode='lines+markers', name='Despesas Totais',
                                              line=dict(width=3, dash='dash', color='#f44336')))
grafico_receita_despesas.update_layout(
    title="Receita Total vs Despesas Totais",
    xaxis_title="Mês/Ano",
    yaxis_title="Valores em R$",
    template="plotly_dark",
    title_font_size=20,
    font=dict(color='#ffffff')
)
st.plotly_chart(grafico_receita_despesas, use_container_width=True)

# Gráfico sugestivo: Análise de Lucro/Prejuízo
grafico_lucro_prejuizo = px.area(
    fin_data, x='Período', y='Lucro/Prejuízo',
    labels={"Lucro/Prejuízo": "Valores em R$", "Período": "Mês/Ano"},
    title="Análise de Lucro/Prejuízo Mensal",
    color_discrete_sequence=['#9e9d24']
)
grafico_lucro_prejuizo.update_layout(
    template="plotly_dark",
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
st.markdown("Essas despesas não estão incluídas nas demonstrações acima.")
st.markdown("- **COMPRA ATIVO**: R$ 78.390,94")
st.markdown("- **MAT USO CONSUMO**: R$ 31.785,62")

# Comentário final
st.markdown(
    "<div style='text-align: center; font-size: 24px; color: #ffffff;'>Confie nos números e impulsione o crescimento da sua empresa!</div>", unsafe_allow_html=True
)

# Cálculos para os comentários finais
num_meses = len(fin_data)

media_compras = fin_data['COMPRAS'].mean()
media_folha = fin_data['Folha_Liquida'].mean()
total_vendas = fin_data['Vendas'].sum()
media_vendas = fin_data['Vendas'].mean()
total_das = fin_data['DAS'].sum()
total_despesas = fin_data['Despesas Totais'].sum()
saldo_negativo = total_vendas - total_despesas

# Formatação dos valores
media_compras_formatted = format_currency(media_compras)
media_folha_formatted = format_currency(media_folha)
total_vendas_formatted = format_currency(total_vendas)
media_vendas_formatted = format_currency(media_vendas)
total_das_formatted = format_currency(total_das)
total_despesas_formatted = format_currency(total_despesas)
saldo_negativo_formatted = format_currency(saldo_negativo)

# Adicionando os comentários finais simplificados
st.markdown("---")  # Linha separadora
st.markdown("## Resumo do Desempenho Financeiro")

st.markdown(f"""
- **Compras**: Média mensal de {media_compras_formatted}.
- **Folha de Pagamento**: Média mensal de {media_folha_formatted}.
- **Vendas**: Total de {total_vendas_formatted} com média mensal de {media_vendas_formatted}.
- **Impostos (DAS)**: Total pago de {total_das_formatted}.
- **Despesas Totais**: {total_despesas_formatted}.
- **Saldo**: {saldo_negativo_formatted} (Receita Total - Despesas Totais).
""")

st.markdown("""
O resultado indica que as receitas não estão cobrindo totalmente os custos e despesas. É importante focar em aumentar as receitas e reduzir despesas para melhorar a sustentabilidade financeira. Recomenda-se manter um controle rigoroso sobre as compras e custos fixos, considerando também a carga tributária, para garantir a saúde financeira da empresa ao longo do ano.
""")

# Ajuste final de estilo para os comentários
st.markdown('''
<style>
h2, h3, h4 {
    color: #ffffff;
}
p, li {
    font-size: 16px;
    line-height: 1.6;
    color: #ffffff;
}
</style>
''', unsafe_allow_html=True)
