# 存放全局变量，共有的配置函数或者类
import logging
import os
from logging import handlers
# 设置一个获取当前文件的父级目录变量

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# os.path.dirname(file) 获取当前文件路径的目录
# os.path.abspath(__file__) 获取当前文件的位置,会把绝对路径的目录和文件名都返回
# D:\授课工作区\深圳14期就业班\web自动化day09\web自动化day09\AutoTpshop
# 定义一个初始化日志配置的函数，初始化日志的输出路径（例如：输出到控制和日志文件中）
# 定义全局变量headers
HEADERS = {"Content-Type":"application/json"}
#定义一个全局变量添加员工成功后ID
EMPID = ""
def init_logging():
# 创建日志器
    logger = logging.getLogger()
# 设置日志等级
    logger.setLevel(logging.INFO)
# 创建处理器：通过处理控制日志的打印（打印到控制台和日志文件中）
#     创建控制台处理器
    sh = logging.StreamHandler()
    # 创建文件处理器
    fh = logging.handlers.TimedRotatingFileHandler(BASE_DIR+"/log/ihrm.log",
                                                   when = "s",
                                                   interval=10,
                                                   backupCount=3,
                                                   encoding="utf-8")
# 设置日志的格式，所以需要创建格式和格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
# 将格式化器添加到处理器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
# 将处理器添加到日志器中
    logger.addHandler(sh)
    logger.addHandler(fh)
if __name__ == '__main__':
    # 初始化日志配置时，由于没有返回日志器，所以这个配置函数中的全部配置都会配置到logging的root节点
    init_logging()
    # 既然初始化到了root节点，那么我们可以就直接使用logging模块打印日志
    logging.info("测试日志会不会打印!")

