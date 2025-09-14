from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import load_config
from logger import get_router_logger


router = APIRouter(
    prefix="/consulta/categorias", 
    tags=["Consulta - Tabela categorias"]
)

# Logger de consulta - manter registro=false para não cair na pasta de logs de registro
logger_consulta = get_router_logger("categorias", registro=False)

def create_db_session(env_type: str):
    DATABASE_URL, ENV_TYPE = load_config(env_type)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal, ENV_TYPE

@router.get("/")
def listar_categorias(request: Request):
    SessionLocal, ENV_TYPE = create_db_session("leitura")
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT id, descricao FROM categoria ORDER BY descricao")).fetchall()
        
        logger_consulta.info(
            "",
            extra={
                "ip": request.client.host,
                "status": 200,
                "method": request.method,
                "detail": "Listagem de categorias realizada com sucesso"
                
            }
        )

        return [
            {
                "id": row.id,  # o nome definido nas aspas é o nome final que vai ser encontrado pelo JS
                "descricao": row.descricao
            } 
            for row in result
        ]

    except Exception as e:
        logger_consulta.error(
            "",
            extra={
                "ip": request.client.host,
                "status": 500,
                "detail": f"Erro ao buscar categorias: {str(e)}",
                "method": request.method
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categorias: {str(e)}")

    finally:
        db.close()
