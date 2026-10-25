
-- Configuración de usuario y rol para PadelBeche
-- Ejecutar como administrador en MySQL Workbench
-- Requiere que exista la base de datos padelbeche

-- Crear rol de la aplicación
CREATE ROLE IF NOT EXISTS 'rol_padelbeche';

-- Asignar permisos sobre la base de datos
GRANT SELECT, INSERT, UPDATE, DELETE
ON padelbeche.*
TO 'rol_padelbeche';

-- Permiso para exportar eventos mediante mysqldump
GRANT EVENT
ON padelbeche.*
TO 'rol_padelbeche';

-- Crear usuario de aplicación
CREATE USER IF NOT EXISTS 'padelbeche_app'@'localhost'
IDENTIFIED BY 'SoftTech2026';


-- Asignar rol al usuario
GRANT 'rol_padelbeche'
TO 'padelbeche_app'@'localhost';

-- Activar rol automáticamente al conectarse
SET DEFAULT ROLE 'rol_padelbeche'
TO 'padelbeche_app'@'localhost';
