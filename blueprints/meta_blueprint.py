from datetime import date
from flask import Blueprint
from flask import render_template, redirect, url_for, flash, abort
from models.forms import CreatePostForm, CommentForm
from flask_login import current_user
from models.usermodel import db, BlogPost, Comment

meta_blueprint = Blueprint('meta_blueprint', __name__)


@meta_blueprint.route("/about")
def about():
    return render_template("about.html")

@meta_blueprint.route("/contact")
def contact():
    return render_template("contact.html")
