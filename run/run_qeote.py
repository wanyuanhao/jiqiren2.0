import multiprocessing
from module.customer_management.Interface_quote import Interface_quote
import configparser, os, json
import threading
from Logs.Logs import Logs
import datetime
interface = Interface_quote()
quote = interface.quote
logger = Logs().logger

def licenseNo(license, QuoteSource):
    sum = 0
    if len(license) >= 4:
        s1 = len(license) % 4
        s2 = len(license) // 4
        for i in range(s2):
            logger.info(f'>>>>>>第{i + 1}批执行时间：{datetime.datetime.now()}')
            response1 = interface.xubao(license[sum], 8)
            response2 = interface.xubao(license[sum + 1], 8)
            response3 = interface.xubao(license[sum + 2], 8)
            response4 = interface.xubao(license[sum + 3], 8)
            m1 = threading.Thread(target=quote, args=(response1, headers, QuoteSource))
            m2 = threading.Thread(target=quote, args=(response2, headers, QuoteSource))
            m3 = threading.Thread(target=quote, args=(response3, headers, QuoteSource))
            m4 = threading.Thread(target=quote, args=(response4, headers, QuoteSource))
            m1.start()
            m2.start()
            m3.start()
            m4.start()
            m1.join()
            logger.info(f'>>>>>>第{i + 1}批结束时间：{datetime.datetime.now()}')
            sum += 4
        if s1 == 3:
            response1 = interface.xubao(license[sum], 8)
            response2 = interface.xubao(license[sum + 1], 8)
            response3 = interface.xubao(license[sum + 2], 8)
            m1 = threading.Thread(target=quote, args=(response1, headers, QuoteSource))
            m2 = threading.Thread(target=quote, args=(response2, headers, QuoteSource))
            m3 = threading.Thread(target=quote, args=(response3, headers, QuoteSource))
            m1.start()
            m2.start()
            m3.start()
            m1.join()
            logger.info(f'>>>>>>最后一批结束时间：{datetime.datetime.now()}')
        elif s1 == 2:
            response1 = interface.xubao(license[sum], 8)
            response2 = interface.xubao(license[sum + 1], 8)
            m1 = threading.Thread(target=quote, args=(response1, headers, QuoteSource))
            m2 = threading.Thread(target=quote, args=(response2, headers, QuoteSource))
            m1.start()
            m2.start()
            m1.join()
            logger.info(f'>>>>>>最后一批结束时间：{datetime.datetime.now()}')
        elif s1 == 1:
            response1 = interface.xubao(license[sum], 8)
            m1 = threading.Thread(target=quote, args=(response1, headers, QuoteSource))
            m1.start()
            m1.join()
            logger.info(f'>>>>>>最后一批结束时间：{datetime.datetime.now()}')
        else:
            print('请传入车牌')
    elif len(license) == 3:
        response1 = interface.xubao(license[sum], 8)
        response2 = interface.xubao(license[sum + 1], 8)
        response3 = interface.xubao(license[sum + 2], 8)
        m1 = threading.Thread(target=quote, args=(response1, headers, QuoteSource))
        m2 = threading.Thread(target=quote, args=(response2, headers, QuoteSource))
        m3 = threading.Thread(target=quote, args=(response3, headers, QuoteSource))
        m1.start()
        m2.start()
        m3.start()
        m1.join()
        logger.info(f'>>>>>>最后一批结束时间：{datetime.datetime.now()}')
    elif len(license) == 2:
        response1 = interface.xubao(license[sum], 8)
        response2 = interface.xubao(license[sum + 1], 8)
        m1 = threading.Thread(target=quote, args=(response1, headers, QuoteSource))
        m2 = threading.Thread(target=quote, args=(response2, headers, QuoteSource))
        m1.start()
        m2.start()
        m1.join()
        logger.info(f'>>>>>>最后一批结束时间：{datetime.datetime.now()}')
    elif len(license) == 1:
        response1 = interface.xubao(license[sum], 8)
        m1 = threading.Thread(target=quote, args=(response1, headers, QuoteSource))
        m1.start()
        m1.join()
        logger.info(f'>>>>>>最后一批结束时间：{datetime.datetime.now()}')
    else:
        print('请传入车牌')


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(__file__))
    conf.read(path + '/config/config.ini')
    headers = json.loads(conf.get('headers', 'token'))
    licenseNo(
        ['苏AW7Q70', '苏AY855N', '苏A1A96M', '苏AW0F08', '苏A8G6Z9', '京FF1234', '京PME088', '辽A3N35X', '苏BD11331', '京JV0107'],
        4)
    print('报价结束')
