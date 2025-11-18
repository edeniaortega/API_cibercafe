import json
import logging

from fastapi import HTTPException
from models.computadoras import computadora

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one() -> list[computadora]:

    selectscript = """
        SELECT [id]
            ,[numero_pc]
            ,[estado]
        FROM [negocio].[computadoras]
    """
    params = [id]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"computadora no encontrada")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")


async def get_all() -> list[computadora]:

    selectscript = """
        SELECT [id]
            ,[numero_pc]
            ,[estado]
        FROM [negocio].[computadoras]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def delete_computadora( id: int) -> str:
    deletescript = """
        DELETE FROM [negocio].[computadoras]
        WHERE [id] = ?;
    """
    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")


async def update_computadora(computadora: computadora) -> computadora:
    dict = computadora.model_dump(exclude_none=True)

    keys = [ k for k in dict.keys() ]
    keys.remove('id')
    variables = " =?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [negocio].[computadoras]
        SET {variables}
        WHERE [id] = ?;
    """
    params = [ dict[v] for v in keys ]
    params.append( computadora.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
    sqlfind: str = """
        SELECT [id]
            ,[numero_pc]
            ,[estado]
        FROM [negocio].[computadoras]
        where [numero_pc]=?
    """
    params = [computadora.numero_pc]

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
    
async def create_computadora(computadora: computadora) -> computadora:
    sqlscript: str = """
        INSERT INTO [negocio].[computadoras] ([numero_pc],[estado])
        VALUES (?, ?);
    """

    params=[
        computadora.numero_pc
        , computadora.estado
    ]

    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    
    sqlfind: str = """
        SELECT [id]
            ,[numero_pc]
            ,[estado]
        FROM [negocio].[computadoras]
        where [numero_pc]=?
    """
    params = [computadora.numero_pc]

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



