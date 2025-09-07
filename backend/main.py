from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import testeBanco, categorias # atualizar sempre que incluir novo router
import os

app = FastAPI()
## atualizar sempre que incluir novo router
app.include_router(testeBanco.router)
app.include_router(categorias.router)

# Caminho absoluto para a pasta frontend (uma pasta acima de backend)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
