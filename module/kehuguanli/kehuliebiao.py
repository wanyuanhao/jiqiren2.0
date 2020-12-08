# -*-conding:utf-8
from util.Requests_util import Requests_util
# from config.Headers import Headers
import datetime, json
import os, configparser
import time
# Headers().token()
r = Requests_util()
config = configparser.ConfigParser()
path = os.path.dirname(__file__)
config.read(path + '..\..\..\config\config.ini', encoding='utf-8')
headers = eval(config.get('headers', 'token'))
urls = config.get('host', 'url')


# 客户列表
class kehuliebiao:
    # 根据车牌查询是否已在客户列表
    def find_licenseno(self, licenseno):
        "根据车牌查询是否已在客户列表"
        data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                "topLabel": "tab_quanbukehu", "orderBy": {"orderByField": "updateTime", "orderByType": "desc"},
                "isFllowUp": "", "isDataLable": "", "dataTag": "", "isOpenGuanjia": 1, "licenseNo": licenseno}
        url = urls + '/carbusiness/api/v1/customer/querylist'
        try:
            # 获取查询结果
            response = r.request(url, 'post', data, headers, content_type='json')
            if response['message'] == '成功':
                if response['data'] is not None and len(response['data']) > 0:
                    print('客户列表查询车牌通过')
                    return [response, True]
                else:
                    print('查询结果为空')
                    return [response, False]
            else:
                print('客户列表查询响应异常：{0}'.format(response))
                return

        except Exception as e:
            return '查询车牌异常：{0}'.format(e)

    # 根据buid录入出单，source默认录入人保
    def enter_chudan(self, licenseno, source=4):
        updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        chudan_time = datetime.datetime.now().strftime('%Y-%m-%d')
        result = self.find_licenseno(licenseno)
        if len(result) > 1:
            if result[1]:
                # 拿第一buid
                buid = result[0]['data'][0]['buid']
                url = urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
                data = {"defeatReasonContent": "", "bizTotal": "1000.99", "forceTotal": "500.11", "taxTotal": "15.01",
                        "reviewContent": "自动化录入", "singleTime": chudan_time, "jyPrice": "222",
                        "appointTime": updatetime,
                        "reviewStatus": 9, "reviewStatusName": "成功出单", "source": source, "buid": buid, "companyType": 4}
                try:
                    # 发起录入出单请求
                    response = r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '成功':
                        url = urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                            buid)
                        assert_response = r.request(url, 'get', headers=headers, content_type='json')
                        # 获取出单记录
                        result = json.loads(assert_response['data']['list'][0]['jsonContent'])
                        if result['Buid'] == buid:
                            if result['ReviewStatusName'] == '成功出单' and int(result['Source']) == source and float(
                                    result['BizTotal']) == 1000.99:
                                print('出单成功')
                                return True
                        else:
                            print('获取出单结果的Buid不匹配：{0}'.format(response))
                            return
                    # 判断本年度是否出过保单
                    elif '本续保年度已存在' in response['message']:
                        data = {"defeatReasonContent": "", "bizTotal": "1000.99", "forceTotal": "500.11",
                                "taxTotal": "15.01",
                                "reviewContent": "自动化录入", "singleTime": chudan_time, "jyPrice": "222",
                                "appointTime": updatetime,
                                "reviewStatus": 9, "reviewStatusName": "成功出单", "source": source, "buid": buid,
                                "companyType": 4,
                                "deteatId": "",
                                "carPolicyId": response['data']['carPolicyId']}
                        response = r.request(url, 'post', data, headers, content_type='json')
                        if response['message'] == '成功':
                            url = urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                                buid)
                            assert_response = r.request(url, 'get', headers=headers, content_type='json')
                            # 获取出单记录
                            result = json.loads(assert_response['data']['list'][0]['jsonContent'])
                            if result['Buid'] == buid:
                                if result['ReviewStatusName'] == '成功出单' and int(result['Source']) == source and float(
                                        result['BizTotal']) == 1000.99:
                                    print('出单成功')
                                    return True
                            else:
                                print('获取出单结果的Buid不匹配：{0}'.format(response))
                                return
                        else:
                            print('出单覆盖异常：{0}'.format(response))
                            return

                    else:
                        print('录入出单不通过，msg：{0},响应：{1}'.format(response['message'], response))
                        return
                except Exception as e:
                    print('录入出单请求异常：{0}'.format(e))
                    return
            elif result[1] == False:
                print('客户列表没有这条数据：{0}'.format(result[0]))
                return
            else:
                print('查询结果异常：{0}'.format(result))
                return
        else:
            print(result)
            return

    def enter_zhanbai(self, licenseno):
        result = self.find_licenseno(licenseno)
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            if len(result) > 1:
                # 校验查询结果是否为真
                if result[1]:
                    buid = result[0]['data'][0]['buid']
                    url = urls + '/carbusiness/api/v1/CustomerDetail/SaveConsumerReview'
                    data = {"defeatReasonContent": "无效数据（停机、空号）", "bizTotal": "", "forceTotal": "", "taxTotal": "",
                            "reviewContent": "自动化录入", "singleTime": "", "jyPrice": "", "appointTime": time,
                            "reviewStatus": 4, "reviewStatusName": "战败", "defeatReasonId": 68255, "buid": buid,
                            "companyType": 4}
                    # 获取响应结果
                    result = r.request(url, 'post', data, headers, content_type='json')
                    # 校验响应是否通过
                    if result['message'] == '成功':
                        url = urls + '/carbusiness/api/v1/CustomerDetail/QueryUserinfoSteps?buid={0}&groupId=0&pageIndex=1&pageSize=20'.format(
                            buid)
                        result = r.request(url, 'get', headers=headers, content_type='json')
                        # 断言录入结果和实际录入结果是否一致
                        assert_result = json.loads(result['data']['list'][0]['jsonContent'])
                        # 断言录入结果和实际录入结果是否一致
                        if assert_result['ReviewStatusName'] == '战败':
                            print('录入战败通过')
                            return True
                        else:
                            return '录入结果和实际结果不符，车牌：{0}'.format(licenseno)

                    # 如果本年度已经录入过，重新覆盖录入结果
                    elif '本续保年度已存在' in result['message']:
                        deteatId = result['data']['deteatId']
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
                                print('录入战败通过')
                                return True
                            else:
                                return '录入结果和实际结果不符，车牌：{0}'.format(licenseno)
                        else:
                            return '覆盖战败响应结果异常：{0}'.format(result)
                    else:
                        return '录入传单响应异常：{0}'.format(result)
                elif result[1] == False:
                    print('客户列表没有这条数据：{0}'.format(result[0]))
                    return
            else:
                return result
        except Exception as e:
            print('战败请求异常：{0}'.format(e))

    def del_licenseno(self, licenseno):
        u'查询车牌是否有数据'
        find_result = self.find_licenseno(licenseno)
        # 返回大于1的结果往下执行，否则结果异常
        if len(find_result) > 1:
            # 查询结果为真往下执行
            if find_result[1]:
                url = urls + '/carbusiness/api/v1/customer/deleteCustomer'
                buid_list = []
                # 遍历结果拿到buid
                for result in find_result[0]['data']:
                    buid_list.append(result['buid'])
                    print(buid_list)
                # 如果拿到buid大于1，则把buid全部传过去删除
                if len(buid_list) > 1:
                    if find_result:
                        data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                                "topLabel": "tab_quanbukehu",
                                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                                "isDataLable": "", "dataTag": "", "licenseNo": licenseno, "buids": buid_list,
                                "DelFunc": 1}
                        response = r.request(url, 'post', data, headers, content_type='json')
                        if response['message'] == '操作成功':
                            return True
                        else:
                            print('删除失败：{0}'.format(response))
                            return

                # 删除单个
                else:
                    data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "selectSearchValue": licenseno,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"},
                            "isFllowUp": "", "isDataLable": "", "dataTag": "", "licenseNo": licenseno, "DelFunc": 1}
                    response = r.request(url, 'post', data, headers, content_type='json')
                    if response['message'] == '操作成功':
                        return True
                    else:
                        print('删除失败：{0}'.format(response))
                        return
            # 等于False代表客户列表查询结果为空
            elif find_result[1] == False:
                print('客户列表查询结果为空:{0}'.format(find_result[0]))
                return
        else:
            return '客户列表查询异常：{0}'.format(find_result)

    def fenpei_avg(self):
        try:
            # 获取客户列表数据接口
            url = urls + '/carbusiness/api/v1/customer/querylist'
            data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_quanbukehu",
                    "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                    "isDataLable": "", "dataTag": "", "isOpenGuanjia": 1}
            resutl = r.request(url, 'post', data, headers, content_type='json')
            if resutl['message'] == '成功':
                # 默认获取客户列表前4条数据的buid，然后分配
                buids = []
                conut = 0
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
                # 获取分配结果
                resutl = r.request(url, 'post', data, headers, 'json')
                if resutl['message'] == '操作成功':
                    url = urls + '/carbusiness/api/v1/customer/querylist'
                    data = {"pageIndex": 1, "pageSize": 15, "buids": buids, "selectType": 1,
                            "topLabel": "tab_quanbukehu",
                            "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                            "isDataLable": "", "dataTag": "", "firstSearch": ""}
                    resutl = r.request(url, 'post', data, headers, content_type='json')
                    if resutl['message'] == '成功':
                        for buid in resutl['data']:
                            if buid['employeeId'] == 287523:
                                print('分配人和查询结果匹配')
                            else:
                                print('分配的业务员和实际结果业务员不匹配，默认分配人ID是（287523）：{0}'.format(resutl))
                        return True
                    else:
                        print('获取客户列表数据异常：{0}'.format(resutl))
                        return
                else:
                    print('分配异常：{0}'.format(resutl))
            else:
                print('获取客户列表数据异常：{0}'.format(resutl))
                return
        except Exception as e:
            print('分配接口异常：{0}'.format(e))
            return

    # 客户列表各个TAB总数
    def kehuliebiao_tab_count(self, headers):
        url = urls + '/carbusiness/api/v1/customer/queryTopLabelCount'
        data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_dangqikehu",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isDataLable": "",
                "dataTag": "", "tabs": ["tab_zhinengxubao", "tab_dangqikehu", "tab_shoufangkehu", "tab_jihuahuifang",
                                        "tab_jinrijindian", "tab_yuyuejindian", "tab_yuqikehu", "tab_quanbukehu",
                                        "tab_yichangshuju"]}
        result = r.request(url, 'post', data, headers, 'json')
        return result

    # 出单总数
    def chudan_count(self, headers):
        url = urls + '/carbusiness/api/v1/customer/quotationReceiptCount'
        data = {"pageIndex": 1, "pageSize": 15}
        result = r.request(url, 'post', data, headers, 'json')
        return result

    # 战败总数
    def zhanbai_count(self, headers):
        url = urls + '/carbusiness/api/v1/customer/defeatCount'
        data = {"pageIndex": 1, "pageSize": 15}
        result = r.request(url, 'post', data, headers, 'json')
        return result

    # 获取顶级ID
    def get_empolyeeid(self, headers):
        url = urls + '/employee/api/v1/Login/EmployeeModuleAndInfo'
        data = {}
        result = r.request(url, 'post', data, headers, 'json')
        return result['data']['employeeInfo']['agentId']

    # 业务员总数
    def agent_count(self, headers, top_agent):
        url = urls + '/employee/api/v1/Role/RoleListByCompId'
        data = {"compId": top_agent, "employeeId": top_agent}
        result = r.request(url, 'post', data, headers, 'json')
        return len(result['data'])

    # 角色总数
    def juese_count(self, headers, top_agent):
        url = urls + '/employee/api/v1/Role/RoleListByCompId'
        data = {"compId": top_agent, "employeeId": top_agent}
        result = r.request(url, 'post', data, headers, 'json')
        return len(result['data'])

    # 通话记录总数
    def call_count(self, headers):
        u'通话记录总数'
        url = urls + '/stats/api/v1/Call/GetCallRecordList'
        data = {"PageIndex": 1, "PageSize": 15}
        result = r.request(url, 'post', data, headers, 'json')
        return result['data']['totalCount']

    def plan_count_jinri(self, headers):
        u'获取接口返回的计划回访数量'
        try:
            url = urls + '/carbusiness/api/v1/Customer/QueryReviewCount'
            data = {"pageIndex": 1, "pageSize": 15, "selectType": 1, "topLabel": "tab_jihuahuifang",
                    "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "labelTimeSpan": 2,
                    "isDataLable": "", "dataTag": "", "dataTypeId": 0}
            result = r.request(url, 'post', data, headers, 'json')
            results = result['data']
            count_result = [results['jinrihuifang'], results['mingrihuifang'], results['liangrihuifang'],
                            results['sanrihuifang'], results['sirihuifang'], results['wurihuifang'],
                            results['liurihuifang'], results['qirihuifang'], results['qirihouhuifang']]
            return count_result
        except Exception as e:
            return ' plan_count_jinri执行异常'

    def plan_counts(self, headers, data_type=15, type=1):
        u'循环获取计划回访数据'
        url = urls + '/carbusiness/api/v1/customer/querylist'
        data = {"pageIndex": 1, "pageSize": data_type, "selectType": 1, "topLabel": "tab_jihuahuifang",
                "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "",
                "labelTimeSpan": type, "isDataLable": "", "dataTag": "", "dataTypeId": 0}
        result = r.request(url, 'post', data, headers, 'json')
        count = result['data']
        return [len(count),result]


if __name__ == '__main__':
    run = kehuliebiao()
    result = run.plan_counts(headers)
    print(result)
