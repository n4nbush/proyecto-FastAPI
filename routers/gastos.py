from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from contextlib import closing

import database

motivos = ["Moto","Auto","Uber"]


router = APIRouter(
    prefix='/gastos',
    tags=['gastos']
)

templates = Jinja2Templates(directory='templates')

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request":request, "motivos":motivos}
        )

@router.post("/registrar")
async def registrar(
    fecha_hora : str = Form(...),
    tipo : str = Form(...),
    motivo : str = Form(...),
    monto : float = Form(...),
    descripcion : str = Form ("")
    ):
    database.init_db()
    with closing(database.get_db()) as db:
        db.execute(
            "INSERT INTO datos VALUES (?, ?, ?, ?, ?)",
            (fecha_hora, tipo, motivo, monto, descripcion)
        )
        db.commit()

    print(f"Recibido: {fecha_hora}, {tipo}, {motivo}, {monto}, {descripcion}")
    return RedirectResponse(url="/gastos/", status_code=303)

