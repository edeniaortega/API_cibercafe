import json
import logging

from fastapi import HTTPException
from models.clientes import cliente
from models.reservas import reserva

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one( id: int ) -> cliente:

    selectscript = """
        SELECT [id]
            ,[nombre]
            ,[apellido]
            ,[email]
            ,[telefono]
        FROM [negocio].[clientes]
        where [id] = ?;
    """

    params = [id]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"cliente no encontrado")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")



async def get_all() -> list[cliente]:

    selectscript = """
        SELECT [id]
            ,[nombre]
            ,[apellido]
            ,[email]
            ,[telefono]
        FROM [negocio].[clientes]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def delete_cliente( id: int) -> str:
    deletescript = """
        DELETE FROM [negocio].[clientes]
        WHERE [id] = ?;
    """
    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    

async def update_cliente( cliente: cliente ) -> cliente:

    dict = cliente.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [negocio].[clientes]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( cliente.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    sqlfind: str = """
        SELECT [id]
            ,[nombre]
            ,[apellido]
            ,[email]
            ,[telefono]
        FROM [negocio].[clientes]
        WHERE id = ?;
    """

    params = [cliente.id]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")



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
    
#----Interaccion clientes con reservas----
async def get_all_reservas(id_cliente: int) -> list[dict]:
   
    select_script = """
        SELECT
            r.id AS id,
            r.id_computadora,
            r.id_factura,
            r.id_cliente,
            c.nombre AS nombre_cliente,
            c.apellido AS apellido_cliente,
            c.email AS email_cliente
        FROM [negocio].[reservas] AS r
        INNER JOIN [negocio].[clientes] AS c 
        ON r.id_cliente = c.id
        WHERE r.id_cliente = ?
    """

    params = [id_cliente]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron reservas para el cliente")

        return dict_result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

async def get_one_reserva(id_cliente: int, id_reserva: int) -> dict:
    select_script = """
        SELECT
            r.id AS id,
            r.id_computadora,
            r.id_factura,
            r.id_cliente,
            c.nombre AS nombre_cliente,
            c.apellido AS apellido_cliente,
            c.email AS email_cliente
        FROM [negocio].[reservas] AS r
        INNER JOIN [negocio].[clientes] AS c 
        ON r.id_cliente = c.id
        WHERE 
            r.id_cliente = ? 
            AND r.id = ?
            
    """

    params = [id_cliente, id_reserva]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron reservas para el cliente")

        return dict_result[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    