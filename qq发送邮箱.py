import smtplib
from email.mime.text import MIMEText
_user = "2533916647@qq.com"
_pwd  = "uwaendbwhypweagi"   #授权码
_to   = "2533916647@qq.com"

msg = MIMEText('啦啦啦啦。', 'plain', 'utf-8')
msg["Subject"] = "爱自己爱生活，啧啧"
msg["From"]  = _user
msg["To"]    = _to

try:
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(_user, _pwd)
    s.sendmail(_user, _to, msg.as_string())
    s.quit()
    print("Success!")
except smtplib.SMTPException as e:
    print("Falied,%s"%e)
