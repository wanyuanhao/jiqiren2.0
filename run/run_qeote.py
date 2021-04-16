import multiprocessing
from module.customer_management.Interface_quote import Interface_quote
import configparser, os, json
import threading
from Logs.Logs import Logs
import time


class RunQuote:

    def __init__(self):
        self.interface = Interface_quote()
        self.logger = Logs().logger

    def avg(self, List):
        if len(List) >= 4:
            n = len(List) // 4
            Tail = len(List) % 4
            Lists = [list(i) for i in zip(List[:n], List[n:2 * n], List[2 * n:3 * n], List[3 * n:4 * n])]
            if Tail > 0:
                Lists.append(List[4 * n:])
            return Lists
        else:
            return List

    def quote_multiline(self, Licenses=[], city=1, *, headers, quote_source):
        try:
            # 如果车牌不为空则执行
            self.logger.info(f'报价车牌：{Licenses}')
            if Licenses:
                # 把一个大列表拆分成小列表
                self.logger.info('拆成4个一组的列表')
                list_license = self.avg(Licenses)
                self.logger.info(f'拆分结果：{list_license}')
                str_threads = []
                for i in list_license:
                    if type(i) == list:
                        # 循环续保报价小列表的车牌
                        threads = []
                        for licenseNo in i:
                            self.thread = threading.Thread(target=self.interface.quote,
                                                           args=(licenseNo, headers, quote_source, city))
                            self.thread.start()
                            threads.append(self.thread)
                        # 等待上一轮报价执行结束
                        self.logger.info(f'等待报价进程结束：{i}')
                        for thr in threads:
                            thr.join()
                    else:
                        self.thread = threading.Thread(target=self.interface.quote,
                                                       args=(i, headers, quote_source, city))
                        self.thread.start()
                        str_threads.append(self.thread)
                for thr in str_threads:
                    thr.join()
            else:
                self.logger.info('请传入车牌')
                return '请传入车牌'
        except Exception as e:
            self.logger.error(f'Quote_licenseno执行异常：{e}')
            return f'Quote_licenseno执行异常：{e}'
        finally:
            self.logger.info('报价结束➽➽➽➽➽➽➽')
            return '报价结束➽➽➽➽➽➽➽'

    def quote_one(self, Licenses=[], city=1, *, headers, quote_source):
        for lic in Licenses:
            self.interface.quote(lic, headers, quote_source, city)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(__file__))
    conf.read(path + '/config/config.ini')
    headers = json.loads(conf.get('headers', 'token'))
    MyQuote = RunQuote()
    # licenseNo = ['苏A8VZ66', '苏A9D0V7', '苏AQ917W', '苏ABJ126', '苏AV729T', '苏A199CJ', '苏A29C8T', '苏A2R2J0', '苏A9D0V7']
    licenseNo = ['苏AE8A52', '苏AW456P', '苏AY596L', '苏AY621K', '苏AB5B50', '苏A80Z0L', '苏A1B26Z', '苏A76D0U', '苏A6U28S']
    # 多线程
    # MyQuote.quote_multiline(licenseNo, 8, headers=headers, quote_source=1)
    # 单线程
    MyQuote.quote_one(['苏A8VZ66'], 8, headers=headers, quote_source=1)
