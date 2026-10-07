import sys
import os

# Agrega la carpeta raíz del proyecto al path de Python para encontrar BASE_DE_DATOS
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox
from BASE_DE_DATOS.database import obtener_conexion
import mysql.connector


def ventana_consultas(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Consultas")
        ventana.geometry("1280x720")

    titulo = tk.Label(
        ventana,
        text="Consultas de Reservas",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=(15, 10))

    # Contenedor principal que divide la tabla y el panel derecho
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Panel Izquierdo/Medio: Tabla de resultados
    panel_izq = tk.Frame(contenedor, padx=5, pady=5)
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # ------------------------------------------------
    # TABLA DE RESULTADOS
    # ------------------------------------------------

    tabla = ttk.Treeview(
        panel_izq,
        columns=(
            "Fecha",
            "Cliente",
            "DNI",
            "Cancha",
            "Tipo",
            "Inicio",
            "Fin",
            "Estado"
        ),
        show="headings"
    )

    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("DNI", text="DNI")
    tabla.heading("Cancha", text="Cancha")
    tabla.heading("Tipo", text="Tipo")
    tabla.heading("Inicio", text="Hora Inicio")
    tabla.heading("Fin", text="Hora Fin")
    tabla.heading("Estado", text="Estado")

    tabla.column("Fecha", width=100)
    tabla.column("Cliente", width=150)
    tabla.column("DNI", width=100)
    tabla.column("Cancha", width=80)
    tabla.column("Tipo", width=80)
    tabla.column("Inicio", width=100)
    tabla.column("Fin", width=100)
    tabla.column("Estado", width=100)

    tabla.pack(fill=tk.BOTH, expand=True)

    # Panel Derecho: Filtros y Botones
    panel_der = tk.Frame(contenedor, padx=5, pady=5)
    panel_der.pack(side=tk.RIGHT, fill=tk.Y)

    encabezado_filtros = tk.Frame(panel_der)
    encabezado_filtros.pack(fill=tk.X, pady=(0, 5))

    # Canvas para dibujar la lupa
    lupa = tk.Canvas(
        encabezado_filtros,
        width=22,
        height=22,
        highlightthickness=0
    )
    lupa.pack(side="left", padx=(0, 6))

    # Círculo de la lupa
    lupa.create_oval(
        3, 3, 14, 14,
        outline="black",
        width=2
    )

    # Mango de la lupa
    lupa.create_line(
        13, 13, 19, 19,
        fill="black",
        width=2
    )

    # Texto
    tk.Label(
        encabezado_filtros,
        text="Filtros de búsqueda",
        font=("Arial", 11, "bold")
    ).pack(side="left")

    # ------------------------------------------------
    # CAMPOS DE FILTRO
    # ------------------------------------------------

    tk.Label(panel_der, text="Desde:").pack(anchor="w")
    entrada_desde = tk.Entry(panel_der)
    entrada_desde.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Hasta:").pack(anchor="w")
    entrada_hasta = tk.Entry(panel_der)
    entrada_hasta.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Cliente:").pack(anchor="w")
    entrada_cliente = ttk.Combobox(
        panel_der,
        state="readonly"
    )
    entrada_cliente.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Cancha:").pack(anchor="w")
    entrada_cancha = ttk.Combobox(
        panel_der,
        state="readonly"
    )
    entrada_cancha.pack(fill=tk.X, pady=2)

    # ------------------------------------------------
    # FUNCIONES INTERNAS
    # ------------------------------------------------

    def cargar_filtros():
        """Carga los nombres de clientes y los IDs de canchas desde la base de datos MySQL para los combobox."""
        conexion = obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                
                # Cargar clientes
                cursor.execute("SELECT nombre_apellido FROM clientes")
                nombres_clientes = ["Todos"] + [row[0] for row in cursor.fetchall()]
                entrada_cliente["values"] = nombres_clientes
                entrada_cliente.set("Todos")

                # Cargar canchas
                cursor.execute("SELECT id_cancha FROM canchas")
                ids_canchas = ["Todas"] + [str(row[0]) for row in cursor.fetchall()]
                entrada_cancha["values"] = ids_canchas
                entrada_cancha.set("Todas")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudieron cargar los filtros: {err}")
            finally:
                cursor.close()
                conexion.close()

    def limpiar_resultados():
        for item in tabla.get_children():
            tabla.delete(item)

    def buscar():
        desde = entrada_desde.get().strip()
        hasta = entrada_hasta.get().strip()
        cliente_filtro = entrada_cliente.get()
        cancha_filtro = entrada_cancha.get()

        limpiar_resultados()

        # Consulta robusta uniendo reservas, clientes y canchas en MySQL
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
                    query += " AND c.nombre_apellido = %s"
                    params.append(cliente_filtro)

                if cancha_filtro != "Todas" and cancha_filtro != "":
                    query += " AND r.id_cancha = %s"
                    params.append(cancha_filtro)

                cursor.execute(query, tuple(params))
                registros = cursor.fetchall()

                for reserva in registros:
                    tabla.insert(
                        "",
                        tk.END,
                        values=reserva
                    )

                if len(registros) == 0:
                    messagebox.showinfo(
                        "Consulta",
                        "No se encontraron reservas."
                    )

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al realizar la consulta: {err}")
            finally:
                cursor.close()
                conexion.close()

    # ------------------------------------------------
    # BOTONES
    # ------------------------------------------------

    botones = tk.Frame(panel_der, pady=10)
    botones.pack(fill=tk.X)

    tk.Button(
        botones,
        text="Buscar",
        command=buscar,
        width=12
    ).pack(pady=2)

    tk.Button(
        botones,
        text="Limpiar",
        command=limpiar_resultados,
        width=12
    ).pack(pady=2)

    cargar_filtros()

    if parent is not None:
        parent.pack(fill=tk.BOTH, expand=True)
    return ventana