"""
database mododels for app
"""
from app import db

class User(db.Model):
    """
    users class for the db
    """

    user_id = db.Column(db.Float, primary_key=True)
    username = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.username}>"

    def get_username(self):
        '''
        return username
        '''
        return self.username

db.create_all()
