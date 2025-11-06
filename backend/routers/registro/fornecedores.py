from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db  # função que retorna a sessão do SQLAlchemy
from models import Fornecedores   # modelo SQLAlchemy da tabela fornecedors
from schemas import FornecedoresCreate, FornecedoresResponse  # Pydantic para validação de entrada e saída
from logger import get_router_logger

# =========================
# CONFIGURAÇÃO DO ROUTER
# =========================
router = APIRouter(
    prefix="/registro/fornecedores",
    tags=["Registro - Fornecedores"]
)

# Logger específico do router de registro
logger_registro = get_router_logger("fornecedores", registro=True)


# =========================
# ROTA DE CRIAÇÃO DE FORNECEDOR
# =========================
@router.post("/", response_model=FornecedoresResponse)
def criar_fornecedor(fornecedor: FornecedoresCreate, request: Request, db: Session = Depends(get_db)):
    """
    Cria um novo fornecedor na tabela 'fornecedors'.
    
    Passos:
    1. Recebe os dados validados pelo Pydantic (fornecedorCreate)
    2. Verifica se já existe um fornecedor com o mesmo razao_social (unicidade)
    3. Insere no banco se não existir
    4. Retorna o objeto criado (fornecedorResponse)
    """
    try:
        # 1️.Verificação de existência
        existente = db.query(Fornecedores).filter(Fornecedores.razao_social == fornecedor.razao_social).first()
        if existente:
            # Log de aviso caso fornecedor já exista
            logger_registro.warning(
                "Tentativa de criar fornecedor existente",
                extra={
                    "ip": request.client.host,
                    "status": 400,
                    "method": "POST",
                    "detail": f"Falha ao criar fornecedor: fornecedor '{fornecedor.razao_social}' já existe"
                }
            )
            raise HTTPException(status_code=400, detail="fornecedor já existe")

        # 2️. Criação do objeto SQLAlchemy
        novo_fornecedor = Fornecedores(
            razao_social=fornecedor.razao_social,
            contato=fornecedor.contato,
            email=fornecedor.email,
            cnpj=fornecedor.cnpj,
            status=fornecedor.status
        )

        # 3️. Adiciona e confirma no banco
        db.add(novo_fornecedor)
        db.commit()
        db.refresh(novo_fornecedor)  # atualiza o objeto com o ID gerado pelo banco

        # Log de sucesso
        logger_registro.info(
            "Fornecedor criado com sucesso",
            extra={
                "ip": request.client.host,
                "status": 201,
                "method": "POST",
                "detail": f"Fornecedor '{novo_fornecedor.razao_social}' criado com sucesso"
            }
        )

        # 4️. Retorno do objeto criado (Pydantic converte para JSON)
        return novo_fornecedor

    except SQLAlchemyError as e:
        # Desfaz a transação em caso de erro de banco
        db.rollback()
        logger_registro.error(
            "Erro ao criar fornecedor no banco",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "POST",
                "detail": f"Erro ao criar fornecedor (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        # Captura outros erros inesperados
        logger_registro.error(
            "Erro inesperado ao criar fornecedor",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "POST",
                "detail": f"Erro inesperado ao criar fornecedor: {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")