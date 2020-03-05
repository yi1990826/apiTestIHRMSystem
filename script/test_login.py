import unittest
import requests
import logging
from api.login_api import LoginApi
from app import HEADERS
from utils import assert_common_utils


class TestLogin(unittest.TestCase):
    # 初始化
    def setUp(self):
        self.loginapi = LoginApi()
    def tearDown(self):
        pass
    def test01_login_success(self):
        response = self.loginapi.login("13800000002","123456")
        # 打印结果
        logging.info("登陆成功的结果为：{}".format(response.json()))
        # 断言登陆结果
        assert_common_utils(self, response, 200, True, 10000, "操作成功")
    # 无参数
    def test02_login_null(self):
        response = self.loginapi.login_params(jsonData="")
        logging.info("没有参数的登录结果为：{}".format(response.json()))
