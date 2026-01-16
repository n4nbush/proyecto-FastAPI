from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime


class registrar_gasto(BaseModel):
    fecha_hora: str = Field(default_factory=lambda: datetime.now().isoformat())
    tipo: str
    categoria: str 
    monto: int
    descripcion: Optional[str] = None


