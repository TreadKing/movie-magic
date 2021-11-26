"""
handles enviroment variable, flask app, and db initial setup
"""
import os

import flask
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import firebase_admin

cred_obj = firebase_admin.credentials.Certificate({
    'type': 'service_account',
    'project_id': os.getenv('FIREBASE_PROJECT_ID'),
    'client_email': os.getenv('FIREBASE_CLIENT_EMAIL'),
    'private_key': os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    'token_uri': 'https://oauth2.googleapis.com/token'
})
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": "https://movie-magic-db-default-rtdb.firebaseio.com"})


app = flask.Flask(__name__, static_folder="./build/static")
