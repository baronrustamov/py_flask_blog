from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from functools import wraps
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar

from flask_ckeditor import CKEditor

application = Flask(__name__)
ckeditor = CKEditor(application)

application.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(application)

##CONNECT TO DB
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


##CONFIGURE TABLES
# User class HAVE to be defined first.
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)

    posts = relationship("BlogPost", back_populates="author")

    # ** adding parent relationship, comment_author " refers to the comment_author property in the Comment class.
    # in Comment class we have:
    # author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # comment_author = relationship("User", back_populates="comments")
    comments = relationship("Comment", back_populates="comment_author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # author = db.Column(db.String(250), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    # adding child relationship
    # users.id, the users refer to the tablename of the user class.
    # comments, refer to the property in the User class.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

db.create_all()


@application.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@application.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    print('email: ', request.form.get('email'))
    if User.query.filter_by(email=request.form.get('email') ).first():
        flash("您已經註冊過了，請登入。")
        print("您已經註冊過了，請登入。")
        return redirect(url_for('login'))

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


login_manager = LoginManager()
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@application.route('/login', methods=["GET", "POST"])
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


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@application.route("/post/<int:post_id>")
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post, form=form)


@application.route("/about")
def about():
    return render_template("about.html")


@application.route("/contact")
def contact():
    return render_template("contact.html")

def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.id != 1:
            print('cannot add post! ', func)
            return abort(403)
        else:
            print('admin only: ', func)
            return func(*args, **kwargs)
    return wrapper

@application.route("/new-post", methods=["GET", "POST"])
#mark with the decorator
#@admin_only
def add_new_post():
    form = CreatePostForm()
    print('add_new_post form: ', form)
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        print('new_post: ', new_post)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    print('before make-post')
    return render_template("make-post.html", form=form)


@application.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@application.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    application.debug = True
    application.run()
    # application.run(host='0.0.0.0', port=5000)
