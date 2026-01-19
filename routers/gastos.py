from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from contextlib import closing
from utils.helpers import backup
from models.schemas import registrar_gasto, filtrar
from utils.constant import grupos,categorias
import database


router = APIRouter(
    prefix='/gastos',
    tags=['gastos']
)

templates = Jinja2Templates(directory='templates')

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    backup()

    return templates.TemplateResponse(
        name="index.html",
        context={"request":request, "categorias":categorias}
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

@router.get("/movimientos", response_class=HTMLResponse)
async def movimientos(request: Request,filtros: filtrar = Depends()):
    resultados,total = database.filtrar(
        filtros.filtro_fecha, 
        grupo_select=filtros.grupo, 
        categoria_select=filtros.categoria)

    return templates.TemplateResponse(
        name="movimientos.html",
        context={"request":request, "categorias":categorias,"grupos":grupos, "resultados":resultados,"total":total}
    )

@router.get("/resumen_grupos", response_class=HTMLResponse)
async def resumen_grupos(request: Request):

    return templates.TemplateResponse(
        name='resumen_grupos.html',
        context={"request":request}
    )

