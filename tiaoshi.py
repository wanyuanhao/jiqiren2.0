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
import json, time

conf = configparser.ConfigParser()
conf.read('./config/config.ini', encoding='utf-8')
header = json.loads(conf.get('headers', 'token'))

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


Isquote = {
    "LicenseNo": "苏A8G6Z9",
    "CityCode": 8,
    "EngineNo": "J90805",
    "CarVin": "LFV2A21K8G4043336",
    "RegisterDate": "2016-05-24",
    "MoldName": "大众FV7146BBDBG轿车",
    "MoldNameUrlEncode": "",
    "ForceTax": 0,
    "CustKey": "6FD1DD6DA67D6EC6C78EBA0D4B9B39E9",
    "Agent": 189469,
    "ChildAgent": 189469,
    "SecCode": "6FD1DD6DA67D6EC6C78EBA0D4B9B39E9",
    "CarOwnersName": "徐胜",
    "IdCard": "5130291981******37",
    "OwnerIdCardType": 1,
    "InsuredName": "徐胜",
    "InsuredIdCard": "5130291981******37",
    "InsuredIdType": 1,
    "InsuredMobile": "",
    "HolderIdCard": "5130291981******37",
    "HolderName": "徐胜",
    "BizTimeStamp": "1620576000",
    "VehicleAlias": "大众FV7146BBDBG轿车/大众FV7146BBDBG轿车/1.395/5/0.00/13880",
    "NewBuid": 207365606,
    "BoLi": 0,
    "SheShui": 0,
    "HuaHen": [],
    "SiJi": 50000,
    "ChengKe": 10000,
    "CheSun": 0,
    "SanZhe": 300000,
    "SheBeiSunshi": 0,
    "BjmSheBeiSunshi": 0,
    "HcJingShenSunShi": 0,
    "HcSanFangTeYue": 0,
    "HcXiuLiChang": 0,
    "HcXiuLiChangType": 0,
    "SanZheJieJiaRi": 300000,
    "HcHuoWuZeRen": 0,
    "YongYaoSanZhe": 10000,
    "YongYaoSiJi": 10000,
    "YongYaoChengKe": 10000,
    "JingShenSiJi": 0,
    "JingShenChengKe": 0
}


def Quote(quoteinfo):
    if type(quoteinfo) is dict and len(quoteinfo) > 1:
        city = quoteinfo["CityCode"]
        chesun = quoteinfo['CheSun']
        sanzhe = quoteinfo['SanZhe']
        if city > 0:
            # 车损和三者大于0则发起报价
            if chesun > 0 and sanzhe > 0:
                return '请求成功'
            # 车损和三者小于0，提示选择险种
            elif chesun < 0 and sanzhe < 0:
                return '请选择保价险种'
            # 校验车损险是否投保，
            elif chesun <= 0 and sanzhe > 0:
                huahen = quoteinfo['HuaHen']
                if type(huahen) == int:
                    if huahen == 0:
                        return '请求成功'
                    else:
                        return '投保划痕险，必须投保车损险'
                elif type(huahen) == list:
                    if len(huahen):
                        return '投保划痕险，必须投保车损险'
                    else:
                        return '请求成功'
            else:
                return '暂不支持'


        else:
            return '请选择投保城市'
    else:
        return '请求参数不正确'


# result = Quote(Isquote)
# print(result)
# import json
#
# conf = configparser.ConfigParser()
# conf.read('./config/config.ini', encoding='utf-8')
# to = conf.get('headers', 'token')
# tos = json.loads(to)
# print(type(tos))
from util import Requests_util

r = Requests_util.Requests_util()
quote_body = {
    "buid": 601151202,
    "carInfo": {
        "paAutoModelCode": "",
        "vehicleSource": 0,
        "discountChange": 0,
        "isLoans": 0,
        "licenseNo": "苏AW0F08",
        "licenseType": 0,
        "engineNo": "448900",
        "carVin": "LFV3A23C8F3040080",
        "registerDate": "2015-05-19",
        "vehicleName": "大众FV7187FBDBG轿车/迈腾1.8TSI DSG舒适型/1.798/5/0.0/176800.0/2015",
        "purchasePrice": 176800,
        "seatCount": 5,
        "exhaustScale": 1.798,
        "carType": 1,
        "carUsedType": 1,
        "carTonCount": 0,
        "drivlicenseCartypeValue": "",
        "isTransferCar": 0,
        "transferDate": "0001-01-01",
        "beneFiciary": "",
        "remark": "",
        "modelName": "大众FV7187FBDBG轿车",
        "isNewCar": 2,
        "tonCount": 0,
        "autoMoldCode": "DZAAWD0073",
        "autoMoldCodeSource": "",
        "renewalCarType": 0,
        "vehicleSourcefield": "",
        "specialDiscount": 0,
        "seatUpdated": "",
        "specialOption": "",
        "actualDiscounts": "",
        "vehicleAlias": "大众FV7187FBDBG轿车/迈腾1.8TSI DSG舒适型/1.798/5/0.0/176800",
        "vehicleYear": "",
        "discountJson": "",
        "isPaFloorPrice": 0,
        "sendInsurance": 0,
        "invoiceType": 0,
        "cityCode": 8
    },
    "preRenewalInfo": {
        "relevantPeopleInfo": {
            "holderInfo": {
                "name": "罗虎成",
                "idCard": "422422198001200095",
                "idCardType": 1,
                "mobile": "",
                "address": "",
                "eMail": "",
                "nation": "",
                "authority": "",
                "certiStartDate": "",
                "certiEndDate": "",
                "isTemp": 0,
                "mobileOwner": "",
                "mobileIdCard": ""
            },
            "operator": "",
            "salerInfo": "",
            "insuredInfo": {
                "name": "罗虎成",
                "idCard": "422422198001200095",
                "idCardType": 1,
                "mobile": "",
                "address": "",
                "eMail": "",
                "nation": "",
                "authority": "",
                "certiStartDate": "",
                "certiEndDate": "",
                "isTemp": 0,
                "sameWithHolder": 0,
                "mobileOwner": "",
                "mobileIdCard": ""
            },
            "ownerInfo": {
                "name": "罗虎成",
                "idCard": "422422198001200095",
                "idCardType": 1,
                "isTemp": 0,
                "sameWithHolder": 0
            }
        },
        "xianZhong": {
            "jiaoQiang": {
                "baoE": 0
            },
            "cheSun": {
                "buJiMianBaoFei": 0,
                "buJiMian": 1,
                "depreciationPrice": 0,
                "chesunShow": 101483.2,
                "baoE": 101483.2,
                "baoFei": 1864.08
            },
            "sanZhe": {
                "buJiMian": 1,
                "buJiMianBaoFei": 0,
                "baoE": 1000000,
                "baoFei": 755.5
            },
            "siJi": {
                "buJiMian": 0,
                "buJiMianBaoFei": 0,
                "baoE": 0,
                "baoFei": 0
            },
            "chengKe": {
                "buJiMian": 0,
                "buJiMianBaoFei": 0,
                "baoE": 0,
                "baoFei": 0
            },
            "sheBei": {
                "buJiMian": 0,
                "buJiMianBaoFei": 0,
                "baoE": 0,
                "baoFei": 0
            },
            "huaHen": {
                "buJiMian": 0,
                "buJiMianBaoFei": 0,
                "baoE": 0,
                "baoFei": 0
            },
            "yongYaoSanZhe": {
                "baoE": 0,
                "baoFei": 0
            },
            "yongYaoSiJi": {
                "baoE": 0,
                "baoFei": 0
            },
            "yongYaoChengKe": {
                "baoE": 0,
                "baoFei": 0
            },
            "zengZhiJiuYuan": {
                "baoE": 0,
                "baoFei": 0
            },
            "zengZhiAnJian": {
                "zengZhiAnJianJson": "",
                "baoE": 0,
                "baoFei": 0
            },
            "zengZhiDaiJia": {
                "baoE": 0,
                "baoFei": 0
            },
            "zengZhiSongJian": {
                "zengZhiSongJianJson": "",
                "baoE": 0,
                "baoFei": 0
            },
            "cheLunSunShi": {
                "baoE": 0,
                "baoFei": 0
            },
            "faDongJiSunHuaiChuWai": {
                "baoE": 0,
                "baoFei": 0
            },
            "mianPeiCheSun": {
                "baoE": 0,
                "baoFei": 0
            },
            "mianPeiSanZhe": {
                "baoE": 0,
                "baoFei": 0
            },
            "mianPeiSiJi": {
                "baoE": 0,
                "baoFei": 0
            },
            "mianPeiChengKe": {
                "baoE": 0,
                "baoFei": 0
            },
            "jingShenSanZhe": {
                "baoE": 0,
                "baoFei": 0
            },
            "jingShenSiJi": {
                "baoE": 0,
                "baoFei": 0
            },
            "jingShenChengKe": {
                "baoE": 0,
                "baoFei": 0
            },
            "xiuLiBuChang": {
                "days": 0,
                "xiShu": 0,
                "baoE": 0,
                "baoFei": 0
            },
            "sanZheJieJiaRi": {
                "baoE": 0,
                "baoFei": 0
            }
        }
    },
    "quoteInfo": {
        "bizStartDateTime": "2021/05/05 00:00:00",
        "forceStartDateTime": "2021/05/05 00:00:00",
        "selectBF": 1,
        "quoteSource": [
            4
        ],
        "submitSource": [

        ],
        "cityCode": 8,
        "quotePlan": 0
    },
    "sheBeis": [

    ],
    "jiaYi": "",
    "isSumbit": 0,
    "isZongGai": 1,
    "isPaFloorPrice": 0,
    "tempRequestInfo": {
        "discountChangeInfo": {

        }
    },
    "multiChannels": [
        {
            "channelId": 42993,
            "source": 4,
            "channelName": "万园浩-人保车险-胡甜甜-人保车险-智能",
            "discountChange": 0
        }
    ]
}

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


# 多线程
import threading


def func(a):
    print("1", a)
    time.sleep(5)
    print(a)


thread = threading.Thread


# thread(target=func('aa')).start()
# thread(target=func('bb')).start()
# print(threading.current_thread())

class MYThearding(threading.Thread):
    sum = 0
    locks = threading.Lock()

    def run(self):
        sum2 = 0
        with MYThearding.locks:
            for i in range(1000000):
                MYThearding.sum += 1
                sum2 += 1
        print(MYThearding.sum)
        print(sum2)


# thread1 = MYThearding()
# thread2 = MYThearding()
# thread3 = MYThearding()
#
# thread1.start()
# thread2.start()
# time.sleep(5)
# thread3.start()
#
# thread1.join()
# thread2.join()

import multiprocessing  # 导入进程模块
import datetime
import time


def function(data,name):
    with  MYThearding.locks:
        sum = data + 100
        print(sum,name)
        time.sleep(5)
        print('over')
        return datetime.datetime.now()


if __name__ == '__main__':
    p = multiprocessing.Process(target=function, args=(123,'哈哈'))  # 创建一个进程，args传参 必须是元组
    time.sleep(3)
    s1 = p.start()  # 运行线程p
    p1 = multiprocessing.Process(target=function, args=(23,'呵呵'))  # 创建一个进程，args传参 必须是元组
    time.sleep(2)
    s2 = p1.start()  # 运行线程p

