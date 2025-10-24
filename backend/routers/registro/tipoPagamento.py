from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

# Importa o modelo e os schemas
from models import TipoPagamento  # Ajuste o nome conforme seu models.py
from schemas import TipoPagamentoCreate, TipoPagamentoResponse  # Ajuste os nomes conforme seu schemas.py
from database import get_db
from logger import get_router_logger

# Configuração do Router
router = APIRouter(
    prefix="/registro/tipopagamento",
    tags=["Registro - Tipo Pagamento (CRUD)"]
)

# Logger específico do router de registro
logger_registro = get_router_logger("tipo_pagamento", registro=True)

# 1. CRIAR NOVO TIPO DE PAGAMENTO (POST)
@router.post("/", response_model=TipoPagamentoResponse, status_code=status.HTTP_201_CREATED)
def create_tipo_pagamento(
    tipo_pagamento: TipoPagamentoCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo tipo de pagamento no banco de dados.
    Inclui verificação de unicidade pela descrição.
    """
    try:
        # Verificação de unicidade pela 'descricao'
        existente = db.query(TipoPagamento).filter(
            TipoPagamento.descricao == tipo_pagamento.descricao
        ).first()

        if existente:
            logger_registro.warning(
                "",
                extra={
                    "ip": "N/A", "status": 400, "method": "POST",
                    "detail": f"Falha ao criar Tipo Pagamento: '{tipo_pagamento.descricao}' já existe"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de Pagamento já existe"
            )

        # Cria a instância do modelo
        db_item = TipoPagamento(**tipo_pagamento.model_dump())

        # Adiciona e confirma no banco
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        logger_registro.info(
            "",
            extra={
                "ip": "N/A", "status": 201, "method": "POST",
                "detail": f"Tipo Pagamento '{tipo_pagamento.descricao}' criado com sucesso (ID: {db_item.id})"
            }
        )

        return db_item

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "POST",
                "detail": f"Erro ao criar Tipo Pagamento (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "POST",
                "detail": f"Erro inesperado ao criar Tipo Pagamento: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

# 2. ATUALIZAR TIPO DE PAGAMENTO (PUT)
@router.put("/{tipo_pagamento_id}", response_model=TipoPagamentoResponse)
def update_tipo_pagamento(
    tipo_pagamento_id: int,
    tipo_pagamento: TipoPagamentoCreate,
    db: Session = Depends(get_db)
):
    """
    Atualiza as informações de um tipo de pagamento existente pelo ID.
    """
    try:
        db_item = db.query(TipoPagamento).filter(
            TipoPagamento.id == tipo_pagamento_id
        ).first()

        if db_item is None:
            logger_registro.warning(
                "",
                extra={
                    "ip": "N/A", "status": 404, "method": "PUT",
                    "detail": f"Falha ao atualizar Tipo Pagamento: ID {tipo_pagamento_id} não encontrado"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de Pagamento não encontrado"
            )

        # Atualiza os campos do modelo
        for key, value in tipo_pagamento.model_dump(exclude_unset=True).items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)

        logger_registro.info(
            "",
            extra={
                "ip": "N/A", "status": 200, "method": "PUT",
                "detail": f"Tipo Pagamento ID {tipo_pagamento_id} atualizado com sucesso"
            }
        )
        return db_item

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "PUT",
                "detail": f"Erro ao atualizar Tipo Pagamento (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "PUT",
                "detail": f"Erro inesperado ao atualizar Tipo Pagamento: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )

# 3. DELETAR TIPO DE PAGAMENTO (DELETE)
@router.delete("/{tipo_pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_pagamento(
    tipo_pagamento_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um tipo de pagamento pelo ID.
    """
    try:
        db_item = db.query(TipoPagamento).filter(
            TipoPagamento.id == tipo_pagamento_id
        ).first()

        if db_item is None:
            logger_registro.warning(
                "",
                extra={
                    "ip": "N/A", "status": 404, "method": "DELETE",
                    "detail": f"Falha ao deletar Tipo Pagamento: ID {tipo_pagamento_id} não encontrado"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tipo de Pagamento não encontrado"
            )

        db.delete(db_item)
        db.commit()

        logger_registro.info(
            "",
            extra={
                "ip": "N/A", "status": 204, "method": "DELETE",
                "detail": f"Tipo Pagamento ID {tipo_pagamento_id} excluído com sucesso"
            }
        )
        return  # Retorno HTTP 204 No Content

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "DELETE",
                "detail": f"Erro ao deletar Tipo Pagamento (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": "N/A", "status": 500, "method": "DELETE",
                "detail": f"Erro inesperado ao deletar Tipo Pagamento: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )