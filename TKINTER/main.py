from consultas import ventana_consultas
from reservas import ventana_reservas
from canchas import ventana_canchas
from clientes import ventana_clientes
import tkinter as tk


def abrir_reservas():
    ventana_reservas()


def abrir_clientes():
    ventana_clientes()


def abrir_canchas():
    ventana_canchas()


def abrir_consultas():
    ventana_consultas()


ventana = tk.Tk()
ventana.title("PadelBeche")
ventana.geometry("800x600")

titulo = tk.Label(
    ventana,
    text="GESTOR DE RESERVAS PADEL BECHE",
    font=("Arial", 20)
)
titulo.pack(pady=30)

boton_reservas = tk.Button(
    ventana,
    text="Reservas",
    command=abrir_reservas
)
boton_reservas.pack(pady=10)

boton_clientes = tk.Button(
    ventana,
    text="Clientes",
    command=abrir_clientes
)
boton_clientes.pack(pady=10)

boton_canchas = tk.Button(
    ventana,
    text="Canchas",
    command=abrir_canchas
)
boton_canchas.pack(pady=10)

boton_consultas = tk.Button(
    ventana,
    text="Consultas",
    command=abrir_consultas
)
boton_consultas.pack(pady=10)

boton_salir = tk.Button(
    ventana,
    text="Salir",
    command=ventana.destroy
)
boton_salir.pack(pady=30)

ventana.mainloop()