from pydantic import BaseModel,Field, field_validator
from typing import Optional
import re

class servicio(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincremental del servicio"
    )

    descripcion: Optional[str] = Field(
        description="Descripcion del servicio que se ofrece",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        default=None
    )

    precio_unitario: Optional[float] = Field(
        description="precio por unidad o por hora",
        ge=0,
        examples=[15.00, 2.00]
    )