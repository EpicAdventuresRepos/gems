
class Resultado:
    """
    """
    HECHO    = "Éxito"
    NO_HECHO = "Fallo"
    REINICIA = "Indeterminado"
    FIN_JUEGO = "Salir del juego"


def vocabulario():
    verbos = {
        "encende": "ENCENDER",
        "abrir"  : "ABRIR",
        "coger"  : "COGER",
        "recoger": "COGER",
        "dejar"  : "DEJAR",
        "soltar" : "SOLTAR",
        "i"      : "INV",
        "inventa": "INV",
        "ver"    : "VER",
        "mirar"  : "VER",
        "m"      : "VER",
        "ex"     : "EXAMINAR",
        "examina": "EXAMINAR",
        "n"      : "N",
        "s"      : "S",
        "e"      : "E",
        "o"      : "O",
        "salir"  : "FIN_JUEGO",
        "quit"  : "FIN_JUEGO",
        "exit"  : "FIN_JUEGO",
        "termina": "FIN_JUEGO",
        "save": "GUARDAR_PARTIDA",
        "load": "CARGAR_PARTIDA",
        "debug": "DEBUG",
    }

    nombres = {
        "lintern": "LINTERNA",
        "pila"   : "PILA",
        "llave"  : "LLAVE",
        "puerta"  : "PUERTA",
    }

    return verbos, nombres



# Esto aún no lo estoy usando
class Complemento:
    Vacio = 0 # No puede llevar una segunda palabra
    Nombre = 1 # La segunda palabra debe estar en la lista de nombres
    Cadena = 2 # Debe llegvar una palabra que nos e valida con la lista de nombres
    Cualquiera = 3 # No se valida si lleva algo o no

tokens = {
    "EXAMINAR": Complemento.Nombre,
    "N": Complemento.Vacio,
    "S": Complemento.Vacio,
    "E": Complemento.Vacio,
    "O": Complemento.Vacio,
    "GUARDAR_PARTIDA": Complemento.Cadena,
    "CARGAR_PARTIDA": Complemento.Cadena
}

def comando(verbo, nombre="*"):
    verbos, nombres = vocabulario()
    token_verbo = None

    for palabra, token in verbos.items():
        if palabra == verbo:
            token_verbo = token
            break

    token_nombre = None
    if nombre == "*":
        token_nombre = nombre
    else:
        for palabra, token in nombres.items():
            if palabra == nombre:
                token_nombre = token
                break
    return Comando(verbo = verbo, nombre = nombre, token_verbo=token_verbo, token_nombre=token_nombre)


from dataclasses import dataclass

@dataclass(frozen=True)
class Comando:
    """
    Clase inmutable que representa una acción con un verbo, un nombre, y un token asociado.
    """
    verbo: str
    nombre: str
    token_verbo: str
    token_nombre: str

    def __str__(self):
        """
        Devuelve una descripción completa de la acción.
        """
        return f"Acción: {self.verbo} {self.nombre} (Tokens: {self.token_verbo}, {self.token_nombre})"