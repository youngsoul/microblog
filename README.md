
# Flask Mega Tutorial

**Miguel Grinberg**

This repository will hold my work while following along with Miguel Grinberg's *Flask Mega Tutorial* which can be found here. [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

The Video / PDF tutorial can be found at:

[Learn Miguel Grinberg](https://learn.miguelgrinberg.com)



### Progress

Chapter 11: Facelift

Section: Intro


### Flask Migrate

must set the FLASK_APP environment variable
export FLASK_APP=microblog.py


#### Initialize the db migrations

flask db init


#### Migrate
flask db migrate -m "create user table"

#### Apply upgrade migrations
flask db upgrade

#### Apply downgrade migrations
flask db downgrade

#### Migration History
flask db history

#### Migration current
flask db current

after adding a new model:
flask db migrate -m "added new model"
flask db upgrade

### Flask Shell
flask shell

Creates a python session with the flask app available

See microblog.py for the *@app.shell_context_processor* annotated method which exports all of the objects to the flash shell


### Debug Mode
To enable debug mode there are 2 options:

- export FLASK_DEBUG=1

- in *microblog.py* set debug flag in app.run:  app.run(host='0.0.0.0', debug=True)


### Python Debug Email Server
Python has a debugging smtp server.  This server will not actually send email but instead
display what the email would have looked like.

*python -m smtpd -n -c DebuggingServer localhost:8025*

To configure or override the config.py:

*export MAIL_SERVER=localhost*

*export MAIL_PORT=8025*


### Chapter 11: Flask Bootstrap

pip install flask-bootstrap

see *app/__init__.py* for how to import and initialize Flask Bootstrap

Flask Bootstrap can render forms with a single call like:

*{% import 'bootstrap/wtf.html' as wtf %}*

*{{ wtf.quick_form(form) }}*

### Chapter 12: Flask Moment

pip install flask-moment

**moment.js**

[Moment JS Link](http://momentjs.com)

### Chapter 13: I18n and L10n

**Note that babel cannot use the 3.6 format strings**

This works:

*flash(_('User %(username) does not exist', username=username))*

This does not:

*flash(_('User {username} does not exist'))*


pip install flask-babel

Use Babel to extract all of the strings to translate.

create a babel.cfg file

To extract the files:

*pybabel extract -F babel.cfg -k _l -o messages.pot .*


To add another language messages.po file:

*pybabel init -i messages.pot -d app/translations -l fr*

*pybabel compile -d app/translations*

To update messages:

Extract the messages.pot file again, it is a transient file that does not need to be source controlled.

