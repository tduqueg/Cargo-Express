from fastapi import FastAPI, HTTPException, Form, Depends, Request
from pydantic import BaseModel
from datetime import datetime
from app.database import conn
from fastapi.security import OAuth2PasswordBearer
from app.auth import crear_token, verificar_token
import sqlite3
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from mangum import Mangum
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="app/templates")

class Producto(BaseModel):
    id_producto: str
    cantidad: int

class Pedido(BaseModel):
    productos: List[Producto]
    id_repartidor: str
    fecha_entrega: datetime


@app.post("/token")
async def login_token(username: str = Form(...), password: str = Form(...)):
    if autenticar_usuario(username, password):
        # Si el usuario es válido, generar el token
        token = crear_token({"sub": username})
        return {"access_token": token}
    else:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

@app.post("/entrega")
async def registrar_pedido(pedido: Pedido, token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM repartidores WHERE id_repartidor = ?', (pedido.id_repartidor,))
    if cursor.fetchone()[0] == 0:
        raise HTTPException(status_code=400, detail="Repartidor no válido")

    for producto in pedido.productos:
        cursor.execute('SELECT COUNT(*) FROM productos WHERE id_producto = ?', (producto.id_producto,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=400, detail=f"Producto {producto.id_producto} no válido")

        fecha_entrega_str = pedido.fecha_entrega.isoformat()
        cursor.execute('''
        INSERT INTO pedidos (id_producto, id_repartidor, cantidad, fecha_entrega)
        VALUES (?, ?, ?, ?)
        ''', (producto.id_producto, pedido.id_repartidor, producto.cantidad, fecha_entrega_str))

    conn.commit()
    return {"mensaje": "Pedidos registrados exitosamente", "data": pedido}

@app.get("/repartidores")
async def obtener_repartidores(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM repartidores')
    rows = cursor.fetchall()
    return {"repartidores": rows}

@app.get("/productos")
async def obtener_productos(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    rows = cursor.fetchall()
    return {"productos": rows}

@app.get("/metricas")
async def obtener_metricas(token: str = Depends(oauth2_scheme)):
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    cursor = conn.cursor()

    cursor.execute('''
    SELECT id_repartidor, strftime('%Y-%m-%d', fecha_entrega) as dia, COUNT(*) as entregas
    FROM pedidos
    GROUP BY id_repartidor, dia
    ''')
    entregas_por_dia = cursor.fetchall()

    cursor.execute('''
    SELECT id_producto, SUM(cantidad) as cantidad_vendida
    FROM pedidos
    GROUP BY id_producto
    ORDER BY cantidad_vendida DESC
    ''')
    productos_mas_vendidos = cursor.fetchall()

    cursor.execute('''
    SELECT id_repartidor, COUNT(*) as total_pedidos
    FROM pedidos
    GROUP BY id_repartidor
    ''')
    pedidos_por_repartidor = cursor.fetchall()

    cursor.execute('''
    SELECT id_repartidor, SUM(cantidad) as total_productos_entregados
    FROM pedidos
    GROUP BY id_repartidor
    ''')
    total_productos_por_repartidor = cursor.fetchall()

    cursor.execute('''
    SELECT strftime('%Y-%m-%d', fecha_entrega) as dia, COUNT(*) as total_entregas
    FROM pedidos
    GROUP BY dia
    ORDER BY total_entregas DESC
    LIMIT 1
    ''')
    dia_max_entregas = cursor.fetchone()

    return {
        "entregas_por_dia": entregas_por_dia,
        "productos_mas_vendidos": productos_mas_vendidos,
        "pedidos_por_repartidor": pedidos_por_repartidor,
        "total_productos_por_repartidor": total_productos_por_repartidor,
        "dia_max_entregas": dia_max_entregas
    }

@app.get("/monitoreo", response_class=HTMLResponse)
async def monitoreo(request: Request):
    token = request.cookies.get("token")
    
    if not token:
        raise HTTPException(status_code=401, detail="No se encontró un token")

    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id_repartidor, strftime('%H', fecha_entrega) as hora, COUNT(*) as entregas
    FROM pedidos
    GROUP BY id_repartidor, hora
    ''')
    entregas_por_hora = cursor.fetchall()
    
    cursor.execute('''
    SELECT p.nombre, SUM(pe.cantidad) as cantidad_vendida
    FROM pedidos pe
    JOIN productos p ON pe.id_producto = p.id_producto
    GROUP BY pe.id_producto
    ORDER BY cantidad_vendida DESC
    ''')
    productos_mas_vendidos = cursor.fetchall()
    

    cursor.execute('''
    SELECT id_repartidor, strftime('%Y-%m-%d', fecha_entrega) as dia, COUNT(*) as entregas
    FROM pedidos
    GROUP BY id_repartidor, dia
    ''')
    entregas_por_dia = cursor.fetchall()

    cursor.execute('''
    SELECT id_repartidor, COUNT(*) as total_pedidos
    FROM pedidos
    GROUP BY id_repartidor
    ''')
    pedidos_por_repartidor = cursor.fetchall()

    cursor.execute('''
    SELECT id_repartidor, SUM(cantidad) as total_productos_entregados
    FROM pedidos
    GROUP BY id_repartidor
    ''')
    total_productos_por_repartidor = cursor.fetchall()

    cursor.execute('''
    SELECT strftime('%Y-%m-%d', fecha_entrega) as dia, COUNT(*) as total_entregas
    FROM pedidos
    GROUP BY dia
    ORDER BY total_entregas DESC
    LIMIT 1
    ''')
    dia_max_entregas = cursor.fetchone()
    

    repartidores = {}
    for repartidor, hora, entregas in entregas_por_hora:
        if repartidor not in repartidores:
            repartidores[repartidor] = {}
        repartidores[repartidor][hora] = entregas
    
    labels_horas = sorted({hora for _, hora, _ in entregas_por_hora})
    datasets_entregas = []
    for repartidor, horas in repartidores.items():
        entregas = [horas.get(hora, 0) for hora in labels_horas]
        datasets_entregas.append({
            "label": repartidor,
            "data": entregas
        })
    
    labels_productos = [producto for producto, _ in productos_mas_vendidos]
    data_productos = [cantidad for _, cantidad in productos_mas_vendidos]
    

    labels_dias = sorted(set(dia for _, dia, _ in entregas_por_dia))
    datasets_entregas_por_dia = []
    for repartidor in set(r for r, _, _ in entregas_por_dia):
        entregas = [next((e for r, d, e in entregas_por_dia if r == repartidor and d == dia), 0) for dia in labels_dias]
        datasets_entregas_por_dia.append({
            "label": repartidor,
            "data": entregas
        })
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "labels_horas": labels_horas,
        "datasets_entregas": datasets_entregas,
        "labels_productos": labels_productos,
        "data_productos": data_productos,
        "labels_dias": labels_dias,
        "datasets_entregas_por_dia": datasets_entregas_por_dia,
        "pedidos_por_repartidor": pedidos_por_repartidor,
        "total_productos_por_repartidor": total_productos_por_repartidor,
        "dia_max_entregas": dia_max_entregas
    })

# Lógica de autenticación centralizada
def autenticar_usuario(username: str, password: str):
    if (username == "user1" and password == "password") or (username == "admin" and password == "password"):
        return True
    return False
    
# Vista del formulario de login
@app.get("/login", response_class=HTMLResponse)
async def mostrar_login():
    with open("app/templates/login.html") as f:
        return HTMLResponse(content=f.read())

# Este endpoint maneja el POST del formulario de login y redirige
@app.post("/login")
async def handle_login(username: str = Form(...), password: str = Form(...)):
    if autenticar_usuario(username, password):
        # Si el usuario es válido, generar el token
        token = crear_token({"sub": username})
        response = RedirectResponse(url="/monitoreo")  # Redirigir a /monitoreo tras el login
        response.set_cookie(key="token", value=token)  # Guardar token en la cookie
        return response
    else:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")


handler = Mangum(app)