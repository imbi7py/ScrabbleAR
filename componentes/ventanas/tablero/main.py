"""
Módulo principal de la ventana del tablero de juego.
"""


from componentes.ventanas.tablero.funciones import *
from componentes.ventanas.tablero.cambio_fichas.main import main as cambiar_fichas
from componentes.ventanas.tablero.logica.logica_computadora import jugar_computadora
from componentes.ventanas.tablero.logica.logica_jugador import *
from componentes.ventanas.general import leer_evento


def main(configuracion, partida_anterior = None):
    """
    Función donde se muestra el tablero de juego y se leen los diferentes eventos.

    Parámetros:
      - configuracion (dict): diccionario con la configuración del juego.
      - partida_anterior (dict): diccionario con el tablero de la partida anterior.

    Retorna:
      - (dict): diccionario con la partida jugada.
      - (Jugador): instancia de Jugador que representa al usuario.
      - (Jugador): instancia de Jugador que representa a la computadora.
    """
    
    tablero, parametros = inicializar_parametros(configuracion, partida_anterior)
    
    window = crear_ventana_tablero(tablero, parametros, partida_anterior)
    
    comenzar = partida_guardada = None

    while True:
        event, values, tiempo = leer_evento(window, 1000)
        if event in (None, 'Salir'):
            break
        elif event ==  "Iniciar":
            comenzar = iniciar_partida(window, parametros, partida_anterior)
        elif event ==  "Pausa":
            comenzar = pausar(window, comenzar)
        elif event ==  "Posponer":
            salir, partida_guardada = posponer(tablero, parametros["jugada"])
            if salir:
              break
        elif event ==  "Terminar":
            finalizar_partida(window, tablero)
        elif comenzar:
            parametros['fin_juego'], tablero['contador'] = actualizar_tiempo(window, tablero['contador'], tiempo)
            if tablero['turno'] == 'Computadora':
              jugar_computadora(window, parametros, tablero)
            elif tablero['turno'] == 'Jugador':
              if event == "cambiar":
                cambiar_fichas(window, tablero, parametros)
              elif event == "Pasar":
                pasar(window, parametros, tablero)
              elif event == "confirmar":
                confirmar_palabra(window, parametros, tablero)
              elif event in range(7):
                seleccionar_ficha(window, parametros, event)
              elif event:
                colocar_ficha(window, parametros, tablero, event)
            if parametros['fin_juego']:
              comenzar = finalizar_partida(window, tablero)
            window["cantidad_fichas"].Update(len(fichas_totales(tablero['bolsa_de_fichas'])))

    window.Close()
    return partida_guardada, tablero['jugador'], tablero['computadora']