"""
main backend for flask server.
includes routes
"""

from logging import debug
import os
import json
import random
from flask.templating import render_template

import requests
import flask
from flask import request, url_for, redirect
from flask.json import jsonify
from flask_login import login_user, current_user, LoginManager, logout_user
from flask_login.utils import login_required
from oauthlib.oauth2 import WebApplicationClient

from app import app, db
from models import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Flask-Login helper to retrieve a user from our db
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/api/login', methods=['POST'])
def login():

    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )

    return redirect(request_uri)

@app.route('/api/login/callback')
def login_callback():
    # get code from google
    code = request.args.get('code')

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        user_id = userinfo_response.json()["sub"]
        email = userinfo_response.json()["email"]
        username = userinfo_response.json()["given_name"]

        print(user_id)
        print(email)
        print(username)
        
    else:
        return "User email not available or not verified by Google.", 400

    return 'hi'

    

# @app.route('/login/callback')
# def login_callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get('code')

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(
        debug=True,
        ssl_context='adhoc'
    )
