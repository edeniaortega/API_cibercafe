import json
import logging

from fastapi import HTTPException
from models.servicios import servicio

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def update_servicio(servicio: servicio) -> dict:
    
    data_dict = servicio.model_dump(exclude_none=True)
    keys = [ k for k in data_dict.keys() if k != 'id']
    
    if not keys:
        raise HTTPException(status_code=400, detail="No se envio un campo para actualizar")

    variables = " =?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [negocio].[servicios]
        SET {variables}
        WHERE [id] = ?;
    """
    
    params = [ data_dict[v] for v in keys ]
    
    params.append( servicio.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error during update: { str(e) }")
        
    sqlfind: str = """
        SELECT [id]
            ,[descripcion]
            ,[precio_unitario]
        FROM [negocio].[servicios] 
        WHERE id = ?;
    """
    params_find = [servicio.id] 

    result_dict = []
    try: 
        result = await execute_query_json(sqlfind, params=params_find)
        result_dict = json.loads(result)

        if len(result_dict)> 0:
            return result_dict[0]
        else:
            return {"message": "servicio actualizado pero no se encuentra el historial."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error during select: { str(e) }")
    

async def create_servicio (servicio: servicio) -> servicio:
    sqlscript: str = """
        INSERT INTO [negocio].[servicios] ([id],[descripcion],[precio_unitario])
        VALUES(?, ?, ?)
    """

    params= [
        servicio.id
        , servicio.descripcion
        , servicio.precio_unitario
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    
    sqlfind: str = """
        SELECT [id]
            ,[descripcion]
            ,[precio_unitario]
        FROM [negocio].[servicios]
        WHERE [id] = SCOPE_IDENTITY();
    """
    params = []


    result_dict = []
    try: 
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict)> 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    

async def delete_servicio( id: int) -> str:
    deletescript = """
        DELETE FROM [negocio].[servicios]
        WHERE [id] = ?;
    """
    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")