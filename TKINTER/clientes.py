import tkinter as tk
from tkinter import ttk, messagebox


clientes = []


def ventana_clientes(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Gestión de Clientes")
        ventana.geometry("1280x720")

    titulo = tk.Label(
        ventana,
        text="GESTIÓN DE CLIENTES",
        font=("Arial", 20)
    )
    titulo.pack(pady=20)

    # Datos del cliente
    formulario = tk.LabelFrame(ventana)
    formulario.pack(fill="x",padx=20, pady=10)

    tk.Label(formulario, text="DNI:").grid(row=1, column=0, padx=10, pady=5)
    entrada_dni = tk.Entry(formulario)
    entrada_dni.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Nombre y apellido:").grid(row=2, column=0, padx=10, pady=5)
    entrada_nombre = tk.Entry(formulario)
    entrada_nombre.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Teléfono:").grid(row=1, column=2, padx=10, pady=5)
    entrada_telefono = tk.Entry(formulario)
    entrada_telefono.grid(row=1, column=3, padx=10, pady=5)

    tk.Label(formulario, text="Email:").grid(row=2, column=2, padx=10, pady=5)
    entrada_email = tk.Entry(formulario)
    entrada_email.grid(row=2, column=3, padx=10, pady=5)

    # Tabla
    tabla = ttk.Treeview(
        ventana,
        columns=("DNI", "Nombre", "Telefono", "Email"),
        show="headings"
    )

    tabla.heading("DNI", text="DNI")
    tabla.heading("Nombre", text="Nombre y apellido")
    tabla.heading("Telefono", text="Teléfono")
    tabla.heading("Email", text="Email")

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    def limpiar():
        entrada_dni.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_telefono.delete(0, tk.END)
        entrada_email.delete(0, tk.END)

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

        for cliente in clientes:
            tabla.insert(
                "",
                tk.END,
                values=(
                    cliente["dni"],
                    cliente["nombre"],
                    cliente["telefono"],
                    cliente["email"]
                )
            )

    def guardar():
        dni = entrada_dni.get()
        nombre = entrada_nombre.get()
        telefono = entrada_telefono.get()
        email = entrada_email.get()

        if dni == "" or nombre == "":
            messagebox.showwarning(
                "Datos incompletos",
                "DNI y nombre son obligatorios."
            )
            return

        for cliente in clientes:
            if cliente["dni"] == dni:
                messagebox.showerror(
                    "Error",
                    "Ya existe un cliente con ese DNI."
                )
                return

        clientes.append({
            "dni": dni,
            "nombre": nombre,
            "telefono": telefono,
            "email": email
        })

        actualizar_tabla()
        limpiar()

        messagebox.showinfo(
            "Cliente",
            "Cliente guardado correctamente."
        )

    def buscar():
        dni = entrada_dni.get()

        for cliente in clientes:
            if cliente["dni"] == dni:
                entrada_nombre.delete(0, tk.END)
                entrada_nombre.insert(0, cliente["nombre"])

                entrada_telefono.delete(0, tk.END)
                entrada_telefono.insert(0, cliente["telefono"])

                entrada_email.delete(0, tk.END)
                entrada_email.insert(0, cliente["email"])

                return

        messagebox.showinfo(
            "Buscar",
            "No se encontró un cliente con ese DNI."
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

    actualizar_tabla()