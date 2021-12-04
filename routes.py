"""
main backend for flask server.
includes routes
"""

import os

from flask.templating import render_template

import requests
import flask
from flask import request, make_response
from flask.json import jsonify
from oauthlib.oauth2 import WebApplicationClient

# from requests import api
from firebase_admin import auth, db

# pylint: disable=E0401
from app import app

# pylint: disable=E0401
from auth_token import decode_auth_token

# pylint: disable=E0401
from get_movie import search, get_upcoming, get_similar

bp = flask.Blueprint("bp", __name__, template_folder="./build")
# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    """Gets google provider configuration"""
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login", methods=["POST"])
def new_login():
    """Handles user login"""
    try:
        id_token = request.json["access_token"]
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]
        username = decoded_token["name"]

        users_ref = db.reference("/").child("users").child(str(user_id))

        if not users_ref.get():
            # print(f"new user: {user_id}")
            users_ref.set({"name": username})
            return make_response(jsonify({"message": "new user added"})), 200

        msg = f"user {user_id} already exists"
        # print(msg)
        return make_response(jsonify({"message": msg})), 200

    except AttributeError as error:
        # print(error)
        return make_response(jsonify({"message": str(error)})), 500


@bp.route("/")
def home():
    """Render login page"""
    return render_template("index.html")


def on_watchlist(user_id):
    """Gets user watchlist"""
    user_watchlist = []
    ref = db.reference("users").child(user_id).child("watch_list")
    watchlist = ref.get()

    if not watchlist:
        return user_watchlist

    for key in watchlist.items():
        user_watchlist.append(key[0])

    return user_watchlist


def filter_watchlist(user_id, results):
    """This function receives a user id and a list of movie results.
    It then obtains a list of films
    on a user's watchlist and performs a set interesection with
    the list of movie results to check
    what movies are on the watchlist and set their status of
    on_watchlist to True in the results.
    It then returns results"""
    films_on_watchlist = on_watchlist(user_id)

    films_from_results = []

    for item in results:
        films_from_results.append(str(item["movie_id"]))
    already_added = list(set(films_from_results) & set(films_on_watchlist))

    for item in already_added:
        movie_id = int(item)
        for key in results:
            if key["movie_id"] == movie_id:
                key["on_watchlist"] = True
    return results


@app.route("/search", methods=["POST", "GET"])
def search_movie():
    """Retrieves a list of movies that match the input query"""
    # print(request.json)

    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return make_response(
            jsonify({"error": "Invalid token. Please log in again."}), 500
        )
    filters = {
        "genre_filter": "",
        "year_filter": None,
        "year_before_after": False,
        "rating_filter": None,
        "rating_before_after": False,
    }
    user_input = request.json["search_key"]

    try:
        genre_filter = request.json["genre"]
        if not genre_filter:
            filters["genre_filter"] = ""
        else:
            filters["genre_filter"] = genre_filter
    except KeyError:
        pass
    try:
        year_filter = request.json["year"]
        year_before_after = request.json["year_before_after"]
        filters["year_filter"] = year_filter
        filters["year_before_after"] = year_before_after
    except KeyError:
        pass
    try:
        rating_filter = request.json["rating"]
        rating_before_after = request.json["rating_before_after"]
        if rating_filter:
            filters["rating_filter"] = int(rating_filter)
        else:
            filters["rating_filter"] = rating_filter
        filters["rating_before_after"] = rating_before_after
    except KeyError:
        pass

    try:
        # print(search(user_input, filters))
        api_results = filter_watchlist(user_id, search(user_input, filters))

        return make_response(jsonify(api_results)), 200

    except KeyError as error:
        return make_response(jsonify({"message": str(error)})), 500


@app.route("/getSimilar", methods=["POST"])
def similar():
    """Gets information from db to output to the user their watchlist"""
    # Query information from db pertaining to user

    auth_token = request.json["auth_token"]
    movie_id = request.json["movie_id"]

    user_id = decode_auth_token(auth_token)

    if user_id == "Invalid token. Please log in again.":
        return (
            make_response(jsonify({"error": "Invalid token. Please log in again."})),
            500,
        )

    try:
        similar_movies = get_similar(movie_id)

    except KeyError:
        similar_movies = []

    return make_response(jsonify(similar_movies)), 200


@app.route("/getUpcoming", methods=["POST"])
def upcoming():
    """Get a list of upcoming movies"""
    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return make_response(
            jsonify({"error": "Invalid token. Please log in again."}), 500
        )
    try:
        upcoming_results = filter_watchlist(user_id, get_upcoming())
        return make_response(jsonify(upcoming_results)), 200
    except KeyError as error:
        return make_response(jsonify({"message": str(error)})), 500


@app.route("/getWatchList", methods=["POST"])
def get_list():
    """Gets information from db to output to the user their watchlist"""

    auth_token = request.json["auth_token"]

    user_id = decode_auth_token(auth_token)

    if user_id == "Invalid token. Please log in again.":
        return (
            make_response(jsonify({"error": "Invalid token. Please log in again."})),
            500,
        )

    watch_list_ref = (
        db.reference("/").child("users").child(str(user_id)).child("watch_list")
    )
    watch_list = watch_list_ref.get()

    try:
        watch_list_output = []
        for key in watch_list:
            watch_list_item = {
                "movie_id": key,
                "movie_title": watch_list[key]["movie_title"],
                "movie_image": watch_list[key]["movie_image"],
                "rating": watch_list[key]["rating"],
                "status": watch_list[key]["status"],
                "comment": None,
                "on_watchlist": True,
            }
            watch_list_output.append(watch_list_item)

    except TypeError:
        watch_list_output = []

    return make_response(jsonify(watch_list_output)), 200


@app.route("/getOtherUsersWatchlist", methods=["POST"])
def get_other_watchlist(friend_id):
    """Gets information from db to output to the user their watchlist"""
    # Query information from db pertaining to user

    auth_token = request.json["auth_token"]

    user_id = decode_auth_token(auth_token)

    if user_id == "Invalid token. Please log in again.":
        return (
            make_response(jsonify({"error": "Invalid token. Please log in again."})),
            500,
        )

    watch_list_ref = (
        db.reference("/").child("users").child(str(friend_id)).child("watch_list")
    )
    watch_list = watch_list_ref.get()

    try:
        watch_list_output = []
        for key in watch_list:
            watch_list_item = {
                "movie_id": key,
                "movie_title": watch_list[key]["movie_title"],
                "movie_image": watch_list[key]["movie_image"],
                "rating": watch_list[key]["rating"],
                "status": watch_list[key]["status"],
                "comment": None,
            }
            watch_list_output.append(watch_list_item)

    except KeyError:
        watch_list_output = []
    return make_response(jsonify(watch_list_output)), 200


@app.route("/addToWatchList", methods=["POST"])
def add_to_list():
    """After adding to the watchlist, send the user to the watchlist to see their change"""

    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return make_response(
            jsonify({"error": "Invalid token. Please log in again."}), 500
        )

    # status = request.json["Status"]
    movie_id = request.json["movie_id"]
    movie_title = request.json["movie_title"]
    movie_image = request.json["movie_image"]
    rating = request.json["rating"]
    status = request.json["status"]

    movie_id_ref = (
        db.reference("/")
        .child("users")
        .child(str(user_id))
        .child("watch_list")
        .child(str(movie_id))
    )

    if not movie_id_ref.get():
        movie_id_ref.set(
            {
                "status": "unwatched",
                "movie_title": movie_title,
                "movie_image": movie_image,
                "rating": rating,
            }
        )

        # Send user to view their own watchlist
    else:
        # print(status)
        # movie_id_ref.set({})
        movie_id_ref.set(
            {
                "status": status,
                "movie_title": movie_title,
                "movie_image": movie_image,
                "rating": rating,
            }
        )
        return make_response(jsonify({"message": "movie already in watchlist"})), 200
    return make_response(jsonify({"message": "add successful"})), 200


@app.route("/deleteFromWatchList", methods=["POST"])
def delete_from_list():
    """Find a movie object in the db and delete that entry from the watchlist"""
    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return (
            make_response(jsonify({"error": "Invalid token. Please log in again."})),
            500,
        )

    movie_id = request.json["movie_id"]
    movie_id_ref = (
        db.reference("users").child(user_id).child("watch_list").child(str(movie_id))
    )
    movie_id_ref.set({})

    if not movie_id_ref.get():
        return make_response(jsonify({"message": "delete successful"})), 200
    return make_response(jsonify({"message": "delete not successful"})), 500


@app.route("/getUsers", methods=["POST"])
def getusers():
    """Query all users from db and output the list for users to view"""
    users_list = []
    ref = db.reference("users")
    names = ref.get()
    for i in names.items():
        user = {"id": i, "name": i[1]["name"]}
        users_list.append(user)
    return users_list


app.register_blueprint(bp)
# pylint: disable=W1508
if __name__ == "__main__":
    if os.getenv("PORT"):
        app.run(
            host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", 8080)),
        )
    else:
        app.run(debug=True)
