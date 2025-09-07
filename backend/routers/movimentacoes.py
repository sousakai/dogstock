from fastapi import APIRouter, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config

router = APIRouter()

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/movimentacoes")
def listar_movimentacoes():
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM movimentacoes ORDER BY id")).fetchall() 
        return [
            {
                "id": row.id, #o nome definido nas aspas é o nome final que vai ser encontrado pelo JS, independentemente do nome da tabela.
                "produto_id": row.produto_id, 
                "quantidade": row.quantidade, 
                "data": row.data,
                "tipo_mov_id": row.tipo_mov_id, 
                "preco_venda": row.preco_venda,
                "preco_compra": row.preco_compra,  
                "fornecedor_id": row.fornecedor_id, 
                "tipo_pag_id": row.tipo_pag_id
            } for row in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar movimentações: {str(e)}")
    finally:
        db.close()
