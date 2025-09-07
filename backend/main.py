from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers import testeBanco, categorias, produtos, movimentacoes, fornecedores # atualizar sempre que incluir routers
import os

app = FastAPI()

# routers das apis.
app.include_router(testeBanco.router)
app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)
app.include_router(fornecedores.router)

# caminho para ser hosteado (arquivo testes.html, evita conflito com index.html)
teste_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "testes.html")

# busca o end point do testes.html
@app.get("/")
async def serve_teste():
    return FileResponse(teste_file)

# joga os arquivos .css e .js no staticfiles, assim conseguimos usar isso no html. necessário, não remover.
frontend_static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_static_path), name="frontend_static")

print(app.routes)

