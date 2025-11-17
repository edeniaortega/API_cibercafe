from pydantic import BaseModel,Field, field_validator
from typing import Optional
import re

class cliente(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable para el cliente"
    )

    nombre: Optional[str] = Field(
        description="Primer nombre del cliente",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None,
        examples=["Elisa","Pedro"]
    )

    apellido: Optional[str] = Field(
        description="Primer apellido del cliente",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None,
        examples=["Gomez","Salgado"]
    )

    email: Optional[str] = Field(
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        default=None,
        examples=["usuario@gmail.com"]
    )

    telefono: Optional[str] = Field(
        pattern=r"^[\d-]+$",
        default=None,
        examples=["9857-6574"]
    )


