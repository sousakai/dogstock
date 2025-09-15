from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config
from logger import get_router_logger

router = APIRouter(
    prefix="/consulta/movimentacoes", 
    tags=["Consulta - Tabela movimentacoes"]) 

# Logger de consulta - manter registro=false para não cair na pasta de logs de registro
logger_consulta = get_router_logger("movimentacoes", registro=False)

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/")
def listar_movimentacoes(request: Request):
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT * FROM movimentacoes ORDER BY id")).fetchall() 
        
        logger_consulta.info(
            "",  #mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 200,              # status HTTP
                "method": request.method,   # método HTTP
                "detail": "Listagem de movimentacoes realizada com sucesso"  # descrição detalhada
            }
        )
        
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
        logger_consulta.error(
            "",  # mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 500,              # status HTTP de erro
                "detail": f"Erro ao buscar movimentacoes: {str(e)}",  # descrição do erro
                "method": request.method    # método HTTP
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro ao buscar movimentacoes: {str(e)}")

    finally:
        db.close()
