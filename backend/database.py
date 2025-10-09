# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import load_config

# -------------------------------------------------------------------
# Carrega a URL do banco a partir do config (que lê o .env)
# Aqui você escolhe qual ambiente (ex: "escrita", "leitura", etc.)
# -------------------------------------------------------------------
DATABASE_URL = load_config("escrita")[0]   # retorna a URL do banco

# -------------------------------------------------------------------
# Cria a "engine" = a conexão com o banco em si
# Ela é responsável por traduzir os comandos Python -> SQL real
# -------------------------------------------------------------------
engine = create_engine(DATABASE_URL)

# -------------------------------------------------------------------
# Cria a "SessionLocal"
# A sessão é um objeto que representa uma transação com o banco.
# É através dela que fazemos SELECT, INSERT, UPDATE, DELETE.
# "autoflush=False" = não manda query automática antes da hora
# "autocommit=False" = só confirma quando chamamos db.commit()
# -------------------------------------------------------------------
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# -------------------------------------------------------------------
# Declarative Base
# É daqui que todos os models (classes do banco) vão herdar.
# O SQLAlchemy usa isso pra saber quais tabelas existem.
# -------------------------------------------------------------------
Base = declarative_base()

# -------------------------------------------------------------------
# Função de dependência do FastAPI
# Toda vez que um endpoint precisar acessar o banco,
# ele chama get_db(), que abre uma sessão e depois fecha.
# Assim não deixamos conexões penduradas.
# -------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()