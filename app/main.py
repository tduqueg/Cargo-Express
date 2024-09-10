from fastapi import FastAPI 
from pydantic import BaseModel
from datetime import datetime
from database import conn
import sqlite3

app = FastAPI()

# Modelo de datos para los pedidos
class Pedido(BaseModel):
    id_producto: str
    id_repartidor: str
    cantidad: int
    fecha_entrega: datetime

# Endpoit registro pedidos
@app.post("/entrega")
async def registrar_pedido(pedido: Pedido):
    cursor = conn.cursor()

    fecha_entrega_str = pedido.fecha_entrega.isoformat()

    cursor.execute('''
    INSERT INTO pedidos (id_producto, id_repartidor, cantidad, fecha_entrega)
    VALUES (?, ?, ?, ?)
        ''', (pedido.id_producto, pedido.id_repartidor, pedido.cantidad, fecha_entrega_str))
    conn.commit()
    return {"mensaje": "Pedido registrado exitosamente", "data": pedido}
