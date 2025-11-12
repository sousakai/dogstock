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

# Detecta se está rodando no Docker ou local
if os.path.exists("/frontend"):
    # Rodando no Docker
    frontend_path = "/frontend"
    assets_path = "/frontend/assets"
else:
    # Rodando local (fora do Docker)
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
    assets_path = os.path.join(frontend_path, "assets")

# Endpoint raiz - serve o index.html
@app.get("/")
async def serve_index():
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        return {"message": "Frontend não encontrado", "api_docs": "/docs"}

# Monta a pasta assets (CSS, JS, imagens)
if os.path.exists(assets_path) and os.path.isdir(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    print(f"✅ Assets montados em: {assets_path}")
else:
    print(f"⚠️  Assets não encontrados em: {assets_path}")

# Monta todas as páginas HTML da pasta Pages
pages_path = os.path.join(frontend_path, "Pages")
if os.path.exists(pages_path) and os.path.isdir(pages_path):
    app.mount("/pages", StaticFiles(directory=pages_path, html=True), name="pages")
    print(f"✅ Pages montadas em: {pages_path}")
