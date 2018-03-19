from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# can be used with any model
# needs 3 properties and one method
login = LoginManager(app)
login.login_view = 'login' # function to log a user in to protect a route

# reference to the Mail object.
mail = Mail(app)

# bootstrap initialization
boostrap = Bootstrap(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)

        # this will set the error handler level to ERROR for the mail handler.  Meaning all
        # ERROR level messages will be directed to the mail_handler.
        # to tie the logger to the mail_handler, call addHandler on the logger associated
        # with the Flask app instance.
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # Setup application level logging
    if not os.path.exists('logs'):
            os.mkdir('logs')

    # create a rotating log file handler, in the
    log_file = os.path.join('logs', 'microblog.log')
    file_handler = RotatingFileHandler(log_file, maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

# routes import is at the bottom, to avoid a circular dependency which is why this is at the bottom.
from app import routes, models, errors


