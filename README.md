
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


### Chapter 17 Linux Deployment

Install Vagrant and Virtual box.

See *Vagrantfile* in root of project

type:  *vagrant up*

to ssh into vagrant box: *vagrant ssh*

In the Vagrant, Ubuntu shell:

sudo apt-get -y update

sudo apt-get -y install python3 python3-venv python3-dev

sudo apt-get -y install mysql-server postfix supervisor nginx git

after the vagrant box is setup,

git clone <git repo from mg microblog.>

cd repo

python3 -m venv venv

pip install -r requirements.txt

pip install --upgrade pip

pip install gunicorn  pymysql

*create .env file*

nano .env

----- Contents ----

SECRET_KEY=wponf972oiwbvgywigfbnopejhug

MAIL_SERVER=localhost

MAIL_PORT=25

DATABASE_URL=mysql+pymysql://microblog:microblog@localhost:3306/microblog

MS_TRANSLATOR_KEY=aaaaaaa

------- End Contents --------


add flask app to profile

*echo "export FLASK_APP=microblog.py" >> ~/.profile*

flask translate compile

#### Create mysql db

mysql -u root -p

mysql> create database microblog character set utf8 collate utf8_bin;

mysql> create user 'microblog'@'localhost' identified by 'microblog';

mysql> grant all privileges on microblog.* to 'microblog'@'localhost';

mysql> flush privileges;

mysql> quit;

*flask db upgrade*

the above will use the values in .env to connect to the database and run the migrations

#### Setup Supervisor, Gunicorn and Nginx

##### Gunicorn


*gunicorn -b localhost:8000 -w 4 microblog:app*

if you use 0.0.0.0 instead of localhost then it is accessible outside the vagrant vm.

But in general, we just want to expose Nginx.  Using 0.0.0.0 lets us test the webapp right away.

*gunicorn -b 0.0.0.0:8000 -w 4 microblog:app*

##### Supervisor

sudo nano /etc/supervisor/conf.d/microblog.conf

----- Contents ----
[program:microblog]

command=/home/vagrant/microblog/venv/bin/gunicorn -b 0.0.0.0:8000 -w 4 microblog:app

directory=/home/vagrant/microblog

user=vagrant

autostart=true

autorestart=true

stopasgroup=true

killasgroup=true

----- End Contents -----

*sudo supervisorctl reload*

*sudo supervisorctl status*

*sudo supervisorctl stop microblog*

*sudo supervisorctl start microblog*
exit

##### Nginx

Create a self signed certificate

**letsencrypt is free cert company**

*mkdir certs*

*openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout certs/key.pem -out certs/cert.pem*

*sudo service nginx reload*


#### To run on raspberry pi:

sudo apt-get install supervisor

sudo service supervisor restart
