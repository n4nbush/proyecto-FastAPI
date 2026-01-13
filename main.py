from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi. templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from contextlib import closing
import database
import sqlite3

from database import init_db
from routers import gastos

app = FastAPI(
    title="Gestor de Gastos",
    description="App para gestionar gastos personales",
    version="2.0.0")

templates = Jinja2Templates(directory='templates')  # ¿Qué carpeta? 
app.mount("/static", StaticFiles(directory='static'), name="static") 

# Inicializar DB al arrancar
@app.on_event("startup")
def startup():
    database.init_db()
    print("✅ Base de datos inicializada")

# Incluir routers
app.include_router(gastos.router) 

# Ruta raíz (redirige a /gastos/)
@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/gastos/")
