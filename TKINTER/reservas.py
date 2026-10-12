import mysql.connector
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk
from BASE_DE_DATOS.database import obtener_conexion

"""Minutos que tiene el cliente para pagar una reserva Pendiente"""
MINUTOS_PAGO = 15

def ventana_reservas(parent=None):
    """ventana principal o Toplevel"""
    ventana = parent or tk.Toplevel()

    if parent is None:
        ventana.title("Gestión de Reservas")
        ventana.geometry("1280x720")

    """Titulo principal"""
    titulo = tk.Label(
        ventana, text="Gestión de Reservas", font=("Arial", 20, "bold")
    )
    titulo.pack(pady=(15, 10))

    """Cartel de alerta por pagos vencidos"""
    lbl_alerta = tk.Label(
        ventana, text="", font=("Arial", 11, "bold"), fg="#842029"
    )
    lbl_alerta.pack()

    """Contenedor principal que divide la interfaz en dos columnas"""
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    """=========================PANEL IZQUIERDO: Tabla de Resultados========================="""
    panel_izq = tk.Frame(contenedor, padx=5, pady=5)
    panel_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    """Columnas para mostrar la info completa"""
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

    """Estilo para reservas pendientes con el plazo de pago vencido"""
    tabla.tag_configure("vencida", background="#f8d7da", foreground="#842029")

    """=========================PANEL DERECHO: Formulario y Botones========================="""
    panel_der = tk.Frame(contenedor, padx=10, pady=5)
    panel_der.pack(side=tk.RIGHT, fill=tk.Y)

    """ID Reserva"""
    tk.Label(panel_der, text="ID Reserva:").pack(anchor="w")
    entrada_id = tk.Entry(panel_der)
    entrada_id.pack(fill=tk.X, pady=2)

    """DNI Cliente"""
    tk.Label(panel_der, text="DNI Cliente:").pack(anchor="w")
    entrada_cliente = tk.Entry(panel_der)
    entrada_cliente.pack(fill=tk.X, pady=2)

    """Campo visual para mostrar el nombre del cliente automaticamente al escribir el DNI"""
    tk.Label(panel_der, text="Nombre y Apellido:").pack(anchor="w")
    entrada_nombre_cliente = tk.Entry(
        panel_der, state="readonly", fg="navy"
    )
    entrada_nombre_cliente.pack(fill=tk.X, pady=2)

    """=========================FUNCIONES DE APOYO Y LÓGICA========================="""

    def buscar_nombre_cliente(dni):
        """Busca en la base de datos de clientes y retorna el nombre y apellido directamente"""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT nombre_apellido FROM clientes WHERE dni = %s", (dni,))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            if resultado:
                return resultado["nombre_apellido"]
        except Exception:
            pass
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

    """Enlaza el campo DNI para que actualice el nombre en tiempo real"""
    entrada_cliente.bind("<KeyRelease>", actualizar_campo_nombre)

    """Cancha"""
    tk.Label(panel_der, text="ID Cancha:").pack(anchor="w")
    entrada_cancha = tk.Entry(panel_der)
    entrada_cancha.pack(fill=tk.X, pady=2)

    """Fecha"""
    tk.Label(panel_der, text="Fecha (AAAA-MM-DD):").pack(anchor="w")
    entrada_fecha = tk.Entry(panel_der)
    entrada_fecha.pack(fill=tk.X, pady=2)

    """Hora inicio"""
    tk.Label(panel_der, text="Hora inicio (HH:MM):").pack(anchor="w")
    entrada_inicio = tk.Entry(panel_der)
    entrada_inicio.pack(fill=tk.X, pady=2)

    """Hora fin"""
    tk.Label(panel_der, text="Hora fin (HH:MM):").pack(anchor="w")
    entrada_fin = tk.Entry(panel_der)
    entrada_fin.pack(fill=tk.X, pady=2)

    """Estado"""
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

        """Limpiamos el campo auxiliar del nombre"""
        entrada_nombre_cliente.config(state="normal")
        entrada_nombre_cliente.delete(0, tk.END)
        entrada_nombre_cliente.insert(0, "Ingrese DNI")
        entrada_nombre_cliente.config(state="readonly")

    def actualizar_tabla():
        for item in tabla.get_children():
            tabla.delete(item)

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT r.id_reserva AS id, r.dni_cliente AS cliente, c.nombre_apellido AS nombre,
                       r.id_cancha AS cancha, r.fecha, TIME_FORMAT(r.hora_inicio, '%H:%i') AS inicio,
                       TIME_FORMAT(r.hora_fin, '%H:%i') AS fin, r.estado_reserva AS estado
                FROM reservas r
                JOIN clientes c ON r.dni_cliente = c.dni
                ORDER BY r.fecha, r.hora_inicio
            """)
            lista_reservas = cursor.fetchall()
            cursor.close()
            conexion.close()

            for reserva in lista_reservas:
                fecha_str = reserva["fecha"].strftime("%Y-%m-%d") if hasattr(reserva["fecha"], "strftime") else str(reserva["fecha"])
                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        reserva["id"],
                        reserva["cliente"],
                        reserva["nombre"],
                        reserva["cancha"],
                        fecha_str,
                        reserva["inicio"],
                        reserva["fin"],
                        reserva["estado"],
                    ),
                )
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo cargar la tabla: {e}")

        """Vuelve a resaltar las reservas con pago vencido"""
        verificar_vencidas()

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
        """'id_excluir' permite que la funcion Modificar ignore la reserva actual al verificar si la cancha se cruza consigo misma"""
        inicio_nuevo = convertir_hora(inicio)
        fin_nuevo = convertir_hora(fin)

        if inicio_nuevo is None or fin_nuevo is None:
            return True

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_reserva AS id, id_cancha AS cancha, fecha,
                       TIME_FORMAT(hora_inicio, '%H:%i') AS inicio,
                       TIME_FORMAT(hora_fin, '%H:%i') AS fin, estado_reserva AS estado
                FROM reservas
                WHERE id_cancha = %s AND fecha = %s AND estado_reserva != 'Cancelada'
            """, (cancha, fecha))
            registros = cursor.fetchall()
            cursor.close()
            conexion.close()

            for reserva in registros:
                """Si estamos modificando, saltamos el registro que posee el mismo ID"""
                if id_excluir and str(reserva["id"]) == str(id_excluir):
                    continue

                inicio_existente = convertir_hora(reserva["inicio"])
                fin_existente = convertir_hora(reserva["fin"])

                if (
                    inicio_nuevo < fin_existente
                    and fin_nuevo > inicio_existente
                ):
                    return True
        except Exception:
            pass

        return False

    def calcular_vencimiento():
        """El cliente tiene MINUTOS_PAGO minutos desde que se hace la reserva."""
        return datetime.now() + timedelta(minutes=MINUTOS_PAGO)

    def obtener_id_libre():
        """Devuelve el menor ID de reserva que no este en uso (reutiliza huecos)."""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_reserva FROM reservas ORDER BY id_reserva")
        ids_usados = {fila[0] for fila in cursor.fetchall()}
        cursor.close()
        conexion.close()

        id_libre = 1
        while id_libre in ids_usados:
            id_libre += 1
        return id_libre

    def obtener_estado_cancha(id_cancha):
        """Devuelve 'Activa', 'Inactiva' o None si la cancha no existe."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                "SELECT estado FROM canchas WHERE id_cancha = %s", (id_cancha,)
            )
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()
            return resultado["estado"] if resultado else None
        except Exception:
            return None

    def validar_formulario(requiere_id):
        """
        Lee y valida los campos del formulario.
        Devuelve un diccionario con los datos limpios, o None si hay error
        (en ese caso ya mostro el mensaje al usuario).
        """
        id_reserva = entrada_id.get().strip()
        cliente = entrada_cliente.get().strip()
        cancha = entrada_cancha.get().strip()
        fecha = entrada_fecha.get().strip()
        inicio = entrada_inicio.get().strip()
        fin = entrada_fin.get().strip()
        estado = entrada_estado.get().strip()

        if requiere_id:
            if not id_reserva:
                messagebox.showwarning(
                    "Atención", "Ingrese el ID de la reserva a modificar."
                )
                return None
            if not id_reserva.isdigit():
                messagebox.showerror("Error", "El ID de reserva debe ser un número.")
                return None

        if not (cliente and cancha and fecha and inicio and fin and estado):
            messagebox.showwarning(
                "Datos incompletos", "Complete todos los campos obligatorios."
            )
            return None

        if not cliente.isdigit():
            messagebox.showerror(
                "Error", "El DNI del cliente debe contener solamente números."
            )
            return None

        if len(cliente) < 7 or len(cliente) > 8:
            messagebox.showerror(
                "Error", "El DNI del cliente debe tener entre 7 y 8 dígitos."
            )
            return None

        if buscar_nombre_cliente(cliente) == "No registrado":
            messagebox.showerror(
                "Cliente inexistente",
                "No hay ningún cliente registrado con ese DNI.",
            )
            return None

        if not cancha.isdigit() or int(cancha) <= 0:
            messagebox.showerror(
                "Error", "El ID de la cancha debe ser un número mayor a cero."
            )
            return None

        if not validar_fecha(fecha):
            messagebox.showerror(
                "Error de formato",
                "La fecha debe tener el formato AAAA-MM-DD (ej: 2026-09-25).",
            )
            return None

        inicio_dt = convertir_hora(inicio)
        fin_dt = convertir_hora(fin)
        if inicio_dt is None or fin_dt is None:
            messagebox.showerror("Error", "Las horas deben tener el formato HH:MM.")
            return None

        if inicio_dt >= fin_dt:
            messagebox.showerror(
                "Error", "La hora de inicio debe ser menor que la hora de fin."
            )
            return None

        return {
            "id": id_reserva,
            "cliente": cliente,
            "cancha": int(cancha),
            "fecha": fecha,
            "inicio": inicio,
            "fin": fin,
            "estado": estado,
        }

    def guardar():
        datos = validar_formulario(requiere_id=False)
        if datos is None:
            return

        """Una reserva Pendiente necesita fecha de vencimiento"""
        vence = None
        if datos["estado"] == "Pendiente":
            vence = calcular_vencimiento()

        """Los triggers de MySQL validan cancha activa y superposicion"""
        try:
            id_libre = obtener_id_libre()
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                INSERT INTO reservas
                    (id_reserva, dni_cliente, id_cancha, fecha, hora_inicio,
                     hora_fin, estado_reserva, vence_pago)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    id_libre,
                    datos["cliente"],
                    datos["cancha"],
                    datos["fecha"],
                    datos["inicio"],
                    datos["fin"],
                    datos["estado"],
                    vence,
                ),
            )
            conexion.commit()
            cursor.close()
            conexion.close()

            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Reserva", "Reserva guardada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error en Base de Datos", f"No se pudo guardar: {err.msg}"
            )

    def modificar():
        datos = validar_formulario(requiere_id=True)
        if datos is None:
            return

        """Traemos la reserva actual para saber su estado, cancha y vencimiento"""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id_cancha, estado_reserva, vence_pago
                FROM reservas WHERE id_reserva = %s
                """,
                (datos["id"],),
            )
            actual = cursor.fetchone()
            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error en Base de Datos", f"No se pudo consultar la reserva: {err.msg}"
            )
            return

        if actual is None:
            messagebox.showwarning("Modificar", "No se encontró una reserva con ese ID.")
            return

        if datos["estado"] != "Cancelada":
            """validamos la cancha activa (solo si cambia de cancha) y la superposicion."""
            if datos["cancha"] != actual["id_cancha"]:
                estado_cancha = obtener_estado_cancha(datos["cancha"])
                if estado_cancha is None:
                    messagebox.showerror("Error", "La cancha indicada no existe.")
                    return
                if estado_cancha != "Activa":
                    messagebox.showerror(
                        "Cancha inactiva",
                        "No se puede reservar una cancha inactiva.",
                    )
                    return

            if existe_superposicion(
                datos["cancha"],
                datos["fecha"],
                datos["inicio"],
                datos["fin"],
                id_excluir=datos["id"],
            ):
                messagebox.showerror(
                    "Cancha ocupada",
                    "La cancha ya se encuentra reservada en ese horario por otra reserva.",
                )
                return

        """Vencimiento: solo las Pendientes lo tienen. Si ya era Pendiente y conserva su vencimiento, se mantiene."""
        vence = None
        if datos["estado"] == "Pendiente":
            if actual["estado_reserva"] == "Pendiente" and actual["vence_pago"]:
                vence = actual["vence_pago"]
            else:
                vence = calcular_vencimiento()

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(
                """
                UPDATE reservas
                SET dni_cliente = %s, id_cancha = %s, fecha = %s,
                    hora_inicio = %s, hora_fin = %s,
                    estado_reserva = %s, vence_pago = %s
                WHERE id_reserva = %s
                """,
                (
                    datos["cliente"],
                    datos["cancha"],
                    datos["fecha"],
                    datos["inicio"],
                    datos["fin"],
                    datos["estado"],
                    vence,
                    datos["id"],
                ),
            )
            conexion.commit()
            cursor.close()
            conexion.close()

            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Reserva modificada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error en Base de Datos", f"No se pudo modificar: {err.msg}"
            )

    def buscar():
        id_reserva = entrada_id.get().strip()
        if not id_reserva:
            messagebox.showwarning("Atención", "Ingrese un ID de reserva para buscar.")
            return

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_reserva AS id, dni_cliente AS cliente, id_cancha AS cancha, fecha,
                       TIME_FORMAT(hora_inicio, '%H:%i') AS inicio,
                       TIME_FORMAT(hora_fin, '%H:%i') AS fin, estado_reserva AS estado
                FROM reservas WHERE id_reserva = %s
            """, (id_reserva,))
            reserva = cursor.fetchone()
            cursor.close()
            conexion.close()

            if reserva:
                limpiar()
                entrada_id.insert(0, reserva["id"])
                entrada_cliente.insert(0, reserva["cliente"])
                actualizar_campo_nombre()
                entrada_cancha.insert(0, reserva["cancha"])
                fecha_str = reserva["fecha"].strftime("%Y-%m-%d") if hasattr(reserva["fecha"], "strftime") else str(reserva["fecha"])
                entrada_fecha.insert(0, fecha_str)
                entrada_inicio.insert(0, reserva["inicio"])
                entrada_fin.insert(0, reserva["fin"])
                entrada_estado.set(reserva["estado"])
                return
        except Exception:
            pass

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

        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))
            conexion.commit()
            cursor.close()
            conexion.close()

            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Reserva eliminada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo eliminar: {err.msg}")

    def seleccionar_tabla(event):
        """Permite cargar de forma automatica los datos en el formulario al hacer clic sobre una fila de la tabla"""
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

    """=========================ALERTA DE PAGO VENCIDO========================="""
    avisadas = set()  # reservas por las que ya se mostro el aviso

    def verificar_vencidas():
        """Busca reservas Pendientes con el plazo de pago vencido,
        las resalta en la tabla y avisa una sola vez por cada una."""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("""
                SELECT r.id_reserva AS id, c.nombre_apellido AS nombre,
                       r.id_cancha AS cancha, r.fecha,
                       TIME_FORMAT(r.hora_inicio, '%H:%i') AS inicio,
                       r.vence_pago
                FROM reservas r
                JOIN clientes c ON r.dni_cliente = c.dni
                WHERE r.estado_reserva = 'Pendiente'
                ORDER BY r.vence_pago
            """)
            pendientes = cursor.fetchall()
            cursor.close()
            conexion.close()
        except Exception:
            return

        """La comparacion se hace en Python, con la misma hora con la que se calculo el vencimiento al guardar."""
        ahora = datetime.now()
        vencidas = [
            r for r in pendientes
            if r["vence_pago"] and r["vence_pago"] <= ahora
        ]
        ids_vencidas = {r["id"] for r in vencidas}

        """Resaltar filas sin reconstruir la tabla"""
        for fila in tabla.get_children():
            id_fila = int(tabla.item(fila)["values"][0])
            tabla.item(
                fila, tags=("vencida",) if id_fila in ids_vencidas else ()
            )

        """Cartel permanente mientras haya reservas vencidas"""
        if vencidas:
            lbl_alerta.config(
                text=f"⚠ {len(vencidas)} reserva(s) pendiente(s) con el plazo de pago vencido"
            )
        else:
            lbl_alerta.config(text="")

        """Aviso emergente: una sola vez por reserva"""
        nuevas = [r for r in vencidas if r["id"] not in avisadas]
        avisadas.intersection_update(ids_vencidas)  # olvida las ya resueltas
        if nuevas:
            avisadas.update(r["id"] for r in nuevas)
            detalle = "\n".join(
                f"• Reserva {r['id']} - {r['nombre']} - Cancha {r['cancha']} "
                f"- {r['fecha']} {r['inicio']}"
                for r in nuevas[:10]
            )
            messagebox.showwarning(
                "Pago vencido",
                f"Pasaron {MINUTOS_PAGO} minutos y estas reservas siguen "
                f"pendientes de pago:\n\n{detalle}\n\n"
                "Modificá su estado a Confirmada (si se recibió el pago) "
                "o a Cancelada (si no se pagó).",
                parent=ventana,
            )

    def ciclo_verificacion():
        """Revisa cada 30 segundos mientras esta pantalla este abierta."""
        if not ventana.winfo_exists():
            return
        verificar_vencidas()
        ventana.after(30000, ciclo_verificacion)

    """Bloque de botones"""
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

    """Inicialización de vistas"""
    actualizar_campo_nombre()
    actualizar_tabla()
    ciclo_verificacion()

    """Si se pasa un contenedor padre (parent), empaqueta y retorna la ventana principal"""
    if parent is not None:
        ventana.pack(fill=tk.BOTH, expand=True)
    return ventana