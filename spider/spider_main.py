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
        url = self.url.url_manager()
        response = self.downloader.downloader(url)
        result = self.parser.parser(response)
        self.datastorage.stoage(result)
if __name__ == '__main__':
    spider = SpiderMain()
    spider.start()
