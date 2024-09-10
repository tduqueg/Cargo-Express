from fastapi import FastAPI, HTTPException, Form, Depends
from pydantic import BaseModel
from datetime import datetime
from database import conn
from fastapi.security import OAuth2PasswordBearer
from auth import crear_token, verificar_token
import sqlite3

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo de datos para los productos
class Producto(BaseModel):
    id_producto: str
    cantidad: int

# Modelo de datos para los pedidos
class Pedido(BaseModel):
    productos: list[Producto]
    id_repartidor: str
    fecha_entrega: datetime

# Endpoint para obtener un token 
@app.post("/token")
async def login(username: str = Form(...), password: str = Form(...)):

    if username == "user1" and password == "password":
        token = crear_token({"sub": username})
        return {"access_token": token}
    else:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
# Endpoint para registrar pedidos
@app.post("/entrega")
async def registrar_pedido(pedido: Pedido, token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    cursor = conn.cursor()

    # Verificamos la existencia del repartidor en la tabla repartidores
    cursor.execute('SELECT COUNT(*) FROM repartidores WHERE id_repartidor = ?', (pedido.id_repartidor,))
    if cursor.fetchone()[0] == 0:
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

# Endpoint para obtener repartidores
@app.get("/repartidores")
async def obtener_repartidores(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM repartidores')
    rows = cursor.fetchall()
    return {"repartidores": rows}

# Endpoint para obtener productos
@app.get("/productos")
async def obtener_productos(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    rows = cursor.fetchall()
    return {"productos": rows}

# Endpoint para obtener métricas
@app.get("/metricas")
async def obtener_metricas(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    cursor = conn.cursor()

    # Cantidad de entregas por hora por repartidor
    cursor.execute('''
    SELECT id_repartidor, strftime('%Y-%m-%d %H:00:00', fecha_entrega) as hora, COUNT(*) as entregas
    FROM pedidos
    GROUP BY id_repartidor, hora
    ''')
    entregas_por_hora = cursor.fetchall()

    # Productos más vendidos
    cursor.execute('''
    SELECT id_producto, SUM(cantidad) as cantidad_vendida
    FROM pedidos
    GROUP BY id_producto
    ORDER BY cantidad_vendida DESC
    ''')
    productos_mas_vendidos = cursor.fetchall()

    # Cantidad total de pedidos por repartidor
    cursor.execute('''
    SELECT id_repartidor, COUNT(*) as total_pedidos
    FROM pedidos
    GROUP BY id_repartidor
    ''')
    pedidos_por_repartidor = cursor.fetchall()

    return {
        "entregas_por_hora": entregas_por_hora,
        "productos_mas_vendidos": productos_mas_vendidos,
        "pedidos_por_repartidor": pedidos_por_repartidor
    }
