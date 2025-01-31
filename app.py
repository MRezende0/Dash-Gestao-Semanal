import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

################################################# DADOS #################################################

tarefas = pd.read_csv("dados/tarefas.csv")
extras = pd.read_excel("dados/atividades_extras.xlsx")
auditoria = pd.read_excel("dados/auditoria.xlsx")
base = pd.read_csv("dados/base.csv")
pos_aplicacao = pd.read_excel("dados/pos_aplicacao.xlsx")

tarefas = tarefas.sort_values("Data", ascending=False)

# Garantir que a coluna 'Data' esteja no formato datetime
tarefas['Data'] = pd.to_datetime(tarefas['Data'], dayfirst=True)
tarefas["Setor"] = tarefas["Setor"].astype(int)
tarefas["Status"] = tarefas["Status"].astype(str)
tarefas["Colaborador"] = tarefas["Colaborador"].astype(str)
tarefas["Tipo"] = tarefas["Tipo"].astype(str)

################################ MERGE COM UNIDADE E AREA ################################

# Realizar a junção entre df_filtrado e base, trazendo as colunas 'unidade' e 'area' do 'base'
tarefas = pd.merge(tarefas, base[['Setor', 'Unidade', 'Area']], on='Setor', how='left')
tarefas["Unidade"] = tarefas["Unidade"].astype(str)

################################################# BOTÃO ATUALIZAR #################################################

# Botão para rodar os scripts
if st.button("Atualizar dados"):

    atualizar_data_hora()

    try:
        # Mensagem temporária para "Autenticando token..."
        auth_message = st.empty()
        auth_message.write("Autenticando token...")
        
        # Executa o script de autenticação
        subprocess.run(["python", "scripts/auth.py"], check=True)
        
        # Mensagem temporária para "Coletando dados..."
        coleta_message = st.empty()
        coleta_message.write("Coletando dados...")
        
        # Executa o script de coleta de dados
        subprocess.run(["python", "scripts/coleta.py"], check=True)
        
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

################################################# SIDEBAR - DASH ATIVIDADES #################################################

def update_sidebar(dashboard_number):
    if dashboard_number == 1:
        st.sidebar.markdown("### Última Atualização")

        # # Exibir a última data e hora de atualização na sidebar
        # if 'ultima_atualizacao' in st.session_state:
        #     st.sidebar.write(f"Atualizado em: {st.session_state['ultima_atualizacao']}")
        # else:
        #     st.sidebar.write("Não disponível")

        # # Adicionar barra lateral
        # st.sidebar.title("Filtros")

        # ################################ DATA ################################

        # # Converter min_value e max_value para datetime.datetime
        # min_value = tarefas["Data"].min().to_pydatetime()  # Converte para datetime.datetime
        # max_value = tarefas["Data"].max().to_pydatetime()  # Converte para datetime.datetime

        # # Aplicando o slider com os valores convertidos
        # data_inicio, data_fim = st.sidebar.slider(
        #     "Selecione o intervalo de datas",
        #     min_value=min_value,
        #     max_value=max_value,
        #     value=(min_value, max_value),  # Valor inicial do slider
        #     format="DD/MM/YYYY",  # Formato de exibição das datas
        #     key="slider_1_1"  # Chave única para o slider
        # )

        # # Agora você pode usar data_inicio e data_fim para filtrar as tarefas
        # tarefas_filtradas = tarefas[(tarefas['Data'] >= data_inicio) & (tarefas['Data'] <= data_fim)]

        # ################################ SETOR ################################

        # # Seção de Filtro por Setor (campo para digitar o número do setor)
        # st.sidebar.subheader("Setor")
        # setor_selecionado = st.sidebar.text_input(
        #     "Digite o número do Setor:", value="", max_chars=5, placeholder="Setor:",
        #     key="input_1_1"  # Chave única para o campo de texto
        # )

        # # Filtro de Setor
        # if setor_selecionado:
        #     tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Setor"].astype(str).str.contains(setor_selecionado)]

        # ################################ STATUS ################################

        # # Seção de Filtro de Status (drop box para selecionar o status)
        # st.sidebar.subheader("Status")
        # status_selecionado = st.sidebar.selectbox(
        #     "Selecione o Status:",
        #     options=["Todos"] + tarefas_filtradas["Status"].unique().tolist(),
        #     index=0,
        #     key="selectbox_1_1"  # Chave única para o selectbox
        # )

        # # Filtro de Status
        # if status_selecionado != "Todos":
        #     tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Status"] == status_selecionado]

        # ################################ COLABORADOR ################################

        # # Seção de Filtro por Pessoas (drop box para selecionar a pessoa)
        # st.sidebar.subheader("Colaborador")
        # pessoa_selecionada = st.sidebar.selectbox(
        #     "Selecione a Pessoa:",
        #     options=["Todos"] + tarefas_filtradas["Colaborador"].unique().tolist(),
        #     index=0,
        #     key="selectbox_1_2"  # Chave única para o selectbox
        # )

        # # Filtro de Pessoas
        # if pessoa_selecionada != "Todos":
        #     tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Colaborador"] == pessoa_selecionada]

        # ################################ TIPO DE PROJETO ################################

        # # Seção de Filtro por Projeto (drop box para selecionar o tipo de projeto)
        # st.sidebar.subheader("Tipo")
        # projeto_selecionado = st.sidebar.selectbox(
        #     "Selecione o Projeto:",
        #     options=["Todos"] + tarefas_filtradas["Tipo"].unique().tolist(),
        #     index=0,
        #     key="selectbox_1_3"  # Chave única para o selectbox
        # )

        # # Filtro de Projeto
        # if projeto_selecionado != "Todos":
        #     tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Tipo"] == projeto_selecionado]

        # ################################ UNIDADE ################################

        # # Seção de Filtro de Unidade (botões para selecionar unidade)
        # st.sidebar.subheader("Unidade")
        # unidade_selecionada = st.sidebar.multiselect(
        #     "Selecione a(s) Unidade(s):",
        #     options=tarefas_filtradas["Unidade"].unique().tolist(),
        #     default=tarefas_filtradas["Unidade"].unique().tolist(),
        #     key="multiselect_1_1"  # Chave única para o multiselect
        # )

        # # Filtro de Unidade
        # if unidade_selecionada:
        #     tarefas_filtradas = tarefas_filtradas[tarefas_filtradas["Unidade"].isin(unidade_selecionada)]

        # # Retorna o DataFrame filtrado
        # return tarefas_filtradas

    ################################################# SIDEBAR - DASH EXTRAS #################################################

    elif dashboard_number == 2:
        st.sidebar.write("Opções específicas do Dashboard 2")

    ################################################# SIDEBAR - DASH AUDITORIA #################################################

    elif dashboard_number == 3:
        st.sidebar.write("Opções específicas do Dashboard 3")

################################################# DASHBOARD - ATIVIDADES #################################################

# Função para o Dashboard 1
def dashboard_1():
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

    # tarefas_filtradas = update_sidebar(dashboard_number=1)  # Aplica os filtros na sidebar
    tarefas_filtradas = tarefas.copy()

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

    # # Layout em colunas
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     total_area = tarefas_filtradas['Area'].sum()
    #     formatted_area = f"{total_area:,.0f}".replace(',', '.')
    #     st.markdown(f"""
    #         <div class="info-box">
    #             <h8><strong>Área Total</strong></h8>
    #             <h3>{formatted_area} ha</h3>
    #         </div>
    #     """, unsafe_allow_html=True)

    # with col2:
    #     st.markdown(f"""
    #         <div class="info-box">
    #             <h8><strong>Quantidade de Atividades</strong></h8>
    #             <h3>{tarefas_filtradas['Colaborador'].size}</h3>
    #         </div>
    #     """, unsafe_allow_html=True)

    # with col3:
    #     st.markdown(f"""
    #         <div class="info-box">
    #             <h8><strong>Colaboradores</strong></h8>
    #             <h3>{tarefas_filtradas['Colaborador'].unique().size}</h3>
    #         </div>
    #     """, unsafe_allow_html=True)

    # Adiciona uma linha horizontal e espaçamento
    st.divider()

################################################# GRÁFICO - COLABORADORES #################################################

        # Gráfico de Atividades por Colaborador
    df_contagem_responsavel = (
        tarefas_filtradas.groupby("Colaborador")["Tipo"].count().reset_index()
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
        text="Quantidade de Projetos",
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
    st.plotly_chart(fig_responsavel, key="fig_responsavel_1")

    # Adiciona uma linha horizontal e espaçamento
    st.divider()

################################################# GRÁFICO - TIPO DE PROJETO #################################################

    # Calcular a quantidade de projetos por tipo no DataFrame filtrado
    df_contagem_tipo = (
        tarefas_filtradas.groupby("Tipo")["Colaborador"].count().reset_index()
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
        tarefas_filtradas.groupby("Status")["Tipo"].count().reset_index()
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

################################################# GRÁFICO - PÓS APLIC #################################################

    # Certifique-se de que a coluna 'DATA' esteja no formato datetime
    pos_aplicacao["DATA"] = pd.to_datetime(pos_aplicacao["DATA"], format="%d/%m/%Y", errors="coerce")

    # Criar um mapeamento de meses para ordenação
    ordem_meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    # Criar a coluna 'MÊS' corretamente formatada em português
    pos_aplicacao["MÊS"] = pos_aplicacao["DATA"].dt.strftime('%B').str.capitalize()

    # Remover duplicatas para considerar apenas setores distintos
    df_unico = pos_aplicacao.drop_duplicates(subset=["MÊS", "SETOR"])

    # Contar quantas vezes cada mês aparece
    df_contagem = df_unico["MÊS"].value_counts().reset_index()
    df_contagem.columns = ["MÊS", "QUANTIDADE"]

    # Criar o gráfico com a ordem correta dos meses
    st.subheader("Mapas de Pós-Aplicação")
    fig_mes = px.bar(
        df_contagem,
        x="QUANTIDADE",
        y="MÊS",
        color="MÊS",
        orientation="h",
        text="QUANTIDADE",
        category_orders={"MÊS": ordem_meses}  # Definir ordem cronológica manualmente
    )

    # Configurar o texto corretamente no gráfico
    fig_mes.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )

    # Ajustar layout
    fig_mes.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )

    fig_mes.update_layout(
        xaxis_title=None,  # Remove o título do eixo X
        yaxis_title=None   # Remove o título do eixo Y
    )

    # Exibir o gráfico
    st.plotly_chart(fig_mes)

    st.divider()

################################################# GRÁFICO - UNIDADE #################################################

    # Calcular a quantidade de projetos por unidade
    df_contagem_unidade = tarefas_filtradas.groupby("Unidade")["Tipo"].count().reset_index()
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

################################################# DASHBOARD - EXTRAS #################################################

# Função para o Dashboard 2
def dashboard_2():
    st.write("### Atividades Extras")

################################################# DASHBOARD - AUDITORIA #################################################

# Função para o Dashboard 3
def dashboard_3():
    st.write("### Auditoria")

################################################# LAYOUT #################################################

# Layout da página
def main():

    # Botões na parte superior para selecionar o dashboard
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Atividades Semanais"):
            st.session_state['dashboard'] = 1
    with col2:
        if st.button("Atividades Extras"):
            st.session_state['dashboard'] = 2
    with col3:
        if st.button("Auditoria"):
            st.session_state['dashboard'] = 3

    # Inicializa o estado da sessão se não existir
    if 'dashboard' not in st.session_state:
        st.session_state['dashboard'] = 1

    # Atualiza o sidebar com base no dashboard selecionado
    update_sidebar(st.session_state['dashboard'])

    # Exibe o dashboard selecionado
    if st.session_state['dashboard'] == 1:
        dashboard_1()
    elif st.session_state['dashboard'] == 2:
        dashboard_2()
    elif st.session_state['dashboard'] == 3:
        dashboard_3()

if __name__ == "__main__":
    main()