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
    color: #000000;
}
h1, h2, h3, h4 {
    text-align: center;
    color: #1f4e79;
}
</style>
''', unsafe_allow_html=True)

# Função para formatar valores monetários, incluindo tratamento para valores negativos
def format_currency(value):
    is_negative = value < 0
    value = abs(value)
    formatted = f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    if is_negative:
        formatted = f"({formatted})"
    return formatted

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

# Gráficos e tabela interativa permanecem os mesmos (inclua-os aqui)

# Cálculos para os comentários finais
num_meses = len(fin_data)

total_compras = fin_data['COMPRAS'].sum()
media_compras = total_compras / num_meses

total_folha = fin_data['Folha_Liquida'].sum()
media_folha = total_folha / num_meses

total_vendas = fin_data['Vendas'].sum()
media_vendas = total_vendas / num_meses

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

# Adicionando os comentários finais com valores calculados
st.markdown("---")  # Linha separadora
st.markdown("## Resumo do Desempenho Financeiro")

st.markdown(f"""
Gostaria de compartilhar um resumo do desempenho financeiro da empresa de janeiro a setembro de 2024, focando em alguns pontos importantes sobre as **compras**, **folha de pagamento**, **vendas** e os **impostos pagos**.

### Compras e Folha de Pagamento

As **compras** têm se mantido estáveis, com uma média mensal de **{media_compras_formatted}**. Observamos que os valores variaram ao longo dos meses, mas têm se mantido dentro do esperado, sem grandes oscilações inesperadas. Isso mostra um controle consistente e bem ajustado em relação aos fornecimentos necessários.

Em relação à **folha de pagamento**, a média mensal foi de **{media_folha_formatted}**, representando um valor relativamente constante ao longo do ano. Esse comportamento permite uma previsibilidade financeira e maior controle dos custos com pessoal, facilitando o planejamento financeiro.

### Vendas e Impostos (DAS)

O total de **vendas** realizadas no período foi de **{total_vendas_formatted}**, com uma média mensal de **{media_vendas_formatted}**. Comparando com o valor de **DAS** pago, que somou **{total_das_formatted}** durante o mesmo período, temos uma relação clara entre a receita gerada e a carga tributária correspondente. Essa comparação é crucial para garantir que a margem de lucro da empresa esteja sendo mantida mesmo após o pagamento dos tributos.

### Total de Despesas e Custos vs Receita

Ao observarmos o total de **despesas**, que inclui compras, folha de pagamento e impostos, notamos que o valor acumulado das despesas chegou a **{total_despesas_formatted}**. Com uma receita total de **{total_vendas_formatted}**, a empresa apresenta um **saldo negativo de {saldo_negativo_formatted}**, indicando que, até o momento, as receitas não estão conseguindo cobrir os custos e as despesas.

Esse resultado mostra que a empresa enfrentou um saldo negativo, onde as receitas não foram suficientes para cobrir os custos e despesas acumulados. É importante focar em aumentar as receitas e reduzir despesas para melhorar a sustentabilidade financeira. Recomendo manter o controle rigoroso sobre as compras e os custos fixos, especialmente considerando a carga tributária, para que possamos garantir essa sustentabilidade financeira ao longo do ano.
""")

# Ajuste final de estilo para os comentários
st.markdown('''
<style>
h2, h3, h4 {
    color: #1f4e79;
}
p {
    font-size: 16px;
    line-height: 1.6;
    color: #000000;
}
</style>
''', unsafe_allow_html=True)
