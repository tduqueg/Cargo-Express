# Este script permite insertar los 10 repartidores y productos en la base de datos
import sqlite3

conn = sqlite3.connect('cargo_express.db', check_same_thread=False)
cursor = conn.cursor()

# Insertar productos
productos = [
    ('pk0001', 'Moneda', 1.00),
    ('pk0002', 'Estuche para gafas', 8.00),
    ('pk0003', 'Pequeño espejo de bolsillo', 5.00),
    ('pk0004', 'Pendrive', 12.00),
    ('pk0005', 'Tarjeta SIM', 3.00),
    ('pk0006', 'Adaptador de corriente', 10.00),
    ('pk0007', 'Tijeras pequeñas', 4.00),
    ('pk0008', 'Pila de botón', 2.50),
    ('pk0009', 'Goma de borrar', 0.50),
    ('pk0010', 'Clip sujetapapeles', 0.20)
]

# Insertar repartidores
repartidores = [
    ('101', 'María López'),
    ('102', 'Carlos García'),
    ('103', 'Ana Fernández'),
    ('104', 'Juan Martínez'),
    ('105', 'Laura Sánchez'),
    ('106', 'Pedro Gómez'),
    ('107', 'Elena Rodríguez'),
    ('108', 'Jorge Pérez'),
    ('109', 'Sofía Morales'),
    ('110', 'Daniel Castillo')
]

# Insertar datos en las tablas
cursor.executemany('INSERT INTO productos VALUES (?, ?, ?)', productos)
cursor.executemany('INSERT INTO repartidores VALUES (?, ?)', repartidores)

conn.commit()
conn.close()
