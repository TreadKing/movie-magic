import jwt
import os

def encode_auth_token(user_id):
    try:
            payload = {
                'user_id': user_id
            }
            return jwt.encode(
                payload,
                os.environ.get("AUTH_SECRET", None),
                algorithm='HS256'
            )

    except Exception as e:
        return e

def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, os.environ.get("SECRET", None))
        return payload['sub']

    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'

    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'