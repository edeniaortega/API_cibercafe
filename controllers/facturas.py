import json
import logging

from fastapi import HTTPException
from models.facturas import factura

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one() -> list[factura]:

    selectscript = """
        SELECT [id]
            ,[id_cliente]
            ,[fecha]
            ,[total]
        FROM [negocio].[factura]
    """
    params = [id]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"student not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    

async def get_all() -> list[factura]:

    selectscript = """
        SELECT [id]
            ,[id_cliente]
            ,[fecha]
            ,[total]
        FROM [negocio].[factura]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def delete_factura( id: int) -> str:
    deletescript = """
        DELETE FROM [negocio].[factura]
        WHERE [id] = ?;
    """
    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")


async def update_factura (factura: factura) -> factura:
    dict = factura.model_dump(exclude_none=True)

    keys = [ k for k in dict.keys() ]
    keys.remove('id')
    variables = " =?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [negocio].[factura]
        SET {variables}
        WHERE [id] = ?;
    """
    params = [ dict[v] for v in keys ]
    params.append( factura.id )

    update_results = None
    try:
        insert_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    
    sqlfind: str = """
        SELECT [id]
            ,[id_cliente]
            ,[fecha]
            ,[total]
        FROM [negocio].[factura]
        WHERE [id] = SCOPE_IDENTITY();
    """
    params = [factura.id]

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



async def create_factura (factura: factura) -> factura:
    sqlscript: str = """
        INSERT INTO [negocio].[factura] ([id_cliente],[fecha],[total])
        VALUES(?, ?, ?)
    """

    params= [
        factura.id_cliente
        , factura.fecha
        , factura.total
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    
    sqlfind: str = """
        SELECT [id]
            ,[id_cliente]
            ,[fecha]
            ,[total]
        FROM [negocio].[factura]
        WHERE [id] = SCOPE_IDENTITY();
    """
    params = [factura.id]

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