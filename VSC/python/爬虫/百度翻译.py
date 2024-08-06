import requests
import json
 
# 1.获取请求的 URL
post_url='https://fanyi.baidu.com/sug'
# 并进行UA伪装
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
 
# 2.参数处理（发起请求的URL有参数才需要处理），然后发送请求
word=input('enter the word:')
data={'kw':word}
response=requests.post(post_url,data,headers=header)
 
# 3.获取响应数据 
# .text返回的是一个字符串形式的 json 串，若确认响应数据是json类型，才可以使用.json返回，响应头信息当中的Content-Type可以确认
dic_obj=response.json()
print(type(response))
print(dic_obj)
print(type(dic_obj))
 
# 4.持久化存储
fp=open(word+'.json','w',encoding='utf-8')
json.dump(dic_obj,fp=fp,ensure_ascii=False) # 中文不能使用Ascii进行编码
 
print('over')