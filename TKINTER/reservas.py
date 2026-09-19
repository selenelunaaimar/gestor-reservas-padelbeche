from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

reservas = []

def ventana_reservas(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Gestión de Reservas")
        ventana.geometry("1280x720")

    titulo = tk.Label(
        ventana, text="GESTIÓN DE RESERVAS", font=("Arial", 20)
    )
    titulo.pack(pady=20)

    # Contenedor superior para el formulario y botones
    contenedor_superior = tk.LabelFrame(ventana)
    contenedor_superior.pack(anchor="w", padx=20, pady=10)

    # Formulario
    formulario = tk.Frame(contenedor_superior)
    formulario.pack(side="left", padx=(0, 20))

    tk.Label(formulario, text="ID Reserva:").grid(
        row=0, column=0, padx=10, pady=5
    )
    entrada_id = tk.Entry(formulario)
    entrada_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Cliente:").grid(
        row=1, column=0, padx=10, pady=5
    )
    entrada_cliente = tk.Entry(formulario)
    entrada_cliente.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Cancha:").grid(
        row=2, column=0, padx=10, pady=5
    )
    entrada_cancha = tk.Entry(formulario)
    entrada_cancha.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Fecha (AAAA-MM-DD):").grid(
        row=3, column=0, padx=10, pady=5
    )
    entrada_fecha = tk.Entry(formulario)
    entrada_fecha.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Hora inicio:").grid(
        row=4, column=0, padx=10, pady=5
    )
    entrada_inicio = tk.Entry(formulario)
    entrada_inicio.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Hora fin:").grid(
        row=5, column=0, padx=10, pady=5
    )
    entrada_fin = tk.Entry(formulario)
    entrada_fin.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(formulario, text="Estado:").grid(
        row=6, column=0, padx=10, pady=5
    )
    entrada_estado = ttk.Combobox(
        formulario,
        values=["Confirmada", "Pendiente", "Cancelada"],
        state="readonly",
    )
    entrada_estado.grid(row=6, column=1, padx=10, pady=5)
    entrada_estado.set("Pendiente")

    # Funciones internas
    def limpiar():
        entrada_id.delete(0, tk.END)
        entrada_cliente.delete(0, tk.END)
        entrada_cancha.delete(0, tk.END)
        entrada_fecha.delete(0, tk.END)
        entrada_inicio.delete(0, tk.END)
        entrada_fin.delete(0, tk.END)
        entrada_estado.set("Pendiente")

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

        for reserva in reservas:
            tabla.insert(
                "",
                tk.END,
                values=(
                    reserva["id"],
                    reserva["cliente"],
                    reserva["cancha"],
                    reserva["fecha"],
                    reserva["inicio"],
                    reserva["fin"],
                    reserva["estado"],
                ),
            )

    def convertir_hora(hora):
        try:
            horas, minutos = hora.split(":")
            return int(horas) * 60 + int(minutos)
        except ValueError:
            return None

    def validar_fecha(fecha_str):
        try:
            # Valida el formato YYYY-MM-DD y que sea una fecha real
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def existe_superposicion(cancha, fecha, inicio, fin):
        inicio_nuevo = convertir_hora(inicio)
        fin_nuevo = convertir_hora(fin)

        if inicio_nuevo is None or fin_nuevo is None:
            return True

        for reserva in reservas:
            if reserva["estado"] == "Cancelada":
                continue

            if reserva["cancha"] == cancha and reserva["fecha"] == fecha:
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

        # Validacion para que todos los campos sean obligatorios
        if not id_reserva or not cliente or not cancha or not fecha or not inicio or not fin or not estado:
            messagebox.showwarning("Datos incompletos", "Complete todos los campos obligatorios.")
            return
        
        # Validacion estricta del formato de fecha
        if not validar_fecha(fecha):
            messagebox.showerror(
                "Error de formato",
                "La fecha debe tener el formato AAAA-MM-DD (ej: 2026-09-25).",
            )
            return

        if not id_reserva.isdigit(): #valida id sea integer
            messagebox.showerror(
                "Error", "El ID de reserva debe ser un número."
            )
            return

        if not cliente.isdigit(): #valida id cliente sea integer
            messagebox.showerror(
                "Error", "El ID del cliente debe ser un número."
            )
            return

        if len(cliente) < 7 or len(cliente) > 8: #valida la long del DNI
            messagebox.showerror(
                "Error", "El ID del cliente debe tener entre 7 y 8 dígitos."
            )
            return

        if not cancha.isdigit(): #valida id cancha sea integer
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

        for reserva in reservas:
            if reserva["id"] == id_reserva:
                messagebox.showerror(
                    "Error", "Ya existe una reserva con ese ID."
                )
                return

        if estado != "Cancelada":
            if existe_superposicion(cancha, fecha, inicio, fin):
                messagebox.showerror(
                    "Cancha ocupada",
                    "La cancha ya tiene una reserva en ese horario.",
                )
                return

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
    #fin guardar()

    def buscar():
        id_reserva = entrada_id.get().strip()

        for reserva in reservas:
            if reserva["id"] == id_reserva:
                entrada_cliente.delete(0, tk.END)
                entrada_cliente.insert(0, reserva["cliente"])

                entrada_cancha.delete(0, tk.END)
                entrada_cancha.insert(0, reserva["cancha"])

                entrada_fecha.delete(0, tk.END)
                entrada_fecha.insert(0, reserva["fecha"])

                entrada_inicio.delete(0, tk.END)
                entrada_inicio.insert(0, reserva["inicio"])

                entrada_fin.delete(0, tk.END)
                entrada_fin.insert(0, reserva["fin"])

                entrada_estado.set(reserva["estado"])
                return

        messagebox.showinfo("Buscar", "No se encontró la reserva.")

    # Bloque de botones, al lado del formulario, uno debajo del otro
    botones = tk.Frame(contenedor_superior)
    botones.pack(side="left", anchor="n", padx=10)

    tk.Button(
        botones, text="Limpiar", command=limpiar, width=12
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
        columns=(
            "id",
            "Cliente",
            "Cancha",
            "Fecha",
            "Inicio",
            "Fin",
            "Estado",
        ),
        show="headings",
    )

    tabla.heading("id", text="ID Reserva")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Cancha", text="Cancha")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Inicio", text="Hora Inicio")
    tabla.heading("Fin", text="Hora Fin")
    tabla.heading("Estado", text="Estado")

    tabla.column("id", width=100)
    tabla.column("Cliente", width=150)
    tabla.column("Cancha", width=100)
    tabla.column("Fecha", width=100)
    tabla.column("Inicio", width=100)
    tabla.column("Fin", width=100)
    tabla.column("Estado", width=100)

    tabla.pack(fill="both", expand=True, padx=20, pady=20)

    actualizar_tabla()