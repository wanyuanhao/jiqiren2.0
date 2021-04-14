# -*-coding:utf-8
from util.Requests_util import Requests_util
import configparser, os, json, time, datetime
from Logs import Logs


class Interface_quote:
    def __init__(self):
        config = configparser.ConfigParser()
        path = os.path.dirname(__file__)
        config.read(path + '\..\..\config\config.ini', encoding='utf-8')
        self.logger = Logs.Logs().logger
        self.r = Requests_util()
        self.urls = config.get('host', 'url')
        self.headers = json.loads(config.get('headers', 'token'))

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
                    self.logger.info(f'{licenseno}新增成功')
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
                    self.logger.info(f'{licenseno}新增成功')
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

    def quote(self, xubaoResponse, headers, quote_source):
        try:
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
                response = self.r.request(url, 'post', data, self.headers, 'json')
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

                    holderInfoname = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['holderInfo']['name']
                    holderInfoidCard = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['holderInfo']['idCard']
                    holderInfoididCardType = response['data']["preRenewalInfo"]["relevantPeopleInfo"]['holderInfo'][
                        'idCardType']
                    # 默认关系人
                    sparename = '万园浩'
                    spareidcar = '37152219901014873X'
                    spareidtype = '1'
                    # 如果续保结果里没有完整的关系人信息就用默认设置的关系人
                    if holderInfoname and holderInfoidCard and holderInfoididCardType:
                        sparename = holderInfoname
                        spareidcar = holderInfoidCard
                        spareidtype = holderInfoididCardType
                    elif insuredInfoname and insuredInfoidCard and insuredInfoididCardType:
                        sparename = insuredInfoname
                        spareidcar = insuredInfoname
                        spareidtype = insuredInfoname
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
                                    "name": f"{sparename}",
                                    "idCard": f"{spareidcar}",
                                    "idCardType": spareidtype,
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
                                    "name": f"{sparename}",
                                    "idCard": f"{spareidcar}",
                                    "idCardType": spareidtype,
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
                                    "name": f"{sparename}",
                                    "idCard": f"{spareidcar}",
                                    "idCardType": spareidtype,
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
                                4
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
                    SendQuoteTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    quote_url = 'https://bot.91bihu.com/carbusiness/api/v1/Renewal/SubmitQuote'
                    self.logger.info(f'{license}发起报价请求')
                    quote_result = self.r.request(quote_url, 'post', quote_body, headers, content_type='json')

                    if quote_result['message'] == '请求发送成功':
                        self.logger.info(f'{license}报价请求通过')
                        time.sleep(60)
                        url = 'https://bot.91bihu.com/carbusiness/api/v1/Renewal/GetQuote'
                        data = {"buid": buid}
                        self.logger.info(f'{license}获取报价结果')
                        result = self.r.request(url, 'post', data, headers=headers, content_type='json')
                        if len(result) > 0:
                            self.logger.info(f'{license}校验报价结果是否返回')
                            if result['message'] == '获取成功':
                                sendtimes1 = (datetime.datetime.now() + datetime.timedelta(minutes=3)).strftime(
                                    "%Y-%m-%d %H:%M:%S")
                                sendtimes2 = (datetime.datetime.now() + datetime.timedelta(minutes=-3)).strftime(
                                    "%Y-%m-%d %H:%M:%S")
                                # 发送报价时间在上下3分钟内，则算本次报价请求
                                self.logger.info(f'校验返回的发送报价时间和获取到的发送报价时间是否在这个区间：{result}')
                                if result['data']['quetoTime'] > sendtimes2 and result['data'][
                                    'quetoTime'] < sendtimes1:
                                    MoneyResult = result['data']['quoteResultInfos']
                                    self.logger.info(f'{license}报价通过：{MoneyResult}')
                                    return [True, MoneyResult]
                                else:
                                    return [False, f'等待1分钟后，获取到的请求时间小于请求时间{SendQuoteTime}']

                            else:
                                return [False, f'获取报价结果失败:{result}']
                        else:
                            return [False, f'获取报价结果失败:{result}']
                    else:
                        return [False, f'报价请求失败：{quote_result}']

                else:
                    return [False, '续保失败，不能发起报价']
        except Exception as e:
            print(e)
            return '报价执行异常', f'{e}'


if __name__ == '__main__':
    config = configparser.ConfigParser()
    path = os.path.dirname(__file__)
    config.read(path + '\..\..\config\config.ini', encoding='utf-8')
    headers = json.loads(config.get('headers', 'token'))
    i = Interface_quote()
    xubao = i.xubao('苏AW0F08', 8)
    print(i.quote(xubao, headers, 4))
