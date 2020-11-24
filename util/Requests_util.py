import requests


class Requests_util:

    def request(self, url, method, params=None, headers=None, content_type=None):
        try:
            if method == 'get':
                result = requests.get(url=url, params=params, headers=headers).json()
                return result
            elif method == 'post':
                if content_type == 'json':
                    result = requests.post(url=url, json=params, headers=headers).json()
                    return result
                else:
                    result = requests.post(url=url, data=params, headers=headers).json()
                    return result
        except Exception as e:
            print(e)
            return


if __name__ == '__main__':
    print("发起request请求")
