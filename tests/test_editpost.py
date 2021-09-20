# https://www.maxlist.xyz/2020/08/17/flask-unittest/
import unittest
from flask import url_for
from flask_testing import TestCase
from application import create_app, db, application
import json

class SettingBase(TestCase):
    def create_app(self):
        return create_app("testing")

      # 在運行測試之前會先被執行
    def setUp(self):

        import os
        db_user = "admin"
        db_pass = os.environ["DB_PASS"]
        db_name = "test_db"
        db_host = "localhost:3306"

        # Extract host and port from db_host
        host_args = db_host.split(":")
        db_hostname, db_port = host_args[0], int(host_args[1])
        mysql_url = "mysql+pymysql://" + db_user + ":" + db_pass + "@" + db_host \
            + "/" + db_name
        print('**************************')
        print('**************************')
        print('**************************')
        print('mysql_url: ', mysql_url)

        db.init_app(application)
        # https://stackoverflow.com/a/19438054/720276
        with application.app_context():
            # Extensions like Flask-SQLAlchemy now know what the "current" app
            # is while within this block. Therefore, you can now run........
#            db.drop_all()
            db.create_all()

        application.config['TESTING'] = True
        # Wrong key:
        # app.config['CSRF_ENABLED'] = False
        # Right key:
        application.config['WTF_CSRF_ENABLED'] = False

        self.email = "test@a.com"
        self.password = "666666"
        self.name = "pac"
        print('test setUp: ', self.email, self.password, self.name)
        

      # 在結束測試時會被執行
    def tearDown(self):
        pass

        db.session.remove()
        db.drop_all()

      # signup 是測試時很常會被用到的功能，所以寫成函式，可以重複利用
    def signup(self):
        print('test setUp: ', self.email, self.password, self.name)
        response = self.client.post(
            url_for('user_blueprint.register'),
            follow_redirects=True,
            json={"email": self.email,
                "password": self.password,
                "name": self.name})
        return response
# 這邊繼承剛剛的寫的 SettingBase class，接下來會把測試都寫在這裡
class CheckUserAndLogin(SettingBase):
    def test_pass(self):
        pass
    # def test_signup(self):
    #     response = self.signup()
    #     self.assertEqual(response.status_code, 200)

    # def test_signup_400(self):
    #     # 測試密碼少於六位數
    #     self.passwords = '123'
    #     response = self.signup()
    #     self.assertEqual(response.status_code, 400)

    # def test_signup_422(self):
    #     # 測試重複註冊
    #     response = self.signup()
    #     response = self.signup()
    #     self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
