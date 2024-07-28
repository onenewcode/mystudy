import pandas as pd
import io
def style_apply(content, colors, back_ground=''):
    if content != None and content in colors.keys():
        return 'background-color: ' + colors[content]
    return back_ground

def style_color(df, colors):
    return df.style.applymap(style_apply, colors=colors)
#主要的文件地址
masterpath=r"C:\Users\ztf\OneDrive\Desktop\3.11\2022各学院优秀校友信息汇总-2.xlsx"
# 从属文件地址
path=r"C:\Users\ztf\OneDrive\Desktop\6Z(1).xlsx"
# 储存新的的数据
new_data=[]
# sheet_name=0
# 设置header参数，可以指定目标行的数据为列标签
newpath=[]
oldpath=[]
oldOder=0
newOder=0
try:
    pathResult=pd.read_excel(path,header=1,index_col="姓名")
    masterResult = pd.read_excel(masterpath,header=1,index_col="姓名",sheet_name="总表")
except  Exception:
    print("文件夹路径出错，请重新检查路径")
    exit(0)   
# result=pd.(masterResult.columns)
re=[]
# re.append(masterResult.columns)
for index,row in pathResult.iterrows():
    # 追加数据
    try:
        masterResult.loc[index]
        # oldOder.append(row)
        oldpath.append(index)
    except Exception:
        newpath.append(index)    
    # print(index)  
    # oldpath.append(index)      
    # print(masterResult.loc[index])
# print(masterResult.loc["孟景昱"])    
# filename=r'./test.txt'
print(oldpath)
# with open(filename, 'w',encoding='utf-8') as file_object:
#     for i in oldpath:
#      file_object.write(i)
     
# newpath=pd.DataFrame(newpath)
# newpath.index.name="姓名"
# print(newpath.reset_index(drop = False))
# pd.DataFrame(re).to_excel(r"C:\Users\ztf\OneDrive\桌面\11.xlsx")
#     except Exception,e:
#   print e
# print(masterResult.columns)     
# print(result) 
# for index,row in masterResult.iterrows():
#     print(index)
#     # 添加一行数据 
#     result.append(row)  
# print(result.set_index("序号",drop=False))

# [(x, y) for x in range(5) if x % 2 == 0 for y in range(5) if y % 2 == 1]
# 根据列名获取
# print(result['name'])
# print([[i] for i in range(len(new_data)-1)])

# print(pd.DataFrame(new_data).set_index("姓名", drop=False))

# index 决定是否加载索引，header决定是否加载表头
#  to_excel的参数startrow、startcol为写入的起始行列
# pd.DataFrame(new_data).to_excel("test.xlsx",sheet_name='Sheet1', header=False)
# print(result)

# 根据行和列的标签获取
# print(result.loc[0,"name"])


"""
writer = pd.ExcelWriter("demo1.xlsx")
workbook = writer.book
workbook

excle数据遍历 1
data = pd.read_excel(filePath, None, header=None) #设置header才能读取到第一行
for jKey in data.keys():
	jSheetData = data[jKey]
    totalRow = len(jSheetData.index) #总行数
    for kRow in range(1, totalRow):#从第二行开始遍历
    	oneRow = jSheetData.loc[kRow][0:]
    	for kIndex in range(len(oneRow)):
            kContent = oneRow[kIndex] #获取到单元格内容
excle数据遍历 2

for index,row in result.iterrows():
    new_data.append(row)
print(pd.DataFrame(new_data))       
            
"""
"""
excel单元格颜色设置以及excel写入

def style_apply(content, colors, back_ground=''):
    if content != None and content in colors.keys():
        return 'background-color: ' + colors[content]
    return back_ground

def style_color(df, colors):
    return df.style.applymap(style_apply, colors=colors)
    
resultMap = {'A':['test1', 'test2', 'test3'], 'B':['test2', 'test4', 'test5']} #写入数据结构示例
filePath = "{}.xlsx".format(int(time.time()*1000))

compare_pd=pd.DataFrame(resultMap)
writer = pd.ExcelWriter(filePath, engine='openpyxl')#创建数据存放路径

colors = {'test1':'#ff0000', 'test2':'#ffff00'}
style_df = style_color(compare_pd, colors)

style_df.to_excel(writer, header=None, index=False, sheet_name='compare')

writer.save()#文件保存
writer.close()

os.startfile(filePath)# 使用默认程序自动打开新生成的excel文件

"""