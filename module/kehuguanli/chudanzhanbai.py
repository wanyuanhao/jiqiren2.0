from util.Requests_util import Requests_util
# from config.Headers import Headers
import datetime
import os, configparser
from config import Logs


# 出单、战败列表查询
class chudan_zhanbai:
    def __init__(self):
        config = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        config.read(path + '..\..\..\config\config.ini', encoding='utf-8')
        self.logger = Logs.Logs().logger
        self.headers = eval(config.get('headers', 'token'))
        self.urls = config.get('host', 'url')
        self.r = Requests_util()

    # 根据车牌查询是否有出单数据
    def find_chudan(self, licenseno):
        self.logger.info('出单列表查询')
        data = {"pageIndex": 1, "pageSize": 15, "LicenseNo": licenseno}
        url = self.urls + '/carbusiness/api/v1/customer/quotationReceiptList'
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        try:
            response = self.r.request(url, 'post', data, self.headers, content_type='json')
            if response['message'] == '成功':
                if len(response['data']) == 0:
                    self.logger.info('查询结果为空：{0}'.format(response))
                    return False
                elif response['data'][0]['licenseNo'] == licenseno and time in response['data'][0]['appearTime']:
                    self.logger.info('出单列表查询通过')
                    return True
                else:
                    self.logger.info('已出保单查询不通过，校验类型（车牌是否匹配、出单时间是否今天）：{0}'.format(response))
                    return False
            else:
                self.logger.info('已出保单查询结果异常：{0}'.format(response))
                return False

        except Exception as e:
            self.logger.error('已出保单查询请求异常：{0}'.format(e))
            return False

    def find_zhanbai(self, licenseno):
        self.logger.info('战败列表查询')
        data = {"pageIndex": 1, "pageSize": 15, "LicenseNo": licenseno}
        url = self.urls + '/carbusiness/api/v1/customer/defeatList'
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        try:
            response = self.r.request(url, 'post', data, headers=self.headers, content_type='json')
            if response['message'] == '成功':
                if len(response['data']) == 0:
                    self.logger.info('查询结果为空：{0}'.format(response))
                    return False
                elif response['data'][0]['licenseNo'] == licenseno and time in response['data'][0]['actionTime']:
                    self.logger.info('战败列表查询通过')
                    return True
                else:
                    self.logger.info('战败查询校验不通过，对比类型（车牌、录入时间是否今天），响应结果：{0}'.format(response))
                    return False
            else:
                self.logger.info('响应结果异常：{0}'.format(response))
                return False
        except Exception as e:
            self.logger.error('战败查询异常：{0}'.format(e))
            return False


if __name__ == '__main__':
    print('执行出单战败接口')
    run = chudan_zhanbai()
    print(run.find_zhanbai('京NJY977'))
