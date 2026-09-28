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

    -- La hora de finalización debe ser posterior
    -- a la hora de inicio.
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
('35222333', 'Maria Gomez', '3415552222', 'maria@gmail.com'),
('38444555', 'Carlos Lopez', '3415553333', 'carlos@gmail.com');

-- Carga inicial de datos de prueba: Canchas
INSERT INTO canchas (tipo_deporte, capacidad, precio_hora, estado) VALUES
('Padel', 4, 10000, 'Activa'),
('Padel', 4, 10000, 'Activa'),
('Futbol', 10, 25000, 'Activa'),
('Futbol', 10, 25000, 'Inactiva');

-- Carga inicial de datos de prueba: Reservas
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
