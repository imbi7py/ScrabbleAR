"""
Módulo que contiene las funciones usadas por la ventana de reglas.
"""


import PySimpleGUI as sg
from componentes.ventanas.general import parametros_ventana
    

def crear_ventana_reglas():
    """
    Función usada para crear la ventana de reglas.

    Retorna:
        - (sg.Window): la ventana de reglas.
    """

    layout = [
        [sg.Text("Reglas del juego", size=(60, 1), justification = 'center', background_color = '#1d3557')],
        [sg.Text('')],
        [sg.Button("Fácil", size=(7, 1)), sg.Button("Medio", size=(7, 1)), sg.Button("Difícil", size=(7, 1))],
        [sg.Text('')],
        [sg.Multiline("Seleccione un nivel", key="nivel", disabled=True, size = (60, 3))],
        [sg.Text('')],
        [sg.Button("Volver", size=(7, 1))],
    ]
    
    return sg.Window("Reglas", layout, **parametros_ventana)
    
    
def mostrar_texto(ventana_reglas, event, color, texto, ultimo_presionado):
    """
    Función usada para mostrar las reglas de un nivel.
    
    Actualiza los widgets de la ventana y muestra el texto correspondiente
    al nivel seleccionado.

    Parámetros:
        - ventana_reglas (sg.Window): ventana de reglas.
        - event (str): botón de dificultad presionado.
        - color (str): color de la dificultad seleccionada.
        - texto (str): texto sobre la dificultad seleccionada.
        - ultimo_presionado (str): el anterior botón de dificultad presionado.

    Retorna:
        - (str): parametro event (botón de dificultad presionado).
    """

    if ultimo_presionado != "":
        ventana_reglas[ultimo_presionado].Update(button_color=sg.DEFAULT_BUTTON_COLOR)
    ventana_reglas[event].Update(button_color=color)
    ultimo_presionado = event
    ventana_reglas["nivel"].Update(texto)
    
    return ultimo_presionado