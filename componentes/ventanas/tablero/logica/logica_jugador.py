"""
Autores: Garea Antonella, Garofalo Pedro y Giorgetti Valentín
Licencia: GNU General Public License

Módulo que contiene funciones usadas por el jugador.
"""


import PySimpleGUI as sg
from functools import reduce
from componentes.ventanas.general import parametros_popup
from componentes.ventanas.tablero.logica.funciones import (
    es_palabra, es_repetida, fichas_totales, 
    actualizar_tabla, reproducir_sonido_palabra, contar_jugada, 
    letra_random, reiniciar_parametros, finalizar_jugada
)


def posicion_valida(posicion, posiciones_ocupadas, posiciones_bloqueadas, orientacion):
    """
    Función que verifica si el usuario puede colocar una ficha en una posicion determinada del tablero. 

    Se comprueba que se respete la orientación elegida y que la casilla no esté ocupada.

    Parámetros:
        - posicion (tuple): tupla que indica la posición del tablero a verificar.
        - posiciones_ocupadas (OrderedDict): diccionario ordenado donde las claves son las posiciones del tablero
                                             ocupadas en la jugada (tuplas) y el valor es la posición del atril de 
                                             la letra ubicada en la casilla correspondiente.
        - posiciones_bloqueadas (list): lista de tuplas que indican las posiciones bloqueadas.
        - orientacion (str): string que indica la orientación de la jugada.

    Retorna:
        - (str): orientación de la jugada.
        - (bool): indica si la posición es válida
    """
    
    if posicion in range(8, 15):
        return orientacion, False
    misma_orientacion = False
    if not posicion in posiciones_bloqueadas:
        if not posiciones_ocupadas or posicion in posiciones_ocupadas:
            return orientacion, True
        elif (posicion[0] - 1, posicion[1]) in posiciones_ocupadas:
            if not orientacion:
                return "vertical", True
            else:
                misma_orientacion = orientacion == "vertical"
        elif (posicion[0], posicion[1] - 1) in posiciones_ocupadas:
            if not orientacion:
                return "horizontal", True
            else:
                misma_orientacion = orientacion == "horizontal"
        if misma_orientacion:
            return orientacion, True
        else:
            mensaje = ""
            if orientacion == "horizontal":
                mensaje = "Solo se pueden agregar letras en forma horizontal, de izquierda a derecha"
            elif orientacion == "vertical":
                mensaje = "Solo se pueden agregar letras en forma vertical, de arriba hacia abajo"
            else:
                mensaje = "Las letras sólo se pueden agregar de izquierda a derecha o de abajo hacia arriba"
            sg.Popup(mensaje + "\n", **parametros_popup)
            return orientacion, False
    else:
        sg.Popup("La casilla está ocupada\n", **parametros_popup)
        return orientacion, False


def palabra_formada(letras, posiciones_ocupadas):
    """
    Función que retorna un string con la palabra formada por el jugador.

    Parámetros:
        - letras (list): fichas del jugador.
        - posiciones_ocupadas (OrderedDict): diccionario ordenado donde las claves son las posiciones del tablero
                                             ocupadas en la jugada (tuplas) y el valor es la posición del atril de 
                                             la letra ubicada en la casilla correspondiente.

    Retorna:
        - (str): la palabra formada por la jugada.
    """

    return reduce(lambda anterior, posicion: anterior + letras[posicion], posiciones_ocupadas.values(), "")


def verificar_palabra(parametros, tablero):
    """
    Función que verifica si la casilla de inicio está ocupada en caso de que sea la primer
    jugada de la partida, y que la palabra sea válida para el nivel.

    Parámetros:
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - tablero (dict): diccionario con la información del tablero.
        
    Retorna:
        - (bool): indica si la jugada es válida.
    """

    palabra = palabra_formada(tablero["jugador"].fichas, parametros["jugada"])
    
    if es_repetida(palabra, tablero["palabras_ingresadas"]):
        sg.Popup("No se pueden ingresar palabras repetidas\n", **parametros_popup)
        
        return False
        
    if tablero["primer_jugada"] and not tablero["centro"] in parametros["jugada"]:
        sg.Popup("La casilla de inicio no está ocupada\n", **parametros_popup)
        
        return False
        
    if len(parametros["jugada"]) < 2:
        sg.Popup("Palabra inválida, vuelva a intentarlo\n", **parametros_popup)
        
        return False
        
    else:
        if es_palabra(tablero["nivel"], tablero["palabras_validas"], palabra):
        
            return True
            
        else:
            sg.Popup("Palabra inválida, vuelva a intentarlo\n", **parametros_popup)
            
            return False


def confirmar_palabra(window, parametros, tablero):
    """
    Función usada para confirmar la palabra ingresada por el jugador.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - tablero (dict): diccionario con la información del tablero.
    """

    jugador = tablero["jugador"]
    jugada = parametros["jugada"]
    quedan_fichas = len(fichas_totales(tablero["bolsa_de_fichas"])) >= len(jugada)
    letras_jugador = jugador.fichas
    es_correcta = verificar_palabra(parametros, tablero)
    if parametros["letra_seleccionada"]:
        window[parametros["letra"]].Update(button_color=("white", "green"))
        parametros["letra_seleccionada"] = False
    if es_correcta:
        tablero["primer_jugada"] = False
        palabra = palabra_formada(letras_jugador, jugada)
        puntos_jugada = contar_jugada(
            window, palabra, list(jugada.keys()), tablero, parametros["casillas_especiales"], jugador
        )[1]
        finalizar_jugada(window, parametros, tablero, palabra, puntos_jugada, jugador, "El jugador")
        reiniciar_parametros(parametros)
        if quedan_fichas:
            for posicion in jugada:
                letra = letra_random(tablero["bolsa_de_fichas"])
                letras_jugador[jugada[posicion]] = letra
                window[jugada[posicion]].Update(letra, disabled=False, button_color=("white", "green"))
            tablero["turno"] = "Computadora"
            window["turno"].Update("Computadora")
        else:
            for letra in palabra:
                letras_jugador.remove(letra)
            parametros["fin_juego"] = True
            parametros["historial"] += "\n\n - Fin de la partida. No quedan suficientes fichas para repartir."
            window["historial"].Update(parametros["historial"])
        actualizar_tabla(jugador, tablero["computadora"], window)
    reproducir_sonido_palabra(es_correcta)
    
    
def seleccionar_ficha(window, parametros, event, color):
    """
    Función usada para que el usuario seleccione una ficha.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - event (int): indica la posición de la letra seleccionada en el atril del jugador.
        - color (tuple): tupla que indica el color de las fichas del usuario.
    """

    if parametros["letra_seleccionada"]:
        window[parametros["letra"]].Update(button_color=("white", "green"))
        
    if parametros["letra"] != event:
        window[event].Update(button_color=color)
        parametros["letra"] = event
        parametros["letra_seleccionada"] = True
    else:
        parametros["letra"] = -1
        parametros["letra_seleccionada"] = False


def colocar_ficha(window, parametros, tablero, event):
    """
    Función usada para que el usuario coloque la ficha seleccionada en el tablero.

    Parámetros:
        - window (sg.Window): ventana del tablero.
        - parametros (dict): diccionario con párametros que controlan la lógica del juego.
        - tablero (dict): diccionario con la información del tablero.
        - event (tuple): tupla que indica la posición del tablero donde colocar la ficha.
    """

    casilla_vacia = {"text" : " ", "button_color" : ("white", "green")}
    if parametros["letra_seleccionada"]:
        parametros["orientacion"], es_valida = posicion_valida(
            event, parametros["jugada"], tablero["posiciones_ocupadas"], parametros["orientacion"]
        )
        if es_valida:
            if event in parametros["jugada"]:
                window[parametros["jugada"][event]].Update(button_color=("white", "green"), disabled=False)
            else:
                parametros["ultima_posicion"] = event
            window[event].Update(tablero["jugador"].fichas[parametros["letra"]], button_color=tablero["jugador"].color)
            parametros["jugada"][event] = parametros["letra"]
            window[parametros["letra"]].Update(disabled=True)
            parametros["letra"] = -1
            parametros["letra_seleccionada"] = False
            if len(parametros["jugada"]) == 1:
                parametros["primer_posicion"] = parametros["ultima_posicion"] = event
    else:
        if event in (parametros["primer_posicion"], parametros["ultima_posicion"]):
            casillas_especiales = parametros["casillas_especiales"]
            param = casillas_especiales[event]["parametros_boton"] if event in casillas_especiales else casilla_vacia
            window[event].Update(**param, disabled=False)
            window[parametros["jugada"][event]].Update(button_color=("white", "green"), disabled=False)
            del parametros["jugada"][event]
            if len(parametros["jugada"]) <= 1:
                parametros["orientacion"] = ""
                if not parametros["jugada"]:
                    parametros["primer_posicion"] = parametros["ultima_posicion"] = ()
            if event == parametros["primer_posicion"]:
                parametros["primer_posicion"] = (
                    (event[0] + 1, event[1]) if parametros["orientacion"] == "vertical" else (event[0], event[1] + 1)
                )
            else:
                parametros["ultima_posicion"] = (
                    (event[0] - 1, event[1]) if parametros["orientacion"] == "vertical" else (event[0], event[1] - 1)
                )