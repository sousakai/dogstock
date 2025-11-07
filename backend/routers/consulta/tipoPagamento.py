from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config
from logger import get_router_logger

router = APIRouter(
    prefix="/consulta/tipopagamento",
    tags=["Consulta - Tabela tipo_pagamento"]
)


logger_consulta = get_router_logger("tipo_pagamento", registro=False)

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/")
def listar_pagamentos(request: Request):
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(
            text("SELECT id, descricao, status FROM tipo_pagamento ORDER BY id")
        ).fetchall()

        logger_consulta.info(
            "",  
            extra={
                "ip": request.client.host,  
                "status": 200,              
                "method": request.method, 
                "detail": "Listagem de tipos de pagamento realizada com sucesso"
            }
        )

        return [
            {"id": row.id, "descricao": row.descricao, "status": row.status}  # Adicionado 'status'
            for row in result
        ]
    except Exception as e:
        logger_consulta.error(
            "",  # mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 500,              # status HTTP
                "method": request.method,  # método HTTP
                "detail": f"Erro ao listar tipos de pagamento: {str(e)}"  # Correção no log
            }
        )
        raise HTTPException(
            status_code=500, detail=f"Erro interno ao buscar tipos de pagamento: {str(e)}"
        )
    finally:
        db.close()