import tkinter as tk
from tkinter import messagebox, ttk

canchas = []

def ventana_canchas(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Gestión de Canchas")
        ventana.geometry("1280x720")
        ventana.configure(bg="#f0f0f0")

    # Título principal de la ventana
    titulo = tk.Label(
        ventana, text="Gestión de Canchas", font=("Arial", 20, "bold"), bg="#f0f0f0"
    )
    titulo.pack(pady=(15, 10))

    # Contenedor principal que divide la tabla y el panel derecho
    contenedor = tk.Frame(ventana, bg="#f0f0f0")
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Panel Izquierdo
    panel_izq = tk.Frame(contenedor, padx=5, pady=5, bg="#f0f0f0")
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tabla = ttk.Treeview(
        panel_izq,
        columns=("id", "Capacidad", "Tipo", "Precio", "Estado"),
        show="headings",
    )

    tabla.heading("id", text="ID Cancha")
    tabla.heading("Capacidad", text="Capacidad")
    tabla.heading("Tipo", text="Tipo")
    tabla.heading("Precio", text="Precio/Hora")
    tabla.heading("Estado", text="Estado")

    tabla.column("id", width=100)
    tabla.column("Capacidad", width=100)
    tabla.column("Tipo", width=120)
    tabla.column("Precio", width=100)
    tabla.column("Estado", width=100)

    tabla.pack(fill=tk.BOTH, expand=True)

    # Panel Derecho
    panel_der = tk.Frame(contenedor, padx=5, pady=5, bg="#f0f0f0")
    panel_der.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(panel_der, text="ID Cancha:", bg="#f0f0f0").pack(anchor="w")
    entrada_id = tk.Entry(panel_der)
    entrada_id.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Capacidad:", bg="#f0f0f0").pack(anchor="w")
    entrada_capacidad = tk.Entry(panel_der)
    entrada_capacidad.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Tipo:", bg="#f0f0f0").pack(anchor="w")
    entrada_tipo = ttk.Combobox(
        panel_der, values=["Pádel", "Fútbol"], state="readonly"
    )
    entrada_tipo.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Precio por hora:", bg="#f0f0f0").pack(anchor="w")
    entrada_precio = tk.Entry(panel_der)
    entrada_precio.pack(fill=tk.X, pady=2)

    tk.Label(panel_der, text="Estado:", bg="#f0f0f0").pack(anchor="w")
    entrada_estado = ttk.Combobox(
        panel_der, values=["Activa", "Inactiva"], state="readonly"
    )
    entrada_estado.pack(fill=tk.X, pady=2)
    entrada_estado.set("Activa")

    # Funciones internas
    def limpiar():
        entrada_id.config(state="normal") # Permitir limpiar y editar el ID para nuevas altas
        entrada_id.delete(0, tk.END)
        entrada_capacidad.delete(0, tk.END)
        entrada_tipo.set("")
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
                    cancha["precio"],
                    cancha["estado"],
                )
            )

    def guardar():
        id_cancha = entrada_id.get().strip()
        capacidad = entrada_capacidad.get().strip()
        tipo = entrada_tipo.get()
        precio = entrada_precio.get().strip()
        estado = entrada_estado.get()

        precio = precio.replace(",", ".") #reemplazar coma por punto

        # Validacion para que todos los campos sean obligatorios
        if not id_cancha or not capacidad or not tipo or not precio or not estado:
            messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios.")
            return

        if not id_cancha.isdigit(): #validar id sea integer
            messagebox.showerror(
                "Error", 
                "El ID de cancha debe ser un número."
            )
            return

        if not capacidad.isdigit(): #validar capac sea integer
            messagebox.showerror(
                "Error",
                "La capacidad debe ser un número."
            )
            return
        capacidad_num = int(capacidad) #para validar q sea !=0

        if capacidad_num <= 0: #validar sea != 0
            messagebox.showerror(
                "Error",
                "La capacidad debe ser mayor a cero."
            )
            return
        
        try:                    #precio_hora admite decimales
            precio_num = float(precio)
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser un número válido."
            )
            return
        
        if precio_num <= 0:
            messagebox.showerror(
                "Error",
                "El precio debe ser mayor a cero."
            )
            return
             
        for cancha in canchas: #validar id dupli
            if cancha["id"] == id_cancha:
                messagebox.showerror(
                    "Error", "Ya existe una cancha con ese ID."
                )
                return

        canchas.append({ #guardar datos
            "id": id_cancha,
            "capacidad": capacidad_num,
            "tipo": tipo,
            "precio": precio_num,
            "estado": estado,
        })

        actualizar_tabla()
        limpiar()

        messagebox.showinfo("Cancha", "Cancha guardada correctamente.")

    def modificar():
        id_cancha = entrada_id.get().strip()
        capacidad = entrada_capacidad.get().strip()
        tipo = entrada_tipo.get()
        precio = entrada_precio.get().strip()
        estado = entrada_estado.get()

        if not id_cancha:
            messagebox.showwarning("Atención", "Seleccione o ingrese el ID de la cancha a modificar.")
            return

        precio = precio.replace(",", ".")

        # Validaciones de campos obligatorios y formatos
        if not capacidad or not tipo or not precio or not estado:
            messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios.")
            return

        if not capacidad.isdigit():
            messagebox.showerror("Error", "La capacidad debe ser un número.")
            return
        capacidad_num = int(capacidad)

        if capacidad_num <= 0:
            messagebox.showerror("Error", "La capacidad debe ser mayor a cero.")
            return
        
        try:
            precio_num = float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return
        
        if precio_num <= 0:
            messagebox.showerror("Error", "El precio debe ser mayor a cero.")
            return

        # Buscar y actualizar la cancha existente
        encontrada = False
        for cancha in canchas:
            if cancha["id"] == id_cancha:
                cancha["capacidad"] = capacidad_num
                cancha["tipo"] = tipo
                cancha["precio"] = precio_num
                cancha["estado"] = estado
                encontrada = True
                break

        if not encontrada:
            messagebox.showerror("Error", "No se encontró una cancha con ese ID.")
            return

        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Éxito", "Cancha modificada correctamente.")

    def buscar():
        id_cancha = entrada_id.get().strip()

        for cancha in canchas:
            if cancha["id"] == id_cancha:
                entrada_capacidad.delete(0, tk.END)
                entrada_capacidad.insert(0, cancha["capacidad"])

                entrada_tipo.set(cancha["tipo"])

                entrada_precio.delete(0, tk.END)
                entrada_precio.insert(0, cancha["precio"])

                entrada_estado.set(cancha["estado"])

                return

        messagebox.showinfo(
            "Buscar", "No se encontró una cancha con ese ID."
        )

    # Función para autorrellenar los campos al hacer clic en la tabla
    def seleccionar_registro(event):
        seleccion = tabla.selection()
        if seleccion:
            item = tabla.item(seleccion)
            valores = item["values"]
            if valores:
                # Limpiamos y rellenamos los campos con los valores de la fila seleccionada
                limpiar()
                entrada_id.insert(0, str(valores[0]))
                entrada_id.config(state="disabled") # Bloquear ID para que no se altere la clave primaria al modificar
                
                entrada_capacidad.insert(0, str(valores[1]))
                entrada_tipo.set(str(valores[2]))
                entrada_precio.insert(0, str(valores[3]))
                entrada_estado.set(str(valores[4]))

    # Vincular el evento de selección de la tabla
    tabla.bind("<<TreeviewSelect>>", seleccionar_registro)

    # Bloque de botones
    botones = tk.Frame(panel_der, pady=10, bg="#f0f0f0")
    botones.pack(fill=tk.X)

    tk.Button(
        botones, text="Guardar", command=guardar, width=12
    ).pack(pady=2)

    tk.Button(
        botones, text="Modificar", command=modificar, width=12
    ).pack(pady=2)

    tk.Button(
        botones, text="Buscar", command=buscar, width=12
    ).pack(pady=2)

    tk.Button(
        botones, text="Limpiar", command=limpiar, width=12
    ).pack(pady=2)

    limpiar()
    actualizar_tabla()

    if parent is not None:
        parent.configure(bg="#f0f0f0")
        parent.pack(fill=tk.BOTH, expand=True)
    return ventana