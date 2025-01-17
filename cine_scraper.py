import requests
from bs4 import BeautifulSoup
import re
from tabulate import tabulate

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
    movies_list = []
    for movie in soup.find_all("li"):
        data_layer = movie.find("span", class_="data-layer")
        
        if data_layer:
            title = data_layer.get("data-titulo", "No available")
            og_title_info = data_layer.get("data-titulooriginal", "No available")
            original_title = split_data(text=og_title_info, patron=r"^(.*?)(?:\s*\([^,]+,\s*(\d{4})\))")
            country = split_data(text=og_title_info, patron=r"\(([^,]+),")
            year = split_data(text=og_title_info, patron=r",\s*(\d{4})\)")
            actor = data_layer.get("data-actor", "No available")
            rating = data_layer.get("data-clasificacion", "No available")
            distributor = data_layer.get("data-distribuidora", "No available")
            genre = data_layer.get("data-genero", "No available")
            director = data_layer.get("data-director", "No available")
            
            movie_data = [
                movie_id,
                title,          # Título
                genre,          # Género
                rating,         # Calificación
                original_title, # Título original
                year,           # Año
                director,       # Director
                actor,          # Actor
                country,        # País
                distributor     # Distribuidor
            ]
            
            movies_list.append(movie_data)
            movie_id += 1
        movies_list.sort(key=lambda x: x[1])  

    return movies_list

def print_terminal():
    movies_list = get_new_releases()
    
    headers = [
                "ID", 
                "Title", 
                "Genre",
                "Rating",
                "Original Title",
                "Year",
                "Director",
                "Actor",
                "Country",
                "Distributor"
              ]
    
    print(tabulate(movies_list, headers=headers, tablefmt="grid"))