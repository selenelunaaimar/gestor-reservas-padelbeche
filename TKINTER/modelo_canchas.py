import mysql.connector
from BASE_DE_DATOS.database import obtener_conexion

def obtener_canchas_db():
    """Consulta las canchas registradas en la base de datos."""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT
                id_cancha AS id,
                tipo_deporte AS tipo,
                capacidad,
                precio_hora AS precio,
                estado
            FROM canchas
            ORDER BY id_cancha
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def insertar_cancha_db(id_cancha, tipo, capacidad_num, precio_num, estado):
    """Inserta una nueva cancha en la base de datos."""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = """
            INSERT INTO canchas
                (id_cancha, tipo_deporte, capacidad, precio_hora, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_cancha, tipo, capacidad_num, precio_num, estado))
        conexion.commit()
    except mysql.connector.Error as err:
        if conexion is not None:
            conexion.rollback()
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def actualizar_cancha_db(tipo, capacidad_num, precio_num, estado, id_cancha):
    """Actualiza los datos de una cancha existente en la base de datos."""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = """
            UPDATE canchas
            SET
                tipo_deporte = %s,
                capacidad = %s,
                precio_hora = %s,
                estado = %s
            WHERE id_cancha = %s
        """
        cursor.execute(query, (tipo, capacidad_num, precio_num, estado, id_cancha))
        filas = cursor.rowcount
        if filas == 0:
            conexion.rollback()
        else:
            conexion.commit()
        return filas
    except mysql.connector.Error as err:
        if conexion is not None:
            conexion.rollback()
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def buscar_cancha_db(id_cancha):
    """Busca una cancha por su ID en la base de datos."""
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT
                id_cancha AS id,
                tipo_deporte AS tipo,
                capacidad,
                precio_hora AS precio,
                estado
            FROM canchas
            WHERE id_cancha = %s
        """
        cursor.execute(query, (id_cancha,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()