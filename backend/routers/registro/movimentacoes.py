from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db  # função que retorna a sessão do SQLAlchemy
from models import Movimentacoes   # modelo SQLAlchemy da tabela Categoria
from schemas import MovimentacoesCreate, MovimentacoesResponse  # Pydantic para validação de entrada e saída
from logger import get_router_logger

# =========================
# CONFIGURAÇÃO DO ROUTER
# =========================
router = APIRouter(
    prefix="/registro/movimentacoes",
    tags=["Registro - Movimentações"]
)

# Logger específico do router de registro
logger_registro = get_router_logger("movimentacoes", registro=True)


# =========================
# ROTA DE CRIAÇÃO DE Categoria
# =========================
@router.post("/", response_model=MovimentacoesResponse)
def criar_Movimentacao(movimentacoes: MovimentacoesCreate, request: Request, db: Session = Depends(get_db)):
    """
    Cria uma nova categoria na tabela 'movimentacoes'.
    
    Passos:
    1. Recebe os dados validados pelo Pydantic (MovimentacoesCreate)
    2. Verifica se já existe um Categoria com o mesmo nome (unicidade)
    3. Insere no banco se não existir
    4. Retorna o objeto criado (MovimentacoesResponse)
    """

        # 1️.Verificação de existência
    try:

            # 2️. Criação do objeto SQLAlchemy
        nova_movimentacao = Movimentacoes(
                produto_id=movimentacoes.produto_id,
                quantidade=movimentacoes.quantidade,
                data=movimentacoes.data,
                tipo_mov_id=movimentacoes.tipo_mov_id,
                preco_venda=movimentacoes.preco_venda,
                preco_compra=movimentacoes.preco_compra,
                fornecedor_id=movimentacoes.fornecedor_id,
                tipo_pag_id=movimentacoes.tipo_pag_id
                       
            )

            # 3️. Adiciona e confirma no banco
        db.add(nova_movimentacao)
        db.commit()
        db.refresh(nova_movimentacao)  # atualiza o objeto com o ID gerado pelo banco

        # Log de sucesso
        logger_registro.info(
            "Movimentação registrada com sucesso",  # mensagem principal preenchida
            extra={
                "ip": request.client.host,
                "status": 201,
                "method": "POST",
                "detail": f"Movimentação: '{nova_movimentacao}' criada com sucesso"
                }
            )

            # 4️. Retorno do objeto criado (Pydantic converte para JSON)
        return nova_movimentacao

    except SQLAlchemyError as e:
        # Desfaz a transação em caso de erro de banco
        db.rollback()
        logger_registro.error(
            "Erro ao registrar movimentação no banco",  # mensagem principal preenchida
            extra={
                "ip": request.client.host,
                    "status": 500,
                    "method": "POST",
                    "detail": f"Erro ao registrar movimentação (SQLAlchemy): {str(e)}"
                }
            )
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        # Captura outros erros inesperados
        logger_registro.error(
            "Erro inesperado ao registrar movimentação",  # mensagem principal preenchida
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "POST",
                "detail": f"Erro inesperado ao registrar movimentcação: {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
# =========================
# 2. ROTA DE ATUALIZAÇÃO DE MOVIMENTAÇÃO (PUT)
# =========================
@router.put("/{movimentacao_id}", response_model=MovimentacoesResponse, status_code=status.HTTP_200_OK)
def atualizar_movimentacao(
    movimentacao_id: int, 
    movimentacao_update: MovimentacoesCreate, 
    request: Request, 
    db: Session = Depends(get_db)
):
    """
    Atualiza uma movimentação existente na tabela 'movimentacoes' pelo ID.
    
    Passos:
    1. Recebe o ID da movimentação e os novos dados (MovimentacoesCreate).
    2. Busca a movimentação no banco.
    3. Se encontrar, atualiza todos os campos de forma dinâmica.
    4. Se não encontrar, retorna 404.
    """
    try:
        # 1️. Busca a movimentação pelo ID
        db_movimentacao = db.query(Movimentacoes).filter(Movimentacoes.id == movimentacao_id).first()

        if not db_movimentacao:
            logger_registro.warning(
                "Tentativa de atualizar movimentação inexistente",
                extra={
                    "ip": request.client.host,
                    "status": 404,
                    "method": "PUT",
                    "detail": f"Falha ao atualizar Movimentação: ID {movimentacao_id} não encontrado."
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movimentação com ID {movimentacao_id} não encontrada")

        # 2️. Aplica as atualizações em todos os campos de forma dinâmica (Padrão do Cliente)
        update_data = movimentacao_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_movimentacao, key, value)

        # 3️. Confirma no banco
        db.commit()
        db.refresh(db_movimentacao) # atualiza o objeto

        # Log de sucesso
        logger_registro.info(
            "Movimentação atualizada com sucesso",
            extra={
                "ip": request.client.host,
                "status": 200,
                "method": "PUT",
                "detail": f"Movimentação ID {movimentacao_id} atualizada."
            }
        )

        # 4️. Retorno do objeto atualizado
        return db_movimentacao

    except HTTPException:
        # Re-lança exceções HTTP já tratadas (404)
        raise
    
    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao atualizar movimentação no banco",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro ao atualizar movimentação (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger_registro.error(
            "Erro inesperado ao atualizar movimentação",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro inesperado ao atualizar movimentação: {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


# =========================
# 3. ROTA DE EXCLUSÃO DE MOVIMENTAÇÃO (DELETE)
# =========================
@router.delete("/{movimentacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movimentacao(movimentacao_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Deleta uma movimentação existente pelo ID.
    """
    try:
        # 1️. Busca a movimentação pelo ID
        db_item = db.query(Movimentacoes).filter(Movimentacoes.id == movimentacao_id).first()

        if db_item is None:
            logger_registro.warning(
                "Tentativa de deletar movimentação inexistente",
                extra={
                    "ip": request.client.host,
                    "status": 404,
                    "method": "DELETE",
                    "detail": f"Falha ao deletar Movimentação: ID {movimentacao_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movimentação não encontrada."
            )

        # 2️. Deleta e confirma no banco
        db.delete(db_item)
        db.commit()

        # Log de sucesso (204 No Content)
        logger_registro.info(
            "Movimentação excluída com sucesso",
            extra={
                "ip": request.client.host,
                "status": 204,
                "method": "DELETE",
                "detail": f"Movimentação ID {movimentacao_id} excluída com sucesso."
            }
        )
        # Retorno HTTP 204 No Content para exclusão bem-sucedida
        return

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao deletar movimentação no banco",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "DELETE",
                "detail": f"Erro ao deletar Movimentação (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger_registro.error(
            "Erro inesperado ao deletar movimentação",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "DELETE",
                "detail": f"Erro inesperado ao deletar Movimentação: {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")
