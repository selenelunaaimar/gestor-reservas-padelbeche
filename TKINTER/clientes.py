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

    # Contenedor superior (contiene formulario y botones)
    contenedor_superior = tk.LabelFrame(ventana)
    contenedor_superior.pack(anchor="w", padx=20, pady=10)

    # Formulario
    formulario = tk.Frame(contenedor_superior)
    formulario.pack(side="left", padx=(0, 20))

    # Título dentro de formulario
    tk.Label(
        formulario,
        text="👤 CLIENTES",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(0, 10))

    tk.Label(formulario, text="DNI:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entrada_dni = tk.Entry(formulario)
    entrada_dni.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Nombre y apellido:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entrada_nombre = tk.Entry(formulario)
    entrada_nombre.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Teléfono:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
    entrada_telefono = tk.Entry(formulario)
    entrada_telefono.grid(row=1, column=3, padx=10, pady=5)

    tk.Label(formulario, text="Email:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
    entrada_email = tk.Entry(formulario)
    entrada_email.grid(row=2, column=3, padx=10, pady=5)

    # Funciones internas
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
        dni = entrada_dni.get().strip() #.strip elimina espacios
        nombre = entrada_nombre.get().strip()
        telefono = entrada_telefono.get().strip()
        email = entrada_email.get().strip()

        #if dni == "" or nombre == "":
         #   messagebox.showwarning(
          #      "Datos incompletos",
           #     "DNI y nombre son obligatorios."
            #)
            #return
        if not dni: #validac dni
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar DNI"
            )
            return

        if not nombre: #validac nombre
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar nombre y apellido."
            )
            return

        if not telefono: #validac telefono
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar el teléfono."
            )
            return
        
        if not email: #validac email
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar mail."
            )
            return

        if not dni.isdigit(): #valida q DNI sea numérico
            messagebox.showerror(
                "Error",
                "El DNI debe contener sólo números."
            )
            return

        if len(dni) < 7 or len(dni) > 8: #valida la long del DNI
            messagebox.showerror(
                "Error",
                "El DNI debe tener entre 7 y 8 dígitos."
            )
            return

        if not telefono.isdigit():
            messagebox.showerror(
                "Error",
                "El teléfono debe contener sólo números."
            )
            return
        #sigo aca 
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

    # Bloque de botones (al lado del formulario)
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
        columns=("DNI", "Nombre", "Telefono", "Email"),
        show="headings"
    )

    tabla.heading("DNI", text="DNI")
    tabla.heading("Nombre", text="Nombre y apellido")
    tabla.heading("Telefono", text="Teléfono")
    tabla.heading("Email", text="Email")

    tabla.column("DNI", width=150)
    tabla.column("Nombre", width=300)
    tabla.column("Telefono", width=200)
    tabla.column("Email", width=300)

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    actualizar_tabla()