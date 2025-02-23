import requests
import random
from bs4 import BeautifulSoup

urls_juegos = (
    "https://wiki.caad.club/ELF,_La_Aventura",
    "https://wiki.caad.club/Escape_Espacial_I",
    "https://wiki.caad.club/Escape_From_Desert",
    "https://wiki.caad.club/Escape_from_Happy_Hills:_Parrish_Origins",
    "https://wiki.caad.club/Espejos",
    "https://wiki.caad.club/La_Mansi%C3%B3n",
    "https://wiki.caad.club/The_Time_Machine_(Sequentia_Soft)",
    "https://wiki.caad.club/Legend",
    "https://wiki.caad.club/Los_anillos_de_Saturno",
    "https://wiki.caad.club/Los_p%C3%A1jaros_de_Bangkok",
    "https://wiki.caad.club/Nutca",
    "https://wiki.caad.club/Tribus",
    "https://wiki.caad.club/Rescate",
    "https://wiki.caad.club/Whoami",
    "https://wiki.caad.club/Zipi_y_Zape",
    "https://wiki.caad.club/Post_Mortem",
    "https://wiki.caad.club/Memorias_de_un_hobbit",
)

preguntas = {
    "Autor/es": "¿Quién es el autor (o autores) de ",
    "Compañía": "¿Qué compañía programó ",
    "Año": "¿En qué año se publicó ",
    "Plataformas": "¿En qué plataforma se publicó ",
    "Ambientación": "¿Cuál es la ambientación de ",
    "Sistema": "¿En qué sistema se programó ",
}

respuestas_correctas = 0
respuestas_incorrectas = 0

def load_page(url):
    #headers = {"User-Agent": "Mozilla/5.0"}
    headers = {"User-Agent": "Epic Agent/0.1"}
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa (código 200)
    if response.status_code == 200:
        return response.text

    # Ha habido un error
    # Raise una excepcion
    print("Error ", response.status_code)
    return None


def get_name_from(url_juego):
    nombre = url_juego.split('/')[-1]
    return nombre.replace("_", " ")
    #return nombre


def find_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table_html = soup.find("table", class_ = "infobox infobox-ltr skin-infobox ext-status-unknown")
    return str(table_html)


def table_to_dict(table_html):
    soup = BeautifulSoup(table_html, "html.parser")
    lines_html = soup.find_all("tr")
    table_dict = dict()
    for line_html in lines_html:
        cells_html = line_html.find_all("td")
        if len(cells_html) != 2:
            continue
        data_cell = cells_html[1].p
        fragment = data_cell.find("a")
        data = None
        if fragment is not None:
            # print("a ", str(fragment))
            data = fragment.string
        else:
            #print("datacell ", str(data_cell))
            #fragment = data_cell.find("p")
            #print("p ", str(fragment))
            data = data_cell.string
        """
        fragment = data_cell.find("p")
        if fragment is not None:
            print("p ", str(fragment))
            data = fragment.string
"""
        # print(cells_html[0].string, data)
        table_dict[cells_html[0].string] = data.strip()

    return table_dict


def ask_question(game_info):
    global respuestas_correctas, respuestas_incorrectas

    while True:
        clave_aleatoria = random.choice(list(preguntas.keys()))
        if clave_aleatoria in game_info:
            break

    #print(clave_aleatoria)
    #print(game_info[clave_aleatoria])
    print(preguntas[clave_aleatoria] + nombre_juego + "?")
    respuesta_case = input(">> ")
    respuesta = respuesta_case.lower()
    if respuesta == "" or respuesta == "fin" or respuesta == "salir":
        return None
    if respuesta in game_info[clave_aleatoria].lower():
        print("Correcto.")
        respuestas_correctas += 1
    else:
        print("Incorrecto. La respueta es", game_info[clave_aleatoria])
        respuestas_incorrectas += 1
    return "Mas"


if __name__ == "__main__":
    page_html = None
    loop = "no"
    while loop is not None:
        random_int = random.randint(0, len(urls_juegos))
        #print(random_int)
        page_html = load_page(urls_juegos[random_int])
        #print("Page loaded.")
        nombre_juego = get_name_from(urls_juegos[random_int])
        #print(nombre_juego)
        table_html = find_table(page_html)
        # print("Table found: ", table_html)
        game_info = table_to_dict(table_html)
        #print("Game info: ", game_info)
        loop = ask_question(game_info)

    print("Preguntas totales: ", (respuestas_correctas + respuestas_incorrectas))
    print("Correctas: ", respuestas_correctas)
    print("Incorrectas: ", respuestas_incorrectas)


