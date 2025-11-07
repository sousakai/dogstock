import os
from dotenv import load_dotenv

def load_config(env_type: str):
    """
    Carrega o .env correto (leitura ou escrita) e retorna a URL do banco
    e o tipo de ambiente.
    """
    # Garante que o caminho seja relativo à pasta do projeto
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    dotenv_path = os.path.join(base_dir, "envs", f".env.{env_type}")


    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"{dotenv_path} não encontrado")

    load_dotenv(dotenv_path)

    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")

    if not all([DB_HOST, DB_NAME, DB_USER, DB_PASS]):
        raise ValueError(f"Alguma variável de {dotenv_path} não está definida corretamente.")

    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    return DATABASE_URL, env_type
    print(f"[DEBUG] carregando env: {dotenv_path}")



