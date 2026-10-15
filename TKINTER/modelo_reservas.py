import mysql.connector
from BASE_DE_DATOS.database import obtener_conexion

def obtener_canchas_activas_db():
    """Consulta las canchas que se encuentran en estado Activa para el combobox."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_cancha, tipo_deporte, capacidad FROM canchas WHERE estado = 'Activa'")
        canchas = cursor.fetchall()
        cursor.close()
        conexion.close()
        return canchas
    except Exception:
        return []

def obtener_reservas_db():
    """Obtiene todas las reservas con sus respectivos clientes."""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id_reserva AS id, r.dni_cliente AS cliente, c.nombre_apellido AS nombre, 
               r.id_cancha AS cancha, r.fecha, TIME_FORMAT(r.hora_inicio, '%H:%i') AS inicio, 
               TIME_FORMAT(r.hora_fin, '%H:%i') AS fin, r.estado_reserva AS estado,
               r.vence_pago
        FROM reservas r
        JOIN clientes c ON r.dni_cliente = c.dni
        ORDER BY r.fecha, r.hora_inicio
    """)
    lista_reservas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return lista_reservas

def buscar_nombre_cliente_db(dni):
    """Busca en la base de datos de clientes y retorna el nombre y apellido directamente"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT nombre_apellido FROM clientes WHERE dni = %s", (dni,))
        resultado = cursor.fetchone()
        cursor.close()
        conexion.close()
        if resultado:
            return resultado["nombre_apellido"]
    except Exception:
        pass
    return None

def obtener_id_libre_db():
    """Devuelve el menor ID de reserva que no este en uso (reutiliza huecos)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_reserva FROM reservas ORDER BY id_reserva")
    ids_usados = {fila[0] for fila in cursor.fetchall()}
    cursor.close()
    conexion.close()

    id_libre = 1
    while id_libre in ids_usados:
        id_libre += 1
    return id_libre

def insertar_reserva_db(id_reserva, cliente, cancha, fecha, inicio, fin, estado, vence):
    """Inserta una nueva reserva en la base de datos"""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO reservas
            (id_reserva, dni_cliente, id_cancha, fecha, hora_inicio,
             hora_fin, estado_reserva, vence_pago)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (id_reserva, cliente, cancha, fecha, inicio, fin, estado, vence),
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_reserva_db(cliente, cancha, fecha, inicio, fin, estado, vence, id_reserva):
    """Actualiza una reserva existente en la base de datos"""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE reservas
        SET dni_cliente = %s, id_cancha = %s, fecha = %s,
            hora_inicio = %s, hora_fin = %s,
            estado_reserva = %s, vence_pago = %s
        WHERE id_reserva = %s
        """,
        (cliente, cancha, fecha, inicio, fin, estado, vence, id_reserva),
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_reserva_db(id_reserva):
    """Elimina una reserva de la base de datos"""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_pendientes_db():
    """Obtiene las reservas pendientes para verificar pagos vencidos"""
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id_reserva AS id, c.nombre_apellido AS nombre,
               r.id_cancha AS cancha, r.fecha,
               TIME_FORMAT(r.hora_inicio, '%H:%i') AS inicio,
               r.vence_pago
        FROM reservas r
        JOIN clientes c ON r.dni_cliente = c.dni
        WHERE r.estado_reserva = 'Pendiente'
        ORDER BY r.vence_pago
    """)
    pendientes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return pendientes