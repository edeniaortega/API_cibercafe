from pydantic import BaseModel,Field, field_validator
from typing import Optional
import re

class detalle_factura(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincremental del detalle de la factura"
    )
    
    id_factura: Optional[int] = Field(
        default=None,
        description="El ID de la factura"
    )

    id_servicio: Optional[int] = Field(
        default=None,
        description="El ID del servicio"
    )

    cantidad: Optional[float] = Field(
        description="Se especifica la cantidad de horas que un cliente uso una computadora o tambien el numero de hojas impresas o fotocopiadas",
        ge=0,
        examples=[1.00, 2.00]
    )

    subtotal: Optional[float] = Field(
        description="especifica el precio total por servicio",
        ge=0,
        examples=[20.00, 30.00]
    )

