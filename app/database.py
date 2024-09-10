import sqlite3

conn = sqlite3.connect('cargo_express.db')
cursor = conn.cursor()

# Crear tabla pedidos
cursor.execute('''

CREATE TABLE IF NOT EXISTS pedidos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
id_producto TEXT NOT NULL,
id_repartidor TEXT NOT NULL,
cantidad INTEGER NOT NULL,
fecha_entrega TEXT NOT NULL,
FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
FOREIGN KEY (id_repartidor) REFERENCES repartidores(id_repartidor)
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