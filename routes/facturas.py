from fastapi import APIRouter, HTTPException, Request , status
from models.facturas import factura
from models.detalle_facturas import detalle_factura
from controllers.facturas import(
    create_factura
    , update_factura
    , delete_factura
    , get_all
    , get_one
    , get_all_detalles
    , get_one_detalle
    , add_detalle_factura
)

router_factura = APIRouter(prefix="/facturas")

@router_factura.get( "/" , tags=["Facturas"], status_code=status.HTTP_200_OK )
async def Obtener_todas_las_facturas():
    result = await get_all()
    return result

@router_factura.post("/", tags=["Facturas"], status_code=status.HTTP_201_CREATED)
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
async def Obtener_una_factura( id: int ):
    result: factura =  await get_one(id)
    return result

@router_factura.get("/{id}/detalle_facturas", tags=["Facturas(Relación)"], status_code=status.HTTP_200_OK)
async def Obtener_todos_los_detalles_de_una_factura( id: int ):
    result: factura =  await get_all_detalles(id)
    return result

@router_factura.get("/{id}/detalle_facturas/{id_detalle_facturas}", tags=["Facturas(Relación)"], status_code=status.HTTP_200_OK)
async def obtener_el_detalle_de_una_factura( id: int, id_detalle_facturas: int ):
    result = await get_one_detalle(id, id_detalle_facturas)
    return result

@router_factura.post("/{id}/detalle_facturas", tags=["Facturas(Relación)"],status_code=status.HTTP_201_CREATED)
async def crear_un_detalle_a_una_factura(id:int, detalle: detalle_factura):
    result = await add_detalle_factura(id, detalle)
    return result