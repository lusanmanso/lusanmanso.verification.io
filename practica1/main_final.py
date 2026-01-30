import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from flask import request, render_template_string

# Crear constantes para etiquetas
TIEMPO = "Tiempo (s)"
FRECUENCIA = "Frecuencia (Hz)"
AMPLITUD = "Amplitud"

fm=4000 # frecuencia muestro 4000 Hz

tm=120 # tiempo de análisis
tm=2*tm


def generar_senial(frecuencia, tipo, duracion):
    tiempo = np.linspace(0, duracion, int(1000 * duracion), endpoint=False)

    if tipo == 'sinusoidal':
        return tiempo, np.sin(2 * np.pi * frecuencia * tiempo)
    elif tipo == 'cuadrada':
        return tiempo, np.sign(np.sin(2 * np.pi * frecuencia * tiempo))
    elif tipo == 'triangular':
        return tiempo, np.abs(2 * np.mod(tiempo * frecuencia, 1) - 1) - 0.5

def calcular_transformada_fourier(senal, duracion):
    fft_resultado = np.fft.fft(senal)
    frecuencias = np.fft.fftfreq(len(senal), d=(duracion/len(senal)))
    return frecuencias, fft_resultado

def solicitar_duracion():
    duracion = simpledialog.askfloat("Duración", "Ingrese la duración en segundos:")
    return duracion

def actualizar_graficas():
    duracion = solicitar_duracion()
    if duracion is None:
        return  # Si el usuario cancela, no actualiza las gráficas

    frecuencia_sinusoidal = float(entry_frec_sinusoidal.get())
    frecuencia_cuadrada = float(entry_frec_cuadrada.get())
    frecuencia_triangular = float(entry_frec_triangular.get())

    tiempo_sinusoidal, onda_sinusoidal = generar_senial(frecuencia_sinusoidal, 'sinusoidal', duracion)
    tiempo_cuadrada, onda_cuadrada = generar_senial(frecuencia_cuadrada, 'cuadrada', duracion)
    tiempo_triangular, onda_triangular = generar_senial(frecuencia_triangular, 'triangular', duracion)

    # Calcular y graficar transformadas de Fourier
    frecuencias_sinusoidal, fft_sinusoidal = calcular_transformada_fourier(onda_sinusoidal, duracion)
    frecuencias_cuadrada, fft_cuadrada = calcular_transformada_fourier(onda_cuadrada, duracion)
    frecuencias_triangular, fft_triangular = calcular_transformada_fourier(onda_triangular, duracion)

    # Gráficas de las señales temporales y transformadas de Fourier
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(8, 6))

    # Sinusoidal
    axs[0, 0].plot(tiempo_sinusoidal, onda_sinusoidal, label='Sinusoidal')
    axs[0, 0].set_xlabel(TIEMPO)
    axs[0, 0].set_ylabel(AMPLITUD)
    axs[0, 0].legend()
    axs[0, 1].plot(frecuencias_sinusoidal, np.abs(fft_sinusoidal), label='Transformada')
    axs[0, 1].set_xlabel(FRECUENCIA)
    axs[0, 1].set_ylabel(AMPLITUD)
    axs[0, 1].legend()


    # Cuadrada
    axs[1, 0].plot(tiempo_cuadrada, onda_cuadrada, label='Cuadrada')
    axs[1, 0].set_xlabel(TIEMPO)
    axs[1, 0].set_ylabel(AMPLITUD)
    axs[1, 0].legend()
    axs[1, 1].plot(frecuencias_cuadrada, np.abs(fft_cuadrada), label='Transformada')
    axs[1, 1].set_xlabel(FRECUENCIA)
    axs[1, 1].set_ylabel(AMPLITUD)
    axs[1, 1].legend()

    # Triangular
    axs[2, 0].plot(tiempo_triangular, onda_triangular, label='Triangular')
    axs[2, 0].set_xlabel(TIEMPO)
    axs[2, 0].set_ylabel(AMPLITUD)
    axs[2, 0].legend()
    axs[2, 1].plot(frecuencias_triangular, np.abs(fft_triangular), label='Transformada')
    axs[2, 1].set_xlabel(FRECUENCIA)
    axs[2, 1].set_ylabel(AMPLITUD)
    axs[2, 1].legend()

    # Configurar los widgets de lienzo para las gráficas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    root.update()  # Actualizar la ventana

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Generador de Señales y Transformadas de Fourier")

# Crear y configurar los widgets
frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Frecuencia Sinusoidal:").grid(column=0, row=0, sticky=tk.W)
entry_frec_sinusoidal = ttk.Entry(frame)
entry_frec_sinusoidal.grid(column=1, row=0, sticky=tk.W)

ttk.Label(frame, text="Frecuencia Cuadrada:").grid(column=0, row=1, sticky=tk.W)
entry_frec_cuadrada = ttk.Entry(frame)
entry_frec_cuadrada.grid(column=1, row=1, sticky=tk.W)

ttk.Label(frame, text="Frecuencia Triangular:").grid(column=0, row=2, sticky=tk.W)
entry_frec_triangular = ttk.Entry(frame)
entry_frec_triangular.grid(column=1, row=2, sticky=tk.W)

button_actualizar = ttk.Button(frame, text="Actualizar", command=actualizar_graficas)
button_actualizar.grid(column=0, row=3, columnspan=2)

button_salir = ttk.Button(frame, text="Salir", command=root.destroy)
button_salir.grid(column=0, row=7, columnspan=2)

# Iniciar la aplicación
root.mainloop()
