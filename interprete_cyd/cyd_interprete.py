from dataclasses import dataclass

@dataclass
class Opcion:
    label: str
    text: str


class CYD_Interprete(object):

    LABEL = "LABEL"

    def __init__(self, lista_tokens):
        self._lista = lista_tokens
        self.tokens = {"TEXT": self._text,
                  "END": self._end,
                  "OPTION": self._option,
                  "CHOOSE": self._choose,
                  "GOTO": self._goto,
                  "GOSUB": self._gosub,
                  "RETURN": self._return,
                  }
        self._indice = 0
        self._exit = False
        self._elecciones = list()
        self._opcion_actual = None
        self._indice_return = 0

    def _print_elecciones(self):
        for indice in range(0, len(self._elecciones)):
            print(f"{indice}. {self._elecciones[indice].text}")

    def _move_index_to_label(self, label):
        self._indice = 0
        while True:
            token = self._lista[self._indice]
            if token[0] == CYD_Interprete.LABEL:
                if token[1] == label:
                    # print("Salta a token: ", self._indice)
                    return
            self._indice += 1

############

    def _text(self, token):
        texto = token[1].replace('\r', '\n')
        if self._opcion_actual is None:
            print(texto)
        else:
            self._opcion_actual.text = texto
            self._elecciones.append(self._opcion_actual)
            #print(self._opcion_actual)
            self._opcion_actual = None

    def _end(self, token):
        #print("--- FIN ---")
        self._exit = True

    def _option(self, token):
        self._opcion_actual = Opcion(token[2], None)

    def _choose(self, token):
        #print(self._elecciones)
        eleccion = -1
        while eleccion < 0 or eleccion >= len(self._elecciones):
            self._print_elecciones()
            eleccion = int(input(">> "))
        self._move_index_to_label(self._elecciones[eleccion].label)
        self._elecciones = list()
        self._opcion_actual = None

    def _goto(self, token):
        self._move_index_to_label(token[1])

    def _gosub(self, token):
        self._indice_return = self._indice
        self._goto(token)

    def _return(self, token):
        self._indice = self._indice_return
        print("Vuelve a token: ", self._indice)

##########

    def ejecuta(self):
        while not self._exit:
            token = self._lista[self._indice]
            self._indice += 1
            if token[0] in self.tokens:
                # print("Ejecuta token: ", self._indice-1, " : ", token[0])
                self.tokens[token[0]](token)

        print("End.")

#--------------

if __name__ == "__main__":
    game = [('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_PICTURE',), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_DISPLAY',), ('PUSH_D', ('CONSTANT', [('C_VAL', 31)])), ('PUSH_D', ('CONSTANT', [('C_VAL', 23)])), ('POP_AT',), ('WAITKEY',), ('DECLARE', 0, 'graficos'), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_SET', ('VARIABLE', 'graficos', 0)), ('DECLARE', 1, 'ColorTexto'), ('PUSH_D', ('CONSTANT', [('C_VAL', 7)])), ('POP_SET', ('VARIABLE', 'ColorTexto', 0)), ('DECLARE', 2, 'ColorOpcion'), ('PUSH_D', ('CONSTANT', [('C_VAL', 6)])), ('POP_SET', ('VARIABLE', 'ColorOpcion', 0)), ('DECLARE', 3, 'Modo'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('DECLARE', 4, 'Imagen'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Imagen', 0)), ('PAGEPAUSE', ('CONSTANT', [('C_VAL', 1)])), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_BORDER',), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_BRIGHT',), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_FLASH',), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_PAPER',), ('CLEAR',), ('TEXT', '\r\r'), ('LABEL', 'TITULO'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r*****************************************\r*                                       *\r*                  ETPA                 *\r*                                       *\r* por R.H. Montgomery y Edward Packard  *\r*                                       *\r*****************************************\r\r   Elige tu propia aventura Volumen 00\r              versi\x18n 0.1\r\r'), ('PUSH_D', ('CONSTANT', [('C_VAL', 6)])), ('POP_INK',), ('TEXT', '      Conversi\x18n para ZX Spectrum\r\r       por An\x18nimo\r\r\r'), ('PUSH_D', ('CONSTANT', [('C_VAL', 5)])), ('POP_INK',), ('TEXT', '      Creado con ChooseYourDestiny\r\r      de Sergio Chico "cronomantic"'), ('PUSH_D', ('CONSTANT', [('C_VAL', 7)])), ('POP_INK',), ('TEXT', ' '), ('WAITKEY',), ('CLEAR',), ('TEXT', '\r'), ('PUSH_D', ('CONSTANT', [('C_VAL', 5)])), ('POP_INK',), ('TEXT', '\x11TU ERES EL PROTAGONISTA DE LA AVENTURA!'), ('PUSH_D', ('CONSTANT', [('C_VAL', 7)])), ('POP_INK',), ('TEXT', '\r\r Te has perdido en una extra\x1aa cueva, tenuemente iluminada. Gradualmente empiezas a distinguir dos t\x19neles. Uno de ellos, el de la derecha, forma una curva hacia abajo. El otro sube en pendiente hacia la izquierda.\r\r \x12Qu\x16 sucede a continuaci\x18n? Todo depende de tu elecci\x18n. \x12C\x18mo finaliza la aventura? \x11S\x18lo t\x19 puedes averiguarlo! Y lo mejor es que puedes seguir leyendo y vivir no una, sino muchas aventuras incre\x17bles.\r\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('TEXT', ' Q '), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('TEXT', ' / '), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('TEXT', ' A '), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('TEXT', ' para seleccionar las opciones.\r\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('TEXT', ' SPACE '), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('TEXT', ' / '), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('TEXT', ' ENTER '), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('TEXT', ' para elegir una opci\x18n.\r'), ('WAITKEY',), ('TEXT', '\r'), ('LABEL', 's1'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r  Ya hab\x17as pasado en anteriores ocasiones por el Ca\x1a\x18n de la Serpiente, cuando ibas en bicicleta a visitar a tu t\x17o Howard en el rancho Red Creek, pero nunca te hab\x17as fijado en la entrada de la cueva. Parece como si un desprendimiento de rocas la hubiese dejado al descubierto recientemente.\r\r  El sol de la tarde ilumina la entrada de la cueva, pero su interior permanece en la m\x15s absoluta oscuridad. Das unos pasos hacia dentro para hacerte una idea de su tama\x1ao. A medida que te vas acostumbrando a la oscuridad, empiezas a vislumbrar una especie de t\x19nel iluminado d\x16bilmente por alg\x19n tipo de material fosforescente incrustado en las rocas.\r'), ('WAITKEY',), ('CLEAR',), ('TEXT', '\r  Las paredes del t\x19nel tienen una forma suave, como si hubiesen sido modeladas por el curso del agua. Cinco o seis metros m\x15s adelante, el t\x19nel describe una curva. Te preguntas a d\x18nde conduce. Das unos pasos m\x15s. Te pone nervioso estar solo en un lugar tan extra\x1ao. Das la vuelta y sales corriendo al exterior.\r\r  A juzgar por la oscuridad que reina en el exterior, est\x15 a punto de desencadenarse una tormenta. De pronto, te das cuenta que el sol ya se ha puesto y que la \x19nica iluminaci\x18n procede de la p\x15lida luna llena. Quiz\x15s has debido quedarte dormido un par de horas. Entonces recuerdas algo que todav\x17a te resulta mucho m\x15s extra\x1ao: la noche anterior, la luna apenas estaba empezando su cuarto creciente. '), ('WAITKEY',), ('TEXT', '\r\r'), ('LABEL', 's2'), ('PUSH_D', ('CONSTANT', [('C_VAL', 2)])), ('POP_SET', ('VARIABLE', 'Imagen', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r  Empiezas a dudar del tiempo que has pasado dentro de la cueva. No tienes hambre, ni te parece que hayas podido quedarte dormido. No sabes si intentar volver a casa guiado por la luz de la luna o si esperar a que amanezca para no correr el riesgo de resbalar en el escarpado sendero.\r\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('OPTION', 0, 's4', 0, 0), ('TEXT', 'Decides volver a casa.\r\r'), ('OPTION', 0, 's5', 0, 0), ('TEXT', 'Decides esperar.\r'), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('CHOOSE',), ('TEXT', '\r\r'), ('LABEL', 's4'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r  A medida que avanzas hacia el rancho, tienes la sensaci\x18n de que el sendero no es el que t\x19 recuerdas, aunque desde luego la luz de la luna puede darle un aspecto diferente. De pronto, te das cuenta que no est\x15s caminando por un sendero, sino por algo que se asemeja al cauce seco de un r\x17o. Vuelves corriendo a la entrada de la cueva. Miras a tu alrededor y descubres que todo el paisaje ha cambiado. Parece como si una lluvia torrencial hubiese borrado todo el rastro del camino durante el rato que has estado dentro de la cueva, a pesar de que no logras ver un solo charco. Tiemblas, hace fr\x17o, mucho m\x15s del que corresponde a esta \x16poca del a\x1ao. Te pones la chaqueta que llevabas en la mochila, pero sigues sintiendo un fr\x17o terrible.\r'), ('WAITKEY',), ('CLEAR',), ('TEXT', '\r  Por fin, el paisaje empieza a aclararse. Por el este asoma un poco de luz. Pronto saldr\x15 el sol. Echas un vistazo a tu reloj y descubres que se ha parado, a pesar de que s\x18lo hace unas horas que le has dado cuerda. Parece que nada funcione correctamente.\r\r  Sabes que debes volver al rancho lo antes posible, pero de alg\x19n modo, sientes que la \x19nica forma de hacer que las cosas vuelvan a ser como antes es retornar al interior de la cueva.\r\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('OPTION', 0, 's8', 0, 0), ('TEXT', 'Sigues hacia el rancho.\r\r'), ('OPTION', 0, 's5', 0, 0), ('TEXT', 'Decides esperar a que amanezca.\r'), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('CHOOSE',), ('TEXT', '\r\r'), ('LABEL', 's5'), ('PUSH_D', ('CONSTANT', [('C_VAL', 2)])), ('POP_SET', ('VARIABLE', 'Imagen', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r  Esperas hasta la ma\x1aana siguiente, pero a medida que los rosados jirones del amanecer iluminan el cielo por el este, empieza a soplar un viento helado y amenazador.\r\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('OPTION', 0, 's6', 0, 0), ('TEXT', 'Buscas refugio.\r\r'), ('OPTION', 0, 's8', 0, 0), ('TEXT', 'Decides soportar el viento y caminar un poco mas.\r'), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('CHOOSE',), ('TEXT', '\r\r'), ('LABEL', 's6'), ('PUSH_D', ('CONSTANT', [('C_VAL', 6)])), ('POP_SET', ('VARIABLE', 'Imagen', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r  Buscas refugio en un hueco entre las rocas para protegerte de las terribles r\x15fagas de viento y te recuestas en su fondo. De repente, la roca se desmorona y resbalas por una pendiente fangosa hasta un estanque.\r\r  Cuando logras levantarte, calado hasta los huesos, y llegar hasta la hierba que cubre la orilla, el sol brilla con todo su esplendor. Miras hacia las rocas que se elevan por detr\x15s del estanque, pero no logras descubrir por d\x18nde has podido caer.\r\r  Tratas de hacerte una idea de tu situaci\x18n, cuando de pronto aparece un caballo montado por un caballero con armadura, como los de los libros de historia. La visi\x18n te resulta tan inusitada que te dan ganas de echarte a re\x17r.\r\r  El caballero levanta su casco e irrumpe en sonoras carcajadas. -\x11Menudo sitio para tomar un ba\x1ao! -grita-. De todos modos, opino que ha valido la pena, \x11Has quedado tan limpio como un cerdo!\r'), ('PUSH_I', ('VARIABLE', 'graficos', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('CP_EQ',), ('IF_N_GOTO', '__LABEL_0', 0, 0), ('GOSUB', 'WaitkeyClear', 0, 0), ('LABEL', '__LABEL_0'), ('TEXT', '\r  Est\x15 a punto de caerse del caballo a causa de las fuertes carcajadas. -Anda, sigueme y te llevar\x16 de vuelta al castillo -dice-. \r  \r  Parece feliz de tener un nuevo siervo.\r'), ('WAITKEY',), ('GOTO', 'Fin', 0, 0), ('TEXT', '\r\r'), ('LABEL', 's8'), ('PUSH_D', ('CONSTANT', [('C_VAL', 8)])), ('POP_SET', ('VARIABLE', 'Imagen', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 2)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r  A medida que aclara el d\x17a te das cuenta que no est\x15s en el buen camino. El ca\x1a\x18n parece menos profundo y el cauce del r\x17o est\x15 sembrado de cantos rodados que nunca hab\x17as visto. El viento es helado a pesar de estar en pleno verano. Al subir a un terreno m\x15s elevado descubres manchas de nieve. Desde un risco, divisas una llanura \x15rida con lagos helados y, a lo lejos, una cadena monta\x1aosa con picos cubiertos por la nieve. Empiezas a pensar que no se trata simplemente de que te hayas perdido; te has perdido en el tiempo y, por alguna extra\x1aa raz\x18n, has sido transportado varios millones de a\x1aos atr\x15s a la Edad del Hielo.\r'), ('WAITKEY',), ('CLEAR',), ('TEXT', '\r  Te diriges a una de las colinas que bordean el ca\x1a\x18n, buscando un lugar para resguardarte del viento y descubres la entrada de otra cueva.\r  '), ('PUSH_I', ('VARIABLE', 'graficos', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('CP_EQ',), ('IF_N_GOTO', '__LABEL_1', 0, 0), ('GOSUB', 'WaitkeyClear', 0, 0), ('LABEL', '__LABEL_1'), ('TEXT', '\r  Sientes la tentaci\x18n de penetrar en ella aunque piensas que deber\x17as seguir andando para ver si de alg\x19n modo logras llegar a un sitio conocido.\r\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('OPTION', 0, 's10', 0, 0), ('TEXT', 'Entras en la cueva.\r\r'), ('OPTION', 0, 's4', 0, 0), ('TEXT', 'Sigues andando.\r'), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('CHOOSE',), ('TEXT', '\r\r'), ('LABEL', 's10'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\r  Entras en la extra\x1aa cueva y te detienes hasta que logras acostumbrarte a la tenue luz ambarina que ilumina su interior. Gradualmente empiezas a distinguir un t\x19nel y se te ocurre que puede llevarte a casa.\r\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('OPTION', 0, 's11', 0, 0), ('TEXT', 'Sigue el tunel y te hundes en la oscuridad.\r\r'), ('OPTION', 0, 's8', 0, 0), ('TEXT', 'Vuelves a salir de la cueva.\r'), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('CHOOSE',), ('TEXT', '\r\r'), ('LABEL', 's11'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('GOSUB', 'Pantalla', 0, 0), ('TEXT', '\rLentamente recuperas el sentido. Est\x15s en tu cama en el rancho Red Creek contemplando a tu t\x17o Howard. A su lado est\x15 un m\x16dico amigo suyo.\r\r  -Tuviste una mala ca\x17da trepando por esas rocas del ca\x1a\x18n -dice tu t\x17o Howard-. El doctor Parsons dice que no entiende c\x18mo no te has roto ning\x19n hueso. Est\x15bamos muy preocupados pensando que te hab\x17as perdido en una de esas cuevas.\r\r  Te sientes un poco aturdido y muy d\x16bil, as\x17 que te limitas a sonre\x17r sin decir nada. De todos modos, seguro que nadie te creer\x17a. No obstante, a\x1aos despu\x16s escribes un libro acerca de tus aventuras en la Cueva del Tiempo.\r'), ('GOTO', 'Fin', 0, 0), ('TEXT', '\r\r\r'), ('TEXT', '\r\r'), ('LABEL', 'Fin'), ('TEXT', '\r'), ('PUSH_I', ('VARIABLE', 'ColorOpcion', 0)), ('POP_INK',), ('TEXT', '\rF I N'), ('TAB', ('CONSTANT', [('C_VAL', 13)])), ('PUSH_I', ('VARIABLE', 'ColorTexto', 0)), ('POP_INK',), ('WAITKEY',), ('GOTO', 's2', 0, 0), ('TEXT', '\r\r\r'), ('LABEL', 'Pantalla'), ('TEXT', '\r'), ('CLEAR',), ('PUSH_I', ('VARIABLE', 'graficos', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('CP_EQ',), ('IF_N_GOTO', '__LABEL_2', 0, 0), ('GOTO', 'Pantalla_Return', 0, 0), ('LABEL', '__LABEL_2'), ('PUSH_I', ('VARIABLE', 'Modo', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('CP_EQ',), ('IF_N_GOTO', '__LABEL_3', 0, 0), ('GOSUB', 'SoloTexto', 0, 0), ('LABEL', '__LABEL_3'), ('PUSH_I', ('VARIABLE', 'Modo', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('CP_EQ',), ('IF_N_GOTO', '__LABEL_4', 0, 0), ('GOSUB', 'ImagenIzq', 0, 0), ('LABEL', '__LABEL_4'), ('PUSH_I', ('VARIABLE', 'Modo', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 2)])), ('CP_EQ',), ('IF_N_GOTO', '__LABEL_5', 0, 0), ('GOSUB', 'ImagenSup', 0, 0), ('LABEL', '__LABEL_5'), ('LABEL', 'Pantalla_Return'), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Imagen', 0)), ('PUSH_D', ('CONSTANT', [('C_VAL', 0)])), ('POP_SET', ('VARIABLE', 'Modo', 0)), ('CLEAR',), ('RETURN',), ('TEXT', '\r\r'), ('LABEL', 'ImagenIzq'), ('PUSH_I', ('VARIABLE', 'Imagen', 0)), ('POP_PICTURE',), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_DISPLAY',), ('MARGINS', ('CONSTANT', [('C_VAL', 11)]), ('CONSTANT', [('C_VAL', 0)]), ('CONSTANT', [('C_VAL', 21)]), ('CONSTANT', [('C_VAL', 24)])), ('CLEAR',), ('MARGINS', ('CONSTANT', [('C_VAL', 12)]), ('CONSTANT', [('C_VAL', 0)]), ('CONSTANT', [('C_VAL', 20)]), ('CONSTANT', [('C_VAL', 24)])), ('RETURN',), ('TEXT', '\r\r'), ('LABEL', 'ImagenSup'), ('PUSH_I', ('VARIABLE', 'Imagen', 0)), ('POP_PICTURE',), ('PUSH_D', ('CONSTANT', [('C_VAL', 1)])), ('POP_DISPLAY',), ('MARGINS', ('CONSTANT', [('C_VAL', 0)]), ('CONSTANT', [('C_VAL', 11)]), ('CONSTANT', [('C_VAL', 32)]), ('CONSTANT', [('C_VAL', 13)])), ('CLEAR',), ('MARGINS', ('CONSTANT', [('C_VAL', 0)]), ('CONSTANT', [('C_VAL', 12)]), ('CONSTANT', [('C_VAL', 32)]), ('CONSTANT', [('C_VAL', 12)])), ('RETURN',), ('TEXT', '\r\r'), ('LABEL', 'SoloTexto'), ('MARGINS', ('CONSTANT', [('C_VAL', 0)]), ('CONSTANT', [('C_VAL', 0)]), ('CONSTANT', [('C_VAL', 32)]), ('CONSTANT', [('C_VAL', 24)])), ('RETURN',), ('TEXT', '\r\r'), ('LABEL', 'WaitkeyClear'), ('WAITKEY',), ('CLEAR',), ('RETURN',)]
    game = [('LABEL', 'inicio'), ('TEXT', '\rTienes que elegir entre dos opciones.\r\r'), ('OPTION', 0, 'inicio', 0, 0), ('TEXT', 'Vuelves a empezar.\r'), ('OPTION', 0, 'fin', 0, 0), ('TEXT', 'Terminas.\r'), ('CHOOSE',), ('TEXT', '\r'), ('LABEL', 'fin'), ('TEXT', '\r'), ('END',)]

    interprete = CYD_Interprete(game)
    interprete.ejecuta()