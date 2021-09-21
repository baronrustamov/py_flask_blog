# https://stackoverflow.com/a/48120470/720276
import pytest
import unittest
from application import application
from flask_login import login_user, LoginManager, current_user, logout_user
from models.usermodel import User
from flask import url_for, render_template, abort

login_manager = LoginManager()
login_manager.init_app(application)
@login_manager.user_loader
def load_user(user_id):
  return User.get(user_id)

class TestHello(unittest.TestCase):
  def setUp(self):
    application.config['TESTING'] = True
    application.config['SERVER_NAME'] = '127.0.0.1'
    application.config['WTF_CSRF_ENABLED'] = False

  @application.route('/about')
  def about():
    return abort(403)

  def test_hello(self):
    with application.app_context():
      response = application.test_client().get(url_for('about') )
      assert response.status_code == 403

if __name__ == '__main__':
    unittest.main()
