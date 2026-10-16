CREATE DATABASE IF NOT EXISTS padelbeche
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE padelbeche;


CREATE TABLE clientes (
    dni INT PRIMARY KEY,
    nombre_apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL
) ENGINE = InnoDB;


CREATE TABLE canchas (
    id_cancha INT AUTO_INCREMENT PRIMARY KEY,
    tipo_deporte VARCHAR(20) NOT NULL,
    capacidad INT NOT NULL,
    precio_hora DECIMAL(10,2) NOT NULL,
    estado ENUM('Activa', 'Inactiva') NOT NULL DEFAULT 'Activa',

    CONSTRAINT chk_canchas_capacidad
        CHECK (capacidad > 0),

    CONSTRAINT chk_canchas_precio
        CHECK (precio_hora > 0)
) ENGINE = InnoDB;


CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    dni_cliente INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,

    estado_reserva ENUM(
        'Confirmada',
        'Pendiente',
        'Cancelada'
    ) NOT NULL,

    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    vence_pago DATETIME NULL,

    CONSTRAINT fk_reservas_cliente
        FOREIGN KEY (dni_cliente)
        REFERENCES clientes(dni),

    CONSTRAINT fk_reservas_cancha
        FOREIGN KEY (id_cancha)
        REFERENCES canchas(id_cancha),

    -- La hora de finalización debe ser posterior a la hora de inicio.
    CONSTRAINT chk_reservas_horario
        CHECK (hora_fin > hora_inicio),

    -- Una reserva pendiente debe tener vencimiento.
    CONSTRAINT chk_reservas_vencimiento
        CHECK (
            estado_reserva <> 'Pendiente'
            OR vence_pago IS NOT NULL
        ),

    INDEX idx_reservas_cancha_fecha
        (id_cancha, fecha),

    INDEX idx_reservas_estado
        (estado_reserva)
) ENGINE = InnoDB;


DELIMITER //

CREATE TRIGGER validar_cancha_activa
BEFORE INSERT ON reservas
FOR EACH ROW
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM canchas
        WHERE id_cancha = NEW.id_cancha
          AND estado = 'Activa'
    ) THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'No se puede reservar una cancha inactiva.';

    END IF;

END//

DELIMITER ;


DELIMITER //

CREATE TRIGGER validar_horario_reserva
BEFORE INSERT ON reservas
FOR EACH ROW
BEGIN

    IF EXISTS (
        SELECT 1
        FROM reservas
        WHERE id_cancha = NEW.id_cancha
          AND fecha = NEW.fecha

          -- Solo estas reservas bloquean el horario.
          AND estado_reserva IN ('Confirmada', 'Pendiente')

          -- Verifica que los horarios se superpongan.
          AND NEW.hora_inicio < hora_fin
          AND NEW.hora_fin > hora_inicio
    ) THEN

        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'El horario seleccionado ya está ocupado.';

    END IF;

END//

DELIMITER ;

-- Carga inicial de datos de prueba: Clientes
INSERT INTO clientes (dni, nombre_apellido, telefono, email) VALUES
('30111222', 'Juan Perez', '3415551111', 'juan@gmail.com'),
('35222333', 'Maria Gimenez', '3415552222', 'maria@gmail.com'),
('38444555', 'Carlos Lopez', '3415553333', 'carlos@gmail.com'),
('40123456', 'Lucía Martínez', '3515554444', 'lucia@gmail.com'),
('41234567', 'Esteban Quito', '3515555555', 'esteban@gmail.com'),
('42345678', 'Sofía Benítez', '3515556666', 'sofia@gmail.com'),
('43456789', 'Martín Gómez', '3515557777', 'martin@gmail.com'),
('44567890', 'Carmen Ríos', '3515558888', 'carmen@gmail.com'),
('45678901', 'Federico Díaz', '3515559999', 'federico@gmail.com'),
('46789012', 'Valentina Sosa', '3515550000', 'valentina@gmail.com'),
('42440440', 'Cecilia Alfonso', '3510009990', 'cecilia@gmail.com');

-- Carga inicial de datos de prueba: Canchas
INSERT INTO canchas (tipo_deporte, capacidad, precio_hora, estado) VALUES
('Padel', 4, 10000, 'Activa'),
('Padel', 4, 10000, 'Activa'),
('Futbol', 10, 25000, 'Activa'),
('Futbol', 10, 25000, 'Inactiva'),
('Padel', 4, 12000, 'Activa'),
('Padel', 4, 12000, 'Activa'),
('Padel', 4, 10000, 'Activa'),
('Padel', 4, 12000, 'Inactiva');

-- Carga inicial de datos de prueba: Reservas
INSERT INTO reservas (
    dni_cliente,
    id_cancha,
    fecha,
    hora_inicio,
    hora_fin,
    estado_reserva,
    vence_pago
) VALUES
('30111222', 1, '2026-10-16', '18:00', '19:00', 'Confirmada', NULL),
('35222333', 2, '2026-10-16', '19:00', '20:00', 'Pendiente', '2026-10-16 18:30:00'),
('38444555', 1, '2026-10-17', '18:00', '19:00', 'Confirmada', NULL),
('40123456', 3, '2026-10-17', '14:00', '15:30', 'Confirmada', NULL),
('41234567', 1, '2026-10-18', '16:00', '17:00', 'Pendiente', '2026-10-18 15:00:00'),
('42345678', 2, '2026-10-18', '18:00', '19:00', 'Confirmada', NULL),
('43456789', 5, '2026-10-19', '20:00', '21:30', 'Confirmada', NULL),
('44567890', 2, '2026-10-19', '17:00', '18:00', 'Cancelada', NULL),
('45678901', 1, '2026-10-20', '09:00', '10:00', 'Confirmada', NULL),
('46789012', 3, '2026-10-20', '11:00', '12:30', 'Pendiente', '2026-10-20 10:00:00'),
('44567890', 2, '2026-10-21', '17:00', '18:00', 'Cancelada', NULL),
('45678901', 1, '2026-10-21', '09:00', '10:00', 'Confirmada', NULL),
('46789012', 3, '2026-10-22', '11:00', '12:30', 'Confirmada', NULL),
('30111222', 5, '2026-10-22', '13:00', '14:00', 'Pendiente', '2026-10-22 12:00:00'),
('35222333', 6, '2026-10-23', '15:00', '16:00', 'Confirmada', NULL),
('38444555', 7, '2026-10-23', '17:00', '18:00', 'Confirmada', NULL),
('40123456', 1, '2026-10-24', '19:00', '20:00', 'Pendiente', '2026-10-24 18:00:00'),
('41234567', 2, '2026-10-24', '21:00', '22:00', 'Cancelada', NULL),
('42345678', 5, '2026-10-25', '19:00', '20:00', 'Confirmada', NULL),
('43456789', 3, '2026-10-25', '20:30', '21:30', 'Cancelada', NULL),
('44567890', 5, '2026-10-26', '14:00', '15:00', 'Confirmada', NULL),
('45678901', 6, '2026-10-26', '17:00', '18:00', 'Confirmada', NULL),
('46789012', 7, '2026-10-27', '18:00', '19:00', 'Confirmada', NULL),
('30111222', 1, '2026-10-27', '20:00', '21:00', 'Pendiente', '2026-10-27 19:00:00'),
('35222333', 2, '2026-10-28', '11:00', '12:00', 'Confirmada', NULL),
('38444555', 3, '2026-10-28', '15:00', '16:00', 'Cancelada', NULL),
('40123456', 5, '2026-10-29', '16:00', '17:00', 'Confirmada', NULL),
('41234567', 6, '2026-10-29', '19:00', '20:00', 'Pendiente', '2026-10-29 18:00:00'),
('42345678', 7, '2026-10-30', '10:00', '11:00', 'Confirmada', NULL),
('43456789', 1, '2026-10-30', '13:00', '14:00', 'Cancelada', NULL),
('42440440', 1, '2026-10-31', '10:00', '11:00', 'Confirmada', NULL),
('42440440', 3, '2026-11-01', '15:00', '16:00', 'Cancelada', NULL);
