## 数据操作
| 函数	| 功能|
|-----------|---------|
|Tensor(*sizes)	|基础构造函数|
|tensor(data,)	|类似np.array的构造函数|
|ones(*sizes)	|全1Tensor|
|zeros(*sizes)	|全0Tensor|
|eye(*sizes)	|对角线为1，其他为0|
|arange(s,e,step)	|从s到e，步长为step|
|linspace(s,e,steps)|	从s到e，均匀切分成steps份|
|rand/randn(*sizes)	|均匀/标准分布|
|normal(mean,std)/uniform(from,to) |	正态分布/均匀分布|
|randperm(m)	|随机排列|

| index_select(input, dim, index)	|在指定维度dim上选取，比如选取某些行、某些列|
| masked_select(input, mask)	|例子如上，a[a>0]，使用ByteTensor进行选取|
|nonzero(input)	| 非0元素的下标|
|gather(input, dim, index)	|根据index，在dim维度上选取数
## 使用张量表征真实数据