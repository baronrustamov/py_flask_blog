# https://realpython.com/flask-blueprint/

from flask import Blueprint
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_login import login_user, LoginManager, current_user, logout_user
from models.usermodel import db, BlogPost, Comment, User
from werkzeug.security import generate_password_hash, check_password_hash

example_blueprint = Blueprint('example_blueprint', __name__)
@example_blueprint.route('/example')
def index():
    return "This is an example app"


@example_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@example_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    print('email: ', request.form.get('email'))
    if User.query.filter_by(email=request.form.get('email') ).first():
        flash("您已經註冊過了，請登入。")
        print("您已經註冊過了，請登入。")
        return redirect(url_for('example_blueprint.login'))

    if form.validate_on_submit():
        hash_salt_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_salt_password
        )

        db.session.add(new_user)
        db.session.commit()

        # this line will authenticate the user with Flask-login
        login_user(new_user)
        return redirect(url_for("get_all_posts") )
    return render_template("register.html", form=form)


@example_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('get_all_posts'))
        else:
            # sometimes we just don't want user to know, login or password which one is wrong.
            # if the user is a hacker.
            flash("wrong email or password! 請重新輸入。")
            return redirect(url_for('login'))

        # if not user:
        #     flash("That email does not exist, please try again.")
        #     return redirect(url_for('login'))
        # # Password incorrect
        # elif not check_password_hash(user.password, password):
        #     flash('Password incorrect, please try again.')
        #     return redirect(url_for('login'))
        # else:
        #     login_user(user)
        #     return redirect(url_for('get_all_posts'))

    return render_template("login.html", form=form)


