# author wan
# -*- coding:utf-8 -*-
import configparser
import os,json
import datetime
from util.Requests_util import Requests_util


class WorkPanel:
    def __init__(self):
        conf = configparser.ConfigParser()
        path = os.path.dirname(__file__) + '../../../config/config.ini'
        conf.read(path, encoding='utf-8')
        self.url = conf.get('host', 'url')
        self.r = Requests_util()
        self.headers = json.loads(conf.get('headers', 'token'))

    def today_personnel_work(self, compid, headers, employeeid=None):
        '获取人员当日人员效能统计结果'
        url = self.url + '/stats/api/v1/Panel/EmpEffectTotalNew'
        if employeeid == None:
            employeeid = compid
        today_time = datetime.datetime.now().strftime('%Y-%m-%d')
        data = {"deptId": [], "categoryinfoId": [], "searchEmployeeId": [],
                "dataRangeTime": [f"{today_time} 00:00:00", f"{today_time} 23:59:59"], "pageIndex": 1, "pageSize": 50,
                "total": 1, "compId": compid, "employeeId": employeeid}
        result = self.r.request(url, 'post', data, headers, 'json')
        return result


if __name__ == '__main__':
    w = WorkPanel()
    rs = w.today_personnel_work('171383', w.headers)
    print(rs)
