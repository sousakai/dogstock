from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# imports dos routers de consulta
from routers.consulta import testeBanco
from routers.consulta import categorias as con_categorias
from routers.consulta import produtos as con_produtos
from routers.consulta import movimentacoes as con_movimentacoes
from routers.consulta import fornecedores as con_fornecedores
from routers.consulta import tipoPagamento as con_tipoPagamento
from routers.consulta import tipoMovimentacao as con_tipoMovimentacao

# imports dos routers de registro
from routers.registro import fornecedores as reg_fornecedores
from routers.registro import categoria as reg_categoria
from routers.registro import produtos as reg_produtos
from routers.registro import movimentacoes as reg_movimentacoes
from routers.registro import tipomovimentacao as reg_tipoMovimentacao

from routers.registro.tipoPagamento import router as registro_tipo_pagamento_router

import os

app = FastAPI()

# routers das apis.
app.include_router(testeBanco.router)
app.include_router(con_categorias.router)
app.include_router(con_produtos.router)
app.include_router(con_movimentacoes.router)
app.include_router(con_fornecedores.router)
app.include_router(con_tipoPagamento.router)
app.include_router(con_tipoMovimentacao.router)
app.include_router(reg_fornecedores.router)
app.include_router(reg_categoria.router)
app.include_router(reg_produtos.router)
app.include_router(reg_movimentacoes.router)

# caminho para ser hosteado (arquivo testes.html, evita conflito com index.html)
teste_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.include_router(registro_tipo_pagamento_router)

app.include_router(reg_tipoMovimentacao.router)

# busca o end point do testes.html


@app.get("/")
async def serve_teste():
    return FileResponse(teste_file)

# joga os arquivos .css e .js no staticfiles, assim conseguimos usar isso no html. necessário, não remover.
frontend_static_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_static_path),
          name="frontend_static")
