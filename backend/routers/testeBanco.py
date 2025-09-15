from fastapi import APIRouter
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config

router = APIRouter()

def create_db_session(env_type: str):
    """Cria engine e session para o env_type especificado"""
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/teste-db")
def teste_db():
    resultados = {}
    for env in ["leitura", "escrita", "admin", "powerbi"]:
        SessionLocal, ENV_TYPE = create_db_session(env)
        db = SessionLocal()
        try:
            # SQLAlchemy 2.x exige text() para queries textuais
            result = db.execute(text("SELECT 1")).fetchone()
            resultados[ENV_TYPE] = {"status": "ok", "result": result[0]}
        except Exception as e:
            resultados[ENV_TYPE] = {"status": "erro", "mensagem": str(e)}
        finally:
            db.close()
    return resultados