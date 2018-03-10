from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# UserMixin makes this class compatible with FlaskLogin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # backref puts a property on the Post class called, 'author'
    # so we can go from a Post and get the Author ( or User )
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, clear_password):
        self.password_hash = generate_password_hash(clear_password)

    def check_password(self, clear_password):
        return check_password_hash(self.password_hash, clear_password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        avatar_url = f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
        print(avatar_url)
        return avatar_url

@login.user_loader
def load_user(id):
    """
    Used by FlaskLogin to load a user in a persistence independent way.
    :param id:
    :return: Instance of the user for the given ID
    """
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post {self.body}>"

