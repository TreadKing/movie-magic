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

from app import app, db
from models import User
from auth_token import encode_auth_token, decode_auth_token

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

    #  get user info from google login
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # check if email is verified with google
    if userinfo_response.json().get("email_verified"):
        user_id = userinfo_response.json()["sub"]
        username = userinfo_response.json()["given_name"].strip()

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(user_id=user_id, username=username)
            db.session.add(user)
            db.session.commit()
        
        auth_token = encode_auth_token(user.user_id)
        print(auth_token)

        if auth_token:
            output = {
                'auth_token': auth_token, 
                'username': user.username
            }
            
            return make_response(jsonify(output)), 200

        
    else:
        return "User email not available or not verified by Google.", 400

    

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
