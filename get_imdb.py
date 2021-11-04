import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = "https://imdb-api.com/en/API"
API_KEY = os.getenv("API_KEY")

# The search assumes the first option is the intended actor
def get_actorid(actor_name):
    # Replace Jean Reno with actor_name
    r = requests.get(BASE_URL + "/SearchName/" + API_KEY + "/Jean Reno")
    r = r.json()

    actor_id = r["results"][0]["id"]
    search_movies(actor_id)


# search_movies should accept a watchlist so that movies already added will not be shown
# Should change i to count and provide a reason why 10 films are returned
def search_movies(actor_id):
    saved_films = []
    r = requests.get(BASE_URL + "/Name/" + API_KEY + "/" + actor_id)
    r = r.json()
    i = 0

    actor_img = r["image"]

    while i < 10 and i < len(r["castMovies"]):
        film_desc = r["castMovies"][i]["description"]
        if "TV Series" not in film_desc:
            film = [r["castMovies"][i]["title"], r["castMovies"][i]["id"]]
            saved_films.append(film)
        i += 1
    print(saved_films)


def display_movie(film_list):
    film_posters = []
    for i in range(len(film_list)):
        film_id = film_list[i][1]
        r = requests.get(BASE_URL + "/Title/" + API_KEY + "/" + film_id)
        r = r.json()
        film_posters.append(r["image"])
    # Some movies do not have a image url so the link will be None
    print(film_posters)


# Gets the movie poster, genre, and similar movies about the provided film id
def get_movie_info(film_id):
    saved_info = ["D"] * 3
    similar_movies = []
    r = requests.get(BASE_URL + "/Title/" + API_KEY + "/" + film_id)
    r = r.json()
    saved_info[0] = r["image"]  # Saves the movie poster associated with the film
    saved_info[1] = r["genres"]  # Saves a String of the genres associated with the film
    # Saves film id and title pairs that are similar to the film
    for i in range(len(r["similars"])):
        film_combo = []
        film_combo.append(r["similars"][i]["id"])
        film_combo.append(r["similars"][i]["title"])
        similar_movies.append(film_combo)

    saved_info[2] = similar_movies
    print(saved_info)
