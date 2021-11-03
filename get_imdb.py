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

    actor_img = r["image"]

    while i < 10:
        film_desc = r["castMovies"][i]["description"]
        if "TV Series" not in film_desc:
            film = [r["castMovies"][i]["title"], r["castMovies"][i]["id"]]
            saved_films.append(film)
        i += 1
    print(saved_films)
    display_movie(saved_films)

def display_movie(film_list):
    film_posters = []
    for i in range(len(film_list)):
        film_id = film_list[i][1]
        r = requests.get(BASE_URL + "/Title/" + API_KEY + "/" +film_id)
        r = r.json()
        film_posters.append(r["image"])
    #Some movies do not have a image url so the link will be None
    print(film_posters)
get_actorid()