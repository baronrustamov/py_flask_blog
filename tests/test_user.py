# import unittest
# import pytest
# from flask_testing import TestCase
# from flask import app, url_for
# from application import create_app, db, application
# from flask_bootstrap import Bootstrap
# from flask_login import login_user, LoginManager, current_user, logout_user
# import os

# class SettingBase(unittest.TestCase):
#     def create_app(self):
#       return create_app("testing")

#     def setUp(self):
#       db_user = "admin"
#       db_pass = os.environ["DB_PASS"]
#       db_name = "test_db"
#       db_host = os.environ["DB_HOST"]

#       # Extract host and port from db_host
#       host_args = db_host.split(":")
#       db_hostname, db_port = host_args[0], int(host_args[1])
#       mysql_url = "mysql+pymysql://" + db_user + ":" + db_pass + "@" + db_host \
#           + "/" + db_name
#       print('**************************')
#       print('**************************')
#       print('**************************')
#       print('mysql_url: ', mysql_url)

#       db.init_app(application)
#       # https://stackoverflow.com/a/19438054/720276
#       with application.app_context():
#           # Extensions like Flask-SQLAlchemy now know what the "current" app
#           # is while within this block. Therefore, you can now run........
#           # db.engine.execute("drop database IF EXISTS 'test_db';")
#           # db.engine.execute("drop all;")
#           db.create_all()

#       application.config['TESTING'] = True
#       # Wrong key:
#       # app.config['CSRF_ENABLED'] = False
#       # Right key:
#       application.config['WTF_CSRF_ENABLED'] = False
#     #   application.config['SERVER_NAME'] = '127.0.0.1'

#       self.email = "test@a.com"
#       self.password = "666666"
#       self.name = "pac"
#       print('test setUp: ', self.email, self.password, self.name)

#       login_manager = LoginManager()
#       login_manager.init_app(application)
#       self.application = application.test_client()

#     def tearDown(self):
#       db.session.remove()
#       db.drop_all()

#     def signup(self):
#       with application.app_context():
#         print('current user: ', current_user)
#         print('current user: ', current_user)
#         print('current user: ', current_user)
#       # with self.application:
#         print('current user: ', current_user)
#         print('current user: ', current_user)
#         print('current user: ', current_user)
#         print('current user: ', current_user)
#         print('test setUp: ', self.email, self.password, self.name)

#         login_manager = LoginManager()
#         login_manager.init_app(application)

#         data = {"email": self.email,
#             "password": self.password,
#             "name": self.name}
#         response = self.application.post(
#             url_for('user_blueprint.register'),
#             follow_redirects=True, data=data
#             )

#         # response = self.client.post(
#         #     url_for('user_blueprint.register'),
#         #     follow_redirects=True,
#         #     json={"email": self.email,
#         #         "password": self.password,
#         #         "name": self.name})
#         return response

# class CheckUserAndLogin(SettingBase):
#     def test_pass(self):
#         pass
#     def test_signup(self):
#         response = self.signup()
#         self.assertEqual(response.status_code, 200)

#     # def test_signup_400(self):
#     #     # 測試密碼少於六位數
#     #     self.passwords = '123'
#     #     response = self.signup()
#     #     self.assertEqual(response.status_code, 400)

#     # def test_signup_422(self):
#     #     # 測試重複註冊
#     #     response = self.signup()
#     #     response = self.signup()
#     #     self.assertEqual(response.status_code, 422)


# if __name__ == '__main__':
#     unittest.main()
