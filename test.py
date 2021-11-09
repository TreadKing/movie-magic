import firebase_admin
from firebase_admin import db
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

cred_obj = firebase_admin.credentials.Certificate({
    'type': 'service_account',
    'project_id': os.getenv('FIREBASE_PROJECT_ID'),
    'client_email': os.getenv('FIREBASE_CLIENT_EMAIL'),
    'private_key': os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    'token_uri': 'https://oauth2.googleapis.com/token'
})
default_app = firebase_admin.initialize_app(cred_obj, {"databaseURL": "https://movie-magic-db-default-rtdb.firebaseio.com"})


ref = db.reference("/")
user_id = '100372782874119952908'
users_ref = ref.child('Users').child(user_id)

user = users_ref.get()

if user:
    print(user)
else:
    print('no')