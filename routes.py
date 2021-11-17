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
from requests import api

from app import app

# from models import User
from auth_token import encode_auth_token, decode_auth_token
from firebase_admin import db

from get_movie import search

bp = flask.Blueprint("bp", __name__, template_folder="./build")
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

    print(request_uri)
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

            users_ref = db.reference("/").child("users").child(str(user_id))

            if not users_ref.get():
                print(f"new user: {user_id}")
                users_ref.set({"Name": username})

            else:
                print(f"user {user_id} already exists")
            
            return redirect(flask.url_for("bp.index", auth_token=auth_token, username=username))
            # return make_response(jsonify(output)), 200
            # return render_template("search.html")

    else:
        return make_response("User email not available or not verified by Google."), 200


@app.route("/")
def home():
    return render_template("login.html")

@bp.route("/index")
def index():
    # data = {
    #     "auth_token": request.args["auth_token"],
    #     "username": request.args["username"]
    # }
    # print(data)
    resp = make_response(render_template("index.html"))
    resp.set_cookie("auth_token", request.args["auth_token"])
    return resp

def on_watchlist(user_id):
    on_watchlist = []
    ref = db.reference("users").child(user_id).child("watch_list")
    watchlist = ref.get()

    for key, value in watchlist.items():
        on_watchlist.append(key)
        print(value)
    return on_watchlist


@app.route("/search", methods=["POST", "GET"])
def search_movie():
    """The function gets all the movie ids from a user's watchlist and all the movie ids from the API call.
    Then a list intersection is performed to determine what movie ids already appear in the watchlist.
    For each value in the list intersection, the value of 'on_watchlist' in the API results is changed to True
    so that the Frontend JS knows what movies from the API search can not be added to the user's watchlist."""
    # I tested by putting a movie id 671 under by Name in the db. By searching for 'Alan Rickman', the movie
    # from the search will have 'on_watchlist' = True
    print('aaaa')
    print(request.json)
    print('ASDASAAAA')
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
def getList():
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
                "comment": None
            }
            watch_list_output.append(watch_list_item)

    except:
        watch_list_output = []

    return make_response(jsonify(watch_list_output)), 200


@app.route("/addToWatchList", methods=["POST"])
def addToList():
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
        movie_id_ref.set({
            "status": 'unwatched',
            "movie_title": movie_title,
            "movie_image": movie_image,
            "rating": rating
        })

        # Send user to view their own watchlist
        return make_response(jsonify({"message": "add successful"})), 200
     
    else:
        return make_response(jsonify({"message": "movie already in watchlist"})), 200


@app.route("/deleteFromWatchList", methods=["POST"])
def deleteFromList():
    """Find a movie object in the db and delete that entry from the watchlist"""
    print('aaa')
    print(request.json)
    auth_token = request.json["auth_token"]
    user_id = decode_auth_token(auth_token)
    if user_id == "Invalid token. Please log in again.":
        return (
            make_response(jsonify({"error": "Invalid token. Please log in again."})),
            500
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
def addFriend(friend_id):
    """Given a friend id, add an id to a user's friendlist"""
    # Needs to receive a user id and a friend id
    user_id = ""
    ref = db.reference("users").child(user_id).child("FriendList")
    friendlist = ref.get()

    # Insert friend id to friends list


@app.route("/deleteFromFriendsList", methods=["POST"])
def deleteFriend():
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
    for key, value in names.items():
        names_list.append(value["Name"])
    # return names_list
    return render_template("users.html")

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(
        debug=True, ssl_context="adhoc"
    )
