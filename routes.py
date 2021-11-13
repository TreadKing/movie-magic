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
from flask import request, url_for, redirect, make_response
from flask.json import jsonify
from oauthlib.oauth2 import WebApplicationClient

from app import app

# from models import User
from auth_token import encode_auth_token, decode_auth_token
from firebase_admin import db

from get_movie import search

ref = db.reference("/")


# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/api/login", methods=["POST"])
def login():

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


@app.route("/api/login/callback")
def login_callback():
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
            output = {"auth_token": auth_token, "username": username}

            users_ref = ref.child("Users").child(str(user_id))
            if not users_ref.get():
                print(f"new user: {user_id}")
                users_ref.set({"Name": username})

            else:
                print(f"user {user_id} already exists")

            # return make_response(jsonify(output)), 200
            return render_template("search.html")

    else:
        return "User email not available or not verified by Google.", 400


@app.route("/")
def home():
    # If user is already logged in, skip this step
    return render_template("login.html")


def on_watchlist(user_id):
    on_watchlist = []
    ref = db.reference("Users").child(user_id).child("WatchList")
    watchlist = ref.get()

    for key, value in watchlist.items():
        on_watchlist.append(key)
    return on_watchlist


@app.route("/search", methods=["POST", "GET"])
def search_movie():

    user_input = flask.request.form.get("user_input")
    try:
        films_on_watchlist = on_watchlist("100372782874119952908")
        api_results = search(user_input)
        films_from_search = []
        for item in api_results:
            films_from_search.append(str(item["movie_id"]))
        already_added = list(set(films_from_search) & set(films_on_watchlist))

        results = {"api_results": api_results, "on_watchlist": already_added}

        return render_template("search.html")
    except Exception:
        # Give some sort of error that that actor name does not exist
        # return None
        print("Error")
        return render_template("search.html")


@app.route("/getWatchlist", methods=["POST"])
def getList():
    """Gets information from db to output to the user their watchlist"""
    # From the frontend, it fetches /getWatchlist with options containing "userId"
    # Then return list of dictionaries containing {"movie_id", "movie_title", "movie_image","rating"}

    # Needs to receive a user_id
    user_id = ""  # 100372782874119952908 Sample id to use
    ref = db.reference("Users").child(user_id).child("WatchList")
    watchlist = ref.get()

    return watchlist


@app.route("/addToWatchlist", methods=["POST"])
def addToList(movie_id):
    """After adding to the watchlist, send the user to the watchlist to see their change"""
    # Needs to receieve a movie id and a user id
    user_id = ""
    ref = db.reference("Users").child(user_id).child("WatchList")
    watchlist = ref.get()

    # Add movie_id to out database
    # return "", 200


@app.route("/deleteFromWatchlist", methods=["POST"])
def deleteFromList(movie_id):
    """Find a movie object in the db and delete that entry from the watchlist"""

    # Needs to receive a movie id and a user id
    user_id = ""
    ref = db.reference("Users").child(user_id).child("WatchList")
    watchlist = ref.get()

    for key, value in watchlist.items():
        if value["movie_id"] == movie_id:
            ref.child(key).set({})
    return "", 200


@app.route("/addToFriendslist", methods=["POST"])
def addFriend(friend_id):
    """Given a friend id, add an id to a user's friendlist"""
    # Needs to receive a user id and a friend id
    user_id = ""
    ref = db.reference("Users").child(user_id).child("FriendList")
    friendlist = ref.get()

    # Insert friend id to friends list


@app.route("/deleteFromFriendsList", methods=["POST"])
def deleteFriend(friend_id):
    """Given a friend id, delete that id from a user's friendlist"""
    # Needs to receive a user id and a friend id
    user_id = ""
    ref = db.reference("Users").child(user_id).child("FriendList")
    friendlist = ref.get()

    for key, value in friendlist.items():
        if value["friend_id"] == friend_id:
            ref.child(key).set({})


@app.route("/getUsers", methods=["POST"])
def getUsers():
    """Query all users from db and output the list for users to view"""
    names_list = []
    ref = db.reference("Users")
    names = ref.get()
    for key, value in names.items():
        names_list.append(value["Name"])
    # return names_list
    return render_template("users.html")


if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc")
