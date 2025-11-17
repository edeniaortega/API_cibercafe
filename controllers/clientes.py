import json
import logging

from fastapi import HTTPException
from models.clientes import cliente

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_cliente( cliente: cliente ) -> cliente:
    
    sqlscript: str = """
        INSERT INTO [negocio].[clientes] ([nombre],[apellido],[email],[telefono])
        VALUES(?, ?, ?, ?);
    """
    params= [
        cliente.nombre
        , cliente.apellido
        , cliente.email
        , cliente.telefono
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    
    sqlfind: str = """
        SELECT [id]
            ,[nombre]
            ,[apellido]
            ,[email]
            ,[telefono]
        FROM [negocio].[clientes]
        WHERE email = ?;
    """
    params = [cliente.email]

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






