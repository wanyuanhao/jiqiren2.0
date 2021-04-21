import unittest
import os
import HTMLTestRunner
import sender_mail
import datetime
from config.headers import Headers
from logs import logs


def run_test_case():
    path = os.path.dirname(os.path.dirname(__file__))
    result = unittest.defaultTestLoader.discover(path + "/case", pattern="test_case.py", top_level_dir=None)
    return result


def file_dir(path):
    is_file = os.path.isdir(path)
    if is_file:
        pass
    else:
        os.mkdir(path)


if __name__ == '__main__':
    logger = logs.Logs('run_case').logger
    logger.info('登录账户获取touken')
    Headers.token_update_config('wanyuanhao')
    times = datetime.datetime.now()
    time = times.strftime('%Y-%m-%d')
    # wb写入内容，没有文件会创建，有文件会覆盖文件内容
    path = os.path.dirname(__file__)
    file_dir(path + "./test_report")
    report_path = open(f"./test_report/{time}result.html", 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=report_path, title=u"自动化测试报告(详情请看附件)", description="执行结果",
                                           verbosity=2)
    ss = runner.run(run_test_case())
    # 关闭报告
    report_path.close()

    # 打开测试报告

    file = open(path + f"/test_report/{time}result.html", "rb")
    report = file.read()
    file.close()

    # 邮件中添加日志文件
    log_path = os.path.dirname(__file__)
    log_file = open(f"../logs/log_info/{times.strftime('%Y-%m-%d_%H')}.log", "rb")
    log_report = log_file.read()
    log_file.close()

    # 发送邮件
    logger.info('发送邮件')
    sendmail = sender_mail.SendMail()
    sendmail.send_mail(report, log_report)
