# Documentación de la Aplicación de Gestión de Pedidos y Monitoreo

## Introducción

Esta aplicación permite registrar pedidos y monitorear diferentes métricas sobre la operación de entregas. Además, cuenta con un sistema de autenticación basado en **Tokens JWT**, que asegura que solo usuarios autenticados puedan acceder a los datos y funcionalidades de la aplicación.

### Características principales:

- **Autenticación con Tokens JWT**.
- Registro de pedidos de productos.
- Consulta de repartidores y productos.
- Visualización de métricas de rendimiento (entregas por día, productos más vendidos, total de pedidos por repartidor).

---

## Clonación del Repositorio

Para comenzar, clona el repositorio desde GitHub:

```bash
git clone https://github.com/tduqueg/Cargo-Express.git
cd Cargo-Express
```

## Requisitos del Proyecto

Para ejecutar la aplicación es necesario contar con los siguientes elementos:

- Python 3.8 o superior.
- FastAPI: Un framework de Python para construir APIs.
- SQLite3: Base de datos ligera para almacenar los datos de productos, repartidores y pedidos.

### Dependencias

Para instalar las dependencias, es necesario crear un entorno virtual y luego instalar los paquetes indicados en `requirements.txt`.

#### Pasos:

1. Crear un entorno virtual:

```bash
python -m venv venv
```

2. Activar el entorno virtual (en Linux o macOS):

```bash
source venv/bin/activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

# Iniciar el Proyecto

Sigue los siguientes pasos para iniciar la aplicación.

1. Asegúrate de haber instalado las dependencias como se mencionó en la sección anterior.
2. Inicia la aplicación FastAPI con el siguiente comando:

```bash
uvicorn main:app --reload
```

## Esto lanzará el servidor en `http://127.0.0.1:8000`.

## Autenticación

Para interactuar con la aplicación, es necesario autenticar al usuario mediante un token JWT. Este token debe ser incluido en cada solicitud a los endpoints protegidos.

### Obtener un Token de Acceso

#### Endpoint

```plaintext
POST /token
```

#### Descripción:

Este endpoint genera un token JWT válido por 30 minutos, que se deberá utilizar en las solicitudes a los endpoints protegidos.

#### Parámetros:

`username (requerido)`: Nombre de usuario.
`password (requerido)`: Contraseña del usuario.

#### Ejemplo de Solicitud en Postman:

Método: `POST`
URL: `http://localhost:8000/token`
En el cuerpo de la solicitud (seleccionar **x-www-form-urlencoded**):

- username: `user1`
- password: `password`

#### Respuesta Exitosa:

```json
{
  "access_token": "TOKEN_JWT_GENERADO"
}
```

El token obtenido debe ser utilizado en las siguientes solicitudes dentro del Header de la petición, en el campo Authorization, con el formato:

```plaintext
Bearer TOKEN_JWT_GENERADO
```

---

# Funcionalidades Principales

## Registrar un Pedido

### Endpoint

```plaintext
POST /entrega
```

#### Descripción:

Permite registrar un pedido de productos, especificando el repartidor y la fecha de entrega.

Parámetros:

- `id_repartidor` (requerido): ID del repartidor encargado de la entrega.
- `productos` (requerido): Lista de productos con sus cantidades.
- `fecha_entrega` (requerido): Fecha y hora de la entrega (en formato ISO8601).

#### Ejemplo de Solicitud:

```json
{
  "id_repartidor": "r1",
  "productos": [
    { "id_producto": "p1", "cantidad": 3 },
    { "id_producto": "p2", "cantidad": 5 }
  ],
  "fecha_entrega": "2024-09-09T15:30:00"
}
```

#### Respuesta Exitosa:

```json
{
  "mensaje": "Pedidos registrados exitosamente",
  "data": {
    "id_repartidor": "r1",
    "productos": [
      { "id_producto": "p1", "cantidad": 3 },
      { "id_producto": "p2", "cantidad": 5 }
    ],
    "fecha_entrega": "2024-09-09T15:30:00"
  }
}
```

---

# Obtener Repartidores

## Endpoint

```plaintext
GET /repartidores
```

### Descripción:

Devuelve una lista de los repartidores registrados en la base de datos.

Requiere Token:
Sí. Debe incluirse el token JWT en la cabecera de la solicitud.

### Respuesta Exitosa:

```json
{
  "repartidores": [
    { "id_repartidor": "r1", "nombre": "Carlos" },
    { "id_repartidor": "r2", "nombre": "Maria" }
  ]
}
```

---

# Obtener Productos

### Endpoint

```plaintext
GET /products
```

### Descripción:

Devuelve una lista de los productos registrados en la base de datos.

### Requiere Token:

Sí. Debe incluirse el token JWT en la cabecera de la solicitud.

### Respuesta Exitosa:

```json
{
  "productos": [
    { "id_producto": "p1", "nombre": "Producto 1" },
    { "id_producto": "p2", "nombre": "Producto 2" }
  ]
}
```

---

# Métricas de Monitoreo

## Obtener Métricas de Entregas

### Endpoint

```plaintext
GET /metricas
```

#### Descripción:

Devuelve un conjunto de métricas relacionadas con las entregas de pedidos.

#### Métricas Devueltas:

1. **Cantidad de entregas por día por repartidor**:

- Muestra cuántas entregas realizó cada repartidor por cada hora del día.

2. **Productos más vendidos**:

- Lista de productos ordenados por la cantidad total vendida.

3. **Cantidad total de pedidos por repartidor**:

- Número total de pedidos entregados por cada repartidor.

4. **Cantidad total de productos entregados por repartidor**:

- Número total de productos entregados por cada repartidor.

5. **Día con mayor número de entregas**:

- El día con el mayor número de entregas registradas.

#### Requiere Token:

Sí. Debe incluirse el token JWT en la cabecera de la solicitud.

#### Ejemplo de Respuesta:

```json
{
  "entregas_por_dia": [["101", "2024-09-09", 7]],
  "productos_mas_vendidos": [
    ["pk0001", 15],
    ["pk0004", 8]
  ],
  "pedidos_por_repartidor": [["101", 7]],
  "total_productos_por_repartidor": [["101", 23]],
  "dia_max_entregas": ["2024-09-09", 7]
}
```

---

# Preguntas Teóricas

1. **Escalabilidad**: Recomendaría utilizar servicios escalables, como bases de datos serverless (DynamoDB o Aurora Serverless) que permiten manejar aumentos en la demanda sin requerir una reconfiguración manual.
2. **Microservicios**: Dividir la solución en microservicios para mejorar la capacidad de escalar independientemente cada parte del sistema.
3. **Serverless**: Utilizar servicios serverless (como AWS Lambda y API Gateway) para gestionar cargas fluctuantes de manera eficiente.

## Capacidad de la solución

La solución planteada, si se construye con una arquitectura escalable como la basada en microservicios y utilizando recursos serverless, puede soportar el crecimiento proyectado sin necesidad de modificaciones importantes.
