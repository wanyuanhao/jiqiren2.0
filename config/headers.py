from util.requestsutil import RequestsUtil
import configparser
import os,json
from logs import logs

r = RequestsUtil()
# 找到配置文件路径
path = os.path.dirname(__file__)
# 把读取配置的类包赋值
configs = configparser.ConfigParser()
# 读取配置文件
configs.read(path + '\config.ini', encoding='utf-8')
# 读取配置文件的指定配置
users = configs.get('host', 'user')
urls = configs.get('host', 'url')
logger = logs.Logs().logger


class Headers:
    # 获取到的token更新到config文件
    @classmethod
    def token_update_config(self, user):
        try:
            # url = urls + '/identity/connect/token'  # 老接口
            # data = {'grant_type': 'password',
            #         'username': user,
            #         'password': 'wyh12345',
            #         'scope': 'employee_center car_business smart_car_mgts',
            #         'client_id': 'bot',
            #         'client_secret': 'secret'}
            url = urls + '/identity/api/v1/Login/LoginApi2'
            data = {"grant_type": "password", "username": "wanyuanhao", "password": "wyh12345",
                    "scope": "employee_center car_business smart_car_mgts", "client_id": "bot",
                    "client_secret": "secret"}
            response = r.request(url, 'post', data,content_type='json')
            if 'error' in response:
                logger.info('账号：{0}，登录报错：{1}'.format(user, response))
                return False
            else:
                token = {'Authorization': 'Bearer ' + response['data']['access_token']}
                # 把token存到config文件
                configs.set('headers', 'token',json.dumps(token))
                # 修改配置文件
                logger.info('token更新到config文件中')
                configs.write(open(path + '\config.ini', 'w', encoding='utf-8'))
                return token
        except Exception as e:
            logger.error(f'token_update_config执行报错：{e}')
            return False

    # 获取到的token返回给调用方，不会更新config文件
    def tokens(self, user):
        try:
            # 这个是老的登录接口和参数，未更换新的
            url = urls + '/identity/connect/token'
            data = {'grant_type': 'password',
                    'username': user,
                    'password': 'wyh12345',
                    'scope': 'employee_center car_business smart_car_mgts',
                    'client_id': 'bot',
                    'client_secret': 'secret'}
            response = r.request(url, 'post', data)
            if 'error' in response:
                logger.info('账号：{0}，登录报错：{1}'.format(user, response))
                return False
            else:
                token = {'Authorization': 'Bearer ' + response['access_token']}
                logger.info('返回token')
                return token
        except Exception as e:
            logger.error(f'token_update_config执行报错：{e}')
            return False


if __name__ == '__main__':
    print('执行token')
    Headers.token_update_config("wanyuanhao")
