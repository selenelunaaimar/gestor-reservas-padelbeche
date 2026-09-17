import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "padelbeche.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def crear_base_de_datos():
    # Eliminar la base anterior si existe
    if DB_PATH.exists():
        DB_PATH.unlink()

    conexion = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as archivo:
        script_sql = archivo.read()

    conexion.executescript(script_sql)
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_base_de_datos()
    print("Base de datos creada correctamente.")