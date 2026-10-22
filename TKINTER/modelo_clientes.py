import mysql.connector
from BASE_DE_DATOS.database import obtener_conexion

def obtener_clientes_db():
    """Consulta los clientes, incluyendo la fecha de baja si corresponde."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT dni, nombre_apellido, telefono, email, fecha_baja
                FROM clientes
                ORDER BY fecha_baja IS NOT NULL, nombre_apellido
                """
            )
            registros = cursor.fetchall()
            return registros
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return []

def insertar_cliente_db(dni, nombre_apellido, telefono, email):
    """Inserta un nuevo cliente en la base de datos MySQL."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO clientes (dni, nombre_apellido, telefono, email) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (dni, nombre_apellido, telefono, email))
            conexion.commit()
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()

def actualizar_cliente_db(nombre_apellido, telefono, email, dni):
    """Actualiza un cliente existente en la base de datos MySQL."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                UPDATE clientes
                SET nombre_apellido = %s, telefono = %s, email = %s
                WHERE dni = %s AND fecha_baja IS NULL
            """
            cursor.execute(query, (nombre_apellido, telefono, email, dni))
            conexion.commit()
            return cursor.rowcount
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return 0


def dar_de_baja_cliente_db(dni):
    """Marca un cliente como dado de baja sin eliminar sus reservas."""
    conexion = obtener_conexion()
    if not conexion:
        raise RuntimeError("No se pudo conectar a la base de datos.")

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            UPDATE clientes
            SET fecha_baja = CURRENT_DATE
            WHERE dni = %s AND fecha_baja IS NULL
            """,
            (dni,),
        )
        filas = cursor.rowcount
        conexion.commit()
        return filas
    except mysql.connector.Error as err:
        conexion.rollback()
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def eliminar_cliente_sin_reservas_db(dni):
    """Elimina físicamente un cliente solo si no tiene reservas asociadas."""
    conexion = obtener_conexion()
    if not conexion:
        raise RuntimeError("No se pudo conectar a la base de datos.")

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT dni FROM clientes WHERE dni = %s FOR UPDATE",
            (dni,),
        )
        if cursor.fetchone() is None:
            conexion.rollback()
            return "no_encontrado"

        cursor.execute(
            "SELECT 1 FROM reservas WHERE dni_cliente = %s LIMIT 1",
            (dni,),
        )
        if cursor.fetchone() is not None:
            conexion.rollback()
            return "tiene_reservas"

        cursor.execute("DELETE FROM clientes WHERE dni = %s", (dni,))
        conexion.commit()
        return "eliminado"
    except mysql.connector.Error as err:
        conexion.rollback()
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def buscar_cliente_db(dni):
    """Busca un cliente por DNI e incluye su fecha de baja, si existe."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT nombre_apellido, telefono, email, fecha_baja
                FROM clientes
                WHERE dni = %s
                """,
                (dni,),
            )
            resultado = cursor.fetchone()
            return resultado
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return None