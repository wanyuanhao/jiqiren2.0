# -*- encoding:utf-8 -*-
from config.Headers import Headers
from util.Requests_util import Requests_util
# 循环录入定保信息
# 筛选获取有微信好友的buid
headers = Headers().tokens('jiagou01')
r = Requests_util()
url = 'http://userssodev1.91bihu.me/carbusiness/api/v1/customer/querylist'
data = {"pageIndex": 1, "pageSize": 45, "selectType": 1, "topLabel": "tab_quanbukehu",
        "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isWeChat": 1,
        "isDataLable": "", "dataTag": "", "dataTypeId": 0, "lastMaintainDayRange": "", "isMaintain": 1,
        "isOpenGuanjia": 1}
resutl = r.request(url, 'post', data, headers, 'json')
sum = 0
for buid in resutl['data']:
    id = buid['buid']
    # 录入定保信息
    url1 = 'http://userssodev1.91bihu.me/carbusiness/api/v1/CustomerDetail/SaveMaintainInfo'
    data1 = {"buid": id, "mileage": 1230, "maintainDate": "", "lastMaintainDate": "2020-04-29",
             "maintainRemark": "", "maintainActive": "", "maintainClintLevelRmark": "", "maintainOil": "",
             "maintainCategoryinfo": 0, "maintainDayRemark": "", "purchaseDate": "2017-11-06",
         "maintainCategoryinfoString": ""}
    r.request(url1, 'post', data1, headers, 'json')
    sum+=1
    if sum ==3:
        break

# 轮循给每一条数据添加定保信息
