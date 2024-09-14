# Documentación de la Aplicación de Gestión de Pedidos y Monitoreo Cargo-Express

## Introducción

Esta aplicación permite registrar pedidos y monitorear diferentes métricas sobre la operación de entregas. Cuenta con un sistema de autenticación basado en Tokens JWT, que asegura que solo usuarios autenticados puedan acceder a los datos y funcionalidades de la aplicación.

## Características principales:

- Autenticación con Tokens JWT.
- Registro de pedidos de productos.
- Consulta de repartidores y productos.
- Visualización de métricas de rendimiento (entregas por día, productos más vendidos, total de pedidos por repartidor).
- Desplegada en AWS Lambda y conectada a Amazon RDS con PostgreSQL.
- Escalabilidad mediante arquitectura serverless y seguridad mediante VPC y Security Groups.

## Despliegue en AWS Lambda

La aplicación está desplegada en AWS Lambda, utilizando una base de datos en Amazon RDS (PostgreSQL). La conectividad segura entre Lambda y RDS se asegura mediante el uso de una VPC. Los siguientes componentes están involucrados:

- **AWS Lambda**: La lógica de la aplicación.
- **Amazon RDS (PostgreSQL)**: La base de datos donde se almacenan los datos.
- **VPC**: La red privada que contiene Lambda y RDS.
- **Subnets y Security Groups**: Para asegurar el tráfico entre Lambda y RDS.

### Variables de Entorno

El archivo `.env` debe incluir las siguientes variables de conexión a la base de datos:

```env
DB_HOST=<host_rds>
DB_NAME=<nombre_base_de_datos>
DB_USER=<usuario_base_de_datos>
DB_PASSWORD=<contraseña_base_de_datos>
```

La conexión a la base de datos está restringida por un **Security Group**, lo que garantiza que solo las funciones Lambda puedan acceder a RDS.

## Autenticación

Para interactuar con la aplicación, es necesario autenticar al usuario mediante un token JWT. Este token debe ser incluido en cada solicitud a los endpoints protegidos.

### Obtener un Token de Acceso

Endpoint: `POST /token`
Descripción: Genera un token JWT válido por 30 minutos, que se debe utilizar en las solicitudes a los endpoints protegidos.

**Ejemplo de Solicitud:**

- **Método**: POST
- **URL:** `https://hbvy5e4idefg5dyhendk7wrxqq0mvqzz.lambda-url.us-east-1.on.aws/token`
- **Cuerpo de la solicitud (x-www-form-urlencoded):**
- - `username`:`user1`
- - `password`: `password`
    **Respuesta Exitosa:**

```json
{
  "access_token": "TOKEN_JWT_GENERADO"
}
```

El token obtenido debe ser utilizado en el campo Authorization de las siguientes solicitudes, con el formato: `Bearer TOKEN_JWT_GENERADO`

## Funcionalidades Principales

### Registrar un Pedido

- **Endpoint:** `POST /entrega`
- **Descripción:** Permite registrar un pedido de productos, especificando el repartidor y la fecha de entrega.
  **Ejemplo de Solicitud:**

```json
{
  "id_repartidor": "101",
  "productos": [
    { "id_producto": "pk0001", "cantidad": 3 },
    { "id_producto": "pk0004", "cantidad": 5 }
  ],
  "fecha_entrega": "2024-09-09T15:30:00"
}
```

**Respuesta Exitosa:**

```json
{
  "mensaje": "Pedidos registrados exitosamente",
  "data": {
    "id_repartidor": "101",
    "productos": [
      { "id_producto": "pk0001", "cantidad": 3 },
      { "id_producto": "pk0004", "cantidad": 5 }
    ],
    "fecha_entrega": "2024-09-09T15:30:00"
  }
}
```

### Obtener Repartidores

- **Endpoint:** `GET /repartidores`
- **Descripción:** Devuelve una lista de los repartidores registrados.
  **Respuesta Exitosa:**

```json
{
  "repartidores": [
    { "id_repartidor": "101", "nombre": "María López" },
    { "id_repartidor": "102", "nombre": "Carlos García" }
  ]
}
```

### Obtener Productos

- **Endpoint:** `GET /productos`
- **Descripción:** Devuelve una lista de los productos registrados.
  **Respuesta Exitosa:**

```json
{
  "productos": [
    { "id_producto": "pk0001", "nombre": "Moneda" },
    { "id_producto": "pk0004", "nombre": "Pendrive" }
  ]
}
```

### Métricas de Monitoreo

- **Endpoint:** `GET /metricas`
- **Descripción:** Devuelve métricas relacionadas con las entregas de pedidos.
  **Ejemplo de Respuesta:**

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

## Front-End de la Aplicación

La interacción del usuario final con la aplicación se realiza a través de dos principales URLs:

### 1. /login (Inicio de Sesión)

- **Descripción:** Página de inicio de sesión donde el usuario ingresa sus credenciales para autenticarse.
- **Flujo:**

1. El usuario accede a la URL `/login`.
2. Ingresa su **username** y **password**.
3. Al enviar el formulario, las credenciales se envían al backend y, si son correctas, se genera un token JWT.
4. El token JWT se guarda automáticamente en una cookie del navegador.
5. El usuario es redirigido a la URL `/monitoreo`, donde se encuentra el dashboard con las métricas.
   **Ejemplo:**

- **URL:** `https://hbvy5e4idefg5dyhendk7wrxqq0mvqzz.lambda-url.us-east-1.on.aws/login`
- **Formulario:**
- - `username`: `user1`
- - `password`: `password`

### 2. /monitoreo (Dashboard de Métricas)

- **Descripción:** Esta URL muestra el dashboard con las métricas de entregas, productos más vendidos, y pedidos por repartidor.
- **Flujo:**

1. Al acceder a esta URL, la aplicación verifica si el token JWT está almacenado en las cookies del navegador.
2. Si el token es válido, se muestran las métricas de monitoreo en un formato visual (gráficas y tablas).
3. Si el token no es válido o ha expirado, se redirige al usuario nuevamente a la página de inicio de sesión.
   **Ejemplo:**
   **URL:** `https://hbvy5e4idefg5dyhendk7wrxqq0mvqzz.lambda-url.us-east-1.on.aws/monitoreo`

#### Dashboard de Monitoreo

El dashboard permite ver las siguientes métricas:

- **Entregas por día y por repartidor.**
- **Productos más vendidos.**
- **Pedidos totales por repartidor.**
- **Día con el mayor número de entregas registradas.**

## Preguntas Teóricas

### Escalabilidad de la Solución

La arquitectura serverless permite escalar automáticamente según la demanda con AWS Lambda. Amazon RDS puede escalar mediante read replicas y el uso de Multi-AZ. Además, la solución puede dividirse en microservicios independientes.

### Seguridad de la Solución

La conexión entre Lambda y RDS está asegurada mediante una VPC, y solo Lambda puede acceder a la base de datos a través de los Security Groups. Las solicitudes HTTP están protegidas mediante JWT, que garantiza que solo usuarios autenticados puedan acceder a la API.

### Proyección de Crecimiento

Con un crecimiento del 500% el primer año y el doble en el segundo, la solución planteada puede soportar la carga adicional mediante la escalabilidad automática de Lambda y la replicación de RDS. Para futuras expansiones, se recomienda monitorear la carga de trabajo y ajustar los recursos de AWS según sea necesario.

## Diagramas

### Diagrama de Arquitectura: Representa la interacción entre los componentes de AWS.
![ArquitecturaCargoExpress](https://github.com/user-attachments/assets/409cc6ef-4308-41af-baa1-2007ed87e652)


