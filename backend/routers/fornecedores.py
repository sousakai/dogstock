from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config

router = APIRouter()

def create_db_session(env_type: str):
    emailBASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(emailBASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/fornecedores")
def listar_movimentacoes():
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM fornecedores ORDER BY id")).fetchall() 
        return [
            {
                "id": row.id,
                "nome": row.nome, 
                "contato": row.contato, 
                "email": row.email,
                "cnpj": row.cnpj, 
                "status": row.status
            } for row in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categorias: {str(e)}")
    finally:
        db.close()
