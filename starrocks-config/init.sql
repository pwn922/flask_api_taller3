CREATE DATABASE IF NOT EXISTS ventas_db;

CREATE USER IF NOT EXISTS 'starrocks'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'starrocks'@'%';

DROP TABLE IF EXISTS ventas_db.ventas;

CREATE TABLE ventas_db.ventas (
    usuario_id INT,
    edad TINYINT,
    ciudad VARCHAR(100),
    producto VARCHAR(200),
    categoria VARCHAR(200),
    precio FLOAT,
    fecha DATE,
    hora VARCHAR(20),
    metodo_pago VARCHAR(100)
)
ENGINE=OLAP
DUPLICATE KEY(usuario_id)
DISTRIBUTED BY HASH(usuario_id) BUCKETS 10
PROPERTIES (
    "replication_num" = "1"
);
