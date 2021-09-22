# https://stackoverflow.com/a/48120470/720276
import pytest
import unittest
from application import application
from flask_login import login_user, LoginManager, current_user, logout_user
from models.usermodel import User
from flask import url_for, render_template, abort
from tests.base import BaseTest

login_manager = LoginManager()
login_manager.init_app(application)
@login_manager.user_loader
def load_user(user_id):
  return User.get(user_id)

class TestHello(BaseTest):
  def setUp(self):
    application.config['TESTING'] = True
    application.config['SERVER_NAME'] = 'localhost.localdomain'
  #   application.config['WTF_CSRF_ENABLED'] = False
  #   # login_manager = LoginManager()
  #   # login_manager.init_app(application)

  # # @application.route('/about')
  # # def about():
  # #   return abort(403)

  def test_hello(self):
    with application.app_context():
      response = application.test_client().get(url_for('about') )
      print("res: ", response.status_code )
      assert response.status_code == 200

  def test_register(self):
    self.signup()

  def test_login(self):
    self.signup()
    data = {"email": "test@a.com",
        "password": "666666",
        "name": "pac"}
    print("login data: ", data)
    print("application.app_context(): ", application.app_context() )
    with application.app_context():
      response = application.test_client().get(url_for('user_blueprint.login'),
          follow_redirects=True, data=data)
      assert response.status_code == 200
      print("res: ", response.status_code )


if __name__ == '__main__':
    unittest.main()
