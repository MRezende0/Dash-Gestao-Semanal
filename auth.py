import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para obter o token de acesso
def obter_token():
    # Token obtido a partir do arquivo .env
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    if not ACCESS_TOKEN:
        raise ValueError("O token de acesso não foi encontrado. Verifique o arquivo .env.")

    # Configurar cabeçalhos da requisição
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    return headers