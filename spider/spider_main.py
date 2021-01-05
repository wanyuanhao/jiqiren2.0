from spider.html_downloader import HtmlDownLoader
from spider.data_storage import Datastorage
from spider.html_parser import Html_Parser
from spider.url_manager import Url_mannager

class SpiderMain:
    def __init__(self):
        self.parser = Html_Parser()
        self.downloader = HtmlDownLoader()
        self.datastorage = Datastorage()
        self.url = Url_mannager()

    def start(self):
        # 从url管理器获取url
        url = self.url.url_manager()
        # 将获取到的url使用下载器进行下载
        response = self.downloader.downloader(url)
        # 将下载内容进行解析
        result = self.parser.parser(response)
        # 把解析结果进行存储
        self.datastorage.stoage(result)
if __name__ == '__main__':
    spider = SpiderMain()
    spider.start()
