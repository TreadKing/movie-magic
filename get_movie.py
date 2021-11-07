import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MOVIEDB_KEY = os.getenv("MOVIEDB_KEY")
IMDB_KEY = os.getenv("IMDB_KEY")
POSTER_URL = "https://image.tmdb.org/t/p/original"


def search_movie_by_text(query):
    """Uses TheMovieDB API to find a movie by text input.
    Returns a film list where each entry is a list containing information about a specific film"""

    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": query}
    r = requests.get("https://api.themoviedb.org/3/search/movie", params=params)
    r = r.json()
    for i in range(len(r)):
        film = ["id", "title", "image"]
        film[0] = r["results"][i]["id"]
        film[1] = r["results"][i]["original_title"]
        film[2] = POSTER_URL + r["results"][i]["poster_path"]
        film_list.append(film)
    return film_list


def get_movie_details(movie_id):
    """Uses TheMovieDB API to get additional info about a movie.
    Returns a list containing all the genres and the summary of the movie"""

    movie_info = ["genres", "summary"]
    genre_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US"}
    r = requests.get("https://api.themoviedb.org/3/movie/" + movie_id, params=params)
    r = r.json()

    for i in range(len(r["genres"])):
        genre_list.append(r["genres"][i]["name"])

    movie_info[0] = genre_list
    movie_info[1] = r["overview"]
    return movie_info


# Gets 20 options, can get multiple pages however some of the results are old and have already released
def get_upcoming():
    """Uses TheMovieDB API to get a"""
    movie_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US"}
    r = requests.get("https://api.themoviedb.org/3/movie/upcoming", params=params)
    r = r.json()
    for i in range(len(r["results"])):
        film = []
        film.append(r["results"][i]["original_title"])
        film.append(r["results"][i]["release_date"])
        movie_list.append(film)
    print(movie_list)


# Gets 19 results, up to Nov 26th
def get_comingSoon():
    movie_list = []
    r = requests.get("https://imdb-api.com/en/API/ComingSoon/" + IMDB_KEY)
    r = r.json()
    for i in range(len(r["items"])):
        film = []
        film.append(r["items"][i]["title"])
        # film.append(r["items"][i]["image"])
        film.append(r["items"][i]["releaseState"])
        movie_list.append(film)
    print(movie_list)


# search_movie_by_text("Dune")
# get_movie_details("562")
# get_upcoming()
# get_comingSoon()
