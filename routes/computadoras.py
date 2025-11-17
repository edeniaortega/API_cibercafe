from fastapi import APIRouter, HTTPException, Request, status
from models.computadoras import computadora
from controllers.computadoras import(
    create_computadora
    , update_computadora
    , delete_computadora
    , get_all
    , get_one
)

router_computadora = APIRouter(prefix="/computadoras")
@router_computadora.get( "/" , tags=["Computadoras"], status_code=status.HTTP_200_OK )
async def Obtener_todas_las_computadoras():
    result = await get_all()
    return result


@router_computadora.post("/", tags=["Computadoras"], status_code=status.HTTP_201_CREATED)
async def crear_nueva_computadora(computadora_data: computadora):
    result = await create_computadora(computadora_data)

    return result

@router_computadora.put("/{id}", tags=["Computadoras"], status_code=status.HTTP_201_CREATED)
async def actualizar_una_computadora(computadora_data: computadora):
    result = await update_computadora(computadora_data)
    return result

@router_computadora.delete("/{id}", tags=["Computadoras"], status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_una_computadora( id: int ):
    status: str =  await delete_computadora(id)
    return status

@router_computadora.get("/{id}", tags=["Computadoras"], status_code=status.HTTP_200_OK)
async def Obtener_una_computadora( id: int ):
    result: computadora =  await get_one(id)
    return result