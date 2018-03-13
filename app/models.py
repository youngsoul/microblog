from app import db, login, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt
from time import time

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )

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
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic'
                               )

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


    def follow(self, followed_user):
        if not self.is_following(followed_user):
            self.followed.append(followed_user)

    def unfollow(self, followed_user):
        if self.is_following(followed_user):
            self.followed.remove(followed_user)

    def is_following(self, followed_user):
        return self.followed.filter(followers.c.followed_id == followed_user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)
        ).filter(
            followers.c.follower_id == self.id
        )

        return followed.union(self.posts).order_by(
            Post.timestamp.desc()
        )

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return

        return User.query.get(id)


@login.user_loader
def load_user(id):
    """
    Used by FlaskLogin to load a user in a persistence independent way.

    This also adds the user reference to the database session.

    :param id:
    :return: Instance of the user for the given ID
    """
    return User.query.get(int(id))

class Post(db.Model):
    """
    See User:  that model class has added a synthetic 'author' property to Post model class.
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author = reference to a User

    def __repr__(self):
        return f"<Post {self.body}>"

