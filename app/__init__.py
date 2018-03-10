from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# can be used with any model
# needs 3 properties and one method
login = LoginManager(app)
login.login_view = 'login' # function to log a user in to protect a route

# routes import is at the bottom, to avoid a circular dependency which is why this is at the bottom.
from app import routes, models


