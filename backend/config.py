import os
from dotenv import load_dotenv

def load_config(env_type: str):
    """
    Carrega o .env correto (leitura ou escrita) e retorna a URL do banco
    e o tipo de ambiente.
    """
    dotenv_path = f".env.{env_type}"
    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f"{dotenv_path} não encontrado")

    load_dotenv(dotenv_path)

    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")

    if not all([DB_HOST, DB_NAME, DB_USER, DB_PASS]):
        raise ValueError(f"Alguma variável de {dotenv_path} não está definida corretamente.")

    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    return DATABASE_URL, env_type
