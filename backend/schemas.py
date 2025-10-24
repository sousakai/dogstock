from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

# Schema para criar produto (entrada da API)
'''class ProdutoCreate(BaseModel):
    nome: str                     # nome obrigatório
    medida: str                   # ex: "kg", "unidade", etc.
    qtd_disponivel: Decimal       # estoque inicial
    qtd_minima: Decimal           # limite mínimo
    categoria_id: int             # FK (tem que existir no banco)
    status: Optional[str] = "ativo"  # default "ativo" se não for informado


# Schema para resposta da API (saída)
class ProdutoResponse(BaseModel):
    id: int                       # vem do banco
    nome: str
    medida: str
    qtd_disponivel: Decimal
    qtd_minima: Decimal
    categoria_id: int
    status: str

    class Config:
        orm_mode = True  # permite retornar objetos SQLAlchemy direto'''


class FornecedoresCreate(BaseModel):
    razao_social: str                     # nome obrigatório
    contato: str                   # ex: "kg", "unidade", etc.
    email: str       # estoque inicial
    cnpj: str           # limite mínimo
    status: Optional[str] = "ativo"  # default "ativo" se não for informado


class FornecedoresResponse(BaseModel):
    id: int                       # vem do banco
    razao_social: str                     # nome obrigatório
    contato: str                   # ex: "kg", "unidade", etc.
    email: str       # estoque inicial
    cnpj: str           # limite mínimo
    status: str

    class Config:
        orm_mode = True  # permite retornar objetos SQLAlchemy direto


class TipoMovimentacaoCreateSchema(BaseModel):
    descricao: str


# Schema de resposta (saída de dados)
class TipoMovimentacaoResponseSchema(BaseModel):
    id: int
    descricao: str

    class Config:
        orm_mode = True
