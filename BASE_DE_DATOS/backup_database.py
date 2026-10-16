
import os
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

#funcion respaldo
def crear_respaldo():
    # 1. Datos de conexión
    base = os.getenv("DB_NAME", "padelbeche")
    usuario = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "12345")
    servidor = os.getenv("DB_HOST", "localhost")
    puerto = os.getenv("DB_PORT", "3306")

    # 2. Carpeta de destino
    carpeta = Path.home() / "Documents" / "PadelBeche" / "BackUps"
    carpeta.mkdir(parents=True, exist_ok=True)

    # 3. Nombre único del archivo
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archivo = carpeta / f"backup_{base}_{fecha}.sql"

    # 4. Buscar mysqldump
    programa = shutil.which("mysqldump")

    if not programa:
        programa = (
            r"C:\Program Files\MySQL"
            r"\MySQL Server 8.0\bin\mysqldump.exe"
        )

    if not Path(programa).is_file():
        raise FileNotFoundError("No se encontró mysqldump.exe")

    # 5. Archivo temporal con credenciales
    config = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".cnf",
            delete=False,
            encoding="utf-8"
        ) as temporal:
            config = Path(temporal.name)
            temporal.write("[client]\n")
            temporal.write(f"host={servidor}\n")
            temporal.write(f"port={puerto}\n")
            temporal.write(f"user={usuario}\n")
            temporal.write(
                'password="' +
                password.replace("\\", "\\\\").replace('"', '\\"') +
                '"\n'
            )

        # 6. Ejecutar el respaldo
        with open(archivo, "wb") as salida:
            resultado = subprocess.run(
                [
                    programa,
                    f"--defaults-extra-file={config}",
                    "--single-transaction",
                    "--quick",
                    "--routines",
                    "--triggers",
                    "--events",
                    "--no-tablespaces",
                    "--set-gtid-purged=OFF",
                    "--databases",
                    base
                ],
                stdout=salida,
                stderr=subprocess.PIPE,
                timeout=180
            )

        if resultado.returncode != 0:
            raise RuntimeError(
                resultado.stderr.decode("utf-8", errors="replace")
            )

        if archivo.stat().st_size == 0:
            raise RuntimeError("El respaldo está vacío")

        return archivo

    except Exception:
        archivo.unlink(missing_ok=True)
        raise

    finally:
        if config:
            config.unlink(missing_ok=True)
