import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from BASE_DE_DATOS.database import obtener_conexion

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
        panel_der, values=["Padel", "Futbol"], state="readonly"
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

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT id_cancha AS id, tipo_deporte AS tipo, capacidad, precio_hora AS precio, estado FROM canchas")
            lista_canchas = cursor.fetchall()
            cursor.close()
            conexion.close()

            for cancha in lista_canchas:
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
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la tabla de canchas: {e}")

    def guardar():
        id_cancha = entrada_id.get().strip()
        capacidad = entrada_capacidad.get().strip()
        tipo = entrada_tipo.get()
        precio = entrada_precio.get().strip()
        estado = entrada_estado.get()

        precio = precio.replace(",", ".") # reemplazar coma por punto

        if not id_cancha or not capacidad or not tipo or not precio or not estado:
            messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios.")
            return

        if not id_cancha.isdigit():
            messagebox.showerror("Error", "El ID de cancha debe ser un número.")
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
             
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            query = """
                INSERT INTO canchas (id_cancha, tipo_deporte, capacidad, precio_hora, estado)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_cancha, tipo, capacidad_num, precio_num, estado))
            conexion.commit()
            cursor.close()
            conexion.close()

            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Cancha guardada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error en Base de Datos", f"No se pudo guardar la cancha: {err.msg}")

    def buscar():
        id_cancha = entrada_id.get().strip()

        if not id_cancha:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese el ID de la cancha que desea buscar.")
            return

        if not id_cancha.isdigit():
            messagebox.showerror("Error", "El ID de cancha debe ser un número.")
            return

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT id_cancha AS id, tipo_deporte AS tipo, capacidad, precio_hora AS precio, estado FROM canchas WHERE id_cancha = %s"
            cursor.execute(query, (id_cancha,))
            cancha = cursor.fetchone()
            cursor.close()
            conexion.close()

            if cancha:
                entrada_capacidad.delete(0, tk.END)
                entrada_capacidad.insert(0, str(cancha["capacidad"]))
                entrada_tipo.set(cancha["tipo"])
                entrada_precio.delete(0, tk.END)
                entrada_precio.insert(0, str(cancha["precio"]))
                entrada_estado.set(cancha["estado"])
                
                # Bloquear el ID para evitar modificarlo por accidente durante la edición
                entrada_id.config(state="disabled")
                messagebox.showinfo("Encontrado", "Datos de la cancha cargados correctamente.")
            else:
                messagebox.showwarning("No encontrado", "No existe ninguna cancha registrada con ese ID.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error en Base de Datos", f"No se pudo realizar la búsqueda: {err.msg}")

    def modificar():
        # Si el ID estaba deshabilitado por haber buscado, lo habilitamos un momento para leerlo
        id_cancha = entrada_id.get().strip()
        capacidad = entrada_capacidad.get().strip()
        tipo = entrada_tipo.get()
        precio = entrada_precio.get().strip()
        estado = entrada_estado.get()

        precio = precio.replace(",", ".")

        if not id_cancha or not capacidad or not tipo or not precio or not estado:
            messagebox.showwarning("Datos incompletos", "Todos los campos son obligatorios para modificar.")
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

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            query = """
                UPDATE canchas 
                SET tipo_deporte = %s, capacidad = %s, precio_hora = %s, estado = %s 
                WHERE id_cancha = %s
            """
            cursor.execute(query, (tipo, capacidad_num, precio_num, estado, id_cancha))
            conexion.commit()
            cursor.close()
            conexion.close()

            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Cancha modificada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error en Base de Datos", f"No se pudo modificar la cancha: {err.msg}")

    # Función auxiliar para autocompletar campos al hacer clic en una fila de la tabla
    def seleccionar_fila(event):
        seleccion = tabla.selection()
        if seleccion:
            item = tabla.item(seleccion)
            valores = item['values']
            
            limpiar()
            entrada_id.insert(0, str(valores[0]))
            entrada_id.config(state="disabled") # Bloquear ID para edición segura
            entrada_capacidad.insert(0, str(valores[1]))
            entrada_tipo.set(valores[2])
            entrada_precio.insert(0, str(valores[3]))
            entrada_estado.set(valores[4])

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    # Botones de acción organizados en el panel derecho
    botones = tk.Frame(panel_der, pady=10, bg="#f0f0f0")
    botones.pack(fill=tk.X)

    tk.Button(
        botones, text="Guardar", command=guardar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Buscar", command=buscar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Modificar", command=modificar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Limpiar", command=limpiar, width=15
    ).pack(pady=3)

    actualizar_tabla()

    if parent is not None:
        ventana.pack(fill=tk.BOTH, expand=True)
    return ventana