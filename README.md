# Sistema de Gestión de Inventario y Ventas

## 1. Integrantes del Equipo

- Nombre Completo 1 (Documento / Correo)
- Nombre Completo 2 (Documento / Correo)
- Nombre Completo 3 (Documento / Correo)

## 2. Descripción del Negocio y Justificación

### Contexto general del problema a resolver

Las pequeñas tiendas necesitan controlar de forma organizada sus productos, clientes y ventas. Cuando esta información se administra manualmente pueden presentarse errores en el inventario, dificultades para consultar ventas y pérdida de información.

Este proyecto propone desarrollar una aplicación en Python utilizando PEEWEE ORM para gestionar una base de datos relacional que permita almacenar y consultar información relacionada con clientes, categorías, productos y ventas.

La aplicación será diseñada para trabajar con diferentes motores de bases de datos, permitiendo estudiar el comportamiento de una misma aplicación sobre SQLite, MySQL y PostgreSQL.

### Objetivo de la aplicación

Desarrollar una aplicación en Python que permita administrar el inventario y las ventas de una tienda mediante una base de datos relacional, utilizando PEEWEE ORM y diferentes motores de bases de datos.

## 3. Entidades Principales del Dominio

### Cliente

Representa a las personas que realizan compras.

Relación:

- Un cliente puede realizar muchas ventas (1:N).

### Categoria

Representa los grupos o categorías a los que pertenecen los productos.

Relación:

- Una categoría puede contener muchos productos (1:N).

### Producto

Representa los productos disponibles para la venta.

Relaciones:

- Un producto pertenece a una categoría.
- Un producto puede aparecer en muchos detalles de venta.

### Venta

Representa una transacción realizada por un cliente.

Relaciones:

- Una venta pertenece a un cliente.
- Una venta puede contener muchos detalles de venta.

### DetalleVenta

Representa cada producto incluido dentro de una venta.

Relaciones:

- Pertenece a una venta.
- Hace referencia a un producto.

Esta entidad permite representar la relación N:M entre Venta y Producto.

## 4. Matriz de Entornos y Conexiones

| Motor | Proveedor/Entorno | Uso |
|---|---|---|
| SQLite | Archivo local | Desarrollo y pruebas |
| MySQL | AiViven.io | Base de datos remota |
| PostgreSQL | Neon.tech | Base de datos remota |
| PostgreSQL | Render.com | Base de datos remota |

## 5. Instrucciones de Ejecución

### Instalación de librerías

```bash
pip install peewee psycopg2-binary pymysql