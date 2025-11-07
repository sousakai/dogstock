from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db  # função que retorna a sessão do SQLAlchemy
from models import Categoria   # modelo SQLAlchemy da tabela Categoria
# Pydantic para validação de entrada e saída
from schemas import CategoriaCreate, CategoriaResponse
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
        existente = db.query(Categoria).filter(
            Categoria.descricao == categoria.descricao).first()
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
        # atualiza o objeto com o ID gerado pelo banco
        db.refresh(novo_Categoria)

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
        raise HTTPException(
            status_code=500, detail=f"Erro no banco de dados: {str(e)}")

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

# =========================
# ROTA DE ATUALIZAÇÃO DE Categoria (PUT)
# =========================


@router.put("/{categoria_id}", response_model=CategoriaResponse, status_code=status.HTTP_200_OK)
def atualizar_Categoria(
    categoria_id: int,
    categoria_update: CategoriaCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma categoria existente na tabela 'Categorias' pelo ID.

    Passos:
    1. Recebe o ID da categoria a ser atualizada e os novos dados (CategoriaCreate).
    2. Busca a categoria no banco.
    3. Se encontrar, atualiza a descrição (garantindo unicidade).
    4. Se não encontrar, retorna 404.
    """
    try:
        # 1️. Busca a categoria pelo ID
        db_categoria = db.query(Categoria).filter(
            Categoria.id == categoria_id).first()

        if not db_categoria:
            logger_registro.warning(
                "Tentativa de atualizar categoria inexistente",
                extra={
                    "ip": request.client.host,
                    "status": 404,
                    "method": "PUT",
                    "detail": f"Falha ao atualizar Categoria: Categoria ID {categoria_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=404, detail=f"Categoria com ID {categoria_id} não encontrada")

        # 2️. Verifica se a nova descrição já existe em outra categoria (para manter a unicidade)
        if db_categoria.descricao != categoria_update.descricao:
            existente = db.query(Categoria).filter(
                Categoria.descricao == categoria_update.descricao).first()
            if existente and existente.id != categoria_id:
                logger_registro.warning(
                    "Tentativa de atualizar categoria para uma descrição existente",
                    extra={
                        "ip": request.client.host,
                        "status": 400,
                        "method": "PUT",
                        "detail": f"Falha ao atualizar Categoria: Descrição '{categoria_update.descricao}' já existe em outra categoria."
                    }
                )
                raise HTTPException(
                    status_code=400, detail=f"A descrição '{categoria_update.descricao}' já existe em outra categoria.")

        # 3️. Aplica a atualização
        db_categoria.descricao = categoria_update.descricao

        # 4️. Confirma no banco
        db.commit()
        db.refresh(db_categoria)  # atualiza o objeto

        # Log de sucesso
        logger_registro.info(
            "Categoria atualizada com sucesso",
            extra={
                "ip": request.client.host,
                "status": 200,
                "method": "PUT",
                "detail": f"Categoria ID {categoria_id} atualizada para '{db_categoria.descricao}'"
            }
        )

        # 5️. Retorno do objeto atualizado
        return db_categoria

    except HTTPException:
        # Re-lança exceções HTTP já tratadas (404, 400)
        raise

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao atualizar categoria no banco",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro ao atualizar categoria (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(
            status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger_registro.error(
            "Erro inesperado ao atualizar categoria",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro inesperado ao atualizar categoria: {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# 3. DELETAR CATEGORIA (DELETE)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Deleta uma categoria pelo ID.

    Passos:
    1. Busca a categoria pelo ID.
    2. Verifica se a categoria existe.
    3. Deleta do banco e confirma (commit).
    4. Retorna status 204 No Content.
    """
    try:
        # 1. Busca a Categoria pelo ID
        db_item = db.query(Categoria).filter(
            Categoria.id == categoria_id).first()

        if db_item is None:
            logger_registro.warning(
                "Tentativa de deletar Categoria inexistente",
                extra={
                    "ip": request.client.host, "status": 404, "method": "DELETE",
                    "detail": f"Falha ao deletar Categoria: ID {categoria_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada."
            )

        # 2. Deleta e confirma no banco
        db.delete(db_item)
        db.commit()

        logger_registro.info(
            "Categoria excluída com sucesso",
            extra={
                "ip": request.client.host, "status": 204, "method": "DELETE",
                "detail": f"Categoria ID {categoria_id} excluída com sucesso."
            }
        )
        # Retorno HTTP 204 No Content para exclusão bem-sucedida
        return

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao deletar Categoria no banco",
            extra={
                "ip": request.client.host, "status": 500, "method": "DELETE",
                "detail": f"Erro ao deletar Categoria (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger_registro.error(
            "Erro inesperado ao deletar Categoria",
            extra={
                "ip": request.client.host, "status": 500, "method": "DELETE",
                "detail": f"Erro inesperado ao deletar Categoria: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")