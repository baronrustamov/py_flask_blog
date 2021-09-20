from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, current_user, logout_user
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor
from models.usermodel import db, BlogPost, Comment, User

application = Flask(__name__)

from blueprints.user_blueprint import user_blueprint
from blueprints.post_blueprint import post_blueprint
application.register_blueprint(user_blueprint)
application.register_blueprint(post_blueprint)

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

login_manager = LoginManager()
login_manager.init_app(application)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@application.route("/about")
def about():
    return render_template("about.html")


@application.route("/contact")
def contact():
    return render_template("contact.html")



if __name__ == "__main__":
    application.debug = True
    application.run()
    # application.run(host='0.0.0.0', port=5000)
