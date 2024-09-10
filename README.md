# Documentación de la Aplicación de Gestión de Pedidos y Monitoreo

## Introducción

Esta aplicación permite registrar pedidos y monitorear diferentes métricas sobre la operación de entregas. Además, cuenta con un sistema de autenticación basado en **Tokens JWT**, que asegura que solo usuarios autenticados puedan acceder a los datos y funcionalidades de la aplicación.

### Características principales:

- **Autenticación con Tokens JWT**.
- Registro de pedidos de productos.
- Consulta de repartidores y productos.
- Visualización de métricas de rendimiento (entregas por hora, productos más vendidos, total de pedidos por repartidor).

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
