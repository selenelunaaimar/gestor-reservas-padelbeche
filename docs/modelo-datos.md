# Modelo de datos

## Estado del desarrollo

Este documento describe el diseño inicial de la base de datos del gestor de
reservas PadelBeche. La estructura se encuentra definida en
`BASE_DE_DATOS/schema.sql` y puede generarse mediante
`BASE_DE_DATOS/database.py`.

La base de datos se encuentra en una etapa inicial y todavía no está conectada
con la interfaz gráfica. La aplicación utiliza listas temporales en memoria
para probar el funcionamiento de las pantallas, los botones y las
validaciones. La conexión entre Tkinter y SQLite será realizada en una etapa
posterior.

## Entidades

### Clientes

Almacena los datos de las personas que realizan reservas.

| Campo | Tipo | Restricciones |
|---|---|---|
| `dni` | `INTEGER` | Clave primaria y obligatorio |
| `nombre_apellido` | `VARCHAR(100)` | Obligatorio |
| `telefono` | `INTEGER` | Obligatorio |
| `email` | `VARCHAR(100)` | Obligatorio |

### Canchas

Almacena las canchas disponibles en el complejo deportivo.

| Campo | Tipo | Restricciones |
|---|---|---|
| `id_cancha` | `INTEGER` | Clave primaria autoincremental |
| `tipo_deporte` | `VARCHAR(20)` | Obligatorio |
| `capacidad` | `INTEGER` | Obligatorio |
| `precio_hora` | `REAL` | Obligatorio |
| `estado` | `VARCHAR(20)` | `Activa` o `Inactiva` |

### Reservas

Relaciona un cliente con una cancha en una fecha y horario determinados.

| Campo | Tipo | Restricciones |
|---|---|---|
| `id_reserva` | `INTEGER` | Clave primaria autoincremental |
| `dni_cliente` | `INTEGER` | Obligatorio y clave foránea |
| `id_cancha` | `INTEGER` | Obligatorio y clave foránea |
| `fecha` | `DATE` | Obligatorio |
| `hora_inicio` | `TIME` | Obligatorio |
| `hora_fin` | `TIME` | Obligatorio |
| `estado_reserva` | `VARCHAR(20)` | `Confirmada`, `Pendiente` o `Cancelada` |

## Relaciones

- Un cliente puede realizar muchas reservas.
- Una cancha puede tener muchas reservas.
- Cada reserva pertenece a un único cliente.
- Cada reserva pertenece a una única cancha.
- `reservas.dni_cliente` referencia a `clientes.dni`.
- `reservas.id_cancha` referencia a `canchas.id_cancha`.

## Reglas de negocio previstas

- El DNI identifica de manera única a cada cliente.
- La capacidad de una cancha debe ser mayor que cero.
- El precio por hora debe ser mayor que cero.
- La hora de inicio debe ser anterior a la hora de fin.
- Una cancha no debería tener reservas superpuestas en la misma fecha y
  horario.
- Las reservas canceladas no bloquean el horario.
- Una cancha puede estar activa o inactiva.
- Una reserva puede estar confirmada, pendiente o cancelada.

Estas reglas ya se prueban parcialmente desde la interfaz mediante
validaciones en Python. Cuando se conecte SQLite, también deberán contemplarse
en la capa de persistencia.

## Datos iniciales

El archivo `schema.sql` incluye registros de ejemplo para las tres entidades:

- Tres clientes.
- Cuatro canchas de pádel y fútbol, con estados activos e inactivos.
- Tres reservas de ejemplo.

Estos registros permiten probar la creación de la base de datos antes de
conectar la interfaz.

## Consideraciones para la próxima etapa

La aplicación y el esquema SQL utilizan actualmente estructuras y nombres
similares, pero independientes. La futura conexión deberá definir una única
fuente de datos y reemplazar las listas en memoria por consultas SQL para
crear, consultar, modificar y eliminar registros.

También deberá verificarse si `dni` y `telefono` deben mantenerse como
`INTEGER` o almacenarse como texto, ya que no se utilizan para realizar
operaciones matemáticas y podrían requerir conservar ceros iniciales.
