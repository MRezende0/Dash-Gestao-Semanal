import pandas as pd

def load_data(file_path):
    """Carrega uma base de dados CSV."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise FileNotFoundError(f"Erro ao carregar o arquivo {file_path}: {e}")