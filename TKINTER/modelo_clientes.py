import mysql.connector
from BASE_DE_DATOS.database import obtener_conexion

def obtener_clientes_db():
    """Consulta todos los registros de clientes en la base de datos MySQL."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT dni, nombre_apellido, telefono, email FROM clientes")
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
            query = "UPDATE clientes SET nombre_apellido = %s, telefono = %s, email = %s WHERE dni = %s"
            cursor.execute(query, (nombre_apellido, telefono, email, dni))
            conexion.commit()
            return cursor.rowcount
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return 0

def eliminar_cliente_db(dni):
    """Elimina un cliente y sus reservas asociadas de la base de datos por su DNI."""
    conexion = obtener_conexion()
    if not conexion:
        raise Exception("No se pudo conectar a la base de datos.")
    
    cursor = None
    try:
        cursor = conexion.cursor()
        
        """1. Primero borramos las reservas asociadas a este cliente para evitar error de clave foránea"""
        cursor.execute("DELETE FROM reservas WHERE dni_cliente = %s", (dni,))
        
        """2. Luego borramos al cliente"""
        cursor.execute("DELETE FROM clientes WHERE dni = %s", (dni,))
        filas = cursor.rowcount
        
        conexion.commit()
        return filas
    except mysql.connector.Error as err:
        conexion.rollback()
        raise err
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

def buscar_cliente_db(dni):
    """Busca un cliente por su DNI en la base de datos MySQL."""
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre_apellido, telefono, email FROM clientes WHERE dni = %s", (dni,))
            resultado = cursor.fetchone()
            return resultado
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
            conexion.close()
    return None