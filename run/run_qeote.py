import multiprocessing
from module.customer_management.Interface_quote import Interface_quote
import configparser, os, json

if __name__ == '__main__':
    conf = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(__file__))
    print(path)
    conf.read(path + '/config/config.ini')
    headers = json.loads(conf.get('headers', 'token'))
    interface = Interface_quote()
    quote = interface.quote
    def quotes(license,header):
        for i in license:
            response1 =interface.xubao(i, 8)
            quote(response1,header,4)

    quotes(
        ['苏AW7Q70', '苏AY855N', '苏A1A96M', '苏AW0F08', '苏A8G6Z9', '京FF1234', '京PME088', '辽A3N35X', '苏BD11331', '京JV0107'],headers)

    #
    # def licenseNo(license):
    #     sum = 0
    #     if len(license) >= 4:
    #         s1 = len(license) % 4
    #         s2 = len(license) // 4
    #         for i in range(s2):
    #             response1 =interface.xubao(license[sum], 8)
    #             response2 =interface.xubao(license[sum+1], 8)
    #             response3 =interface.xubao(license[sum+2], 8)
    #             response4 =interface.xubao(license[sum+3], 8)
    #             m1 = multiprocessing.Process(target=quote, args=(response1, headers))
    #             m2 = multiprocessing.Process(target=quote, args=(response2, headers))
    #             m3 = multiprocessing.Process(target=quote, args=(response3, headers))
    #             m4 = multiprocessing.Process(target=quote, args=(response4, headers))
    #             m1.start()
    #             m2.start()
    #             m3.start()
    #             m4.start()
    #             sum += 4
    #         if s1 == 3:
    #             response1 =interface.xubao(license[sum], 8)
    #             response2 =interface.xubao(license[sum+1], 8)
    #             response3 =interface.xubao(license[sum+2], 8)
    #             m1 = multiprocessing.Process(target=quote, args=(response1, headers))
    #             m2 = multiprocessing.Process(target=quote, args=(response2, headers))
    #             m3 = multiprocessing.Process(target=quote, args=(response3, headers))
    #             m1.start()
    #             m2.start()
    #             m3.start()
    #         elif s1 == 2:
    #             response1 =interface.xubao(license[sum], 8)
    #             response2 =interface.xubao(license[sum+1], 8)
    #             m1 = multiprocessing.Process(target=quote, args=(response1, headers))
    #             m2 = multiprocessing.Process(target=quote, args=(response2, headers))
    #             m1.start()
    #             m2.start()
    #         elif s1 == 1:
    #             response1 =interface.xubao(license[sum], 8)
    #             m1 = multiprocessing.Process(target=quote, args=(response1, headers))
    #             m1.start()
    #         else:
    #             pass
    #     elif len(license) == 3:
    #         response1 =interface.xubao(license[sum], 8)
    #         response2 =interface.xubao(license[sum+1], 8)
    #         response3 =interface.xubao(license[sum+2], 8)
    #         m1 = multiprocessing.Process(target=quote, args=(response1, headers))
    #         m2 = multiprocessing.Process(target=quote, args=(response2, headers))
    #         m3 = multiprocessing.Process(target=quote, args=(response3, headers))
    #         m1.start()
    #         m2.start()
    #         m3.start()
    #     elif len(license) == 2:
    #         response1 =interface.xubao(license[sum], 8)
    #         response2 =interface.xubao(license[sum+1], 8)
    #         m1 = multiprocessing.Process(target=quote, args=(response1, headers))
    #         m2 = multiprocessing.Process(target=quote, args=(response2, headers))
    #         m1.start()
    #         m2.start()
    #     elif len(license) == 1:
    #         response1 =interface.xubao(license[sum], 8)
    #         m1 = multiprocessing.Process(target=quote, args=(response1, headers))
    #         m1.start()
    #     else:
    #         print('请传入车牌')
    #
    #
    # licenseNo(
    #     ['苏AW7Q70', '苏AY855N', '苏A1A96M', '苏AW0F08', '苏A8G6Z9', '京FF1234', '京PME088', '辽A3N35X', '苏BD11331', '京JV0107'])
