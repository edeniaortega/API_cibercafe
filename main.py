from fastapi import FastAPI
from routes.clientes import router_cliente
from routes.computadoras import router_computadora
from routes.facturas import router_factura
from routes.reservas import router_reserva

app = FastAPI()

app.include_router(router_cliente)
app.include_router(router_computadora)
app.include_router(router_factura)
app.include_router(router_reserva)

@app.get("/")
def read_root():
    return {"Hello": "World"}



