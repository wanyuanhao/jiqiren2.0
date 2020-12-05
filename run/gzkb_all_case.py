import os
import unittest
import HTMLTestRunner
import datetime
import sender_mail
def gzkb_all_case():
    case_path = os.path.join(os.getcwd(), '..\module\gongzuokanban')
    result = unittest.defaultTestLoader.discover(case_path, pattern='gongzuokanban_request.py', top_level_dir=None)
    return result


if __name__ == '__main__':
    print('开始执行')
    # run = unittest.TextTestRunner(verbosity=2)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H")
    #测试报告保存路径和名称拼接
    paths = "./test_report/"+time+'result.html'
    path = open("./test_report/"+time+'result.html','wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=path,title=u'机器人测试报告',description=u"测试结果")
    runner.run(gzkb_all_case())
    path.close()
    report = open(paths,'rb')
    reports = report.read()
    report.close()
    sender_mail.SendMail.send_mail(reports)



