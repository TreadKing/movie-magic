"""
main backend for flask server.
includes routes
"""

import os
import json

import random
from flask.templating import render_template

import requests
import flask
from flask import request, redirect, make_response
from flask.json import jsonify
from oauthlib.oauth2 import WebApplicationClient

# from requests import api

from app import app

# from models import User
from auth_token import encode_auth_token, decode_auth_token
from firebase_admin import db

from get_movie import search, get_upcoming, get_genres, get_similar

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


@app.route("/api/login", methods=["POST"])
def login():
    """Handles user login"""

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    print(request_uri)
    return redirect(request_uri)


@app.route("/api/login/callback")
def login_callback():
    """Handles login callback"""
    # get code from google
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    #  get user info from google login
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # check if email is verified with google
    if userinfo_response.json().get("email_verified"):
        user_id = userinfo_response.json()["sub"]
        username = userinfo_response.json()["given_name"].strip()

        auth_token = encode_auth_token(str(user_id))

        if auth_token:
            # output = {"auth_token": auth_token, "username": username}

            users_ref = db.reference("/").child("users").child(str(user_id))

            if not users_ref.get():
                print(f"new user: {user_id}")
                users_ref.set({"name": username})

            else:
                print(f"user {user_id} already exists")

            return redirect(
                flask.url_for("bp.index", auth_token=auth_token, username=username)
            )
            # return make_response(jsonify(output)), 200

            # return make_response(jsonify(output)), 200
            # return render_template("search.html")

    else:
        return make_response("User email not available or not verified by Google."), 200


@app.route("/")
def home():
    """Render login page"""
    return render_template("login.html")


@bp.route("/index")
def index():
    """Render index page"""
    # data = {
    #     "auth_token": request.args["auth_token"],
    #     "username": request.args["username"]
    # }
    # print(data)
    resp = make_response(render_template("index.html"))
    resp.set_cookie("auth_token", request.args["auth_token"])
    return resp


def on_watchlist(user_id):
    """Gets user watchlist"""
    user_watchlist = []
    ref = db.reference("users").child(user_id).child("watch_list")
    watchlist = ref.get()

    for key, value in watchlist.items():
        user_watchlist.append(key)
        print(value)
    return user_watchlist


def filter_watchlist(user_id, results):
    """This function receives a user id and a list of movie results. It then obtains a list of films
    on a user's watchlist and performs a set interesection with the list of movie results to check
    what movies are on the watchlist and set their status of on_watchlist to True in the results. It then returns results"""
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

    print(request.json)

    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return make_response(
            jsonify({"error": "Invalid token. Please log in again."}), 500
        )

    user_input = request.json["search_key"]
    try:
        genre_filter = request.json["genre"]
    except Exception:
        pass
    try:
        year_filter = request.json["year"]
        year_before_after = request.json["year_before_after"]
    except Exception:
        pass
    try:
        rating_filter = request.json["rating"]
        rating_before_after = request.json["rating_before_after"]
    except Exception:
        pass

    try:
        api_results = filter_watchlist(user_id, search(user_input))

        return make_response(jsonify(api_results)), 200

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": str(e)})), 500


@app.route("/getUpcoming", methods=["POST"])
def upcoming():
    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return make_response(
            jsonify({"error": "Invalid token. Please log in again."}), 500
        )
    try:
        upcoming_results = filter_watchlist(user_id, get_upcoming())
        return make_response(jsonify(upcoming_results)), 200
    except Exception as e:
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
        # Get random movie ids to get suggestions for
        random_index = random.randint(0, len(watch_list_output) - 1)
        random_id = watch_list_output[random_index]["movie_id"]
        movie_suggestions = get_similar(random_id)

    except Exception as e:
        watch_list_output = []
        print(e)

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


@app.route("/getUsers", methods=["POST"])
def getusers():
    """Query all users from db and output the list for users to view"""
    names_list = []
    ref = db.reference("users")
    names = ref.get()
    for i in names.items():
        names_list.append(i[1]["name"])
    return names_list


app.register_blueprint(bp)

if __name__ == "__main__":
    if os.getenv("port"):
        app.run(
            host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", 8080)),
            debug=True,
            ssl_context="adhoc",
        )
    else:
        app.run(debug=True, ssl_context="adhoc")
