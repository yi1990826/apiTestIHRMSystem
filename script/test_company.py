import requests
import unittest
import pymysql



class TestCompany(unittest.TestCase):
# 创建获取部门信息函数
    def test01_company(self):
        # 登录IHRM系统
        response_login = requests.post("http://182.92.81.159/api/sys/login",
                                 json={"mobile": "13800000002", "password": "123456"})
        print("登录结果为：",response_login.json())
        # 取出令牌，并拼接成以Bearer 开头的字符串
        token = "Bearer " + response_login.json().get("data")
        print("打印令牌",token)
        # 设置部门模块所需要的请求头
        headers = {"Content-Type": "application/json", "Authorization": token}
        #添加部门
        jsonData = {"name":"搞笑","code":"8899"}
        response_add_company = requests.post("http://182.92.81.159/api/company/department",headers = headers,
                                             json = jsonData)
        print("添加部门信息：",response_add_company.json())
        # 断言结果：响应状态码，success，code，message,data
        self.assertEqual(200, response_add_company.status_code)
        self.assertEqual(True, response_add_company.json().get("success"))
        self.assertEqual(10000, response_add_company.json().get("code"))
        self.assertIn("操作成功", response_add_company.json().get("message"))
        self.assertEqual(None, response_add_company.json().get("data"))
        # 连接数据库查询新增部门信息，并获取ID
        conn = pymysql.connect(host="182.92.81.159", user='readuser', password='iHRM_user_2019', database='ihrm')
        # 获取游标
        cursor = conn.cursor()
        sql = "select id from co_department where name = '搞笑' "
        cursor.execute(sql)#执行SQL语句查看ID信息
        result = cursor.fetchone()#用fetchone()取出的数据
        add_id = result[0] # 该部门ID为
        print("查看部门的ID为：",add_id)
        cursor.close()       # 关闭游标
        conn.close()  # 关闭连接

        #进入IHRM系统查看添加的部门信息
        response_get_compant = requests.get("http://182.92.81.159/api/company/department/"+add_id,headers = headers)
        # 打印部门信息
        print("获取添加新部门信息：",response_get_compant.json())
        # 断言结果：响应状态码，success，code，message,data
        self.assertEqual(200, response_get_compant.status_code)
        self.assertEqual(True, response_get_compant.json().get("success"))
        self.assertEqual(10000, response_get_compant.json().get("code"))
        self.assertIn("操作成功", response_get_compant.json().get("message"))



        # 修改部门
        jsonData = {"name": "搞笑修改", "code": "5566"}
        response_updata_company = requests.put("http://182.92.81.159/api/company/department/"+add_id,
                                               headers=headers,json =jsonData)
        print("修改部门信息：", response_add_company.json())
        # 断言结果：响应状态码，success，code，message,data
        self.assertEqual(200, response_updata_company.status_code)
        self.assertEqual(True, response_updata_company.json().get("success"))
        self.assertEqual(10000, response_updata_company.json().get("code"))
        self.assertIn("操作成功", response_updata_company.json().get("message"))
        self.assertEqual(None, response_updata_company.json().get("data"))
        # 连接数据库查询新增部门信息，并获取更改的部门名称?
        conn = pymysql.connect(host="182.92.81.159", user='readuser', password='iHRM_user_2019', database='ihrm')
        # 获取游标
        cursor = conn.cursor()
        sql = "select name from co_department where id = {}  ".format(add_id)
        cursor.execute(sql)  # 执行SQL语句查看修改部门的信息
        result = cursor.fetchone()  # 用fetchone()取出的数据
        updata_company = result[0]
        print("查看部门的ID为：", updata_company)
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接

        # 删除新建的部门
        response_delete_company = requests.delete("http://182.92.81.159/api/company/department/"+add_id,
                                                  headers = headers)
        print("删除部门的结果为：{}".format(response_delete_company.json()))
        # 断言结果：响应状态码，success，code，message,data
        self.assertEqual(200, response_updata_company.status_code)
        self.assertEqual(True, response_updata_company.json().get("success"))
        self.assertEqual(10000, response_updata_company.json().get("code"))
        self.assertIn("操作成功", response_updata_company.json().get("message"))
        self.assertEqual(None, response_updata_company.json().get("data"))

