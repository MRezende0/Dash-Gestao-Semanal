import streamlit as st
from config import DATA_PATHS
from utils.db_handler import load_data
from utils.sidebar import render_sidebar
from pages import atividade_semanal, atividade_extra, auditoria

# Cache para carregar as bases de dados
@st.cache_data
def load_all_data():
    return {
        "atividade_semanal": load_data(DATA_PATHS["atividade_semanal"]),
        "atividade_extra": load_data(DATA_PATHS["atividade_extra"]),
        "auditoria": load_data(DATA_PATHS["auditoria"]),
    }

# Carregar todas as bases
dataframes = load_all_data()

# Criar sidebar
st.sidebar.title("Selecione o Dashboard")
selected_dashboard = st.sidebar.radio(
    "Dashboards",
    ["Atividade Semanal", "Atividade Extra", "Auditoria"]
)

# Renderizar filtros globais
filtros = render_sidebar()

# Selecionar e renderizar o dashboard correspondente
if selected_dashboard == "Atividade Semanal":
    atividade_semanal.render(dataframes["atividade_semanal"], filtros)
elif selected_dashboard == "Atividade Extra":
    atividade_extra.render(dataframes["atividade_extra"], filtros)
elif selected_dashboard == "Auditoria":
    auditoria.render(dataframes["auditoria"], filtros)





















import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess
import time
from datetime import datetime

import scripts.atividade_semanal as atividade_semanal
import scripts.atividade_extra as atividade_extra
import scripts.auditoria as auditoria

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

################################################# BOTÕES DAS ABAS #################################################

# CSS para estilizar os botões
st.markdown(
    """
    <style>
    .info-box-btn {
        background-color: rgba(42, 157, 244, 0.7);
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 5px;
        color: white;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .info-box-btn:hover {
        background-color: rgba(42, 157, 244, 1);
        transform: scale(1.05);
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Inicializa o estado para a aba ativa
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Atividade Semanal"

# Função para trocar de aba
def switch_tab(tab_name):
    st.session_state.current_tab = tab_name

# Layout para os botões
col1, col2, col3 = st.columns([1, 2, 1])  # Usando colunas com largura ajustada para centralizar

with col1:
    st.empty()  # Mantém espaço vazio na primeira coluna

with col2:
    # Sub-colunas dentro da coluna central
    btn_col1, btn_col2, btn_col3 = st.columns(3)  # 3 colunas para os botões

    with btn_col1:
        if st.button("Gestão Semanal", key="Gestao"):
            switch_tab("Gestão Semanal")
    with btn_col2:
        if st.button("Atividade Extra", key="Atividade"):
            switch_tab("Atividade Extra")
    with btn_col3:
        if st.button("Auditoria", key="Auditoria"):
            switch_tab("Auditoria")

with col3:
    st.empty()  # Mantém espaço vazio na última coluna

# Filtros dinâmicos na sidebar
st.sidebar.markdown("---")
if st.session_state.current_tab == "Atividade Semanal":
    st.sidebar.subheader("Filtros - Atividade Semanal")
    setor = st.sidebar.selectbox("Setor", ["Todos", "Setor A", "Setor B"])
    unidade = st.sidebar.selectbox("Unidade", ["Todas", "Unidade 1", "Unidade 2"])
elif st.session_state.current_tab == "Atividade Extra":
    st.sidebar.subheader("Filtros - Atividade Extra")
    tipo_atividade = st.sidebar.multiselect("Tipo de Atividade", ["Mapeamento", "Drone", "Análise"])
elif st.session_state.current_tab == "Auditoria":
    st.sidebar.subheader("Filtros - Auditoria")
    projeto = st.sidebar.text_input("Projeto")
    porcentagem = st.sidebar.slider("Porcentagem de Adesão", 0, 100, 50)

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

################################################# BOTÕES DAS ABAS #################################################

# Controle de abas
if st.session_state.current_tab == "Atividade Semanal":
    atividade_semanal.render()
elif st.session_state.current_tab == "Atividade Extra":
    atividade_extra.render()
elif st.session_state.current_tab == "Auditoria":
    auditoria.render()