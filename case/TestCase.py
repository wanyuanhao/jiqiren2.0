# -*- coding:utf-8
import unittest
from module.customer_management.CustomerList import CustomerList
from module.customer_management.chudan_and_zhanbai import chudan_zhanbai
from module.customer_management.Interface_quote import Interface_quote
import configparser
import os,json
from config.Headers import Headers
from Logs import Logs
from module.workpanel.WorkPanel import WorkPanel
import datetime
from time import sleep


class TestCase(unittest.TestCase):
    # 调登录接口拿到token
    @classmethod
    def setUpClass(cls):
        cls.logger = Logs.Logs().logger
        conf = configparser.ConfigParser()
        '''读取配置文件'''
        path = os.path.join(os.getcwd(), '..\config\config.ini')
        conf.read(path, encoding='utf-8')  # 文件路径
        cls.licenseno = conf.get("baojia", "licenseno")  # 获取配置文件指定的值
        cls.city = conf.get("baojia", "city")
        cls.xinzeng = Interface_quote()
        cls.chudan = chudan_zhanbai()
        cls.customer = CustomerList()
        cls.headers = json.loads(conf.get('headers', 'token'))
        cls.urls = conf.get('host', 'url')
        cls.work = WorkPanel()
        cls.today_Ymd = datetime.datetime.now().strftime('%Y-%m-%d')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_case01(self):
        u'新增车牌—>录入出单'
        self.logger.info('※※※test_case01：新增数据——录入出单流程')
        result = self.xinzeng.xubao(self.licenseno, self.city)
        print(type(self.headers))
        self.assertTrue(result[0])
        result = self.customer.find_licenseno(self.licenseno, self.headers)
        self.assertTrue(result[0])
        result = self.customer.enter_chudan(self.licenseno, self.headers)
        if result[0]:
            result = self.chudan.find_chudan(self.licenseno, self.headers)
            self.assertTrue(result[0])

    def test_case02(self):
        u'顶级账户计划回访数据量对比'
        self.logger.info('※※※test_case02：顶级账户计划回访数据量对比')
        # i+1是计划回访的页码
        # result+10 是在接口返回的数量上+10，避免库里的数据比接口返回的数量多
        plan_name = ["今日", '明日', '两日', '三日', '四日', '五日', '六日', '七日', '七日后']
        result = self.customer.plan_count(self.headers)
        for i in range(len(result)):
            if i + 1 == 9:
                plan_count = self.customer.plan_counts(self.headers, result[i] + 10, 9999)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    self.logger.info('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])
            else:
                plan_count = self.customer.plan_counts(self.headers, result[i] + 10, i + 1)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    self.logger.info('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])

    def test_case03(self):
        '校验报价成功的数据是否有报价历史'
        self.logger.info('※※※test_case03：校验报价成功的数据是否有报价历史')
        result = self.customer.shaixuan_baojiachenggong(self.headers)
        # 判断结果是否为真
        self.assertTrue(result)
        self.logger.info(f"使用{result['data'][0]['buid']}获取报价历史，车牌：{result['data'][0]['licenseNo']}")
        lishi_result = self.customer.quote_lishi(result['data'][0]['buid'], self.headers)
        # 判断结果是否为真
        self.assertTrue(lishi_result)

    def test_case04(self):
        '校验切换报价历史是否成功'
        self.logger.info('※※※test_case04：校验切换报价历史是否成功')
        result = self.customer.shaixuan_baojiachenggong(self.headers)
        # 判断结果是否为真
        self.assertTrue(result)
        for index in range(len(result['data'])):
            lishi_result = self.customer.quote_lishi(result['data'][index]['buid'], self.headers)
            # 校验报价历史是否为空
            if lishi_result:
                # 校验报价历史数量是否大于1
                if len(lishi_result['data']) > 1:
                    id = lishi_result['data'][1]['id']
                    time1 = lishi_result['data'][1]['quoteTime']
                    lishi = self.customer.qiehuan_quote_lishi(id, self.headers)
                    time = lishi['data']['quetoTime']
                    print(time, time1)
                    self.assertEqual(time, time1)
                    break

    def test_case05(self):
        u'下级账户计划回访数据量对比,使用账号：18612938273'
        self.logger.info('※※※test_case05：下级账户计划回访数据量对比,使用账号：wanyuanhao')
        token = Headers().tokens('wanyuanhao')
        self.assertTrue(token)
        # i+1是计划回访的页码
        # result+10 是在接口返回的数量上+10，避免库里的数据比接口返回的数量多
        plan_name = ["今日", '明日', '两日', '三日', '四日', '五日', '六日', '七日', '七日后']
        result = self.customer.plan_count(token)
        for i in range(len(result)):
            if i + 1 == 9:
                # 七日后Tab的ID
                plan_count = self.customer.plan_counts(token, result[i] + 10, 9999)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    print('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])
            else:
                # i+1 是TABid
                plan_count = self.customer.plan_counts(token, result[i] + 10, i + 1)
                ss = f"接口返回数量：{result[i]}", f'实际条数：{plan_count[0]},f"接口响应：{plan_count[1]}"'
                if result[i] != plan_count[0]:
                    print('计划回访{0}数量不一致:{1}'.format(plan_name[i], ss))
                self.assertTrue(result[i] == plan_count[0])

    def test_case06(self):
        '客户列表分配，使用账号wanyuanhao,分配人：17501110001'
        self.logger.info('※※※test_case06：客户列表分配，使用账号wanyuanhao,分配人：17501110001')
        self.logger.info('执行分配用例')
        token = Headers().tokens('wanyuanhao')
        self.assertTrue(token)
        result = self.customer.fenpei_avg(token)
        self.assertTrue(result)

    def test_case07(self):
        '使用全部客户第5条数据录入战败'
        self.logger.info('※※※test_case07：使用全部客户第5条数据录入战败')
        query_result = self.customer.query(self.headers)
        licenseno = query_result['data'][4]['licenseNo']
        result = self.customer.enter_zhanbai(licenseno, self.headers)
        self.assertTrue(result[0])
        find_result = self.chudan.find_zhanbai(licenseno, self.headers)
        self.assertTrue(find_result[0])

    def test_case08(self):
        '使用全部客户第8条数据录入续保跟进'
        self.logger.info('※※※test_case08：使用全部客户第8条数据录入续保跟进')
        query_result = self.customer.query(self.headers)
        buid = query_result['data'][7]['buid']
        response = self.customer.enter_genjin(buid, self.headers)
        self.assertTrue(response['message'] == '成功')

    def test_case09(self):
        '客户列表不筛选导出全部客户TAB数据'
        self.logger.info('※※※test_case09：客户列表不筛选导出全部客户TAB数据')
        result = self.customer.export_customer(self.headers)
        self.assertTrue(result['message'] == '操作成功' or result['message'] == '未找到对应的内容')

    def test_case10(self):
        '客户列表筛选（战败）导出全部客户数据'
        self.logger.info('※※※test_case10：客户列表筛选（战败）导出全部客户数据')
        # [4] 是战败的筛选条件
        result = self.customer.export_customer(self.headers, [4])
        self.assertTrue(result['message'] == '操作成功' or result['message'] == '未找到对应的内容')

    def test_case11(self):
        '客户列表第9条数据录入定保成功预约'
        self.logger.info('※※※test_case11：定保录入成功预约')
        query_result = self.customer.query(self.headers)
        buid = query_result['data'][8]['buid']
        result = self.customer.enter_dingbao_chudan(buid, self.headers)
        self.assertTrue(result[0], True)

    def test_case12(self):
        '客户列表第10条数据录入定保成功预约'
        self.logger.info('※※※test_case12：定保录入战败')
        query_result = self.customer.query(self.headers)
        buid = query_result['data'][0]['buid']
        result = self.customer.enter_dingbao_zhanbai(buid, self.headers)
        self.assertTrue(result[0], True)

    def test_case13(self):
        '批量续保文件上传，上传完成后校验批次ID是否存在列表'
        self.logger.info('※※※test_case13：批量续保文件上传')
        path = os.path.dirname(__file__) + '/自动化上传.xlsx'
        response = self.customer.upload_file('自动化上传.xlsx', path, self.headers)
        self.assertTrue(response[0], True)
        resutl = self.customer.assert_upload(self.headers, response[1])
        self.assertTrue(resutl[0], True)

    def test_case14(self):
        '工作看板人员效能统计，校验录入出单、保费是否有统计'
        self.logger.info('※※※test_case14：工作看板人员效能统计，校验录入出单、保费是否有统计')
        # 获取没有录入战败前工作看板的历史统计结果
        result_count = self.work.today_personnel_work('171383', self.headers)
        self.logger.info(f'校验人员效能响应结果是否为None ：{result_count}')
        self.assertTrue(result_count != None)
        #出单统计 【insurancedCount】 出单金额 【insuranceAmount】
        insurancedCount = result_count['data']['insurancedCount']
        insuranceAmount = result_count['data']['insuranceAmount']
        # 获取出单列表出单时间是今天的buid
        chudan_re = self.chudan.query_chudan(self.headers, self.today_Ymd)
        today_chudan_buid = []
        self.logger.info("获取出单列表出单时间是今天的buid")
        if chudan_re is not None and len(chudan_re['data']) > 0:
            for i in chudan_re['data']:
                today_chudan_buid.append(i['buid'])
        else:
            self.logger.info(f'出单列表没有今日出单数据：{chudan_re}')
        # 获取客户列表的buid
        self.logger.info(f"出单时间是今天的buid:{today_chudan_buid}")
        self.logger.info('获取客户列表数据')
        response = self.customer.query(self.headers)
        self.logger.info(f"{response}")
        # 校验客户列表是否有数据
        if len(response['data']) > 0:
            for i in response['data']:
                # 校验客户列表的buid是否在今日出过单
                if i['buid'] not in today_chudan_buid:
                    # 如果未出单则拿这个buid录入出单，默认录入出单总金额 1738.11
                    self.logger.info(f"校验出此buid：{i['buid']}|车牌：{i['licenseNo']}今日未录入出单，发起出单录入请求")
                    result = self.customer.enter_chudan(i['licenseNo'], self.headers)
                    # 校验是否成功录入出单
                    self.assertTrue(result[0])
                    self.logger.info("出单录入成功后等待5秒，防止统计延迟。出单响应：{0}".format(result))
                    # 出单录入成功后等待5秒，防止统计延迟
                    sleep(5)
                    pre_result_count = self.work.today_personnel_work('171383', self.headers)
                    self.logger.info(f'二次获取人员效能响应结果，断言响应结果是否为None ：{pre_result_count}')
                    self.assertTrue(result_count != None)
                    pre_insurancedCount = pre_result_count['data']['insurancedCount']
                    pre_insuranceAmount = pre_result_count['data']['insuranceAmount']
                    self.logger.info(f'历史出单台次：{insurancedCount}+1，出单后台次：{pre_insurancedCount}')
                    self.assertTrue(insurancedCount +1 == pre_insurancedCount)
                    self.logger.info(f'历史出单金额：{insuranceAmount}+1738.11，出单后金额：{pre_insuranceAmount}')
                    self.assertTrue(str(insuranceAmount +1738.11) == str(pre_insuranceAmount))
                    break
        else:
            self.logger.info(f'客户列表无数据。响应：{response}')
            self.assertTrue(False)

    def test_case15(self):
        u'修改客户状态'
        self.logger.info("※※※test_case15：修改客户状态")
        response = self.customer.query(self.headers)
        buid = response['data'][13]['buid']
        result = self.customer.modify_state(buid,self.headers)
        self.assertTrue(result[0])

    def test_case16(self):
        u'修改客户类别'
        self.logger.info("※※※test_case16：修改客户类别")
        response = self.customer.query(self.headers)
        buid = response['data'][14]['buid']
        result = self.customer.modify_category(buid,self.headers)
        self.assertTrue(result[0])



if __name__ == '__main__':
    print('执行Case')
    # unittest.main(verbosity=2)
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestSuite()
    suite.addTest((TestCase("test_case01")))
    print(runner.run(suite))