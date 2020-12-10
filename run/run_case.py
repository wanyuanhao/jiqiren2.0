import unittest
import os
import HTMLTestRunner
import sender_mail

def run_test_case():
    path = os.path.dirname(os.path.dirname(__file__))
    result = unittest.defaultTestLoader.discover(path + "/case", pattern="Test_case.py", top_level_dir=None)
    return result


if __name__ == '__main__':
    # wb写入内容，没有文件会创建，有文件会覆盖文件内容
    report_path = open("./test_report/result.html", 'wb')
    # 生成测试报告
    runner = HTMLTestRunner.HTMLTestRunner(stream=report_path, title=u"自动化测试报告", description="执行结果")
    ss = runner.run(run_test_case())
    # 关闭文件，如果不关闭文件后面的程序读取，会是空内容
    report_path.close()

    # 打开测试报告
    path = os.path.dirname(__file__)
    file = open(path+"/test_report/result.html", "rb")
    report = file.read()
    file.close()

    # 发送邮件
    sendmail = sender_mail.SendMail()
    sendmail.send_mail(report)
