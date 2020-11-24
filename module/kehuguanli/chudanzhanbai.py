from util.Requests_util import Requests_util
# from config.Headers import Headers
import datetime
import os,configparser

# Headers().token()
config = configparser.ConfigParser()
path = os.path.join(os.getcwd())
config.read(path+'..\..\..\config\config.ini',encoding='utf-8')
headers = eval(config.get('headers','token'))
urls = config.get('host','url')
r = Requests_util()


# 出单、战败列表查询
class chuzhan_zhanbai:
    # 根据车牌查询是否有出单数据
    def find_chudan(self, licenseno):
        data = {"pageIndex": 1, "pageSize": 15, "LicenseNo": licenseno}
        url = urls+'/carbusiness/api/v1/customer/quotationReceiptList'
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        try:
            response = r.request(url, 'post', data, headers, content_type='json')
            if response['message'] == '成功':
                if len(response['data']) == 0:
                    return '查询结果为空：{0}'.format(response)
                elif response['data'][0]['licenseNo'] == licenseno and time in response['data'][0]['appearTime']:
                    print('出单列表查询通过')
                    return True
                else:
                    return '已出保单查询不通过，校验类型（车牌是否匹配、出单时间是否今天）：{0}'.format(response)
            else:
                print('已出保单查询结果异常：{0}'.format(response))
                return

        except Exception as e:
            return '已出保单查询请求异常：{0}'.format(e)
    def find_zhanbai(self,licenseno):
        data = {"pageIndex":1,"pageSize":15,"LicenseNo":licenseno}
        url = urls+'/carbusiness/api/v1/customer/defeatList'
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        try :
            response = r.request(url,'post',data,headers=headers,content_type='json')
            if response['message'] == '成功':
                if len(response['data']) == 0:
                    return '查询结果为空：{0}'.format(response)
                elif response['data'][0]['licenseNo'] == licenseno and  time in response['data'][0]['actionTime']:
                    print('战败列表查询通过')
                    return True
                else:
                    return '战败查询校验不通过，对比类型（车牌、录入时间是否今天），响应结果：{0}'.format(response)
            else:
                return '响应结果异常：{0}'.format(response)
        except Exception as e:
            print('战败查询异常：{0}'.format(e))

if __name__ == '__main__':
    print('执行出单战败接口')
    run = chuzhan_zhanbai()
    print(run.find_zhanbai('京NJY977'))