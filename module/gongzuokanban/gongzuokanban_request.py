import unittest
from util.Requests_util import Requests_util
from config.Headers import Headers
import configparser
import os
config = configparser.ConfigParser()
path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
config.read(path+'/config/config.ini',encoding='utf-8')
headers = config.get('headers','token')
header = eval(headers)

# header = Headers().token()
r = Requests_util()
host = 'https://bot.91bihu.com'  # 线上

# host='http://userssodev.91bihu.me'   #线下

class Test_Case(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Headers().token('wanyuanhao')

    def testcase01(self):
        '工作看板EmpEffectTotalNew'
        # 工作看板EmpEffectTotalNew
        url = host + '/stats/api/v1/Panel/EmpEffectTotalNew'
        data = {"deptId": [], "categoryinfoId": [], "searchEmployeeId": [],
                "dataRangeTime": ["2020-09-20 00:00:00", "2020-09-20 23:59:59"], "pageIndex": 1, "pageSize": 50,
                "total": 0, "compId": 171383, "employeeId": 171383}
        response = r.request(url, 'post', params=data, headers=header, content_type='json')
        self.assertEqual(response['code'], 1)

    def testcase02(self):
        # 工作看板GetContinuedPeriods获取续保天数
        u"工作看板GetContinuedPeriods获取续保天数"
        url = host + '/carbusiness/api/v1/Renewal/GetContinuedPeriods'
        response = r.request(url, 'post', headers=header)
        self.assertEqual(response['code'], 1)

    def testcase03(self):
        # 工作看板RenewStatisNew
        url = host + '/stats/api/v1/Panel/RenewStatisNew'
        data = {"dataRangeTime": ["2020-05-01 00:00:00", "2020-10-31 23:59:59"], "deptId": [], "categoryinfoId": [],
                "searchEmployeeId": [], "compId": 171383, "employeeId": 171383}
        response = r.request(url, 'post', data, headers=header, content_type='json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '结果异常：{}'.format(response))

    def testcase04(self):
        url = host + '/stats/api/v1/Panel/EmpEffectNewList'
        data = {"deptId": [], "categoryinfoId": [], "searchEmployeeId": [],
                "dataRangeTime": ["2020-09-22 00:00:00", "2020-09-22 23:59:59"], "pageIndex": 1, "pageSize": 50,
                "total": 0, "compId": 171383, "employeeId": 171383}
        response = r.request(url, 'post', data, headers=header, content_type='json')
        self.assertTrue(response['code'], 1)

    def testcase05(self):
        url = host + '/stats/api/v1/Panel/CustomerAnalysisList'
        data = {"year": 2020, "month": 9, "renewPeriod": 90, "categoryinfoId": [], "deptId": [], "searchEmployeeId": [],
                "compId": 171383, "employeeId": 171383, "pageSize": 15, "pageIndex": 1, "total": 0}
        response = r.request(url, 'post', data, headers=header, content_type='json')
        list = response['data']['dataList']
        for i in list:
            self.assertTrue(len(i['employeeName']) > 0, '结果异常employeeId=' + str(i['employeeId']))

    def testcase06(self):
        url = host + '/stats/api/v1/Panel/DefeatCategoryinfoAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1, '结果异常:{}'.format(response))

    def testcase07(self):
        url = host + '/stats/api/v1/Panel/DefeatDayAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)

    def testcase08(self):
        url = host + '/stats/api/v1/Panel/FollowUpAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '结果异常')

    def testcase09(self):
        url = host + '/stats/api/v1/Panel/FollowUpStatusAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '结果异常')

    def testcase10(self):
        url = host + '/stats/api/v1/Panel/InsuranceCompAnalysisNew'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '结果异常')

    def testcase11(self):
        url = host + '/stats/api/v1/Panel/InsuranceCategoryinfoAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '结果异常')

    def testcase12(self):
        url = host + '/stats/api/v1/Panel/InsuranceDayAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '结果异常')

    def testcase13(self):
        # 人员效能导出
        url = host + '/stats/api/v1/Panel/ExcelExportEmpEffect'
        data = {"deptId": [], "categoryinfoId": [], "searchEmployeeId": [],
                "dataRangeTime": ["2020-09-01 00:00:00", "2020-09-30 23:59:59"], "pageIndex": 1, "pageSize": 50,
                "total": 4, "compId": 171383, "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertTrue(response['message'] == '成功', '结果异常：{}'.format(response))
        self.assertTrue('image.91bihu.com' in response['data'], '下载链接异常')

    def testcase14(self):
        # 人员效能筛选部门名称
        url = host + '/stats/api/v1/Panel/EmpEffectTotalNew'
        data = {"deptId": [2869, 4208, 7862], "categoryinfoId": [], "searchEmployeeId": [],
                "dataRangeTime": ["2020-09-01 00:00:00", "2020-09-30 23:59:59"], "pageIndex": 1, "pageSize": 50,
                "total": 4, "compId": 171383, "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '人员效能筛选结果异常')

        url2 = host + '/stats/api/v1/Panel/EmpEffectNewList'
        data2 = {"deptId": [2869, 4208, 7862], "categoryinfoId": [], "searchEmployeeId": [],
                 "dataRangeTime": ["2020-09-01 00:00:00", "2020-09-30 23:59:59"], "pageIndex": 1, "pageSize": 50,
                 "total": 4, "compId": 171383, "employeeId": 171383}
        response2 = r.request(url2, 'post', data2, header, 'json')
        self.assertEqual(response2['code'], 1)
        self.assertTrue(len(response2['data']['dataList']) > 0, '人员效能查询结果异常：{EmpEffectNewList}')

    def testcase15(self):
        # 客户分析筛选客户类别
        url = host + '/stats/api/v1/Panel/CustomerAnalysisList'
        data = {"year": 2020, "month": 9, "renewPeriod": 90, "categoryinfoId": [40047, 40049, 40051, 46547, 100017, 0],
                "deptId": [], "searchEmployeeId": [], "compId": 171383, "employeeId": 171383, "pageSize": 15,
                "pageIndex": 1, "total": 6}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']['dataList']) > 0, '客户分析筛选结果异常')

    def testcase16(self):
        # 客户分析导出
        url = host + '/stats/api/v1/Panel/ExcelExportCustomerAnalysis'
        data = {"year": 2020, "month": 9, "renewPeriod": 90, "categoryinfoId": [40047, 40049, 40051, 46547, 100017, 0],
                "deptId": [], "searchEmployeeId": [], "compId": 171383, "employeeId": 171383, "pageSize": 15,
                "pageIndex": 1, "total": 6}
        response = r.request(url, 'post', data, header, 'json')
        self.assertTrue(response['message'] == '成功', '客户分析导出异常')
        self.assertTrue('image.91bihu.com' in response['data'], '下载链接异常')

    def testcase17(self):
        # 跟进分析导出
        url = host + '/stats/api/v1/Panel/ExcelExportFollowAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertTrue(response['message'] == '成功', '跟进分析导出异常')
        self.assertTrue('image.91bihu.com' in response['data'], '下载链接异常')

    def testcase18(self):
        # 跟进分析筛选用户姓名
        url = host + '/stats/api/v1/Panel/FollowUpAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [],
                "searchEmployeeId": [171383, 222523, 244365, 287523, 290405, 350357, 377639, 377643], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '跟进次数结果异常')
        url2 = host + '/stats/api/v1/Panel/FollowUpStatusAnalysis'
        data2 = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [],
                 "searchEmployeeId": [171383, 222523, 244365, 287523, 290405, 350357, 377639, 377643], "compId": 171383,
                 "employeeId": 171383}
        response2 = r.request(url2, 'post', data2, header, 'json')
        self.assertTrue(len(response2['data']) > 0, '跟进信息分布结果异常')

    def testcase19(self):
        # 出单分析出单保司分布筛选
        url = host + '/stats/api/v1/Panel/InsuranceCompAnalysisNew'
        data = {"year": 2020, "month": 9, "deptId": [2869, 4208, 7862],
                "categoryinfoId": [40047, 40049, 40051, 46547, 100017, 0],
                "searchEmployeeId": [171383, 222523, 244365, 287523, 290405, 350357, 377639, 377643], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '出单保司分布异常')
        url2 = host + '/stats/api/v1/Panel/InsuranceCategoryinfoAnalysis'
        data2 = {"year": 2020, "month": 9, "deptId": [2869, 4208, 7862],
                 "categoryinfoId": [40047, 40049, 40051, 46547, 100017, 0],
                 "searchEmployeeId": [171383, 222523, 244365, 287523, 290405, 350357, 377639, 377643], "compId": 171383,
                 "employeeId": 171383}
        response2 = r.request(url2, 'post', data2, header, 'json')
        self.assertEqual(response2['code'], 1, '出单客户类别分布异常')
        url3 = host + '/stats/api/v1/Panel/InsuranceDayAnalysis'
        data3 = {"year": 2020, "month": 9, "deptId": [2869, 4208, 7862],
                 "categoryinfoId": [40047, 40049, 40051, 46547, 100017, 0],
                 "searchEmployeeId": [171383, 222523, 244365, 287523, 290405, 350357, 377639, 377643], "compId": 171383,
                 "employeeId": 171383}
        response3 = r.request(url3, 'post', data3, header, 'json')
        self.assertTrue(len(response3['data']) > 0, '出单投保天数分布异常')

    def testcase20(self):
        # 出单分析导出
        url = host + '/stats/api/v1/Panel/ExcelExportInsuranceAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [2869, 4208, 7862],
                "categoryinfoId": [40047, 40049, 40051, 46547, 100017, 0],
                "searchEmployeeId": [171383, 222523, 244365, 287523, 290405, 350357, 377639, 377643], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['message'], '成功')
        self.assertTrue('image.91bihu.com' in response['data'], '出单分析导出异常')

    def testcase21(self):
        # 战败分析出单保司分布筛选
        url = host + '/stats/api/v1/Panel/DefeatReasonAnalysisNew'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['code'], 1)
        self.assertTrue(len(response['data']) > 0, '战败原因分布异常')
        url2 = host + '/stats/api/v1/Panel/DefeatCategoryinfoAnalysis'
        data2 = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                 "employeeId": 171383}
        response2 = r.request(url2, 'post', data2, header, 'json')
        self.assertEqual(response2['code'], 1, '战败：客户类别分布异常')
        url3 = host + '/stats/api/v1/Panel/DefeatDayAnalysis'
        data3 = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                 "employeeId": 171383}
        response3 = r.request(url3, 'post', data3, header, 'json')
        self.assertTrue(len(response3['data']) > 0, '战败投保天数分布异常')

    def testcase22(self):
        # 战败分析导出
        url = host + '/stats/api/v1/Panel/ExcelExportDefeatAnalysis'
        data = {"year": 2020, "month": 9, "deptId": [], "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383,
                "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertEqual(response['message'], '成功')
        self.assertTrue('image.91bihu.com' in response['data'], '战败分析导出异常')

    def testcase23(self):
        # 续保分析筛选查询
        url = host + '/stats/api/v1/Panel/RenewStatisNew'
        data = {"dataRangeTime": ["2020-07-01 00:00:00", "2020-12-31 23:59:59"], "deptId": [2869, 4208, 7862],
                "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383, "employeeId": 171383}
        response = r.request(url, 'post', data, header, 'json')
        self.assertTrue(len(response['data']) > 0, '续保分析筛选结果异常')

    def testcase24(self):
        # 续保分析导出
        url = host + '/stats/api/v1/Panel/ExcelExportRenewStatis'
        data = {"dataRangeTime": ["2020-07-01 00:00:00", "2020-12-31 23:59:59"], "deptId": [2869, 4208, 7862],
                "categoryinfoId": [], "searchEmployeeId": [], "compId": 171383, "employeeId": 171383}
        response = r.request(url, 'post', params=data, headers=header, content_type='json')
        self.assertTrue('image.91bihu.com' in response['data'], '续保分析导出异常')


if __name__ == '__main__':
    # 用例调试
    # suite = unittest.TestSuite()
    # suite.addTests([Test_Case('testcase13'), Test_Case('testcase14'), Test_Case('testcase15'), Test_Case('testcase16')])
    # run = unittest.TextTestRunner(verbosity=2)
    # run.run(suite)
    unittest.main(verbosity=2)
