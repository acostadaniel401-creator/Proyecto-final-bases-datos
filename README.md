# Sistema de Gestión de Inventario y Ventas (SOFA)

## 1. Integrantes del Equipo

- Daniel Josue Acosta Galindo (10185664213 / acostadaniel345@gmail.com)
- Sebastian Hernandez Mendoza (1256897453 / sebastianmn8@gmail.com)

## 2. Descripción del Negocio y Justificación

### Contexto general del problema a resolver

Las pequeñas tiendas de barrio y comercios locales necesitan controlar de forma ágil y organizada sus existencias de productos, registro de clientes y transacciones de ventas diarias. Cuando esta información se administra de forma manual (libretas o planillas aisladas), se presentan inconsistencias de inventario, descuadres de caja, falta de trazabilidad en las compras y demoras al consultar el historial de ventas.

Este proyecto propone desarrollar una solución centralizada en Python utilizando el ORM Peewee para gestionar una base de datos relacional normalizada que permita registrar, consultar, actualizar y eliminar información relacionada con clientes, categorías, productos, ventas y detalles de venta.

La aplicación está diseñada bajo una arquitectura multi-motor, permitiendo alternar de forma transparente entre motores locales (SQLite) y motores alojados en la nube (MySQL en Aiven.io, PostgreSQL en Neon.tech y PostgreSQL en Render.com).

### Objetivo de la aplicación

Desarrollar una aplicación en Python que administre de manera íntegra el inventario y las ventas de una tienda comercial mediante una base de datos relacional, implementando operaciones CRUD completas y consultas relacionales avanzadas con Peewee ORM a través de múltiples motores de bases de datos.

## 3. Entidades Principales del Dominio

El modelo relacional consta de 5 entidades principales normalizadas:

### Cliente

Representa a los compradores registrados en la tienda.

- **Campos**: `id` (PK), `nombre`, `correo` (UNIQUE), `telefono`.
- **Relación**: Un cliente puede realizar múltiples ventas (1:N con `Venta`).

### Categoria

Clasificación temática o por tipo de los artículos comerciales.

- **Campos**: `id` (PK), `nombre` (UNIQUE).
- **Relación**: Una categoría agrupa uno o varios productos (1:N con `Producto`).

### Producto

Catálogo de mercancía disponible para comercialización.

- **Campos**: `id` (PK), `nombre`, `precio`, `stock`, `categoria_id` (FK).
- **Relación**: Pertenece a una categoría (N:1) y puede estar presente en múltiples transacciones (1:N con `DetalleVenta`).

### Venta

Encabezado de cada comprobante o transacción realizada por un cliente.

- **Campos**: `id` (PK), `fecha`, `cliente_id` (FK), `total`.
- **Relación**: Pertenece a un cliente (N:1) y se desglosa en uno o más renglones de detalle (1:N con `DetalleVenta`).

### DetalleVenta

Renglón individual de compra que asocia un producto vendido con una venta específica, registrando cantidad y precio histórico.

- **Campos**: `id` (PK), `venta_id` (FK), `producto_id` (FK), `cantidad`, `precio_unitario`.
- **Relación**: Resuelve la relación N:M entre `Venta` y `Producto`.

## 4. Matriz de Entornos y Conexiones

| Motor                | Proveedor / Entorno               | Tipo              | Uso en el Proyecto                                    |
| :------------------- | :-------------------------------- | :---------------- | :---------------------------------------------------- |
| **SQLite**     | Archivo local (`mi_negocio.db`) | Local embebido    | Pruebas locales y desarrollo rápido sin conexión    |
| **MySQL**      | Aiven.io Cloud                    | Remoto gestionado | Motor relacional MySQL 8 con conexión SSL requerida  |
| **PostgreSQL** | Neon.tech Serverless              | Remoto serverless | Motor PostgreSQL cloud de alta disponibilidad         |
| **PostgreSQL** | Render.com                        | Remoto gestionado | Instancia cloud PostgreSQL para despliegue y respaldo |

## 5. Instrucciones de Ejecución

### 1. Requisitos Previos

Tener instalado Python 3.10 o superior en el sistema.

### 2. Instalación de Dependencias

Ejecutar en la terminal la instalación de las librerías necesarias para Peewee y los controladores de bases de datos:

```bash
pip install peewee psycopg2-binary pymysql
```

### 3. Configuración del Motor

En el archivo [app.py](<file:///c:/Users/eduar/OneDrive/Escritorio/Todo/ADSO%20SENA/Bases%20de%20Datos/Proyecto-final-bases-datos/app.py>), en la sección del **Bloque A**, ajustar la variable `MOTOR_ACTIVO` con la opción deseada:

- `"sqlite"` (por defecto, no requiere credenciales externas).
- `"mysql_aiven"`
- `"postgres_neon"`
- `"postgres_render"`

### 4. Ejecución del Programa

Ejecutar el script principal desde la consola:

```bash
python app.py
```

El script permite operar en dos modalidades:

- **Demostración Automática**: Ejecuta de forma secuencial la creación de tablas, inserción (Create), consultas con JOIN (Read), modificación de datos (Update) y eliminación (Delete).
- **Menú Interactivo**: Permite gestionar manualmente clientes, productos, categorías y ventas.

## 6. Estructura del Repositorio

```
proyecto-final-bases-datos/
├── README.md                          <- Documentación del proyecto (este archivo)
├── app.py                             <- Script Python principal (Conexión, Modelos ORM y CRUD)
├── sql/
│   ├── schema_sqlite.sql              <- Script DDL para SQLite
│   ├── schema_mysql.sql               <- Script DDL para MySQL
│   ├── schema_postgres.sql            <- Script DDL para PostgreSQL
│   └── seed_data.sql                  <- Script DML con datos de prueba y consulta analítica con JOIN
├── docs/
│   └── der.png                        <- Diagrama Entidad-Relación (DER)
└── evidencias/
    ├── conexion_neon_dbeaver.png      <- Captura de conexión activa en DBeaver con Neon
    ├── conexion_aiven_heidisql.png    <- Captura de conexión activa en HeidiSQL con Aiven
    ├── conexion_render_pgadmin.png    <- Captura de conexión activa en pgAdmin con Render
    └── consulta_sql_gui.png           <- Captura de consulta SELECT con JOIN en cliente gráfico
```
