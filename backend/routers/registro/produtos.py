from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import get_db  # função que retorna a sessão do SQLAlchemy
from models import Produto   # modelo SQLAlchemy da tabela produtos
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
