"""This file contains api functions that are utilized throughout the app"""
import json
import os
import operator
from datetime import date, datetime
import requests

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

MOVIEDB_KEY = os.getenv("MOVIEDB_KEY")
POSTER_URL = "https://image.tmdb.org/t/p/original"


def get_genres(movie_id):
    """Uses TheMovieDB API to get additional info about a movie.
    Returns a list containing all the genres and the summary of the movie"""

    genre_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US"}
    request = requests.get(
        "https://api.themoviedb.org/3/movie/" + str(movie_id), params=params
    )
    request = request.json()

    for i in range(len(request["genres"])):
        genre_list.append(request["genres"][i]["name"])

    return genre_list


def check_genre(genres, target_genre):
    """Checks if a movie contains the specified genre. Returns true/false"""
    if target_genre not in genres:
        return False
    return True


def check_year(target_year, movie_release_year, year_before_after):
    """Checks if a movie release year is greater than or less than the specified year"""
    # print(movie_release_year)
    # print(target_year)
    if year_before_after == 'false':
        # print('after')
        if int(movie_release_year) < int(target_year):
            return False
    else:
        # print('before')
        if int(movie_release_year) > int(target_year):
            return False
    return True


def check_rating(target_rating, movie_rating, rating_to_look_for):
    """Checks if a movie is rated greater than or less than a given rating"""
    print(rating_to_look_for)
    if rating_to_look_for == 'false':
        # We include movies where the rating is above the rating_to_look_for
        print(movie_rating)
        print(target_rating)
        if movie_rating < target_rating:
            return False
    else:
        if movie_rating > target_rating:
            return False
    return True


def search_movie(query, filters):
    """Finds a movie based on title"""
    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": query}
    request = requests.get("https://api.themoviedb.org/3/search/movie", params=params)
    request = request.json()

    if request["total_results"] != 0:
        for i in range(len(request["results"])):
            # Split out the movie info and perform try excepts to
            # prevent errors if there is no rating or image link
            genres = get_genres(request["results"][i]["id"])
            release_date = request["results"][i]["release_date"]
            if request["results"][i]["poster_path"] is not None:
                image_link = request["results"][i]["poster_path"]
            else:
                image_link = ""
            if request["results"][i]["vote_average"] is not None:
                rating = request["results"][i]["vote_average"]
            else:
                rating = 0
            if filters["genre_filter"] is not "":
                genre_to_look_for = filters["genre_filter"]
                if not check_genre(genres, genre_to_look_for):
                    continue
            if filters["rating_filter"] is not None:
                if not check_rating(
                    filters["rating_filter"], rating, filters["rating_before_after"]
                ):
                    continue
            if filters["year_filter"] is not None:
                release_year = release_date[:4]
                if check_year(
                    release_year,
                    filters["year_filter"],
                    filters["year_before_after"],
                ):
                    continue
            film = {
                "movie_id": request["results"][i]["id"],
                "movie_title": request["results"][i]["original_title"],
                "movie_image": POSTER_URL + image_link,
                "genres": genres,
                "release_date": release_date,
                "rating": rating,
                "on_watchlist": False,
            }
            film_list.append(film)
    return film_list


def search_actor(query, filters):
    """Searches for movies based on actor name"""
    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": query}
    request = requests.get("https://api.themoviedb.org/3/search/person", params=params)
    request = request.json()
    if request["total_results"] != 0:
        for i in range(len(request["results"][0]["known_for"])):
            if (request["results"][0]["known_for"][i]["media_type"]) != "movie":
                i = i + 1
            else:
                genres = get_genres(request["results"][0]["known_for"][i]["id"])
                release_date = request["results"][0]["known_for"][i]["release_date"]
                rating = None
                try:
                    image_link = request["results"][0]["known_for"][i]["poster_path"]
                except KeyError:
                    image_link = ""
                try:
                    rating = request["results"][0]["known_for"][i]["vote_average"]
                except KeyError:
                    rating = None
                if filters["genre_filter"] != "":
                    genre_to_look_for = filters["genre_filter"]
                    if not check_genre(genres, genre_to_look_for):
                        continue
                if filters["rating_filter"] is not None:
                    if not check_rating(
                        filters["rating_filter"], rating, filters["rating_before_after"]
                    ):
                        continue
                if filters["year_filter"] is not None:
                    release_year = release_date[:4]
                    year_to_look_for = filters["year_filter"]
                    if check_year(
                        filters["year_filter"], release_year, year_to_look_for
                    ):
                        continue
                film = {
                    "movie_id": request["results"][0]["known_for"][i]["id"],
                    "movie_title": request["results"][0]["known_for"][i][
                        "original_title"
                    ],
                    "movie_image": POSTER_URL + image_link,
                    "genres": genres,
                    "release_date": release_date,
                    "rating": rating,
                    "on_watchlist": False,
                }
                film_list.append(film)
    return film_list


def search(query, filters):
    """Performs two API calls, one for searching by movie name and another for searching
    by actor name"""
    if query == "":
        return None
    film_by_actor = search_actor(query, filters)
    film_by_name = search_movie(query, filters)
    film_list = film_by_actor + film_by_name
    return film_list


def get_upcoming():
    """Gets a list of upcoming movies and sorts them by release date"""
    movie_list = []
    date_today = date.today()
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "region": "US"}
    request = requests.get("https://api.themoviedb.org/3/movie/upcoming", params=params)
    request = request.json()
    for i in range(len(request["results"])):
        movie_date = request["results"][i]["release_date"]
        release_date = datetime.strptime(movie_date, "%Y-%m-%d").date()
        if release_date > date_today:
            film = {
                "movie_id": request["results"][i]["id"],
                "movie_title": request["results"][i]["original_title"],
                "movie_image": POSTER_URL + request["results"][i]["poster_path"],
                "genres": get_genres(request["results"][i]["id"]),
                "release_date": request["results"][i]["release_date"],
                "on_watchlist": False,
            }
            movie_list.append(film)
    movie_list = sorted(movie_list, key=operator.itemgetter("release_date"))
    return movie_list


def get_similar(movie_id):
    """Gets a list of similar films to the movie specified by the movie id"""
    similar_films = []
    params = {"api_key": MOVIEDB_KEY}

    request = requests.get(
        "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/similar", params
    )

    request = request.json()
    for i in range(len(request["results"])):
        film = {
            "movie_id": request["results"][i]["id"],
            "movie_title": request["results"][i]["title"],
            "movie_image": POSTER_URL + request["results"][i]["poster_path"],
            "rating": request["results"][i]["vote_average"],
            "genres": get_genres(request["results"][i]["id"]),
            "release_date": request["results"][i]["release_date"],
            "on_watchlist": False,
        }
        similar_films.append(film)
    return similar_films


filters = {
    "genre_filter": "",
    "year_filter": None,
    "year_before_after": False,
    "rating_filter": None,
    "rating_before_after": False,
}
# search("Rush Hour", filters)

# print(search("dune", filters))