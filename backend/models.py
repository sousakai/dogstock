from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

#aqui, o models serve para "validar os dados" antes de enviar pro banco. é como um guia de como os dados devem ser
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False, unique=True)
    medida = Column(String(100), nullable=False)
    qtd_disponivel = Column(Numeric(10, 3), nullable=False)
    qtd_minima = Column(Numeric(10, 3), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False) #MUDAR PARA FALSE ASSIM QUE CRIAR A CLASSE DE CATEGORIA!!! não se pode registrar produto sem categoria.
    status = Column(String(50), nullable=False, default="ativo")
    
    categoria = relationship("Categoria") #relacionamento entre tabelas, colocar nome da CLASSE
    
class Fornecedores(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    razao_social = Column(String(255), nullable=False, unique=True)
    contato = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    cnpj = Column(String(255), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="ativo")
    
    
class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False, unique=True)

#ainda não funcional, funcionará completamente com os models das outras tabelas tipo_movimentacao e tipo_pagamento
#testes até aqui, ok
class Movimentacoes(Base):
    __tablename__ = "movimentacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Numeric(10, 3), nullable=False)
    data = Column(TIMESTAMP, nullable=False)
    tipo_mov_id = Column(Integer, ForeignKey("tipo_movimentacao.id"), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)
    tipo_pag_id = Column(Integer, ForeignKey("tipo_pagamento.id"), nullable=True) ## averiguar se deve ser nula ou não, já que é chave estrangeira. atualmente é nullable pois nem toda movimentação tem pagamento (ex: entrada por doação)
    preco_compra = Column(Numeric(12, 2), nullable=True)
    preco_venda = Column(Numeric(12, 2), nullable=True)
    
    #relacionamento entre tabelas
    produto = relationship("Produto")
    tipo_movimentacao = relationship("TipoMovimentacao")
    fornecedor = relationship("Fornecedores")
    tipo_pagamento = relationship("TipoPagamento")
  
