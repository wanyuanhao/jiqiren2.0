import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class SendMail:
    @classmethod
    def send_mail(self, report):
        sender = "632604593@qq.com"
        receiver = ["wanyuanhao@91bihu.com", "243004032@qq.com"]
        auth_code = "zbrmlqqlhupobchb"
        subject = "自动化测试报告"
        # 生成html文件内容
        html = MIMEText(report, _subtype="html", _charset="utf-8")
        # 使用MIMEMultipart方法的时候这里可以不写收发件人和主题
        # html["subject"] = subject
        # html["from"] = sender
        # html["to"] = str(receiver)

        # 添加到附件，"base64","gb2312" 是编码
        file = MIMEText(report, "base64", "gb2312")
        file["Content-Type"] = "application/octet-stream"
        file["Content-Disposition"] = 'attachment; filename="result111.html"'

        # 把邮件内容和附件添加进去
        msg = MIMEMultipart()
        msg.attach(html)
        msg.attach(file)
        msg["subject"] = subject
        msg["from"] = sender
        msg["to"] = str(receiver)
        # 链接smtp服务器
        smtp = smtplib.SMTP()
        smtp.connect("smtp.qq.com")
        # 登录邮箱
        smtp.login(sender, auth_code)
        # 发送邮件给多人使用list，单人可以是字符串
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.close()


if __name__ == '__main__':
    sender = SendMail()
    path = os.path.dirname(__file__)
    # 只读模式打开文件
    f = open(path + "/run/test_report/result.html", "rb")
    report = f.read()
    f.close()
    sender.send_mail(report)
