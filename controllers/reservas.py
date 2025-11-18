import json
import logging

from fastapi import HTTPException
from models.reservas import reserva

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one( id: int ) -> reserva:

    selectscript = """
       SELECT
            r.id AS id,
            r.id_cliente,
            c.nombre AS nombre_cliente,
            r.id_computadora,
            r.id_factura,
            f.fecha,
            df.id_servicio,
            s.precio_unitario,
            df.cantidad,
            df.subtotal
        FROM [negocio].[reservas] AS r
        JOIN [negocio].[clientes] AS c ON r.id_cliente = c.id
        JOIN [negocio].[factura] AS f ON r.id_factura = f.id
        JOIN [negocio].[detalle_factura] AS df ON f.id = df.id_factura
        JOIN [negocio].[servicios] AS s ON df.id_servicio = s.id
        WHERE r.id = ?;
    """

    params = [id]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"reserva no encontrada")
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")



async def get_all() -> list[reserva]:

    selectscript = """
        SELECT [id]
            ,[id_cliente]
            ,[id_computadora]
            ,[id_factura]
        FROM [negocio].[reservas]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")


async def delete_reserva( id: int) -> str:
    deletescript = """
        DELETE FROM [negocio].[reservas]
        WHERE [id] = ?;
    """
    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")


async def update_reserva (reserva: reserva) -> reserva:
    dict = reserva.model_dump(exclude_none=True)

    keys = [ k for k in dict.keys() ]
    keys.remove('id')
    variables = " =?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [negocio].[reservas]
        SET {variables}
        WHERE [id] = ?;
    """
    params = [ dict[v] for v in keys ]
    params.append( reserva.id )

    update_results = None
    try:
        insert_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    
    sqlfind = """
        SELECT [id]
            ,[id_cliente]
            ,[id_computadora]
            ,[id_factura]
        FROM [negocio].[reservas]
        Where [id] = SCOPE_IDENTITY();
    """

    params = [reserva.id]

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




async def create_reserva (reserva: reserva) -> reserva:

    sqlscript = """
        INSERT INTO [negocio].[reservas] ([id_cliente],[id_computadora],[id_factura])
        VALUES (?, ?, ?);
    """

    params= [
        reserva.id_cliente
        , reserva.id_computadora
        , reserva.id_factura
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e)}")
    
    sqlfind = """
        SELECT [id]
            ,[id_cliente]
            ,[id_computadora]
            ,[id_factura]
        FROM [negocio].[reservas]
        Where [id] = SCOPE_IDENTITY();
    """

    params = [reserva.id]

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


