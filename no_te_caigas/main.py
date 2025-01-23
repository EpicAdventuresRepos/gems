from no_te_caigas.datos import Global, Caverna, Jugador
from no_te_caigas.lexico import Resultado, comando


def load_data():

    estado = Global.get_instance()

    # Ejemplo de uso
    caverna = Caverna(5, 5)
    caverna.agregar_agujero(2, 3)
    caverna.agregar_agujero(3, 4)
    caverna.agregar_agujero(4, 1)
    estado.set_caverna(caverna)

    # Ejemplo de uso
    jugador = Jugador(0, 0, 5, 5)
    estado.set_jugador(jugador)


"""
    print("Posición inicial:", jugador.obtener_posicion())

    jugador.mover_norte()
    print("Después de moverse al norte:", jugador.obtener_posicion())

    jugador.mover_este()
    print("Después de moverse al este:", jugador.obtener_posicion())

    jugador.mover_sur()
    print("Después de moverse al sur:", jugador.obtener_posicion())

    jugador.mover_oeste()
    print("Después de moverse al oeste:", jugador.obtener_posicion())

    jugador.mover_norte()
    jugador.mover_norte()  # Movimiento no permitido
"""


def procesar_cadena(cadena):
    palabras = cadena.split()  # Divide la cadena en palabras
    palabras_procesadas = [palabra[:6] if len(palabra) > 6 else palabra for palabra in palabras]
    return palabras_procesadas

def intrucciones():
    print("""
    No te caigas.
    -------------

    Empiezas en la casilla 0, 0 de una caverna de 5x5 y tienes que llegar a la casilla 4x4.
    Si entras en una casilla con un agujero, se acabará la partida.
    Si entras en una casilla que tiene un agujero adyacente, notarás una brisa de aire. 
    Muévete con: n, s, e, o (n es abajo y s arriba).
    >> Pulsa ENTER
    """)
    input()

def main_game():
    # Cargar datos iniciales
    load_data()
    estado = Global.get_instance()
    caverna = estado.caverna()
    resultado = None

    intrucciones()

    while resultado != Resultado.FIN_JUEGO:
        resultado = None
        jugador = estado.jugador()
        print("Estás en la caverna: " + str(jugador))

        if caverna.casilla_final(jugador):
            print("Has llegado a tu destino.")
            break

        if caverna.hay_agujero(jugador):
            print("Te has caido al agujero.")
            break

        if caverna.hay_agujero_adyacente(jugador):
            print("Una corriente de aire cruza la caverna.")


        user_input = input(">> ")
        palabras = procesar_cadena(user_input)
        user_command = comando(palabras[0])

        # Ver si existen
        if user_command.token_verbo is None:
            print("Verbo no encontrado.")
            continue

        # Procesar comando en los comandos por defecto.
        c_comunes = comandos_comunes(jugador)
        command_method = None
        if user_command.token_verbo in c_comunes:
            verbs = c_comunes[user_command.token_verbo]
            command_method = verbs["*"]

        if command_method is not None:
            resultado = command_method()

        # Si no hay un HECHO es que no puedes hacerlo
        if resultado == Resultado.NO_HECHO or command_method is None:
            print("No puedes hacerlo.")

    caverna.mostrar_caverna()
    # Fin del juego


# Verbos genéricos

def cmd_fin(comando):
    return Resultado.FIN_JUEGO


def cmd_guardar(comando):
    import pickle
    with open("save_game.pck", "wb") as save_file:
        pickle.dump(Global.get_instance(), save_file)
    print("Guardado.")
    return Resultado.HECHO


def cmd_cargar(comando):
    import pickle
    with open("save_game.pck", "rb") as save_file:
        save_data = pickle.load(save_file)
    Global._instance = save_data
    print("Cargado.")
    # Pulsa una tecla.
    return Resultado.REINICIA


def cmd_debug(comando):
    estado = Global.get_instance()
    print(estado)
    return Resultado.HECHO

def comandos_comunes(jugador):
    comandos = {
        "N": {"*": jugador.mover_norte},
        "S": {"*": jugador.mover_sur},
        "E": {"*": jugador.mover_este},
        "O": {"*": jugador.mover_oeste},
        "FIN_JUEGO": {"*": cmd_fin},
        "GUARDAR_PARTIDA": {"*": cmd_guardar},
        "CARGAR_PARTIDA": {"*": cmd_cargar},
        "DEBUG": {"*": cmd_debug},
    }
    return comandos


if __name__ == '__main__':
    main_game()
