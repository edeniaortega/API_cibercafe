import json
import logging

from fastapi import HTTPException
from models.facturas import factura
from models.detalle_facturas import detalle_factura

from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one(id: int) -> dict:

    selectscript = """
        SELECT [id]
            ,[id_cliente]
            ,[fecha]
            ,[total]
        FROM [negocio].[factura]
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
            raise HTTPException(status_code=404, detail=f"factura no encontrada")
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


async def update_factura(factura: factura) -> dict:
    
    data_dict = factura.model_dump(exclude_none=True)
    keys = [ k for k in data_dict.keys() if k != 'id']
    
    if not keys:
        raise HTTPException(status_code=400, detail="No se envio un campo para actualizar")

    variables = " =?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [negocio].[factura]
        SET {variables}
        WHERE [id] = ?;
    """
    
    params = [ data_dict[v] for v in keys ]
    
    params.append( factura.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error during update: { str(e) }")
        
    sqlfind: str = """
        SELECT [id]
            ,[id_cliente]
            ,[fecha]
            ,[total]
        FROM [negocio].[factura] 
        WHERE id = ?;
    """
    params_find = [factura.id] 

    result_dict = []
    try: 
        result = await execute_query_json(sqlfind, params=params_find)
        result_dict = json.loads(result)

        if len(result_dict)> 0:
            return result_dict[0]
        else:
            return {"message": "Factura actualizada pero no se encuentra el historial."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error during select: { str(e) }")



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
    

    #--Relación con Factura-Detalle_Factura

async def get_all_detalles(factura_id: int) -> list[dict]:
    select_script = """
        SELECT
            d.id,
            d.id_factura,
            d.id_servicio,
            d.cantidad,
            d.subtotal,
            s.descripcion AS servicio_descripcion,
            s.precio_unitario
        FROM[negocio].[detalle_factura] AS d
        INNER JOIN [negocio].[servicios] AS s
        ON d.id_servicio = s.id
        WHERE d.id_factura = ?
    """

    params = [factura_id]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No se encontro ningun detalle de la factura")

        return dict_result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    

async def get_one_detalle(id_factura: int, id_detalle_facturas: int) -> dict:
    select_script = """
        SELECT
            d.id AS id,
            d.id_factura,
            d.id_servicio,
            d.cantidad,
            d.subtotal,
            s.descripcion AS servicio_descripcion,
            s.precio_unitario
        FROM [negocio].[detalle_factura] AS d
        INNER JOIN [negocio].[servicios] AS s 
        ON d.id_servicio = s.id
        WHERE 
            d.id_factura = ? 
            AND d.id = ?
    """

    params = [id_factura, id_detalle_facturas]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No se encontraron reservas para el cliente")

        return dict_result[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")


async def add_detalle_factura(id_factura: int, detalle: detalle_factura):

    insert_script = """
        INSERT INTO negocio.detalle_factura
            (id_factura, id_servicio, cantidad, subtotal)
        VALUES (?, ?, ?, ?);
    """

    insert_params = [
        id_factura, 
        detalle.id_servicio,
        detalle.cantidad,
        detalle.subtotal
    ]

    try:
        await execute_query_json(insert_script, insert_params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (insert): {str(e)}")

    select_script = """
        SELECT 
            df.id_factura,
            df.id_servicio,
            s.descripcion AS servicio,
            df.cantidad,
            df.subtotal
        FROM negocio.detalle_factura df
        INNER JOIN negocio.servicios s
            ON df.id_servicio = s.id
        WHERE df.id_factura = ?
        AND df.id_servicio = ?;
    """

    select_params = [id_factura, detalle.id_servicio] 

    try:
        result = await execute_query_json(select_script, select_params)
        result_dict = json.loads(result)
        
        if result_dict:
            return result_dict[0]
        else:
            raise HTTPException(status_code=500, detail="Detail inserted, but record retrieval failed.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error (select): {str(e)}")
    
