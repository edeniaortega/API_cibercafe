from fastapi import APIRouter, HTTPException, Request , status
from models.facturas import factura
from controllers.facturas import(
    create_factura
    , update_factura
    , delete_factura
    , get_all
    , get_one
)

router_factura = APIRouter(prefix="/facturas")

@router_factura.get( "/" , tags=["Facturas"], status_code=status.HTTP_200_OK )
async def Obtener_todas_las_facturas():
    result = await get_all()
    return result

@router_factura.post("/", tags=["Facturas"] )
async def crear_nueva_factura(factura_data: factura):
    result = await create_factura(factura_data)

    return result

@router_factura.put("/{id}", tags=["Facturas"])
async def actualizar_una_factura(factura_data: factura):
    result = await update_factura(factura_data)
    return result 

@router_factura.delete("/{id}", tags=["Facturas"], status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_una_factura( id: int ):
    status: str =  await delete_factura(id)
    return status

@router_factura.get("/{id}", tags=["Facturas"], status_code=status.HTTP_200_OK)
async def Obtener_una_computadora( id: int ):
    result: factura =  await get_one(id)
    return result