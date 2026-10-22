from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk
from .modelo_reservas import (
    obtener_canchas_activas_db,
    obtener_reservas_db,
    buscar_nombre_cliente_db,
    obtener_id_libre_db,
    insertar_reserva_db,
    actualizar_reserva_db,
    eliminar_reserva_db,
    obtener_pendientes_db
)
import sesion
import mysql.connector
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

    """----------------------------------PANEL IZQUIERDO: Tabla de Resultados--------------------------------------"""
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
    tabla.heading("Fecha", text="Fecha (DD/MM/AAAA)")
    tabla.heading("Inicio", text="Hora Inicio")
    tabla.heading("Fin", text="Hora Fin")
    tabla.heading("Estado", text="Estado")

    tabla.column("id", width=80)
    tabla.column("Cliente", width=90)
    tabla.column("Nombre", width=140)
    tabla.column("Cancha", width=110)
    tabla.column("Fecha", width=100)
    tabla.column("Inicio", width=80)
    tabla.column("Fin", width=80)
    tabla.column("Estado", width=90)

    tabla.pack(fill=tk.BOTH, expand=True)

    """Estilo para reservas pendientes con el plazo de pago vencido"""
    tabla.tag_configure("vencida", background="#f8d7da", foreground="#842029")

    """---------------------------------------PANEL DERECHO: Formulario y Botones--------------------------------------"""
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

    """-------------------------------------FUNCIONES DE APOYO Y LÓGICA----------------------------------------------"""

    def actualizar_campo_nombre(event=None):
        dni = entrada_cliente.get().strip()
        entrada_nombre_cliente.config(state="normal")
        entrada_nombre_cliente.delete(0, tk.END)
        if not dni:
            entrada_nombre_cliente.insert(0, "Ingrese DNI")
        else:
            try:
                nombre = buscar_nombre_cliente_db(dni)
                entrada_nombre_cliente.insert(
                    0,
                    nombre if nombre else "No registrado o dado de baja"
                )
            except (mysql.connector.Error, RuntimeError) as err:
                messagebox.showerror(
                    "Error de base de datos",
                    f"No se pudo validar el cliente: {err}"
                )
        entrada_nombre_cliente.config(state="readonly")

    """Enlaza el campo DNI para que actualice el nombre en tiempo real"""
    entrada_cliente.bind("<KeyRelease>", actualizar_campo_nombre)

    """Combobox de Canchas Activas"""
    tk.Label(panel_der, text="Cancha Activa:").pack(anchor="w")
    combo_cancha = ttk.Combobox(panel_der, state="readonly")
    combo_cancha.pack(fill=tk.X, pady=2)

    def cargar_canchas_activas():
        canchas = obtener_canchas_activas_db()
        mapeo = {f"ID {c['id_cancha']} - {c['tipo_deporte']} (Cap: {c['capacidad']})": c['id_cancha'] for c in canchas}
        combo_cancha['values'] = list(mapeo.keys())
        combo_cancha.mapeo_canchas = mapeo
        if mapeo:
            combo_cancha.current(0)

    cargar_canchas_activas()

    """Fecha en formato DD/MM/AAAA"""
    tk.Label(panel_der, text="Fecha (DD/MM/AAAA):").pack(anchor="w")
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
        if combo_cancha['values']:
            combo_cancha.current(0)
        entrada_fecha.delete(0, tk.END)
        entrada_inicio.delete(0, tk.END)
        entrada_fin.delete(0, tk.END)
        entrada_estado.set("Pendiente")

        """Limpiamos el campo auxiliar del nombre"""
        entrada_nombre_cliente.config(state="normal")
        entrada_nombre_cliente.delete(0, tk.END)
        entrada_nombre_cliente.insert(0, "Ingrese DNI")
        entrada_nombre_cliente.config(state="readonly")

    def convertir_fecha_a_bd(fecha_str):
        """Convierte de DD/MM/AAAA a AAAA-MM-DD para la base de datos"""
        try:
            dt = datetime.strptime(fecha_str.strip(), "%d/%m/%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def convertir_fecha_a_pantalla(fecha_db):
        """Convierte de AAAA-MM-DD a DD/MM/AAAA para mostrar en el formulario"""
        try:
            if hasattr(fecha_db, "strftime"):
                return fecha_db.strftime("%d/%m/%Y")
            partes = str(fecha_db).split("-")
            return f"{partes[2]}/{partes[1]}/{partes[0]}" if len(partes) == 3 else str(fecha_db)
        except Exception:
            return str(fecha_db)

    def actualizar_tabla():
        if not ventana.winfo_exists():
            return
        for item in tabla.get_children():
            tabla.delete(item)

        try:
            lista_reservas = obtener_reservas_db()

            for reserva in lista_reservas:
                fecha_mostrar = convertir_fecha_a_pantalla(reserva["fecha"])
                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        reserva["id"],
                        reserva["cliente"],
                        reserva["nombre"],
                        f"ID {reserva['cancha']}",
                        fecha_mostrar,
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

    def calcular_vencimiento():
        """El cliente tiene MINUTOS_PAGO minutos desde que se hace la reserva."""
        return datetime.now() + timedelta(minutes=MINUTOS_PAGO)

    def validar_formulario(requiere_id):
        """
        Lee y valida los campos del formulario.
        Devuelve un diccionario con los datos limpios, o None si hay error
        """
        id_reserva = entrada_id.get().strip()
        cliente = entrada_cliente.get().strip()
        seleccion_cancha = combo_cancha.get()
        fecha_usuario = entrada_fecha.get().strip()
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

        if not (cliente and seleccion_cancha and fecha_usuario and inicio and fin and estado):
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

        try:
            nombre_cliente = buscar_nombre_cliente_db(cliente)
        except (mysql.connector.Error, RuntimeError) as err:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudo validar el cliente: {err}"
            )
            return None

        if nombre_cliente is None:
            messagebox.showerror(
                "Cliente inexistente",
                "No hay ningún cliente activo con ese DNI.",
            )
            return None

        """Obtenemos el ID de la cancha seleccionada en el Combobox"""
        id_cancha_real = combo_cancha.mapeo_canchas.get(seleccion_cancha)
        if not id_cancha_real:
            messagebox.showerror("Error", "Seleccione una cancha activa válida.")
            return None

        """Validación y conversión de fecha DD/MM/AAAA a AAAA-MM-DD"""
        fecha_bd = convertir_fecha_a_bd(fecha_usuario)
        if not fecha_bd:
            messagebox.showerror(
                "Error de formato",
                "La fecha debe tener el formato DD/MM/AAAA (ej: 25/09/2026).",
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
            "cancha": id_cancha_real,
            "fecha": fecha_bd,
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

        """Los triggers de MySQL validan superposicion automaticamente"""
        try:
            id_libre = obtener_id_libre_db()
            insertar_reserva_db(
                id_libre,
                datos["cliente"],
                datos["cancha"],
                datos["fecha"],
                datos["inicio"],
                datos["fin"],
                datos["estado"],
                vence
            )

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

        """Traemos la reserva actual para saber su estado y vencimiento"""
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT estado_reserva, vence_pago
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

        """Vencimiento: solo las Pendientes lo tienen."""
        vence = None
        if datos["estado"] == "Pendiente":
            if actual["estado_reserva"] == "Pendiente" and actual["vence_pago"]:
                vence = actual["vence_pago"]
            else:
                vence = calcular_vencimiento()

        try:
            actualizar_reserva_db(
                datos["cliente"],
                datos["cancha"],
                datos["fecha"],
                datos["inicio"],
                datos["fin"],
                datos["estado"],
                vence,
                datos["id"]
            )

            actualizar_tabla()
            limpiar()
            messagebox.showinfo("Éxito", "Reserva modificada correctamente.")
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error en Base de Datos", f"No se pudo modificar: {err.msg}"
            )

    def buscar():
        id_reserva = entrada_id.get().strip()
        if not id_reserva or not id_reserva.isdigit():
            messagebox.showwarning("Atención", "Ingrese un ID numérico de reserva para buscar.")
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
                
                """Seleccionar la cancha en el combobox"""
                for idx, texto in enumerate(combo_cancha['values']):
                    if combo_cancha.mapeo_canchas[texto] == reserva["cancha"]:
                        combo_cancha.current(idx)
                        break

                entrada_fecha.insert(0, convertir_fecha_a_pantalla(reserva["fecha"]))
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
            eliminar_reserva_db(id_reserva)
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
            
            """Buscar la cancha correspondiente en el combobox según el ID mostrado"""
            cancha_texto_tabla = str(valores[3]) # ej: "ID 1"
            for idx, texto in enumerate(combo_cancha['values']):
                if cancha_texto_tabla in texto:
                    combo_cancha.current(idx)
                    break

            entrada_fecha.insert(0, valores[4])
            entrada_inicio.insert(0, valores[5])
            entrada_fin.insert(0, valores[6])
            entrada_estado.set(valores[7])

    tabla.bind("<<TreeviewSelect>>", seleccionar_tabla)

    """--------------------------------------------ALERTA DE PAGO VENCIDO---------------------------------------------"""
    avisadas = set()  # reservas por las que ya se mostro el aviso

    def verificar_vencidas():
        """Busca reservas Pendientes con el plazo de pago vencido,
        las resalta en la tabla y avisa una sola vez por cada una."""
        try:
            """Validar que tanto la ventana como la tabla sigan vivas antes de interactuar"""
            if not ventana.winfo_exists() or not tabla.winfo_exists():
                return
            
            pendientes = obtener_pendientes_db()
            if pendientes is None:
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
        except Exception:
            """Captura cualquier error de ciclo en segundo plano si la ventana se destruye"""
            pass

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
        botones, text="Buscar", command=buscar, width=15
    ).pack(pady=3)
    tk.Button(
        botones, text="Limpiar", command=limpiar, width=15
    ).pack(pady=3)
    if sesion.rol_actual == "Supervisor":
        tk.Button(
            botones, text="Eliminar", command=eliminar, width=15
        ).pack(pady=3)

    """Inicialización de vistas"""
    actualizar_campo_nombre()
    actualizar_tabla()
    ciclo_verificacion()

    """Si se pasa un contenedor padre (parent), empaqueta y retorna la ventana principal"""
    if parent is not None:
        ventana.pack(fill=tk.BOTH, expand=True)
    return ventana