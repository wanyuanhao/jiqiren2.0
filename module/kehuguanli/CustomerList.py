# -*-conding:utf-8
from util.Requests_util import Requests_util
# from config.Headers import Headers
import datetime, json
import os, configparser
from config import Logs
# 后引入的包，有的方法里面存在time所以改名为times
import time as times


# 客户列表
class CustomerList:
    def __init__(self):
        conf = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        conf.read(path + '..\..\..\config\config.ini', encoding='utf-8')
        self.logger = Logs.Logs().logger
        self.r = Requests_util()
        self.urls = conf.get('host', 'url')

    # 根据车牌查询是否已在客户列表
    def find_licenseno(self, licenseno, headers):
        "根据车牌查询是否已在客户列表"
        data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                "topLabel": "tab_quanbukehu", "orderBy": {"orderByField": "updateTime", "orderByType": "desc"},
                "isFllowUp": "", "isDataLable": "", "dataTag": "", "isOpenGuanjia": 1, "licenseNo": licenseno}
        url = self.urls + '/carbusiness/api/v1/customer/querylist'
        try:
            self.logger.info(f'获取{licenseno}查询结果')
            response = self.r.request(url, 'post', data, headers, content_type='json')
            if response['message'] == '成功':
                if response['data'] is not None and len(response['data']) > 0:
                    self.logger.info('客户列表查询车牌通过')
                    return [True, response]
                else:
                    self.logger.info(f'{licenseno}查询结果为空')
                    return [False, response]
            else:
                self.logger.info('客户列表查询响应异常：{0}'.format(response))
                return [False]

        except Exception as e:
            self.logger.error('查询车牌异常：{0}'.format(e))
            return [False]

    # 根据buid录入出单，source默认录入人保
    def enter_chudan(self, licenseno, headers, source=4):
        self.logger.info('根据buid录入出单，默认录入人保')
        updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        chudan_time = datetime.datetime.now().strftime('%Y-%m-%d')
        self.logger.info(f'客户列表查询{licenseno}是否存在')
        find_result = self.find_licenseno(licenseno, headers)
        # 查询结果为True则执行
        if find_result[0]:
            # 拿第一buid
            self.logger.info('查询结果拿第一个buid')
            buid = find_result[1]['data'][0]['buid']
            url = self.urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
            data = {"defeatReasonContent": "", "bizTotal": "1000.99", "forceTotal": "500.11", "taxTotal": "15.01",
                    "reviewContent": "自动化录入", "singleTime": chudan_time, "jyPrice": "222",
                    "appointTime": updatetime,
                    "reviewStatus": 9, "reviewStatusName": "成功出单", "source": source, "buid": buid, "companyType": 4}
            try:
                # 发起录入出单请求
                self.logger.info('发起录入出单请求')
                response = self.r.request(url, 'post', data, headers, content_type='json')
                if response['message'] == '成功':
                    self.logger.info('message响应成功')
                    url = self.urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                        buid)
                    # 等待2秒，录完之后库里有延迟会导致刚录入的获取不到
                    times.sleep(2)
                    assert_response = self.r.request(url, 'get', headers=headers, content_type='json')
                    self.logger.info('获取响应message校验是否出单成功')
                    result = json.loads(assert_response['data']['list'][0]['jsonContent'])
                    if result['Buid'] == buid:
                        if result['ReviewStatusName'] == '成功出单' and int(result['Source']) == source and float(
                                result['BizTotal']) == 1000.99:
                            self.logger.info('出单成功')
                            return True
                    else:
                        self.logger.info('获取出单结果的Buid({0})不匹配：{1}'.format(buid, response))
                        return False
                # 判断本年度是否出过保单
                elif '本续保年度已存在' in response['message']:
                    self.logger.info('本年度已出过保单,提交覆盖')
                    carPolicyId = response['data']['carPolicyId']
                    deteatId = response['data']['deteatId']
                    # if carPolicyId is None:
                    #     logger.info('carPolicyId为None，替换成deteatId')
                    #     carPolicyId =  response['data']['deteatId']
                    data = {"defeatReasonContent": "", "bizTotal": "1000.99", "forceTotal": "500.11",
                            "taxTotal": "15.01",
                            "reviewContent": "自动化录入", "singleTime": chudan_time, "jyPrice": "222",
                            "appointTime": updatetime,
                            "reviewStatus": 9, "reviewStatusName": "成功出单", "source": source, "buid": buid,
                            "companyType": 4,
                            "deteatId": deteatId,
                            "carPolicyId": carPolicyId}
                    self.logger.info('获取响应message校验是否出单成功')
                    response = self.r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '成功':
                        url = self.urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                            buid)
                        # 等待2秒，录完之后库里有延迟会导致刚录入的获取不到
                        times.sleep(2)
                        assert_response = self.r.request(url, 'get', headers=headers, content_type='json')
                        self.logger.info(f'出单成功，校验buid[{buid}]是否一致')
                        result = json.loads(assert_response['data']['list'][0]['jsonContent'])
                        if result['Buid'] == buid:
                            self.logger.info('校验出单状态、录入保司、金额是否一致')
                            if result['ReviewStatusName'] == '成功出单' and int(result['Source']) == source and float(
                                    result['BizTotal']) == 1000.99:
                                self.logger.info('出单成功')
                                return True
                        else:
                            self.logger.info('获取出单结果的Buid({0})不匹配：{1}'.format(buid, response))
                            return False
                    else:
                        self.logger.info('出单覆盖异常：{0}'.format(response))
                        return False

                else:
                    self.logger.info('录入出单不通过，msg：{0},响应：{1}'.format(response['message'], response))
                    return False
            except Exception as e:
                self.logger.error('录入出单请求异常：{0}'.format(e))
                return False
        else:
            self.logger.info('查询结果异常：{0}'.format(find_result))
            return False

    def enter_zhanbai(self, licenseno, headers):
        self.logger.info('录入战败')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info(f'客户列表查询{licenseno}是否存在')
        find_result = self.find_licenseno(licenseno, headers)
        try:
            self.logger.info('校验查询结果是否为真')
            if find_result[0]:
                buid = find_result[1]['data'][0]['buid']
                url = self.urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
                data = {"defeatReasonContent": "无效数据（停机、空号）", "bizTotal": "", "forceTotal": "", "taxTotal": "",
                        "reviewContent": "自动化录入", "singleTime": "", "jyPrice": "", "appointTime": time,
                        "reviewStatus": 4, "reviewStatusName": "战败", "defeatReasonId": 68255, "buid": buid,
                        "companyType": 4}
                # 获取响应结果
                response = self.r.request(url, 'post', data, headers, content_type='json')
                # 校验响应是否通过
                if response['message'] == '成功':
                    url = self.urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                        buid)
                    result = self.r.request(url, 'get', headers=headers, content_type='json')
                    # 等待2秒，录完之后库里有延迟会导致刚录入的获取不到
                    times.sleep(2)
                    assert_result = json.loads(result['data']['list'][0]['jsonContent'])
                    # 断言录入结果和实际录入结果是否一致
                    if assert_result['ReviewStatusName'] == '战败':
                        self.logger.info('录入战败通过')
                        return True
                    else:
                        self.logger.info(
                            '录入结果和实际结果不符，校验字段（[ReviewStatusName]是否等于战败）车牌：{0}[{1}]'.format(licenseno, assert_result))
                        return False

                # 如果本年度已经录入过，重新覆盖录入结果
                elif '本续保年度已存在' in response['message']:
                    deteatId = response['data']['carPolicyId']
                    if deteatId is None:
                        self.logger.info('carPolicyId为None，替换成deteatId')
                        deteatId = response['data']['deteatId']
                    data = {"defeatReasonContent": "无效数据（停机、空号）", "bizTotal": "", "forceTotal": "", "taxTotal": "",
                            "reviewContent": "自动化录入", "singleTime": "", "jyPrice": "", "appointTime": time,
                            "defeatReasonId": 68255, "reviewStatus": 4, "reviewStatusName": "战败", "buid": buid,
                            "companyType": 4, "deteatId": deteatId, "carPolicyId": ""}
                    result = self.r.request(url, 'post', data, headers, content_type='json')
                    # 校验响应是否通过
                    if result['message'] == '成功':
                        url = self.urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                            buid)
                        result = self.r.request(url, 'get', headers=headers, content_type='json')
                        # 等待2秒，录完之后库里有延迟会导致刚录入的获取不到
                        times.sleep(2)
                        assert_result = json.loads(result['data']['list'][0]['jsonContent'])
                        # 断言录入结果和实际录入结果是否一致
                        if assert_result['ReviewStatusName'] == '战败':
                            self.logger.info('录入战败通过')
                            return True
                        else:
                            self.logger.info('录入结果和实际结果不符，校验字段（[ReviewStatusName]是否等于战败）车牌：{0}[{1}]'.format(licenseno,
                                                                                                            assert_result))
                            return False
                    else:
                        self.logger.info('覆盖战败响应结果异常：{0}'.format(result))
                        return False
                else:
                    self.logger.info('录入传单响应异常：{0}'.format(response))
                    return False
            elif find_result[1] == False:
                self.logger.info('客户列表没有这条数据：{0}'.format(find_result[0]))
                return False

        except Exception as e:
            self.logger.error('战败请求异常：{0}'.format(e))
            return False

    def del_licenseno(self, licenseno, headers):
        f'删除车牌{licenseno}'
        self.logger.info(f'客户列表查询{licenseno}是否存在')
        find_result = self.find_licenseno(licenseno, headers)
        try:
            self.logger.info("校验查询结果是否通过")
            if find_result[0]:
                url = self.urls + '/carbusiness/api/v1/customer/deleteCustomer'
                buid_list = []
                self.logger.info('遍历查询结果拿到所有buid')
                for result in find_result[1]['data']:
                    buid_list.append(result['buid'])
                # 如果拿到buid大于1，则把buid全部传过去删除
                if len(buid_list) > 1:
                    self.logger.info(f'拿到多个buid：{buid_list}，删除数据')
                    data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                            "isDataLable": "", "dataTag": "", "licenseNo": licenseno, "buids": buid_list,
                            "DelFunc": 1}
                    response = self.r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '操作成功':
                        self.logger.info('删除成功')
                        return True
                    else:
                        self.logger.info('删除失败：{0}'.format(response))
                        return False

                # 删除单个
                else:
                    self.logger.info(f"只拿到一个buid：{buid_list}，删除单个")
                    data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"},
                            "isFllowUp": "", "isDataLable": "", "dataTag": "", "licenseNo": licenseno, "DelFunc": 1}
                    response = self.r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '操作成功':
                        self.logger.info('删除成功')
                        return True
                    else:
                        self.logger.info('删除失败：{0}'.format(response))
                        return False
            # 等于False代表客户列表查询结果为空
            elif find_result[1] == False:
                self.logger.error('客户列表查询结果为空:{0}'.format(find_result[0]))
                return False
        except Exception as e:
            self.logger.info(f'删除车牌异常：{e}')
            return False

    def fenpei_avg(self, headers):
        '客户列表分配'
        self.logger.info('客户列表分配')
        try:
            # 获取客户列表数据接口
            url = self.urls + '/carbusiness/api/v1/customer/querylist'
            data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_quanbukehu",
                    "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                    "isDataLable": "", "dataTag": "", "isOpenGuanjia": 1}
            self.logger.info("获取客户列表全部客户的数据")
            resutl = self.r.request(url, 'post', data, headers, content_type='json')
            if resutl['message'] == '成功':
                # 默认获取客户列表前4条数据的buid，然后分配
                buids = []
                conut = 0
                self.logger.info('拿到前4个buid')
                for buid in resutl['data']:
                    conut += 1
                    buids.append(buid['buid'])
                    if conut == 4:
                        break
                # 分配接口
                url = self.urls + '/carbusiness/api/v1/customer/DistributeCustomer'
                data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_quanbukehu",
                        "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                        "isDataLable": "", "dataTag": "", "distributeEmployeeIds": [287523], "averageCount": 4,
                        "allocationRule": 1, "buids": buids}
                self.logger.info(f'分配数据[{buids}]给ID为(287523)的用户')
                resutl = self.r.request(url, 'post', data, headers, 'json')
                if resutl['message'] == '操作成功':
                    url = self.urls + '/carbusiness/api/v1/customer/querylist'
                    data = {"pageIndex": 1, "pageSize": 15, "buids": buids, "selectType": 1,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                            "isDataLable": "", "dataTag": "", "firstSearch": ""}
                    resutl = self.r.request(url, 'post', data, headers, content_type='json')
                    if resutl['message'] == '成功':
                        self.logger.info('校验分配人员是否匹配')
                        for buid in resutl['data']:
                            if buid['employeeId'] == 287523:
                                pass
                            else:
                                self.logger.info('分配的业务员和实际结果业务员不匹配，默认分配人ID是（287523）：{0}'.format(resutl['data'][0]))
                                return False
                        return True
                    else:
                        self.logger.info('获取客户列表数据异常：{0}'.format(resutl))
                        return False
                else:
                    self.logger.info('分配异常：{0}'.format(resutl))
                    return False
            else:
                self.logger.info('获取客户列表数据异常：{0}'.format(resutl))
                return False
        except Exception as e:
            self.logger.error('分配接口异常：{0}'.format(e))
            return False

    def customerlist_tab_count(self, headers):
        '获取客户列表每个TAB页的数量'
        self.logger.info('获取客户列表每个TAB页的数量')
        url = self.urls + '/carbusiness/api/v1/customer/queryTopLabelCount'
        data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_dangqikehu",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isDataLable": "",
                "dataTag": "", "tabs": ["tab_zhinengxubao", "tab_dangqikehu", "tab_shoufangkehu", "tab_jihuahuifang",
                                        "tab_jinrijindian", "tab_yuyuejindian", "tab_yuqikehu", "tab_quanbukehu",
                                        "tab_yichangshuju"]}
        result = self.r.request(url, 'post', data, headers, 'json')
        return result

    def chudan_count(self, headers):
        '获取出单总数'
        self.logger.info('获取出单总数')
        url = self.urls + '/carbusiness/api/v1/customer/quotationReceiptCount'
        data = {"pageIndex": 1, "pageSize": 15}
        result = self.r.request(url, 'post', data, headers, 'json')
        return result

    def zhanbai_count(self, headers):
        '获取战败总数'
        self.logger.info('获取战败总数')
        url = self.urls + '/carbusiness/api/v1/customer/defeatCount'
        data = {"pageIndex": 1, "pageSize": 15}
        result = self.r.request(url, 'post', data, headers, 'json')
        return result

    def get_empolyeeid(self, headers):
        '获取顶级ID'
        self.logger.info('获取顶级ID')
        url = self.urls + '/employee/api/v1/Login/EmployeeModuleAndInfo'
        data = {}
        result = self.r.request(url, 'post', data, headers, 'json')
        return result['data']['employeeInfo']['agentId']

    def agent_count(self, headers, top_agent):
        '业务员总数'
        url = self.urls + '/employee/api/v1/Role/RoleListByCompId'
        data = {"compId": top_agent, "employeeId": top_agent}
        result = self.r.request(url, 'post', data, headers, 'json')
        return len(result['data'])

    def role_count(self, headers, top_agent):
        '角色总数'
        url = self.urls + '/employee/api/v1/Role/RoleListByCompId'
        data = {"compId": top_agent, "employeeId": top_agent}
        result = self.r.request(url, 'post', data, headers, 'json')
        return len(result['data'])

    def call_count(self, headers):
        u'通话记录总数'
        url = self.urls + '/stats/api/v1/Call/GetCallRecordList'
        data = {"PageIndex": 1, "PageSize": 15}
        result = self.r.request(url, 'post', data, headers, 'json')
        return result['data']['totalCount']

    def plan_count(self, headers):
        u'获取接口返回的计划回访数量'
        self.logger.info('获取接口返回的计划回访数量')
        try:
            url = self.urls + '/carbusiness/api/v1/Customer/QueryReviewCount'
            data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_jihuahuifang",
                    "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                    "labelTimeSpan": 2,
                    "isDataLable": "", "dataTag": "", "dataTypeId": 0}
            result = self.r.request(url, 'post', data, headers, 'json')
            results = result['data']
            count_result = [results['jinrihuifang'], results['mingrihuifang'], results['liangrihuifang'],
                            results['sanrihuifang'], results['sirihuifang'], results['wurihuifang'],
                            results['liurihuifang'], results['qirihuifang'], results['qirihouhuifang']]
            self.logger.info(f'列表形式返回计划回访数量：{count_result}')
            return count_result
        except Exception as e:
            self.logger.error(f'plan_count执行异常:{e}')
            return False

    def plan_counts(self, headers, data_type=15, type=1):
        u'循环获取计划回访每个TAB页的数据'
        self.logger.info('循环获取计划回访每个TAB页的数据')
        url = self.urls + '/carbusiness/api/v1/customer/querylist'
        data = {"pageIndex": 1, "pageSize": data_type, "selectType": 1, "topLabel": "tab_jihuahuifang",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                "labelTimeSpan": type, "isDataLable": "", "dataTag": "", "dataTypeId": 0}
        result = self.r.request(url, 'post', data, headers, 'json')
        count = result['data']
        return [len(count), result]

    def shaixuan_baojiachenggong(self, headers):
        '筛选报价成功数据'
        self.logger.info('筛选报价成功数据')
        url = self.urls + '/carbusiness/api/v1/customer/querylist'
        data = {"pageIndex": 1, "pageSize": 45, "selectType": 1, "quoteStatus": [1], "topLabel": "tab_quanbukehu",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isDataLable": "",
                "dataTag": "", "dataTypeId": 0, "isMaintain": 1, "firstSearch": True}
        result = self.r.request(url, 'post', data, headers, 'json')
        if len(result['data']) > 0:
            self.logger.info('返回筛选结果')
            return result
        else:
            self.logger.error('没有报价成功数据')
            return False

    def quote_lishi(self, buid, headers):
        '获取报价历史'
        self.logger.info('获取报价历史')
        url = self.urls + '/carbusiness/api/v1/Renewal/GetQuoteHistory'
        data = {"buid": buid}
        result = self.r.request(url, 'post', data, headers, 'json')
        if len(result['data']) > 0:
            self.logger.info('返回报价历史结果')
            return result
        else:
            self.logger.error(f'buid：{buid}，无报价历史')
            return False

    def qiehuan_quote_lishi(self, id, headers):
        '根据报价历史id切换报价历史'
        self.logger.info('根据报价历史id切换报价历史')
        url = self.urls + '/carbusiness/api/v1/Renewal/GetQuoteRecord'
        data = {"id": id}
        result = self.r.request(url, 'post', data, headers, 'json')
        if result['message'] == "获取成功":
            self.logger.info('报价历史已切换')
            return result
        else:
            self.logger.error(f'切换报价历史失败')
            return False

    def query(self, headers):
        self.logger.info('获取全部客户数据')
        url = self.urls + '/carbusiness/api/v1/customer/querylist'
        data = {"pageIndex": 1, "pageSize": 45, "selectType": 1, "topLabel": "tab_quanbukehu",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isDataLable": "",
                "dataTag": "", "dataTypeId": 0, "lastMaintainDayRange": "", "isMaintain": 1, "isOpenGuanjia": 1,
                "firstSearch": True}
        try:
            result = self.r.request(url, 'post', data, headers, 'json')
            if result['message'] == '成功':
                return result
            else:
                return False
        except Exception as e:
            self.logger.info(f'获取全部客户数据异常：{e}')
            return False

    def enter_genjin(self, buid, headers):
        self.logger.info(f'[buid:{buid}]录入普通跟进')
        time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        url = self.urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
        data = {"defeatReasonContent": "", "bizTotal": "", "forceTotal": "", "taxTotal": "", "reviewContent": "自动化录入",
                "singleTime": "", "jyPrice": "", "appointTime": f"{time}", "reviewStatus": 205619,
                "reviewStatusName": "自动化录入", "isTrusted": True, "buid": buid, "companyType": 4, "groupId": 1}
        self.logger.info('请求录入跟进')
        result = self.r.request(url, 'post', data, headers=headers, content_type='json')
        self.logger.info(f'返回录入跟进响应结果：{result}')
        return result

    def export_customer(self, headers, body=None):
        # body为None则是不筛选导出
        try:
            if body == None:
                self.logger.info('客户列表导出')
                url = self.urls + '/carbusiness/api/v1/customer/exportCustomer'
                data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_quanbukehu",
                        "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                        "isDataLable": "",
                        "dataTag": "", "dataTypeId": 0, "lastMaintainDayRange": "", "isMaintain": 1}
                response = self.r.request(url, 'post', data, headers, 'json')
                self.logger.info(f'返回导出响应结果：{response}')
                return response
            else:
                self.logger.info('客户列表导出')
                url = self.urls + '/carbusiness/api/v1/customer/exportCustomer'
                data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_quanbukehu",
                        "customerStatusIds": body,
                        "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                        "isDataLable": "",
                        "dataTag": "", "dataTypeId": 0, "lastMaintainDayRange": "", "isMaintain": 1}
                response = self.r.request(url, 'post', data, headers, 'json')
                self.logger.info(f'返回导出响应结果：{response}')
                return response
        except Exception as e:
            self.logger.error(f'export_customer 执行异常：{e}')
            return f'export_customer 执行异常：{e}'

    def enter_dingbao_chudan(self, buid, headers, deteatId=None, carPolicyId=None):
        '定保录入成功预约'
        try:
            self.logger.info('定保录入成功预约')
            time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            url = self.urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
            data = {"groupId": 7, "defeatReasonContent": "", "maintainAmount": "1000", "reviewContent": "自动化录入内容",
                    "singleTime": "2021-01-06", "appointTime": time, "reviewStatusName": "成功预约",
                    "reviewStatus": 9, "contentCategoryId": 8193, "contentCategoryInfo": "自动化录入", "isTrusted": True,
                    "deteatId": deteatId, "carPolicyId": carPolicyId, "buid": buid, "companyType": 4}
            result = self.r.request(url, 'post', data, headers, 'json')
            self.logger.info(f'校验响应结果：{result}')
            if result['message'] == '成功':
                self.logger.info('定保录入成功')
                return [True]
            elif '已存在定保预约出单/战败记录' in result['message']:
                self.logger.info('定保出单重复，确认覆盖')
                carPolicyId = result['data']['carPolicyId']
                deteatId = result['data']['deteatId']
                result = self.enter_dingbao_chudan(buid, headers, deteatId=deteatId, carPolicyId=carPolicyId)
                return result
            else:
                return [False, f'响应结果异常：{result}']
        except Exception as e:
            self.logger.error(f'enter_dingbao_chudan方法执行异常：{e}')
            return [False, f'enter_dingbao_chudan方法执行异常：{e}']

    def enter_dingbao_zhanbai(self, buid, headers, deteatId=None, carPolicyId=None):
        '定保录入战败'
        try:
            self.logger.info('定保录入战败')
            time = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            url = self.urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
            data = {"groupId": 7, "defeatReasonContent": "自动化录入", "maintainAmount": 0, "reviewContent": "自动化录入内容",
                    "singleTime": "", "appointTime": time, "reviewStatusName": "战败", "reviewStatus": 4,
                    "defeatReasonId": 8193, "contentCategoryId": 8193, "contentCategoryInfo": "自动化录入",
                    "isTrusted": True,
                    "deteatId": deteatId, "carPolicyId": carPolicyId, "buid": buid, "companyType": 4}
            result = self.r.request(url, 'post', data, headers, 'json')
            self.logger.info(f'校验响应结果：{result}')
            if result['message'] == '成功':
                self.logger.info('定保录入成功')
                return [True]
            elif '已存在定保预约出单/战败记录' in result['message']:
                self.logger.info('定保出单重复，确认覆盖')
                carPolicyId = result['data']['carPolicyId']
                deteatId = result['data']['deteatId']
                result = self.enter_dingbao_zhanbai(buid, headers, deteatId=deteatId, carPolicyId=carPolicyId)
                return result
            else:
                return [False, f'响应结果异常：{result}']

        except Exception as e:
            self.logger.error(f'enter_dingbao_chudan方法执行异常：{e}')
            return [False, f'enter_dingbao_chudan方法执行异常：{e}']

    def upload_file(self, filename, filepath, headers):
        '批量续保文件上传'
        try:
            self.logger.info('上传文件')
            url = self.urls + '/carbusiness/api/v1/BatchRenewal/BatchRenewalUpload'
            form_data = {'file': (filename, open(filepath, 'rb').read())}
            result_response = self.r.request(url, 'post', headers=headers, files=form_data)
            if result_response['message'] == '成功':
                file_path = result_response["data"]["filePath"]
                file_name = result_response['data']['fileName']
                self.logger.info(f'文件已上传到服务器：{file_path}')
                self.logger.info('默认FindDeptId: 2869（部门ID），只适用于wanyuanhao账号，上传城市为【北京】')
                # 默认FindDeptId: 2869（部门ID），只适用于wanyuanhao账号
                upload_url = self.urls + '/carbusiness/api/v1/BatchRenewal/BatchRenewalMethod'
                data = {"cityId": 1, "channelType": 2, "isHistoryRenewal": 0, "batchRenewalType": 1, "FindDeptId": 2869,
                        "isCoverSalesman": 0, "isAddWechat": 0, "fileName": file_name,
                        "filePath": file_path, "businessType": 0}
                upload_result = self.r.request(upload_url, 'post', data, headers, 'json')
                if upload_result['message'] == '上传成功':
                    self.logger.info(f'文件上传成功：{upload_result}')
                    return [True, upload_result]
                else:
                    self.logger.info(f"文件上传失败:{upload_result}")
                    return [False]
            else:
                self.logger.info(f"文件上传到服务器失败:{result_response}")
                return [False, f"文件上传到服务器失败:{result_response}"]
        except Exception as e:
            self.logger.error(f'upload_file方法执行异常：{e}')
            return [False, f'upload_file方法执行异常：{e}']

    def assert_upload(self, headers, response):
        '通过上传j结果校验列表是否存在该批次'
        try:
            self.logger.info(f'通过上传响应结果校验列表是否存在该批次，响应信息:{response}')
            upload_id = response['data']['batchRenewalId']
            url = self.urls + '/carbusiness/api/v1/BatchRenewal/GetBatchRenewalListMethod'
            data = {"pageIndex": 1, "pageSize": 15}
            self.logger.info('等待3秒获取列表批次，校验ID是否存在列表')
            times.sleep(3)
            # 获取列表批次
            result = self.r.request(url, 'post', data, headers, 'json')
            result_id = result['data']['dataList'][0]['id']
            if result_id == upload_id:
                return [True]
            else:
                self.logger.info(f'批次ID不存在列表，上传结果返回的id：{upload_id}，响应结果：{result}')
                return [False, f'批次ID不存在列表，上传结果返回的id：{upload_id}，响应结果：{result}']
        except Exception as e:
            self.logger.error(f'assert_upload方法执行异常：{e}')
            return [False, f'assert_upload方法执行异常：{e}']


if __name__ == '__main__':
    print('CustomerList')
