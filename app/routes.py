from app import app, db
from flask import render_template, flash, redirect, url_for, request, g
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email
from flask_babel import _, lazy_gettext as _l, get_locale

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # note that the user was added to the session already
        # added to session when flask login loaded the user in models.py
        # @login.user_loader
        # def load_user(id):
        db.session.commit()
    g.locale = str(get_locale())

# note that we always have the @app decorators FIRST because the order is important.
# the login decorator should be the last one.
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        # then this was a post of the form
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        # even though we could render the index.html  here, it is considered
        # bad form to render the template as a result of a post request.
        # therefore, we redirect to force a get request and then render the
        # template as a result of the GET request.
        return redirect(url_for('index'))

    # this is a get, and we need to get the posts to show
    page_number = request.args.get('page', 1, type=int)
    items_per_page = app.config['POSTS_PER_PAGE']
    raise_404_on_less = False
    # note: posts is a pagination object, and 'items' property is the collection
    posts = current_user.followed_posts().paginate(page_number, items_per_page, raise_404_on_less)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html', posts=posts.items, title='Home Page', form=form, next_url=next_url, prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    # this is a get, and we need to get the posts to show
    page_number = request.args.get('page', 1, type=int)
    items_per_page = app.config['POSTS_PER_PAGE']
    raise_404_on_less = False
    # note: posts is a pagination object, and 'items' property is the collection
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page_number, items_per_page, raise_404_on_less)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # form as form data and valid, and therefore a post
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))

        # when you get here, it is a valid login
        # so log the person and save in session
        login_user(user, remember=form.remember_me.data)

        #flask will append a 'next' url variable if the user tried to go to
        #page without being logged in.
        next_page = request.args.get('next')
        # if we do not have a next page
        # or if we do, but the netloc is not empty, which means this is not a url
        # for our app, and a malicious user might be trying to hack the url
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    else:
        return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        #posting the form
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)

        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))

    # else it was a get so show the form
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        # then this token is not valid, just redirect to index page
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page_number = request.args.get('page', 1, type=int)
    items_per_page = app.config['POSTS_PER_PAGE']
    raise_404_on_less = False

    # note: posts is a pagination object, and 'items' property is the collection
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page_number, items_per_page, raise_404_on_less)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None

    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        # then a request to view form
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))

    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))

    # if you get here everything is ok
    current_user.follow(user)
    db.session.commit()
    flash(_('You are now following %(username)', username=username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username)
    if user is None:
        flash(_l('User %(username) does not exist', username=username))
        return redirect(url_for('index'))

    if user == current_user:
        flash(_(f'You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))

    # if you get here everything is ok
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are now unfollowing %(username)', username=username))
    return redirect(url_for('user', username=username))

