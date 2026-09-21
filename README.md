# Gestor de reservas PadelBeche

Aplicación de escritorio para gestionar clientes, canchas y reservas de un
complejo deportivo. El proyecto está desarrollado en Python utilizando la
biblioteca gráfica Tkinter.

## Alcance de esta etapa

El objetivo de esta primera etapa es desarrollar y probar la interfaz gráfica
del sistema. Actualmente se encuentran implementadas las pantallas, la
navegación entre secciones, el funcionamiento de los botones y las principales
validaciones de datos.

También se comenzó a diseñar la base de datos SQLite mediante un esquema SQL y
un script de creación. La base de datos todavía no está conectada a la
interfaz gráfica.

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
- SQLite, para el diseño inicial de la base de datos
- Git para el control de versiones

No se requieren paquetes externos para ejecutar la interfaz.

## Estructura del proyecto

```text
.
|-- BASE_DE_DATOS/
|   |-- database.py       # Crea la base SQLite a partir del esquema
|   `-- schema.sql        # Tablas y datos iniciales
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
- Tkinter disponible junto con la instalación de Python.

En Windows, la instalación habitual de Python incluye Tkinter. No se necesita
instalar una base de datos ni dependencias adicionales para probar la
interfaz.

## Ejecución de la interfaz

Desde una terminal ubicada en la carpeta del proyecto, ejecutar:

```bash
cd TKINTER
python main.py
```

La ventana principal permite acceder a las secciones **Reservas**,
**Clientes**, **Canchas** y **Consultas**.

## Creación de la base de datos de prueba

La base inicial puede generarse de forma independiente ejecutando:

```bash
cd BASE_DE_DATOS
python database.py
```

El script crea el archivo `padelbeche.db`, elimina una versión anterior si
existe y ejecuta `schema.sql`, que contiene las tablas y registros de ejemplo.

Este archivo se genera como parte del desarrollo de la base de datos, pero no
es utilizado todavía por las pantallas de Tkinter.

## Próximas etapas

- Conectar la interfaz gráfica con SQLite.
- Reemplazar las listas temporales por operaciones de lectura y escritura en
	la base de datos.
- Mantener los registros al cerrar y volver a abrir la aplicación.
- Aplicar desde SQLite las relaciones entre clientes, canchas y reservas.
- Completar las validaciones de integridad y persistencia.

## Documentación adicional

La descripción de las tablas, sus relaciones y las reglas principales del
modelo se encuentra en [docs/modelo-datos.md](docs/modelo-datos.md).
