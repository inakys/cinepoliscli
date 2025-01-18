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

    for article in soup.find_all("article", class_="estrenoFecha cf"):
        data_layer = article.find("div", class_="diaEstreno")
        if data_layer:
            day = data_layer.find("span").text.strip()
            day_month = day + " " + data_layer.text.replace(day, "").strip()
        
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
                    'day_month': day_month     
                }
                movies_list.append(movie_data)
                movie_id += 1
        movies_list.sort(key=lambda x: x['title']) 
    print(movies_list)
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
                "Distributor",
                "Date"
              ]
    
    print(tabulate(movies_list, headers=headers, tablefmt="grid"))