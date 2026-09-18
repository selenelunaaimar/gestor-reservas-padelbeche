import tkinter as tk
from tkinter import ttk, messagebox

from reservas import reservas
from clientes import clientes
from canchas import canchas


def ventana_consultas(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Consultas")
        ventana.geometry("1280x720")

    titulo = tk.Label(
        ventana,
        text="CONSULTAS DE RESERVAS",
        font=("Arial", 20)
    )
    titulo.pack(pady=20)

    # Filtros
    filtros = tk.LabelFrame(
        ventana,
        text="Filtros de búsqueda",
        padx=10,
        pady=10
    )
    filtros.pack(fill="x", padx=20, pady=10)

    tk.Label(filtros, text="Desde:").grid(
        row=0, column=0, padx=5, pady=5
    )

    entrada_desde = tk.Entry(filtros, width=15)
    entrada_desde.grid(
        row=0, column=1, padx=5, pady=5
    )

    tk.Label(filtros, text="Hasta:").grid(
        row=0, column=2, padx=5, pady=5
    )

    entrada_hasta = tk.Entry(filtros, width=15)
    entrada_hasta.grid(
        row=0, column=3, padx=5, pady=5
    )

    tk.Label(filtros, text="Cliente:").grid(
        row=1, column=0, padx=5, pady=5
    )

    entrada_cliente = ttk.Combobox(
        filtros,
        state="readonly",
        width=20
    )
    entrada_cliente.grid(
        row=1, column=1, padx=5, pady=5
    )

    tk.Label(filtros, text="Cancha:").grid(
        row=1, column=2, padx=5, pady=5
    )

    entrada_cancha = ttk.Combobox(
        filtros,
        state="readonly",
        width=20
    )
    entrada_cancha.grid(
        row=1, column=3, padx=5, pady=5
    )

    # Titulo dentro de formulario
    tk.Label(
        ventana, text="RESULTADOS", font=("Arial", 14, "bold")
    ).pack(anchor="w", padx=20, pady=(10, 0))

    # Tabla de resultados
    tabla = ttk.Treeview(
        ventana,
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

    tabla.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    def cargar_filtros():
        nombres_clientes = ["Todos"]

        for cliente in clientes:
            nombres_clientes.append(cliente["nombre"])

        entrada_cliente["values"] = nombres_clientes
        entrada_cliente.set("Todos")

        ids_canchas = ["Todas"]

        for cancha in canchas:
            ids_canchas.append(cancha["id"])

        entrada_cancha["values"] = ids_canchas
        entrada_cancha.set("Todas")

    def limpiar_resultados():
        for item in tabla.get_children():
            tabla.delete(item)

    def buscar():
        desde = entrada_desde.get()
        hasta = entrada_hasta.get()
        cliente_filtro = entrada_cliente.get()
        cancha_filtro = entrada_cancha.get()

        limpiar_resultados()

        resultados = 0

        for reserva in reservas:

            if desde != "" and reserva["fecha"] < desde:
                continue

            if hasta != "" and reserva["fecha"] > hasta:
                continue

            if (
                cliente_filtro != "Todos"
                and cliente_filtro != ""
                and reserva["cliente"] != cliente_filtro
            ):
                continue

            if (
                cancha_filtro != "Todas"
                and cancha_filtro != ""
                and reserva["cancha"] != cancha_filtro
            ):
                continue

            dni = ""

            for cliente in clientes:
                if cliente["nombre"] == reserva["cliente"]:
                    dni = cliente["dni"]
                    break

            tipo = ""

            for cancha in canchas:
                if cancha["id"] == reserva["cancha"]:
                    tipo = cancha["tipo"]
                    break

            tabla.insert(
                "",
                tk.END,
                values=(
                    reserva["fecha"],
                    reserva["cliente"],
                    dni,
                    reserva["cancha"],
                    tipo,
                    reserva["inicio"],
                    reserva["fin"],
                    reserva["estado"]
                )
            )

            resultados += 1

        if resultados == 0:
            messagebox.showinfo(
                "Consulta",
                "No se encontraron reservas."
            )

    botones = tk.Frame(ventana)
    botones.pack(pady=10)

    tk.Button(
        botones,
        text="Buscar",
        command=buscar
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        botones,
        text="Limpiar",
        command=limpiar_resultados
    ).grid(row=0, column=1, padx=5)

    cargar_filtros()