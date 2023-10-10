# 各种基本类型及方法
## dict（字典）
**创建方法**
```py
p=dict()
p={'':}
```
**方法**
list(d)
返回字典 d 中使用的所有键的列表。

len(d)
返回字典 d 中的项数。

d[key]
返回 d 中以 key 为键的项。 如果映射中不存在 key 则会引发 KeyError。
key in d
如果 d 中存在键 key 则返回 True，否则返回 False。

key not in d
等价于 not key in d。

iter(d)
返回以字典的键为元素的迭代器。 这是 iter(d.keys()) 的快捷方式。

clear()
移除字典中的所有元素。

copy()
返回原字典的浅拷贝。
get(key[, default])
如果 key 存在于字典中则返回 key 的值，否则返回 default。 如果 default 未给出则默认为 None，因而此方法绝不会引发 KeyError。

items()
返回由字典项 ((键, 值) 对) 组成的一个新视图。 参见 视图对象文档。

keys()
返回由字典键组成的一个新视图。 参见 视图对象文档。

pop(key[, default])
如果 key 存在于字典中则将其移除并返回其值，否则返回 default。 如果 default 未给出且 key 不存在于字典中，则会引发 KeyError。

popitem()
从字典中移除并返回一个 (键, 值) 对。 键值对会按 LIFO 的顺序被返回。

popitem() 适用于对字典进行消耗性的迭代，这在集合算法中经常被使用。 如果字典为空，调用 popitem() 将引发 KeyError。

在 3.7 版更改: 现在会确保采用 LIFO 顺序。 在之前的版本中，popitem() 会返回一个任意的键/值对。

reversed(d)
返回一个逆序获取字典键的迭代器。 这是 reversed(d.keys()) 的快捷方式。

3.8 新版功能.

setdefault(key[, default])
如果字典存在键 key ，返回它的值。如果不存在，插入值为 default 的键 key ，并返回 default 。 default 默认为 None。

update([other])
使用来自 other 的键/值对更新字典，覆盖原有的键。 返回 None。