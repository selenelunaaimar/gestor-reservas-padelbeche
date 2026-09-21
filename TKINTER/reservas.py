from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Importamos clientes si se utiliza el modulo externo, de lo contrario se deja una lista base
try:
    from clientes import clientes
except ImportError:
    clientes = []

reservas = [
    {
         "id": "1",
         "cliente": "12345678",
         "cancha": "1",
         "fecha": "2026-09-25",
         "inicio": "10:00",
         "fin": "11:00",
         "estado": "Confirmada",
     }
]


def ventana_reservas(parent=None):
    # ventana principal o Toplevel
    ventana = parent or tk.Toplevel()

    if parent is None:
        ventana.title("Gestión de Reservas")
        ventana.geometry("1280x720")

    # Titulo principal
    titulo = tk.Label(
        ventana, text="Gestión de Reservas", font=("Arial", 20, "bold")
    )
    titulo.pack(pady=(15, 10))

    # Contenedor principal que divide la interfaz en dos columnas
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # =========================
    # PANEL IZQUIERDO: Tabla de Resultados
    # =========================
    panel_izq = tk.Frame(contenedor, padx=5, pady=5)
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Columnas para mostrar la info completa
    columnas = (
        "id",
        "Cliente",
        "Nombre",
        "Cancha",
        "Fecha",
        "Inicio",
        "Fin",
        "Estado",
    )
    tabla = ttk.Treeview(panel_izq, columns=columnas, show="headings")

    tabla.heading("id", text="ID Reserva")
    tabla.heading("Cliente", text="DNI Cliente")
    tabla.heading("Nombre", text="Nombre y Apellido")
    tabla.heading("Cancha", text="Cancha")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Inicio", text="Hora Inicio")
    tabla.heading("Fin", text="Hora Fin")
    tabla.heading("Estado", text="Estado")

    tabla.column("id", width=80)
    tabla.column("Cliente", width=90)
    tabla.column("Nombre", width=140)
    tabla.column("Cancha", width=70)
    tabla.column("Fecha", width=90)
    tabla.column("Inicio", width=80)
    tabla.column("Fin", width=80)
    tabla.column("Estado", width=90)

    tabla.pack(fill=tk.BOTH, expand=True)

    # =========================
    # PANEL DERECHO: Formulario y Botones
    # =========================
    panel_der = tk.Frame(contenedor, padx=10, pady=5)
    panel_der.pack(side=tk.RIGHT, fill=tk.Y)

    # ID Reserva
    tk.Label(panel_der, text="ID Reserva:").pack(anchor="w")
    entrada_id = tk.Entry(panel_der)
    entrada_id.pack(fill=tk.X, pady=2)

    # DNI Cliente
    tk.Label(panel_der, text="DNI Cliente:").pack(anchor="w")
    entrada_cliente = tk.Entry(panel_der)
    entrada_cliente.pack(fill=tk.X, pady=2)

    # Campo visual para mostrar el nombre del cliente automaticamente al escribir el DNI
    tk.Label(panel_der, text="Nombre y Apellido:").pack(anchor="w")
    entrada_nombre_cliente = tk.Entry(
        panel_der, state="readonly", fg="navy"
    )
    entrada_nombre_cliente.pack(fill=tk.X, pady=2)

    # =========================
    # FUNCIONES DE APOYO Y LÓGICA
    # =========================

    def buscar_nombre_cliente(dni):
        """Busca en la lista de clientes y retorna el nombre y apellido directamente."""
        for c in clientes:
            if str(c.get("dni")) == str(dni):
                return c.get("nombre_apellido", "Desconocido")
        return "No registrado"

    def actualizar_campo_nombre(event=None):
        dni = entrada_cliente.get().strip()
        entrada_nombre_cliente.config(state="normal")
        entrada_nombre_cliente.delete(0, tk.END)
        if not dni:
            entrada_nombre_cliente.insert(0, "Ingrese DNI")
        else:
            nombre = buscar_nombre_cliente(dni)
            entrada_nombre_cliente.insert(0, nombre)
        entrada_nombre_cliente.config(state="readonly")

    # Enlazamos el campo DNI para que actualice el nombre en tiempo real
    entrada_cliente.bind("<KeyRelease>", actualizar_campo_nombre)

    # Cancha
    tk.Label(panel_der, text="ID Cancha:").pack(anchor="w")
    entrada_cancha = tk.Entry(panel_der)
    entrada_cancha.pack(fill=tk.X, pady=2)

    # Fecha
    tk.Label(panel_der, text="Fecha (AAAA-MM-DD):").pack(anchor="w")
    entrada_fecha = tk.Entry(panel_der)
    entrada_fecha.pack(fill=tk.X, pady=2)

    # Hora inicio
    tk.Label(panel_der, text="Hora inicio (HH:MM):").pack(anchor="w")
    entrada_inicio = tk.Entry(panel_der)
    entrada_inicio.pack(fill=tk.X, pady=2)

    # Hora fin
    tk.Label(panel_der, text="Hora fin (HH:MM):").pack(anchor="w")
    entrada_fin = tk.Entry(panel_der)
    entrada_fin.pack(fill=tk.X, pady=2)

    # Estado
    tk.Label(panel_der, text="Estado:").pack(anchor="w")
    entrada_estado = ttk.Combobox(
        panel_der,
        values=["Confirmada", "Pendiente", "Cancelada"],
        state="readonly",
    )
    entrada_estado.pack(fill=tk.X, pady=2)
    entrada_estado.set("Pendiente")

    def limpiar():
        entrada_id.delete(0, tk.END)
        entrada_cliente.delete(0, tk.END)
        entrada_cancha.delete(0, tk.END)
        entrada_fecha.delete(0, tk.END)
        entrada_inicio.delete(0, tk.END)
        entrada_fin.delete(0, tk.END)
        entrada_estado.set("Pendiente")

        # Limpiamos también el campo auxiliar del nombre
        entrada_nombre_cliente.config(state="normal")
        entrada_nombre_cliente.delete(0, tk.END)
        entrada_nombre_cliente.insert(0, "Ingrese DNI")
        entrada_nombre_cliente.config(state="readonly")

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

        for reserva in reservas:
            nombre_cliente = buscar_nombre_cliente(reserva["cliente"])
            tabla.insert(
                "",
                tk.END,
                values=(
                    reserva["id"],
                    reserva["cliente"],
                    nombre_cliente,
                    reserva["cancha"],
                    reserva["fecha"],
                    reserva["inicio"],
                    reserva["fin"],
                    reserva["estado"],
                ),
            )

    def convertir_hora(hora):
        try:
            return datetime.strptime(hora, "%H:%M")
        except ValueError:
            return None

    def validar_fecha(fecha_str):
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def existe_superposicion(cancha, fecha, inicio, fin, id_excluir=None):
        # 'id_excluir' permite que la funcion Modificar ignore la reserva actual al verificar si la cancha se cruza consigo misma
        inicio_nuevo = convertir_hora(inicio)
        fin_nuevo = convertir_hora(fin)

        if inicio_nuevo is None or fin_nuevo is None:
            return True

        for reserva in reservas:
            if reserva["estado"] == "Cancelada":
                continue

            # Si estamos modificando, saltamos el registro que posee el mismo ID
            if id_excluir and str(reserva["id"]) == str(id_excluir):
                continue

            if (
                str(reserva["cancha"]) == str(cancha)
                and reserva["fecha"] == fecha
            ):
                inicio_existente = convertir_hora(reserva["inicio"])
                fin_existente = convertir_hora(reserva["fin"])

                if (
                    inicio_nuevo < fin_existente
                    and fin_nuevo > inicio_existente
                ):
                    return True

        return False

    def guardar():
        id_reserva = entrada_id.get().strip()
        cliente = entrada_cliente.get().strip()
        cancha = entrada_cancha.get().strip()
        fecha = entrada_fecha.get().strip()
        inicio = entrada_inicio.get().strip()
        fin = entrada_fin.get().strip()
        estado = entrada_estado.get().strip()

        # Validación de campos obligatorios
        if (
            not id_reserva
            or not cliente
            or not cancha
            or not fecha
            or not inicio
            or not fin
            or not estado
        ):
            messagebox.showwarning(
                "Datos incompletos", "Complete todos los campos obligatorios."
            )
            return

        # Validación de fecha
        if not validar_fecha(fecha):
            messagebox.showerror(
                "Error de formato",
                "La fecha debe tener el formato AAAA-MM-DD (ej: 2026-09-25).",
            )
            return

        # Validación ID reserva
        if not id_reserva.isdigit():
            messagebox.showerror("Error", "El ID de reserva debe ser un número.")
            return

        # Validación DNI
        if not cliente.isdigit():
            messagebox.showerror(
                "Error", "El DNI del cliente debe contener solamente números."
            )
            return

        if len(cliente) < 7 or len(cliente) > 8:
            messagebox.showerror(
                "Error", "El DNI del cliente debe tener entre 7 y 8 dígitos."
            )
            return

        # Validación cancha
        if not cancha.isdigit():
            messagebox.showerror(
                "Error", "El ID de la cancha debe ser un número."
            )
            return

        cancha_num = int(cancha)
        if cancha_num <= 0:
            messagebox.showerror(
                "Error", "El ID de la cancha debe ser mayor a cero."
            )
            return

        # Validación de horas
        inicio_nuevo = convertir_hora(inicio)
        fin_nuevo = convertir_hora(fin)

        if inicio_nuevo is None or fin_nuevo is None:
            messagebox.showerror(
                "Error", "Las horas deben tener el formato HH:MM."
            )
            return

        if inicio_nuevo >= fin_nuevo:
            messagebox.showerror(
                "Error",
                "La hora de inicio debe ser menor que la hora de fin.",
            )
            return

        # Validación ID duplicado
        for reserva in reservas:
            if reserva["id"] == id_reserva:
                messagebox.showerror(
                    "Error", "Ya existe una reserva con ese ID."
                )
                return

        # Validación superposición
        if estado != "Cancelada":
            if existe_superposicion(cancha, fecha, inicio, fin):
                messagebox.showerror(
                    "Cancha ocupada",
                    "La cancha ya tiene una reserva en ese horario.",
                )
                return

        # Guardar reserva
        reservas.append({
            "id": id_reserva,
            "cliente": cliente,
            "cancha": cancha,
            "fecha": fecha,
            "inicio": inicio,
            "fin": fin,
            "estado": estado,
        })

        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Reserva", "Reserva guardada correctamente.")

    def modificar():
        id_reserva = entrada_id.get().strip()
        cliente = entrada_cliente.get().strip()
        cancha = entrada_cancha.get().strip()
        fecha = entrada_fecha.get().strip()
        inicio = entrada_inicio.get().strip()
        fin = entrada_fin.get().strip()
        estado = entrada_estado.get().strip()

        if not id_reserva:
            messagebox.showwarning(
                "Atención", "Ingrese el ID de la reserva a modificar."
            )
            return

        inicio_nuevo = convertir_hora(inicio)
        fin_nuevo = convertir_hora(fin)
        if inicio_nuevo and fin_nuevo and inicio_nuevo >= fin_nuevo:
            messagebox.showerror(
                "Error de Horario",
                "La hora de fin no puede ser menor o igual a la hora de inicio.",
            )
            return

        if estado != "Cancelada":
            if existe_superposicion(
                cancha, fecha, inicio, fin, id_excluir=id_reserva
            ):
                messagebox.showerror(
                    "Cancha ocupada",
                    "La cancha ya se encuentra reservada en ese horario por otra reserva.",
                )
                return

        for r in reservas:
            if r["id"] == id_reserva:
                r["cliente"] = cliente
                r["cancha"] = cancha
                r["fecha"] = fecha
                r["inicio"] = inicio
                r["fin"] = fin
                r["estado"] = estado
                actualizar_tabla()
                limpiar()
                messagebox.showinfo(
                    "Éxito", "Reserva modificada correctamente."
                )
                return

        messagebox.showwarning(
            "Modificar", "No se encontró una reserva con ese ID."
        )

    def buscar():
        id_reserva = entrada_id.get().strip()

        for reserva in reservas:
            if reserva["id"] == id_reserva:
                limpiar()
                entrada_id.insert(0, reserva["id"])
                entrada_cliente.insert(0, reserva["cliente"])
                actualizar_campo_nombre()
                entrada_cancha.insert(0, reserva["cancha"])
                entrada_fecha.insert(0, reserva["fecha"])
                entrada_inicio.insert(0, reserva["inicio"])
                entrada_fin.insert(0, reserva["fin"])
                entrada_estado.set(reserva["estado"])
                return

        messagebox.showinfo("Buscar", "No se encontró la reserva.")

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Eliminar", "Debe seleccionar una reserva de la tabla."
            )
            return

        item = tabla.item(seleccion[0])
        id_reserva = str(item["values"][0])

        if not messagebox.askyesno(
            "Eliminar",
            f"¿Está seguro de eliminar la reserva con ID {id_reserva}?",
        ):
            return

        global reservas
        reservas = [
            reserva
            for reserva in reservas
            if str(reserva["id"]) != str(id_reserva)
        ]

        actualizar_tabla()
        limpiar()
        messagebox.showinfo("Éxito", "Reserva eliminada correctamente.")

    def seleccionar_tabla(event):
        # Permite cargar de forma automatica los datos en el formulario al hacer clic sobre una fila de la tabla
        seleccion = tabla.selection()
        if seleccion:
            item = tabla.item(seleccion[0])
            valores = item["values"]
            limpiar()
            entrada_id.insert(0, valores[0])
            entrada_cliente.insert(0, valores[1])
            actualizar_campo_nombre()
            entrada_cancha.insert(0, valores[3])
            entrada_fecha.insert(0, valores[4])
            entrada_inicio.insert(0, valores[5])
            entrada_fin.insert(0, valores[6])
            entrada_estado.set(valores[7])

    tabla.bind("<<TreeviewSelect>>", seleccionar_tabla)

    # Bloque de botones
    botones = tk.Frame(panel_der, pady=10)
    botones.pack(fill=tk.X)

    tk.Button(
        botones, text="Guardar", command=guardar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Modificar", command=modificar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Eliminar", command=eliminar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Buscar", command=buscar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Limpiar", command=limpiar, width=15
    ).pack(pady=3)

    # Inicialización de vistas
    actualizar_campo_nombre()
    actualizar_tabla()

    # Si se pasa un contenedor padre (parent), empaqueta y retorna la ventana principal
    if parent is not None:
        ventana.pack(fill=tk.BOTH, expand=True)
    return ventana