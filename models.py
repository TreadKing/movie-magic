"""
database mododels for app
"""
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    """
    users class for the db
    """

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    username = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        '''
        return username
        '''
        return self.username

db.create_all()
