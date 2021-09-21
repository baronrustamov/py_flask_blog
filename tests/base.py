from application import application, db
import unittest

class BaseTest(unittest.TestCase):
  def setUp(self):


    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager

    app = Flask(__name__)
    # app.config[u'DEBUG'] = settings.debug
    db = SQLAlchemy(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"

    application.config['TESTING'] = True
    # application.config['LOGIN_DISABLED'] = False
    #application.login_manager._login_disabled = False #doesn't help either
    self.application = application.test_client()
    db.create_all()
