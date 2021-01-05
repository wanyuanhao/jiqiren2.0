# -*- coding:utf-8
import unittest
from module.kehuguanli.CustomerList import CustomerList
from module.kehuguanli.chudanzhanbai import chudan_zhanbai
from module.kehuguanli.Interface_quote import Interface_quote
import configparser
import os
from config.Headers import Headers
from config import Logs

logger = Logs.logs().logger
conf = configparser.ConfigParser()
'''读取配置文件'''
path = os.path.join(os.getcwd(), '..\config\config.ini')
conf.read(path, encoding='utf-8')  # 文件路径
licenseno = conf.get("baojia", "licenseno")  # 获取配置文件指定的值
city = conf.get("baojia", "city")
xinzeng = Interface_quote()
chudan = chudan_zhanbai()
kehu = CustomerList()
headers = eval(conf.get('headers', 'token'))
urls = conf.get('host', 'url')


class Test_case(unittest.TestCase):
    # 调登录接口拿到token
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_case01(self):
        u'新增车牌—>录入出单'
        logger.info('用例：新增数据——录入出单流程')
        result = xinzeng.xubao(licenseno, city)
        self.assertTrue(result)
        result = kehu.find_licenseno(licenseno, headers)
        self.assertTrue(result[0])
        result = kehu.enter_chudan(licenseno, headers)
        print(result)
        if result:
            result = chudan.find_chudan(licenseno)
            print(result)
            self.assertTrue(result)

    def test_case02(self):
        u'顶级账户计划回访数据量对比，使用账号：jiao'
        logger.info('用例：顶级账户计划回访数据量对比，使用账号：jiao')
        token = Headers().tokens('jiao')
        self.assertTrue(token)
        # i+1是计划回访的页码
        # result+10 是在接口返回的数量上+10，避免库里的数据比接口返回的数量多
        plan_name = ["今日", '明日', '两日', '三日', '四日', '五日', '六日', '七日', '七日后']
        result = kehu.plan_count(token)
        for i in range(len(result)):
            if i + 1 == 9:
                plan_count = kehu.plan_counts(token, result[i] + 10, 9999)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    logger.info('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])
            else:
                plan_count = kehu.plan_counts(token, result[i] + 10, i + 1)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    logger.info('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])

    def test_case03(self):
        '校验报价成功的数据是否有报价历史'
        logger.info('用例：校验报价成功的数据是否有报价历史')
        result = kehu.shaixuan_baojiachenggong(headers)
        # 判断结果是否为真
        self.assertTrue(result)
        lishi_result = kehu.quote_lishi(result['data'][0]['buid'], headers)
        # 判断结果是否为真
        self.assertTrue(lishi_result)

    def test_case04(self):
        '校验切换报价历史是否成功'
        logger.info('用例：校验切换报价历史是否成功')
        result = kehu.shaixuan_baojiachenggong(headers)
        # 判断结果是否为真
        self.assertTrue(result)
        for index in range(len(result['data'])):
            lishi_result = kehu.quote_lishi(result['data'][index]['buid'], headers)
            # 校验报价历史是否为空
            if lishi_result:
                # 校验报价历史数量是否大于1
                if len(lishi_result['data']) > 1:
                    id = lishi_result['data'][1]['id']
                    time1 = lishi_result['data'][1]['quoteTime']
                    lishi = kehu.qiehuan_quote_lishi(id, headers)
                    time = lishi['data']['quetoTime']
                    print(time, time1)
                    self.assertEqual(time, time1)
                    break

    def test_case05(self):
        u'下级账户计划回访数据量对比,使用账号：18612938273'
        logger.info('用例：下级账户计划回访数据量对比,使用账号：18612938273')
        token = Headers().tokens('18612938273')
        self.assertTrue(token)
        # i+1是计划回访的页码
        # result+10 是在接口返回的数量上+10，避免库里的数据比接口返回的数量多
        plan_name = ["今日", '明日', '两日', '三日', '四日', '五日', '六日', '七日', '七日后']
        result = kehu.plan_count(token)
        for i in range(len(result)):
            if i + 1 == 9:
                plan_count = kehu.plan_counts(token, result[i] + 10, 9999)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    print('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])
            else:
                plan_count = kehu.plan_counts(token, result[i] + 10, i + 1)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    print('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])

    def test_case06(self):
        '客户列表分配，使用账号wanyuanhao,分配人：17501110001'
        logger.info('用例：客户列表分配，使用账号wanyuanhao,分配人：17501110001')
        logger.info('执行分配用例')
        token = Headers().tokens('wanyuanhao')
        self.assertTrue(token)
        result = kehu.fenpei_avg(token)
        self.assertTrue(result)

    def test_case07(self):
        '使用全部客户第5条数据录入战败'
        logger.info('用例：使用全部客户第5条数据录入战败')
        query_result = kehu.query(headers)
        licenseno = query_result['data'][4]['licenseNo']
        result = kehu.enter_zhanbai(licenseno, headers)
        self.assertTrue(result)
        find_result = chudan.find_zhanbai(licenseno)
        self.assertTrue(find_result)

    def test_case08(self):
        '使用全部客户第8条数据录入续保跟进'
        logger.info('用例：使用全部客户第8条数据录入续保跟进')
        query_result = kehu.query(headers)
        buid = query_result['data'][7]['buid']
        response = kehu.enter_genjin(buid, headers)
        self.assertTrue(response['message'] == '成功')

    def test_case09(self):
        '客户列表不筛选导出全部客户TAB数据'
        logger.info('用例：客户列表不筛选导出全部客户TAB数据')
        result = kehu.export_customer(headers)
        self.assertTrue(result['message'] == '操作成功' or result['message'] == '未找到对应的内容')

    def test_case10(self):
        '客户列表筛选（战败）导出全部客户数据'
        logger.info('用例：客户列表筛选（战败）导出全部客户数据')
        # [4] 是战败的筛选条件
        result = kehu.export_customer(headers, [4])
        self.assertTrue(result['message'] == '操作成功' or result['message'] == '未找到对应的内容')

    def test_case11(self):
        '客户列表第9条数据录入定保成功预约'
        logger.info('用例：定保录入成功预约')
        query_result = kehu.query(headers)
        buid = query_result['data'][8]['buid']
        result = kehu.enter_dingbao_chudan(buid, headers)
        self.assertTrue(result[0], True)

    def test_case12(self):
        '客户列表第10条数据录入定保成功预约'
        logger.info('用例：定保录入战败')
        query_result = kehu.query(headers)
        buid = query_result['data'][0]['buid']
        result = kehu.enter_dingbao_zhanbai(buid, headers)
        self.assertTrue(result[0], True)


if __name__ == '__main__':
    print('执行Case')
    # unittest.main(verbosity=2)
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestSuite()
    suite.addTest(Test_case("test_case12"))
    runner.run(suite)
