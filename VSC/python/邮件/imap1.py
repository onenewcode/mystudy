#coding: UTF-8

import imaplib
import email
from email.parser import Parser
import re,os
import win32gui, win32api, win32com 
from win32com.client import Dispatch

pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')

def Start_mailbox(host,post,uesr,passwrod):#启动imap邮箱服务
    try:
        conn = imaplib.IMAP4(host, post)
        conn.login(uesr, passwrod)
        print("[+] Connect to {0}:{1} successfully".format(host, post))
        return conn
    except BaseException as e:
        print("Connect to {0}:{1} failed".format(host, post), e)

def GetTxtName(dir):#获取dir文件下的所有文件名
    listName = []
    for fileName in os.listdir(dir):  
        fileName = os.path.splitext(fileName)[0]
        listName.append(fileName)
    return listName

def get_filename(wkb_path,Download_path,sheetname,From_mail_name_all,From_mail_type):
    os.system('taskkill /IM EXCEL.exe /F')
    xlapp = win32com.client.gencache.EnsureDispatch('Excel.Application')
    xlapp.Visible = 1
    xlapp.DisplayAlerts = False # 关闭警告
    wkb = xlapp.Workbooks.Open(wkb_path)
    wkb_sheet = wkb.Worksheets(sheetname)
    listName = GetTxtName(Download_path)
    #print(listName)
    n=1
    last_row = wkb_sheet.Range('A2').End(-4121).Row
    for i in range(0,len(listName)-3):
        #one_range = 'A' + str(last_row+1+i)
        two_range = 'B' + str(last_row+1+i)
        true_range = 'C' + str(last_row+1+i)
        #print(one_range)
        wkb_sheet.Select()
        #wkb_sheet.Range(one_range).Value = listName[i]
        try:
            wkb_sheet.Range(two_range).Value = From_mail_name_all[i]
            wkb_sheet.Range(true_range).Value = From_mail_type[i]
        except:
            pass
        n=n+1
    wkb.Save()
    wkb.Close()
    xlapp.Quit()

def savefile(filename, data, path):#保存文件方法（保存在path目录下）
    try:
       filepath = path +r'\\'+ filename
       print(filepath)
       f = open(filepath, 'wb')
    except:
        print('filename error')
        f.close()
    f.write(data)
    f.close()
    
def remove_email(old_maildir,new_maildir):#移动邮箱文件夹
    try:
        conn.select(old_maildir, readonly=False)
        type_, data = conn.search(None,"ALL")
        email_ids = data[0].split()
        for i in range(-1,len(email_ids)-1):
            latest_email_id = email_ids[i]
            resp,data = conn.fetch(latest_email_id,'(UID)')
            match = pattern_uid.match(data[0].decode('utf-8'))
            msg_uid = match.group('uid')
            result = conn.uid('COPY',msg_uid,new_maildir)
            if result[0]=='OK':
                conn.select(old_maildir, readonly=False)
                type_,data = conn.search(None,"ALL")
                mov,data = conn.uid('STORE',msg_uid, '+FLAGS', '(\\Deleted)')
                conn.expunge()
    except BaseException as e:
        print('fail error:',e)

def remove_email_file(old_maildir,new_maildir,msg_uid):#移动邮箱文件夹
    try:
        conn.select(old_maildir, readonly=False)
        type_, data = conn.search(None,"ALL")
        result = conn.uid('COPY',msg_uid,new_maildir)
        print('copy successful:',msg_uid)
        if result[0]=='OK':
            conn.select(old_maildir, readonly=False)
            type_,data = conn.search(None,"ALL")
            mov,data = conn.uid('STORE',msg_uid, '+FLAGS', '(\\Deleted)')
            conn.expunge()
            print('delect successful:',msg_uid)
    except BaseException as e:
        print('fail error:',e)
          
def parseHeader(msg):#解析邮件首部,备用方案
    # 发件人
    From_mail = email.utils.parseaddr(msg.get('from'))[1]
    # 收件人
    To_mail = email.utils.parseaddr(msg.get('to'))[1]
    # 抄送人
    Cc_mail = email.utils.parseaddr(msg.get_all('cc'))[1]
    
def imap4(conn,old_maildir,new_maildir,Download_path,wkb_path,sheetname2):
    # 初始化变量
    list_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
    From_mail_name_all = {}
    From_mail_name_all_list = {}
    
    # Select and search folder
    conn.select(old_maildir, readonly=True)
    type_, data = conn.search(None, "ALL")#ALL参数可以进行修改，类似匹配，假如不想要全部文件，可以进行筛选查询
    
    #获取邮件正文和附件并重命名保存，优先保存附件，没有附件的情况下保存正文（正文大于500字），
    pcount = 1
    mail_list = data[0].split()#传输当前文件夹下的文件给mail_list
    for num in mail_list:
        
        type_, data = conn.fetch(num,'(RFC822)')
        msg = email.message_from_string(data[0][1].decode('utf-8'))#传输邮件全部内容，用email解析
        
        # email解析件内容，获取发件人名称，以@进行截取
        From_mail = email.utils.parseaddr(msg.get('from'))[1]
        From_mail_name = From_mail.split('@')[0]
        print(From_mail_name)
        mail_title,mail_charset = email.header.decode_header(msg.get('Subject'))[0]
        print(mail_title)
        
        # email解析件内容
        for part in msg.walk():
            if not part.is_multipart():
            
                filename = part.get_filename() #如果是附件，这里就会取出附件的文件名
                contentType = part.get_content_type()
                mycode = part.get_content_charset()
                print(filename)
                
                if filename:
                    #保存附件
                    print('下载文件')
                    attach_data = part.get_payload(decode=True)
                    #filename = list_pattern.findall(filename)
                    save_name = From_mail_name + '.docx'#以发件人名称的方式保存为doc的文件
                    savefile(save_name, attach_data, Download_path)
                    From_mail_name_all['EM'] = From_mail_name
                    From_mail_name_all['文件发送方式'] = '附件'
                    From_mail_name_all_list[num] = From_mail_name_all
                    print(From_mail_name_all_list)
                    #下载一个文件之后把这个文件移动到新的邮件文件夹，以便后面遍历for少一些数据。
                    try:
                        resp,data = conn.fetch(num,'(UID)')
                        match = pattern_uid.match(data[0].decode('utf-8'))
                        msg_uid = match.group('uid')
                        print(msg_uid)
                        remove_email_file(old_maildir,new_maildir,msg_uid)
                    except BaseException as e:
                        print("remove email failed", e)
                        
                elif contentType == 'text/plain' or contentType == 'text/html':
                    print('邮件正文')
                    #保存正文
                    try:
                        data = part.get_payload(decode=True).decode('utf-8')
                        data = re.sub(u"\<br\>\</p\>","\n   ", data)
                        data = re.sub(u"\<br\>","\n", data)
                        data = re.sub(u"\</p\>","  ", data)
                        data = re.sub(u"\<.*?\>","", data)
                        data = re.sub(u"\{.*?\}","", data)
                        data = re.sub(u"\ ","", data)
                        data = re.sub(u"table\.customTableClassName","", data)
                        data = re.sub(u"职业培训领跑者！ 学习是一种信仰！","", data)
                        data = re.sub(u"\[object Object\]","", data)
                        data = re.sub(u"\.customTableClassName td, \.customTableClassName th","", data)
                        #print('邮件正文长度:',len(data))
                        if len(data) <500:#指定邮件内容最小长度。
                            pass
                        else:
                            save_name = From_mail_name + '.txt'
                            savefile(save_name,data.encode('utf-8'),Download_path)
                            From_mail_name_all['EM'] = From_mail_name
                            From_mail_name_all['文件发送方式'] = '邮件文本'
                            From_mail_name_all_list[num] = From_mail_name_all
                            print(From_mail_name_all_list)
                            try:
                                resp,data = conn.fetch(num,'(UID)')
                                match = pattern_uid.match(data[0].decode('utf-8'))
                                msg_uid = match.group('uid')
                                remove_email_file(old_maildir,new_maildir,msg_uid)
                            except BaseException as e:
                                print("failed", e)
                                pass
                            
                    except BaseException as e:
                        print("failed", e)
                        pass
                    
                else: #From_mail_type.append('其他文件')
                    pass
        print ('</br>')
        print ('\n\n')
        pcount += 1
        
    print(From_mail_name_all_list)
    #get_filename(wkb_path,Download_path,sheetname2,From_mail_name_all,From_mail_type)#向excel中写入统计结果
    conn.close()
    conn.logout()

# ******************主程序************************#

#参数设置
Download_path = r'C:\Users\1\Desktop\4月关于“为用户创造价值的思考和理解”的总结报告\aaaa'
wkb_path = r"C:\Users\1\Desktop\4月关于“为用户创造价值的思考和理解”的总结报告\汇总.xlsx"
sheetname2 = '邮箱接受文件数'
old_maildir = 'INBOX'
new_maildir = '&XfJfUmhj-/&XfJn5ZYFZwllSA-'
rubbish_maildir = '&XfJfUmhj-/&U4ZT8leDVz5lh072-'
host = 'imap.263.net'
post = '143'
uesr = '***************'
passwrod = '*************'

#启动imap邮箱服务
conn = Start_mailbox(host,post,uesr,passwrod)
'''
#查看imap邮箱有多少个文件夹，imap不是ut-f8编码，不能自动编译，需自行查看
try:
    type_, folders = conn.list()
    for i in folders:
        print(i)
except BaseException as e:
    print("the {0}:{1} no file".format("imap.263.net", 143), e)
'''
imap4(conn,old_maildir,new_maildir,Download_path,wkb_path,sheetname2)
#remove_email(old_maildir,rubbish_maildir)#移动收件箱数据到指定的文件夹中
#'''