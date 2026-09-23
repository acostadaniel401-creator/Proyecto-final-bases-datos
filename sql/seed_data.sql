-- =============================================================================
-- PROYECTO FINAL: GESTIÓN MULTI-MOTOR DE BASES DE DATOS CON PYTHON Y PEEWEE ORM
-- SCRIPT DML: POBLADO DE DATOS DE PRUEBA (SEED DATA) Y CONSULTA GUI CON JOIN
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. POBLADO DE TABLA: cliente (Mínimo 5 registros)
-- -----------------------------------------------------------------------------
INSERT INTO cliente (nombre, correo, telefono) VALUES
('Carlos Andres Gomez', 'carlos.gomez@email.com', '+57 310 1234567'),
('Maria Fernanda Rodriguez', 'maria.rodriguez@email.com', '+57 311 9876543'),
('Juan David Perez', 'juan.perez@email.com', '+57 312 4567890'),
('Laura Marcela Martinez', 'laura.martinez@email.com', '+57 315 3216549'),
('Andres Felipe Lopez', 'andres.lopez@email.com', '+57 320 6549871'),
('Valentina Morales Castro', 'valentina.morales@email.com', '+57 314 7891230');

-- -----------------------------------------------------------------------------
-- 2. POBLADO DE TABLA: categoria (Mínimo 5 registros)
-- -----------------------------------------------------------------------------
INSERT INTO categoria (nombre) VALUES
('Bebidas y Refrescos'),
('Lácteos y Derivados'),
('Granos y Abarrotes'),
('Snacks y Confitería'),
('Aseo y Cuidado Personal');

-- -----------------------------------------------------------------------------
-- 3. POBLADO DE TABLA: producto (Mínimo 5 registros)
-- -----------------------------------------------------------------------------
INSERT INTO producto (nombre, precio, stock, categoria_id) VALUES
('Gaseosa Cola 1.5L', 5500.00, 45, 1),
('Jugo Natural Naranja 1L', 4200.00, 30, 1),
('Leche Entera Ultra Pasteurizada 1L', 3800.00, 60, 2),
('Queso Campesino Bloque 500g', 12500.00, 20, 2),
('Arroz Blanco Premium 1kg', 4600.00, 100, 3),
('Frijol Rojo Calima 500g', 5800.00, 40, 3),
('Papas Fritas Onduladas 115g', 3500.00, 50, 4),
('Galletas de Chocolate 180g', 2900.00, 75, 4),
('Jabón de Baño Antibacterial 3x110g', 8900.00, 35, 5),
('Detergente en Polvo Floral 1kg', 9400.00, 25, 5);

-- -----------------------------------------------------------------------------
-- 4. POBLADO DE TABLA: venta (Mínimo 5 registros)
-- -----------------------------------------------------------------------------
INSERT INTO venta (fecha, cliente_id, total) VALUES
('2026-03-01 09:30:00', 1, 19300.00),
('2026-03-01 11:15:00', 2, 28800.00),
('2026-03-02 14:45:00', 3, 14700.00),
('2026-03-02 17:20:00', 4, 30800.00),
('2026-03-03 10:05:00', 5, 23700.00),
('2026-03-03 16:50:00', 1, 16900.00);

-- -----------------------------------------------------------------------------
-- 5. POBLADO DE TABLA: detalle_venta (Mínimo 5 registros)
-- -----------------------------------------------------------------------------
-- Venta 1 (Carlos Gomez): Gaseosa (1 * 5500) + Arroz (3 * 4600) = 19300
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 1, 5500.00),
(1, 5, 3, 4600.00);

-- Venta 2 (Maria Rodriguez): Leche (2 * 3800) + Queso (1 * 12500) + Detergente (1 * 9400) = 29500 -> Ajuste:
-- Leche (1 * 3800) + Queso (2 * 12500) = 28800
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES
(2, 3, 1, 3800.00),
(2, 4, 2, 12500.00);

-- Venta 3 (Juan David Perez): Papas Fritas (2 * 3500) + Galletas (1 * 2900) + Gaseosa (1 * 5500) = wait (7000+2900+5500 = 15400)
-- 2 * 3500 (7000) + 1 * 5800 (Frijol) + 1 * 1900 -> Let's make exact:
-- Jugo (1 * 4200) + Galletas (2 * 2900 = 5800) + Frijol (1 * 4700) = 14700
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES
(3, 2, 1, 4200.00),
(3, 8, 2, 2900.00),
(3, 6, 1, 4700.00);

-- Venta 4 (Laura Martinez): Queso (1 * 12500) + Jabon (1 * 8900) + Detergente (1 * 9400) = 30800
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES
(4, 4, 1, 12500.00),
(4, 9, 1, 8900.00),
(4, 10, 1, 9400.00);

-- Venta 5 (Andres Felipe Lopez): Arroz (2 * 4600 = 9200) + Frijol (2 * 5800 = 11600) + Galletas (1 * 2900) = 23700
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES
(5, 5, 2, 4600.00),
(5, 6, 2, 5800.00),
(5, 8, 1, 2900.00);

-- Venta 6 (Carlos Gomez): Gaseosa (2 * 5500 = 11000) + Frijol (1 * 5900 = 5900) = 16900
INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio_unitario) VALUES
(6, 1, 2, 5500.00),
(6, 6, 1, 5900.00);

-- =============================================================================
-- CONSULTA GUI CON JOIN (Comprobación y Reporte Consolidado para Clientes Gráficos)
-- Compatible con SQLite, MySQL y PostgreSQL
-- =============================================================================
-- Esta consulta une las 5 tablas relacionadas del modelo de negocio,
-- permitiendo visualizar desde la herramienta gráfica (DBeaver, HeidiSQL o pgAdmin)
-- el detalle de cada factura, el cliente, la categoría y el producto con subtotales.

SELECT 
    v.id AS nro_factura,
    v.fecha AS fecha_venta,
    c.nombre AS cliente,
    c.correo AS email_cliente,
    cat.nombre AS categoria,
    p.nombre AS producto,
    dv.cantidad,
    dv.precio_unitario,
    (dv.cantidad * dv.precio_unitario) AS subtotal_item,
    v.total AS total_factura
FROM venta v
INNER JOIN cliente c 
    ON v.cliente_id = c.id
INNER JOIN detalle_venta dv 
    ON v.id = dv.venta_id
INNER JOIN producto p 
    ON dv.producto_id = p.id
INNER JOIN categoria cat 
    ON p.categoria_id = cat.id
ORDER BY 
    v.id ASC, 
    dv.id ASC;

-- =============================================================================
-- CONSULTA GUI ADICIONAL: Resumen de Ventas por Categoría y Total Recaudado
-- =============================================================================
SELECT 
    cat.nombre AS categoria,
    COUNT(DISTINCT v.id) AS total_transacciones,
    SUM(dv.cantidad) AS unidades_vendidas,
    SUM(dv.cantidad * dv.precio_unitario) AS total_recaudado
FROM categoria cat
INNER JOIN producto p 
    ON cat.id = p.categoria_id
INNER JOIN detalle_venta dv 
    ON p.id = dv.producto_id
INNER JOIN venta v 
    ON dv.venta_id = v.id
GROUP BY 
    cat.id, 
    cat.nombre
ORDER BY 
    total_recaudado DESC;
