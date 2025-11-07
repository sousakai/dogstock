from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db  # função que retorna a sessão do SQLAlchemy
from models import Produto, Movimentacoes  # modelo SQLAlchemy da tabela produtos
from schemas import ProdutoCreate, ProdutoResponse  # Pydantic para validação de entrada e saída
from logger import get_router_logger

# =========================
# CONFIGURAÇÃO DO ROUTER
# =========================
router = APIRouter(
    prefix="/registro/produtos",
    tags=["Registro - Produtos"]
)

# Logger específico do router de registro
logger_registro = get_router_logger("produtos", registro=True)


# =========================
# ROTA DE CRIAÇÃO DE PRODUTO
# =========================
@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto: ProdutoCreate, request: Request, db: Session = Depends(get_db)):
    """
    Cria um novo produto na tabela 'produtos'.
    
    Passos:
    1. Recebe os dados validados pelo Pydantic (ProdutoCreate)
    2. Estabelece a sessão com o banco via dependência da tabela categoria
    3. Verifica se já existe um produto com o mesmo nome (unicidade)
    4. Insere no banco se não existir
    5. Retorna o objeto criado (ProdutoResponse)
    """
    try:
        # 1️.Verificação de existência
        existente = db.query(Produto).filter(Produto.nome == produto.nome).first()
        if existente:
            # Log de aviso caso produto já exista
            logger_registro.warning(
                "",
                extra={
                    "ip": request.client.host,
                    "status": 400,
                    "method": "POST",
                    "detail": f"Falha ao criar produto: Produto '{produto.nome}' já existe"
                }
            )
            raise HTTPException(status_code=400, detail="Produto já existe")

        # 2️. Criação do objeto SQLAlchemy
        novo_produto = Produto(
            nome=produto.nome,
            medida=produto.medida,
            qtd_disponivel=produto.qtd_disponivel,
            qtd_minima=produto.qtd_minima,
            categoria_id=produto.categoria_id,
            status=produto.status or "ativo"  # se não passar status, usa "ativo"
        )

        # 3️. Adiciona e confirma no banco
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)  # atualiza o objeto com o ID gerado pelo banco

        # Log de sucesso
        logger_registro.info(
            "",
            extra={
                "ip": request.client.host,
                "status": 201,
                "method": "POST",
                "detail": f"Produto '{produto.nome}' criado com sucesso"
            }
        )

        # 4️. Retorno do objeto criado (Pydantic converte para JSON)
        return novo_produto

    except SQLAlchemyError as e:
        # Desfaz a transação em caso de erro de banco
        db.rollback()
        logger_registro.error(
            "",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "POST",
                "detail": f"Erro ao criar produto (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        # Captura outros erros inesperados
        logger_registro.error(
            "",
            extra={
                "ip": "N/A",
                "status": 500,
                "method": "POST",
                "detail": f"Erro inesperado ao criar produto: {str(e)}"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# =========================
# 2. ROTA DE ATUALIZAÇÃO DE PRODUTO (PUT)
# =========================
@router.put("/{produto_id}", response_model=ProdutoResponse, status_code=status.HTTP_200_OK)
def atualizar_produto(
    produto_id: int, 
    produto_update: ProdutoCreate, 
    request: Request, 
    db: Session = Depends(get_db)
):
    """
    Atualiza um produto existente na tabela 'produtos' pelo ID.
    
    Passos:
    1. Busca o produto pelo ID.
    2. Verifica se o novo nome (se fornecido) já existe em OUTRO produto.
    3. Aplica as atualizações dinamicamente.
    """
    try:
        # 1. Busca o produto pelo ID
        db_produto = db.query(Produto).filter(Produto.id == produto_id).first()

        if not db_produto:
            logger_registro.warning(
                "Tentativa de atualizar produto inexistente",
                extra={
                    "ip": request.client.host,
                    "status": 404,
                    "method": "PUT",
                    "detail": f"Falha ao atualizar Produto: ID {produto_id} não encontrado."
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto com ID {produto_id} não encontrado")

        # 2. Verifica a unicidade do nome (se o nome foi alterado)
        if produto_update.nome and produto_update.nome != db_produto.nome:
            existente_com_novo_nome = db.query(Produto).filter(Produto.nome == produto_update.nome).first()
            if existente_com_novo_nome:
                logger_registro.warning(
                    "Tentativa de alterar nome para um produto já existente",
                    extra={
                        "ip": request.client.host,
                        "status": 400,
                        "method": "PUT",
                        "detail": f"Falha ao atualizar Produto: Nome '{produto_update.nome}' já existe."
                    }
                )
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Produto com nome '{produto_update.nome}' já existe.")


        # 3. Aplica as atualizações em todos os campos de forma dinâmica
        update_data = produto_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            # Garante que status use 'ativo' como padrão se for nulo na atualização
            if key == 'status' and value is None:
                value = "ativo"
            setattr(db_produto, key, value)

        # 4. Confirma no banco
        db.commit()
        db.refresh(db_produto) # atualiza o objeto

        # Log de sucesso
        logger_registro.info(
            "Produto atualizado com sucesso",
            extra={
                "ip": request.client.host,
                "status": 200,
                "method": "PUT",
                "detail": f"Produto ID {produto_id} ('{db_produto.nome}') atualizado."
            }
        )

        # 5. Retorno do objeto atualizado
        return db_produto

    except HTTPException:
        # Re-lança exceções HTTP já tratadas (404, 400)
        raise
    
    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao atualizar produto no banco",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro ao atualizar produto (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger_registro.error(
            "Erro inesperado ao atualizar produto",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "PUT",
                "detail": f"Erro inesperado ao atualizar produto: {str(e)}"
            }
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(e)}")


# =========================
# 3. ROTA DE EXCLUSÃO DE PRODUTO (DELETE)
# =========================
@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(produto_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Deleta um produto existente pelo ID.
    Não permite exclusão se houver movimentações associadas.
    """
    try:
        # 1. Busca o produto pelo ID
        db_item = db.query(Produto).filter(Produto.id == produto_id).first()

        if db_item is None:
            logger_registro.warning(
                "Tentativa de deletar produto inexistente",
                extra={
                    "ip": request.client.host,
                    "status": 404,
                    "method": "DELETE",
                    "detail": f"Falha ao deletar Produto: ID {produto_id} não encontrado."
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado."
            )

        # 2. Verificar se existem movimentações associadas
        movimentacoes_count = db.query(Movimentacoes).filter(
            Movimentacoes.produto_id == produto_id
        ).count()
        
        if movimentacoes_count > 0:
            logger_registro.warning(
                "Tentativa de deletar produto com movimentações",
                extra={
                    "ip": request.client.host,
                    "status": 400,
                    "method": "DELETE",
                    "detail": f"Produto ID {produto_id} possui {movimentacoes_count} movimentação(ões) associada(s)."
                }
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não é possível excluir este produto pois ele possui {movimentacoes_count} movimentação(ões) associada(s)."
            )

        # 3. Deleta e confirma no banco
        db.delete(db_item)
        db.commit()

        # Log de sucesso (204 No Content)
        logger_registro.info(
            "Produto excluído com sucesso",
            extra={
                "ip": request.client.host,
                "status": 204,
                "method": "DELETE",
                "detail": f"Produto ID {produto_id} excluído com sucesso."
            }
        )
        # Retorno HTTP 204 No Content para exclusão bem-sucedida
        return

    except HTTPException:
        # Re-lançar exceções HTTP já tratadas
        raise

    except SQLAlchemyError as e:
        db.rollback()
        logger_registro.error(
            "Erro ao deletar produto no banco",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "DELETE",
                "detail": f"Erro ao deletar Produto (SQLAlchemy): {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro no banco de dados: {str(e)}"
        )

    except Exception as e:
        db.rollback()
        logger_registro.error(
            "Erro inesperado ao deletar produto",
            extra={
                "ip": request.client.host,
                "status": 500,
                "method": "DELETE",
                "detail": f"Erro inesperado ao deletar Produto: {str(e)}"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Erro interno: {str(e)}"
        )