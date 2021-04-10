# -*-coding:utf-8
from util.Requests_util import Requests_util
import configparser, os,json
from Logs import Logs


class Interface_quote:
    def __init__(self):
        config = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        config.read(path + '\..\..\config\config.ini', encoding='utf-8')
        self.logger = Logs.Logs().logger
        self.r = Requests_util()
        self.urls = config.get('host', 'url')
        self.headers = json.loads(config.get('headers', 'token'))

    def xubao(self, licenseno, city):
        try:
            url = self.urls + '/carbusiness/api/v1/Renewal/RenewalCheck'
            data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                    "sixDigitsAfterIdCard": "", "renewalType": 4}
            # 发起续保请求
            self.logger.info(f'{licenseno}发起续保')
            response = self.r.request(url, 'post', data, headers=self.headers, content_type='json')
            if response['code'] == 1:
                url = self.urls + '/carbusiness/api/v1/Renewal/SubmitRenewalAsync'
                data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                        "sixDigitsAfterIdCard": "", "renewalType": 4, "buid": 0}
                # 获取续保响应结果
                self.logger.info('获取续保响应结果')
                response = self.r.request(url, 'post', data, headers=self.headers, content_type='json')
                if response['code'] == 1:
                    self.logger.info('新增车牌成功')
                    return [True,response]
                else:
                    self.logger.info('获取续保结果异常：{0}'.format(response))
                    return [False]
            elif response['code'] == 2:
                url = self.urls + '/carbusiness/api/v1/Renewal/SubmitRenewalAsync'
                data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                        "sixDigitsAfterIdCard": "", "renewalType": 4, "buid": 0}
                self.logger.info('获取续保响应结果')
                response = self.r.request(url, 'post', data, headers=self.headers, content_type='json')
                if response['code'] == 1:
                    self.logger.info('新增车牌成功')
                    return [True,response]
                else:
                    self.logger.info('获取续保结果异常：{0}'.format(response))
                    return [False]
            else:
                self.logger.info('续保响应结果异常:{0}'.format(response))
                return [False]
        except Exception as e:
            self.logger.error(f'续保执行异常：{e}')
            return [False]

    def baojia(self, response):
        try:
            if response[0]:
                res = response[1]
                buid = res['data']['buid']
            else:
                return [False,'续保失败，不能发起报价']
        except Exception as e:
            return '报价执行异常',f'{e}'

if __name__ == '__main__':
    i = Interface_quote()
