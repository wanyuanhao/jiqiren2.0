# -*-coding:utf-8
from util.requests_util import RequestsUtil
import configparser, os, json, time, datetime
from logs import logs
from util.mysql_db import MYdb
import threading
import xlwt


class InterfaceQuote:
    lock = threading.Lock()

    def __init__(self):
        config = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        config.read(path + '\..\..\config\config.ini', encoding='utf-8')
        self.logger = logs.Logs().logger
        self.r = RequestsUtil()
        self.urls = config.get('host', 'url')
        self.headers = json.loads(config.get('headers', 'token'))
        self.Mydb = MYdb()

    def xubao(self, licenseno, city):
        try:
            url = self.urls + '/carbusiness/api/v1/Renewal/RenewalCheck'
            data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                    "sixDigitsAfterIdCard": "", "renewalType": 4}
            # 发起续保请求
            self.logger.info(f'{licenseno}发起续保')
            response = self.r.request(url, 'post', data, headers=self.headers, content_type='json')
            if response['code'] == 1:
                url = self.urls + '/carbusiness/api/v1/Renewal/SubmitRenewalAsync'
                data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                        "sixDigitsAfterIdCard": "", "renewalType": 4, "buid": 0}
                # 获取续保响应结果
                self.logger.info(f'{licenseno}获取续保响应结果')
                response = self.r.request(url, 'post', data, headers=self.headers, content_type='json')
                if response['code'] == 1:
                    self.logger.info(f'{licenseno}新增成功，返回结果：{[True, response, city]}')
                    return [True, response, city]
                else:
                    self.logger.info(f'{licenseno}获取续保结果异常：{response}')
                    return [False]
            elif response['code'] == 2:
                url = self.urls + '/carbusiness/api/v1/Renewal/SubmitRenewalAsync'
                data = {"licenseNo": licenseno, "cityCode": city, "renewalSource": "", "carType": 1, "typeId": 1,
                        "sixDigitsAfterIdCard": "", "renewalType": 4, "buid": 0}
                self.logger.info(f'{licenseno}获取续保响应结果')
                response = self.r.request(url, 'post', data, headers=self.headers, content_type='json')
                if response['code'] == 1:
                    self.logger.info(f'{licenseno}新增成功，返回结果：{[True, response, city]}')
                    return [True, response, city]
                else:
                    self.logger.info(f'{licenseno}获取续保结果异常：{response}')
                    return [False]
            else:
                self.logger.info(f'{licenseno}获取续保结果异常：{response}')
                return [False]
        except Exception as e:
            self.logger.error(f'{licenseno}续保执行异常：{e}')
            return [False]

    def quote(self, licenseNo, header, quote_source, city):
        try:
            self.logger.info(f'执行报价方法，传入参数：{licenseNo, header, quote_source, city}')
            # 调用续保
            self.logger.info(f'{licenseNo}调用续保方法')
            xubaoResponse = self.xubao(licenseNo, city)
            # 校验续保结果是不是True
            if xubaoResponse[0]:
                # 续保城市
                city = xubaoResponse[2]
                # 续保响应信息
                res = xubaoResponse[1]
                url = self.urls + '/carbusiness/api/v1/Renewal/GetRenewalInfo'
                buid = res['data']['buid']
                data = {"buid": f'{buid}', "renewalDay": 90}
                # 获取续保结果
                self.logger.info(f'休眠20秒获取【{licenseNo}】续保信息')
                time.sleep(20)
                response = self.r.request(url, 'post', data, header, 'json')
                if response['message'] == '续保成功':
                    buid = response['data']["buid"]
                    carvin = response['data']["carInfo"]['carVin']
                    license = response['data']["carInfo"]["licenseNo"]
                    EngineNo = response['data']["carInfo"]["engineNo"]
                    IsNewCar = response['data']["carInfo"]["isNewCar"]
                    carType = response['data']["carInfo"]["carType"]
                    registerDate = response['data']["carInfo"]["registerDate"]
                    modelName = response['data']["carInfo"]["modelName"]
                    vehicleName = response['data']["carInfo"]["vehicleName"]
                    autoMoldCode = response['data']["carInfo"]["autoMoldCode"]
                    purchasePrice = response['data']["carInfo"]["purchasePrice"]
                    seatCount = response['data']["carInfo"]["seatCount"]
                    exhaustScale = response['data']["carInfo"]["exhaustScale"]
                    carUsedType = response['data']["carInfo"]["carUsedType"]
                    transferDate = response['data']["carInfo"]["transferDate"]
                    tonCount = response['data']["carInfo"]["tonCount"]
                    renewalCarType = response['data']["carInfo"]["renewalCarType"]
                    specialDiscount = response['data']["carInfo"]["specialDiscount"]
                    invoiceType = response['data']["carInfo"]["invoiceType"]
                    sendInsurance = response['data']["carInfo"]["sendInsurance"]
                    isPaFloorPrice = response['data']["carInfo"]["isPaFloorPrice"]
                    # 关系人
                    insuredInfoname = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['insuredInfo']['name']
                    insuredInfoidCard = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['insuredInfo'][
                        'idCard']
                    insuredInfoididCardType = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['insuredInfo'][
                        'idCardType']

                    ownerInfoname = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['ownerInfo']['name']
                    ownerInfoidCard = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['ownerInfo']['idCard']
                    ownerInfoidCardType = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['ownerInfo'][
                        'idCardType']

                    holderInfoname = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['holderInfo']['name']
                    holderInfoidCard = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['holderInfo']['idCard']
                    holderInfoididCardType = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['holderInfo'][
                        'idCardType']
                    # 默认关系人
                    sparename = '万园浩'
                    spareidcar = '37152219901014873X'
                    spareidtype = '1'
                    # 如果续保结果里没有完整的关系人信息就用默认设置的关系人
                    if holderInfoname is False and holderInfoidCard is False and holderInfoididCardType is False:
                        holderInfoname = sparename
                        holderInfoidCard = sparename
                        holderInfoididCardType = sparename
                    if insuredInfoname is False and insuredInfoidCard is False and insuredInfoididCardType is False:
                        insuredInfoname = sparename
                        insuredInfoidCard = spareidcar
                        insuredInfoididCardType = spareidtype
                    if ownerInfoname is False and ownerInfoidCard is False and ownerInfoidCardType is False:
                        ownerInfoname = sparename
                        ownerInfoidCard = spareidcar
                        ownerInfoidCardType = spareidtype
                    # 起保时间
                    StartQuoteTime = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(
                        "%Y-%m-%d %H:%M:%S")
                    quote_body = {
                        "buid": buid,
                        "carInfo": {
                            "paAutoModelCode": "",
                            "vehicleSource": 0,
                            "discountChange": 0,
                            "isLoans": 0,
                            "licenseNo": f"{license}",
                            "licenseType": 0,
                            "engineNo": f"{EngineNo}",
                            "carVin": f"{carvin}",
                            "registerDate": f"{registerDate}",
                            "vehicleName": f"{vehicleName}",
                            "purchasePrice": purchasePrice,
                            "seatCount": seatCount,
                            "exhaustScale": exhaustScale,
                            "carType": carType,
                            "carUsedType": carUsedType,
                            "carTonCount": 0,
                            "drivlicenseCartypeValue": "",
                            "isTransferCar": 0,
                            "transferDate": f"{transferDate}",
                            "beneFiciary": "",
                            "remark": "",
                            "modelName": f"{modelName}",
                            "isNewCar": IsNewCar,
                            "tonCount": tonCount,
                            "autoMoldCode": f"{autoMoldCode}",
                            "autoMoldCodeSource": "",
                            "renewalCarType": renewalCarType,
                            "vehicleSourcefield": "",
                            "specialDiscount": specialDiscount,
                            "seatUpdated": "",
                            "specialOption": "",
                            "actualDiscounts": "",
                            "vehicleAlias": f"{vehicleName}",
                            "vehicleYear": "",
                            "discountJson": "",
                            "isPaFloorPrice": isPaFloorPrice,
                            "sendInsurance": sendInsurance,
                            "invoiceType": invoiceType,
                            "cityCode": city
                        },
                        "preRenewalInfo": {
                            "relevantPeopleInfo": {
                                "holderInfo": {
                                    "name": f"{holderInfoname}",
                                    "idCard": f"{holderInfoidCard}",
                                    "idCardType": holderInfoididCardType,
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
                                    "name": f"{insuredInfoname}",
                                    "idCard": f"{insuredInfoidCard}",
                                    "idCardType": insuredInfoididCardType,
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
                                    "name": f"{ownerInfoname}",
                                    "idCard": f"{ownerInfoidCard}",
                                    "idCardType": ownerInfoidCardType,
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
                                    "chesunShow": 1,
                                    "baoE": 1,
                                    "baoFei": 0
                                },
                                "sanZhe": {
                                    "buJiMian": 1,
                                    "buJiMianBaoFei": 0,
                                    "baoE": 1000000,
                                    "baoFei": 0
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
                            "bizStartDateTime": f"{StartQuoteTime}",
                            "forceStartDateTime": f"{StartQuoteTime}",
                            "selectBF": 0,
                            "quoteSource": [
                                quote_source
                            ],
                            "submitSource": [

                            ],
                            "cityCode": city,
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
                                "source": quote_source,
                                "channelName": "万园浩-人保车险-胡甜甜-人保车险-智能",
                                "discountChange": 0
                            }
                        ]
                    }
                    # 发送报价时间
                    if carvin is not None and EngineNo is not None and modelName is not None and carvin != 'None' and EngineNo != 'None' and modelName != 'None':
                        SendQuoteTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        quote_url = 'https://bot.91bihu.com/carbusiness/api/v1/Renewal/SubmitQuote'
                        self.logger.info(f'{license}续保成功，发起报价请求')
                        quote_result = self.r.request(quote_url, 'post', quote_body, header, content_type='json')
                        if quote_result['message'] == '请求发送成功':
                            self.logger.info(f'{license}报价请求通过')
                            self.logger.info(f'休眠60秒获取【{license}】报价结果')
                            time.sleep(60)
                            with InterfaceQuote.lock:
                                self.obtain_quote(buid, licenseNo, SendQuoteTime, header)
                                time.sleep(1)
                        else:
                            self.logger.info(f'{licenseNo}报价请求失败：{quote_result}')
                            return self.quote_parser([False, f'报价请求失败：{quote_result}', licenseNo])
                    else:
                        return self.quote_parser([False, f'车辆信息不全，不能发起报价：{response}', licenseNo])
                else:
                    self.logger.info(f'【{licenseNo}】续保失败，不能发起报价')
                    return self.quote_parser([False, f'【{licenseNo}】续保失败，不能发起报价', licenseNo])
        except Exception as e:
            self.logger.error('报价执行异常', f'{e}')
            return self.quote_parser([False, f'报价执行异常:{e}', licenseNo])

    def quote_parser(self, responses):
        licenseNo = None
        is_pass = False
        is_biz = 0
        is_force = 0
        is_quote_result = ""
        response = responses
        try:
            if responses[0]:
                response = responses[1]
                licenseNo = responses[2]
                is_quote_result = quote_money_result = response['data']["quoteResultInfos"]
                if quote_money_result:
                    is_biz = biz = quote_money_result[0]['bizTotal']
                    is_force = force = quote_money_result[0]['forceTotal']
                    if biz or force:
                        is_pass = True
                else:
                    is_pass = False
                    self.logger.info('quoteResultInfos响应字段为空')

            else:
                response = responses[1]
                licenseNo = responses[2]
                self.logger.info(f'{licenseNo}续保或报价失败：{response}')
        except Exception as e:
            self.logger.error(f"▁▂▃▄▅▆▇█▇▆▅▄▃▂▁quote_parser执行异常：{e}")
            response = f"▁▂▃▄▅▆▇█▇▆▅▄▃▂▁quote_parser执行异常：{e}"
        finally:
            self.update_result(licenseNo, response=response, is_pass=is_pass, biz=is_biz, force=is_force,
                               quote_result=is_quote_result)

    def update_result(self, licenseNo, biz=0, force=0, quote_result=None, is_pass=None, response=None):
        try:
            times = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(
                f"{licenseNo}报价结果插入到数据库:is_pass:{is_pass},biz：{biz},force:{force},quote_result:{quote_result},response:{response}")
            if is_pass:
                sql = f"insert into quote_result(licenseNo,biz_money,force_money,createTime,quote_result,is_pass) values(\"{licenseNo}\",{biz},{force},'{times}',\"{quote_result}\",'{is_pass}')"
                self.Mydb.execute(sql)
            else:
                sql = f"insert into quote_result(licenseNo,biz_money,force_money,createTime,quote_result,is_pass,response) values(\"{licenseNo}\",{biz},{force},'{times}',\"{quote_result}\",'{is_pass}',\"{response}\")"
                self.Mydb.execute(sql)
        except Exception as e:
            self.logger.error(f'执行update_result方法报错,插入内容:{licenseNo}：{e}')
            sql = f"insert into quote_result(licenseNo,response) value(\"{licenseNo}\",\"{e}\")"
            self.Mydb.execute(sql)

    def obtain_quote(self, buid, licenseNo, sendTime, header):
        try:
            url = 'https://bot.91bihu.com/carbusiness/api/v1/Renewal/GetQuote'
            data = {"buid": buid}
            self.logger.info(f'{licenseNo}获取报价结果')
            result = self.r.request(url, 'post', data, headers=header, content_type='json')
            if len(result) > 0:
                self.logger.info(f'{licenseNo}校验报价结果是否返回')
                if result['message'] == '获取成功':
                    sendtimes1 = (datetime.datetime.now() + datetime.timedelta(minutes=3)).strftime(
                        "%Y-%m-%d %H:%M:%S")
                    sendtimes2 = (datetime.datetime.now() + datetime.timedelta(minutes=-3)).strftime(
                        "%Y-%m-%d %H:%M:%S")
                    # 发送报价时间在上下3分钟内，则算本次报价请求
                    self.logger.info(f'校验返回的发送报价时间和获取到的发送报价时间是否在这个区间：{result}')
                    if result['data']['quetoTime'] > sendtimes2 and result['data'][
                        'quetoTime'] < sendtimes1:
                        self.logger.info(f'{licenseNo}报价通过：{result}')
                        return self.quote_parser([True, result, licenseNo])
                    else:
                        self.logger.info(f'等待1分钟后，获取到的请求时间小于请求时间{sendTime}')
                        return self.quote_parser(
                            [False, f'等待1分钟后，获取到的请求时间小于请求时间{sendTime}', licenseNo])

                else:
                    self.logger.info(f'获取报价结果失败:{result}')
                    return self.quote_parser([False, f'获取报价结果失败:{result}', licenseNo])
            else:
                self.logger.info(f'获取报价结果失败:{result}')
                return self.quote_parser([False, f'报价结果响应为空:{result}', licenseNo])
        except Exception as e:
            self.logger.error('obtain_quote执行异常', f'{e}')
            return self.quote_parser([False, f'obtain_quote执行异常:{e}', licenseNo])

    def insert_excel(self, head_name, content_list, report_name, sheet_name):

        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet(sheet_name)
        for x in range(len(head_name)):
            worksheet.write(0, x, label=f"{head_name[x]}")
            workbook.save(f'{report_name}.xls')
        for i in range(len(content_list)):
            content = content_list[i]
            for y in range(len(content)):
                worksheet.write(i + 1, y, label=f"{content[y]}")
                # 保存
                workbook.save(f'{report_name}.xls')

    def insert_dict(self, content, sheet_name, excel_name):
        try:
            workbook = xlwt.Workbook(encoding='utf-8')
            worksheet = workbook.add_sheet(sheet_name)
            if len(content) and type(content) == list:
                tab = content[0]
                if type(tab) is dict:
                    index = 0
                    for y in tab.keys():
                        worksheet.write(0, index, label=f"{y}")
                        index += 1
                        workbook.save(f"{excel_name}.xls")
                # 循环列表
                for i in range(len(content)):
                    value_index = 0
                    if type(content[i]) is dict:
                        # 循环字典
                        for data in content[i].values():
                            if type(data) == type(datetime.datetime.now()):
                                data = datetime.datetime.strftime(data, '%Y-%m-%d')
                            worksheet.write(i + 1, value_index, label=f"{data}")
                            workbook.save(f"{excel_name}.xls")
                            value_index += 1
                    else:
                        return '传入参数必须为字典'

        except Exception as e:
            return f'insert_dict方法执行异常：{e}'


if __name__ == '__main__':
    config = configparser.ConfigParser()
    path = os.path.dirname(__file__)
    config.read(path + '\..\..\config\config.ini', encoding='utf-8')
    header = json.loads(config.get('headers', 'token'))
    i = InterfaceQuote()
    # tab = ["姓名","性别","年龄","入职日期"]
    # data = [["张三", "男", 21,"2012-13-15"], ["李四", "女", 18,"2021-15"], ["女警", "女", 20,"2021.10.15"]]
    # i.update_result('AAAAA',1.2,3.1,z1,True,z1)
    # times = datetime.datetime.now().strftime("%Y-%m-%d_%H")
    # i.insert_excel(tab,data, times, 'shee')
    from util.mysql_db import MYdb

    mydb = MYdb()
    result = mydb.query("select licenseNo,biz_money,createTime from quote_result limit 2")
    # i.insert_dict(result, 'sheet', 'mysqldata')
    print(result)
