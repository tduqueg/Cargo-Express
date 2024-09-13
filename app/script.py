import requests
import uuid
import random
import json
import datetime
import time

# Datos de productos y repartidores
productos = [
  {"IdProducto": "pk0001", "producto": "Moneda"},
  {"IdProducto": "pk0002", "producto": "Estuche para gafas"},
  {"IdProducto": "pk0003", "producto": "Pequeño espejo de bolsillo"},
  {"IdProducto": "pk0004", "producto": "Pendrive"},
  {"IdProducto": "pk0005", "producto": "Tarjeta SIM"},
  {"IdProducto": "pk0006", "producto": "Adaptador de corriente"},
  {"IdProducto": "pk0007", "producto": "Tijeras pequeñas"},
  {"IdProducto": "pk0008", "producto": "Pila de botón"},
  {"IdProducto": "pk0009", "producto": "Goma de borrar"},
  {"IdProducto": "pk0010", "producto": "Clip sujetapapeles"}
]

repartidores = [
  {"IdRepartidor": "101", "Nombre": "María López"},
  {"IdRepartidor": "102", "Nombre": "Carlos García"},
  {"IdRepartidor": "103", "Nombre": "Ana Fernández"},
  {"IdRepartidor": "104", "Nombre": "Juan Martínez"},
  {"IdRepartidor": "105", "Nombre": "Laura Sánchez"},
  {"IdRepartidor": "106", "Nombre": "Pedro Gómez"},
  {"IdRepartidor": "107", "Nombre": "Elena Rodríguez"},
  {"IdRepartidor": "108", "Nombre": "Jorge Pérez"},
  {"IdRepartidor": "109", "Nombre": "Sofía Morales"},
  {"IdRepartidor": "110", "Nombre": "Daniel Castillo"}
]

# Función para obtener el token JWT
def obtener_token():
    url = "http://127.0.0.1:8000/token"
    payload = {
        "username": "user1",
        "password": "password"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print("Error al obtener el token")
        return None

# Función para generar una fecha y hora aleatoria en los últimos 30 días
def generar_fecha_aleatoria():
    hoy = datetime.datetime.now()
    dias_atras = random.randint(0, 30)  
    horas = random.randint(0, 23) 
    minutos = random.randint(0, 59)  
    fecha_aleatoria = hoy - datetime.timedelta(days=dias_atras)
    fecha_aleatoria = fecha_aleatoria.replace(hour=horas, minute=minutos)  
    return fecha_aleatoria.isoformat()  

# Función para registrar un pedido entregado
def registrar_pedido_entregado(pedido_id, repartidor, productos, token):
    url = "http://127.0.0.1:8000/entrega"
    payload = {
        "id_repartidor": repartidor["IdRepartidor"],
        "productos": [{"id_producto": p["IdProducto"], "cantidad": random.randint(1, 5)} for p in productos],
        "fecha_entrega": generar_fecha_aleatoria()  # Usa la fecha aleatoria generada
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        print("### Pedido entregado, registrado exitosamente")
    else:
        print("### Error al registrar el pedido entregado", response.text)

# Función principal
def main():
    token = obtener_token()  # Obtener el token JWT
    if not token:
        return
    
    while True:
        pedido_id = str(uuid.uuid4())
        repartidor = random.choice(repartidores)
        productos_seleccionados = random.choices(productos, k=random.randint(1, 5))

        registrar_pedido_entregado(pedido_id, repartidor, productos_seleccionados, token)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
