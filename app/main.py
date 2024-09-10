from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import conn
import sqlite3

app = FastAPI()

# Modelo de datos para los productos
class Producto(BaseModel):
    id_producto: str
    cantidad: int

# Modelo de datos para los pedidos
class Pedido(BaseModel):
    productos: list[Producto]  # Cambiado de id_producto a productos
    id_repartidor: str
    fecha_entrega: datetime

# Endpoint registro pedidos
@app.post("/entrega")
async def registrar_pedido(pedido: Pedido):
    cursor = conn.cursor()

    # Verificamos la existencia del repartidor en la tabla repartidores
    cursor.execute('SELECT COUNT(*) FROM repartidores WHERE id_repartidor = ?', (pedido.id_repartidor,))
    if cursor.fetchone()[0] == 0:
        print(f"Repartidor {pedido.id_repartidor} no encontrado en la base de datos")
        raise HTTPException(status_code=400, detail="Repartidor no válido")

    # Verificamos la existencia de cada producto en la tabla productos
    for producto in pedido.productos:
        cursor.execute('SELECT COUNT(*) FROM productos WHERE id_producto = ?', (producto.id_producto,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=400, detail=f"Producto {producto.id_producto} no válido")

        # Insertamos cada producto en la base de datos
        fecha_entrega_str = pedido.fecha_entrega.isoformat()
        cursor.execute('''
        INSERT INTO pedidos (id_producto, id_repartidor, cantidad, fecha_entrega)
        VALUES (?, ?, ?, ?)
        ''', (producto.id_producto, pedido.id_repartidor, producto.cantidad, fecha_entrega_str))

    conn.commit()
    return {"mensaje": "Pedidos registrados exitosamente", "data": pedido}

@app.get("/repartidores")
async def obtener_repartidores():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM repartidores')
    rows = cursor.fetchall()
    return {"repartidores": rows}

@app.get("/productos")
async def obtener_repartidores():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    rows = cursor.fetchall()
    return {"productos": rows}