import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
import sesion
from .modelo_canchas import (
    obtener_canchas_db,
    insertar_cancha_db,
    actualizar_cancha_db,
    buscar_cancha_db
)


def ventana_canchas(parent=None):
    ventana = parent or tk.Toplevel()

    if parent is None:
        ventana.title("Gestión de Canchas")
        ventana.geometry("1280x720")
        ventana.configure(bg="#f0f0f0")

    # Verificar el rol del usuario que inició sesión.
    es_supervisor = sesion.rol_actual == "Supervisor"

    # Título principal de la ventana.
    titulo = tk.Label(
        ventana,
        text="Gestión de Canchas",
        font=("Arial", 20, "bold"),
        bg="#f0f0f0"
    )
    titulo.pack(pady=(15, 10))

    # Contenedor principal.
    contenedor = tk.Frame(ventana, bg="#f0f0f0")
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Panel izquierdo: tabla de canchas.
    panel_izq = tk.Frame(
        contenedor,
        padx=5,
        pady=5,
        bg="#f0f0f0"
    )
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    tabla = ttk.Treeview(
        panel_izq,
        columns=("id", "Capacidad", "Tipo", "Precio", "Estado"),
        show="headings"
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

    # Panel derecho: campos de información.
    panel_der = tk.Frame(
        contenedor,
        padx=5,
        pady=5,
        bg="#f0f0f0"
    )
    panel_der.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(
        panel_der,
        text="ID Cancha:",
        bg="#f0f0f0"
    ).pack(anchor="w")

    entrada_id = tk.Entry(panel_der)
    entrada_id.pack(fill=tk.X, pady=2)

    tk.Label(
        panel_der,
        text="Capacidad:",
        bg="#f0f0f0"
    ).pack(anchor="w")

    entrada_capacidad = tk.Entry(panel_der)
    entrada_capacidad.pack(fill=tk.X, pady=2)

    tk.Label(
        panel_der,
        text="Tipo:",
        bg="#f0f0f0"
    ).pack(anchor="w")

    entrada_tipo = ttk.Combobox(
        panel_der,
        values=["Padel", "Futbol"],
        state="readonly"
    )
    entrada_tipo.pack(fill=tk.X, pady=2)

    tk.Label(
        panel_der,
        text="Precio por hora:",
        bg="#f0f0f0"
    ).pack(anchor="w")

    entrada_precio = tk.Entry(panel_der)
    entrada_precio.pack(fill=tk.X, pady=2)

    tk.Label(
        panel_der,
        text="Estado:",
        bg="#f0f0f0"
    ).pack(anchor="w")

    entrada_estado = ttk.Combobox(
        panel_der,
        values=["Activa", "Inactiva"],
        state="readonly"
    )
    entrada_estado.pack(fill=tk.X, pady=2)
    entrada_estado.set("Activa")

    # Funciones internas.

    def limpiar():
        """Limpia los campos y permite seleccionar otra cancha."""

        entrada_id.config(state="normal")
        entrada_id.delete(0, tk.END)

        entrada_capacidad.delete(0, tk.END)
        entrada_tipo.set("")
        entrada_precio.delete(0, tk.END)
        entrada_estado.set("Activa")

        tabla.selection_remove(tabla.selection())

    def actualizar_tabla():
        """Carga las canchas registradas en la tabla."""

        for item in tabla.get_children():
            tabla.delete(item)

        try:
            lista_canchas = obtener_canchas_db()

            for cancha in lista_canchas:
                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        cancha["id"],
                        cancha["capacidad"],
                        cancha["tipo"],
                        cancha["precio"],
                        cancha["estado"]
                    )
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error",
                f"No se pudo cargar la tabla de canchas: {err}"
            )

    def guardar():
        """Registra una nueva cancha. Solo puede hacerlo el supervisor."""

        if sesion.rol_actual != "Supervisor":
            messagebox.showwarning(
                "Acceso denegado",
                "Solo el supervisor puede guardar nuevas canchas."
            )
            return

        id_cancha = entrada_id.get().strip()
        capacidad = entrada_capacidad.get().strip()
        tipo = entrada_tipo.get()
        precio = entrada_precio.get().strip()
        estado = entrada_estado.get()

        # Aceptar coma o punto como separador decimal.
        precio = precio.replace(",", ".")

        # Validar que todos los campos estén completos.
        if not all([id_cancha, capacidad, tipo, precio, estado]):
            messagebox.showwarning(
                "Datos incompletos",
                "Todos los campos son obligatorios."
            )
            return

        if not id_cancha.isdigit():
            messagebox.showerror(
                "Error",
                "El ID de cancha debe ser un número."
            )
            return

        if not capacidad.isdigit():
            messagebox.showerror(
                "Error",
                "La capacidad debe ser un número."
            )
            return

        capacidad_num = int(capacidad)

        if capacidad_num <= 0:
            messagebox.showerror(
                "Error",
                "La capacidad debe ser mayor a cero."
            )
            return

        try:
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

        try:
            insertar_cancha_db(
                int(id_cancha),
                tipo,
                capacidad_num,
                precio_num,
                estado
            )

            actualizar_tabla()
            limpiar()

            messagebox.showinfo(
                "Éxito",
                "Cancha guardada correctamente."
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error en Base de Datos",
                f"No se pudo guardar la cancha: {err}"
            )

    def buscar():
        """Busca una cancha por su identificador."""

        id_cancha = entrada_id.get().strip()

        if not id_cancha:
            messagebox.showwarning(
                "Campo vacío",
                "Por favor, ingrese el ID de la cancha que desea buscar."
            )
            return

        if not id_cancha.isdigit():
            messagebox.showerror(
                "Error",
                "El ID de cancha debe ser un número."
            )
            return

        try:
            cancha = buscar_cancha_db(int(id_cancha))

            if cancha:
                limpiar()

                entrada_id.insert(0, str(cancha["id"]))
                entrada_capacidad.insert(
                    0,
                    str(cancha["capacidad"])
                )
                entrada_tipo.set(cancha["tipo"])
                entrada_precio.insert(
                    0,
                    str(cancha["precio"])
                )
                entrada_estado.set(cancha["estado"])

                # El supervisor puede preparar la edición.
                # El empleado solo puede consultar los datos.
                if not es_supervisor:
                    entrada_id.config(state="disabled")
                    entrada_capacidad.config(state="readonly")
                    entrada_tipo.config(state="disabled")
                    entrada_precio.config(state="readonly")
                    entrada_estado.config(state="disabled")
                else:
                    entrada_id.config(state="disabled")

                messagebox.showinfo(
                    "Encontrado",
                    "Datos de la cancha cargados correctamente."
                )

            else:
                messagebox.showwarning(
                    "No encontrado",
                    "No existe ninguna cancha registrada con ese ID."
                )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error en Base de Datos",
                f"No se pudo realizar la búsqueda: {err}"
            )

    def modificar():
        """Modifica los datos de una cancha. Solo puede hacerlo el supervisor."""

        if sesion.rol_actual != "Supervisor":
            messagebox.showwarning(
                "Acceso denegado",
                "Solo el supervisor puede modificar las canchas."
            )
            return

        id_cancha = entrada_id.get().strip()
        capacidad = entrada_capacidad.get().strip()
        tipo = entrada_tipo.get()
        precio = entrada_precio.get().strip()
        estado = entrada_estado.get()

        precio = precio.replace(",", ".")

        if not all([id_cancha, capacidad, tipo, precio, estado]):
            messagebox.showwarning(
                "Datos incompletos",
                "Todos los campos son obligatorios para modificar."
            )
            return

        if not id_cancha.isdigit():
            messagebox.showerror(
                "Error",
                "El ID de cancha debe ser un número."
            )
            return

        if not capacidad.isdigit():
            messagebox.showerror(
                "Error",
                "La capacidad debe ser un número."
            )
            return

        capacidad_num = int(capacidad)

        if capacidad_num <= 0:
            messagebox.showerror(
                "Error",
                "La capacidad debe ser mayor a cero."
            )
            return

        try:
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

        try:
            filas = actualizar_cancha_db(
                tipo,
                capacidad_num,
                precio_num,
                estado,
                int(id_cancha)
            )

            if filas == 0:
                messagebox.showwarning(
                    "Sin cambios",
                    "No se encontró la cancha o los datos no cambiaron."
                )
                return

            actualizar_tabla()
            limpiar()

            messagebox.showinfo(
                "Éxito",
                "Cancha modificada correctamente."
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error en Base de Datos",
                f"No se pudo modificar la cancha: {err}"
            )

    def seleccionar_fila(event):
        """Carga los datos de la cancha seleccionada."""

        seleccion = tabla.selection()

        if not seleccion:
            return

        item = tabla.item(seleccion)
        valores = item["values"]

        limpiar()

        entrada_id.insert(0, str(valores[0]))
        entrada_capacidad.insert(0, str(valores[1]))
        entrada_tipo.set(valores[2])
        entrada_precio.insert(0, str(valores[3]))
        entrada_estado.set(valores[4])

        # Bloquear la edición de campos para el empleado.
        if not es_supervisor:
            entrada_id.config(state="disabled")
            entrada_capacidad.config(state="readonly")
            entrada_tipo.config(state="disabled")
            entrada_precio.config(state="readonly")
            entrada_estado.config(state="disabled")
        else:
            entrada_id.config(state="disabled")

    tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

    # Botones de acción.
    botones = tk.Frame(
        panel_der,
        pady=10,
        bg="#f0f0f0"
    )
    botones.pack(fill=tk.X)

    # Solo el supervisor puede guardar.
    if es_supervisor:
        tk.Button(
            botones,
            text="Guardar",
            command=guardar,
            width=15
        ).pack(pady=3)

    # Ambos roles pueden buscar.
    tk.Button(
        botones,
        text="Buscar",
        command=buscar,
        width=15
    ).pack(pady=3)

    # Solo el supervisor puede modificar.
    if es_supervisor:
        tk.Button(
            botones,
            text="Modificar",
            command=modificar,
            width=15
        ).pack(pady=3)

    # Ambos roles pueden limpiar.
    tk.Button(
        botones,
        text="Limpiar",
        command=limpiar,
        width=15
    ).pack(pady=3)

    # Cargar las canchas al abrir la pantalla.
    actualizar_tabla()

    if parent is not None:
        ventana.pack(fill=tk.BOTH, expand=True)

    return ventana