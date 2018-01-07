#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

class Msg(object):
    def __init__(self):
        pass
    def send(self):
        print("发送成功")

class Email(object):
    '''发送邮件'''
    def __init__(self):
        self.email = "2533916647@126.com"  #自己的邮箱
        self.user = "不冷不热的温柔"  #用户名
        self.pwd = "授权码"

    def send(self,subject,body,to,name):
        msg = MIMEText(body, 'plain', 'utf-8')  # 发送内容
        msg['From'] = formataddr([self.user, self.email])  # 发件人
        msg['To'] = formataddr([name,to])  # 收件人
        msg['Subject'] =subject  # 主题

        server = smtplib.SMTP("smtp.126.com", 25) # SMTP服务
        server.login(self.email,self.pwd) # 邮箱用户名和密码
        server.sendmail(self.email, [to, ], msg.as_string()) # 发送者和接收者
        server.quit()

