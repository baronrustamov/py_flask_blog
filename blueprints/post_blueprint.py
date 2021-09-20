from functools import wraps
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, abort
from models.forms import CreatePostForm, CommentForm
from flask_login import current_user
from models.usermodel import db, BlogPost, Comment

post_blueprint = Blueprint('post_blueprint', __name__)

@post_blueprint.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@post_blueprint.route('/example')
def index():
    return "This is an example app"


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

@post_blueprint.route("/new-post", methods=["GET", "POST"])
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


@post_blueprint.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
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


@post_blueprint.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@post_blueprint.route("/post/<int:post_id>", methods=["GET", "POST"])
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

