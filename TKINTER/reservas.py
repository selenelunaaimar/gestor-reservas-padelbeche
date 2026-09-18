import tkinter as tk
from tkinter import ttk, messagebox


reservas = []


def ventana_reservas(parent=None):
    ventana = parent or tk.Toplevel()
    if parent is None:
        ventana.title("Gestión de Reservas")
        ventana.geometry("1280x720")

    titulo = tk.Label(
        ventana,
        text="GESTIÓN DE RESERVAS",
        font=("Arial", 20)
    )
    titulo.pack(pady=20)

    # Formulario
    formulario = tk.LabelFrame(ventana)
    formulario.pack(fill="x",padx=20, pady=10)

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

    tk.Label(formulario, text="Fecha:").grid(
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
        state="readonly"
    )
    entrada_estado.grid(row=6, column=1, padx=10, pady=5)
    entrada_estado.set("Pendiente")

    # Tabla
    tabla = ttk.Treeview(
        ventana,
        columns=(
            "ID",
            "Cliente",
            "Cancha",
            "Fecha",
            "Inicio",
            "Fin",
            "Estado"
        ),
        show="headings"
    )

    tabla.heading("ID", text="ID Reserva")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Cancha", text="Cancha")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Inicio", text="Hora Inicio")
    tabla.heading("Fin", text="Hora Fin")
    tabla.heading("Estado", text="Estado")

    tabla.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

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
                    reserva["estado"]
                )
            )

    def convertir_hora(hora):
        try:
            horas, minutos = hora.split(":")
            return int(horas) * 60 + int(minutos)
        except ValueError:
            return None

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

                if inicio_nuevo < fin_existente and fin_nuevo > inicio_existente:
                    return True

        return False

    def guardar():
        id_reserva = entrada_id.get()
        cliente = entrada_cliente.get()
        cancha = entrada_cancha.get()
        fecha = entrada_fecha.get()
        inicio = entrada_inicio.get()
        fin = entrada_fin.get()
        estado = entrada_estado.get()

        if (
            id_reserva == ""
            or cliente == ""
            or cancha == ""
            or fecha == ""
            or inicio == ""
            or fin == ""
        ):
            messagebox.showwarning(
                "Datos incompletos",
                "Complete todos los campos obligatorios."
            )
            return

        inicio_nuevo = convertir_hora(inicio)
        fin_nuevo = convertir_hora(fin)

        if inicio_nuevo is None or fin_nuevo is None:
            messagebox.showerror(
                "Error",
                "Las horas deben tener el formato HH:MM."
            )
            return

        if inicio_nuevo >= fin_nuevo:
            messagebox.showerror(
                "Error",
                "La hora de inicio debe ser menor que la hora de fin."
            )
            return

        for reserva in reservas:
            if reserva["id"] == id_reserva:
                messagebox.showerror(
                    "Error",
                    "Ya existe una reserva con ese ID."
                )
                return

        if estado != "Cancelada":
            if existe_superposicion(
                cancha,
                fecha,
                inicio,
                fin
            ):
                messagebox.showerror(
                    "Cancha ocupada",
                    "La cancha ya tiene una reserva en ese horario."
                )
                return

        reservas.append({
            "id": id_reserva,
            "cliente": cliente,
            "cancha": cancha,
            "fecha": fecha,
            "inicio": inicio,
            "fin": fin,
            "estado": estado
        })

        actualizar_tabla()
        limpiar()

        messagebox.showinfo(
            "Reserva",
            "Reserva guardada correctamente."
        )

    def buscar():
        id_reserva = entrada_id.get()

        for reserva in reservas:

            if reserva["id"] == id_reserva:

                entrada_cliente.delete(0, tk.END)
                entrada_cliente.insert(
                    0,
                    reserva["cliente"]
                )

                entrada_cancha.delete(0, tk.END)
                entrada_cancha.insert(
                    0,
                    reserva["cancha"]
                )

                entrada_fecha.delete(0, tk.END)
                entrada_fecha.insert(
                    0,
                    reserva["fecha"]
                )

                entrada_inicio.delete(0, tk.END)
                entrada_inicio.insert(
                    0,
                    reserva["inicio"]
                )

                entrada_fin.delete(0, tk.END)
                entrada_fin.insert(
                    0,
                    reserva["fin"]
                )

                entrada_estado.set(
                    reserva["estado"]
                )

                return

        messagebox.showinfo(
            "Buscar",
            "No se encontró la reserva."
        )

    botones = tk.Frame(ventana)
    botones.pack(pady=10)

    tk.Button(
        botones,
        text="Nuevo",
        command=limpiar
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        botones,
        text="Guardar",
        command=guardar
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        botones,
        text="Buscar",
        command=buscar
    ).grid(row=0, column=2, padx=5)

    actualizar_tabla()