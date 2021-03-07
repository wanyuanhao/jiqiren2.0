import requests
from Logs import Logs


class Requests_util:
    def __init__(self):
        self.logger = Logs.Logs().logger

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
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjRFOTAzNEM5NzQ1RDZCNTlBNzgzMzBDQThFRUMwN0RDRTc4NDQ2NTMiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJUcEEweVhSZGExbW5nekRLanV3SDNPZUVSbE0ifQ.eyJuYmYiOjE2MTQwNjQ5NTQsImV4cCI6MTYxNTM2MDk1NCwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS45MWJpaHUuY29tIiwiYXVkIjpbImh0dHBzOi8vaWRlbnRpdHkuOTFiaWh1LmNvbS9yZXNvdXJjZXMiLCJjYXJfYnVzaW5lc3MiLCJlbXBsb3llZV9jZW50ZXIiLCJzbWFydF9jYXJfbWd0cyJdLCJjbGllbnRfaWQiOiJib3QiLCJzdWIiOiIxNzEzODMiLCJhdXRoX3RpbWUiOjE2MTQwNjQ5NTQsImlkcCI6ImxvY2FsIiwiZW1wbG95ZWVJZCI6IjE3MTM4MyIsImNvbXBJZCI6IjE3MTM4MyIsInVzZXJOYW1lIjoi5LiH5Zut5rWpIiwidXNlckFjY291bnQiOiJ3YW55dWFuaGFvIiwiRGVwdElkIjoiMjg2OSIsIklzQWRtaW4iOiJUcnVlIiwiUm9sZVR5cGUiOiIzIiwiUm9sZUlkcyI6IjQwMDMzIiwibG9naW5DbGllbnRUeXBlIjoiMiIsImxvZ2luU3RhbXAiOiIxNjE0MDY0OTU1LWQ3ZjZkOWZmLTk0MmQtNGFjZS1iZjViLWM0OGRiOGM3ZDdjOCIsInNjb3BlIjpbImNhcl9idXNpbmVzcyIsImVtcGxveWVlX2NlbnRlciIsInNtYXJ0X2Nhcl9tZ3RzIl0sImFtciI6WyJwd2QiXX0.cRsfL_BhodxV3Fus9sAJ-ZVHzTJJdKtKJ32TMzzAU6IxkorI14Y2RwM4REKzH9enzqdB4ZA_UvYC-G4wk12jcH6jOfpHh6a9zOaRzLYHoj-Iy8TT44Bt1HfDwzzoZAsnUjmnyOuiycvnhtMeB4_6XV_S8klWApnEZHOLJevAp4LpsqXthBgzFvZ8XessixzBqsNbnMQPwYk12b1nbFUTUDaO16nafbQetBGR_0PDLA5A-PqpiSg7U_JLVsBuOoW3jO_l6Wt4vlujUuhlFeskQYUuti-VgGFIxH9kWVQ67MwwpshJ015Xu03zhaO-UssWhgFl_6FlxIjBScj1z9vkRA'}
    r = Requests_util()
    data = {"buid":"601074911"}
    res = r.request('https://bot.91bihu.com/carbusiness/api/v1/CustomerDetail/Detial','get',data,headers)
    print(res)
