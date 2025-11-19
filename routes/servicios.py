from fastapi import APIRouter, HTTPException, Request, status
from models.servicios import servicio
from controllers.servicios import(
    update_servicio,
    create_servicio,
    delete_servicio
)

router_servicio = APIRouter(prefix="/servicios")
@router_servicio.put("/{id}", tags=["Servicios"])
async def actualizar_un_servicio(servicio_data: servicio):
    result = await update_servicio(servicio_data)
    return result 

@router_servicio.post("/", tags=["Servicios"], status_code=status.HTTP_201_CREATED)
async def crear_un_nuevo_servicio(servicio_data: servicio):
    result = await create_servicio(servicio_data)
    return result

@router_servicio.delete("/{id}", tags=["Servicios"], status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_un_servicio( id: int ):
    status: str =  await delete_servicio(id)
    return status


