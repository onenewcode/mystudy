import imaplib
import email
from email.header import decode_header
import os

'''第一部分：收件IMAP4********************************************'''
'''登录邮箱IMAP4=========================================================='''
from_addr = 'lovestudy@qq.com'  # 发件邮箱
password = 'bfuqoamxsryhdecf'  # 邮箱密码(或者客户端授权码)
imap_server = 'imap.qq.com'


try:
    email_server = imaplib.IMAP4_SSL(imap_server, 993)  #邮箱服务器及SSL端口
    print("imap4 服务器连接成功")
except:
    print("imap4 服务器连接失败")
    exit(1)

try:
    email_server.login(from_addr, password)
    print("imap4 账号密码正确，登录成功")

except:
    print("imap4 账号密码不正确，登录失败")
    exit(1)

''' 邮箱中收到的未读邮件的数量=========================================================='''\
# 选择收件箱
email_server.select()


# search方法返回状态和查找得到的含有邮箱编号的字节数组
email_unseen_id_byte= email_server.search(None, 'UNSEEN')[1][0].split() #所有未读邮件的id 格式email_unseen_id_byte [b'5255', b'5256', b'5257']
print('未读邮件一共有：',len(email_unseen_id_byte),'封')


# #得到所有未读邮件标号将byte格式转为为str email_unseen_id ['5255', '5256', '5257', '5258']
email_unseen_id = []
count_byte = 0
for row in email_unseen_id_byte:
    email_unseen_id.append(row.decode('utf-8'))

# '''读取邮件标题，地址========================================================='''
# 通过fetch(index)读取第index封邮件的内容
sub_list = []
addr_list = []
 
# #对每一封邮件进行处理
for a in email_unseen_id:
    # 获取邮件主题和地址信息，byte格式
    typ, email_content = email_server.fetch(f'{a}'.encode(), '(RFC822)')
    mail_text = email_content[0][1]
    # 编码转化
    msg = email.message_from_bytes(mail_text)
    subject = msg['Subject']
    email_from = msg['from']
    subdecode = decode_header(subject)   #[(b'\xc9\xed\xdd\xc8\xcf\xd6\xbb\xd8\xcc\xc2\xeb', 'gb18030')]
    from_decode = decode_header(email_from)  # [(b'"', None), (b'\xd0\xa1\xe3', 'gb18030'), (b'" <3825@qq.com>', None)]
    print(from_decode)
    
    # 遍历邮件中的每一个附件
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        # 下载附件
        filename = part.get_filename()
        if bool(filename):
            filepath = os.path.join("downloads", filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))

