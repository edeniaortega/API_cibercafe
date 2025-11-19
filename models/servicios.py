from pydantic import BaseModel,Field, field_validator
from typing import Optional
import re

class servicio(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincremental del servicio"
    )

    descripcion: Optional[str] = Field (
        default=None,
        description="Descripcion del servicio que se ofrece",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["fotocopias", "impresion a color"]
        
    )

    precio_unitario: Optional[float] = Field(
        description="precio por unidad o por hora",
        ge=0,
        examples=[2.00, 15.00]
    )