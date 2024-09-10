from fastapi import FastAPI 
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Modelo de datos para los pedidos
class Pedido(BaseModel):
    id_product: str
    id_repartidor: str
    cantidad: int
    fecha_entrega: datetime

# Endpoit registro pedidos
@app.post("/entrega")
async def registrar_pedido(pedido: Pedido):
    print(f"Pedido registrado: {pedido}")
    
    return {"mensaje": "Pedido registrado exitosamente", "data": pedido}
