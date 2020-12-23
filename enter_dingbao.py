# -*- encoding:utf-8 -*-
from config.Headers import Headers
from util.Requests_util import Requests_util
# 循环录入定保信息
# 筛选获取有微信好友的buid
headers = Headers().tokens('jiagou01')
r = Requests_util()
url = 'http://userssodev1.91bihu.me/carbusiness/api/v1/customer/querylist'
data = {"pageIndex": 1, "pageSize": 30, "selectType": 1, "topLabel": "tab_quanbukehu",
        "orderBy": {"orderByField": "updateTime", "orderByType": "desc"}, "isFllowUp": "", "isWeChat": 1,
        "isDataLable": "", "dataTag": "", "dataTypeId": 0, "lastMaintainDayRange": "", "isMaintain": 1,
        "isOpenGuanjia": 1}
resutl = r.request(url, 'post', data, headers, 'json')
sum = 0
for buid in resutl['data']:
    buids = buid['buid']
    # 系统推荐5种，内容中心三种，自定义三种，共11种
    #系统推荐-保险（2020-05-10）常规（2020-05-20）通用（2020-05-15）易损件（2020-05-25）保养提醒（2020-05-5）
    # 内容 文章（）海报（）视频（）
    # 自定义 文本（）图片（）视频（）
    datetime = ['2020-06-5','2020-06-10','2020-06-15','2020-06-20','2020-06-25','2020-06-28','2020-07-5','2020-07-10','2020-07-15','2020-07-20','2020-07-25']
    # 没请求一次定保保存sum加1
    # 当sum等于11的时候，从0开始循环datetime
    if sum==11:
        sum=0
    url1 = 'http://userssodev1.91bihu.me/carbusiness/api/v1/CustomerDetail/SaveMaintainInfo'
    data1 = {"buid": buids, "mileage": 8000, "maintainDate": "", "lastMaintainDate": datetime[sum],
             "maintainRemark": "", "maintainActive": "", "maintainClintLevelRmark": "", "maintainOil": "",
             "maintainCategoryinfo": 0, "maintainDayRemark": "", "purchaseDate": "2017-11-06",
             "maintainCategoryinfoString": ""}
    print(f'buid:{buids},定保日期：{datetime[sum]}')
    r.request(url1, 'post', data1, headers, 'json')
    sum += 1

# 轮循给每一条数据添加定保信息
