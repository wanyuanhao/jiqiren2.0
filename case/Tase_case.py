# -*- coding:utf-8
import unittest
from module.kehuguanli.kehuliebiao import kehuliebiao
from module.kehuguanli.chudanzhanbai import chuzhan_zhanbai
from module.kehuguanli.Interface_quote import Interface_quote
import configparser
import os

conf = configparser.ConfigParser()
'''读取配置文件'''
root_path = os.path.join(os.getcwd(), '..\config\config.ini')
conf.read(root_path, encoding='utf-8')  # 文件路径
licenseno = conf.get("baojia", "licenseno")# 获取配置文件指定的值
city = conf.get("baojia", "city")
xinzeng = Interface_quote()
chudan = chuzhan_zhanbai()
kehu = kehuliebiao()


class Test_case(unittest.TestCase):
    # 调登录接口拿到token
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # 新增续保——录入出单流程
    def test_case01(self):
        xinzeng.xubao(licenseno, city)
        result = kehu.find_licenseno(licenseno)
        kehu.enter_chudan(result['data'][0]['buid'])
        chudan.find_chudan(licenseno)


if __name__ == '__main__':
    print('执行Case')
    unittest.main(verbosity=2)

