from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db  # função que retorna a sessão do SQLAlchemy
from models import Fornecedores   # modelo SQLAlchemy da tabela fornecedors
# Pydantic para validação de entrada e saída
from schemas import FornecedoresCreate, FornecedoresResponse
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
        existente = db.query(Fornecedores).filter(
            Fornecedores.razao_social == fornecedor.razao_social).first()
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
        # atualiza o objeto com o ID gerado pelo banco
        db.refresh(novo_fornecedor)

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
        raise HTTPException(
            status_code=500, detail=f"Erro no banco de dados: {str(e)}")

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

    # =========================
# ROTA DE ATUALIZAÇÃO DE FORNECEDOR (PUT)
# =========================


@router.put("/{fornecedor_id}", response_model=FornecedoresResponse, status_code=status.HTTP_200_OK)
def atualizar_fornecedor(
    fornecedor_id: int,
    fornecedor_update: FornecedoresCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Atualiza um fornecedor existente na tabela 'fornecedores' pelo ID.

    Passos:
    1. Recebe o ID do fornecedor a ser atualizado e os novos dados (FornecedoresCreate).
    2. Busca o fornecedor no banco.
    3. Se encontrar, atualiza todos os campos (garantindo unicidade de razao_social se for alterada).
    4. Se não encontrar, retorna 404.
    """
    try:
        # 1️. Busca o fornecedor pelo ID
        db_fornecedor = db.query(Fornecedores).filter(
            Fornecedores.id == fornecedor_id).first()

        if not db_fornecedor:
            logger_registro.warning(
                "Tentativa de atualizar fornecedor inexistente",
                extra={
                    "ip": request.client.host,
                    "status": 404,
                    "method": "PUT",
                    "detail": f"Falha ao atualizar Fornecedor: ID {fornecedor_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=404, detail=f"Fornecedor com ID {fornecedor_id} não encontrado")

        # 2️. Verifica se a nova razao_social já existe em outro fornecedor (para manter a unicidade)
        if db_fornecedor.razao_social != fornecedor_update.razao_social:
            existente = db.query(Fornecedores).filter(
                Fornecedores.razao_social == fornecedor_update.razao_social).first()
            if existente and existente.id != fornecedor_id:
                logger_registro.warning(
                    "Tentativa de atualizar fornecedor para uma razao_social existente",
                    extra={
                        "ip": request.client.host,
                        "status": 400,
                        "method": "PUT",
                        "detail": f"Falha ao atualizar Fornecedor: Razão Social '{fornecedor_update.razao_social}' já existe."
                    }
                )
                raise HTTPException(
                    status_code=400, detail=f"A Razão Social '{fornecedor_update.razao_social}' já existe.")

        # 3️. Aplica as atualizações em todos os campos
        db_fornecedor.razao_social = fornecedor_update.razao_social
        db_fornecedor.contato = fornecedor_update.contato
        db_fornecedor.email = fornecedor_update.email
        db_fornecedor.cnpj = fornecedor_update.cnpj
        db_fornecedor.status = fornecedor_update.status

        # 4️. Confirma no banco
        db.commit()
        db.refresh(db_fornecedor)  # atualiza o objeto

        # Log de sucesso
        logger_registro.info(
            "Fornecedor atualizado com sucesso",
            extra={
                "ip": request.client.host,
                "status": 200,
                "method": "PUT",
                "detail": f"Fornecedor ID {fornecedor_id} atualizado."
            }
        )

        # 5️. Retorno do objeto atualizado
        return db_fornecedor

    except HTTPException:
        # Re-lança exceções HTTP já tratadas (404, 400)
        raise

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao atualizar fornecedor no banco",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro ao atualizar fornecedor (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(
            status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger_registro.error(
            "Erro inesperado ao atualizar fornecedor",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro inesperado ao atualizar fornecedor: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=500, detail=f"Erro interno: {str(e)}")

# =======================================================
# 3. ROTA DE EXCLUSÃO DE FORNECEDOR (DELETE)
# =======================================================


@router.delete("/{fornecedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fornecedor(fornecedor_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Deleta um fornecedor existente pelo ID.

    Passos:
    1. Busca o fornecedor pelo ID, usando o modelo Fornecedor (com 'F' maiúsculo).
    2. Verifica se o fornecedor existe.
    3. Deleta do banco e confirma (commit).
    4. Retorna status 204 No Content.
    """
    try:
        # 1. Busca o Fornecedor pelo ID
        db_item = db.query(Fornecedores).filter(
            Fornecedores.id == fornecedor_id).first()

        if db_item is None:
            logger_registro.warning(
                "Tentativa de deletar Fornecedor inexistente",
                extra={
                    "ip": request.client.host, "status": 404, "method": "DELETE",
                    "detail": f"Falha ao deletar Fornecedor: ID {fornecedor_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fornecedor não encontrado."
            )

        # 2. Deleta e confirma no banco
        db.delete(db_item)
        db.commit()

        logger_registro.info(
            "Fornecedor excluído com sucesso",
            extra={
                "ip": request.client.host, "status": 204, "method": "DELETE",
                "detail": f"Fornecedor ID {fornecedor_id} excluído com sucesso."
            }
        )
        # Retorno HTTP 204 No Content para exclusão bem-sucedida
        return

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao deletar Fornecedor no banco",
            extra={
                "ip": request.client.host, "status": 500, "method": "DELETE",
                "detail": f"Erro ao deletar Fornecedor (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger_registro.error(
            "Erro inesperado ao deletar Fornecedor",
            extra={
                "ip": request.client.host, "status": 500, "method": "DELETE",
                "detail": f"Erro inesperado ao deletar Fornecedor: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")