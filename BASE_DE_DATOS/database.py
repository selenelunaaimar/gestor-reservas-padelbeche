import os
import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "padelbeche"),
    )


# Bloque de prueba de conectividad local. Permite verificar que la conexion
# con el servidor MySQL Workbench y la base de datos se establezca correctamente.


if __name__ == "__main__":
    try:
        conexion = obtener_conexion()
        if conexion.is_connected():
            print("¡Conexión exitosa a la base de datos MySQL!")
            
            cursor = conexion.cursor()
            cursor.execute("SELECT VERSION();")
            print(f"Versión de MySQL: {cursor.fetchone()[0]}")
            
            cursor.close()
            conexion.close()
    except Exception as err:
        print(f"Error al conectar con la base de datos: {err}")