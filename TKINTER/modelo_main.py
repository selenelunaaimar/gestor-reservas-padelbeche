import mysql.connector
from BASE_DE_DATOS.database import obtener_conexion

def obtener_reservas_dia_db():
    """Obtiene las reservas y clientes directamente desde MySQL para la pantalla principal."""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.id_reserva AS id, r.dni_cliente AS cliente, c.nombre_apellido AS nombre, 
                   r.id_cancha AS cancha, r.fecha, TIME_FORMAT(r.hora_inicio, '%H:%i') AS inicio, 
                   TIME_FORMAT(r.hora_fin, '%H:%i') AS fin, r.estado_reserva AS estado 
            FROM reservas r
            JOIN clientes c ON r.dni_cliente = c.dni
            ORDER BY r.hora_inicio ASC
        """)
        lista_reservas = cursor.fetchall()
        return lista_reservas
    except Exception as err:
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()