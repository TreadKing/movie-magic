"""This file contains api functions that are utilized throughout the app"""
import json
import os
import operator
import requests

from dotenv import find_dotenv, load_dotenv
from datetime import date, datetime

load_dotenv(find_dotenv())

MOVIEDB_KEY = os.getenv("MOVIEDB_KEY")
POSTER_URL = "https://image.tmdb.org/t/p/original"


def get_genres(movie_id):
    """Uses TheMovieDB API to get additional info about a movie.
    Returns a list containing all the genres and the summary of the movie"""

    genre_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US"}
    r = requests.get(
        "https://api.themoviedb.org/3/movie/" + str(movie_id), params=params
    )
    r = r.json()

    for i in range(len(r["genres"])):
        genre_list.append(r["genres"][i]["name"])

    return genre_list


def search_actor(query, filters):
    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": query}
    r = requests.get("https://api.themoviedb.org/3/search/movie", params=params)
    r = r.json()

    if r["total_results"] != 0:
        for i in range(len(r["results"])):
            # Split out the movie info and perform try excepts to prevent errors if there is no rating or image link
            movie_id = r["results"][i]["id"]
            movie_title = r["results"][i]["original_title"]
            genres = get_genres(r["results"][i]["id"])
            release_date = r["results"][i]["release_date"]
            try:
                image_link = r["results"][i]["poster_path"]
            except:
                image_link = ""
            try:
                rating = r["results"][i]["vote_average"]
            except:
                rating = None
            # Check if there are any filters. If not we can go ahead and add the film to film_list. Otherwise, perform filtering
            if (
                filters["genre_filter"] != ""
                or filters["rating_filter"] != ""
                or filters["year_filter"] != ""
            ):
                # If genre filter is not empty, set the genre_to_look_for as the string in genre_filter.
                # Compare the genres of the current film and see if the target genre is there. Otherwise, look at the next movie
                if filters["genre_filter"] != "":
                    genre_to_look_for = filters["genre_filter"]
                    if genre_to_look_for not in genres:
                        continue
                if filters["rating_filter"] != "":
                    rating_to_look_for = filters["rating_filter"]
                    if filters["rating_before_after"] == True:
                        # We include movies where the rating is above the rating_to_look_for
                        if rating == None or rating < rating_to_look_for:
                            continue
                    else:
                        if rating == None or rating > rating_to_look_for:
                            continue
                if filters["year_filter"] != "":
                    release_year = datetime.strptime(release_date, "%Y-%m-%d")
                    year_to_look_for = filters["year_filter"]
                    if filters["year_before_after"] == True:
                        # We include movies where the year is greater than the year_to_look_for
                        if release_year.year < year_to_look_for:
                            continue
                    else:
                        if release_year.year < year_to_look_for:
                            continue
            film = {
                "movie_id": movie_id,
                "movie_title": movie_title,
                "movie_image": POSTER_URL + image_link,
                "genres": genres,
                "release_date": r["results"][i]["release_date"],
                "rating": rating,
                "on_watchlist": False,
            }
            film_list.append(film)
    return film_list


def search_movie(query, filters):
    # Tests if the query is a person and appends known for movies to the film list
    film_list = []
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "query": query}
    r = requests.get("https://api.themoviedb.org/3/search/person", params=params)
    r = r.json()
    if r["total_results"] != 0:
        for i in range(len(r["results"][0]["known_for"])):
            if (r["results"][0]["known_for"][i]["media_type"]) != "movie":
                i = i + 1
            else:
                movie_id = r["results"][0]["known_for"][i]["id"]
                movie_title = r["results"][0]["known_for"][i]["original_title"]
                genres = get_genres(r["results"][i]["id"])
                release_date = r["results"][0]["known_for"][i]["release_date"]
                try:
                    image_link = r["results"][0]["known_for"][i]["poster_path"]
                except:
                    image_link = ""
                try:
                    rating = r["results"][0]["known_for"][i]["vote_average"]
                except:
                    rating = None
                if (
                    filters["genre_filter"] != ""
                    or filters["rating_filter"] != ""
                    or filters["year_filter"] != ""
                ):
                    if filters["genre_filter"] != "":
                        genre_to_look_for = filters["genre_filter"]
                        if genre_to_look_for not in genres:
                            continue
                    if filters["rating_filter"] != "":
                        rating_to_look_for = filters["rating_filter"]
                        if filters["rating_before_after"] == True:
                            # We include movies where the rating is above the rating_to_look_for
                            if rating == None or rating < rating_to_look_for:
                                continue
                        else:
                            if rating == None or rating > rating_to_look_for:
                                continue
                    if filters["year_filter"] != "":
                        release_year = datetime.strptime(release_date, "%Y-%m-%d")
                        year_to_look_for = filters["year_filter"]
                        if filters["year_before_after"] == True:
                            # We include movies where the year is greater than the year_to_look_for
                            if release_year.year < year_to_look_for:
                                continue
                        else:
                            if release_year.year < year_to_look_for:
                                continue
                film = {
                    "movie_id": movie_id,
                    "movie_title": movie_title,
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
        return Exception
    film_list = []
    film_list.append(search_actor(query, filters))
    film_list.append(search_movie(query, filters))

    return film_list


def get_upcoming():
    """Gets a list of upcoming movies and sorts them by release date"""
    movie_list = []
    date_today = date.today()
    params = {"api_key": MOVIEDB_KEY, "language": "en-US", "region": "US"}
    r = requests.get("https://api.themoviedb.org/3/movie/upcoming", params=params)
    r = r.json()
    for i in range(len(r["results"])):
        movie_date = r["results"][i]["release_date"]
        release_date = datetime.strptime(movie_date, "%Y-%m-%d").date()
        if release_date > date_today:
            film = {
                "movie_id": r["results"][i]["id"],
                "movie_title": r["results"][i]["original_title"],
                "movie_image": POSTER_URL + r["results"][i]["poster_path"],
                "genres": get_genres(r["results"][i]["id"]),
                "release_date": r["results"][i]["release_date"],
                "on_watchlist": False,
            }
            movie_list.append(film)
    movie_list = sorted(movie_list, key=operator.itemgetter("release_date"))
    return json.dumps(movie_list)


def get_similar(movie_id):
    """Gets a list of similar films to the movie specified by the movie id"""
    similar_films = []
    params = {"api_key": MOVIEDB_KEY}

    r = requests.get(
        "https://api.themoviedb.org/3/movie/" + str(movie_id) + "/similar", params
    )

    r = r.json()
    for i in range(len(r["results"])):
        film = {
            "movie_id": r["results"][i]["id"],
            "movie_title": r["results"][i]["title"],
            "movie_image": POSTER_URL + r["results"][i]["poster_path"],
            "rating": r["results"][i]["vote_average"],
            "genres": get_genres(r["results"][i]["id"]),
            "release_date": r["results"][i]["release_date"],
            "on_watchlist": False,
        }
        similar_films.append(film)
    return similar_films
