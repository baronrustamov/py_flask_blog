# # https://www.maxlist.xyz/2020/08/17/flask-unittest/
# import unittest
# import pytest
# from flask_testing import TestCase
# from flask import url_for, render_template, abort
# from application import create_app, db, application
# from flask_bootstrap import Bootstrap
# from flask_login import login_user, LoginManager, current_user, logout_user
# from models.usermodel import db, BlogPost, Comment, User
# import os
# from blueprints.meta_blueprint import meta_blueprint


# class SettingBase(TestCase):
#     def create_app(self):
#         return create_app("testing")

#     def setUp(self):
#         db_user = "admin"
#         db_pass = os.environ["DB_PASS"]
#         db_name = "test_db"
#         db_host = os.environ["DB_HOST"]

#         # Extract host and port from db_host
#         host_args = db_host.split(":")
#         db_hostname, db_port = host_args[0], int(host_args[1])
#         mysql_url = "mysql+pymysql://" + db_user + ":" + db_pass + "@" + db_host \
#             + "/" + db_name
#         print('**************************')
#         print('**************************')
#         print('**************************')
#         print('mysql_url: ', mysql_url)

#         db.init_app(application)
#         # https://stackoverflow.com/a/19438054/720276
#         with application.app_context():
#             # Extensions like Flask-SQLAlchemy now know what the "current" app
#             # is while within this block. Therefore, you can now run........
#             # db.engine.execute("DROP DATABASE IF EXISTS test_db ;")
#             db.create_all()

#         application.config['TESTING'] = True
#         application.config['SERVER_NAME'] = '127.0.0.1'
#         application.config['WTF_CSRF_ENABLED'] = False
#         application.register_blueprint(meta_blueprint)


#         self.email = "test@a.com"
#         self.password = "666666"
#         self.name = "pac"
#         print('test setUp: ', self.email, self.password, self.name)

#         login_manager = LoginManager()
#         login_manager.init_app(application)

#       # 在結束測試時會被執行
#     def tearDown(self):
#       db.session.remove()
#       # db.drop_all()

#     # @application.route('/about')
#     # def about():
#     #   return abort(403)

#     def signup(self):
#         print('test setUp: ', self.email, self.password, self.name)

#         login_manager = LoginManager()
#         login_manager.init_app(application)

#         data = {"email": self.email,
#             "password": self.password,
#             "name": self.name}

#         with application.app_context():
#           with self.client:
#             response = self.client.post(
#               url_for('user_blueprint.register'),
#               follow_redirects=True, data=data
#             )

#         # response = self.client.post(
#         #     url_for('user_blueprint.register'),
#         #     follow_redirects=True,
#         #     json={"email": self.email,
#         #         "password": self.password,
#         #         "name": self.name})
#         return response


# class CheckUserAndLogin(SettingBase):
#   def test_pass(self):
#     pass
#   def test_signup(self):
#     with application.app_context():
#       response = self.signup()
#       self.assertEqual(response.status_code, 200)

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
