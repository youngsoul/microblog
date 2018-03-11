
# Flask Mega Tutorial

**Miguel Grinberg**

This repository will hold my work while following along with Miguel Grinberg's *Flask Mega Tutorial* which can be found here. [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

The Video / PDF tutorial can be found at:

[Learn Miguel Grinberg](https://learn.miguelgrinberg.com)



### Progress

Chapter 8: Followers

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


