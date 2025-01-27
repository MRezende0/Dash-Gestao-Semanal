import streamlit as st
import datetime
from utils.db_handler import load_data
from config import DATA_PATHS

def render_sidebar():

    st.sidebar.title("Filtros")

################################ ATUALIZAÇÃO ################################

    st.sidebar.markdown("### Última Atualização")
    # Configuração inicial do estado da última atualização
    if "ultima_atualizacao" not in st.session_state:
        st.session_state["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Função para atualizar a data e hora
    def atualizar_data_hora():
        st.session_state["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Exibir a última data e hora de atualização na sidebar
    st.sidebar.write(f"Atualizado em: {st.session_state['ultima_atualizacao']}")

################################################# FILTROS #################################################

    # Carregar a base de dados
    tarefas = load_data(DATA_PATHS["tarefas"])
    
    # Aplicando os filtros no DataFrame
    tarefas_filtrado = tarefas.copy()

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

################################################# FILTROS #################################################

    # Adicione filtros personalizados aqui
    # filtro1 = st.sidebar.selectbox("Selecione o Filtro 1", ["Opção 1", "Opção 2"])
    # filtro2 = st.sidebar.slider("Selecione o Filtro 2", 0, 100)
    
    # return {"filtro1": filtro1, "filtro2": filtro2}

################################ DATA ################################

    # Seção de Filtro de Data (barra deslizante para selecionar intervalo de datas)
    st.sidebar.subheader("Data")

    # Converter as datas para datetime.date para o Streamlit aceitar
    data_inicio, data_fim = st.sidebar.slider(
        "Selecione o intervalo de datas:",
        min_value=tarefas["Data"].min().date(),  # Converter para .date() para usar com o slider
        max_value=tarefas["Data"].max().date(),  # Converter para .date() para usar com o slider
        value=(tarefas["Data"].min().date(), tarefas["Data"].max().date()),  # Definir o valor padrão como intervalo completo
        format="DD/MM/YYYY",
    )

    # Filtro de Data: Convertendo a coluna 'Data' para datetime.date antes da comparação
    tarefas_filtrado['Data'] = tarefas_filtrado['Data'].dt.date

    # Filtro de Data
    tarefas_filtrado = tarefas_filtrado[
        (tarefas_filtrado["Data"] >= data_inicio) & (tarefas_filtrado["Data"] <= data_fim)
    ]

################################ SETOR ################################

    # Seção de Filtro por Setor (campo para digitar o número do setor)
    st.sidebar.subheader("Setor")
    setor_selecionado = st.sidebar.text_input(
        "Digite o número do Setor:", value="", max_chars=5, placeholder="Setor:"
    )

    # Filtro de Setor
    if setor_selecionado:
        tarefas_filtrado = tarefas_filtrado[tarefas_filtrado["Setor"].astype(str).str.contains(setor_selecionado)]

################################ STATUS ################################

    # Seção de Filtro de Status (drop box para selecionar o status)
    st.sidebar.subheader("Status")
    status_selecionado = st.sidebar.selectbox(
        "Selecione o Status:",
        options=["Todos"] + tarefas["Status"].unique().tolist(),
        index=0,
    )

    # Filtro de Status
    if status_selecionado != "Todos":
        tarefas_filtrado = tarefas_filtrado[tarefas_filtrado["Status"] == status_selecionado]

################################ COLABORADOR ################################

    # Seção de Filtro por Pessoas (drop box para selecionar a pessoa)
    st.sidebar.subheader("Colaborador")
    pessoa_selecionada = st.sidebar.selectbox(
        "Selecione a Pessoa:",
        options=["Todos"] + tarefas["Colaborador"].unique().tolist(),
        index=0,
    )

    # Filtro de Pessoas
    if pessoa_selecionada != "Todos":
        tarefas_filtrado = tarefas_filtrado[tarefas_filtrado["Colaborador"] == pessoa_selecionada]

################################ TIPO DE PROJETO ################################

    # Seção de Filtro por Projeto (drop box para selecionar o tipo de projeto)
    st.sidebar.subheader("Tipo")
    projeto_selecionado = st.sidebar.selectbox(
        "Selecione o Projeto:",
        options=["Todos"] + tarefas["Tipo"].unique().tolist(),
        index=0,
    )

    # Filtro de Projeto
    if projeto_selecionado != "Todos":
        tarefas_filtrado = tarefas_filtrado[tarefas_filtrado["Tipo"] == projeto_selecionado]

################################ UNIDADE ################################

    # Seção de Filtro de Unidade (botões para selecionar unidade)
    st.sidebar.subheader("Unidade")
    unidade_selecionada = st.sidebar.multiselect(
        "Selecione a(s) Unidade(s):",
        options=tarefas["Unidade"].unique().tolist(),
        default=tarefas["Unidade"].unique().tolist(),
    )

    # Filtro de Unidade
    if unidade_selecionada:
        tarefas_filtrado = tarefas_filtrado[tarefas_filtrado["Unidade"].isin(unidade_selecionada)]