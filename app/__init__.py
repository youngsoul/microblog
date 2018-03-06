from flask import Flask
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

print(app.config['SECRET_KEY'])

# routes import is at the bottom, to avoid a circular dependency which is why this is at the bottom.
from app import routes


