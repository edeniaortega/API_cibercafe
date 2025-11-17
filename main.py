from fastapi import FastAPI
from routes.clientes import router_cliente

app = FastAPI()

app.include_router(router_cliente)

@app.get("/")
def read_root():
    return {"Hello": "World"}



