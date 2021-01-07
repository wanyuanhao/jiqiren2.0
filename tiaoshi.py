import configparser
import datetime
import os
import unittest
from module.kehuguanli.CustomerList import CustomerList
import sys
from urllib3 import encode_multipart_formdata
import requests
from requests_toolbelt import MultipartEncoder
from module.kehuguanli.CustomerList import CustomerList

s = {"data": {"pageIndex": 1, "pageSize": 15, "totalCount": 97, "dataList": [
    {"id": 401334, "fileName": "批续模板1.1.xlsx", "isCompleted": 0, "isAgainRenewal": 0,
     "createTime": "2021-01-07 14:28:59", "totalCount": 0, "errorDataCount": 0, "uploadTotalCount": 0,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/7/171383/93ebda87f0484356be519cf381cd754f.xlsx",
     "progress": 0.0, "businessType": 0},
    {"id": 401332, "fileName": "sz-15-17-1-12-13(1).xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2021-01-06 21:13:40", "totalCount": 1995, "errorDataCount": 5, "uploadTotalCount": 2000,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/6/171383/ecb2978dfa76463a9c6780d94c27844b.xlsx",
     "progress": 0.0, "businessType": 0},
    {"id": 401328, "fileName": "定保模板 (1).xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2021-01-06 13:47:38", "totalCount": 25, "errorDataCount": 0, "uploadTotalCount": 25,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/6/171383/6e5b2db43c86452e846f6d6c48cabac5.xlsx",
     "progress": 0.0, "businessType": 1},
    {"id": 401327, "fileName": "批续模板1.1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2021-01-06 13:45:42", "totalCount": 23, "errorDataCount": 0, "uploadTotalCount": 23,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/6/171383/b706edfdf14841d8aa071c7586eb8a03.xlsx",
     "progress": 0.0, "businessType": 0},
    {"id": 401324, "fileName": "批续模板1.1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2021-01-06 10:28:18", "totalCount": 35, "errorDataCount": 0, "uploadTotalCount": 35,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/6/171383/6ad963cc92fa4d109d32152b94d767ab.xlsx",
     "progress": 0.0, "businessType": 0},
    {"id": 401322, "fileName": "批续模板1.1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2021-01-06 10:26:48", "totalCount": 6, "errorDataCount": 0, "uploadTotalCount": 6,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/6/171383/8fd099a2dd154a8f867eadcfd317ec9a.xlsx",
     "progress": 0.0, "businessType": 0},
    {"id": 401321, "fileName": "批续模板1.1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2021-01-06 10:26:17", "totalCount": 1, "errorDataCount": 0, "uploadTotalCount": 1,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/6/171383/83c67bb0547c4a18899d3f988dd158af.xlsx",
     "progress": 0.0, "businessType": 0},
    {"id": 401317, "fileName": "批续模板1.1.xlsx", "isCompleted": 1, "isAgainRenewal": 1,
     "createTime": "2021-01-06 10:17:55", "totalCount": 1, "errorDataCount": 0, "uploadTotalCount": 1,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 1, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "2021-01-06 10:18:02", "isDistributed": False, "taskStatus": 2,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[1,4],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 0, "filePath": "BatchRenewal/2021/1/6/171383/f91326b56e7748d380091ca5c2595f99.xlsx",
     "progress": 100.0, "businessType": 0},
    {"id": 401316, "fileName": "批续模板1.1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2021-01-06 10:17:11", "totalCount": 1, "errorDataCount": 0, "uploadTotalCount": 1,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 171383,
     "userName": "万园浩", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2021/1/6/171383/07f05b88ae6940128fc94eab2314b115.xlsx",
     "progress": 0.0, "businessType": 0},
    {"id": 401303, "fileName": "123.xlsx", "isCompleted": 1, "isAgainRenewal": 0, "createTime": "2020-12-28 11:03:07",
     "totalCount": 142, "errorDataCount": 8, "uploadTotalCount": 150, "successfullCount": 0, "partSuccessedCount": 0,
     "failedCount": 0, "untreatedCount": 0, "employeeId": 421967, "userName": "葛经理",
     "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0, "cityId": 18,
     "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}", "batchRenewalType": 1,
     "filePath": "BatchRenewal/2020/12/28/171383/421967/b2722c7b206a41f7a3357c137ca6a38b.xlsx", "progress": 0.0,
     "businessType": 1}, {"id": 401302, "fileName": "定保模板2020.12.2-修复1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
                          "createTime": "2020-12-28 11:02:29", "totalCount": 137, "errorDataCount": 2,
                          "uploadTotalCount": 139, "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0,
                          "untreatedCount": 0, "employeeId": 421967, "userName": "葛经理",
                          "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
                          "cityId": 18,
                          "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
                          "batchRenewalType": 1,
                          "filePath": "BatchRenewal/2020/12/28/171383/421967/f871b875e12746169639e8f296cd6540.xlsx",
                          "progress": 0.0, "businessType": 1},
    {"id": 401301, "fileName": "定保模板2020.12.2-修复1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2020-12-28 11:01:42", "totalCount": 137, "errorDataCount": 2, "uploadTotalCount": 139,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 421967,
     "userName": "葛经理", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2020/12/28/171383/421967/eb73ab97c4e048d2911b43d0aa2a67e7.xlsx",
     "progress": 0.0, "businessType": 1},
    {"id": 401300, "fileName": "定保模板2020.12.2-修复1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2020-12-28 11:01:27", "totalCount": 137, "errorDataCount": 2, "uploadTotalCount": 139,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 421967,
     "userName": "葛经理", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2020/12/28/171383/421967/c7922e5a58e94453926b29d75300a8a7.xlsx",
     "progress": 0.0, "businessType": 1},
    {"id": 401298, "fileName": "定保模板2020.12.2-修复1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2020-12-28 10:58:11", "totalCount": 137, "errorDataCount": 2, "uploadTotalCount": 139,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 421967,
     "userName": "葛经理", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2020/12/28/171383/421967/1802c4bbdc1f44febe1cc7754546e2ff.xlsx",
     "progress": 0.0, "businessType": 1},
    {"id": 401297, "fileName": "定保模板2020.12.2-修复1.xlsx", "isCompleted": 1, "isAgainRenewal": 0,
     "createTime": "2020-12-28 10:54:15", "totalCount": 137, "errorDataCount": 2, "uploadTotalCount": 139,
     "successfullCount": 0, "partSuccessedCount": 0, "failedCount": 0, "untreatedCount": 0, "employeeId": 421967,
     "userName": "葛经理", "startExecuteTime": "0001-01-01 00:00:00", "isDistributed": False, "taskStatus": 0,
     "cityId": 18, "channelPattern": "{\"ChannelType\":2,\"SelectedSources\":[],\"IsHistoryRenewal\":0}",
     "batchRenewalType": 1, "filePath": "BatchRenewal/2020/12/28/171383/421967/0857878ad2ba43108f789262db5f3539.xlsx",
     "progress": 0.0, "businessType": 1}]}, "code": 1, "message": "成功"}
upload_id = s['data']['dataList'][0]['id']
print(upload_id)


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

# s = [4,3,7,1]
# print(sorted(s,reverse=True))
