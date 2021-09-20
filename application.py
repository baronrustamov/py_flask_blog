from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from functools import wraps
from datetime import date
from flask_login import login_user, LoginManager, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor
from models.usermodel import db, BlogPost, Comment, User

application = Flask(__name__)

from blueprints.example_blueprint import example_blueprint
application.register_blueprint(example_blueprint)

ckeditor = CKEditor(application)

gravatar = Gravatar(application, size=100, rating='g', default='retro',
                    force_default=False, force_lower=False, use_ssl=False, base_url=None)


application.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(application)

import os
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]

# Extract host and port from db_host
host_args = db_host.split(":")
db_hostname, db_port = host_args[0], int(host_args[1])
mysql_url = "mysql+pymysql://" + db_user + ":" + db_pass + "@" + db_host \
    + "/" + db_name
print('mysql_url: ', mysql_url)

##CONNECT TO DB

application.config['SQLALCHEMY_DATABASE_URI'] = mysql_url
# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(application)
# print('db: ', db.Model)
# https://stackoverflow.com/a/19438054/720276
with application.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    db.create_all()

@application.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


login_manager = LoginManager()
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@application.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("need to login or register to comment")
            return redirect(url_for("login"))

        new_comment = Comment(
            text = form.comment_text.data,
            comment_author = current_user,
            parent_post = requested_post
        )
        print('new comment: ', new_comment)
        db.session.add(new_comment)
        db.session.commit()

    return render_template("post.html", post=requested_post, form=form, current_user=current_user)


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
