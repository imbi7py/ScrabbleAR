import pickle, json, Tablero, Jugador, PySimpleGUI as sg

def menu():

    layout = [[sg.Text('Menú', size = (60, 1), justification = 'center', font = ("Consolas", 11))],
              [sg.Button('Configuración', key = configuracion), sg.Button('Ver reglas del juego', key = reglas), sg.Button('Ver top de puntajes', key = top_puntajes), sg.Button('Volver')]]
    window = sg.Window('Menú', layout, location = (600, 200))

    configuracion_seleccionada = {} 

    while True:
        event = window.Read()[0]    
        if (event in (None, 'Volver')):
            break
        else:
            window.Hide()
            if (event == configuracion): 
                configuracion_seleccionada = configuracion()
                print(configuracion_seleccionada)
            else:
                event()
            window.UnHide()

    window.Close()

    return configuracion_seleccionada

def reglas():

    texto1 = 'Palabras válidas: cualquier palabra que la libería Pattern considere válida.\nTamño del tablero: 19 x 19.'
    texto2 = 'Palabras válidas: adjetivos y verbos.\nTamño del tablero: 17 x 17.'
    texto3 = 'Palabras válidas: adjetivos y verbos. \nTamño del tablero: 15 x 15.'
    ultimo_presionado = ''

    layout = [[sg.Text('Reglas del juego', size = (60, 1), justification = 'center', font = ("Consolas", 11))],
              [sg.Text('                          '), sg.Button('Fácil', button_color = ('white', 'blue')), sg.Button('Medio', button_color = ('white', 'blue')), sg.Button('Difícil', button_color = ('white', 'blue'))],
              [sg.Multiline('Seleccione un nivel', key = 'nivel', disabled = True)],
              [sg.Button('Volver', button_color = ('white', 'blue'))]]
    window = sg.Window('Reglas', layout, location = (600, 200))

    while True:
        event = window.Read()[0]
        if (event in (None, 'Volver')):
            break
        if (ultimo_presionado != ''):
            window.Element(ultimo_presionado).Update(button_color = ('white', 'blue'))
        window.Element(event).Update(button_color = ('white', 'red'))
        ultimo_presionado = event
        window.Element('nivel').Update(texto1 if event == 'Fácil' else (texto2 if event == 'Medio' else texto3))
    window.Close()

def top_puntajes():

    with open('top10', 'rb') as f:
        top = pickle.load(f)

    temp = list(jugador[0] + ' ' + str(jugador[1].get_puntaje()) + ' puntos' for jugador in top)
    strs = ''
    for i in temp:
        strs += i + '\n'
    print(strs)

    layout = [[sg.Text('Top 10 de los mejores puntajes')],
              [sg.Multiline(strs, disabled = True)],
              [sg.Button('Volver')]]

    window = sg.Window('Top puntajes', layout)

    window.Read()
    window.Close()
    

def configuracion():

    def informacion_letras(letras):
        
        if (len(letras) == 0):
            return 'Letras modificadas'
        texto = 'Letra   Puntos   Cantidad de fichas\n\n'
        for letra in letras:
            texto += '   ' + str(letra) + '        ' + str(letras[letra]['puntaje']) + '                  ' + str(letras[letra]['cantidad_fichas']) + '\n'
        return texto

    with open('ultima_configuracion.json') as f:
        configuracion_seleccionada = json.load(f)
    
    with open('configuracion_predeterminada.json') as f:
        configuracion_predeterminada = json.load(f)

    layout = [[sg.Text('Nivel de la partida', size = (80,1), justification = 'center', font = ('Consolas', 11))],
              [sg.Text('')],
              [sg.Text('                                       '), sg.Button('Facil', button_color = ('white', 'green')), sg.Text('               '), sg.Button('Medio', button_color = ('white', 'orange')),sg.Text('            '),sg.Button('Dificil', button_color = ('white', 'red'))],
              [sg.Text('')],
              [sg.Text('Configuración de las fichas\npara todos los niveles', size = (80, 2), justification = 'center', font = ('Consolas', 11))],
              [sg.Text('')],
              [sg.Text('Letra'), sg.Spin(values = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'), initial_value = 'A', enable_events = True, key = 'letra'), sg.Text('Puntaje'), sg.Input(' ', size = (4, 2), key = 'puntaje'), sg.Text('Cantidad de fichas'), sg.Input(' ', size = (4, 2), key = 'fichas'), sg.Button('Confirmar', key = 'confirmar_letra')],
              [sg.Text('')],
              [sg.Text('Tiempo de la partida', size = (80, 1), justification = 'center',font = ('Consolas', 11))],
              [sg.Text('')],
              [sg.Text('         '), sg.Text('Minutos'), sg.Input(' ', size = (4, 2), key = 'tiempo'), sg.Text('           '), sg.Button('Confirmar', key = 'confirmar_tiempo')],
              [sg.Text('')],
              [sg.Text('Configuracion actual', size = (80, 1), justification = 'center', font = ('Consolas', 11))],
              [sg.Text('Nivel'), sg.Text(str(configuracion_seleccionada['nivel']) + '   ', key = 'nivel_seleccionado')],
              [sg.Text('Tiempo'), sg.Text(str(configuracion_seleccionada['tiempo']) + ' minutos     ', key = 'tiempo_seleccionado')],
              [sg.Text('Letras')],
              [sg.Multiline(informacion_letras(configuracion_seleccionada['fichas']), key = 'letras_modificadas', disabled = True, size = (25, 10))],
              [sg.Text('')],
              [sg.Button('Aceptar'), sg.Button('Restablecer\nconfiguración', size = (10,3), key = 'restablecer')]]
    window = sg.Window('Configuración', layout, location = (800, 400))

    while True:
        event, values = window.Read()
        if (event in (None, 'Aceptar')):
            break
        if (event == 'restablecer'):
            configuracion_seleccionada = configuracion_predeterminada.copy()
            window.Element('tiempo_seleccionado').Update(str(configuracion_seleccionada['tiempo']) + ' minutos')
            window.Element('letras_modificadas').Update(informacion_letras(configuracion_seleccionada['fichas']))
            window.Element('nivel_seleccionado').Update(configuracion_seleccionada['nivel'])
        if (event == 'confirmar_tiempo'):
            if (values['tiempo'] == ' '):
                sg.Popup('El campo está vacío', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
            else:
                try:
                    configuracion_seleccionada['tiempo'] = int(values['tiempo'])
                except (ValueError):
                    sg.Popup('No se ingresó un número válido', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
                else:
                    window.Element('tiempo_seleccionado').Update(str(configuracion_seleccionada['tiempo']) + ' minutos' if configuracion_seleccionada['tiempo'] != ' ' else ' ')
        if (event == 'confirmar_letra'):
            if (' ' in (values['letra'], values['puntaje'], values['fichas'])):
                sg.Popup('Todos los campos deben estar completos', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
            else:
                try:
                    configuracion_seleccionada['fichas'][values['letra']] = {'puntaje' : int(values['puntaje']), 'cantidad_fichas' : int(values['fichas'])}
                except (ValueError):
                    sg.Popup('Los datos ingresados deben ser válidos', title = 'Atención', non_blocking = True, auto_close_duration = 5, auto_close = True)
                else:
                    window.Element('letras_modificadas').Update(informacion_letras(configuracion_seleccionada['fichas']))
        if (event in ('Facil', 'Medio', 'Dificil')):
            configuracion_seleccionada['nivel'] = event.lower()
            window.Element('nivel_seleccionado').Update(configuracion_seleccionada['nivel'])

    window.Close()

    with open('ultima_configuracion.json', 'w') as f:
        json.dump(configuracion_seleccionada, f)

    return configuracion_seleccionada

def actualizar_top(top, jugador, computadora):

    top += [('Jugador', jugador)]
    top += [('Computadora', computadora)]

    top = sorted(top, key = lambda x : x[1].get_puntaje(), reverse = True)
    top = top[:10]


with open('guardada', 'rb') as f:
    partida = pickle.load(f)

layout = [[sg.Text('ScrabbleAR')],
          [sg.Button('Imagen scrabble', disabled = True)],
          [sg.Button('Menú', key = menu), sg.Button('Reanudar partida', size = (7,2), key = 'reanudar', disabled = partida == None), sg.Button('Iniciar nueva partida', size = (11, 2), key = Tablero.jugar), sg.Button('Salir')]]
window = sg.Window('ScrabbleAR', layout)

layout_confirmar = [[sg.Text('Hay una partida guardada, si inicia una nueva no podrá continuar con la anterior')],
                    [sg.Button('Cancelar'), sg.Button('Continuar')]]
window_confirmar = sg.Window('Partida nueva', layout_confirmar)

with open('ultima_configuracion.json') as f:
    configuracion_seleccionada = json.load(f)

with open('top10', 'rb') as f:
    top = pickle.load(f)

ok = True

while True:
    event = window.Read()[0]
    if (event in (None, 'Salir')):
        break
    elif (event == menu):
        window.Hide()
        configuracion_seleccionada = menu()
        window.UnHide()
    elif (event == Tablero.jugar):
        if (partida != None):
            window.Hide()
            opcion = window_confirmar.Read()[0]
            window_confirmar.close()
            window.UnHide()
            ok = opcion == 'Continuar'
        if (ok):
            window.Hide()
            partida, jugador, computadora = Tablero.jugar(configuracion_seleccionada, None)
            actualizar_top(top, jugador, computadora)
            with open('top10', 'wb') as f:
                pickle.dump(top, f)
            window.UnHide()
    elif (event == 'reanudar'):
        window.Hide()
        partida, jugador, computadora = Tablero.jugar(configuracion_seleccionada, partida)
        actualizar_top(top, jugador, computadora)
        with open('top10', 'wb') as f:
            pickle.dump(top, f)
        window.UnHide()
    with open('guardada', 'wb') as f:
        pickle.dump(partida, f)
    window.Element('reanudar').Update(disabled = partida == None)

window.Close()