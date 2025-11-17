from fastapi import APIRouter, HTTPException, Request
from models.clientes import cliente
from controllers.clientes import(
    create_cliente
)

router_cliente = APIRouter(prefix="/clientes")
@router_cliente.post("/", tags=["Clientes"] )
async def create_new_cliente(cliente_data: cliente):
    result = await create_cliente(cliente_data)

    return result