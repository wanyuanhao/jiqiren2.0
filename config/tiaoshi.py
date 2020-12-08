import configparser
import os
import time
from selenium import webdriver

s = (lambda b:b**2) (8)
print(s)
# driver = webdriver.Chrome()
#
# conf = configparser.ConfigParser()
# '''读取配置文件'''
# root_path = os.path.dirname(__file__)
# conf.read(root_path + '\config.ini', encoding='utf-8')  # 文件路径
# name = conf.get("baojia", "city")
# url = conf.get('host', 'url')
# '''修改配置文件'''
# conf.set("mysql", "host", "1133")
# conf.write(open(root_path + '\config\config.ini', 'w', encoding='utf-8'))
#
# print([i for i in range(1, 9)])
# s = [1, 2.3, 8, 6, 25.85, 5, 3, 2, 1, 9, 8]
# w = 0
# r = []
# # 需求，每次传3条数据，然后停3秒
# # 判断总数是否能整除3
# if len(s) % 3 == 0:
#     # 遍历列表
#     for i in s:
#         w += 1
#         r.append(i)
#         # 每循环三次输入一次，然后停3秒
#         if w % 3 == 0:
#             print(r[-3:])
#             time.sleep(3)
# elif len(s) % 3 == 1:
#     # 计算列表总数
#     ss = len(s)
#     for ii in s:
#         w += 1
#         r.append(ii)
#         if w % 3 == 0:
#             print(r[-3:])
#             time.sleep(3)
#         # 循环完，输入最后一个
#         elif w == ss:
#             print(r[-1:])
#
# elif len(s) % 3 == 2:
#     sa = len(s)
#     for ai in s:
#         w += 1
#         r.append(ai)
#         if w % 3 == 0:
#             print(r[-3:])
#             time.sleep(3)
#         elif w == sa:
#             print(r[-2:])

# ------------------------------------------------------------------------

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
#
# class SendMail:
#     def send_mail(self, report, smtps):
#         sender = "632604593@qq.com"
#         receiver = "wanyuanhao@91bihu.com"
#         auth_code = "zbrmlqqlhupobchb"
#         subject = "自动化测试报告"
#         html = MIMEText(report, _subtype="html", _charset="utf-8")
#         html["subject"] = subject
#         html["from"] = sender
#         html["to"] = receiver
#         smtp = smtplib.SMTP()
#         smtp.connect(smtps)
#         smtp.login(sender, auth_code)
#         smtp.sendmail(sender, receiver, html.as_string())
#         smtp.quit()
#
#     def send_mail_file(self, report, smtps):
#         sender = "632604593@qq.com"
#         receiver = "wanyuanhao@91bihu.com"
#         auth_code = "zbrmlqqlhupobchb"
#         subject = "自动化测试报告"
#         html = MIMEText(report, _subtype="html", _charset="utf-8")
#
#         file = MIMEText(report, _subtype="base64", _charset="gb2312")
#         file["Content-Type"] = "application/octet-stream"
#         file["Content-Disposition"] = 'attachment; filename="result111.html"'
#
#         msg = MIMEMultipart()
#         msg.attach(html)
#         msg.attach(file)
#         msg["subject"] = subject
#         msg["from"] = sender
#         msg["to"] = receiver
#
#         smtp = smtplib.SMTP()
#         smtp.connect(smtps)
#         smtp.login(sender, auth_code)
#         smtp.sendmail(sender, receiver, msg.as_string())
#         smtp.quit()
#
#
# if __name__ == '__main__':
#     sm = SendMail()
#     sm.send_mail_file("<html><h2>测试结果</h2></html>", "smtp.qq.com")

# import xlrd,json
#
# def read_excel(file_path):
#     data = xlrd.open_workbook(file_path)
#     table = data.sheet_by_index(0)
#     title = table.row_values(0)
#
#     s = table.nrows
#     print(f"数字是：{s}")
#
#     datas = []
#     for i in  range(1,s):
#         data_dict = {}
#         for y  in range(len(title)):
#             data_dict[title[y]]=table.row_values(i)[y]
#         print(data_dict)
#         datas.append(data_dict)
#     json.dumps(datas,ensure_ascii=True)
#     print(datas)
# read_excel('./ttt.xlsx')


# s = [4,3,7,1]
# print(sorted(s,reverse=True))
def time_count(func):
    def my_func():
        action = time.time()
        func()
        time.sleep(1)
        over = time.time()
        result = over - action
        print(result)
    return my_func

@time_count
def s():
    print("demo")
s()
