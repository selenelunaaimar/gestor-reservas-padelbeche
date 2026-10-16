from consultas import ventana_consultas 
from reservas import ventana_reservas
from canchas import ventana_canchas
from clientes import ventana_clientes
import tkinter as tk #importa la biblioteca gráfica Tkinter 
from datetime import datetime #obtiene la fecha y hora actuales
from tkinter import messagebox, ttk
from BASE_DE_DATOS.database import obtener_conexion
import sesion 
from modelo_main import obtener_reservas_dia_db

"""VENTANA PRINCIPAL"""
ventana = tk.Tk()
ventana.title("PadelBeche")
ventana.geometry("1280x720")

"""COLORES"""
FONDO = "#0C3C2B"
BOTON = "#ef841a"
BOTON_HOVER = "#27D7A3"
BLANCO = "#FFFFFF"
NEGRO = "#000000"

""" Credenciales de acceso organizadas por rol - diccionario """
CREDENCIALES = {
    "Supervisor": "Admin2026",
    "Empleado": "1234Hola",
}

""" Agrego una variable de sesion para guardar el rol, y poder usarla en los demas modulos"""
rol_actual = None

ventana.configure(bg=FONDO)

def mostrar_pantalla(constructor, titulo):
    for widget in contenido.winfo_children():
        widget.destroy()

    ventana.title(f"PadelBeche - {titulo}")
    constructor(contenido)
barra_navegacion = tk.Frame(ventana, bg=FONDO, width=220)
""""Tamaño fijo con pack_propagate(False)"""
barra_navegacion.pack_propagate(False)
contenido = tk.Frame(ventana)

"""padx agrega espacio horizontal dentro o alrededor de un elemento
pady agrega espacio vertical.
Convertimos el nombre PADEL BECHE en un boton para que siempre vuelva a la pantalla principal"""
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

def pantalla_inicio(contenedor):
    tk.Label(
        contenedor,
        text="GESTOR DE RESERVAS PADEL BECHE",
        font=("Arial", 25, "bold")
    ).pack(pady=(35, 15))

    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    """ Recuadro de reservas del dia """
    recuadro = tk.LabelFrame(
        contenedor,
        text="Reservas del día",
        font=("Arial", 14, "bold"),
        padx=15,
        pady=15
    )
    recuadro.pack(fill="both", expand=True, padx=35, pady=20)

    tk.Label(
        recuadro,
        text=f"Fecha: {fecha_hoy}",
        font=("Arial", 12, "bold")
    ).pack(anchor="e", pady=(0, 10))

    tabla = ttk.Treeview(
        recuadro,
        columns=("id Reserva","Cliente", "Dni", "Cancha", "Fecha", "Hora Inicio", "Hora Fin", "Estado"),
        show="headings"
    )

    """el ancho de las columnas las definimos con width (920 pixeles), anchor es para colocar el contenido en el un espacio determinado.
        anchor="w"  # izquierda
        anchor="e"  # derecha
        anchor="center"  # centro
        anchor="n"  # arriba
        anchor="s"  # abajo
    stretch es para evitar que Tkinter agrande las columnas automaticamente"""

    tabla.heading("id Reserva", text="ID Reserva")
    tabla.heading("Cliente", text="Cliente")
    tabla.heading("Dni", text="Dni")
    tabla.heading("Cancha", text="Cancha")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Hora Inicio", text="Hora Inicio")
    tabla.heading("Hora Fin", text="Hora Fin")
    tabla.heading("Estado", text="Estado")

    tabla.column("id Reserva", width=80, anchor="center", stretch=True)
    tabla.column("Cliente", width=240, anchor="center", stretch=True)
    tabla.column("Dni", width=100, anchor="center", stretch=True)
    tabla.column("Cancha", width=120, anchor="center", stretch=True)
    tabla.column("Fecha", width=100, anchor="center", stretch=True)
    tabla.column("Hora Inicio", width=100, anchor="center", stretch=True)
    tabla.column("Hora Fin", width=100, anchor="center", stretch=True)
    tabla.column("Estado", width=80, anchor="center", stretch=True)
    tabla.pack(fill="both", expand=True)

    """ Obtenemos las reservas y clientes a través del modelo para la pantalla principal """
    try:
        lista_reservas = obtener_reservas_dia_db()
    except Exception:
        lista_reservas = []

    fecha_actual_str = datetime.now().date()

    for reserva in lista_reservas:
        es_hoy = False
        try:
            """Comparamos la fecha de la base de datos directamente"""
            if reserva["fecha"] == fecha_actual_str:
                es_hoy = True
        except Exception:
            pass

        if es_hoy:
            tabla.insert(
                "",
                tk.END,
                values=(
                    reserva["id"],          # ID Reserva
                    reserva["nombre"],      # Cliente (Nombre y Apellido)
                    reserva["cliente"],     # Dni
                    reserva["cancha"],      # Cancha
                    reserva["fecha"].strftime("%Y-%m-%d") if hasattr(reserva["fecha"], "strftime") else reserva["fecha"],      # Fecha
                    reserva["inicio"],      # Hora Inicio
                    reserva["fin"],         # Hora Fin
                    reserva["estado"]       # Estado
                )
            )

crear_boton("Reservas", ventana_reservas, "Gestión de Reservas")
crear_boton("Clientes", ventana_clientes, "Gestión de Clientes")
crear_boton("Canchas", ventana_canchas, "Gestión de Canchas")
crear_boton("Consultas", ventana_consultas, "Consultas")

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

""" Funcion ingresar"""
def ingresar():
    rol = rol_seleccionado.get()
    contrasena = entrada_contrasena.get()

    if CREDENCIALES.get(rol) != contrasena:
        messagebox.showerror("Acceso denegado", "Rol o contraseña incorrectos.")
        entrada_contrasena.delete(0, tk.END)
        entrada_contrasena.focus_set()
        return
    
    sesion.rol_actual = rol #me guardo en sesion.py el rol

    pantalla_ingreso.destroy()
    barra_navegacion.pack(side="left", fill="y")
    contenido.pack(side="right", fill="both", expand=True)
    mostrar_pantalla(pantalla_inicio, "Inicio")

""""contenedores de la pantalla"""
pantalla_ingreso = tk.Frame(ventana, bg=FONDO)
pantalla_ingreso.pack(fill="both", expand=True) #.pack( hace que la pantalla ocupe la ventana)

formulario_ingreso = tk.Frame(pantalla_ingreso, bg=BLANCO, padx=45, pady=35)
formulario_ingreso.place(relx=0.5, rely=0.5, anchor="center") #.place() hace que se centre el formulario

tk.Label(
    formulario_ingreso,
    text="PADEL BECHE",
    font=("Arial", 26, "bold"),
    bg=BLANCO,
    fg=FONDO
).pack(pady=(0, 8))

tk.Label(
    formulario_ingreso,
    text="Iniciar sesión",
    font=("Arial", 16),
    bg=BLANCO,
    fg=NEGRO
).pack(pady=(0, 22))

tk.Label(
    formulario_ingreso,
    text="Rol",
    font=("Arial", 11, "bold"),
    bg=BLANCO,
    fg=NEGRO
).pack(anchor="w")

#StringVar es una variable especial de Tkinter que mantiene sincronizado un valor de texto con un control de la interfaz
#Combobox es una lista desplegable -> el valor inicial siempre es Empleado
rol_seleccionado = tk.StringVar(value="Empleado")  
selector_rol = ttk.Combobox(
    formulario_ingreso,
    textvariable=rol_seleccionado,
    values=tuple(CREDENCIALES),
    state="readonly", #esto es para que no sea texto libre, si no elegir una opcion.
    width=28
)
selector_rol.pack(pady=(5, 15))

tk.Label(
    formulario_ingreso,
    text="Contraseña",
    font=("Arial", 11, "bold"),
    bg=BLANCO,
    fg=NEGRO
).pack(anchor="w")

entrada_contrasena = tk.Entry(formulario_ingreso, show="*", font=("Arial", 12), width=30)
entrada_contrasena.pack(pady=(5, 20))

def ingresar_con_enter(evento):
    if evento.keysym == "Return":
        ingresar()
        return "break"
    return None

entrada_contrasena.bind("<Return>", ingresar_con_enter)

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