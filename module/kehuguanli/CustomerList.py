# -*-conding:utf-8
from util.Requests_util import Requests_util
# from config.Headers import Headers
import datetime, json
import os, configparser
from config import Logs

logger = Logs.logs().logger
r = Requests_util()
conf = configparser.ConfigParser()
path = os.path.dirname(__file__)
conf.read(path + '..\..\..\config\config.ini', encoding='utf-8')
# headers = eval(config.get('headers', 'token'))
urls = conf.get('host', 'url')


# 客户列表
class CustomerList:
    # 根据车牌查询是否已在客户列表
    def find_licenseno(self, licenseno, headers):
        "根据车牌查询是否已在客户列表"
        data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                "topLabel": "tab_quanbukehu", "orderBy": {"orderByField": "updateTime", "orderByType": "desc"},
                "isFllowUp": "", "isDataLable": "", "dataTag": "", "isOpenGuanjia": 1, "licenseNo": licenseno}
        url = urls + '/carbusiness/api/v1/customer/querylist'
        try:
            logger.info(f'获取{licenseno}查询结果')
            response = r.request(url, 'post', data, headers, content_type='json')
            if response['message'] == '成功':
                if response['data'] is not None and len(response['data']) > 0:
                    logger.info('客户列表查询车牌通过')
                    return [True, response]
                else:
                    logger.info(f'{licenseno}查询结果为空')
                    return [False, response]
            else:
                logger.info('客户列表查询响应异常：{0}'.format(response))
                return [False]

        except Exception as e:
            logger.error('查询车牌异常：{0}'.format(e))
            return [False]

    # 根据buid录入出单，source默认录入人保
    def enter_chudan(self, licenseno, headers, source=4):
        logger.info('根据buid录入出单，默认录入人保')
        updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        chudan_time = datetime.datetime.now().strftime('%Y-%m-%d')
        logger.info(f'客户列表查询{licenseno}是否存在')
        find_result = self.find_licenseno(licenseno, headers)
        # 查询结果为True则执行
        if find_result[0]:
            # 拿第一buid
            logger.info('查询结果拿第一个buid')
            buid = find_result[1]['data'][0]['buid']
            url = urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
            data = {"defeatReasonContent": "", "bizTotal": "1000.99", "forceTotal": "500.11", "taxTotal": "15.01",
                    "reviewContent": "自动化录入", "singleTime": chudan_time, "jyPrice": "222",
                    "appointTime": updatetime,
                    "reviewStatus": 9, "reviewStatusName": "成功出单", "source": source, "buid": buid, "companyType": 4}
            try:
                # 发起录入出单请求
                logger.info('发起录入出单请求')
                response = r.request(url, 'post', data, headers, content_type='json')
                if response['message'] == '成功':
                    logger.info('message响应成功')
                    url = urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                        buid)
                    assert_response = r.request(url, 'get', headers=headers, content_type='json')
                    logger.info('获取响应message校验是否出单成功')
                    result = json.loads(assert_response['data']['list'][0]['jsonContent'])
                    if result['Buid'] == buid:
                        if result['ReviewStatusName'] == '成功出单' and int(result['Source']) == source and float(
                                result['BizTotal']) == 1000.99:
                            logger.info('出单成功')
                            return True
                    else:
                        logger.info('获取出单结果的Buid({0})不匹配：{1}'.format(buid,response))
                        return False
                # 判断本年度是否出过保单
                elif '本续保年度已存在' in response['message']:
                    logger.info('本年度已出过保单,提交覆盖')
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
                    logger.info('获取响应message校验是否出单成功')
                    response = r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '成功':
                        url = urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                            buid)
                        assert_response = r.request(url, 'get', headers=headers, content_type='json')
                        logger.info(f'出单成功，校验buid[{buid}]是否一致')
                        result = json.loads(assert_response['data']['list'][0]['jsonContent'])
                        if result['Buid'] == buid:
                            logger.info('校验出单状态、录入保司、金额是否一致')
                            if result['ReviewStatusName'] == '成功出单' and int(result['Source']) == source and float(
                                    result['BizTotal']) == 1000.99:
                                logger.info('出单成功')
                                return True
                        else:
                            logger.info('获取出单结果的Buid({0})不匹配：{1}'.format(buid,response))
                            return False
                    else:
                        logger.info('出单覆盖异常：{0}'.format(response))
                        return False

                else:
                    logger.info('录入出单不通过，msg：{0},响应：{1}'.format(response['message'], response))
                    return False
            except Exception as e:
                logger.error('录入出单请求异常：{0}'.format(e))
                return False
        else:
            logger.info('查询结果异常：{0}'.format(find_result))
            return False

    def enter_zhanbai(self, licenseno, headers):
        logger.info('录入战败')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'客户列表查询{licenseno}是否存在')
        find_result = self.find_licenseno(licenseno, headers)
        try:
            logger.info('校验查询结果是否为真')
            if find_result[0]:
                buid = find_result[1]['data'][0]['buid']
                url = urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
                data = {"defeatReasonContent": "无效数据（停机、空号）", "bizTotal": "", "forceTotal": "", "taxTotal": "",
                        "reviewContent": "自动化录入", "singleTime": "", "jyPrice": "", "appointTime": time,
                        "reviewStatus": 4, "reviewStatusName": "战败", "defeatReasonId": 68255, "buid": buid,
                        "companyType": 4}
                # 获取响应结果
                response = r.request(url, 'post', data, headers, content_type='json')
                # 校验响应是否通过
                if response['message'] == '成功':
                    url = urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                        buid)
                    result = r.request(url, 'get', headers=headers, content_type='json')
                    # 断言录入结果和实际录入结果是否一致
                    assert_result = json.loads(result['data']['list'][0]['jsonContent'])
                    # 断言录入结果和实际录入结果是否一致
                    if assert_result['ReviewStatusName'] == '战败':
                        logger.info('录入战败通过')
                        return True
                    else:
                        logger.info('录入结果和实际结果不符，校验响应字段（ReviewStatusName是否等于战败）车牌：{0}[{1}]'.format(licenseno,assert_result))
                        return False

                # 如果本年度已经录入过，重新覆盖录入结果
                elif '本续保年度已存在' in response['message']:
                    deteatId = response['data']['carPolicyId']
                    if deteatId is None:
                        logger.info('carPolicyId为None，替换成deteatId')
                        deteatId = response['data']['deteatId']
                    data = {"defeatReasonContent": "无效数据（停机、空号）", "bizTotal": "", "forceTotal": "", "taxTotal": "",
                            "reviewContent": "自动化录入", "singleTime": "", "jyPrice": "", "appointTime": time,
                            "defeatReasonId": 68255, "reviewStatus": 4, "reviewStatusName": "战败", "buid": buid,
                            "companyType": 4, "deteatId": deteatId, "carPolicyId": ""}
                    result = r.request(url, 'post', data, headers, content_type='json')
                    # 校验响应是否通过
                    if result['message'] == '成功':
                        url = urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                            buid)
                        result = r.request(url, 'get', headers=headers, content_type='json')
                        assert_result = json.loads(result['data']['list'][0]['jsonContent'])
                        # 断言录入结果和实际录入结果是否一致
                        if assert_result['ReviewStatusName'] == '战败':
                            logger.info('录入战败通过')
                            return True
                        else:
                            logger.info('录入结果和实际结果不符，校验响应字段（ReviewStatusName是否等于战败）车牌：{0}[{1}]'.format(licenseno,assert_result))
                            return False
                    else:
                        logger.info('覆盖战败响应结果异常：{0}'.format(result))
                        return False
                else:
                    logger.info('录入传单响应异常：{0}'.format(response))
                    return False
            elif find_result[1] == False:
                logger.info('客户列表没有这条数据：{0}'.format(find_result[0]))
                return False

        except Exception as e:
            logger.error('战败请求异常：{0}'.format(e))
            return False

    def del_licenseno(self, licenseno, headers):
        f'删除车牌{licenseno}'
        logger.info(f'客户列表查询{licenseno}是否存在')
        find_result = self.find_licenseno(licenseno, headers)
        try:
            logger.info("校验查询结果是否通过")
            if find_result[0]:
                url = urls + '/carbusiness/api/v1/customer/deleteCustomer'
                buid_list = []
                logger.info('遍历查询结果拿到所有buid')
                for result in find_result[1]['data']:
                    buid_list.append(result['buid'])
                # 如果拿到buid大于1，则把buid全部传过去删除
                if len(buid_list) > 1:
                    logger.info(f'拿到多个buid：{buid_list}，删除数据')
                    data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                            "isDataLable": "", "dataTag": "", "licenseNo": licenseno, "buids": buid_list,
                            "DelFunc": 1}
                    response = r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '操作成功':
                        logger.info('删除成功')
                        return True
                    else:
                        logger.info('删除失败：{0}'.format(response))
                        return False

                # 删除单个
                else:
                    logger.info(f"只拿到一个buid：{buid_list}，删除单个")
                    data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"},
                            "isFllowUp": "", "isDataLable": "", "dataTag": "", "licenseNo": licenseno, "DelFunc": 1}
                    response = r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '操作成功':
                        logger.info('删除成功')
                        return True
                    else:
                        logger.info('删除失败：{0}'.format(response))
                        return False
            # 等于False代表客户列表查询结果为空
            elif find_result[1] == False:
                logger.error('客户列表查询结果为空:{0}'.format(find_result[0]))
                return False
        except Exception as e:
            logger.info(f'删除车牌异常：{e}')
            return False

    def fenpei_avg(self, headers):
        '客户列表分配'
        logger.info('客户列表分配')
        try:
            # 获取客户列表数据接口
            url = urls + '/carbusiness/api/v1/customer/querylist'
            data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_quanbukehu",
                    "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                    "isDataLable": "", "dataTag": "", "isOpenGuanjia": 1}
            logger.info("获取客户列表全部客户的数据")
            resutl = r.request(url, 'post', data, headers, content_type='json')
            if resutl['message'] == '成功':
                # 默认获取客户列表前4条数据的buid，然后分配
                buids = []
                conut = 0
                logger.info('拿到前4个buid')
                for buid in resutl['data']:
                    conut += 1
                    buids.append(buid['buid'])
                    if conut == 4:
                        break
                # 分配接口
                url = urls + '/carbusiness/api/v1/customer/DistributeCustomer'
                data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_quanbukehu",
                        "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                        "isDataLable": "", "dataTag": "", "distributeEmployeeIds": [287523], "averageCount": 4,
                        "allocationRule": 1, "buids": buids}
                logger.info(f'分配数据[{buids}]给ID为(287523)的用户')
                resutl = r.request(url, 'post', data, headers, 'json')
                if resutl['message'] == '操作成功':
                    url = urls + '/carbusiness/api/v1/customer/querylist'
                    data = {"pageIndex": 1, "pageSize": 15, "buids": buids, "selectType": 1,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                            "isDataLable": "", "dataTag": "", "firstSearch": ""}
                    resutl = r.request(url, 'post', data, headers, content_type='json')
                    if resutl['message'] == '成功':
                        logger.info('校验分配人员是否匹配')
                        for buid in resutl['data']:
                            if buid['employeeId'] == 287523:
                                pass
                            else:
                                logger.info('分配的业务员和实际结果业务员不匹配，默认分配人ID是（287523）：{0}'.format(resutl['data'][0]))
                                return False
                        return True
                    else:
                        logger.info('获取客户列表数据异常：{0}'.format(resutl))
                        return False
                else:
                    logger.info('分配异常：{0}'.format(resutl))
                    return False
            else:
                logger.info('获取客户列表数据异常：{0}'.format(resutl))
                return False
        except Exception as e:
            logger.error('分配接口异常：{0}'.format(e))
            return False

    def customerlist_tab_count(self, headers):
        '获取客户列表每个TAB页的数量'
        logger.info('获取客户列表每个TAB页的数量')
        url = urls + '/carbusiness/api/v1/customer/queryTopLabelCount'
        data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_dangqikehu",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isDataLable": "",
                "dataTag": "", "tabs": ["tab_zhinengxubao", "tab_dangqikehu", "tab_shoufangkehu", "tab_jihuahuifang",
                                        "tab_jinrijindian", "tab_yuyuejindian", "tab_yuqikehu", "tab_quanbukehu",
                                        "tab_yichangshuju"]}
        result = r.request(url, 'post', data, headers, 'json')
        return result

    def chudan_count(self, headers):
        '获取出单总数'
        logger.info('获取出单总数')
        url = urls + '/carbusiness/api/v1/customer/quotationReceiptCount'
        data = {"pageIndex": 1, "pageSize": 15}
        result = r.request(url, 'post', data, headers, 'json')
        return result

    def zhanbai_count(self, headers):
        '获取战败总数'
        logger.info('获取战败总数')
        url = urls + '/carbusiness/api/v1/customer/defeatCount'
        data = {"pageIndex": 1, "pageSize": 15}
        result = r.request(url, 'post', data, headers, 'json')
        return result

    def get_empolyeeid(self, headers):
        '获取顶级ID'
        logger.info('获取顶级ID')
        url = urls + '/employee/api/v1/Login/EmployeeModuleAndInfo'
        data = {}
        result = r.request(url, 'post', data, headers, 'json')
        return result['data']['employeeInfo']['agentId']

    def agent_count(self, headers, top_agent):
        '业务员总数'
        url = urls + '/employee/api/v1/Role/RoleListByCompId'
        data = {"compId": top_agent, "employeeId": top_agent}
        result = r.request(url, 'post', data, headers, 'json')
        return len(result['data'])

    def role_count(self, headers, top_agent):
        '角色总数'
        url = urls + '/employee/api/v1/Role/RoleListByCompId'
        data = {"compId": top_agent, "employeeId": top_agent}
        result = r.request(url, 'post', data, headers, 'json')
        return len(result['data'])

    def call_count(self, headers):
        u'通话记录总数'
        url = urls + '/stats/api/v1/Call/GetCallRecordList'
        data = {"PageIndex": 1, "PageSize": 15}
        result = r.request(url, 'post', data, headers, 'json')
        return result['data']['totalCount']

    def plan_count(self, headers):
        u'获取接口返回的计划回访数量'
        logger.info('获取接口返回的计划回访数量')
        try:
            url = urls + '/carbusiness/api/v1/Customer/QueryReviewCount'
            data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_jihuahuifang",
                    "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                    "labelTimeSpan": 2,
                    "isDataLable": "", "dataTag": "", "dataTypeId": 0}
            result = r.request(url, 'post', data, headers, 'json')
            results = result['data']
            count_result = [results['jinrihuifang'], results['mingrihuifang'], results['liangrihuifang'],
                            results['sanrihuifang'], results['sirihuifang'], results['wurihuifang'],
                            results['liurihuifang'], results['qirihuifang'], results['qirihouhuifang']]
            logger.info(f'列表形式返回计划回访数量：{count_result}')
            return count_result
        except Exception as e:
            logger.error(f'plan_count执行异常:{e}')
            return False

    def plan_counts(self, headers, data_type=15, type=1):
        u'循环获取计划回访每个TAB页的数据'
        logger.info('循环获取计划回访每个TAB页的数据')
        url = urls + '/carbusiness/api/v1/customer/querylist'
        data = {"pageIndex": 1, "pageSize": data_type, "selectType": 1, "topLabel": "tab_jihuahuifang",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                "labelTimeSpan": type, "isDataLable": "", "dataTag": "", "dataTypeId": 0}
        result = r.request(url, 'post', data, headers, 'json')
        count = result['data']
        return [len(count), result]

    def shaixuan_baojiachenggong(self, headers):
        '筛选报价成功数据'
        logger.info('筛选报价成功数据')
        url = urls + '/carbusiness/api/v1/customer/querylist'
        data = {"pageIndex": 1, "pageSize": 45, "selectType": 1, "quoteStatus": [1], "topLabel": "tab_quanbukehu",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isDataLable": "",
                "dataTag": "", "dataTypeId": 0, "isMaintain": 1, "firstSearch": True}
        result = r.request(url, 'post', data, headers, 'json')
        if len(result['data']) > 0:
            logger.info('返回筛选结果')
            return result
        else:
            logger.error('没有报价成功数据')
            return False

    def quote_lishi(self, buid, headers):
        '获取报价历史'
        logger.info('获取报价历史')
        url = urls + '/carbusiness/api/v1/Renewal/GetQuoteHistory'
        data = {"buid": buid}
        result = r.request(url, 'post', data, headers, 'json')
        if len(result['data']) > 0:
            logger.info('返回报价历史结果')
            return result
        else:
            logger.error(f'buid：{buid}，无报价历史')
            return False

    def qiehuan_quote_lishi(self, id, headers):
        '根据报价历史id切换报价历史'
        logger.info('根据报价历史id切换报价历史')
        url = urls + '/carbusiness/api/v1/Renewal/GetQuoteRecord'
        data = {"id": id}
        result = r.request(url, 'post', data, headers, 'json')
        if result['message'] == "获取成功":
            logger.info('报价历史已切换')
            return result
        else:
            logger.error(f'切换报价历史失败')
            return False

    def query(self, headers):
        logger.info('获取全部客户数据')
        url = urls + '/carbusiness/api/v1/customer/querylist'
        data = {"pageIndex": 1, "pageSize": 45, "selectType": 1, "topLabel": "tab_quanbukehu",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isDataLable": "",
                "dataTag": "", "dataTypeId": 0, "lastMaintainDayRange": "", "isMaintain": 1, "isOpenGuanjia": 1,
                "firstSearch": True}
        try:
            result = r.request(url, 'post', data, headers, 'json')
            if result['message'] == '成功':
                return result
            else:
                return False
        except Exception as e:
            logger.info(f'获取全部客户数据异常：{e}')
            return False

    def enter_genjin(self, licenseno):
        logger.info(f'[{licenseno}]录入跟进')


if __name__ == '__main__':
    print('CustomerList')
