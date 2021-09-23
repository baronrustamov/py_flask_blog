from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from application import application, db
import unittest

class BaseTest(unittest.TestCase):
  def setUp(self):
    self.email = "test@a.com"
    self.password = "P654321."
    self.name = "pac"

    application = Flask(__name__)
    application.config['TESTING'] = True
    application.config['SERVER_NAME'] = '127.0.0.1'
    application.config['WTF_CSRF_ENABLED'] = False
    application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    # app.config[u'DEBUG'] = settings.debug
    db = SQLAlchemy(application)
    login_manager = LoginManager()
    login_manager.init_app(application)
    # application.config['LOGIN_DISABLED'] = False
    # self.application = application.test_client()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    # db.drop_all()


  def signup(self):
    data = {"email": self.email,
        "password": self.password,
        "name": self.name}
    # data = {"email": "test@a.com",
    #     "password": "666666",
    #     "name": "pac"}
    print("data: ", data)
    print("application.app_context(): ", application.app_context() )
    with application.app_context():
      response = application.test_client().get(url_for('user_blueprint.register'),
          follow_redirects=True, data=data)
      assert response.status_code == 200
      print("res: ", response.status_code )
      # wrong: self.client.post(
      # with self.client:
      #   response = self.client.post(
      #     url_for('user_blueprint.register'),
      #     follow_redirects=True, data=data
      #   )


