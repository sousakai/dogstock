from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config
from logger import get_router_logger

router = APIRouter(
    prefix="/consulta/tipomovimentacao", 
    tags=["Consulta - Tabela tipo_movimentacao"]) 

# Logger de consulta - manter registro=false para não cair na pasta de logs de registro
logger_consulta = get_router_logger("tipo_mov", registro=False)

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/")


def listar_tipoMovimentacao(request: Request):
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM tipo_movimentacao ORDER BY id")).fetchall()
        
        logger_consulta.info(
            "",  #mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 200,              # status HTTP
                "method": request.method,   #  método HTTP
                "detail": "Listagem de tipo de movimentação realizada com sucesso"  
            }
        )
        return [{"id": row.id, 
                 "descricao": row.descricao #o nome definido nas aspas é o nome final que vai ser encontrado pelo JS, independentemente do nome da tabela.
                 } for row in result]
        
    except Exception as e:
        logger_consulta.error(
            "",  #mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 500,              # status HTTP
                "method": request.method,   #  método HTTP
                "detail": "Listagem de tipo de movimentação realizada com sucesso"  
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro ao buscar tipo de movimentação: {str(e)}")
    finally:
        db.close()

