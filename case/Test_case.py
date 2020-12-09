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

    def test_case01(self):
        u'新增数据——录入出单流程'
        result = xinzeng.xubao(licenseno, city)
        self.assertTrue(result)
        # 客户列表查询车牌是否在客户列表
        result = kehu.find_licenseno(licenseno)
        self.assertTrue(result[0])
        result = kehu.enter_chudan(licenseno)
        print(result)
        if result:
            result = chudan.find_chudan(licenseno)
            print(result)
            self.assertTrue(result)

    def test_case02(self):
        u'计划回访数据量对比'
        # i+1是计划回访的页码
        # result+10 是在接口返回的数量上+10，避免库里的数据比接口返回的数量多
        plan_name = ["今日", '明日', '两日', '三日', '四日', '五日', '六日', '七日', '七日后']
        result = kehu.plan_count_jinri(headers)
        for i in range(len(result)):
            if i + 1 == 9:
                plan_count = kehu.plan_counts(headers, result[i] + 10, 9999)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    print('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])
            else:
                plan_count = kehu.plan_counts(headers, result[i] + 10, i + 1)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    print('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])

    def test_cese03(self):
        '校验报价成功的数据是否有报价历史'
        result = kehu.shaixuan_baojiachenggong()
        #判断结果是否为真
        self.assertTrue(result)
        result = kehu.quote_lishi(result['data'][0]['buid'])
        # 判断结果是否为真
        self.assertTrue(result)

    def test_cese04(self):
        '校验报价历史是否切换失败'
        result = kehu.shaixuan_baojiachenggong()
        #判断结果是否为真
        self.assertTrue(result)
        for index in range(len(result['data'])):
            lishi_result = kehu.quote_lishi(result['data'][index]['buid'])
            # 校验报价历史是否为空
            if lishi_result:
                # 校验报价历史数量是否大于1
                if len(lishi_result['data'])>1:
                    id = lishi_result['data'][1]['id']
                    time1 = lishi_result['data'][1]['quoteTime']
                    lishi = kehu.qiehuan_quote_lishi(id)
                    time = lishi['data']['quetoTime']
                    print(time,time1)
                    self.assertEqual(time,time1)
                    break

if __name__ == '__main__':
    print('执行Case')
    # unittest.main(verbosity=2)
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestSuite()
    suite.addTest(Test_case("test_cese04"))
    print(runner.run(suite))

