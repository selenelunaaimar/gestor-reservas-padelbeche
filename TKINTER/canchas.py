import tkinter as tk
from tkinter import ttk, messagebox

canchas = []

def ventana_canchas(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Gestión de Canchas")
        ventana.geometry("1280x720")

    titulo = tk.Label(
        ventana,
        text="GESTIÓN DE CANCHAS",
        font=("Arial", 20)
    )
    titulo.pack(pady=20)

    # Contenedor superior (contiene formulario y botones)
    contenedor_superior = tk.LabelFrame(ventana)
    contenedor_superior.pack(anchor="w", padx=20, pady=10)

    # Formulario
    formulario = tk.Frame(contenedor_superior)
    formulario.pack(side="left", padx=(0, 20))

    tk.Label(formulario, text="ID Cancha:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entrada_id = tk.Entry(formulario)
    entrada_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Capacidad:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entrada_capacidad = tk.Entry(formulario)
    entrada_capacidad.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Tipo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entrada_tipo = ttk.Combobox(
        formulario,
        values=["Pádel", "Fútbol"],
        state="readonly"
    )
    entrada_tipo.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Nro. Personas:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entrada_personas = tk.Entry(formulario)
    entrada_personas.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Precio por hora:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entrada_precio = tk.Entry(formulario)
    entrada_precio.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Estado:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entrada_estado = ttk.Combobox(
        formulario,
        values=["Activa", "Inactiva"],
        state="readonly"
    )
    entrada_estado.grid(row=5, column=1, padx=10, pady=5)
    entrada_estado.set("Activa")

    # Funciones internas
    def limpiar():
        entrada_id.delete(0, tk.END)
        entrada_capacidad.delete(0, tk.END)
        entrada_tipo.set("")
        entrada_personas.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)
        entrada_estado.set("Activa")

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

        for cancha in canchas:
            tabla.insert(
                "",
                tk.END,
                values=(
                    cancha["id"],
                    cancha["capacidad"],
                    cancha["tipo"],
                    cancha["personas"],
                    cancha["precio"],
                    cancha["estado"]
                )
            )

    def guardar():
        id_cancha = entrada_id.get()
        capacidad = entrada_capacidad.get()
        tipo = entrada_tipo.get()
        personas = entrada_personas.get()
        precio = entrada_precio.get()
        estado = entrada_estado.get()

        if id_cancha == "" or capacidad == "" or tipo == "":
            messagebox.showwarning(
                "Datos incompletos",
                "ID, capacidad y tipo son obligatorios."
            )
            return

        for cancha in canchas:
            if cancha["id"] == id_cancha:
                messagebox.showerror(
                    "Error",
                    "Ya existe una cancha con ese ID."
                )
                return

        canchas.append({
            "id": id_cancha,
            "capacidad": capacidad,
            "tipo": tipo,
            "personas": personas,
            "precio": precio,
            "estado": estado
        })

        actualizar_tabla()
        limpiar()

        messagebox.showinfo(
            "Cancha",
            "Cancha guardada correctamente."
        )

    def buscar():
        id_cancha = entrada_id.get()

        for cancha in canchas:
            if cancha["id"] == id_cancha:
                entrada_capacidad.delete(0, tk.END)
                entrada_capacidad.insert(0, cancha["capacidad"])

                entrada_tipo.set(cancha["tipo"])

                entrada_personas.delete(0, tk.END)
                entrada_personas.insert(0, cancha["personas"])

                entrada_precio.delete(0, tk.END)
                entrada_precio.insert(0, cancha["precio"])

                entrada_estado.set(cancha["estado"])

                return

        messagebox.showinfo(
            "Buscar",
            "No se encontró una cancha con ese ID."
        )

    # Bloque de botones
    botones = tk.Frame(contenedor_superior)
    botones.pack(side="left", anchor="n", padx=10)

    tk.Button(
        botones,
        text="Nuevo",
        command=limpiar,
        width=12
    ).pack(pady=5)

    tk.Button(
        botones,
        text="Guardar",
        command=guardar,
        width=12
    ).pack(pady=5)

    tk.Button(
        botones,
        text="Buscar",
        command=buscar,
        width=12
    ).pack(pady=5)


    # Tabla 
    tabla = ttk.Treeview(
        ventana,
        columns=(
            "ID",
            "Capacidad",
            "Tipo",
            "Personas",
            "Precio",
            "Estado"
        ),
        show="headings"
    )

    tabla.heading("ID", text="ID Cancha")
    tabla.heading("Capacidad", text="Capacidad")
    tabla.heading("Tipo", text="Tipo")
    tabla.heading("Personas", text="Nro. Personas")
    tabla.heading("Precio", text="Precio/Hora")
    tabla.heading("Estado", text="Estado")

    tabla.column("ID", width=100)
    tabla.column("Capacidad", width=100)
    tabla.column("Tipo", width=120)
    tabla.column("Personas", width=100)
    tabla.column("Precio", width=100)
    tabla.column("Estado", width=100)

    tabla.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    limpiar()
    actualizar_tabla()