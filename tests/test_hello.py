# https://stackoverflow.com/a/48120470/720276
import pytest
import unittest
from application import application
from flask_login import login_user, LoginManager, current_user, logout_user
from models.usermodel import User
from flask import url_for, render_template, abort
from tests.base import BaseTest

# login_manager = LoginManager()
# login_manager.init_app(application)
# @login_manager.user_loader
# def load_user(user_id):
#   return User.get(user_id)

class TestHello(BaseTest):
  def setUp(self):
    super(TestHello, self).email = "subclass use another email"
    # self.email = "test@a.com"
    # self.password = "P654321."
    # self.name = "pac"

    application.config['TESTING'] = True
    application.config['SERVER_NAME'] = 'localhost.localdomain'

  # @application.route('/about')
  # def about():
  #   return abort(403)

  def test_hello(self):
    with application.app_context():
      response = application.test_client().get(url_for('about') )
      print("res: ", response.status_code )
      assert response.status_code == 200

  def test_register(self):
    self.signup()

  def test_login(self):
    self.signup()
    data = {"email": self.email,
        "password": self.password,
        "name": self.name}
    print("login data: ", data)
    print("application.app_context(): ", application.app_context() )
    with application.app_context():
      response = application.test_client().get(url_for('user_blueprint.login'),
          follow_redirects=True, data=data)
      assert response.status_code == 202
      print("res: ", response.status_code )

    def test_signup_400(self):
      self.password = '123'
      response = self.signup()
      # self.assertEqual(response.status_code, 402)
      assert response.status_code == 200

    def test_signup_422(self):
      response = self.signup()
      # self.assertEqual(response.status_code, 423)
      assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
