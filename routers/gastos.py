from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from contextlib import closing

from models.schemas import registrar_gasto

import database

motivos = [item for lista in database.grupos.values() for item in lista]

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
    categoria : str = Form(...),
    monto : float = Form(...),
    descripcion : str = Form ("")
    ):
    movimiento = registrar_gasto(fecha_hora=fecha_hora,tipo=tipo,categoria=categoria,monto=monto,descripcion=descripcion)

    database.init_db()
    with closing(database.get_db()) as db:
        db.execute(
            "INSERT INTO datos VALUES (?, ?, ?, ?, ?)",
            (movimiento.fecha_hora, movimiento.tipo, movimiento.categoria, movimiento.monto, movimiento.descripcion)
        )
        db.commit()

    print(f"Recibido: {movimiento.fecha_hora}, {movimiento.tipo}, {movimiento.categoria}, {movimiento.monto}, {movimiento.descripcion}")
    return RedirectResponse(url="/gastos/", status_code=303)

