import os
import unittest
import HTMLTestRunner
import datetime
import smtplib
from email.mime.text import MIMEText
def gzkb_all_case():
    case_path = os.path.join(os.getcwd(), '..\module\gongzuokanban')
    result = unittest.defaultTestLoader.discover(case_path, pattern='gongzuokanban_request.py', top_level_dir=None)
    return result


if __name__ == '__main__':
    # run = unittest.TextTestRunner(verbosity=2)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    #测试报告保存路径和名称拼接
    path = open("./test_report/"+time+'result.html','wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=path,title=u'机器人测试报告',description=u"测试结果")
    runner.run(gzkb_all_case())
#---------------------------------------------------------------
    #发件人
    sender = "632604593@qq.com"
    #收件人
    receiver = "wanyuanhao@91bihu.com"
    #授权码
    auth_code = "zbrmlqqlhupobchb"
    #主题名称
    subject = "自动化测试报告"
    msg = MIMEText("<html><h2>工作看板</h2></html>",_subtype="html",_charset="utf-8")
    msg["subject"] = subject
    msg["from"] = sender
    msg["to"] = receiver
    #获取smtplib对象
    smtp = smtplib.SMTP()
    #发件邮箱的服务器地址
    smtp.connect("smtp.qq.com")
    #登录邮箱
    smtp.login(sender,auth_code)
    #发送邮件
    smtp.sendmail(sender,receiver,msg.as_string())
    #关闭邮件
    smtp.quit()

