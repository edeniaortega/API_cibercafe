from fastapi import APIRouter, HTTPException, Request, status
from models.clientes import cliente
from controllers.clientes import(
    create_cliente
    , update_cliente
    , delete_cliente
    , get_all
    , get_one
)

router_cliente = APIRouter(prefix="/clientes")

@router_cliente.get( "/" , tags=["Clientes"], status_code=status.HTTP_200_OK )
async def Obtener_todos_los_clientes():
    result = await get_all()
    return result

@router_cliente.post("/", tags=["Clientes"], status_code=status.HTTP_201_CREATED )
async def crear_nuevo_cliente(cliente_data: cliente):
    result = await create_cliente(cliente_data)

    return result

@router_cliente.put("/{id}", tags=["Clientes"], status_code=status.HTTP_201_CREATED )
async def actualizar_un_cliente( cliente_data: cliente, id: int):
    result = await update_cliente( cliente_data)
    return result

@router_cliente.delete("/{id}", tags=["Clientes"], status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_un_cliente( id: int ):
    status: str =  await delete_cliente(id)
    return status

@router_cliente.get("/{id}", tags=["Clientes"], status_code=status.HTTP_200_OK)
async def Obtener_un_estudiante( id: int ):
    result: cliente =  await get_one(id)
    return result