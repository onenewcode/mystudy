import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


host_server = 'smtp.qq.com'  #qq邮箱smtp服务器
sender_qq = 'lovestudy@qq.com' #发件人邮箱
pwd = 'bfuqoamxsryhdecf' #邮箱的授权码
receiver = 'lovestudy@qq.com' # 接受者
mail_title = 'Python自动发送html格式的邮件' #邮件标题

#邮件正文内容
mail_content = "您好，<p>这是使用python登录QQ邮箱发送HTNL格式邮件的测试：</p> <p><a href='https://blog.csdn.net/weixin_44827418?spm=1000.2115.3001.5113'>CSDN个人主页</a></p>"

msg = MIMEMultipart()
msg["Subject"] = Header(mail_title,'utf-8')
msg["From"] = sender_qq
# 设置接收者名字和字符集格式
msg["To"] = Header("测试邮箱","utf-8")
# 设置发送信息内容和内容格式
msg.attach(MIMEText(mail_content,'html'))

try:
    smtp = SMTP_SSL(host_server) # ssl登录连接到邮件服务器
    smtp.set_debuglevel(1) # 0是关闭，1是开启debug
    smtp.ehlo(host_server) # 跟服务器打招呼，告诉它我们准备连接，最好加上这行代码
    smtp.login(sender_qq,pwd)
    smtp.sendmail(sender_qq,receiver,msg.as_string())
    smtp.quit()
    print("邮件发送成功")
except smtplib.SMTPException:
    print("无法发送邮件")

