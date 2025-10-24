from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Importado para tratamento de erro de banco
from sqlalchemy.exc import SQLAlchemyError
from typing import List

# Importa o modelo e os schemas
# ATENÇÃO: Verifique se os nomes 'TipoMovimentacao', 'TipoMovimentacaoCreateSchema', 'TipoMovimentacaoResponseSchema' estão corretos
from models import TipoMovimentacao
from schemas import TipoMovimentacaoCreateSchema, TipoMovimentacaoResponseSchema
from database import get_db  # Dependência para obter a sessão de DB
from logger import get_router_logger  # Importa o sistema de logger

# =========================
# CONFIGURAÇÃO DO ROUTER
# =========================
router = APIRouter(
    prefix="/registro/tipomovimentacao",
    tags=["Registro - Tipo Movimentação (CRUD)"]
)

# Logger específico do router de registro
logger_registro = get_router_logger("tipo_movimentacao", registro=True)


# =========================
# ROTAS DE REGISTRO (CRUD)
# =========================

# 1. CRIAR NOVO TIPO DE MOVIMENTAÇÃO (POST)
@router.post("/", response_model=TipoMovimentacaoResponseSchema, status_code=status.HTTP_201_CREATED)
def create_tipo_movimentacao(
    tipo_movimentacao: TipoMovimentacaoCreateSchema,
    db: Session = Depends(get_db)  # Injeta a sessão de banco de dados
):
    """
    Cria um novo tipo de movimentação no banco de dados.
    Inclui verificação de unicidade pela descrição.
    """
    try:
        # 1️. Verificação de unicidade pela 'descricao'
        existente = db.query(TipoMovimentacao).filter(
            TipoMovimentacao.descricao == tipo_movimentacao.descricao
        ).first()

        if existente:
            # Log de aviso caso já exista
            logger_registro.warning(
                "",
                extra={
                    "ip": "N/A", "status": 400, "method": "POST",
                    "detail": f"Falha ao criar Tipo Movimentação: '{tipo_movimentacao.descricao}' já existe"
                }
            )
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Tipo de Movimentação já existe")

        # 2️. Cria a instância do modelo - O Pydantic V2 (model_dump()) agora só tem 'descricao'
        db_item = TipoMovimentacao(**tipo_movimentacao.model_dump())

        # 3️. Adiciona e confirma no banco
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        # Log de sucesso
        logger_registro.info(
            "",
            extra={
                "ip": "N/A", "status": 201, "method": "POST",
                "detail": f"Tipo Movimentação '{tipo_movimentacao.descricao}' criado com sucesso (ID: {db_item.id})"
            }
        )

        return db_item

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "POST",
                "detail": f"Erro ao criar Tipo Movimentação (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "POST",
                "detail": f"Erro inesperado ao criar Tipo Movimentação: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


# 2. ATUALIZAR TIPO DE MOVIMENTAÇÃO (PUT)
@router.put("/{tipo_movimentacao_id}", response_model=TipoMovimentacaoResponseSchema)
def update_tipo_movimentacao(
    tipo_movimentacao_id: int,
    # Usa o schema Create, que só tem 'descricao'
    tipo_movimentacao: TipoMovimentacaoCreateSchema,
    db: Session = Depends(get_db)
):
    """
    Atualiza as informações de um tipo de movimentação existente pelo ID.
    """
    try:
        db_item = db.query(TipoMovimentacao).filter(
            TipoMovimentacao.id == tipo_movimentacao_id).first()

        if db_item is None:
            logger_registro.warning(
                "",
                extra={
                    "ip": "N/A", "status": 404, "method": "PUT",
                    "detail": f"Falha ao atualizar Tipo Movimentação: ID {tipo_movimentacao_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de Movimentação não encontrado."
            )

        # Atualiza os campos do modelo (apenas 'descricao')
        for key, value in tipo_movimentacao.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)

        logger_registro.info(
            "",
            extra={
                "ip": "N/A", "status": 200, "method": "PUT",
                "detail": f"Tipo Movimentação ID {tipo_movimentacao_id} atualizado com sucesso."
            }
        )
        return db_item

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "PUT",
                "detail": f"Erro ao atualizar Tipo Movimentação (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "PUT",
                "detail": f"Erro inesperado ao atualizar Tipo Movimentação: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


# 3. DELETAR TIPO DE MOVIMENTAÇÃO (DELETE)
@router.delete("/{tipo_movimentacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_movimentacao(tipo_movimentacao_id: int, db: Session = Depends(get_db)):
    """
    Deleta um tipo de movimentação pelo ID.
    """
    try:
        db_item = db.query(TipoMovimentacao).filter(
            TipoMovimentacao.id == tipo_movimentacao_id).first()

        if db_item is None:
            logger_registro.warning(
                "",
                extra={
                    "ip": "N/A", "status": 404, "method": "DELETE",
                    "detail": f"Falha ao deletar Tipo Movimentação: ID {tipo_movimentacao_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de Movimentação não encontrado."
            )

        db.delete(db_item)
        db.commit()

        logger_registro.info(
            "",
            extra={
                "ip": "N/A", "status": 204, "method": "DELETE",
                "detail": f"Tipo Movimentação ID {tipo_movimentacao_id} excluído com sucesso."
            }
        )
        # Retorno HTTP 204 No Content para exclusão bem-sucedida
        return

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "DELETE",
                "detail": f"Erro ao deletar Tipo Movimentação (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "DELETE",
                "detail": f"Erro inesperado ao deletar Tipo Movimentação: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")
