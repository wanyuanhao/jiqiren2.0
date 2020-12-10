from util.Requests_util import Requests_util
import configparser
import os

r = Requests_util()
# 找到配置文件路径
path = os.path.dirname(__file__)
# 把读取配置的类包赋值
configs = configparser.ConfigParser()
# 读取配置文件
configs.read(path + '\config.ini', encoding='utf-8')
# 读取配置文件的指定配置
users = configs.get('host', 'user')
urls = configs.get('host','url')
class Headers:
    @classmethod
    def token(self,user):
        try:
            url = urls+'/identity/connect/token'
            data = {'grant_type': 'password',
                    'username': user,
                    'password': '91bihu.com',
                    'scope': 'employee_center car_business smart_car_mgts',
                    'client_id': 'bot',
                    'client_secret': 'secret'}
            response = r.request(url, 'post', data)
            if 'error' in response:
                return '账号：{0}，登录报错：{1}'.format(user,response)
            else:
                token = {'Authorization': 'Bearer ' + response['access_token']}
                # 把token存到config文件
                configs.set('headers', 'token', str(token))
                # 修改配置文件
                configs.write(open(path + '\config.ini', 'w', encoding='utf-8'))
                return token
        except Exception as e:
            return e

    def token_down(self, user):
        try:
            url = urls + '/identity/connect/token'
            data = {'grant_type': 'password',
                    'username': user,
                    'password': '91bihu.com',
                    'scope': 'employee_center car_business smart_car_mgts',
                    'client_id': 'bot',
                    'client_secret': 'secret'}
            response = r.request(url, 'post', data)
            if 'error' in response:
                print('账号：{0}，登录报错：{1}'.format(user, response))
                return False
            else:
                token = {'Authorization': 'Bearer ' + response['access_token']}
                return token
        except Exception as e:
            print(e)
            return False

if __name__ == '__main__':
    print('执行token')
    Headers.token(users)
