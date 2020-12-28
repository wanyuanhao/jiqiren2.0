import requests


# HTML下载器
class HtmlDownLoader:
    def downloader(self, url):
        # 获取响应结果，转换成文本
        response = requests.get(url).content.decode('utf-8')

        return response


if __name__ == '__main__':
    html = HtmlDownLoader()
    resutl = html.downloader('http://127.0.0.1:8848/xiaomi-master/index.html')
