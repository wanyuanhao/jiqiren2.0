import multiprocessing
from module.customer_management.Interface_quote import Interface_quote
import configparser, os, json
import threading
from Logs.Logs import Logs


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

    def Quote_licenseno(self, Licenses=[], city=1, *, headers, quote_source):
        try:
            # 如果车牌不为空则执行
            self.logger.info(f'报价车牌：{Licenses}')
            if Licenses:
                # 把一个大列表拆分成小列表
                self.logger.info('拆成4个一组的列表')
                list_license = self.avg(Licenses)
                self.logger.info(f'拆分结果：{list_license}')
                for i in list_license:
                    if type(i) == list:
                        # 循环续保报价小列表的车牌
                        for license in i:
                            response = self.interface.xubao(license, city)
                            self.thread = threading.Thread(target=self.interface.quote,
                                                           args=(response, headers, quote_source))
                            self.thread.start()
                        # 等待上一轮报价执行结束
                        self.logger.info(f'等待报价进程结束：{i}')
                        self.thread.join()
                    else:
                        self.logger.info(f'发起续保：{i}')
                        response = self.interface.xubao(i, city)
                        self.thread = threading.Thread(target=self.interface.quote,
                                                       args=(response, headers, quote_source))
                        self.logger.info(f'发起报价：{i}')
                        self.thread.start()
                    self.thread.join()
                self.logger.info('报价结束➽➽➽➽➽➽➽')
            else:
                self.logger.info('请传入车牌')
                return '请传入车牌'
        except Exception as e:
            self.logger.error(f'Quote_licenseno执行异常：{e}')
            return f'Quote_licenseno执行异常：{e}'


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    path = os.path.dirname(os.path.dirname(__file__))
    conf.read(path + '/config/config.ini')
    headers = json.loads(conf.get('headers', 'token'))
    MyQuote = RunQuote()
    sult = MyQuote.Quote_licenseno(
        ['苏AW7Q70', '苏AY855N', '苏A1A96M', '苏AW0F08', '苏A8G6Z9', '京FF1234', '京PME088', '辽A3N35X', '苏BD11331', '京JV0107'],
        8, headers=headers, quote_source=4)
    print(sult)
