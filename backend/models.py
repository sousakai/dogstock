from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class TipoPagamento(Base):
    __tablename__ = "tipo_pagamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="ativo")


# aqui, o models serve para "validar os dados" antes de enviar pro banco. é como um guia de como os dados devem ser
"""class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False, unique=True)
    medida = Column(String(100), nullable=False)
    qtd_disponivel = Column(Numeric(10, 3), nullable=False)
    qtd_minima = Column(Numeric(10, 3), nullable=False)
    #mUDAR PARA FALSE ASSIM QUE CRIAR A CLASSE DE CATEGORIA!!! não se pode registrar produto sem categoria.
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=True)
    status = Column(String(50), nullable=False, default="ativo")

    categoria = relationship("Categoria", back_populates="produtos")"""


class Fornecedores(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    razao_social = Column(String(255), nullable=False, unique=True)
    contato = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    cnpj = Column(String(255), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="ativo")
