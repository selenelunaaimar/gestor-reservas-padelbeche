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

    # Formulario
    formulario = tk.LabelFrame(ventana)
    formulario.pack(fill="x",padx=20, pady=10)

    tk.Label(formulario, text="ID Cancha:").grid(row=1, column=0, padx=10, pady=5)
    entrada_id = tk.Entry(formulario)
    entrada_id.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Capacidad:").grid(row=2, column=0, padx=10, pady=5 )
    entrada_capacidad = tk.Entry(formulario)
    entrada_capacidad.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Tipo:").grid(row=1, column=2, padx=10, pady=5)
    entrada_tipo = ttk.Combobox(
        formulario,
        values=["Pádel", "Fútbol"],
        state="readonly"
    )
    entrada_tipo.grid(row=1, column=3, padx=10, pady=5)

    tk.Label(formulario, text="Nro. Personas:").grid(row=2, column=2, padx=10, pady=5)
    entrada_personas = tk.Entry(formulario)
    entrada_personas.grid(row=2, column=3, padx=10, pady=5)

    tk.Label(formulario, text="Precio por hora:").grid(row=1, column=5, padx=10, pady=5)
    entrada_precio = tk.Entry(formulario)
    entrada_precio.grid(row=1, column=6, padx=10, pady=5)

    tk.Label(formulario, text="Estado:").grid(row=2, column=5, padx=10, pady=5)
    entrada_estado = ttk.Combobox(
        formulario,
        values=["Activa", "Inactiva"],
        state="readonly"
    )
    entrada_estado.grid(row=2, column=6, padx=10, pady=5)

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

    tabla.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

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

    botones = tk.Frame(ventana)
    botones.pack(pady=10)

    tk.Button(
        botones,
        text="Nuevo",
        command=limpiar
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        botones,
        text="Guardar",
        command=guardar
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        botones,
        text="Buscar",
        command=buscar
    ).grid(row=0, column=2, padx=5)

    limpiar()
    actualizar_tabla()