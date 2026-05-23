USE ventas_db;

INSERT INTO ventas
(usuario_id, edad, ciudad, producto, categoria, precio, fecha, hora, metodo_pago)
VALUES
(1, 34, 'Santiago', 'Laptop', 'Electronica', 899.99, '2026-05-19', '10:15:00', 'Tarjeta'),
(2, 22, 'Valparaiso', 'Silla Gamer', 'Hogar', 199.99, '2026-05-19', '11:00:00', 'Debito'),
(3, 45, 'Concepcion', 'Cafetera', 'Hogar', 79.99, '2026-05-19', '12:30:00', 'Efectivo'),
(4, 30, 'Antofagasta', 'Celular', 'Electronica', 499.99, '2026-05-20', '09:45:00', 'Tarjeta'),
(5, 27, 'Santiago', 'Libro Python', 'Educacion', 29.99, '2026-05-20', '14:20:00', 'Debito'),
(6, 19, 'Valparaiso', 'Audifonos', 'Electronica', 39.99, '2026-05-20', '16:10:00', 'Tarjeta'),
(7, 38, 'Concepcion', 'Escritorio', 'Hogar', 149.99, '2026-05-21', '13:00:00', 'Tarjeta'),
(8, 26, 'Santiago', 'Mouse Gamer', 'Electronica', 49.99, '2026-05-21', '18:30:00', 'Tarjeta'),
(9, 33, 'Antofagasta', 'Sartén', 'Hogar', 24.99, '2026-05-21', '20:15:00', 'Efectivo'),
(10, 41, 'Valparaiso', 'Curso SQL', 'Educacion', 99.99, '2026-05-21', '21:00:00', 'Debito');
