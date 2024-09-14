import psycopg2
import uuid
import random
import datetime
import time
import os
from dotenv import load_dotenv

# Datos de productos y repartidores
productos = [
    {"IdProducto": "pk0001","producto": "Moneda","precio": 1.00},
    {"IdProducto": "pk0002","producto": "Estuche para gafas","precio": 8.00},
    {"IdProducto": "pk0003","producto": "Pequeño espejo de bolsillo","precio": 5.00},
    {"IdProducto": "pk0004","producto": "Pendrive","precio": 12.00},
    {"IdProducto": "pk0005","producto": "Tarjeta SIM","precio": 3.00},
    {"IdProducto": "pk0006","producto": "Adaptador de corriente","precio": 10.00},
    {"IdProducto": "pk0007","producto": "Tijeras pequeñas","precio": 4.00},
    {"IdProducto": "pk0008","producto": "Pila de botón","precio": 2.50},
    {"IdProducto": "pk0009", "producto": "Goma de borrar", "precio": 0.50},
    {"IdProducto": "pk0010","producto": "Clip sujetapapeles","precio": 0.20}
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

# Configuración de la base de datos (modifica con tus valores reales)
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=5432
)


cursor = conn.cursor()

# Función para generar una fecha y hora aleatoria en los últimos 30 días
def generar_fecha_aleatoria():
    hoy = datetime.datetime.now()
    dias_atras = random.randint(0, 30)
    horas = random.randint(0, 23)
    minutos = random.randint(0, 59)
    fecha_aleatoria = hoy - datetime.timedelta(days=dias_atras)
    fecha_aleatoria = fecha_aleatoria.replace(hour=horas, minute=minutos)
    return fecha_aleatoria

# Función para registrar un pedido entregado en la base de datos
def registrar_pedido_entregado(repartidor, productos):
    try:
        for producto in productos:
            cantidad = random.randint(1, 5)
            fecha_entrega = generar_fecha_aleatoria()


            cursor.execute('''
                INSERT INTO pedidos (id_producto, id_repartidor, cantidad, fecha_entrega)
                VALUES (%s, %s, %s, %s)
            ''', (producto['IdProducto'], repartidor['IdRepartidor'], cantidad, fecha_entrega))


        conn.commit()
        print(f"Pedido entregado registrado para {repartidor['Nombre']}")

    except Exception as e:
        conn.rollback()  
        print(f"Error al registrar el pedido: {e}")

# Función principal
def main():
    while True:
        repartidor = random.choice(repartidores)
        productos_seleccionados = random.choices(productos, k=random.randint(1, 5))

        registrar_pedido_entregado(repartidor, productos_seleccionados)
        time.sleep(0.1)  

if __name__ == "__main__":
    main()
