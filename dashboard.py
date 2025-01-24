import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import time
from datetime import datetime

################################################# BASE DE DADOS #################################################

df = pd.read_csv("tarefas.csv")
base = pd.read_csv("base.csv")

df = df.sort_values("Data", ascending=False)

# Garantir que a coluna 'Data' esteja no formato datetime
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)

################################ MERGE COM UNIDADE E AREA ################################

# Realizar a junção entre df_filtrado e base, trazendo as colunas 'unidade' e 'area' do 'base'
df = pd.merge(df, base[['Setor', 'Unidade', 'Area']], on='Setor', how='left')

################################################# CONFIGURAÇÃO DA PÁGINA #################################################

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

st.markdown("""
    <style>
        /* Remove todo o padding no topo da página */
        .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        /* Remove o padding do cabeçalho */
        header {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* Ajusta o tamanho do cabeçalho */
        .css-1lcb2t1 {
            margin-top: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)


################################################# FILTROS #################################################

st.sidebar.markdown("### Última Atualização")

# Configuração inicial do estado da última atualização
if "ultima_atualizacao" not in st.session_state:
    st.session_state["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Função para atualizar a data e hora
def atualizar_data_hora():
    st.session_state["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Exibir a última data e hora de atualização na sidebar
st.sidebar.write(f"Atualizado em: {st.session_state['ultima_atualizacao']}")

# Adicionar barra lateral
st.sidebar.title("Filtros")

# Aplicando os filtros no DataFrame
df_filtrado = df.copy()

st.markdown("""
    <style>
        /* Remove o padding e a margem do topo da sidebar */
        .css-1d391kg {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        /* Ajusta o espaço da sidebar */
        .css-1d391kg .css-18e3th9 {
            margin-top: 0 !important;
        }

        /* Ajuste do padding da sidebar */
        .css-1d391kg .css-1ynp1f4 {
            padding-top: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)


################################ DATA ################################

# Seção de Filtro de Data (barra deslizante para selecionar intervalo de datas)
st.sidebar.subheader("Data")

# Converter as datas para datetime.date para o Streamlit aceitar
data_inicio, data_fim = st.sidebar.slider(
    "Selecione o intervalo de datas:",
    min_value=df["Data"].min().date(),  # Converter para .date() para usar com o slider
    max_value=df["Data"].max().date(),  # Converter para .date() para usar com o slider
    value=(df["Data"].min().date(), df["Data"].max().date()),  # Definir o valor padrão como intervalo completo
    format="DD/MM/YYYY",
)

# Filtro de Data: Convertendo a coluna 'Data' para datetime.date antes da comparação
df_filtrado['Data'] = df_filtrado['Data'].dt.date

# Filtro de Data
df_filtrado = df_filtrado[
    (df_filtrado["Data"] >= data_inicio) & (df_filtrado["Data"] <= data_fim)
]

################################ SETOR ################################

# Seção de Filtro por Setor (campo para digitar o número do setor)
st.sidebar.subheader("Setor")
setor_selecionado = st.sidebar.text_input(
    "Digite o número do Setor:", value="", max_chars=5, placeholder="Setor:"
)

# Filtro de Setor
if setor_selecionado:
    df_filtrado = df_filtrado[df_filtrado["Setor"].astype(str).str.contains(setor_selecionado)]

################################ STATUS ################################

# Seção de Filtro de Status (drop box para selecionar o status)
st.sidebar.subheader("Status")
status_selecionado = st.sidebar.selectbox(
    "Selecione o Status:",
    options=["Todos"] + df["Status"].unique().tolist(),
    index=0,
)

# Filtro de Status
if status_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Status"] == status_selecionado]

################################ COLABORADOR ################################

# Seção de Filtro por Pessoas (drop box para selecionar a pessoa)
st.sidebar.subheader("Colaborador")
pessoa_selecionada = st.sidebar.selectbox(
    "Selecione a Pessoa:",
    options=["Todos"] + df["Colaborador"].unique().tolist(),
    index=0,
)

# Filtro de Pessoas
if pessoa_selecionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Colaborador"] == pessoa_selecionada]

################################ TIPO DE PROJETO ################################

# Seção de Filtro por Projeto (drop box para selecionar o tipo de projeto)
st.sidebar.subheader("Tipo")
projeto_selecionado = st.sidebar.selectbox(
    "Selecione o Projeto:",
    options=["Todos"] + df["Tipo"].unique().tolist(),
    index=0,
)

# Filtro de Projeto
if projeto_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo"] == projeto_selecionado]

################################ UNIDADE ################################

# # Seção de Filtro de Unidade (botões para selecionar unidade)
# st.sidebar.subheader("Unidade")
# unidade_selecionada = st.sidebar.multiselect(
#     "Selecione a(s) Unidade(s):",
#     options=df["Unidade"].unique().tolist(),
#     default=df["Unidade"].unique().tolist(),
# )

# # Filtro de Unidade
# if unidade_selecionada:
#     df_filtrado = df_filtrado[df_filtrado["Unidade"].isin(unidade_selecionada)]

################################################# BOTÃO ATUALIZAR #################################################

# Botão para rodar os scripts
if st.button("Atualizar dados"):

    atualizar_data_hora()

    try:
        # Mensagem temporária para "Autenticando token..."
        auth_message = st.empty()
        auth_message.write("Autenticando token...")
        
        # Executa o script de autenticação
        subprocess.run(["python", "auth.py"], check=True)
        
        # Mensagem temporária para "Coletando dados..."
        coleta_message = st.empty()
        coleta_message.write("Coletando dados...")
        
        # Executa o script de coleta de dados
        subprocess.run(["python", "coleta.py"], check=True)
        
        # Mensagem temporária para "Atualizando gráficos..."
        grafico_message = st.empty()
        grafico_message.write("Atualizando gráficos...")
        
        # Mensagem de sucesso temporária
        success_message = st.empty()
        success_message.success("Dados atualizados com sucesso!")
        
        # Limpa todas as mensagens após a conclusão do processo
        time.sleep(2)  # Espera 5 segundos para visualizar o sucesso
        auth_message.empty()
        coleta_message.empty()
        grafico_message.empty()
        success_message.empty()  # Limpa também a mensagem de sucesso
        
    except subprocess.CalledProcessError as e:
        st.error(f"Erro ao executar um dos scripts: {e}")

################################################# TÍTULO #################################################

# Cabeçalho da página centralizado
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: #000;  /* Cor do texto do título (opcional) */
        font-size: 48px;  /* Tamanho do texto (opcional) */
        font-weight: bold;  /* Deixar o título em negrito (opcional) */
    }
    </style>
    """, unsafe_allow_html=True)

# Título centralizado
st.markdown('<div class="title">Gestão Semanal - Geotecnologia</div>', unsafe_allow_html=True)

################################################# CABEÇALHO #################################################

# Seções com informações
st.markdown(
    """
    <style>
    .info-box {
        background-color: rgba(118, 184, 42, 0.5);
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 5px;
        color: #000
    }
    .info-container {
        background-color: #000;
        padding: 20px;
        border-radius: 10px;
        display: flex;
        justify-content: space-around;
        gap: 10px;
    }
    .info-container .column {
        flex: 1;
    }
    </style>
    """, unsafe_allow_html=True
)

# Layout em colunas
col1, col2, col3 = st.columns(3)

with col1:
    total_area = df_filtrado['Area'].sum()
    formatted_area = f"{total_area:,.0f}".replace(',', '.')
    st.markdown(f"""
        <div class="info-box">
            <h8><strong>Área Total</strong></h8>
            <h3>{formatted_area} ha</h3>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="info-box">
            <h8><strong>Quantidade de Atividades</strong></h8>
            <h3>{df_filtrado['Colaborador'].size}</h3>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="info-box">
            <h8><strong>Colaboradores</strong></h8>
            <h3>{df_filtrado['Colaborador'].unique().size}</h3>
        </div>
    """, unsafe_allow_html=True)

# Adiciona uma linha horizontal e espaçamento
st.divider()

################################################# GRÁFICO - ATIVIDADES POR COLABORADOR #################################################

# Calcular a quantidade de projetos por colaborador
df_contagem_responsavel = (
    df_filtrado.groupby("Colaborador")["Tipo"].count().reset_index()
)
df_contagem_responsavel.columns = ["Colaborador", "Quantidade de Projetos"]

# Ordenar o DataFrame do maior para o menor número de projetos
df_contagem_responsavel = df_contagem_responsavel.sort_values(
    by="Quantidade de Projetos", ascending=False
)

# Criar o gráfico
st.subheader("Atividades por Colaborador")
fig_responsavel = px.bar(
    df_contagem_responsavel,
    x="Quantidade de Projetos",
    y="Colaborador",
    color="Colaborador",
    orientation="h",
    text="Quantidade de Projetos",  # Vincular diretamente o texto ao valor correto
)

# Configurar o texto corretamente no gráfico
fig_responsavel.update_traces(
    texttemplate="%{text}",  # Exibir o texto diretamente dos valores configurados
    textposition="outside"  # Posicionar o texto fora das barras
)

# Remover a legenda
fig_responsavel.update_layout(showlegend=False)

fig_responsavel.update_layout(margin=dict(l=10, r=10, t=10, b=10))  # Margens mais compactas

# Remover as linhas de contagem (ticks) no eixo X
fig_responsavel.update_layout(
    xaxis=dict(
        showticklabels=False,  # Remove os ticks do eixo X
        title=""  # Remove o nome do eixo X
    ),
    yaxis=dict(
        title=""  # Remove o nome do eixo Y
    )
)

# Exibir o gráfico
st.plotly_chart(fig_responsavel)

# Adiciona uma linha horizontal e espaçamento
st.divider()

################################################# GRÁFICO - TIPO DE PROJETO #################################################

# Calcular a quantidade de projetos por tipo no DataFrame filtrado
df_contagem_tipo = (
    df_filtrado.groupby("Tipo")["Colaborador"].count().reset_index()
)
df_contagem_tipo.columns = ["Tipo", "Quantidade de Projetos"]

# Ordenar o DataFrame do maior para o menor número de projetos
df_contagem_tipo = df_contagem_tipo.sort_values(
    by="Quantidade de Projetos", ascending=False
)

# Criar o gráfico
st.subheader("Quantidade de Projetos")
fig_tipo = px.bar(
    df_contagem_tipo,
    x="Tipo",
    y="Quantidade de Projetos",
    color="Tipo",
    text="Quantidade de Projetos",
)

# Configurar o texto corretamente no gráfico
fig_tipo.update_traces(
    texttemplate="%{text}",
    textposition="outside"
)

# Remover a legenda
fig_tipo.update_layout(showlegend=False)

fig_tipo.update_layout(margin=dict(l=10, r=10, t=10, b=10))  # Margens mais compactas

# Remover as linhas de contagem (ticks) no eixo Y
fig_tipo.update_layout(
    yaxis=dict(showticklabels=False, showline=False, showgrid=False),  # Remove ticks, linha do eixo Y e gridlines
    xaxis=dict(showgrid=False),  # Remove gridlines no eixo X
    xaxis_title="",  # Remove o nome do eixo X
    yaxis_title=""   # Remove o nome do eixo Y
)

# Exibir o gráfico
st.plotly_chart(fig_tipo)

# Adiciona uma linha horizontal e espaçamento
st.divider()

################################################# GRÁFICO - STATUS #################################################

# Calcular a quantidade de projetos por status
df_contagem_status = (
    df_filtrado.groupby("Status")["Tipo"].count().reset_index()
)
df_contagem_status.columns = ["Status", "Quantidade de Projetos"]

# Ordenar o DataFrame do maior para o menor número de projetos
df_contagem_status = df_contagem_status.sort_values(
    by="Quantidade de Projetos", ascending=False
)

# Criar o gráfico
st.subheader("Status dos Projetos")
fig_status = px.bar(
    df_contagem_status,
    x="Quantidade de Projetos",
    y="Status",
    color="Status",
    orientation="h",
    text="Quantidade de Projetos",  # Vincular diretamente o texto ao valor correto
)

# Configurar o texto corretamente no gráfico
fig_status.update_traces(
    texttemplate="%{text}",  # Exibir o texto diretamente dos valores configurados
    textposition="outside"  # Posicionar o texto fora das barras
)

# Remover a legenda
fig_status.update_layout(showlegend=False)

fig_status.update_layout(margin=dict(l=10, r=10, t=10, b=10))  # Margens mais compactas

# Configurar o layout para remover os nomes dos eixos
fig_status.update_layout(
    xaxis=dict(
        showticklabels=False,  # Remove os ticks do eixo X
        title=""  # Remove o nome do eixo X
    ),
    yaxis=dict(
        title=""  # Remove o nome do eixo Y
    )
)

# Exibir o gráfico
st.plotly_chart(fig_status)

# Adiciona uma linha horizontal e espaçamento
st.divider()

################################################# GRÁFICO - UNIDADE #################################################

# Calcular a quantidade de projetos por unidade
df_contagem_unidade = df_filtrado.groupby("Unidade")["Tipo"].count().reset_index()
df_contagem_unidade.columns = ["Unidade", "Quantidade de Projetos"]

# Criar o gráfico de pizza
st.subheader("Projetos por Unidade")
fig_pizza = px.pie(
    df_contagem_unidade,
    names="Unidade",
    values="Quantidade de Projetos",
    color="Unidade",  # Opcional: adicionar cores para cada unidade
    hole=0.3,  # Opcional: criar um gráfico de pizza com um buraco no meio (donut)
    labels={'Quantidade de Projetos': 'Porcentagem de Projetos'}
)

# Exibir o gráfico
st.plotly_chart(fig_pizza)