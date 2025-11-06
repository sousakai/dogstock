from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config
from logger import get_router_logger


router = APIRouter(
    prefix="/consulta/fornecedores", 
    tags=["Consulta - Tabela fornecedores"]
)

# Logger de consulta - manter registro=false para não cair na pasta de logs de registro
logger_consulta = get_router_logger("fornecedores", registro=False)

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/")


def listar_fornecedores(request: Request):  # request necessário para pegar IP e método
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        
        result = db.execute(text("SELECT * FROM fornecedores ORDER BY razao_social")).fetchall()
        
        logger_consulta.info(
            "",  # mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 200,              # status HTTP
                "method": request.method,   # método HTTP
                "detail": "Listagem de fornecedores realizada com sucesso"  # descrição detalhada
            }
        )

        return [
            {
                "id": row.id,  # o nome definido nas aspas é o nome final que vai ser encontrado pelo JS
                "razao_social": row.razao_social,
                "contato": row.contato,
                "email": row.email,
                "cnpj": row.cnpj,
                "status": row.status
            } 
            for row in result
        ]

    except Exception as e:
        logger_consulta.error(
            "",  # mensagem principal vazia porque usamos 'extra' para detalhes
            extra={
                "ip": request.client.host,  # captura IP do cliente
                "status": 500,              # status HTTP de erro
                "detail": f"Erro ao buscar fornecedores: {str(e)}",  # descrição do erro
                "method": request.method    # método HTTP
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro ao buscar fornecedores: {str(e)}")

    finally:
        db.close()  # fecha a sessão do banco para liberar recursos
