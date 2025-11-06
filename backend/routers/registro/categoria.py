from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db  # função que retorna a sessão do SQLAlchemy
from models import Categoria   # modelo SQLAlchemy da tabela Categoria
from schemas import CategoriaCreate, CategoriaResponse  # Pydantic para validação de entrada e saída
from logger import get_router_logger

# =========================
# CONFIGURAÇÃO DO ROUTER
# =========================
router = APIRouter(
    prefix="/registro/categoria",
    tags=["Registro - Categoria"]
)

# Logger específico do router de registro
logger_registro = get_router_logger("categoria", registro=True)


# =========================
# ROTA DE CRIAÇÃO DE Categoria
# =========================
@router.post("/", response_model=CategoriaResponse)
def criar_Categoria(categoria: CategoriaCreate, request: Request, db: Session = Depends(get_db)):
    """
    Cria uma nova categoria na tabela 'Categorias'.
    
    Passos:
    1. Recebe os dados validados pelo Pydantic (CategoriaCreate)
    2. Verifica se já existe um Categoria com o mesmo nome (unicidade)
    3. Insere no banco se não existir
    4. Retorna o objeto criado (CategoriaResponse)
    
    """
    try:
        # 1️.Verificação de existência
        existente = db.query(Categoria).filter(Categoria.descricao == categoria.descricao).first()
        if existente:
            # Log de aviso caso Categoria já exista
            logger_registro.warning(
                "Tentativa de criar categoria existente",  # mensagem principal preenchida
                extra={
                    "ip": request.client.host,
                    "status": 400,
                    "method": "POST",
                    "detail": f"Falha ao criar Categoria: Categoria '{categoria.descricao}' já existe"
                }
            )
            raise HTTPException(status_code=400, detail="Categoria já existe")

        # 2️. Criação do objeto SQLAlchemy
        novo_Categoria = Categoria(
            descricao=categoria.descricao            
        )

        # 3️. Adiciona e confirma no banco
        db.add(novo_Categoria)
        db.commit()
        db.refresh(novo_Categoria)  # atualiza o objeto com o ID gerado pelo banco

        # Log de sucesso
        logger_registro.info(
            "Categoria criada com sucesso",  # mensagem principal preenchida
            extra={
                "ip": request.client.host,
                "status": 201,
                "method": "POST",
                "detail": f"Categoria '{novo_Categoria.descricao}' criada com sucesso"
            }
        )

        # 4️. Retorno do objeto criado (Pydantic converte para JSON)
        return novo_Categoria

    except SQLAlchemyError as e:
        # Desfaz a transação em caso de erro de banco
        db.rollback()
        logger_registro.error(
            "Erro ao criar categoria no banco",  # mensagem principal preenchida
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "POST",
                "detail": f"Erro ao criar categoria (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        # Captura outros erros inesperados
        logger_registro.error(
            "Erro inesperado ao criar categoria",  # mensagem principal preenchida
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "POST",
                "detail": f"Erro inesperado ao criar categoria: {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
