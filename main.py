
from TKINTER.consultas import ventana_consultas
from TKINTER.reservas import ventana_reservas
from TKINTER.canchas import ventana_canchas
from TKINTER.clientes import ventana_clientes

import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from BASE_DE_DATOS.database import obtener_conexion
import sesion
from TKINTER.modelo_main import obtener_reservas_dia_db
import threading
from BASE_DE_DATOS.backup_database import crear_respaldo
import os
from pathlib import Path
from dotenv import load_dotenv


# RUTAS DEL PROYECTO
RUTA_PROYECTO = Path(__file__).resolve().parent
RUTA_LOGO = RUTA_PROYECTO / "assets" / "logo_padel.png"

load_dotenv(RUTA_PROYECTO / ".env")


# VENTANA PRINCIPAL
ventana = tk.Tk()
ventana.title("PadelBeche")
ventana.geometry("1280x720")


# COLORES
FONDO = "#0C3C2B"
BOTON = "#ef841a"
BOTON_HOVER = "#27D7A3"
BLANCO = "#FFFFFF"
NEGRO = "#000000"


# CREDENCIALES POR ROL
CREDENCIALES = {
    "Supervisor": os.getenv("SUPERVISOR_PASSWORD"),
    "Empleado": os.getenv("EMPLEADO_PASSWORD"),
}

if not all(CREDENCIALES.values()):
    raise RuntimeError(
        "Faltan contraseñas de los perfiles en el archivo .env"
    )

rol_actual = None

ventana.configure(bg=FONDO)


# NAVEGACION ENTRE PANTALLAS
def mostrar_pantalla(constructor, titulo):
    for widget in contenido.winfo_children():
        widget.destroy()

    ventana.title(f"PadelBeche - {titulo}")
    constructor(contenido)


barra_navegacion = tk.Frame(
    ventana,
    bg=FONDO,
    width=220
)
barra_navegacion.pack_propagate(False)

contenido = tk.Frame(ventana)


# BOTON PARA VOLVER AL INICIO
tk.Button(
    barra_navegacion,
    text="PADEL BECHE",
    command=lambda: mostrar_pantalla(pantalla_inicio, "Inicio"),
    bg=FONDO,
    fg=BLANCO,
    font=("Pagoh Cluser", 18, "bold"),
    activebackground=FONDO,
    activeforeground=BLANCO,
    relief="flat",
    bd=0,
    cursor="hand2"
).pack(pady=(25, 35))


# CREAR BOTONES DE NAVEGACION
def crear_boton(texto, constructor, titulo):
    tk.Button(
        barra_navegacion,
        text=texto,
        command=lambda: mostrar_pantalla(constructor, titulo),
        width=17,
        height=2,
        font=("Montserrat", 12, "bold"),
        bg=BOTON,
        fg=NEGRO,
        activebackground=BOTON_HOVER,
        activeforeground=BLANCO,
        relief="flat",
        bd=0,
        cursor="hand2"
    ).pack(pady=6)


# PANTALLA PRINCIPAL
def pantalla_inicio(contenedor):
    tk.Label(
        contenedor,
        text="GESTOR DE RESERVAS PADEL BECHE",
        font=("Arial", 25, "bold")
    ).pack(pady=(35, 15))

    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    recuadro = tk.LabelFrame(
        contenedor,
        text="Reservas del día",
        font=("Arial", 14, "bold"),
        padx=15,
        pady=15
    )
    recuadro.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=20
    )

    tk.Label(
        recuadro,
        text=f"Fecha: {fecha_hoy}",
        font=("Arial", 12, "bold")
    ).pack(anchor="e", pady=(0, 10))

    tabla = ttk.Treeview(
        recuadro,
        columns=(
            "id Reserva",
            "Cliente",
            "Dni",
            "Cancha",
            "Fecha",
            "Hora Inicio",
            "Hora Fin",
            "Estado"
        ),
        show="headings"
    )

    tabla.heading("id Reserva", text="ID Reserva")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Dni", text="Dni")
    tabla.heading("Cancha", text="Cancha")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Hora Inicio", text="Hora Inicio")
    tabla.heading("Hora Fin", text="Hora Fin")
    tabla.heading("Estado", text="Estado")

    tabla.column(
        "id Reserva", width=80, anchor="center", stretch=True
    )
    tabla.column(
        "Cliente", width=240, anchor="center", stretch=True
    )
    tabla.column(
        "Dni", width=100, anchor="center", stretch=True
    )
    tabla.column(
        "Cancha", width=120, anchor="center", stretch=True
    )
    tabla.column(
        "Fecha", width=100, anchor="center", stretch=True
    )
    tabla.column(
        "Hora Inicio", width=100, anchor="center", stretch=True
    )
    tabla.column(
        "Hora Fin", width=100, anchor="center", stretch=True
    )
    tabla.column(
        "Estado", width=80, anchor="center", stretch=True
    )

    tabla.pack(fill="both", expand=True)

    try:
        lista_reservas = obtener_reservas_dia_db()
    except Exception:
        lista_reservas = []

    fecha_actual_str = datetime.now().date()

    for reserva in lista_reservas:
        es_hoy = False

        try:
            if reserva["fecha"] == fecha_actual_str:
                es_hoy = True
        except Exception:
            pass

        if es_hoy:
            tabla.insert(
                "",
                tk.END,
                values=(
                    reserva["id"],
                    reserva["nombre"],
                    reserva["cliente"],
                    reserva["cancha"],
                    (
                        reserva["fecha"].strftime("%Y-%m-%d")
                        if hasattr(reserva["fecha"], "strftime")
                        else reserva["fecha"]
                    ),
                    reserva["inicio"],
                    reserva["fin"],
                    reserva["estado"]
                )
            )


# BOTONES DEL MENU
crear_boton(
    "Reservas",
    ventana_reservas,
    "Gestión de Reservas"
)
crear_boton(
    "Clientes",
    ventana_clientes,
    "Gestión de Clientes"
)
crear_boton(
    "Canchas",
    ventana_canchas,
    "Gestión de Canchas"
)
crear_boton(
    "Consultas",
    ventana_consultas,
    "Consultas"
)


# BOTON SALIR
boton_salir = tk.Button(
    barra_navegacion,
    text="Salir",
    command=ventana.destroy,
    width=17,
    height=2,
    font=("Arial", 12, "bold"),
    bg=BOTON,
    fg=NEGRO,
    activebackground=BOTON_HOVER,
    activeforeground=BLANCO,
    relief="flat",
    bd=0,
    cursor="hand2"
)
boton_salir.pack(side="bottom", pady=25)


# CREAR RESPALDO
def ejecutar_respaldo():
    confirmar = messagebox.askyesno(
        "Crear respaldo",
        "¿Está seguro de que desea crear un respaldo de la base de datos?"
    )

    if not confirmar:
        return

    boton_respaldo.config(
        state="disabled",
        text="Creando respaldo..."
    )

    def tarea():
        try:
            archivo = crear_respaldo()
            ventana.after(
                0,
                lambda: finalizar_respaldo(str(archivo), None)
            )
        except Exception as error:
            mensaje = str(error)
            ventana.after(
                0,
                lambda: finalizar_respaldo(None, mensaje)
            )

    threading.Thread(target=tarea, daemon=True).start()


def finalizar_respaldo(archivo, error):
    boton_respaldo.config(
        state="normal",
        text="Crear Respaldo"
    )

    if error:
        messagebox.showerror(
            "Error al crear respaldo",
            f"Ocurrió un error al crear el respaldo:\n{error}"
        )
    else:
        messagebox.showinfo(
            "Respaldo exitoso",
            f"El respaldo se creó exitosamente en:\n{archivo}"
        )


boton_respaldo = tk.Button(
    barra_navegacion,
    text="Crear Respaldo",
    command=ejecutar_respaldo,
    width=17,
    height=2,
    font=("Arial", 12, "bold"),
    bg=BOTON,
    fg=NEGRO,
    activebackground=BOTON_HOVER,
    activeforeground=BLANCO,
    relief="flat",
    bd=0,
    cursor="hand2"
)
boton_respaldo.pack(pady=6)


# FUNCION PARA INGRESAR
def ingresar():
    rol = rol_seleccionado.get()
    contrasena = entrada_contrasena.get()

    if CREDENCIALES.get(rol) != contrasena:
        messagebox.showerror(
            "Acceso denegado",
            "Rol o contraseña incorrectos."
        )
        entrada_contrasena.delete(0, tk.END)
        entrada_contrasena.focus_set()
        return

    sesion.rol_actual = rol

    pantalla_ingreso.destroy()

    barra_navegacion.pack(side="left", fill="y")
    contenido.pack(side="right", fill="both", expand=True)

    mostrar_pantalla(pantalla_inicio, "Inicio")


# PANTALLA DE INICIO DE SESION
pantalla_ingreso = tk.Frame(ventana, bg=FONDO)
pantalla_ingreso.pack(fill="both", expand=True)


# FORMULARIO BLANCO CON MARGENES REDUCIDOS
formulario_ingreso = tk.Frame(
    pantalla_ingreso,
    bg=BLANCO,
    padx=15,
    pady=10
)
formulario_ingreso.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# LOGO PNG EN TAMAÑO ORIGINAL
logo_original = tk.PhotoImage(file=str(RUTA_LOGO))

# 1, 1 mantiene las dimensiones originales del PNG.
logo_ingreso = logo_original.subsample(1, 1)

etiqueta_logo = tk.Label(
    formulario_ingreso,
    image=logo_ingreso,
    bg=BLANCO,
    borderwidth=0
)
etiqueta_logo.pack(
    anchor="center",
    pady=(0, 5)
)

# Conserva la imagen en memoria.
formulario_ingreso.logo = logo_ingreso


# TITULO DEL FORMULARIO
tk.Label(
    formulario_ingreso,
    text="Iniciar sesión",
    font=("Arial", 16),
    bg=BLANCO,
    fg=NEGRO
).pack(pady=(0, 22))


# SELECCION DE ROL
tk.Label(
    formulario_ingreso,
    text="Rol",
    font=("Arial", 11, "bold"),
    bg=BLANCO,
    fg=NEGRO
).pack(anchor="w")

rol_seleccionado = tk.StringVar(value="Empleado")

selector_rol = ttk.Combobox(
    formulario_ingreso,
    textvariable=rol_seleccionado,
    values=tuple(CREDENCIALES),
    state="readonly",
    width=28
)
selector_rol.pack(pady=(5, 15))


# CONTRASEÑA
tk.Label(
    formulario_ingreso,
    text="Contraseña",
    font=("Arial", 11, "bold"),
    bg=BLANCO,
    fg=NEGRO
).pack(anchor="w")

entrada_contrasena = tk.Entry(
    formulario_ingreso,
    show="*",
    font=("Arial", 12),
    width=30
)
entrada_contrasena.pack(pady=(5, 20))


def ingresar_con_enter(evento):
    if evento.keysym == "Return":
        ingresar()
        return "break"

    return None


entrada_contrasena.bind("<Return>", ingresar_con_enter)


# BOTON INGRESAR
tk.Button(
    formulario_ingreso,
    text="Ingresar",
    command=ingresar,
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    bg=BOTON,
    fg=NEGRO,
    activebackground=BOTON_HOVER,
    activeforeground=BLANCO,
    relief="flat",
    bd=0,
    cursor="hand2"
).pack()


ventana.mainloop()
