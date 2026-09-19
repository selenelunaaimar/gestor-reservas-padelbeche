import tkinter as tk
from tkinter import ttk, messagebox
import re

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
        patron_email=r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not dni and not nombre and not telefono and not email: #valida q no haya ningun campo sin dato
            messagebox.showerror(
                "Datos incompletos",
                "Debe completar los datos del cliente."
            )
            return 
        
        if not dni: #valida dni oblig
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar DNI"
            )
            return

        if not nombre: #valida nom oblig
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar nombre y apellido."
            )
            return

        if not telefono: #valida tel oblig
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar el teléfono."
            )
            return
        
        if not email: #valida email oblig
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar email."
            )
            return

        if not dni.isdigit(): #valida q DNI sea integer
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
        
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre): #valida nom sólo letras
                messagebox.showerror(
                    "Error",
                    "Ingrese un nombre válido."
                )
                return
        
        if len(nombre) < 3: #valida long nom y apel
            messagebox.showerror(
                "Error",
                "El nombre debe tener al menos 3 caracteres."
            )
            return
        
        if not telefono.isdigit(): #valida tel sea integer
            messagebox.showerror(
                "Error",
                "El teléfono debe contener sólo números."
            )
            return

        if len(telefono) < 8 or len(telefono) > 15:
            messagebox.showerror(
                "Error",
                "El teléfono debe tener entre 8 y 15 dígitos."
            )
            return
        
        if not re.match(patron_email, email): #valida email
            messagebox.showerror(
                "Error",
                "Debe ingresar un mail válido."
            )
            return
        
        for cliente in clientes: #valida dni dupli
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
        columns=("dni", "Nombre", "Telefono", "Email"),
        show="headings"
    )

    tabla.heading("dni", text="DNI")
    tabla.heading("Nombre", text="Nombre y apellido")
    tabla.heading("Telefono", text="Teléfono")
    tabla.heading("Email", text="Email")

    tabla.column("dni", width=150)
    tabla.column("Nombre", width=300)
    tabla.column("Telefono", width=200)
    tabla.column("Email", width=300)

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    actualizar_tabla()