# Html解析器
import re
from spider.html_downloader import HtmlDownLoader
from spider.product import Product


class Html_Parser:
    item_pattem = r'<li class="star-item-[1-7]">[\s\S]*?</li>'
    titile = r'<a href="javascript:;">([\s\S]*?)</a>'
    desc = r'<p class="desc">([\s\S]*?)</p>'
    price = r'<p class="price">([\s\S]*?)</p>'

    def parser(self, html):
        items = re.findall(self.item_pattem, html)
        result = set()
        for i in items:
            titile = re.findall(self.titile, i)
            desc = re.findall(self.desc, i)
            price = re.findall(self.price, i)
            result.add(Product(titile[0], desc[0], price[0]))
        return result


if __name__ == '__main__':
    down = HtmlDownLoader()
    response = down.downloader('http://127.0.0.1:8848/xiaomi-master/index.html')
    Html_Parser().parser(response)
