import requests
import os
import json
import operator
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MOVIEDB_KEY = os.getenv("MOVIEDB_KEY")
POSTER_URL = "https://image.tmdb.org/t/p/original"


def search(query):
    """Performs two API calls, one for searching by movie name and another for searching
    by actor name"""
    if query == "":
        return Exception
    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": query}
    r = requests.get("https://api.themoviedb.org/3/search/movie", params=params)
    r = r.json()

    if r["total_results"] != 0:
        for i in range(len(r["results"])):
            film = {
                "movie_id": r["results"][i]["id"],
                "movie_title": r["results"][i]["original_title"],
                "movie_image": POSTER_URL + r["results"][i]["poster_path"],
                "rating": r["results"][i]["vote_average"],
                "on_watchlist": False,
            }
            film_list.append(film)

    # Tests if the query is a person and appends known for movies to the film list
    r = requests.get("https://api.themoviedb.org/3/search/person", params=params)
    r = r.json()
    if r["total_results"] != 0:
        for i in range(len(r["results"][0]["known_for"])):
            if (r["results"][0]["known_for"][i]["media_type"]) != "movie":
                i = i + 1
            else:
                film = {
                    "movie_id": r["results"][0]["known_for"][i]["id"],
                    "movie_title": r["results"][0]["known_for"][i]["original_title"],
                    "movie_image": POSTER_URL
                    + r["results"][0]["known_for"][i]["poster_path"],
                    "rating": r["results"][0]["known_for"][i]["vote_average"],
                    "on_watchlist": False,
                }
                film_list.append(film)

    return film_list


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


def get_upcoming():
    """Gets a list of upcoming movies and sorts them by release date"""
    movie_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "region": "US"}
    r = requests.get("https://api.themoviedb.org/3/movie/upcoming", params=params)
    r = r.json()
    for i in range(len(r["results"])):
        film = {
            "movie_title": r["results"][i]["original_title"],
            "release_date": r["results"][i]["release_date"],
            "movie_image": POSTER_URL + r["results"][i]["poster_path"],
        }
        movie_list.append(film)
    movie_list = sorted(movie_list, key=operator.itemgetter("release_date"))
    return json.dumps(movie_list)


def get_similar(movie_id):
    """Gets a list of similar films to the movie specified by the movie id"""
    similar_films = []
    params = {"movie_id": movie_id, "api_key": MOVIEDB_KEY}
    r = requests.get("https://api.themoviedb.org/3/movie/" + params)
    r = r.json()
    for i in range(len(r["results"])):
        film = {
            "movie_title": r["results"][i]["title"],
            "movie_image": POSTER_URL + r["results"][i]["poster_path"],
            "rating": r["results"][0]["known_for"][i]["vote_average"],
        }
        similar_films.append(film)
    return json.dumps(similar_films)
