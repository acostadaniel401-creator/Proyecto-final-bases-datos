from peewee import *

# ==========================================
#
# 1. CONFIGURACIÓN DE CONEXIÓN
# Opciones: "sqlite" | "mysql_aiven" | "postgres_neon" | "postgres_render"
# ==========================================
MOTOR_ACTIVO = "sqlite"  # Cambiar según el motor deseado

if MOTOR_ACTIVO == "sqlite":
    db = SqliteDatabase("mi_negocio.db")

elif MOTOR_ACTIVO == "mysql_aiven":
    db = MySQLDatabase(
        "defaultdb",
        user="avnadmin",
        password="AVNS_TIXa703ee0xUyeoPppY",
        host="mysql-326f9b33-proyecto-final-bases-datos.f.aivencloud.com",
        port=23430,
        ssl={"ssl_mode": "REQUIRED"}
    )

elif MOTOR_ACTIVO == "postgres_neon":
    db = PostgresqlDatabase(
        "neondb",
        user="neondb_owner",
        password="npg_Mc9d7pJaYDFP",
        host="ep-soft-band-b4h2qt4l-pooler.c-6.us-east-2.aws.neon.tech",
        port=5432,
        sslmode="require"
    )

elif MOTOR_ACTIVO == "postgres_render":
    db = PostgresqlDatabase(
        "nombre_bd",
        user="postgresdb_4m4c_user",
        password="fProrns0cVSBrUZsM6QpssfCX5dLxKtV",
        host="dpg-dale9obl550s73avneog-a.ohio-postgres.render.com",
        port=5432,
        sslmode="require"
    )

else:
    raise ValueError(f"Motor no reconocido: '{MOTOR_ACTIVO}'. Verifique la configuración en el Bloque A.")

import sys
from datetime import datetime
from decimal import Decimal


# =============================================================================
# BLOQUE B: MODELOS PEEWEE (MAPEO OBJETO-RELACIONAL)
# Mínimo 4 entidades requeridas; aquí se implementan 5 entidades del dominio.
# =============================================================================

class BaseModel(Model):
    """Clase base que asocia todos los modelos al motor de base de datos activo."""
    class Meta:
        database = db


class Cliente(BaseModel):
    """Entidad 1: Clientes registrados en la tienda."""
    nombre = CharField(max_length=100)
    correo = CharField(max_length=150, unique=True)
    telefono = CharField(max_length=30, null=True)

    class Meta:
        table_name = "cliente"

    def __str__(self):
        return f"[Cliente #{self.id}] {self.nombre} ({self.correo})"


class Categoria(BaseModel):
    """Entidad 2: Clasificación de productos en el inventario."""
    nombre = CharField(max_length=80, unique=True)

    class Meta:
        table_name = "categoria"

    def __str__(self):
        return f"[Categoría #{self.id}] {self.nombre}"


class Producto(BaseModel):
    """Entidad 3: Catálogo de productos disponibles con control de stock."""
    nombre = CharField(max_length=120)
    precio = DecimalField(max_digits=12, decimal_places=2)
    stock = IntegerField(default=0)
    categoria = ForeignKeyField(Categoria, backref="productos", on_delete="RESTRICT")

    class Meta:
        table_name = "producto"

    def __str__(self):
        return f"[Producto #{self.id}] {self.nombre} | ${self.precio:,.2f} | Stock: {self.stock}"


class Venta(BaseModel):
    """Entidad 4: Encabezado de transacciones de venta asociadas a un cliente."""
    fecha = DateTimeField(default=datetime.now)
    cliente = ForeignKeyField(Cliente, backref="ventas", on_delete="RESTRICT")
    total = DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        table_name = "venta"

    def __str__(self):
        return f"[Venta #{self.id}] Fecha: {self.fecha} | Cliente: {self.cliente.nombre} | Total: ${self.total:,.2f}"


class DetalleVenta(BaseModel):
    """
    Entidad 5: Renglones individuales de la venta.
    Resuelve la relación N:M entre Venta y Producto con precio unitario congelado.
    """
    venta = ForeignKeyField(Venta, backref="detalles", on_delete="CASCADE")
    producto = ForeignKeyField(Producto, backref="detalles_venta", on_delete="RESTRICT")
    cantidad = IntegerField()
    precio_unitario = DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        table_name = "detalle_venta"
        indexes = (
            (("venta", "producto"), True),  # Clave única compuesta (evita producto duplicado en la misma venta)
        )

    def __str__(self):
        subtotal = self.cantidad * self.precio_unitario
        return f"  - {self.producto.nombre} x{self.cantidad} @ ${self.precio_unitario:,.2f} = ${subtotal:,.2f}"


# =============================================================================
# BLOQUE C: OPERACIONES CRUD COMPLETAS Y DEMOSTRACIÓN
# =============================================================================

# -----------------------------------------------------------------------------
# 1. GESTIÓN DEL ESQUEMA Y SEMILLERO (SEED)
# -----------------------------------------------------------------------------

def inicializar_base_datos():
    """Conecta a la base de datos activa y crea las tablas si no existen."""
    db.connect(reuse_if_open=True)
    tablas = [Cliente, Categoria, Producto, Venta, DetalleVenta]
    db.create_tables(tablas, safe=True)
    print(f"[OK] Conexión establecida con éxito con motor: '{MOTOR_ACTIVO}'.")
    print(f"[OK] Tablas verificadas/creadas: {[t._meta.table_name for t in tablas]}")


def sembrar_datos_iniciales():
    """Inserta datos de prueba si la base de datos está vacía."""
    if Categoria.select().count() > 0:
        print("[INFO] La base de datos ya contiene registros. No se duplicó el semillero.")
        return

    print("\n[SEED] Poblando base de datos con registros iniciales...")
    with db.atomic():
        # Categorías
        cat_bebidas = Categoria.create(nombre="Bebidas y Refrescos")
        cat_lacteos = Categoria.create(nombre="Lácteos y Derivados")
        cat_granos = Categoria.create(nombre="Granos y Abarrotes")
        cat_snacks = Categoria.create(nombre="Snacks y Confitería")
        cat_aseo = Categoria.create(nombre="Aseo y Cuidado Personal")

        # Clientes
        c1 = Cliente.create(nombre="Carlos Andres Gomez", correo="carlos.gomez@email.com", telefono="+57 310 1234567")
        c2 = Cliente.create(nombre="Maria Fernanda Rodriguez", correo="maria.rodriguez@email.com", telefono="+57 311 9876543")
        c3 = Cliente.create(nombre="Juan David Perez", correo="juan.perez@email.com", telefono="+57 312 4567890")
        c4 = Cliente.create(nombre="Laura Marcela Martinez", correo="laura.martinez@email.com", telefono="+57 315 3216549")
        c5 = Cliente.create(nombre="Andres Felipe Lopez", correo="andres.lopez@email.com", telefono="+57 320 6549871")

        # Productos
        p1 = Producto.create(nombre="Gaseosa Cola 1.5L", precio=Decimal("5500.00"), stock=50, categoria=cat_bebidas)
        p2 = Producto.create(nombre="Jugo Naranja 1L", precio=Decimal("4200.00"), stock=35, categoria=cat_bebidas)
        p3 = Producto.create(nombre="Leche Entera 1L", precio=Decimal("3800.00"), stock=60, categoria=cat_lacteos)
        p4 = Producto.create(nombre="Queso Campesino 500g", precio=Decimal("12500.00"), stock=25, categoria=cat_lacteos)
        p5 = Producto.create(nombre="Arroz Blanco 1kg", precio=Decimal("4600.00"), stock=100, categoria=cat_granos)
        p6 = Producto.create(nombre="Frijol Rojo 500g", precio=Decimal("5800.00"), stock=40, categoria=cat_granos)
        p7 = Producto.create(nombre="Papas Fritas 115g", precio=Decimal("3500.00"), stock=50, categoria=cat_snacks)
        p8 = Producto.create(nombre="Galletas Chocolate 180g", precio=Decimal("2900.00"), stock=75, categoria=cat_snacks)
        p9 = Producto.create(nombre="Jabón Corporal 3pk", precio=Decimal("8900.00"), stock=30, categoria=cat_aseo)
        p10 = Producto.create(nombre="Detergente Polvo 1kg", precio=Decimal("9400.00"), stock=25, categoria=cat_aseo)

        # Ventas iniciales con transacciones
        items_v1 = [(p1, 2), (p5, 2)]  # 2x5500 + 2x4600 = 20200
        crear_venta_transaccional(c1.id, items_v1)

        items_v2 = [(p3, 2), (p4, 1)]  # 2x3800 + 1x12500 = 20100
        crear_venta_transaccional(c2.id, items_v2)

        items_v3 = [(p7, 3), (p8, 2), (p2, 1)]  # 3x3500 + 2x2900 + 1x4200 = 20500
        crear_venta_transaccional(c3.id, items_v3)

        items_v4 = [(p9, 1), (p10, 2)]  # 1x8900 + 2x9400 = 27700
        crear_venta_transaccional(c4.id, items_v4)

        items_v5 = [(p5, 3), (p6, 2)]  # 3x4600 + 2x5800 = 25400
        crear_venta_transaccional(c5.id, items_v5)

    print("[SEED COMPLETADO] Se insertaron categorías, clientes, productos y ventas iniciales.")


# -----------------------------------------------------------------------------
# 2. CREATE (OPERACIONES DE INSERCIÓN)
# -----------------------------------------------------------------------------

def crear_cliente(nombre: str, correo: str, telefono: str = None) -> Cliente:
    """Crea y persiste un nuevo cliente en la base de datos."""
    cliente = Cliente.create(nombre=nombre.strip(), correo=correo.strip().lower(), telefono=telefono)
    print(f"[CREATE] Cliente creado exitosamente: ID={cliente.id} - {cliente.nombre}")
    return cliente


def crear_categoria(nombre: str) -> Categoria:
    """Crea una nueva categoría de productos."""
    categoria = Categoria.create(nombre=nombre.strip())
    print(f"[CREATE] Categoría creada: ID={categoria.id} - {categoria.nombre}")
    return categoria


def crear_producto(nombre: str, precio: Decimal, stock: int, categoria_id: int) -> Producto:
    """Registra un nuevo producto vinculado a una categoría existente."""
    categoria = Categoria.get_by_id(categoria_id)
    producto = Producto.create(
        nombre=nombre.strip(),
        precio=Decimal(str(precio)),
        stock=int(stock),
        categoria=categoria
    )
    print(f"[CREATE] Producto registrado: ID={producto.id} - {producto.nombre} | Categoría: {categoria.nombre}")
    return producto


def crear_venta_transaccional(cliente_id: int, items: list) -> Venta:
    """
    Crea una venta con múltiples detalles de forma atómica.
    `items` es una lista de tuplas: [(producto_o_id, cantidad), ...]
    Valida stock disponible, descuenta inventario y calcula total.
    """
    with db.atomic():
        cliente = Cliente.get_by_id(cliente_id)
        venta = Venta.create(cliente=cliente, total=Decimal("0.00"), fecha=datetime.now())
        total_acumulado = Decimal("0.00")

        for prod_item, cantidad in items:
            producto = prod_item if isinstance(prod_item, Producto) else Producto.get_by_id(prod_item)
            if producto.stock < cantidad:
                raise ValueError(f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, Solicitado: {cantidad}")

            # Descontar stock
            producto.stock -= cantidad
            producto.save()

            subtotal = Decimal(str(producto.precio)) * Decimal(str(cantidad))
            total_acumulado += subtotal

            DetalleVenta.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )

        venta.total = total_acumulado
        venta.save()

    print(f"[CREATE] Venta #{venta.id} generada para {cliente.nombre}. Total: ${venta.total:,.2f}")
    return venta


# -----------------------------------------------------------------------------
# 3. READ (CONSULTAS CON JOINS Y FORMATO PROFESIONAL)
# -----------------------------------------------------------------------------

def listar_clientes():
    """Consulta y lista todos los clientes registrados."""
    clientes = Cliente.select().order_by(Cliente.id.asc())
    print("\n" + "=" * 70)
    print(f"{'ID':<5} | {'NOMBRE COMPLETO':<30} | {'CORREO ELECTRÓNICO':<30}")
    print("=" * 70)
    for c in clientes:
        print(f"{c.id:<5} | {c.nombre:<30} | {c.correo:<30}")
    print(f"Total clientes: {len(clientes)}")


def listar_productos_con_categoria():
    """
    Consulta relacional (JOIN): Lista todos los productos junto al nombre
    de su categoría correspondiente.
    """
    consulta = (
        Producto
        .select(Producto, Categoria)
        .join(Categoria)
        .order_by(Categoria.nombre.asc(), Producto.nombre.asc())
    )

    print("\n" + "=" * 80)
    print(f"{'ID':<5} | {'PRODUCTO':<30} | {'CATEGORÍA':<20} | {'PRECIO':<10} | {'STOCK':<6}")
    print("=" * 80)
    for p in consulta:
        print(f"{p.id:<5} | {p.nombre:<30} | {p.categoria.nombre:<20} | ${p.precio:>8,.2f} | {p.stock:>5}")
    print("=" * 80)


def listar_ventas_con_detalle():
    """
    Consulta relacional avanzada (Múltiples JOINs):
    Une Venta -> Cliente y DetalleVenta -> Producto -> Categoria.
    Muestra la factura consolidada con cada ítem y subtotal.
    """
    ventas = Venta.select(Venta, Cliente).join(Cliente).order_by(Venta.id.desc())

    print("\n" + "=" * 90)
    print("REPORTE CONSOLIDADO DE VENTAS (JOIN: Venta -> Cliente -> Detalle -> Producto)")
    print("=" * 90)

    for v in ventas:
        fecha_str = v.fecha.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v.fecha, datetime) else str(v.fecha)
        print(f"\nFactura #{v.id} | Fecha: {fecha_str} | Cliente: {v.cliente.nombre} ({v.cliente.correo})")
        print(f"  {'-'*80}")
        print(f"  {'Artículo':<35} | {'Cant.':<6} | {'Precio Unit.':<14} | {'Subtotal':<14}")
        print(f"  {'-'*80}")

        detalles = (
            DetalleVenta
            .select(DetalleVenta, Producto, Categoria)
            .join(Producto)
            .join(Categoria)
            .where(DetalleVenta.venta == v)
        )

        for d in detalles:
            sub = d.cantidad * d.precio_unitario
            print(f"  {d.producto.nombre:<35} | {d.cantidad:>5} | ${d.precio_unitario:>12,.2f} | ${sub:>12,.2f}")

        print(f"  {'-'*80}")
        print(f"  {'TOTAL DE LA FACTURA:':<58} ${v.total:>12,.2f}")

    print("=" * 90)


def reporte_ventas_por_categoria():
    """
    Consulta analítica agregada con JOIN y GROUP BY:
    Calcula ingresos y volumen vendido por categoría.
    """
    consulta = (
        Categoria
        .select(
            Categoria.nombre,
            fn.COUNT(fn.DISTINCT(DetalleVenta.venta)).alias("total_ventas"),
            fn.SUM(DetalleVenta.cantidad).alias("unidades_vendidas"),
            fn.SUM(DetalleVenta.cantidad * DetalleVenta.precio_unitario).alias("total_ingresos")
        )
        .join(Producto, JOIN.INNER, on=(Categoria.id == Producto.categoria))
        .join(DetalleVenta, JOIN.INNER, on=(Producto.id == DetalleVenta.producto))
        .group_by(Categoria.id, Categoria.nombre)
        .order_by(fn.SUM(DetalleVenta.cantidad * DetalleVenta.precio_unitario).desc())
    )

    print("\n" + "=" * 80)
    print("ANÁLISIS DE VENTAS POR CATEGORÍA (GROUP BY + AGREGACIONES)")
    print("=" * 80)
    print(f"{'CATEGORÍA':<25} | {'Nº VENTAS':<10} | {'UNIDADES':<10} | {'INGRESOS':<15}")
    print("-" * 80)
    for fila in consulta:
        ingresos = fila.total_ingresos or Decimal("0.00")
        print(f"{fila.nombre:<25} | {fila.total_ventas:>9} | {fila.unidades_vendidas:>9} | ${ingresos:>13,.2f}")
    print("=" * 80)


# -----------------------------------------------------------------------------
# 4. UPDATE (OPERACIONES DE ACTUALIZACIÓN)
# -----------------------------------------------------------------------------

def actualizar_stock_producto(producto_id: int, nuevo_stock: int) -> bool:
    """Actualiza la existencia en bodega de un producto."""
    try:
        producto = Producto.get_by_id(producto_id)
        stock_anterior = producto.stock
        producto.stock = int(nuevo_stock)
        producto.save()
        print(f"[UPDATE] Stock de '{producto.nombre}' modificado: {stock_anterior} -> {producto.stock}")
        return True
    except Producto.DoesNotExist:
        print(f"[ERROR] No existe el producto con ID {producto_id}.")
        return False


def actualizar_precio_producto(producto_id: int, nuevo_precio: Decimal) -> bool:
    """Actualiza el precio de venta de un producto."""
    try:
        producto = Producto.get_by_id(producto_id)
        precio_anterior = producto.precio
        producto.precio = Decimal(str(nuevo_precio))
        producto.save()
        print(f"[UPDATE] Precio de '{producto.nombre}' actualizado: ${precio_anterior:,.2f} -> ${producto.precio:,.2f}")
        return True
    except Producto.DoesNotExist:
        print(f"[ERROR] No existe el producto con ID {producto_id}.")
        return False


def actualizar_cliente(cliente_id: int, nombre: str = None, telefono: str = None) -> bool:
    """Actualiza los datos personales o de contacto de un cliente."""
    try:
        cliente = Cliente.get_by_id(cliente_id)
        if nombre:
            cliente.nombre = nombre.strip()
        if telefono:
            cliente.telefono = telefono.strip()
        cliente.save()
        print(f"[UPDATE] Datos de cliente #{cliente.id} actualizados: {cliente.nombre} | Tel: {cliente.telefono}")
        return True
    except Cliente.DoesNotExist:
        print(f"[ERROR] No existe el cliente con ID {cliente_id}.")
        return False


# -----------------------------------------------------------------------------
# 5. DELETE (OPERACIONES DE ELIMINACIÓN SEGURA)
# -----------------------------------------------------------------------------

def eliminar_producto(producto_id: int) -> bool:
    """
    Elimina un producto del catálogo si no tiene detalles de venta asociados,
    garantizando la integridad referencial.
    """
    try:
        producto = Producto.get_by_id(producto_id)
        ventas_asociadas = DetalleVenta.select().where(DetalleVenta.producto == producto).count()
        if ventas_asociadas > 0:
            print(f"[AVISO] No se puede eliminar el producto '{producto.nombre}' porque está vinculado a {ventas_asociadas} venta(s).")
            return False

        nombre_prod = producto.nombre
        producto.delete_instance()
        print(f"[DELETE] Producto eliminado exitosamente: '{nombre_prod}' (ID {producto_id})")
        return True
    except Producto.DoesNotExist:
        print(f"[ERROR] No existe el producto con ID {producto_id}.")
        return False


def eliminar_cliente(cliente_id: int) -> bool:
    """Elimina un cliente si no tiene transacciones registradas."""
    try:
        cliente = Cliente.get_by_id(cliente_id)
        ventas_asociadas = Venta.select().where(Venta.cliente == cliente).count()
        if ventas_asociadas > 0:
            print(f"[AVISO] No se puede eliminar al cliente '{cliente.nombre}' porque registra {ventas_asociadas} factura(s).")
            return False

        nombre_cli = cliente.nombre
        cliente.delete_instance()
        print(f"[DELETE] Cliente eliminado exitosamente: '{nombre_cli}' (ID {cliente_id})")
        return True
    except Cliente.DoesNotExist:
        print(f"[ERROR] No existe el cliente con ID {cliente_id}.")
        return False


# -----------------------------------------------------------------------------
# 6. DEMOSTRACIÓN AUTOMÁTICA DEL FLUJO CRUD COMPLETO
# -----------------------------------------------------------------------------

def ejecutar_demostracion_completa():
    """
    Ejecuta en secuencia automática todas las operaciones del CRUD:
    - Verificación y semillero
    - CREATE (nuevo cliente, producto y venta transaccional)
    - READ (listados con JOIN)
    - UPDATE (precio y stock)
    - DELETE (eliminación controlada)
    """
    print("\n" + "#" * 80)
    print(" INICIANDO DEMOSTRACIÓN COMPLETA DE OPERACIONES CRUD - PEEWEE ORM")
    print(f" Motor Activo Seleccionado: '{MOTOR_ACTIVO}'")
    print("#" * 80)

    # 1. Asegurar tablas y semillero
    inicializar_base_datos()
    sembrar_datos_iniciales()

    # 2. CREATE
    print("\n>>> [PASO 1: CREATE] Creando nuevo cliente, categoría y producto...")
    ts_demo = datetime.now().strftime('%H%M%S')
    nuevo_cli = crear_cliente(f"Cliente Demo {ts_demo}", f"demo.{ts_demo}@testdemo.com", "+57 300 7654321")
    nueva_cat, _ = Categoria.get_or_create(nombre="Panadería y Repostería")
    nuevo_prod = crear_producto(f"Croissant Especial {ts_demo}", Decimal("3200.00"), 40, nueva_cat.id)

    print("\n>>> [PASO 1.1: CREATE VENTA TRANSACCIONAL]")
    prod_ref = Producto.select().first()
    items_nueva_venta = [(nuevo_prod, 3), (prod_ref, 1)]
    venta_demo = crear_venta_transaccional(nuevo_cli.id, items_nueva_venta)

    # 3. READ
    print("\n>>> [PASO 2: READ] Consultando catálogo con JOIN (Producto -> Categoria)...")
    listar_productos_con_categoria()

    print("\n>>> [PASO 2.1: READ] Consultando facturación con JOIN múltiple...")
    listar_ventas_con_detalle()

    print("\n>>> [PASO 2.2: READ AGREGADO] Analítica por categoría...")
    reporte_ventas_por_categoria()

    # 4. UPDATE
    print("\n>>> [PASO 3: UPDATE] Modificando valores en tiempo de ejecución...")
    actualizar_precio_producto(nuevo_prod.id, Decimal("3500.00"))
    actualizar_stock_producto(nuevo_prod.id, 80)
    actualizar_cliente(nuevo_cli.id, telefono="+57 319 9998888")

    # 5. DELETE
    print("\n>>> [PASO 4: DELETE] Comprobando reglas de integridad referencial...")
    # Intentar eliminar un producto con venta (debe ser bloqueado)
    eliminar_producto(nuevo_prod.id)

    # Crear y eliminar un producto sin ventas (debe eliminarse con éxito)
    prod_temporal = crear_producto(f"Producto Prueba {ts_demo}", Decimal("1000.00"), 10, nueva_cat.id)
    eliminar_producto(prod_temporal.id)

    print("\n" + "#" * 80)
    print(" DEMOSTRACIÓN DEL CRUD COMPLETADA EXITOSAMENTE")
    print("#" * 80)


# -----------------------------------------------------------------------------
# 7. MENÚ INTERACTIVO EN CONSOLA
# -----------------------------------------------------------------------------

def menu_interactivo():
    """Despliega un menú en consola para operar la aplicación manualmente."""
    inicializar_base_datos()
    sembrar_datos_iniciales()

    while True:
        print("\n" + "=" * 55)
        print("  SISTEMA DE GESTIÓN DE TIENDA - PEEWEE ORM")
        print(f"  Motor Activo: [{MOTOR_ACTIVO}]")
        print("=" * 55)
        print(" 1. Listar Clientes (READ)")
        print(" 2. Listar Productos y Categorías (READ con JOIN)")
        print(" 3. Listar Facturas y Detalles (READ con JOIN Múltiple)")
        print(" 4. Reporte Analítico de Ventas por Categoría")
        print(" 5. Registrar Nuevo Cliente (CREATE)")
        print(" 6. Registrar Nuevo Producto (CREATE)")
        print(" 7. Actualizar Precio o Stock de Producto (UPDATE)")
        print(" 8. Actualizar Teléfono de Cliente (UPDATE)")
        print(" 9. Eliminar Producto (DELETE)")
        print("10. Ejecutar Demostración Automática de todo el CRUD")
        print(" 0. Salir")
        print("=" * 55)

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            listar_clientes()
        elif opcion == "2":
            listar_productos_con_categoria()
        elif opcion == "3":
            listar_ventas_con_detalle()
        elif opcion == "4":
            reporte_ventas_por_categoria()
        elif opcion == "5":
            nombre = input("Nombre completo: ").strip()
            correo = input("Correo electrónico: ").strip()
            tel = input("Teléfono: ").strip()
            if nombre and correo:
                try:
                    crear_cliente(nombre, correo, tel)
                except Exception as e:
                    print(f"[ERROR] No se pudo crear el cliente: {e}")
            else:
                print("[ERROR] Nombre y correo son obligatorios.")
        elif opcion == "6":
            nombre = input("Nombre del producto: ").strip()
            precio_in = input("Precio unitario: ").strip()
            stock_in = input("Stock inicial: ").strip()
            cat_id = input("ID de Categoría: ").strip()
            try:
                crear_producto(nombre, Decimal(precio_in), int(stock_in), int(cat_id))
            except Exception as e:
                print(f"[ERROR] No se pudo crear el producto: {e}")
        elif opcion == "7":
            prod_id = input("ID del producto a actualizar: ").strip()
            tipo = input("¿Qué desea actualizar? (1: Precio, 2: Stock): ").strip()
            if tipo == "1":
                nuevo_val = input("Nuevo precio: ").strip()
                actualizar_precio_producto(int(prod_id), Decimal(nuevo_val))
            elif tipo == "2":
                nuevo_val = input("Nuevo stock: ").strip()
                actualizar_stock_producto(int(prod_id), int(nuevo_val))
        elif opcion == "8":
            cli_id = input("ID del cliente: ").strip()
            nuevo_tel = input("Nuevo teléfono: ").strip()
            actualizar_cliente(int(cli_id), telefono=nuevo_tel)
        elif opcion == "9":
            prod_id = input("ID del producto a eliminar: ").strip()
            eliminar_producto(int(prod_id))
        elif opcion == "10":
            ejecutar_demostracion_completa()
        elif opcion == "0":
            print("\nCerrando conexión y saliendo del sistema. ¡Hasta pronto!\n")
            if not db.is_closed():
                db.close()
            break
        else:
            print("[AVISO] Opción inválida. Intente de nuevo.")


# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    # Si se pasa argumento '--demo' o la consola no es interactiva, se corre la demo completa
    if "--demo" in sys.argv or not sys.stdin.isatty():
        ejecutar_demostracion_completa()
    else:
        try:
            menu_interactivo()
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada por el usuario.")
            if not db.is_closed():
                db.close()
