from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime


class registrar_gasto(BaseModel):
    fecha_hora: str = Field(default_factory=lambda: datetime.now().isoformat())
    tipo: str
    categoria: str 
    monto: int
    descripcion: Optional[str] = None

class filtrar(BaseModel):
    filtro_fecha: int = 30  # Por defecto: último mes
    grupo: Optional[str] | None = None  # Por defecto: sin filtro
    categoria: Optional[str] | None = None  # Por defecto: sin filtro
    
    # Validación opcional
    '''@validator('fecha')
    def fecha_valida(cls, v):
        if v not in [1, 7, 30, 60, 360]:
            raise ValueError('Período no válido')
        return v'''

