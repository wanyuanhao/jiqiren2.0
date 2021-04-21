import configparser
import datetime
import os
import unittest
from module.customer_management.customer_list import CustomerList
import sys
from urllib3 import encode_multipart_formdata
import requests
from requests_toolbelt import MultipartEncoder
from module.customer_management.customer_list import CustomerList
import json, time

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
# read_excel('./111.xlsx')
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

# import unittest
#
# class Test(unittest.TestCase):
#
#     def test01(self):
#         print("1")
#     def test02(self):
#         print("2")
#     def test03(self):
#         print("3")
# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(Test("test03"))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)

# a=(1,2,3,4,5)
# b =[6,7,8,9]
# c = {'a':'1',"b":"2"}
# d = {"a1","a2","c3"}
# e = "abcd"
# f = [{'a':'1',"b":"2"},{"a1","a2","c3"}]
# g = {'a':[1,2,3],"b":"8"}
# h = {'a':[{'a':'1',"b":"2"}],"b":"2"}
# i = 1
# j = 1.1
# k = True


# result = Quote(Isquote)
# print(result)
# import json
#
# conf = configparser.ConfigParser()
# conf.read('./config/config.ini', encoding='utf-8')
# to = conf.get('headers', 'token')
# tos = json.loads(to)
# print(type(tos))
# quote_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# quote_url = 'https://bot.91bihu.com/carbusiness/api/v1/Renewal/SubmitQuote'
#
# quote_result= r.request(quote_url,'post',quote_body,headers=header,content_type='json')
#
# time.sleep(60)
#
# url = 'https://bot.91bihu.com/carbusiness/api/v1/Renewal/GetQuote'
# data = {"buid":601151202}
# result = r.request(url,'post',data,headers=header,content_type='json')
# print(result['data']['quoteResultInfos'])
#


# import multiprocessing  # 导入进程模块
# import datetime
# import time
#
#
# def function(data,name):
#     for i in range(5):
#         print('func',i)
#         time.sleep(2)
# def pr(Time):
#     for i in range(5):
#         print('pr',i)
#         time.sleep(2)
#     return Time
#
#
#
# if __name__ == '__main__':
#     p = multiprocessing.Process(target=function, args=(123,'哈哈'))  # 创建一个进程，args传参 必须是元组
#     s1 = p.start()  # 运行线程p
#     p1 = multiprocessing.Process(target=function, args=(23,'呵呵'))  # 创建一个进程，args传参 必须是元组
#     s2 = p1.start()  # 运行线程p
#     p.join()
#     print('结束')


# def distribute(seq):
#     if len(seq) >=3:
#         n = len(seq) // 3  # Will work in both Python 2 and 3
#         s = len(seq) % 3
#         lists = [list(x) for x in zip(seq[:n], seq[n:2*n], seq[2*n:3*n])]
#         if s > 0:
#             tail = seq[3*n:]
#             lists.append(tail)
#         return lists
#     else:
#         return seq
#
#
# print(distribute(['a','b','c','d','e','f','g','h','i','j']))
from logs.logs import Logs
# import multiprocessing
# import pre
#
#
# class asd():
#     def __init__(self):
#         print('asd')
#     def a(self):
#         print('a')
#
#
#
# class dda(pre.aa):
#     # def __init__(self):
#     #     print('dda')
#     def a(self,name,age,sex):
#         time.sleep(3)
#         print(name,age,sex)
#     def b(self):
#         multiline = []
#         for i in range(2):
#             self.bb = multiprocessing.Process(target=self.a,args=('哈哈',21,'未知'))
#             self.bb.start()
#             multiline.append(self.bb)
#         for y in multiline:
#              y.join()
#
#
# if __name__ == '__main__':
#     d = dda()
#     d.b()

import xlrd



def read_excel(path,sheetName):
    # 打开文件
    workbook = xlrd.open_workbook(path)
    # 获取所有sheet
    sheet_list = workbook.sheet_names()
    sheet_data = workbook.sheet_by_name(sheetName)
    row_value = sheet_data.row_values(0)
    row = sheet_data.nrows
    col = sheet_data.ncols

    list = []


    for i in range(1,row):
        data = {}
        for y in range(col):
            a =sheet_data.cell(i,y).ctype
            vs = sheet_data.cell_value(i,y)
            print(type(vs),a)
            data[row_value[y]]= vs
        list.append(data)
    print(list)


if __name__ == '__main__':
    path = os.path.dirname(__file__) + '/util/test.xls'
    print(path)
    read_excel(path,'Sheet1')
