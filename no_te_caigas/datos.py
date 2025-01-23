
class Caverna:
    def __init__(self, filas, columnas):
        """Inicializa la caverna con el tamaño especificado y sin agujeros."""
        self.filas = filas
        self.columnas = columnas
        self.agujeros = set()  # Usamos un conjunto para almacenar las posiciones de los agujeros

    def agregar_agujero(self, fila, columna):
        """Agrega un agujero en la ubicación especificada."""
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.agujeros.add((fila, columna))
        else:
            raise ValueError("La posición está fuera de los límites de la caverna.")

    def casilla_final(self, jugador):
        return jugador.posicion() == (4, 4)

    def hay_agujero(self, jugador):
        """Devuelve True si hay un agujero en la ubicación especificada, False en caso contrario."""
        return jugador.posicion() in self.agujeros

    def hay_agujero_adyacente(self, jugador):
        """Devuelve True si hay un agujero en una casilla adyacente (arriba, abajo, izquierda, derecha)."""

        fila, columna = jugador.posicion()
        adyacentes = [
            (fila - 1, columna),  # Norte
            (fila + 1, columna),  # Sur
            (fila, columna - 1),  # Oeste
            (fila, columna + 1),  # Este
        ]

        for f, c in adyacentes:
            if 0 <= f < self.filas and 0 <= c < self.columnas and (f, c) in self.agujeros:
                return True
        return False

    def mostrar_caverna(self):
        """Muestra la caverna en formato de matriz, marcando los agujeros con una 'O'."""
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                if (i, j) in self.agujeros:
                    fila.append("O")  # Representación de un agujero
                else:
                    fila.append(".")  # Espacio vacío
            print(" ".join(fila))



class Jugador:
    def __init__(self, fila, columna, filas_max, columnas_max):
        """Inicializa al jugador en la posición especificada."""
        self.fila = fila
        self.columna = columna
        self.filas_max = filas_max
        self.columnas_max = columnas_max

    def mover_norte(self):
        """Mueve al jugador una fila hacia el norte (arriba)."""
        if self.fila > 0:
            self.fila -= 1
        else:
            print("Movimiento no permitido: fuera de los límites.")

    def mover_sur(self):
        """Mueve al jugador una fila hacia el sur (abajo)."""
        if self.fila < self.filas_max - 1:
            self.fila += 1
        else:
            print("Movimiento no permitido: fuera de los límites.")

    def mover_este(self):
        """Mueve al jugador una columna hacia el este (derecha)."""
        if self.columna < self.columnas_max - 1:
            self.columna += 1
        else:
            print("Movimiento no permitido: fuera de los límites.")

    def mover_oeste(self):
        """Mueve al jugador una columna hacia el oeste (izquierda)."""
        if self.columna > 0:
            self.columna -= 1
        else:
            print("Movimiento no permitido: fuera de los límites.")

    def posicion(self):
        """Devuelve la posición actual del jugador como una tupla (fila, columna)."""
        return self.fila, self.columna

    def __str__(self):
        return str(self.fila) + ", " + str(self.columna)


class Global:

    _instance = None

    @staticmethod
    def get_instance():
        """
        Devuelve la única instancia del Singleton.
        Si no existe, la crea.
        """
        if Global._instance is None:
            Global._instance = Global()
        return Global._instance

    def __init__(self):
        self._caverna = None
        self._jugador = None

    def set_caverna(self, caverna):
        self._caverna = caverna

    def caverna(self):
        return self._caverna

    def set_jugador(self, jugador):
        self._jugador = jugador

    def jugador(self):
        return self._jugador
