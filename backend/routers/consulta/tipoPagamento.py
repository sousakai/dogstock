from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config

router = APIRouter(prefix="/consulta/tipopagamento", tags=["Consulta - Tabela tipo_pagamento"]) 

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/")


def listar_pagamentos():
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM tipo_pagamento ORDER BY id")).fetchall()
        return [{"id": row.id, #o nome definido nas aspas é o nome final que vai ser encontrado pelo JS, independentemente do nome da tabela.
                 "descricao": row.descricao
                 } for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar tipos de pagamento: {str(e)}")
    finally:
        db.close()

