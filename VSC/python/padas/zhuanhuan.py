import numpy as np
import pandas as pd
from pandas import Series, DataFrame

data = {'Country':['Belgium', 'India', 'Brazil'],
        'Capital':['Brussels', 'New Delhi', 'Brasilia'],
        'Population':[11190846, 1303171035, 207847528]
        }

# Series

s1 = Series(data['Country'])
print(s1)
'''
0    Belgium
1      India
2     Brazil
dtype: object
'''
print(s1.values) # 类型： <class 'numpy.ndarray'>
'''
['Belgium' 'India' 'Brazil']
'''
print(s1.index)
'''
RangeIndex(start=0, stop=3, step=1)
'''

# 为Series指定index
s1 = Series(data['Country'], index=['A', 'B', 'C'])
print(s1)
''' 索引更改
A    Belgium
B      India
C     Brazil
dtype: object
'''


# Dataframe

df1 = pd.DataFrame(data)
print(df1)
'''
     Capital  Country  Population
0   Brussels  Belgium    11190846
1  New Delhi    India  1303171035
2   Brasilia   Brazil   207847528
'''

print(df1['Capital']) # 类型: series
'''
0     Brussels
1    New Delhi
2     Brasilia
Name: Capital, dtype: object
'''


print(df1.iterrows()) # 返回 一个 生成器 <generator object DataFrame.iterrows at 0x7f226a67b728>

for row in df1.iterrows():
    print(row)
    print(row[0], row[1])
    print(type(row[0]), type(row[1]))
    break
''' 
print(row) 返回了一个元组
(0, Capital       Brussels
Country        Belgium
Population    11190846
Name: 0, dtype: object)
'''
'''
print(row[0], row[1]) 的返回值
0 Capital       Brussels
Country        Belgium
Population    11190846
Name: 0, dtype: object
'''
'''
print(type(row[0]), type(row[1]))
<class 'int'> <class 'pandas.core.series.Series'>

row[1] 是一个 series，而且原来的列名，现在变成了现在的索引名，
由此可见，dataframe是由多个行列交错的series组成。
'''

#　现在可以　构建几个series
s1 = pd.Series(data['Country'])
s2 = pd.Series(data['Capital'])
s3 = pd.Series(data['Population'])
df_new = pd.DataFrame([s1, s2, s3], index=['Country', 'Captital', 'Population'])
print(df_new)
'''
                   0           1          2
Country      Belgium       India     Brazil
Captital    Brussels   New Delhi   Brasilia
Population  11190846  1303171035  207847528

可以看到，行　和　列　都是颠倒的，因此需要进行一下转置
'''

print(df_new.T)
'''
   Country   Captital  Population
0  Belgium   Brussels    11190846
1    India  New Delhi  1303171035
2   Brazil   Brasilia   207847528

'''

'''
总结：
    series, 就是一个　一维 的数据结构，它是由　ｉｎｄｅｘ　和　ｖａｌｕｅ　组成。
    dataframe, 是一个　二维　数据结构，它由多个　ｓｅｒｉｅｓ　构成。
'''
