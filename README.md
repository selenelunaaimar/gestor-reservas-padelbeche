# Gestor de reservas PadelBeche

Aplicación de escritorio para gestionar clientes, canchas y reservas de un
complejo deportivo. El proyecto está desarrollado en Python utilizando la
biblioteca gráfica Tkinter.

## Alcance de esta etapa

El objetivo de esta primera etapa es desarrollar y probar la interfaz gráfica
del sistema. Actualmente se encuentran implementadas las pantallas, la
navegación entre secciones, el funcionamiento de los botones y las principales
validaciones de datos.

Se definió el esquema de la base de datos en MySQL. La base todavía no está
conectada a la interfaz gráfica.

Por el momento, la aplicación utiliza listas temporales en memoria para
mostrar y modificar los datos. Por ese motivo, los cambios realizados desde
la interfaz se pierden al cerrar el programa.

## Funcionalidades implementadas

- Pantalla de inicio con las reservas correspondientes al día actual.
- Alta, modificación, búsqueda y eliminación de clientes.
- Alta, modificación y búsqueda de canchas.
- Alta, modificación y búsqueda de reservas.
- Validación de campos obligatorios y formatos.
- Validación de DNI, teléfono, email, capacidad y precio.
- Validación de fechas y horarios de las reservas.
- Control de superposición de reservas para una misma cancha.
- Estados para reservas: `Confirmada`, `Pendiente` y `Cancelada`.
- Filtros de consultas por fecha, cliente y cancha.
- Navegación mediante botones entre las distintas pantallas.

## Tecnologías

- Python 3
- Tkinter y ttk
- MySQL 8 para la base de datos
- MySQL Connector/Python para la conexión desde Python
- Git para el control de versiones

La interfaz gráfica todavía trabaja con datos temporales en memoria. El
conector MySQL se instala desde `requirements.txt`.

## Estructura del proyecto

```text
.
|-- BASE_DE_DATOS/
|   |-- database.py       # Conexión a MySQL
|   `-- schema_mysql.sql  # Tablas y datos iniciales
|-- TKINTER/
|   |-- main.py           # Ventana principal y navegación
|   |-- clientes.py       # Pantalla y operaciones de clientes
|   |-- canchas.py        # Pantalla y operaciones de canchas
|   |-- reservas.py       # Pantalla y operaciones de reservas
|   `-- consultas.py      # Pantalla de consultas y filtros
|-- docs/
|   `-- modelo-datos.md   # Documentación del modelo de datos
`-- README.md
```

## Requisitos

- Python 3 instalado.
- MySQL Server 8.0 o superior instalado y en ejecución.
- Tkinter disponible junto con la instalación de Python.
- Dependencias de Python instaladas con `python -m pip install -r requirements.txt`.

En Windows, la instalación habitual de Python incluye Tkinter. Cada integrante
debe instalar MySQL localmente y crear su propia copia de la base usando el
esquema compartido del repositorio.

## Ejecución de la interfaz

Desde una terminal ubicada en la carpeta del proyecto, ejecutar:

```bash
cd TKINTER
python main.py
```

La ventana principal permite acceder a las secciones **Reservas**,
**Clientes**, **Canchas** y **Consultas**.

## Preparar MySQL local

1. Instalar e iniciar MySQL Server 8.0 o superior. MySQL Workbench es opcional,
	pero permite ejecutar el esquema gráficamente.
2. Ejecutar `BASE_DE_DATOS/schema_mysql.sql` desde MySQL Workbench (abrir el
	archivo y ejecutar el script) o, desde CMD o Bash, con el cliente `mysql`
	desde la raíz del repositorio:

```bash
mysql -u root -p < BASE_DE_DATOS/schema_mysql.sql
```

El script crea la base `padelbeche`, sus tablas y registros de ejemplo. Si usan
un usuario distinto de `root`, debe tener permisos para crear la base.

3. Instalar el conector Python desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
```

4. Configurar las variables de conexión en la terminal. En PowerShell, por
	ejemplo:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "root"
$env:DB_PASSWORD = "tu_contraseña_local"
$env:DB_NAME = "padelbeche"
```

Cada integrante debe usar sus propias credenciales locales. No subir
contraseñas a GitHub. Estas variables duran mientras siga abierta esa terminal.

5. Comprobar la conexión desde la raíz del repositorio:

```bash
python -c "from BASE_DE_DATOS.database import obtener_conexion; conexion = obtener_conexion(); print('Conexión a MySQL correcta'); conexion.close()"
```

La interfaz de Tkinter todavía no consume esta conexión; actualmente conserva
los datos en listas en memoria.

## Próximas etapas

- Conectar la interfaz gráfica con MySQL.
- Reemplazar las listas temporales por operaciones de lectura y escritura en
	la base de datos.
- Mantener los registros al cerrar y volver a abrir la aplicación.
- Aplicar desde MySQL las relaciones entre clientes, canchas y reservas.
- Completar las validaciones de integridad y persistencia.

## Documentación adicional

La descripción de las tablas, sus relaciones y las reglas principales del
modelo se encuentra en [docs/modelo-datos.md](docs/modelo-datos.md).
