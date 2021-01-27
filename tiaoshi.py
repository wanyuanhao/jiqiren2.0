import configparser
import datetime
import os
import unittest
from module.customer_management.CustomerList import CustomerList
import sys
from urllib3 import encode_multipart_formdata
import requests
from requests_toolbelt import MultipartEncoder
from module.customer_management.CustomerList import CustomerList

# 指定文件push
# # 集合
# info = ["a",'b','c','d']
# info = set(info)
# info1 = set([2,22,33,4,55])

# # 取交集
# print(info.intersection(info1))
# print(info & info1)
#
# # 取并集
# print(info.union(info1))
# print(info | info1)

# 差集 去info里面有的 info1里面没有的
# print(info.difference(info1))
# print(info - info1)

# # 子集
# print(info.issubset(info1))
# print(info.isdisjoint(info1))

# 集合添加
# info.add(999)
# # 集合添加多个
# info.update([888,999,9999])
# print(info)

# # 删除
# info.remove(999)
# 随机删除
# info.pop()
# print(info)


# -------------------------
# 枚举
# from enum import Enum
# class Tae(Enum):
#     RED = 1
#     YELLOW = 2
#     GREEN =3
#
# def func(value):
#     if value == Tae.RED or value == Tae.YELLOW:
#         print('禁止同行')
#     else:
#         print('允许同行')
#
# func(2)
# print(Tae.YELLOW)

# ————————————————————————————————————————————
# # 递归删除文件
# def remove_dir(dir):
#     if os.path.isdir(dir):
#         for file in os.listdir(dir):
#             print("递归调用")
#             remove_dir(os.path.join(dir, file))
#         print("删除文件夹：{0}".format(dir))
#         os.rmdir(dir)
#     elif os.path.isfile(dir):
#         print(f'行删除文件：{dir}')
#         os.remove(dir)
#     else:
#         print("不确定的文件类型：{0}".format(dir))
#
# remove_dir(os.getcwd() + '/a1')
# ——————————————————————————————————————————

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

# # --------------------------------------------------------------------------------------------
# # 读取excel
# import xlrd,json
#
# def read_excel(file_path):
#     data = xlrd.open_workbook(file_path)
#     # 打开第一个sheet
#     table = data.sheet_by_index(0)
#     # 读取第一个sheet第一行
#     title = table.row_values(0)
#     # 计算有多少行
#     s = table.nrows
#     print(f"行数是：{s}")
#
#     datas = []
#     # 循环每一行
#     for i in  range(1,s):
#         data_dict = {}
#         # 循环每一列，title为key，y值Value
#         for y  in range(len(title)):
#             # 把值添加到字典中
#             data_dict[title[y]]=table.row_values(i)[y]
#         print(data_dict)
#         # 把每一个字典添加到列表
#         datas.append(data_dict)
#     # 转换列表格式
#     json.dumps(datas,ensure_ascii=True)
#     print(datas)
#
# read_excel('./ttt.xlsx')
# -----------------------------------------------------------------------------

# a = [i for i in range(1, 33)]
# b = []
# c = []
# d = []
# s = [b, c, d]
#
# def avg(name,data):
#     sum = 0
#     n = 0
#     for i in data:
#         result = len(data) // len(name)
#         yu = len(data) % len(name)
#         if len(data) > len(name):
#             name[n].append(i)
#             sum += 1
#             if sum % result == 0:
#                 n += 1
#                 if n == len(name):
#                     m =0
#                     for y in data[-yu:]:
#                         name[m].append(y)
#                         m+=1
#                     break
#         else:
#             name = "数据量小于分配人员"
#     return name
#
# result = avg(s,a)
# print(result)

import unittest

class Test(unittest.TestCase):

    def test01(self):
        print("1")
    def test02(self):
        print("2")
    def test03(self):
        print("3")
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Test("test03"))
    runner = unittest.TextTestRunner()
    runner.run(suite)