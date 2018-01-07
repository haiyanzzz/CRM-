import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class Qq(object):
    '''发送邮件'''
    def __init__(self):
        self.email = "2533916647@qq.com"  #自己的邮箱
        self.user = "不冷不热的温柔"  #用户名
        self.pwd = "uwaendbwhypweagi"

    def send(self,subject,body,to,name):
        print(222)
        msg = MIMEText(body, 'plain', 'utf-8')  # 发送内容
        msg['From'] = formataddr([self.user, self.email])  # 发件人
        msg['To'] = formataddr([name,to])  # 收件人
        msg['Subject'] =subject  # 主题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465) # SMTP服务
        print(333333)
        server.login(self.email,self.pwd) # 邮箱用户名和密码
        server.sendmail(self.email, [to, ], msg.as_string()) # 发送者和接收者
        server.quit()
