import mysql.connector
from BASE_DE_DATOS.database import obtener_conexion

def obtener_nombres_clientes_db():
    """Obtiene la lista de nombres y apellidos de los clientes para los filtros."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_apellido FROM clientes")
            nombres = [row[0] for row in cursor.fetchall()]
            return nombres
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return []

def obtener_ids_canchas_db():
    """Obtiene la lista de IDs de las canchas para los filtros."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_cancha FROM canchas")
            ids = [str(row[0]) for row in cursor.fetchall()]
            return ids
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return []

def buscar_reservas_db(desde, hasta, cliente_filtro, cancha_filtro):
    """Realiza la consulta robusta uniendo reservas, clientes y canchas en MySQL con parámetros dinámicos."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            
            query = """
                SELECT r.fecha, c.nombre_apellido, c.dni, r.id_cancha, can.tipo_deporte, r.hora_inicio, r.hora_fin, r.estado_reserva
                FROM reservas r
                JOIN clientes c ON r.dni_cliente = c.dni
                JOIN canchas can ON r.id_cancha = can.id_cancha
                WHERE 1=1
            """
            params = []

            if desde != "":
                query += " AND r.fecha >= %s"
                params.append(desde)

            if hasta != "":
                query += " AND r.fecha <= %s"
                params.append(hasta)

            if cliente_filtro != "Todos" and cliente_filtro != "":
                query += " AND c.nombre_apellido LIKE %s"
                params.append(f"%{cliente_filtro}%")

            if cancha_filtro != "Todas" and cancha_filtro != "":
                query += " AND r.id_cancha = %s"
                params.append(cancha_filtro)

            cursor.execute(query, tuple(params))
            registros = cursor.fetchall()
            return registros
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return []