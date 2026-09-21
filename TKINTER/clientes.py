import tkinter as tk
from tkinter import ttk, messagebox
import re

clientes = [
    {
         "dni": "12345678",
         "nombre_apellido": "Juan Perez",
         "telefono": "3511234567",
         "email": "juan.perez@gmail.com"
     }
]

def ventana_clientes(parent=None):
    # Se unificó el manejo de la ventana principal, manteniendo la compatibilidad tanto si se abre independiente como en solapas
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Gestión de Clientes")
        ventana.geometry("1280x720")

    # Título principal
    titulo = tk.Label(
        ventana,
        text="Gestión de Clientes",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=(15, 10))

    # Contenedor principal que divide en dos columnas
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # ==================== PANEL IZQUIERDO: TABLA ====================
    panel_izq = tk.Frame(contenedor, padx=5, pady=5)
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Tabla que muestra los Clientes
    columnas = ("DNI", "Nombre y Apellido", "Teléfono", "Email")
    tabla = ttk.Treeview(panel_izq, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(fill=tk.BOTH, expand=True)

    # ==================== PANEL DERECHO: FORMULARIO Y BOTONES ====================
    panel_der = tk.Frame(contenedor, padx=10, pady=5)
    panel_der.pack(side=tk.RIGHT, fill=tk.Y)

    # Campos del formulario con diseño vertical apilado
    tk.Label(panel_der, text="DNI:").pack(anchor="w")
    entrada_dni = tk.Entry(panel_der, width=30)
    entrada_dni.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Nombre y apellido:").pack(anchor="w")
    entrada_nombre_apellido = tk.Entry(panel_der, width=30)
    entrada_nombre_apellido.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Teléfono:").pack(anchor="w")
    entrada_telefono = tk.Entry(panel_der, width=30)
    entrada_telefono.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Email:").pack(anchor="w")
    entrada_email = tk.Entry(panel_der, width=30)
    entrada_email.pack(fill=tk.X, pady=2)

    # Funciones internas
    def limpiar(): # Limpia los campos del formulario
        entrada_dni.delete(0, tk.END)
        entrada_nombre_apellido.delete(0, tk.END)
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
                    cliente["nombre_apellido"],
                    cliente["telefono"],
                    cliente["email"]
                )
            )

    def guardar():
        dni = entrada_dni.get().strip() # .strip elimina espacios
        nombre_apellido = entrada_nombre_apellido.get().strip()
        telefono = entrada_telefono.get().strip()
        email = entrada_email.get().strip()
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not dni and not nombre_apellido and not telefono and not email: # Valida que no haya ningún campo sin dato
            messagebox.showerror(
                "Datos incompletos",
                "Debe completar los datos del cliente."
            )
            return 
        
        if not dni: # Valida DNI obligatorio
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar DNI"
            )
            return

        if not nombre_apellido: # Valida nombre obligatorio
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar nombre y apellido."
            )
            return

        if not telefono: # Valida teléfono obligatorio
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar el teléfono."
            )
            return
        
        if not email: # Valida email obligatorio
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar email."
            )
            return

        if not dni.isdigit(): # Valida que DNI sean números
            messagebox.showerror(
                "Error",
                "El DNI debe contener sólo números."
            )
            return

        if len(dni) < 7 or len(dni) > 8: # Valida la longitud del DNI
            messagebox.showerror(
                "Error",
                "El DNI debe tener entre 7 y 8 dígitos."
            )
            return
        
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre_apellido): # Valida nombre sólo letras
            messagebox.showerror(
                "Error",
                "Ingrese un nombre válido."
            )
            return
        
        if len(nombre_apellido) < 3: # Valida longitud de nombre y apellido
            messagebox.showerror(
                "Error",
                "El nombre debe tener al menos 3 caracteres."
            )
            return
        
        if not telefono.isdigit(): # Valida teléfono sean números
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
        
        if not re.match(patron_email, email): # Valida email
            messagebox.showerror(
                "Error",
                "Debe ingresar un mail válido."
            )
            return
        
        for cliente in clientes: # Valida DNI duplicado
            if cliente["dni"] == dni:
                messagebox.showerror(
                    "Error",
                    "Ya existe un cliente con ese DNI."
                )
                return

        clientes.append({
            "dni": dni,
            "nombre_apellido": nombre_apellido,
            "telefono": telefono,
            "email": email
        })

        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Cliente", "Cliente guardado correctamente.")

    def modificar():
        dni = entrada_dni.get().strip()
        nombre_apellido = entrada_nombre_apellido.get().strip()
        telefono = entrada_telefono.get().strip()
        email = entrada_email.get().strip()
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not dni:
            messagebox.showwarning("Atención", "Ingrese o seleccione el DNI del cliente a modificar.")
            return

        if not nombre_apellido or not telefono or not email:
            messagebox.showwarning("Datos incompletos", "Todos los campos deben estar completos para modificar.")
            return

        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre_apellido) or len(nombre_apellido) < 3:
            messagebox.showerror("Error", "Ingrese un nombre y apellido válido (mínimo 3 letras).")
            return

        if not telefono.isdigit() or len(telefono) < 8 or len(telefono) > 15:
            messagebox.showerror("Error", "El teléfono debe contener sólo números (entre 8 y 15 dígitos).")
            return

        if not re.match(patron_email, email):
            messagebox.showerror("Error", "Debe ingresar un mail válido.")
            return

        cliente_encontrado = False
        for cliente in clientes:
            if cliente["dni"] == dni:
                cliente["nombre_apellido"] = nombre_apellido
                cliente["telefono"] = telefono
                cliente["email"] = email
                cliente_encontrado = True
                break

        if cliente_encontrado:
            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Cliente modificado correctamente.")
        else:
            messagebox.showwarning("Modificar", "No se encontró un cliente registrado con ese DNI.")

    def buscar(): # Busca registro por DNI y lo muestra en el formulario
        dni = entrada_dni.get().strip()
        if not dni:
            messagebox.showwarning("Buscar", "Ingrese un DNI para buscar.")
            return

        for cliente in clientes:
            if cliente["dni"] == dni:
                entrada_nombre_apellido.delete(0, tk.END)
                entrada_nombre_apellido.insert(0, cliente["nombre_apellido"])

                entrada_telefono.delete(0, tk.END)
                entrada_telefono.insert(0, cliente["telefono"])

                entrada_email.delete(0, tk.END)
                entrada_email.insert(0, cliente["email"])
                return

        messagebox.showinfo(
            "Buscar",
            "No se encontró un cliente con ese DNI."
        )

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Eliminar",
                "Debe seleccionar un cliente de la tabla."
            )
            return

        item = tabla.item(seleccion[0])
        dni = str(item["values"][0])

        if not messagebox.askyesno(
            "Eliminar",
            f"¿Está seguro de eliminar el cliente con DNI {dni}?"
        ):
            return

        global clientes
        clientes = [
            cliente
            for cliente in clientes
            if str(cliente["dni"]) != str(dni)
        ]
        
        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Eliminar", "Cliente eliminado correctamente.")

    def seleccionar_tabla(event):
        seleccion = tabla.selection()
        if seleccion:
            item = tabla.item(seleccion[0])
            valores = item["values"]
            limpiar()
            entrada_dni.insert(0, valores[0])
            entrada_nombre_apellido.insert(0, valores[1])
            entrada_telefono.insert(0, valores[2])
            entrada_email.insert(0, valores[3])

    # Vinculación del evento de selección en la tabla
    tabla.bind("<<TreeviewSelect>>", seleccionar_tabla)

    # Bloque de botones
    botones = tk.Frame(panel_der, pady=10)
    botones.pack(fill=tk.X)

    tk.Button(
        botones,
        text="Guardar",
        command=guardar,
        width=15
    ).pack(pady=2)

    tk.Button(
        botones,
        text="Modificar",
        command=modificar,
        width=15
    ).pack(pady=2)

    tk.Button(
        botones,
        text="Buscar",
        command=buscar,
        width=15
    ).pack(pady=2)

    tk.Button(
        botones,
        text="Eliminar",
        command=eliminar,
        width=15
    ).pack(pady=2)

    tk.Button(
        botones,
        text="Limpiar",
        command=limpiar,
        width=15
    ).pack(pady=2)

    # Carga inicial de datos en la tabla
    actualizar_tabla()

    # Si se pasa un contenedor padre, empaqueta y retorna la ventana principal
    if parent is not None:
        ventana.pack(fill=tk.BOTH, expand=True)
    return ventana