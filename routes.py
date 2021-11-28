"""
main backend for flask server.
includes routes
"""

import os
import json

# import random
from flask.templating import render_template

import requests
import flask
from flask import request, redirect, make_response, url_for
from flask.json import jsonify
from oauthlib.oauth2 import WebApplicationClient

# from requests import api

from app import app

# from models import User
from auth_token import encode_auth_token, decode_auth_token
from firebase_admin import db
from firebase_admin import auth

from get_movie import search

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
        user_id = decoded_token['uid']
        username = decoded_token["name"]

        users_ref = db.reference("/").child("users").child(str(user_id))

        if not users_ref.get():
            print(f"new user: {user_id}")
            users_ref.set({"name": username})

        else:
            print(f"user {user_id} already exists")

    except:
        print('nope')
        return 'nope'

    return 'hi'

@bp.route("/")
def home():
    """Render login page"""
    return render_template("index.html")

def on_watchlist(user_id):
    """Gets user watchlist"""
    user_watchlist = []
    ref = db.reference("users").child(user_id).child("watch_list")
    watchlist = ref.get()

    if watchlist:
        for key, value in watchlist.items():
            user_watchlist.append(key)
            print(value)

    return user_watchlist


@app.route("/search", methods=["POST", "GET"])
def search_movie():
    """The function gets all the movie ids from a user's watchlist
    and all the movie ids from the API call.
    Then a list intersection is performed to determine what movie
    ids already appear in the watchlist.
    For each value in the list intersection, the value of 'on_watchlist'
    in the API results is changed to True
    so that the Frontend JS knows what movies from the API search can not
    be added to the user's watchlist."""
    # I tested by putting a movie id 671 under by Name in the db.
    # By searching for 'Alan Rickman', the movie
    # from the search will have 'on_watchlist' = True

    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return make_response(
            jsonify({"error": "Invalid token. Please log in again."}), 500
        )

    # user_input = flask.request.form.get("user_input")
    user_input = request.json["search_key"]
    try:
        # films_on_watchlist = on_watchlist("116405330661820156295")
        films_on_watchlist = on_watchlist(user_id)

        api_results = search(user_input)
        films_from_search = []
        for item in api_results:
            films_from_search.append(str(item["movie_id"]))
        already_added = list(set(films_from_search) & set(films_on_watchlist))

        for item in already_added:
            movie_id = int(item)
            for key in api_results:
                if key["movie_id"] == movie_id:
                    key["on_watchlist"] = True
        return make_response(jsonify(api_results)), 200

    except Exception as e:
        # Give some sort of error that that actor name does not exist
        # return None
        print(e)
        return make_response(jsonify({"message": str(e)})), 500


@app.route("/getWatchList", methods=["POST"])
def get_list():
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
            }
            watch_list_output.append(watch_list_item)

    except:
        watch_list_output = []

    return make_response(jsonify(watch_list_output)), 200


@app.route("/addToWatchList", methods=["POST"])
def add_to_list():
    """After adding to the watchlist, send the user to the watchlist to see their change"""
    """
    auth_token
    movie_id
    movie_title
    movie_image
    rating
    """

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
        return make_response(jsonify({"message": "add successful"})), 200

    else:
        return make_response(jsonify({"message": "movie already in watchlist"})), 200


@app.route("/deleteFromWatchList", methods=["POST"])
def delete_from_list():
    """Find a movie object in the db and delete that entry from the watchlist"""
    print("aaa")
    print(request.json)
    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return (
            make_response(jsonify({"error": "Invalid token. Please log in again."})),
            500,
        )

    movie_id = request.json["movie_id"]
    print(movie_id)
    movie_id_ref = (
        db.reference("users").child(user_id).child("watch_list").child(str(movie_id))
    )
    movie_id_ref.set({})

    if not movie_id_ref.get():
        return make_response(jsonify({"message": "delete successful"})), 200
    else:
        return make_response(jsonify({"message": "delete not successful"})), 500


@app.route("/addToFriendslist", methods=["POST"])
def add_friend(friend_id):
    """Given a friend id, add an id to a user's friendlist"""
    # Needs to receive a user id and a friend id
    user_id = ""
    ref = db.reference("users").child(user_id).child("FriendList")
    friendlist = ref.get()

    # Insert friend id to friends list


@app.route("/deleteFromFriendsList", methods=["POST"])
def delete_friend():
    """Given a friend id, delete that id from a user's friendlist"""
    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return (
            make_response(jsonify({"error": "Invalid token. Please log in again."})),
            500,
        )

    ref = db.reference("users").child(user_id).child("FriendList")
    friendlist = ref.get()

    for key, value in friendlist.items():
        if value["friend_id"] == friend_id:
            ref.child(key).set({})

    return make_response(jsonify({"message": "delete sucessful"})), 200


@app.route("/getusers", methods=["POST"])
def getusers():
    """Query all users from db and output the list for users to view"""
    names_list = []
    ref = db.reference("users")
    names = ref.get()
    for value in names.items():
        names_list.append(value["Name"])
    # return names_list
    return render_template("users.html")


app.register_blueprint(bp)

if __name__ == "__main__":
    if os.getenv("PORT"):
        app.run(
            host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", 8080)),
            debug=True,
        )
    else:
        app.run(debug=True)
