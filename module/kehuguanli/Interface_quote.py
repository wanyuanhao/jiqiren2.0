# -*-coding:utf-8
from util.Requests_util import Requests_util
from config.Headers import Headers
import configparser,os
from config import Logs
logger = Logs.Logs().logger
config = configparser.ConfigParser()
r = Requests_util()
# 执行获取token的方法，更新到配置文件
path = os.path.dirname(__file__)
config.read(path+'\..\..\config\config.ini',encoding='utf-8')
urls = config.get('host','url')
headers = eval(config.get('headers','token'))

class Interface_quote:
    def xubao(self, licenseno, city):
        try:
            url = urls+'/carbusiness/api/v1/Renewal/RenewalCheck'
            data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                    "sixDigitsAfterIdCard": "", "renewalType": 4}
            # 发起续保请求
            logger.info(f'{licenseno}发起续保')
            response = r.request(url, 'post', data, headers=headers, content_type='json')
            if response['code'] == 1:
                url =urls+ '/carbusiness/api/v1/Renewal/SubmitRenewalAsync'
                data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                        "sixDigitsAfterIdCard": "", "renewalType": 4, "buid": 0}
                # 获取续保响应结果
                logger.info('获取续保响应结果')
                response = r.request(url, 'post', data, headers=headers, content_type='json')
                if response['code'] == 1:
                    logger.info('新增车牌成功')
                    return True
                else:
                    logger.info('获取续保结果异常：{0}'.format(response))
                    return False
            elif response['code'] == 2:
                url =urls+ '/carbusiness/api/v1/Renewal/SubmitRenewalAsync'
                data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                        "sixDigitsAfterIdCard": "", "renewalType": 4, "buid": 0}
                logger.info('获取续保响应结果')
                response = r.request(url, 'post', data, headers=headers, content_type='json')
                if response['code'] == 1:
                    logger.info('新增车牌成功')
                    return True
                else:
                    logger.info('获取续保结果异常：{0}'.format(response))
                    return False
            else:
                logger.info('续保响应结果异常:{0}'.format(response))
                return False
        except Exception as e:
            logger.error(f'续保执行异常：{e}')
            return False

    def baojia(self, response):
        msg = response['message']

    def tiaoshi(self):
        response = {'data': [1, 1], 'code': 1, 'message': '成功'}
        if response['message'] == '成功':
            if response['data'] is not None:
                is_pass = True
                print(int(len(response['data'])))
                print(response)
                return is_pass
            else:
                is_pass = False
                return is_pass
        else:
            print('已出保单查询响应msg为空：{0}'.format(response))
            return


if __name__ == '__main__':
    i = Interface_quote()
    result = i.xubao('京D12345',1)

