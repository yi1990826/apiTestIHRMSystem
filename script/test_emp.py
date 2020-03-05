import unittest
import requests
import logging
# 创建测试类集成unittest.TestCase
import app
from api.emp_api import EmployeeApi
from utils import assert_common_utils, DBUtils
import pymysql

class TestEmployee(unittest.TestCase):

    # 初始化unittest的函数
    def setUp(self):
        # 实例化EmployeeApi
        self.emp_api = EmployeeApi()

    def tearDown(self):
        pass

    def login(self, mobile, password):
        login_url = "http://182.92.81.159/api/sys/login"
        jsonData = {"mobile": mobile, "password": password}
        return requests.post(login_url, json=jsonData)

    def add_emp(self, username, mobile, headers):
        add_emp_url = "http://182.92.81.159/api/sys/user"
        # 从外界接收username和mobile，并拼接成发送的请求体数据
        jsonData = {"username": username,
                    "mobile": mobile,
                    "timeOfEntry": "2020-02-01",
                    "formOfEmployment": 1,
                    "departmentName": "酱油2部",
                    "departmentId": "1205026005332635648",
                    "correctionTime": "2020-02-03T16:00:00.000Z"}
        # 调用添加员工并返回响应数据
        return requests.post(add_emp_url, json=jsonData, headers=headers)
# 查询员工函数
    def query_emp(self, emp_id, headers):
        query_url = "http://182.92.81.159/api/sys/user" + "/" + emp_id
        return requests.get(query_url, headers=headers)
# 更改员工函数
    def modify_emp(self, emp_id, username, headers):
        modify_url = "http://182.92.81.159/api/sys/user" + "/" + emp_id
        return requests.put(modify_url, json={"username": username}, headers=headers)
# 删除员工函数
    def delete_emp(self, emp_id, headers):
        delete_url = "http://182.92.81.159/api/sys/user" + "/" + emp_id
        return requests.delete(delete_url, headers=headers)

    # 创建测试函数
    # def test01_emp_management(self):
    #     # 调用登陆
    #     response = self.emp_api.login("13800000002", "123456")
    #     # 打印登陆结果
    #     logging.info("员工模块的登陆结果为：{}".format(response.json()))
    #     # 取出令牌，并拼接成以Bearer 开头的字符串
    #     token = "Bearer " + response.json().get('data')
    #     logging.info("取出的令牌为：{}".format(token))
    #
    #     # 设置员工模块所需要的请求头
    #     headers = {"Content-Type": "application/json", "Authorization": token}
    #     logging.info("员工模块请求头为：{}".format(headers))
    #
    #     # 调用添加员工
    #     response_add_emp = self.emp_api.add_emp("22测试24",
    #                                             "13119900826",
    #                                             headers)
    #     logging.info("添加员工接口的结果为：{}".format(response_add_emp.json()))
    #     # 断言结果：响应状态码，success，code，message
    #     assert_common_utils(self, response_add_emp, 200, True, 10000, "操作成功")
    #
    #     # 由于添加员工成功后，还需要保存员工ID给后续的查询、修改、删除员工使用，所以我们需要保存员工ID
    #     emp_id = response_add_emp.json().get("data").get("id")
    #     logging.info("保存的员工ID为：{}".format(emp_id))
    #
    #     # 调用查询员工
    #     response_query = self.emp_api.query_emp(emp_id, headers=headers)
    #     logging.info("查询员工的结果为：{}".format(response_query.json()))
    #     # 断言结果：响应状态码，success，code，message
    #     assert_common_utils(self, response_query, 200, True, 10000, "操作成功")
    #
    #     # 调用修改员工
    #     response_modify = self.emp_api.modify_emp(emp_id, "new_tom", headers=headers)
    #     logging.info("修改员工结果为：{}".format(response_modify.json()))
    #     # 断言结果：响应状态码，success，code，message
    #     assert_common_utils(self, response_modify, 200, True, 10000, "操作成功")
    #
    #     # 调用删除员工
    #     response_delete = self.emp_api.delete_emp(emp_id, headers=headers)
    #     logging.info("删除员工的结果为：{}".format(response_delete.json()))
    #     # 断言结果：响应状态码，success，code，message
    #     assert_common_utils(self, response_delete, 200, True, 10000, "操作成功")
    #     # self.assertEqual(200, response_delete.status_code)
    #     # self.assertEqual(True, response_delete.json().get("success"))
    #     # self.assertEqual(10000, response_delete.json().get("code"))
    #     # self.assertIn("操作成功", response_delete.json().get("message"))
    def test02_login_success(self):
        # 调用登陆
        response = self.emp_api.login("13800000002", "123456")
        # 打印登陆结果
        logging.info("员工模块的登陆结果为：{}".format(response.json()))
        # 取出令牌，并拼接成以Bearer 开头的字符串
        token = "Bearer " + response.json().get('data')
        logging.info("取出的令牌为：{}".format(token))
        # 设置员工模块所需要的请求头
        headers = {"Content-Type": "application/json", "Authorization": token}
        app.HEADERS = headers
        logging.info("员工模块请求头为：{}".format(app.HEADERS))

    def test03_add_emp(self):
        # 调用添加员工
        response_add_emp = self.emp_api.add_emp("王XX77711",
                                                "13732323666",
                                                app.HEADERS)
        logging.info("添加员工接口的结果为：{}".format(response_add_emp.json()))
        # 断言结果：响应状态码，success，code，message
        assert_common_utils(self, response_add_emp, 200, True, 10000, "操作成功")
        # 由于添加员工成功后，还需要保存员工ID给后续的查询、修改、删除员工使用，所以我们需要保存员工ID
        emp_id = response_add_emp.json().get("data").get("id")
        app.EMPID = emp_id
        logging.info("保存的员工ID为：{}".format(app.EMPID))

    def test04_query_emp(self):
        # 调用查询员工
        response_query = self.emp_api.query_emp(app.EMPID, headers=app.HEADERS)
        logging.info("查询员工的结果为：{}".format(response_query.json()))
        # 断言结果：响应状态码，success，code，message
        assert_common_utils(self, response_query, 200, True, 10000, "操作成功")

    def test05_modify_emp(self):
        # 调用修改员工
        response_modify = self.emp_api.modify_emp(app.EMPID, "new_tom", headers=app.HEADERS)
        logging.info("修改员工结果为：{}".format(response_modify.json()))
        # 断言结果：响应状态码，success，code，message
        assert_common_utils(self, response_modify, 200, True, 10000, "操作成功")
        # 建立连接 username：readuser
        # password：iHRM_user_2019
        conn = pymysql.connect(host='182.92.81.159', user='readuser', password='iHRM_user_2019', database='ihrm')
        # 获取游标
        cursor = conn.cursor()
        # 执行SQL语句
        # 根据添加员工返回的id查询数据库中员工表的username，这样就能获取到修改之后的数据
        sql = "select username from bs_user where id = {};".format(app.EMPID)
        logging.info("要查询的SQL语句为：{}".format(sql))
        # 执行查询的sql语句
        cursor.execute(sql)
        # 获取返回结果
        result = cursor.fetchone()
        logging.info("SQL查询出来的结果为：{}".format(result))  # ('new_tom',)
        # 断言修改结果是否正确
        # 注意：如果是用fetchall()取出的数据，那么取出result时，需要有两个下表result[0][0]
        self.assertEqual("new_tom", result[0])
        # 关闭连接
        cursor.close()
        # 关闭游标
        conn.close()
        # 建立连接 username：readuser
        # password：iHRM_user_2019
        # with DBUtils() as db:
        #     # 执行SQL语句
        #     # 根据添加员工返回的id查询数据库中员工表的username，这样就能获取到修改之后的数据
        #     sql = "select username from bs_user where id = {};".format(app.EMPID)
        #     logging.info("要查询的SQL语句为：{}".format(sql))
        #     # 执行查询的sql语句
        #     db.execute(sql)
        #     # 获取返回结果
        #     result = db.fetchone()
        #     logging.info("SQL查询出来的结果为：{}".format(result))  # ('new_tom',)
        #     # 断言修改结果是否正确
        #     # 注意：如果是用fetchall()取出的数据，那么取出result时，需要有两个下标result[0][0]
        #     self.assertEqual("new_tom", result[0])

    def test06_delete_emp(self):
        # 调用删除员工
        response_delete = self.emp_api.delete_emp(app.EMPID, app.HEADERS)
        logging.info("删除员工的结果为：{}".format(response_delete.json()))
        # 断言结果：响应状态码，success，code，message
        assert_common_utils(self, response_delete, 200, True, 10000, "操作成功")