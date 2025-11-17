from pydantic import BaseModel,Field, field_validator
from typing import Optional
import re

class reserva(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable de la reserva"   
    )

    id_cliente: Optional[int] = Field(
        default=None,
        description="El ID del cliente"
    )

    id_computadora: Optional[int] = Field(
        default=None,
        description="El ID de la computadora"
    )

    id_factura: Optional[int] = Field(
        default=None,
        description="El ID de la factura"
    )

    
    