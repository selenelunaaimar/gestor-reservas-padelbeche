CREATE TABLE clientes (
    dni INTEGER PRIMARY KEY NOT NULL,
    nombre_apellido VARCHAR(100) NOT NULL,
    telefono INTEGER NOT NULL,
    email VARCHAR(100) NOT NULL
);
CREATE TABLE canchas (
    id_cancha INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_deporte VARCHAR(20) NOT NULL,
    capacidad INTEGER NOT NULL,
    precio_hora REAL NOT NULL,
    estado VARCHAR(20) NOT NULL CHECK
);
CREATE TABLE reservas (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    dni_cliente INTEGER NOT NULL,
    id_cancha INTEGER NOT NULL,
    fecha DATETIME NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado_reserva VARCHAR(20) NOT NULL CHECK,

    FOREIGN KEY (dni_cliente) REFERENCES clientes(dni),
    FOREIGN KEY (id_cancha) REFERENCES canchas(id_cancha)
);
INSERT INTO clientes (dni, nombre_apellido, telefono, email) VALUES
('30111222','Juan Perez', '3415551111', 'juan@gmail.com'),
('35222333', 'Maria Gomez', '3415552222', 'maria@gmail.com'),
('38444555', 'Carlos Lopez', '3415553333', 'carlos@gmail.com');

INSERT INTO canchas (tipo_deporte, capacidad, precio_hora, estado) VALUES
('Padel', 4, 10000, 'Activa'),
('Padel', 4, 10000, 'Activa'),
('Futbol', 10, 25000, 'Activa'),
('Futbol', 10, 25000, 'Inactiva');

INSERT INTO reservas (
    dni_cliente,
    id_cancha,
    fecha,
    hora_inicio,
    hora_fin,
    estado_reserva
) VALUES
('30111222', 1, '2026-09-18', '18:00', '19:00', 'Confirmada'),
('35222333', 2, '2026-09-18', '19:00', '20:00', 'Pendiente'),
('38444555', 1, '2026-09-19', '18:00', '19:00', 'Confirmada');