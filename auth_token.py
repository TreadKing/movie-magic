"""Encodes and decodes an auth token obtained from Google"""
import os
import jwt
from firebase_admin import auth


def encode_auth_token(user_id):
    """Encodes a user's auth token"""
    try:
        payload = {"sub": user_id}
        return jwt.encode(
            payload, os.environ.get("AUTH_SECRET", None), algorithm="HS256"
        )

    except AttributeError as error:
        return error


# def decode_auth_token(auth_token):
#     try:
#         payload = jwt.decode(auth_token,
#         os.environ.get("AUTH_SECRET", None), algorithms=["HS256"])
#         return payload['sub']

#     except jwt.ExpiredSignatureError:
#         return 'Signature expired. Please log in again.'

#     except jwt.InvalidTokenError:
#         return 'Invalid token. Please log in again.'


def decode_auth_token(auth_token):
    """Decodes auth token"""
    try:
        id_token = auth_token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        print(uid)

        return uid

    except AttributeError:
        return "Invalid token. Please log in again."
