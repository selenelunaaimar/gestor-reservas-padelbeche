import tkinter as tk
from tkinter import ttk, messagebox
import re
import mysql.connector
import sesion

from .modelo_clientes import (
    obtener_clientes_db,
    insertar_cliente_db,
    actualizar_cliente_db,
    dar_de_baja_cliente_db,
    eliminar_cliente_sin_reservas_db,
    buscar_cliente_db
)


def ventana_clientes(parent=None):
    """Maneja la ventana de clientes, independiente o en solapas."""
    ventana = parent or tk.Toplevel()
    es_supervisor = sesion.rol_actual == "Supervisor"

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

    # Contenedor principal
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # PANEL IZQUIERDO: TABLA
    panel_izq = tk.Frame(contenedor, padx=5, pady=5)
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    columnas = ("DNI", "Nombre y Apellido", "Teléfono", "Email", "Estado")
    tabla = ttk.Treeview(
        panel_izq,
        columns=columnas,
        show="headings"
    )

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)

    tabla.pack(fill=tk.BOTH, expand=True)

    # PANEL DERECHO: FORMULARIO Y BOTONES
    panel_der = tk.Frame(contenedor, padx=10, pady=5)
    panel_der.pack(side=tk.RIGHT, fill=tk.Y)

    # Campos del formulario
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

    # FUNCIONES INTERNAS

    def limpiar():
        """Limpia los campos del formulario."""
        entrada_dni.delete(0, tk.END)
        entrada_nombre_apellido.delete(0, tk.END)
        entrada_telefono.delete(0, tk.END)
        entrada_email.delete(0, tk.END)

    def actualizar_tabla():
        """Consulta MySQL y carga los clientes en la tabla."""
        for item in tabla.get_children():
            tabla.delete(item)

        try:
            registros = obtener_clientes_db()

            for cliente in registros:
                estado = f"Baja: {cliente[4]}" if cliente[4] else "Activo"
                tabla.insert("", tk.END, values=(*cliente[:4], estado))

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error de Base de Datos",
                f"No se pudieron cargar los clientes: {err}"
            )

    def guardar():
        dni = entrada_dni.get().strip()
        nombre_apellido = entrada_nombre_apellido.get().strip()
        telefono = entrada_telefono.get().strip()
        email = entrada_email.get().strip()
        patron_email = r'^[\w.-]+@[\w.-]+\.\w+$'

        if not dni and not nombre_apellido and not telefono and not email:
            messagebox.showerror(
                "Datos incompletos",
                "Debe completar los datos del cliente."
            )
            return

        if not dni:
            messagebox.showwarning("Datos incompletos", "Debe ingresar DNI")
            return

        if not nombre_apellido:
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar nombre y apellido."
            )
            return

        if not telefono:
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar el teléfono."
            )
            return

        if not email:
            messagebox.showwarning(
                "Datos incompletos",
                "Debe ingresar email."
            )
            return

        # Validación de DNI
        if not dni.isdigit():
            messagebox.showerror("Error", "El DNI debe contener sólo números.")
            return

        if len(dni) < 7 or len(dni) > 8:
            messagebox.showerror(
                "Error",
                "El DNI debe tener entre 7 y 8 dígitos."
            )
            return

        # Validación de nombre
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre_apellido):
            messagebox.showerror("Error", "Ingrese un nombre válido.")
            return

        if len(nombre_apellido) < 3:
            messagebox.showerror(
                "Error",
                "El nombre debe tener al menos 3 caracteres."
            )
            return

        # Validación de teléfono
        if not telefono.isdigit():
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

        # Validación de email
        if not re.match(patron_email, email):
            messagebox.showerror("Error", "Debe ingresar un mail válido.")
            return

        try:
            insertar_cliente_db(
                dni,
                nombre_apellido,
                telefono,
                email
            )

            actualizar_tabla()
            limpiar()

            messagebox.showinfo(
                "Cliente",
                "Cliente guardado correctamente en la base de datos."
            )

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar (verificá que el DNI no esté repetido):\n{err}"
            )

    def modificar():
        """Modifica un cliente. Solo el Supervisor puede hacerlo."""
        if sesion.rol_actual != "Supervisor":
            messagebox.showerror(
                "Permiso denegado",
                "Solo Supervisor puede modificar clientes."
            )
            return

        dni = entrada_dni.get().strip()
        nombre_apellido = entrada_nombre_apellido.get().strip()
        telefono = entrada_telefono.get().strip()
        email = entrada_email.get().strip()
        patron_email = r'^[\w.-]+@[\w.-]+\.\w+$'

        if not dni:
            messagebox.showwarning(
                "Atención",
                "Ingrese o seleccione el DNI del cliente a modificar."
            )
            return

        if not nombre_apellido or not telefono or not email:
            messagebox.showwarning(
                "Datos incompletos",
                "Todos los campos deben estar completos para modificar."
            )
            return

        if (
            not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", nombre_apellido)
            or len(nombre_apellido) < 3
        ):
            messagebox.showerror(
                "Error",
                "Ingrese un nombre y apellido válido (mínimo 3 letras)."
            )
            return

        if not telefono.isdigit() or len(telefono) < 8 or len(telefono) > 15:
            messagebox.showerror(
                "Error",
                "El teléfono debe contener sólo números (entre 8 y 15 dígitos)."
            )
            return

        if not re.match(patron_email, email):
            messagebox.showerror("Error", "Debe ingresar un mail válido.")
            return

        try:
            filas_afectadas = actualizar_cliente_db(
                nombre_apellido,
                telefono,
                email,
                dni
            )

            if filas_afectadas > 0:
                actualizar_tabla()
                limpiar()
                messagebox.showinfo(
                    "Éxito",
                    "Cliente modificado correctamente."
                )
            else:
                messagebox.showwarning(
                    "Modificar",
                    "No se encontró un cliente registrado con ese DNI."
                )

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo modificar: {err}")

    def dar_de_baja():
        """Da de baja lógicamente a un cliente."""
        if sesion.rol_actual != "Supervisor":
            messagebox.showerror(
                "Permiso denegado",
                "Solo Supervisor puede dar de baja clientes."
            )
            return

        dni = entrada_dni.get().strip()

        if not dni:
            messagebox.showwarning(
                "Cliente",
                "Seleccione un cliente de la tabla primero."
            )
            return

        if not messagebox.askyesno(
            "Confirmar baja",
            f"¿Desea dar de baja al cliente con DNI {dni}?\n\n"
            "El cliente dejará de estar disponible para nuevas reservas. "
            "Sus reservas e historial se conservarán.",
            icon="warning"
        ):
            return

        try:
            filas = dar_de_baja_cliente_db(dni)

            if filas == 0:
                messagebox.showwarning(
                    "Cliente",
                    "No se encontró un cliente activo con ese DNI."
                )
                return

            actualizar_tabla()
            limpiar()

            messagebox.showinfo(
                "Cliente",
                "Cliente dado de baja. Sus reservas se conservaron."
            )

        except (mysql.connector.Error, RuntimeError) as err:
            messagebox.showerror("No se pudo dar de baja", f"{err}")

    def eliminar_definitivamente():
        """Elimina físicamente al cliente solo si no tiene reservas."""
        if sesion.rol_actual != "Supervisor":
            messagebox.showerror(
                "Permiso denegado",
                "Solo Supervisor puede eliminar clientes."
            )
            return

        dni = entrada_dni.get().strip()

        if not dni:
            messagebox.showwarning(
                "Cliente",
                "Seleccione un cliente de la tabla primero."
            )
            return

        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar al cliente con DNI {dni}?\n\n"
            "Solo se permite si no tiene reservas. Esta acción no se puede deshacer.",
            icon="warning"
        ):
            return

        try:
            resultado = eliminar_cliente_sin_reservas_db(dni)

            if resultado == "tiene_reservas":
                messagebox.showwarning(
                    "No se puede eliminar",
                    "El cliente tiene reservas asociadas. Use «Dar de baja» "
                    "para conservar su historial."
                )
                return

            if resultado == "no_encontrado":
                messagebox.showwarning(
                    "Cliente",
                    "No se encontró un cliente con ese DNI."
                )
                return

            actualizar_tabla()
            limpiar()

            messagebox.showinfo(
                "Cliente",
                "Cliente eliminado correctamente."
            )

        except (mysql.connector.Error, RuntimeError) as err:
            messagebox.showerror("No se pudo eliminar", f"{err}")

    def buscar():
        """Busca un registro por DNI y lo muestra en el formulario."""
        dni = entrada_dni.get().strip()

        if not dni:
            messagebox.showwarning("Buscar", "Ingrese un DNI para buscar.")
            return

        try:
            resultado = buscar_cliente_db(dni)

            if resultado:
                entrada_nombre_apellido.delete(0, tk.END)
                entrada_nombre_apellido.insert(0, resultado[0])

                entrada_telefono.delete(0, tk.END)
                entrada_telefono.insert(0, resultado[1])

                entrada_email.delete(0, tk.END)
                entrada_email.insert(0, resultado[2])

                if resultado[3]:
                    messagebox.showinfo(
                        "Cliente dado de baja",
                        f"Este cliente fue dado de baja el {resultado[3]}."
                    )
            else:
                messagebox.showinfo(
                    "Buscar",
                    "No se encontró un cliente con ese DNI."
                )

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al buscar: {err}")

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

    # Vinculación de la selección de la tabla
    tabla.bind("<<TreeviewSelect>>", seleccionar_tabla)

    # BLOQUE DE BOTONES
    botones = tk.Frame(panel_der, pady=10)
    botones.pack(fill=tk.X)

    tk.Button(
        botones,
        text="Guardar",
        command=guardar,
        width=15
    ).pack(pady=2)

    # Estos botones solo aparecen para el Supervisor
    if es_supervisor:
        tk.Button(
            botones,
            text="Modificar",
            command=modificar,
            width=15
        ).pack(pady=2)

        tk.Button(
            botones,
            text="Dar de baja",
            command=dar_de_baja,
            width=15
        ).pack(pady=2)

        tk.Button(
            botones,
            text="Eliminar",
            command=eliminar_definitivamente,
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
        text="Limpiar",
        command=limpiar,
        width=15
    ).pack(pady=2)

    # Carga inicial de datos
    actualizar_tabla()

    if parent is not None:
        ventana.pack(fill=tk.BOTH, expand=True)

    return ventana