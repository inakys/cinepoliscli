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
    movies_list = get_new_releases()  # Lista de diccionarios de películas.
    

    border = "┌───────────────────────────────────────────────────────────────────────────────┐"
    separator = "├───────────────────────────────────────────────────────────────────────────────┤"
    bottom_border = "└───────────────────────────────────────────────────────────────────────────────┘"

    print(border)
    for i, movie in enumerate(movies_list):
        print(f"| Titulo: {movie['title']} | "
            f"Titulo original: {movie['original_title']} | "
            f"Año: {movie['year']} |")
        print(f"| Género: {movie['genre']} | "
            f"Director: {movie['director']} | "
            f"Actor: {movie['actor']} |")
        print(f"| País: {movie['country']} | "
            f"Fecha: {movie['day_month']} |")
        
        # Imprimir el separador si no es el último elemento de la lista
        if i < len(movies_list) - 1:
            print(separator)

    print(bottom_border)

    # Agregar las filas de la película
    # for movie in movies_list:
    #     table.add_row([
    #         movie['movie_id'], movie['title'], movie['genre'], movie['rating'], 
    #         movie['original_title'], movie['year'], movie['director'], 
    #         movie['actor'], movie['country'], movie['distributor'], movie['day_month']
    #     ])
    
    # Imprimir la tabla con un estilo más bonito
    
    
    
def print_weather():
    weather_data = [
        {"time": "Morning", "weather": "Sunny", "temp": "-2 °C", "wind": "6-13 km/h", "rain": "0.0 mm | 0%"},
        {"time": "Noon", "weather": "Sunny", "temp": "+10 °C", "wind": "17-19 km/h", "rain": "0.0 mm | 0%"},
        {"time": "Evening", "weather": "Clear", "temp": "+8 °C", "wind": "25-33 km/h", "rain": "0.0 mm | 0%"},
        {"time": "Night", "weather": "Cloudy", "temp": "+6 °C", "wind": "9-18 km/h", "rain": "0.0 mm | 0%"}
    ]




    # Creating the borders
    border = "┌──────────────────────────────┬──────────────────────────────┐"
    print(border)
    for data in weather_data:
        print(f"│ {data['time']: <20} │ {data['weather']: <20} │")
        print(f"│ Temp: {data['temp']: <18} │ Wind: {data['wind']: <18} │")
        print(f"│ Rain: {data['rain']: <18} │")
        print(border)

