import requests
import os
import json
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = "https://imdb-api.com/en/API"
API_KEY = os.getenv("API_KEY")

def get_actorid():
    r = requests.get(BASE_URL + "/SearchName/" + API_KEY + "/Jean Reno")
    r = r.json()

    actor_id = r["results"][0]["id"]
    search_actor(actor_id)

def search_actor(actor_id):
    saved_films = []
    r = requests.get(BASE_URL + "/Name/" + API_KEY + "/" +actor_id)
    r = r.json()
    i = 0
    while i < 10:
        film = r["castMovies"][i]["description"]
        if "TV Series" not in film:
            saved_films.append(r["castMovies"][i]["title"])
        i += 1
    print(saved_films)

def display_movie(film_list):
    ...
get_actorid()