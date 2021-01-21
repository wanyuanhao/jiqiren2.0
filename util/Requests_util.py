import requests
from config.Logs import Logs


class Requests_util:
    def __init__(self):
        self.logger = Logs().logger

    def request(self, url, method, params=None, headers=None, content_type=None,**kwargs):
        self.logger.info(f"请求参：[{url}{params}{kwargs}]")
        try:
            if method == 'get':
                result = requests.get(url=url, params=params, headers=headers).json()
                return result
            elif method == 'post':
                if content_type == 'json':
                    result = requests.post(url=url, json=params, headers=headers,**kwargs).json()
                    return result
                else:
                    result = requests.post(url=url, data=params, headers=headers,**kwargs).json()
                    return result
        except Exception as e:
            if type(headers) is not dict:
                self.logger.error(f'headers类型错误：{type(headers)}')
                return f'headers类型错误：{type(headers)}'
            self.logger.error(f'request方法执行异常,url：{e}')
            return f'request方法执行异常：{e}'


if __name__ == '__main__':
    print("发起request请求")
