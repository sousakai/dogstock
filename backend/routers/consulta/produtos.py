from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config
from logger import get_router_logger

router = APIRouter(
    prefix="/consulta/produtos", 
    tags=["Consulta - Tabela produtos"]) 


# Logger de consulta - manter registro=false para não cair na pasta de logs de registro
logger_consulta = get_router_logger("produtos", registro=False)

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/")


def listar_produtos(request: Request):
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM produtos ORDER BY id")).fetchall()
        
        logger_consulta.info(
            "",  #mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 200,              # status HTTP
                "method": request.method,   #  método HTTP
                "detail": "Listagem de produtos realizada com sucesso"  
            }
        )
        
        
        return [{"id": row.id,  #o nome definido nas aspas é o nome final que vai ser encontrado pelo JS, independentemente do nome da tabela.
                 "nome": row.nome, 
                 "medida": row.medida, 
                 "qtd_disponivel": row.qtd_disponivel,
                 "qtd_minima": row.qtd_minima, 
                 "categoria_id": row.categoria_id,
                 "status": row.status
                 } for row in result]
    except Exception as e:
        logger_consulta.error(
            "",  #mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 500,              # status HTTP de erro
                "detail": f"Erro ao buscar produtos: {str(e)}",  # descrição do erro
                "method": request.method    # método HTTP
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {str(e)}")

    finally:
        db.close()