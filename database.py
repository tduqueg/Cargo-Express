import psycopg2
import os


conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),  
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=5432
)
cursor = conn.cursor()

# Crear tabla pedidos
cursor.execute('''
CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    id_producto TEXT NOT NULL,
    id_repartidor TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha_entrega TIMESTAMP NOT NULL
)
''')

# Crear tabla repartidores
cursor.execute('''
CREATE TABLE IF NOT EXISTS repartidores (
    id_repartidor TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
)
''')

# Crear tabla productos
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id_producto TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL
)
''')

conn.commit()
