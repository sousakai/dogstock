from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import testeBanco
import os

app = FastAPI()
app.include_router(testeBanco.router)

# Caminho absoluto para a pasta frontend (uma pasta acima de backend)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
