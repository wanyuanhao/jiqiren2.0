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
licenseno = conf.get("baojia", "licenseno")  # 获取配置文件指定的值
city = conf.get("baojia", "city")
xinzeng = Interface_quote()
chudan = chuzhan_zhanbai()
kehu = kehuliebiao()
headers = eval(conf.get('headers', 'token'))


class Test_case(unittest.TestCase):
    # 调登录接口拿到token
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # def test_case01(self):
    #     u'新增数据——录入出单流程'
    #     xinzeng.xubao(licenseno, city)
    #     result = kehu.find_licenseno(licenseno)
    #     kehu.enter_chudan(result['data'][0]['buid'])
    #     chudan.find_chudan(licenseno)

    def test_case02(self):
        u'计划回访数据量对比'
        # i+1是计划回访的页码
        # result+10 是在接口返回的数量上+10，避免库里的数据比接口返回的数量多
        plan_name = ["今日", '明日', '两日', '三日', '四日', '五日', '六日', '七日', '七日后']
        result = kehu.plan_count_jinri(headers)
        for i in range(len(result)):
            plan_count = kehu.plan_counts(headers, result[i] + 10, i + 1)
            ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count}'
            if result[i] == plan_count:
                pass
            else:
                return '计划回访{0}数量不一致，{1}'.format(plan_name[i],ss)

if __name__ == '__main__':
    print('执行Case')
    unittest.main(verbosity=2)



