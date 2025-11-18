from fastapi import APIRouter, HTTPException, Request, status
from models.reservas import reserva
from controllers.reservas import(
    create_reserva
    , update_reserva
    , delete_reserva
    , get_all
    , get_one
)

router_reserva = APIRouter(prefix="/reserva")

@router_reserva.get( "/" , tags=["Reservas"], status_code=status.HTTP_200_OK )
async def Obtener_todas_las_reservas():
    result = await get_all()
    return result

@router_reserva.post("/", tags=["Reservas"] )
async def crear_nueva_reserva(reserva_data: reserva):
    result = await create_reserva(reserva_data)

    return result

@router_reserva.put("/{id}", tags=["Reservas"])
async def actualizar_una_reserva(reserva_data: reserva):
    result = await update_reserva(reserva_data)
    return result

@router_reserva.delete("/{id}", tags=["Reservas"], status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_una_reserva( id: int ):
    status: str =  await delete_reserva(id)
    return status

@router_reserva.get("/{id}", tags=["Reservas"], status_code=status.HTTP_200_OK)
async def Obtener_una_reserva( id: int ):
    result: reserva =  await get_one(id)
    return result

