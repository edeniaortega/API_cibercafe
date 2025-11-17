from pydantic import BaseModel,Field, field_validator
from typing import Optional
import re

class computadora(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincremental de la computadora"
    )

    numero_pc: Optional[str] = Field (
        description="Identificador alfanumerico de la computadora ingresado manualmente",
        pattern=r"^[A-Za-z0-9]+$",
        default=None,
        examples=["PC001","PC002"]
    )

    estado: Optional[str] = Field (
        description="Muestra la disponibilidad de la computadora",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default='Disponible',
        examples=["Disponible","Ocupada","En Mantenimiento"]
    )