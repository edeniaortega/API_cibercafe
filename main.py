import uvicorn
from fastapi import FastAPI
from routes.clientes import router_cliente
from routes.computadoras import router_computadora
from routes.facturas import router_factura
from routes.reservas import router_reserva
from routes.servicios import router_servicio

app = FastAPI(title="API Cibercafé")

app.include_router(router_cliente)
app.include_router(router_computadora)
app.include_router(router_factura)
app.include_router(router_reserva)
app.include_router(router_servicio)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")