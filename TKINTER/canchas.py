import tkinter as tk
from tkinter import messagebox, ttk

canchas = []

def ventana_canchas(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Gestión de Canchas")
        ventana.geometry("1280x720")

    titulo = tk.Label(
        ventana, text="GESTIÓN DE CANCHAS", font=("Arial", 20)
    )
    titulo.pack(pady=20)

    # Contenedor superior (contiene formulario y botones)
    contenedor_superior = tk.LabelFrame(ventana)
    contenedor_superior.pack(anchor="w", padx=20, pady=10)

    # Formulario
    formulario = tk.Frame(contenedor_superior)
    formulario.pack(side="left", padx=(0, 20))

    tk.Label(formulario, text="ID Cancha:").grid(
        row=0, column=0, padx=10, pady=5, sticky="w"
    )
    entrada_id = tk.Entry(formulario)
    entrada_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Capacidad:").grid(
        row=1, column=0, padx=10, pady=5, sticky="w"
    )
    entrada_capacidad = tk.Entry(formulario)
    entrada_capacidad.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Tipo:").grid(
        row=2, column=0, padx=10, pady=5, sticky="w"
    )
    entrada_tipo = ttk.Combobox(
        formulario, values=["Pádel", "Fútbol"], state="readonly"
    )
    entrada_tipo.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Precio por hora:").grid(
        row=3, column=0, padx=10, pady=5, sticky="w"
    )
    entrada_precio = tk.Entry(formulario)
    entrada_precio.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Estado:").grid(
        row=4, column=0, padx=10, pady=5, sticky="w"
    )
    entrada_estado = ttk.Combobox(
        formulario, values=["Activa", "Inactiva"], state="readonly"
    )
    entrada_estado.grid(row=4, column=1, padx=10, pady=5)
    entrada_estado.set("Activa")

    # Funciones internas
    def limpiar():
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

        #capacidad_num=int(capacidad) #para validar q sea !=0
        precio=precio.replace(",", ".") #reemplazar coma por punto

        # Validacion para que todos los campos sean obligatorios
        if not id_cancha or not capacidad or not tipo or not precio or not estado:
            messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios.")
            return
        
        if not id_cancha.isdigit(): #validar id sea integer
            messagebox.showerror(
                "Error", 
                "El ID de cancha de ser un número."
            )
            return

        if not capacidad.isdigit(): #validar capac sea integer
            messagebox.showerror(
                "Error",
                "La capacidad debe ser un número."
            )
            return
        capacidad_num=int(capacidad) #para validar q sea !=0

        if capacidad_num <= 0: #validar sea != 0
            messagebox.showerror(
                "Error",
                "La capacidad deber ser mayor a cero."
            )
            return
        
        try:                    #precio_hora admite decimales?
            precio_num= float(precio)
        except ValueError:
            messagebox.showerror(
                "Error",
                "El precio debe ser un número válido."
            )
            return
        
        if precio_num <=0:
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

        canchas.append({ #guardar datos e
            "id": id_cancha,
            "capacidad": capacidad,
            "tipo": tipo,
            "precio": precio_num,
            "estado": estado,
        })

        actualizar_tabla()
        limpiar()

        messagebox.showinfo("Cancha", "Cancha guardada correctamente.")

    def buscar():
        id_cancha = entrada_id.get()

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

    # Bloque de botones
    botones = tk.Frame(contenedor_superior)
    botones.pack(side="left", anchor="n", padx=10)

    tk.Button(
        botones, text="Nuevo", command=limpiar, width=12
    ).pack(pady=5)

    tk.Button(
        botones, text="Guardar", command=guardar, width=12
    ).pack(pady=5)

    tk.Button(
        botones, text="Buscar", command=buscar, width=12
    ).pack(pady=5)

    # Tabla
    tabla = ttk.Treeview(
        ventana,
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

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    limpiar()
    actualizar_tabla()

