import requests
from bs4 import BeautifulSoup
import re

from prettytable import PrettyTable


url = "https://cinepolis.com/proximos-estrenos"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def split_data(text, patron):
    match = re.search(patron, text)
    if match:
        return match.group(1)
    return "No available"

def get_new_releases():
    movie_id = 1
    data_list = []  # Guardamos solo el último resultado

    # Recorres todos los artículos de estrenos
    for article in soup.find_all("article", class_="estrenoFecha cf"):
        # Extraes la fecha de estreno
        date_container = article.find("div", class_="diaEstreno")
        if date_container:
            day = date_container.find("span").text.strip()
            month = date_container.text.replace(day, "").strip()
            day_month = f"{day} de {month}"  # La fecha con el formato "23 de enero"

        # Ahora recorres todas las películas dentro de este artículo
        for movie in article.find_all("li"):
            data_layer = movie.find("span", class_="data-layer")
            
            if data_layer:
                title = data_layer.get("data-titulo", "No disponible")
                original_title_info = data_layer.get("data-titulooriginal", "No disponible")
                original_title = split_data(text=original_title_info, patron=r"^(.*?)(?:\s*\([^,]+,\s*(\d{4})\))")
                country = split_data(text=original_title_info, patron=r"\(([^,]+),")
                year = split_data(text=original_title_info, patron=r",\s*(\d{4})\)")
                actor = data_layer.get("data-actor", "No disponible")
                rating = data_layer.get("data-clasificacion", "No disponible")
                distributor = data_layer.get("data-distribuidora", "No disponible")
                genre = data_layer.get("data-genero", "No disponible")
                director = data_layer.get("data-director", "No disponible")
                
                # Agregas los datos de la película, incluyendo la fecha
                movie_data = {
                    'movie_id': movie_id,
                    'title': title,
                    'genre': genre,
                    'rating': rating,
                    'original_title': original_title,
                    'year': year,
                    'director': director,
                    'actor': actor,
                    'country': country,
                    'distributor': distributor,
                    'day_month': day_month  # Asociamos la fecha aquí
                }
                
                movie_id += 1  # Incrementas el ID para la siguiente película
            data_list.append(movie_data)
    # Retorna solo el último resultado
    return data_list

def print_terminal():
    # Obtener la lista de nuevas películas (diccionarios) desde la función get_new_releases()
    movies_list = get_new_releases()  # Lista de diccionarios de películas.

    # Definir los bordes para la tabla
    border = "┌───────────────────────────────────────────────────────────────────────────────┐"
    separator = "├───────────────────────────────────────────────────────────────────────────────┤"
    bottom_border = "└───────────────────────────────────────────────────────────────────────────────┘"

    # Imprimir la parte superior de la tabla
    print(border)
    
    # Iterar sobre cada película en la lista y mostrar sus datos
    for i, movie in enumerate(movies_list):
        # Imprimir la fila de la tabla con los datos de la película (Título, Título original y Año)
        print(f"| Titulo: {movie['title']} | "
              f"Titulo original: {movie['original_title']} | "
              f"Año: {movie['year']} |")
        
        # Imprimir la siguiente fila con más detalles (Género, Director y Actor)
        print(f"| Género: {movie['genre']} | "
              f"Director: {movie['director']} | "
              f"Actor: {movie['actor']} |")
        
        # Imprimir la siguiente fila con el País y la Fecha de estreno
        print(f"| País: {movie['country']} | "
              f"Fecha: {movie['day_month']} |")
        
        # Si no es el último elemento de la lista, imprimir el separador entre las películas
        if i < len(movies_list) - 1:
            print(separator)

    # Imprimir la parte inferior de la tabla
    print(bottom_border)
