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
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    print(request_uri)

    return redirect('/')

    

# @app.route('/login/callback')
# def login_callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get('code')

@app.route('/')
def home():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(
        debug=True
    )
