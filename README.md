# Gestor de reservas PadelBeche

Aplicación de escritorio para gestionar clientes, canchas y reservas de un
complejo deportivo. Está desarrollada en Python con Tkinter y utiliza MySQL
para guardar los datos.

## Alcance

La aplicación permite gestionar clientes, canchas y reservas desde una
interfaz gráfica. Los cambios se guardan en MySQL y se mantienen al cerrar el
programa.

La configuración de demostración utiliza una base local con datos ficticios.
No se accede a datos reales de ningún tipo. No conectes esta versión a una base
de datos de producción ni cargues información real.

## Funcionalidades

- Inicio de sesión con los roles `Supervisor` y `Empleado`.
- Pantalla de inicio con las reservas del día actual.
- Gestión de clientes: el Empleado puede registrarlos y consultarlos; el
  Supervisor también puede modificarlos y eliminarlos. Al eliminar un cliente,
  también se eliminan sus reservas asociadas.
- Gestión de canchas: el Supervisor puede registrarlas y modificarlas; el
  Empleado puede consultarlas.
- Gestión de reservas: el Empleado puede registrarlas, consultarlas y
  modificarlas; el Supervisor también puede eliminarlas.
- Reservas vinculadas a un cliente registrado y a una cancha existente.
- Selección de canchas activas al registrar reservas.
- Estados de reserva: `Pendiente`, `Confirmada` y `Cancelada`.
- Plazo de pago de 15 minutos para reservas pendientes y aviso de vencimiento
  mientras la pantalla de reservas está abierta. El estado no cambia
  automáticamente; el usuario debe actualizarlo.
- Consultas con filtros por rango de fechas, cliente y cancha.
- Creación de respaldos de la base de datos.
- Validaciones de campos, formatos, datos de clientes, capacidad, precio,
  fechas y horarios.

Al registrar una reserva, se impide superponer horarios de reservas pendientes
o confirmadas para la misma cancha y fecha. Las reservas canceladas no ocupan
el horario. El control de superposición al modificar una reserva es una
limitación conocida.

## Credenciales de demostración

Estas credenciales permiten probar los roles de la aplicación. Se utilizan
únicamente con datos ficticios; no se accede a datos reales de ningún tipo.

| Rol | Contraseña |
|---|---|
| Supervisor | `Admin2026` |
| Empleado | `1234Hola` |

No reutilices estas contraseñas en otros sistemas.

## Tecnologías

- Python 3
- Tkinter y ttk
- MySQL 8
- MySQL Connector/Python
- Git

El conector MySQL se instala desde `requirements.txt`. La aplicación obtiene
la configuración de conexión de las variables de entorno; el archivo `.env`
no se carga automáticamente.

## Estructura del proyecto

```text
.
|-- BASE_DE_DATOS/
|   |-- backup_database.py # Creación de respaldos
|   |-- database.py        # Conexión a MySQL
|   `-- schema_mysql.sql   # Tablas y datos de ejemplo
|-- TKINTER/
|   |-- clientes.py        # Interfaz de clientes
|   |-- modelo_clientes.py # Acceso a datos de clientes
|   |-- canchas.py         # Interfaz de canchas
|   |-- modelo_canchas.py  # Acceso a datos de canchas
|   |-- reservas.py        # Interfaz de reservas
|   |-- modelo_reservas.py # Acceso a datos de reservas
|   |-- consultas.py       # Interfaz de consultas
|   `-- modelo_consultas.py # Acceso a datos de consultas
|-- docs/
|   `-- modelo-datos.md    # Documentación del modelo de datos
|-- requirements.txt
|-- main.py            # Ventana principal y navegación
|-- sesion.py
`-- README.md
```

## Requisitos

- Python 3 instalado.
- MySQL Server 8.0 o superior instalado y en ejecución.
- Tkinter disponible junto con la instalación de Python.
- Dependencias instaladas con `python -m pip install -r requirements.txt`.

En Windows, la instalación habitual de Python incluye Tkinter. Cada integrante
debe instalar MySQL localmente y crear su propia copia de la base usando el
esquema compartido del repositorio.

## Preparar MySQL local

1. Instalar e iniciar MySQL Server 8.0 o superior. MySQL Workbench es opcional.
2. Ejecutar `BASE_DE_DATOS/schema_mysql.sql` desde MySQL Workbench o, desde la
   raíz del repositorio, con el cliente `mysql`:

```bash
mysql -u root -p < BASE_DE_DATOS/schema_mysql.sql
```

El script crea la base `padelbeche`, sus tablas y registros ficticios de
ejemplo. El usuario de MySQL debe tener permisos para crear la base.

3. Instalar el conector Python desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
```

4. Configurar las variables de conexión en la terminal. En PowerShell:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "tu_contraseña_local"
$env:DB_NAME = "padelbeche"
```

Usa credenciales locales y no subas contraseñas de MySQL al repositorio. Estas
variables duran mientras siga abierta esa terminal.

5. Comprobar la conexión desde la raíz del repositorio:

```bash
python -c "from BASE_DE_DATOS.database import obtener_conexion; conexion = obtener_conexion(); print('Conexión a MySQL correcta'); conexion.close()"
```

## Ejecución

Desde una terminal ubicada en la carpeta del proyecto, ejecutar:

```bash
cd TKINTER
python main.py
```

La ventana principal permite acceder a **Reservas**, **Clientes**, **Canchas**
y **Consultas**.

## Limitaciones conocidas

- El control de superposición de horarios se ejecuta al registrar una reserva,
  pero todavía debe incorporarse al modificarla.
- Los roles restringen acciones desde la interfaz; no son permisos de usuario
  configurados directamente en MySQL.

## Documentación adicional

La descripción de las tablas, sus relaciones y las reglas principales del
modelo se encuentra en [docs/modelo-datos.md](docs/modelo-datos.md).
