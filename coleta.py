import requests
import csv
from datetime import datetime, timedelta, timezone
from auth import obter_token  # Importa a função de autenticação

# Configurar a URL da API para coletar as tarefas
url = "https://graph.microsoft.com/v1.0/planner/plans/MVnlyNS2W0SrUQxwXUPKuWUABICf/tasks"

# Obter os cabeçalhos da autenticação
headers = obter_token()

# Função para coletar as tarefas
def coletar_tarefas():
    response = requests.get(url, headers=headers)

    # Verificar e processar a resposta
    if response.status_code == 200:
        tasks = response.json()

        # Lista para armazenar os dados das tarefas
        data = []

        # Obter a data e hora atual em UTC com fuso horário
        current_date = datetime.now(timezone.utc)

        # Filtrar tarefas dos últimos 30 dias
        for task in tasks.get("value", []):
            # Identificar a categoria
            categories = task.get("appliedCategories", {})
            applied_categories = [key for key, value in categories.items() if value]

            # Converter a data de criação da tarefa
            task_date_str = task.get("createdDateTime")
            task_date = datetime.fromisoformat(task_date_str.replace("Z", "+00:00"))

            # Verificar se a tarefa está dentro dos últimos 30 dias
            if current_date - task_date <= timedelta(days=30):
                # Adicionar os dados da tarefa à lista (usando dicionário)
                data.append({
                    "Setor": task['title'],
                    "Status": task['bucketId'],
                    "Data": task['createdDateTime'],
                    "Colaborador": task['createdBy']['user']['id'],
                    "Tipo": ', '.join(applied_categories) if applied_categories else 'Nenhum'
                })
        return data
    else:
        print("Erro ao obter tarefas:", response.status_code, response.json())
        return []

# Função para processar os dados
def processar_dados(data):
    status_map = {
        "RQhCWnT4M0qf1fC6mVyg3WUAG4NI": "Concluído",
        "ZPwV8CClAUmvCu_zuQaB_GUAFAYR": "Em andamento",
        "57xpzyil_UG7WpTTBMexkGUAM0o5": "A Fazer",
        "Y13R3qmLIUaiUcRJAQyBemUAFKmJ": "A Validar"
    }

    user_map = {
        "80ad7411-e569-4812-9424-d6c33dcdce2b": "Pedro",
        "9a6afc60-29d8-41b3-bc10-33091702a43c": "Márcio",
        "02898f2d-db13-4c60-b39c-2266b503cd7d": "Ana",
        "06deb64d-cd1c-480e-972d-6ba635c245f6": "Willian",
        "8243cac8-c744-4824-b9bf-c87643f1f0ff": "Maico",
        "69b59794-5996-4185-bf2b-979b4b295038": "Camila",
        "5f661255-679b-48a7-8d83-64028e68fdc0": "Gustavo"
    }

    category_map = {
        "category1": "Mapa de Cadastro",
        "category2": "Projeto de Colheita",
        "category3": "Mapa de Sistematização",
        "category4": "Projeto de Sistematização",
        "category5": "Projeto LOC",
        "category6": "Mapa de Pré-Plantio",
        "category7": "Mapa de Pós-Plantio",
        "category8": "Projeto de Sulcação",
        "category9": "Projeto de Fertirrigação",
        "category10": "Auditoria",
        "category11": "Projeto de Transbordo",
        "category12": "Mapa de Pós-Aplicação",
    }

    for row in data:
        # Substitui o ID do status pelo valor correspondente
        row["Status"] = status_map.get(row["Status"], row["Status"])

        # Converte a string de data para um objeto datetime (removendo o "Z" e adicionando "+00:00")
        data_str = row["Data"]
        data_obj = datetime.fromisoformat(data_str.replace("Z", "+00:00"))

        # Formata a data para o formato DD/MM/YYYY
        data_formatada = data_obj.strftime("%d/%m/%Y")
        row["Data"] = data_formatada  # Atualiza o campo de data com o novo formato

        # Substitui o ID do usuário pelo nome correspondente
        row["Colaborador"] = user_map.get(row["Colaborador"], row["Colaborador"])

        # Substitui o ID da categoria pelo nome correspondente
        row["Tipo"] = category_map.get(row["Tipo"], row["Tipo"])

    return data

# Função para salvar os dados em CSV
def salvar_csv(data):
    # Nome do arquivo CSV
    file_name = "tarefas.csv"

    # Cabeçalhos do CSV
    headers = ["Setor", "Status", "Data", "Colaborador", "Tipo"]

    # Escrever no arquivo CSV
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Escreve os cabeçalhos
        writer.writerows(data)  # Escreve os dados processados

    print(f"Arquivo '{file_name}' salvo com sucesso!")

# Função principal para orquestrar o processo
def main():
    tarefas = coletar_tarefas()
    if tarefas:
        dados_processados = processar_dados(tarefas)
        salvar_csv(dados_processados)

if __name__ == "__main__":
    main()