import jwt
import os
from firebase_admin import auth

def encode_auth_token(user_id):
    try:
            payload = {
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.environ.get("AUTH_SECRET", None),
                algorithm="HS256"
            )

    except Exception as e:
        return e

# def decode_auth_token(auth_token):
#     try:
#         payload = jwt.decode(auth_token, os.environ.get("AUTH_SECRET", None), algorithms=["HS256"])
#         return payload['sub']

#     except jwt.ExpiredSignatureError:
#         return 'Signature expired. Please log in again.'

#     except jwt.InvalidTokenError:
#         return 'Invalid token. Please log in again.'

def decode_auth_token(auth_token):
    try: 
        id_token = auth_token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        
        return uid

    except:
        return "Invalid token. Please log in again."