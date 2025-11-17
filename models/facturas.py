from pydantic import BaseModel, Field
from datetime import date, datetime, time, timedelta
from typing import Optional
import re

class factura(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincremental de la factura"
    )

    id_cliente: Optional[int] = Field(
        default=None,
        description="El ID del cliente"
    )

    fecha: Optional[datetime] = Field(
        description="Fecha de emision de la factura"
    )

    total: Optional[float] = Field(
        description="Precio total de la factura",
        ge=0,
        examples=[150.00, 10.00]
    )