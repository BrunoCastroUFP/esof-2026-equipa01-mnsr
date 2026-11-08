"""Ponto de entrada da API: cria a app FastAPI e regista as rotas"""

from fastapi import FastAPI
from src.presentation import obras_api

app = FastAPI(title="App MNSR Digital")
app.include_router(obras_api.router)
