import requests
import os
import json
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MOVIEDB_KEY = os.getenv("MOVIEDB_KEY")
POSTER_URL = "https://image.tmdb.org/t/p/original"


def search_movie_by_text(query):
    """Uses TheMovieDB API to find a movie by text input.
    Returns a film list where each entry is a list containing information about a specific film"""

    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": query}
    r = requests.get("https://api.themoviedb.org/3/search/movie", params=params)
    r = r.json()
    for i in range(len(r)):
        film = {
            "id": r["results"][i]["id"],
            "title": r["results"][i]["original_title"],
            "image": POSTER_URL + r["results"][i]["poster_path"],
        }
        film_list.append(film)
    return json.dumps(film_list)


def search_movie_by_actor(actor_name):
    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": actor_name}
    r = requests.get("https://api.themoviedb.org/3/search/person", params=params)
    r = r.json()
    for i in range(len(r["results"][0]["known_for"])):
        film = {
            "id": r["results"][0]["known_for"][i]["id"],
            "title": r["results"][0]["known_for"][i]["original_title"],
            "image": POSTER_URL + r["results"][0]["known_for"][i]["poster_path"],
        }
        film_list.append(film)
    print(film_list)
    return json.dumps(film_list)


def get_movie_details(movie_id):
    """Uses TheMovieDB API to get additional info about a movie.
    Returns a list containing all the genres and the summary of the movie"""

    genre_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US"}
    r = requests.get("https://api.themoviedb.org/3/movie/" + movie_id, params=params)
    r = r.json()

    for i in range(len(r["genres"])):
        genre_list.append(r["genres"][i]["name"])

    movie_info = {"genres": genre_list, "summary": r["overview"]}
    return json.dumps(movie_info)


# Gets 20 options, can get multiple pages, some of the results are old and have already released
# Example output
# ['Encanto', '2021-11-24', 'image'], ['Ghostbusters: Afterlife', '2021-11-19', 'image'], ['Resident Evil: Welcome to Raccoon City', '2021-11-24', 'image'],
# ['King Richard', '2021-11-19', 'image'], ['House of Gucci', '2021-11-24', 'image'], ['The Unforgivable', '2021-11-24', 'image']
def get_upcoming():
    """Uses TheMovieDB API"""
    movie_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "region": "US"}
    r = requests.get("https://api.themoviedb.org/3/movie/upcoming", params=params)
    r = r.json()
    for i in range(len(r["results"])):
        film = {
            "title": r["results"][i]["original_title"],
            "release_date": r["results"][i]["release_date"],
            "image": POSTER_URL + r["results"][i]["poster_path"],
        }
        movie_list.append(film)
    return json.dumps(movie_list)


def get_similar(movie_id):
    """Gets a list of similar films to the movie specified by the movie id"""
    similar_films = []
    params = {"movie_id": movie_id, "api_key": MOVIEDB_KEY}
    r = requests.get("https://appi.themoviedb.org/3/movie/" + params)
    r = r.json()
    for i in range(len(r["results"])):
        film = {
            "title": r["results"][i]["title"],
            "image": POSTER_URL + r["results"][i]["poster_path"],
        }
        similar_films.append(film)
    return json.dumps(similar_films)


# search_movie_by_text("Dune")
# get_movie_details("562")
# get_upcoming()
# get_comingSoon()
search_movie_by_actor("Alan Rickman")
