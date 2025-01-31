import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import subprocess
import time

# Configuração inicial do estado da última atualização
if "ultima_atualizacao" not in st.session_state:
    st.session_state["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Função para atualizar a data e hora
def atualizar_data_hora():
    st.session_state["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

################################################# CONFIGURAÇÃO DA PÁGINA #################################################

st.set_page_config(layout="wide")

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

################################################# CARREGAMENTO DOS DADOS #################################################

@st.cache_data  # Cache para evitar recarregar os dados a cada interação
def carregar_dados():
    tarefas = pd.read_csv("dados/tarefas.csv")
    extras = pd.read_excel("dados/atividades_extras.xlsx")
    auditoria = pd.read_excel("dados/auditoria.xlsx")
    base = pd.read_csv("dados/base.csv")
    pos_aplicacao = pd.read_excel("dados/pos_aplicacao.xlsx")

    # Garantir que a coluna 'Data' esteja no formato datetime
    tarefas['Data'] = pd.to_datetime(tarefas['Data'], dayfirst=True, errors='coerce')
    tarefas["Setor"] = tarefas["Setor"].astype(int)
    tarefas["Status"] = tarefas["Status"].astype(str)
    tarefas["Colaborador"] = tarefas["Colaborador"].astype(str)
    tarefas["Tipo"] = tarefas["Tipo"].astype(str)

    # Realizar a junção entre df_filtrado e base, trazendo as colunas 'unidade' e 'area' do 'base'
    tarefas = pd.merge(tarefas, base[['Setor', 'Unidade', 'Area']], on='Setor', how='left')
    tarefas["Unidade"] = tarefas["Unidade"].astype(str)

    # Garantir que a coluna 'DATA' do pos_aplicacao esteja no formato datetime
    pos_aplicacao["DATA"] = pd.to_datetime(pos_aplicacao["DATA"], format="%d/%m/%Y", errors="coerce")

    return tarefas, extras, auditoria, pos_aplicacao

tarefas, extras, auditoria, pos_aplicacao = carregar_dados()

################################################# BOTÃO ATUALIZAR #################################################

if st.button("Atualizar dados"):
    atualizar_data_hora()
    try:
        with st.spinner("Autenticando token..."):
            subprocess.run(["python", "scripts/auth.py"], check=True)
        with st.spinner("Coletando dados..."):
            subprocess.run(["python", "scripts/coleta.py"], check=True)
        st.success("Dados atualizados com sucesso!")
        time.sleep(2)
        st.experimental_rerun()  # Recarrega a página para atualizar os dados
    except subprocess.CalledProcessError as e:
        st.error(f"Erro ao executar um dos scripts: {e}")

################################################# SIDEBAR - FILTROS #################################################

def aplicar_filtros(tarefas, pos_aplicacao):
    st.sidebar.markdown("### Última Atualização")
    st.sidebar.write(f"Atualizado em: {st.session_state['ultima_atualizacao']}")

    st.sidebar.title("Filtros")

    # Filtro de datas
    min_data = min(tarefas["Data"].min(), pos_aplicacao["DATA"].min()).to_pydatetime()
    max_data = max(tarefas["Data"].max(), pos_aplicacao["DATA"].max()).to_pydatetime()
    data_inicio, data_fim = st.sidebar.slider(
        "Selecione o intervalo de datas",
        min_value=min_data,
        max_value=max_data,
        value=(min_data, max_data),
        format="DD/MM/YYYY",
        key="slider_data"
    )

    # Aplicar filtro de datas ao dataset de tarefas
    tarefas_filtradas = tarefas[(tarefas['Data'] >= data_inicio) & (tarefas['Data'] <= data_fim)]

    # Aplicar filtro de datas ao dataset de pós-aplicação
    pos_aplicacao_filtrada = pos_aplicacao[(pos_aplicacao['DATA'] >= data_inicio) & (pos_aplicacao['DATA'] <= data_fim)]

    # Filtro de Setor
    setor_selecionado = st.sidebar.text_input(
        "Digite o número do Setor:", value="", max_chars=5, placeholder="Setor:",
        key="input_setor"
    )
    if setor_selecionado:
        tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Setor"].astype(str).str.contains(setor_selecionado)]
        pos_aplicacao_filtrada = pos_aplicacao_filtrada[pos_aplicacao_filtrada["SETOR"].astype(str).str.contains(setor_selecionado)]

    # Filtro de Status
    status_selecionado = st.sidebar.selectbox(
        "Selecione o Status:",
        options=["Todos"] + tarefas_filtradas["Status"].unique().tolist(),
        index=0,
        key="selectbox_status"
    )
    if status_selecionado != "Todos":
        tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Status"] == status_selecionado]

    # Filtro de Colaborador
    colaborador_selecionado = st.sidebar.selectbox(
        "Selecione o Colaborador:",
        options=["Todos"] + tarefas_filtradas["Colaborador"].unique().tolist(),
        index=0,
        key="selectbox_colaborador"
    )
    if colaborador_selecionado != "Todos":
        tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Colaborador"] == colaborador_selecionado]

    # Filtro de Tipo de Projeto
    tipo_selecionado = st.sidebar.selectbox(
        "Selecione o Tipo de Projeto:",
        options=["Todos"] + tarefas_filtradas["Tipo"].unique().tolist(),
        index=0,
        key="selectbox_tipo"
    )
    if tipo_selecionado != "Todos":
        tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Tipo"] == tipo_selecionado]

    # Filtro de Unidade
    unidades_selecionadas = st.sidebar.multiselect(
        "Selecione a(s) Unidade(s):",
        options=tarefas_filtradas["Unidade"].unique().tolist(),
        default=tarefas_filtradas["Unidade"].unique().tolist(),
        key="multiselect_unidade"
    )
    if unidades_selecionadas:
        tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Unidade"].isin(unidades_selecionadas)]
        pos_aplicacao_filtrada = pos_aplicacao_filtrada[pos_aplicacao_filtrada["UNIDADE"].isin(unidades_selecionadas)]

    return tarefas_filtradas, pos_aplicacao_filtrada

################################################# DASHBOARD - ATIVIDADES #################################################

def dashboard_1():
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            color: #000;
            font-size: 48px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="title">Gestão Semanal - Geotecnologia</div>', unsafe_allow_html=True)

    # Aplica os filtros e obtém os DataFrames filtrados
    tarefas_filtradas, pos_aplicacao_filtrada = aplicar_filtros(tarefas, pos_aplicacao)

    # Exibe métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        total_area = tarefas_filtradas['Area'].sum()
        formatted_area = f"{total_area:,.0f}".replace(',', '.')
        st.metric("Área Total", f"{formatted_area} ha")
    with col2:
        st.metric("Quantidade de Atividades", tarefas_filtradas['Colaborador'].size)
    with col3:
        st.metric("Colaboradores", tarefas_filtradas['Colaborador'].unique().size)

    st.divider()

    # Gráfico de Atividades por Colaborador
    st.subheader("Atividades por Colaborador")
    df_contagem_responsavel = tarefas_filtradas.groupby("Colaborador")["Tipo"].count().reset_index()
    df_contagem_responsavel.columns = ["Colaborador", "Quantidade de Projetos"]
    df_contagem_responsavel = df_contagem_responsavel.sort_values(by="Quantidade de Projetos", ascending=False)
    fig_responsavel = px.bar(
        df_contagem_responsavel,
        x="Quantidade de Projetos",
        y="Colaborador",
        color="Colaborador",
        orientation="h",
        text="Quantidade de Projetos",
    )
    fig_responsavel.update_traces(texttemplate="%{text}", textposition="outside")
    fig_responsavel.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_responsavel)

    st.divider()

    # Gráfico de Quantidade de Projetos por Tipo
    st.subheader("Quantidade de Projetos por Tipo")
    df_contagem_tipo = tarefas_filtradas.groupby("Tipo")["Colaborador"].count().reset_index()
    df_contagem_tipo.columns = ["Tipo", "Quantidade de Projetos"]
    df_contagem_tipo = df_contagem_tipo.sort_values(by="Quantidade de Projetos", ascending=False)
    fig_tipo = px.bar(
        df_contagem_tipo,
        x="Tipo",
        y="Quantidade de Projetos",
        color="Tipo",
        text="Quantidade de Projetos",
    )
    fig_tipo.update_traces(texttemplate="%{text}", textposition="outside")
    fig_tipo.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_tipo)

    st.divider()

    # Gráfico de Status dos Projetos
    st.subheader("Status dos Projetos")
    df_contagem_status = tarefas_filtradas.groupby("Status")["Tipo"].count().reset_index()
    df_contagem_status.columns = ["Status", "Quantidade de Projetos"]
    df_contagem_status = df_contagem_status.sort_values(by="Quantidade de Projetos", ascending=False)
    fig_status = px.bar(
        df_contagem_status,
        x="Quantidade de Projetos",
        y="Status",
        color="Status",
        orientation="h",
        text="Quantidade de Projetos",
    )
    fig_status.update_traces(texttemplate="%{text}", textposition="outside")
    fig_status.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_status)

    st.divider()

    # Gráfico de Pós-Aplicação
    st.subheader("Mapas de Pós-Aplicação")
    pos_aplicacao_filtrada["MÊS"] = pos_aplicacao_filtrada["DATA"].dt.strftime('%B').str.capitalize()
    df_unico = pos_aplicacao_filtrada.drop_duplicates(subset=["MÊS", "SETOR"])
    df_contagem = df_unico["MÊS"].value_counts().reset_index()
    df_contagem.columns = ["MÊS", "QUANTIDADE"]
    ordem_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    fig_mes = px.bar(
        df_contagem,
        x="QUANTIDADE",
        y="MÊS",
        color="MÊS",
        orientation="h",
        text="QUANTIDADE",
        category_orders={"MÊS": ordem_meses}
    )
    fig_mes.update_traces(texttemplate="%{text}", textposition="outside")
    fig_mes.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_mes)

    st.divider()

    # Gráfico de Projetos por Unidade
    st.subheader("Projetos por Unidade")
    df_contagem_unidade = tarefas_filtradas.groupby("Unidade")["Tipo"].count().reset_index()
    df_contagem_unidade.columns = ["Unidade", "Quantidade de Projetos"]
    fig_pizza = px.pie(
        df_contagem_unidade,
        names="Unidade",
        values="Quantidade de Projetos",
        color="Unidade",
        hole=0.3,
        labels={'Quantidade de Projetos': 'Porcentagem de Projetos'}
    )
    st.plotly_chart(fig_pizza)

################################################# LAYOUT PRINCIPAL #################################################

def main():
    st.sidebar.title("Navegação")
    opcao = st.sidebar.radio("Selecione o Dashboard", ["Atividades Semanais", "Atividades Extras", "Auditoria"])

    if opcao == "Atividades Semanais":
        dashboard_1()
    elif opcao == "Atividades Extras":
        st.write("### Atividades Extras")
    elif opcao == "Auditoria":
        st.write("### Auditoria")

if __name__ == "__main__":
    main()