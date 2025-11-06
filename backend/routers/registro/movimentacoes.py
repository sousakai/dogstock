from fastapi import APIRouter, HTTPException, Depends, Request
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
