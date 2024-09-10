import sqlite3

conn = sqlite3.connect('pedidos.db')
cursor = conn.cursor()

# Crear tabla pedidos
cursor.execute('''

CREATE TABLE IF NOT EXISTS pedidos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
id_producto TEXT,
id_repartidor TEXT,
cantidad INTEGER,
fecha_entrega TEXT)


''')

conn.commit()