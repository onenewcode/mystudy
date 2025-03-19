# 图像的基础操作
## 图像的 IO 操作
包括点 Point 类、颜色 Scalar 类、尺寸 Size 类、矩形 Rect 类、矩阵 Mat 类
### 读取操作
`cv.imread()`
**参数**
- 要读取的图像
- 读取方式的标志

    - cv.IMREAD*COLOR：以彩色模式加载图像，任何图像的透明度都将被忽略。这是默认参数。

    - cv.IMREAD*GRAYSCALE：以灰度模式加载图像

    -  cv.IMREAD_UNCHANGED：包括 alpha 通道的加载图像模式。

**可以使用 1、0 或者 -1 来替代上面三个标志**,但是必须是对应的图像维度才行，可以通过`img.shape`查看图像维度，彩色三维。灰度二维

### 显示图像
`cv.imshow()`
- 显示图像的窗口名称，以字符串类型表示
- 要加载的图像

在调用显示图像的 API 后，要调用 cv.waitKey() 给图像绘制留下间，否则窗口会出现无响应情况，并且图像无法显示出来。

### 保存图像
`cv.imwrite()`

- 文件名，要保存在哪里
- 要保存的图像

## 绘制几何图形
### 绘制直线
`cv.line(img,start,end,color,thickness)`

- img:要绘制直线的图像
- Start,end: 直线的起点和终点
- color: 线条的颜色
- Thickness: 线条宽度

### 绘制圆形
`cv.circle(img,centerpoint, r, color, thickness)`

- img:要绘制圆形的图像
- Centerpoint, r: 圆心和半径
- color: 线条的颜色
- Thickness: 线条宽度，为 -1 时生成闭合图案并填充颜色

### 绘制矩形
`cv.rectangle(img,leftupper,rightdown,color,thickness)`

- img:要绘制矩形的图像
- Leftupper, rightdown: 矩形的左上角和右下角坐标
- color: 线条的颜色
- Thickness: 线条宽度


## 向图像中添加文字
`cv.putText(img,text,station, font, fontsize,color,thickness,cv.LINE_AA)`

- img: 图像
- text：要写入的文本数据
- station：文本的放置位置
- font：字体
- Fontsize :字体大小

## 获取并修改图像中的像素点
```py
import numpy as np
import cv2 as cv
img = cv.imread('messi5.jpg')
# 获取某个像素点的值
px = img[100,100]
# 仅获取蓝色通道的强度值
blue = img[100,100,0]
# 修改某个位置的像素值
img[100,100] = [255,255,255]
```
## 获取图像的属性
`img.shape`
`img.size`
`img.dtype`
## 图像通道的拆分与合并
```py
# 通道拆分
b,g,r = cv.split(img)
# 通道合并
img = cv.merge((b,g,r))
```

## 算数操作
### 图像的加法
使用 OpenCV 的 cv.add() 函数把两幅图像相加，或者可以简单地通过 numpy 操作添加两个图像

**OpenCV 加法和 Numpy 加法之间存在差异。OpenCV 的加法是饱和操作，而 Numpy 添加是模运算。**
```py
>>> x = np.uint8([250])
>>> y = np.uint8([10])
>>> print( cv.add(x,y) ) # 250+10 = 260 => 255
[[255]]
>>> print( x+y )          # 250+10 = 260 % 256 = 4
[4]
```
### 图像的混合
`cv.addWeighted`

这其实也是加法，但是不同的是两幅图像的权重不同，这就会给人一种混合或者透明的感觉。图像混合的计算公式如下：

g(x) = (1−α)f0(x) + αf1(x)
```py
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# 1 读取图像
img1 = cv.imread("view.jpg")
img2 = cv.imread("rain.jpg")

# 2 图像混合
img3 = cv.addWeighted(img1,0.7,img2,0.3,0)

# 3 图像显示
plt.figure(figsize=(8,8))
plt.imshow(img3[:,:,::-1])
plt.show()
```

## 图像缩放
`cv2.resize(src,dsize,fx=0,fy=0,interpolation=cv2.INTER_LINEAR)`

- src : 输入图像

- dsize: 绝对尺寸，直接指定调整后图像的大小

- fx,fy: 相对尺寸，将 dsize 设置为 None，然后将 fx 和 fy 设置为比例因子即可

- interpolation：插值方法，
##  图像平移
`cv.warpAffine(img,M,dsize)`

- img: 输入图像
- M：2∗3 移动矩阵
- dsize: 输出图像的大小

注意：输出图像的大小，它应该是 (宽度，高度) 的形式。请记住，width=列数，height=行数。

##  图像旋转
`cv2.getRotationMatrix2D(center, angle, scale)`

- center：旋转中心
- angle：旋转角度
- scale：缩放比例

## 仿射变换
图像的仿射变换涉及到图像的形状位置角度的变化，是深度学习预处理中常到的功能，仿射变换主要是对图像的缩放，旋转，翻转和平移等操作的组合。

在 OpenCV 中，仿射变换的矩阵是一个 2×3 的矩阵

TODO


## 透射变换
透射变换是视角变化的结果，是指利用透视中心、像点、目标点三点共线的条件，按透视旋转定律使承影面（透视面）绕迹线（透视轴）旋转某一角度，破坏原有的投影光线束，仍能保持承影面上投影几何图形不变的变换。
M = cv2.getPerspectiveTransform(pos1, pos2) 
 pos1 表示透视变换前的 4 个点对应位置
 pos2 表示透视变换后的 4 个点对应位置
cv2.warpPerspective(src,M,(cols,rows)) 
 src 表示原始图像
 M 表示透视变换矩阵
 (rows,cols) 表示变换后的图像大小，rows 表示行数，cols 表示列
数
## 量化处理
量化（Quantization）旨在将图像像素点对应亮度的连续变化区间转换为单个特定值的过程，即将原始灰度图像的空间坐标幅度值离散化。量化等级越多，图像层次越丰富，灰度分辨率越高，图像的质量也越好；量化等级越少，图像层次欠丰富，灰度分辨率越低，会出现图像轮廓分层的现象，降低了图像的质量。是将图像的连续灰度值转换为 0 至 255 的灰度级的过程
### K-Means 聚类实现量化处理
```PY
compactness, labels, centers = cv2.kmeans(data, K,bestLabels, criteria, attempts, flags, center=None)
```
- data：需要聚类的数据，每一行表示一个样本点。
- K：需要聚类的簇个数。
- bestLabels：预设的标签，如果不为 None，则表示用预设标签作为每个样本点的初始簇。
- criteria：迭代终止条件，可以使用 cv2.TERM_CRITERIA_EPS 或 cv2.TERM_CRITERIA_MAX_ITER，或者它们的组合。
- attempts：算法重复尝试的次数，选择其中最优的一次聚类结果作为输出。
- flags：选择初始中心点的方式，可以为 cv2.KMEANS_RANDOM_CENTERS、cv2.KMEANS_PP_CENTERS 等。
- center：用于存储输出的聚类中心点。如果为 None，则函数会自动为其开辟空间。
函数返回值有 3 个：

- compactness：每个样本点到其所属簇中心的距离平方和。
- labels：每个样本所属的簇的标签。
- centers：所有簇的中心点。
## 采样处理
##  图像金字塔
<!-- 图像的大小是原始图像的一半，分辨率也减少了一半。 -->
cv.pyrUp(img)       #对图像进行上采样
cv.pyrDown(img)        #对图像进行下采样
# 图像运算和图像增强
## 灰度线性变化
对比度增强
```py
# -*- coding: utf-8 -*-
# By：Eastmount
import cv2 
import numpy as np 
import matplotlib.pyplot as plt
#读取原始图像
img = cv2.imread('luo.png')
#图像灰度转换
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#获取图像高度和宽度
height = grayImage.shape[0]
width = grayImage.shape[1]
#创建一幅图像
199
result = np.zeros((height, width), np.uint8)
#图像对比度增强变换 DB=DA×1.5
for i in range(height):
 for j in range(width):
 
 if (int(grayImage[i,j]*1.5) > 255):
 gray = 255
 else:
 gray = int(grayImage[i,j]*1.5)
 
 result[i,j] = np.uint8(gray)
#显示图像
cv2.imshow("Gray Image", grayImage)
cv2.imshow("Result", result)
```
##  图像灰度非线性变换
对比增强
```py
mport cv2 
import numpy as np 
import matplotlib.pyplot as plt
208
#读取原始图像
img = cv2.imread('luo.png')
#图像灰度转换
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#获取图像高度和宽度
height = grayImage.shape[0]
width = grayImage.shape[1]
#创建一幅图像
result = np.zeros((height, width), np.uint8)
#图像灰度非线性变换：DB=DA×DA/255
for i in range(height):
 for j in range(width):
 gray = int(grayImage[i,j])*int(grayImage[i,j]) / 255
 result[i,j] = np.uint8(gray)
#显示图像
209
cv2.imshow("Gray Image", grayImage)
cv2.imshow("Result", result)
#等待显示
cv2.waitKey(0)
cv2.destroyAllWindows()
```
### 图像灰度对数变换
由于对数曲线在像素值较低的区域斜率大，在像素值较高的区域斜率较小，所以图像经过对数变换后，较暗区域的对比度将有所提升。这种变换可用于增强图像的暗部细节，从而用来扩展被压缩的高值图像中的较暗像素。
```py
# -*- coding: utf-8 -*-
# By：Eastmount
import numpy as np
import matplotlib.pyplot as plt
import cv2
#绘制曲线
def log_plot(c):
 x = np.arange(0, 256, 0.01)
 y = c * np.log(1 + x)
 plt.plot(x, y, 'r', linewidth=1)
 plt.rcParams['font.sans-serif']=['SimHei'] #正常显示中文标签
 plt.title('对数变换函数')
 plt.xlabel('x')
 plt.ylabel('y')
 plt.xlim(0, 255), plt.ylim(0, 255)
 plt.show()
#对数变换
def log(c, img):
 output = c * np.log(1.0 + img)
 output = np.uint8(output + 0.5)
 return output
#读取原始图像
img = cv2.imread('dark.png')
#绘制对数变换曲线
log_plot(42)
#图像灰度对数变换
output = log(42, img)
#显示图像
cv2.imshow('Input', img)
cv2.imshow('Output', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
###   图像灰度伽玛变换
 当γ>1 时，会拉伸图像中灰度级较高的区域，压缩灰度级较低的部分。
 当γ<1 时，会拉伸图像中灰度级较低的区域，压缩灰度级较高的部分。
 当γ=1 时，该灰度变换是线性的，此时通过线性方式改变原图像。
```py
import numpy as np

import matplotlib.pyplot as plt
import cv2
#绘制曲线
def gamma_plot(c, v):
 x = np.arange(0, 256, 0.01)
 y = c*x**v
 plt.plot(x, y, 'r', linewidth=1)
 plt.rcParams['font.sans-serif']=['SimHei'] #正常显示中文标签
 plt.title('伽马变换函数')
 plt.xlabel('x')
 plt.ylabel('y')
 plt.xlim([0, 255]), plt.ylim([0, 255])
 plt.show()
#伽玛变换
def gamma(img, c, v):
 lut = np.zeros(256, dtype=np.float32)
 for i in range(256):
 lut[i] = c * i ** v
 output_img = cv2.LUT(img, lut) #像素灰度值的映射
 output_img = np.uint8(output_img+0.5) 
 return output_img
#读取原始图像
img = cv2.imread('white.png')
#绘制伽玛变换曲线
gamma_plot(0.00000005, 4.0)
#图像灰度伽玛变换
output = gamma(img, 0.00000005, 4.0)
#显示图像
cv2.imshow('Imput', img)
cv2.imshow('Output', output)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
## 图像点运算之图像阈值化处理
dst = cv2.threshold(src, thresh, maxval, type[, dst]) 
 src 表示输入图像的数组，8 位或 32 位浮点类型的多通道数
 dst 表示输出的阈值化处理后的图像，其类型和通道数与 src 一致
 thresh 表示阈值
 maxval 表 示 最 大 值，当 参 数 阈 值 类 型 type 选 择
CV_THRESH_BINARY 或 CV_THRESH_BINARY_INV 时，该参数为阈值类型的最大值
 type 表示阈值类型

|算法原型 | 算法含义 |
|--------------|-----------------------|
|threshold(Gray,127,255,cv2.THRESH_BINARY)|像素点的灰度值大于阈值设其灰度值为最大值，小于阈值的像素点灰度值设定为 0。|
|threshold(Gray,127,255,cv2.THRESH_BINARY_INV)|大于阈值的像素点的灰度值设定为 0，而小于该阈值的设定为 255。|
|threshold(Gray,127,255,cv2.THRESH_TRUNC)|像素点的灰度值小于阈值不改变，反之将像素点的灰度值设定为该阈值。|
|threshold(Gray,127,255,cv2.THRESH_TOZERO)|像素点的灰度值小于该阈值的不进行任何改变，而大于该阈值的部分，其灰度值全变为 0。|
|threshold(Gray,127,255,cv2.THRESH_TOZERO_INV)|像素点的灰度值大于该阈值的不进行任何改变，小于该阈值其灰度值全部设定为 0。|
### 自适应阈值化处理
dst = adaptiveThreshold(src, maxValue, adaptiveMethod, 
thresholdType, blockSize, C[, dst]) 
 src 表示输入图像
235
 dst 表示输出的阈值化处理后的图像，其类型和尺寸需与 src 一致
 maxValue 表示给像素赋的满足条件的最大值
 adaptiveMethod 表示要适用的自适应阈值算法，常见取值包括
ADAPTIVE_THRESH_MEAN_C（阈值取邻域的平均值）或 ADAPTIVE_THRESH_GAUSSIAN_C（阈值取自邻域的加权和平均值，权重分布为一个高斯函数分布）
 thresholdType 表示阈值类型，取值必须为 THRESH_BINARY 或 THRESH_BINARY_INV
 blockSize 表示计算阈值的像素邻域大小，取值为 3、5、7 等
 C 表示一个常数，阈值等于平均值或者加权平均值减去这个常数
## 形态学操作
dst = cv2.morphologyEx(src, model, kernel) 
 src 表示原始图像
 model 表示图像进行形态学处理，包括：
  - (1) cv2.MORPH_OPEN：开运算（Opening Operation）
  - (2)cv2.MORPH_CLOSE：闭运算（Closing Operation）
  - (3)cv2.MORPH_GRADIENT：形态学梯度（Morphological Gradient）
  - (4)cv2.MORPH_TOPHAT：顶帽运算（Top Hat）
  - (5)cv2.MORPH_BLACKHAT：黑帽运算（Black Hat）
 kernel 表示卷积核，可以用 numpy.ones() 函数构建
### 腐蚀和膨胀
具体操作是：用一个结构元素扫描图像中的每一个像素，用结构元素中的每一个像素与其覆盖的像素做“与”操作，如果都为 1，则该像素为 1，否则为 0。

腐蚀的作用是消除物体边界点，使目标缩小，可以消除小于结构元素的噪声点。
cv.erode(img,kernel,iterations)

- img: 要处理的图像
- kernel: 核结构
- iterations: 腐蚀的次数，默认是 1

cv.dilate(img,kernel,iterations)

### 开闭运算
开运算和闭运算是将腐蚀和膨胀按照一定的次序进行处理。但这两者并不是可逆的，即先开后闭并不能得到原来的图像。
- 开运算
开运算是先腐蚀后膨胀，其作用是：分离物体，消除小区域。特点：消除噪点，去除小的干扰块，而不影响原来的图像。

- 闭运算
闭运算与开运算相反，是先膨胀后腐蚀，作用是消除/“闭合”物体里面的孔洞，特点：可以填充闭合区域。
cv.morphologyEx(img, op, kernel)

- img: 要处理的图像
- op: 处理方式：若进行开运算，则设为 cv.MORPH_OPEN，若进行闭 - 运算，则设为 cv.MORPH_CLOSE
- Kernel：核结构
### 图像梯度运算 
图像梯度运算是图像膨胀处理减去图像腐蚀处理后的结果，从而得到图像的轮廓，
dst = cv2.morphologyEx(src, cv2.MORPH_GRADIENT, 
kernel) 
 src 表示原始图像
 cv2.MORPH_GRADIENT 表示图像进行梯度运算处理
 kernel 表示卷积核，可以用 numpy.ones() 函数构建

### 礼帽和黑帽
- 礼帽运算
图像与“开运算“的结果图之差，如下式计算：
礼帽运算用来分离比邻近点亮一些的斑块。当一幅图像具有大幅的背景的时候，而微小物品比较有规律的情况下，可以使用顶帽运算进行背景提取。

- 黑帽运算
黑帽运算后的效果图突出了比原图轮廓周围的区域更暗的区域，且这一操作和选择的核的大小相关。
黑帽运算用来分离比邻近点暗一些的斑块。
## 图像直方图理论知识和绘制实现
hist = cv2.calcHist(images, channels, mask, histSize,ranges, accumulate) 
 hist 表示直方图，返回一个二维数组
 images 表示输入的原始图像
 channels 表示指定通道，通道编号需要使用中括号，输入图像是
灰度图像时，它的值为[0]，彩色图像则为[0]、[1]、[2]，分别表示蓝色（B）、绿色（G）、红色（R）
 mask 表示可选的操作掩码。如果要统计整幅图像的直方图，则该
值为 None；如果要统计图像的某一部分直方图时，需要掩码来计算
 histSize 表示灰度级的个数，需要使用中括号，比如[256]
 ranges 表示像素值范围，比如[0, 255]
 accumulate 表示累计叠加标识，默认为 false，如果被设置为
true，则直方图在开始分配时不会被清零，该参数允许从多个对象
中计算单个直方图，或者用于实时更新直方图；多个直方图的累积
结果用于对一组图像的直方图计算
```py
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#读取图像
src = cv2.imread('lena-hd.png')
#计算 256 灰度级的图像直方图
hist = cv2.calcHist([src], [0], None, [256], [0,255])
#输出直方图大小、形状、数量
print(hist.size)
print(hist.shape)
print(hist)
#设置字体
matplotlib.rcParams['font.sans-serif']=['SimHei']
#显示原始图像和绘制的直方图
plt.subplot(121)
plt.imshow(src, 'gray')
plt.axis('off')
plt.title("(a)Lena 灰度图像")
plt.subplot(122)
plt.plot(hist, color='r')
plt.xlabel("x")
plt.ylabel("y")
plt.title("(b) 直方图曲线")
plt.show()
```
```py
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#读取图像
src = cv2.imread('lena.png')
#转换为 RGB 图像
img_rgb = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
#获取 BGR 三个通道的像素值
b, g, r = cv2.split(src)
print(r,g,b)
plt.figure(figsize=(8, 6))
#设置字体
matplotlib.rcParams['font.sans-serif']=['SimHei']
#原始图像
plt.subplot(221)
plt.imshow(img_rgb)
plt.axis('off')
plt.title("(a) 原图像")
#绘制蓝色分量直方图
plt.subplot(222)
plt.hist(b.ravel(), bins=256, density=1, facecolor='b', 
edgecolor='b', alpha=0.75)
plt.xlabel("x")
plt.ylabel("y")
plt.title("(b) 蓝色分量直方图")
#绘制绿色分量直方图
plt.subplot(223)
plt.hist(g.ravel(), bins=256, density=1, facecolor='g', 
edgecolor='g', alpha=0.75)
plt.xlabel("x")
plt.ylabel("y")
plt.title("(c) 绿色分量直方图")
#绘制红色分量直方图
plt.subplot(224)
plt.hist(r.ravel(), bins=256, density=1, facecolor='r', 
edgecolor='r', alpha=0.75)
plt.xlabel("x")
plt.ylabel("y")
plt.title("(d) 红色分量直方图")
plt.show()
```
### 图像掩膜直方图和 HS 直方图
```py
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#读取图像
img = cv2.imread('luo.png')
#转换为 RGB 图像
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#设置掩膜
mask = np.zeros(img.shape[:2], np.uint8)
mask[100:300, 100:300] = 255
masked_img = cv2.bitwise_and(img, img, mask=mask)
#图像直方图计算
hist_full = cv2.calcHist([img], [0], None, [256], [0,256]) #通道
[0]-灰度图
#图像直方图计算 (含掩膜)
hist_mask = cv2.calcHist([img], [0], mask, [256], [0,256])
plt.figure(figsize=(8, 6))
#设置字体
matplotlib.rcParams['font.sans-serif']=['SimHei']
#原始图像
plt.subplot(221)
plt.imshow(img_rgb, 'gray')
plt.axis('off')
plt.title("(a) 原始图像")
#绘制掩膜
plt.subplot(222)
plt.imshow(mask, 'gray')
plt.axis('off')
plt.title("(b) 掩膜")
#绘制掩膜设置后的图像
plt.subplot(223)
plt.imshow(masked_img, 'gray')
plt.axis('off')
plt.title("(c) 图像掩膜处理")
#绘制直方图
plt.subplot(224)
plt.plot(hist_full)
plt.plot(hist_mask)
plt.title("(d) 直方图曲线")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```
### 直方图判断白天黑夜
```py
import cv2 
import numpy as np
import matplotlib.pyplot as plt
#函数：判断黑夜或白天
def func_judge(img):
 #获取图像高度和宽度
 height = grayImage.shape[0]
 width = grayImage.shape[1]
 piexs_sum = height * width
 dark_sum = 0 #偏暗像素个数
 dark_prop = 0 #偏暗像素所占比例
 
 for i in range(height):
 for j in range(width):
 if img[i, j] < 50: #阈值为 50
 dark_sum += 1
 #计算比例
 print(dark_sum)
 print(piexs_sum)
 dark_prop = dark_sum * 1.0 / piexs_sum 
 if dark_prop >=0.8:
 print("This picture is dark!", dark_prop)
else:
 print("This picture is bright!", dark_prop)
 
#读取图像
img = cv2.imread('day.png')
#转换为 RGB 图像
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#图像灰度转换
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#计算 256 灰度级的图像直方图
hist = cv2.calcHist([grayImage], [0], None, [256], [0,255])
#判断黑夜或白天
func_judge(grayImage)
#显示原始图像和绘制的直方图
plt.subplot(121), plt.imshow(img_rgb, 'gray'), plt.axis('off'), plt.title("(a)")
plt.subplot(122), plt.plot(hist, color='r'), plt.xlabel("x"), plt.ylabel("y"), 
324
plt.title("(b)")
plt.show()
```
##  图像增强和直方图均衡化处
<img src="img\屏幕截图 2023-05-28 111921.png">

dst = cv2.equalizeHist(src) 
 src 表示输入图像，即原图像

## 局部直方图均衡化和自动色彩均衡化处理
retval = createCLAHE([, clipLimit[, tileGridSize]]) 
 clipLimit 参数表示对比度的大小
 tileGridSize 参数表示每次处理块的大小

```py
# 加载图像
img = cv2.imread('example.jpg')

# 将图像转换为灰度图像
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 创建 CLAHE 对象
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

# 对灰度图像进行 ACE 增强
result = clahe.apply(gray_img)

# 显示结果
cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
```
## 图像平滑
### 图像噪声
#### 椒盐噪声
椒盐噪声也称为脉冲噪声，是图像中经常见到的一种噪声，它是一种随机出现的白点或者黑点，
#### 高斯噪声
高斯噪声是指噪声密度函数服从高斯分布的一类噪声。由于高斯噪声在空间和频域中数学上的易处理性，这种噪声 (也称为正态噪声) 模型经常被用于实践中
### 图像平滑简介
#### 均值滤波
cv.blur(src, ksize, anchor, borderType)

- src：输入图像
- ksize：卷积核的大小
- anchor：默认值 (-1,-1) ，表示核中心
- borderType：边界类型
### 方块滤波
方框滤波又称为盒式滤波，它利用卷积运算对图像邻域的像素值进行平均处理，从而实现消除图像中的噪声。方框滤波和和均值滤波的模糊内核基本一样，区别为是否需要进行均一化处理。
dst = boxFilter(src, depth, ksize[, dst[, anchor[, normalize[, borderType]]]]) 
 src 表示输入图像
 dst 表示输出图像，其大小和类型与输入图像相同
 depth 表示输出图像深度，通常设置为“-1”，表示与原图深度一致
 ksize 表示模糊内核大小，以（宽度，高度）的形式呈现
 normalize 表示是否对目标图像进行归一化处理，默认值为 true
 anchor 表示锚点，即被平滑的那个点，其默认值 Point（-1，-1）表示位于内核的中央，可省略
 borderType 表示边框模式，用于推断图像外部像素的某种边界模式，
默认值为 BORDER_DEFAULT，可省略
#### 高斯滤波
cv2.GaussianBlur(src,ksize,sigmaX,sigmay,borderType)
- src: 输入图像
- ksize:高斯卷积核的大小，注意：卷积核的宽度和高度都应奇数，且可以不同
- sigmaX: 水平方向的标准差
- sigmaY: 垂直方向的标准差，默认值为 0，表示与 sigmaX 相同
- borderType:填充边界类型
#### 中值滤波
中值滤波是一种典型的非线性滤波技术，基本思想是用像素点邻域灰度值的中值来代替该像素点的灰度值。
cv.medianBlur(src, ksize )
#### 双边滤波
双边滤波（Bilateral filter）是由 Tomasi 和 Manduchi 在 1998 年发明的一种各向异性滤波，它一种非线性的图像平滑法结合了图像的空间邻近度和像素值相似度（即空间域和值域）的一种折中处理，从而达到保边去噪的目的。

dst = bilateralFilter(src, d, sigmaColor, sigmaSpace[, dst[, borderType]]) 
 src 表示待处理的输入图像
 dst 表示输出图像，其大小和类型与输入图像相同
 d 表示在过滤期间使用的每个像素邻域的直径。如果这个值我们设其为非
正数，则它会由 sigmaSpace 计算得出
 sigmaColor 表示颜色空间的标准方差。该值越大，表明像素邻域内较
远的颜色会混合在一起，从而产生更大面积的半相等颜色区域
 sigmaSpace 表示坐标空间的标准方差。该值越大，表明像素的颜色足
够接近，从而使得越远的像素会相互影响，更大的区域中相似的颜色获
取相同的颜色，当 d>0，d 指定了邻域大小且与 sigmaSpace 无关。否
则，d 正比于 sigmaSpace
 borderType 表示边框模式，用于推断图像外部像素的某种边界模式，
默认值为 BORDER_DEFAULT，可省略


## 图像锐化边缘检测
### 原理
边缘检测是图像处理和计算机视觉中的基本问题，边缘检测的目的是标识数字图像中亮度变化明显的点

基于搜索：通过寻找图像一阶导数中的最大值来检测边界，然后利用计算结果估计边缘的局部方向，通常采用梯度的方向，并利用此方向找到局部梯度模的最大值，代表算法是 Sobel 算子和 Scharr 算子。
图像锐化处理的目的是为了使图像的边缘、轮廓线以及图像的细节变得清晰，经过平滑的图像变得模糊的根本原因是图像受到了平均或积分运算，因此可以对其进行逆运算，从而使图像变得清晰。
微分运算是求信号的变化率，具有较强高频分量作用。从频率域来考虑，图像模糊的实质是因为其高频分量被衰减，因此可以用高通滤波器来使图像清晰。
### Roberts 算子
Roberts 算子又称为交叉微分算法，它是基于交叉差分的梯度算法，通过局部差分计算检测边缘线条。常用来处理具有陡峭的低噪声图像，当图像边缘接近于正 45 度或负 45 度时，该算法处理效果更理想，其缺点是对边缘的定位不太准确，提取的边缘线条较粗。
dst = filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, borderType]]]]) 
 src 表示输入图像
 dst 表示输出的边缘图，其大小和通道数与输入图像相同
 ddepth 表示目标图像所需的深度
 kernel 表示卷积核，一个单通道浮点型矩阵
 anchor 表示内核的基准点，其默认值为（-1，-1），位于中心位置
 delta 表示在储存目标图像前可选的添加到像素的值，默认值为 0
 borderType 表示边框模式
在进行 Roberts 算子处理之后，还需要调用 convertScaleAbs() 函数计
算绝对值，并将图像转换为 8 位图进行显示。其算法原型如下：
dst = convertScaleAbs(src[, dst[, alpha[, beta]]]) 
 src 表示原数组
 dst 表示输出数组，深度为 8 位
 alpha 表示比例因子
 beta 表示原数组元素按比例缩放后添加的值
### Prewitt 算子
而 Robert 算子的模板为 2×2，故 Prewitt 算子的边缘检测结果在水平方向和垂直方向均比 Robert 算子更加明显。Prewitt 算子适合用来识别噪声较多、灰度渐变的图像，

### Sobel 检测算子
Sobel 边缘检测算法比较简单，实际应用中效率比 canny 边缘检测效率要高，但是边缘不如 Canny 检测的准确，但是很多实际应用的场合，sobel 边缘却是首选，Sobel 算子是高斯平滑与微分操作的结合体，所以其抗噪声能力很强，用途较多。尤其是效率要求较高，而对细纹理不太关心的时候。

#### 方法

Sobel_x_or_y = cv2.Sobel(src, ddepth, dx, dy, dst, ksize, scale, delta, borderType)

- src：传入的图像

- ddepth: 图像的深度

- dx 和 dy: 指求导的阶数，0 表示这个方向上没有求导，取值为 0、1。

- ksize: 是 Sobel 算子的大小，即卷积核的大小，必须为奇数 1、3、5、7，默认为 3。

注意：如果 ksize=-1，就演变成为 3x3 的 Scharr 算子。

- scale：缩放导数的比例常数，默认情况为没有伸缩系数。

- borderType：图像边界的模式，默认值为 cv2.BORDER_DEFAULT。

Sobel 函数求完导数后会有负值，还有会大于 255 的值。而原图像是 uint8，即 8 位无符号数，所以 Sobel 建立的图像位数不够，会有截断。因此要使用 16 位有符号的数据类型，即 cv2.CV_16S。处理完图像后，再使用 cv2.convertScaleAbs() 函数将其转回原来的 uint8 格式，否则图像无法显示。

Scale_abs = cv2.convertScaleAbs(x)  # 格式转换函数
result = cv2.addWeighted(src1, alpha, src2, beta) # 图像混合
### Laplacian 算子
laplacian = cv2.Laplacian(src, ddepth[, dst[, ksize[, scale[, delta[, borderType]]]]])

- Src: 需要处理的图像，
- Ddepth: 图像的深度，-1 表示采用的是原图像相同的深度，目标图像的深度必须大于等于原图像的深度；
- ksize：算子的大小，即卷积核的大小，必须为 1,3,5,7。
### Scharr 算子 
dst = Scharr(src, ddepth, dx, dy[, dst[, scale[, delta[, 
borderType]]]]]) 
 src 表示输入图像
 dst 表示输出的边缘图，其大小和通道数与输入图像相同
 ddepth 表示目标图像所需的深度，针对不同的输入图像，输出目标图像
有不同的深度
 dx 表示 x 方向上的差分阶数，取值 1 或 0
 dy 表示 y 方向上的差分阶数，取值 1 或 0
 scale 表示缩放导数的比例常数，默认情况下没有伸缩系数
 delta 表示将结果存入目标图像之前，添加到结果中的可选增量值
 borderType 表示边框模式，更多详细信息查阅 BorderTypes
### Canny 边缘检测
第一步：使用高斯平滑噪声去除
第二步：计算图像梯度
第三步：非极大值抑制
第四步，利用双阈值方法来确定潜在的边界。
第五步，利用滞后技术来跟踪边界。若某一像素位置和强边界相连的弱边界认为是边界，其他的弱边界则被删除。
在获得梯度的方向和大小之后，对整幅图像进行扫描，去除那些非边界上的点。对每一个像素进行检查，看这个点的梯度是不是周围具有相同梯度方向的点中最大的。
A 点位于图像的边缘，在其梯度变化方向，选择像素点 B 和 C，用来检验 A 点的梯度是否为极大值，若为极大值，则进行保留，否则 A 点被抑制，最终的结果是具有“细边”的二进制图像。
第四步：滞后阈值
我们设置两个阈值：minVal 和 maxVal。当图像的灰度梯度高于 maxVal 时被认为是真的边界，低于 minVal 的边界会被抛弃
##### 应用
canny = cv2.Canny(image, threshold1, threshold2)

- image:灰度图，
- threshold1: minval，较小的阈值将间断的边缘连接起来
- threshold2: maxval，较大的阈值检测图像中明显的边缘
### LOG 算子
LOG 算子综合考虑了对噪声的抑制和对边缘的检测两个方面，并且把 Gauss 平滑滤波器和 Laplacian 锐化滤波器结合了起来，先平滑掉噪声，再进行边缘检测，所以效果会更好。 
# 图像识别及图像处理经典案例
## 图像分割
### 边缘检测分割
image, contours, hierarchy = findContours(image, mode, 
method[, contours[, hierarchy[, offset]]]) 
 image 表示输入图像，即用于寻找轮廓的图像，为 8 位单通道
 contours 表示检测到的轮廓，其函数运行后的结果存在该变量中，每个轮廓存储为一个点向量

 hierarchy 表示输出变量，包含图像的拓扑信息，作为轮廓数量的表示，它包含了许多元素，每个轮廓 contours[i]对应 4 个
hierarchy 元素 hierarchy[i][0]至 hierarchy[i][3]，分别表示后一个轮廓、前一个轮廓、父轮廓、内嵌轮廓的索引编号
 mode 表示轮廓检索模式。cv2.RETR_EXTERNAL 表示只检测外轮廓；cv2.RETR_LIST 表示提取所有轮廓，且检测的轮廓不建立等级关系；cv2.RETR_CCOMP 提取所有轮廓，并建立两个等级的轮廓，上面的一层为外边界，里面一层为内孔的边界信；cv2.RETR_TREE 表示提取所有轮廓，并且建立一个等级树或网状结构的轮廓
 method 表示轮廓的近似方法。cv2.CHAIN_APPROX_NONE
存储所有的轮廓点，相邻的两个点的像素位置差不超过 1，即 max
（abs(x1-x2), abs(y1-y2) ） =1；cv2.CHAIN_APPROX_SIMPLE 压缩水平方向、垂直方向、对角线方向的元素，只保留该方向的终点坐标，例如一个矩阵轮廓只需 4 个点来保存轮廓信息；cv2.CHAIN_APPROX_TC89_L1 和 cv2.CHAIN_APPROX_TC89_KCOS 使 用 Teh-Chinl Chain 近似算法
 offset 表示每个轮廓点的可选偏移量


image = drawContours(image, contours, contourIdx, color[, 
thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]) 
 image 表示目标图像，即所要绘制轮廓的背景图片
 contours 表示所有的输入轮廓，每个轮廓存储为一个点向量
 contourldx 表示轮廓绘制的指示变量，如果为负数表示绘制所有轮廓
 color 表示绘制轮廓的颜色
 thickness 表里绘制轮廓线条的粗细程度，默认值为 1
 lineType 表示线条类型，默认值为 8，可选线包括 8（8 连通线型）、4（4 连通线型）、CV_AA（抗锯齿线型）
 hierarchy 表示可选的层次结构信息
 maxLevel 表示用于绘制轮廓的最大等级，默认值为 INT_MAX
 offset 表示每个轮廓点的可选偏移量
### 基于纹理背景
基于图像纹理信息（颜色）
mask, bgdModel, fgdModel = grabCut(img, mask, rect, 
bgdModel, fgdModel, iterCount[, mode]) 
 image 表示输入图像，为 8 位三通道图像
 mask 表示蒙板图像，输入/输出的 8 位单通道掩码，确定前景区域、背景区域、不确定区域。当模式设置为 GC_INIT_WITH_RECT 时，该掩码由函数初始化
 rect 表示前景对象的矩形坐标，其基本格式为 (x, y, w, h)，分别为左上角坐标和宽度、高度
 bdgModel 表示后台模型使用的数组，通常设置为大小为（1, 65）np.float64 的数组
 fgdModel 表示前台模型使用的数组，通常设置为大小为（1, 65）np.float64 的数组
 iterCount 表示算法运行的迭代次数
 mode 是 cv::GrabCutModes 操 作 模 式 之 一，cv2.GC_INIT_WITH_RECT 或 cv2.GC_INIT_WITH_MASK 表示使用矩阵模式或蒙板模式
### 基于 K-Means 聚类算法的区域分割
retval, bestLabels, centers = kmeans(data, K, bestLabels, 
criteria, attempts, flags[, centers]) 
 data 表示聚类数据，最好是 np.flloat32 类型的 N 维点集
 K 表示聚类类簇数
 bestLabels 表示输出的整数数组，用于存储每个样本的聚类标签索引
 criteria 表示算法终止条件，即最大迭代次数或所需精度。在某些迭代中，一旦每个簇中心的移动小于 criteria.epsilon，算法就会停止
 attempts 表示重复试验 kmeans 算法的次数，算法返回产生最佳紧凑性的标签
 flags 表 示 初 始 中 心 的 选 择，两 种 方 法 是 cv2.KMEANS_PP_CENTERS ; 和 cv2.KMEANS_RANDOM_CENTERS
 centers 表示集群中心的输出矩阵，每个集群中心为一行数据
### 基于均值漂移算法
它是一种无参估计算法，沿着概率梯度的上升方向寻找分布的峰值。Mean Shift 算法先算出当前点的偏移均值，移动该点到其偏移均值，然后以此为新的起始点，继续移动，直到满足一定的条件结束。

图像在色彩层面的平滑滤波，它可以中和色彩分布相近的颜色，平滑色彩细节，侵蚀掉面积较小的颜色区域
dst = pyrMeanShiftFiltering(src, sp, sr[, dst[, maxLevel[, 
termcrit]]]) 
 src 表示输入图像，8 位三通道的彩色图像
 dst 表示输出图像，需同输入图像具有相同的大小和类型
 sp 表示定义漂移物理空间半径的大小
 sr 表示定义漂移色彩空间半径的大小
 maxLevel 表示定义金字塔的最大层数
 termcrit 表示定义的漂移迭代终止条件，可以设置为迭代次数满足终止，迭代目标与中心点偏差满足终止，或者两者的结合
### 基于分水岭算法的图像分割 
分水岭算法是基于拓扑理论的数学形态学的分割方法，灰度图像根据灰度值把像素之间的关系看成山峰和山谷的关系，高亮度（灰度值高）的地方是山峰，低亮度（灰度值低）的地方是山谷
markers = watershed(image, markers) 
 image 表示输入图像，需为 8 位三通道的彩色图像
 markers 表示用于存储函数调用之后的运算结果，输入/输出 32 位单通道图像的标记结构，输出结果需和输入图像的尺寸和类型一致。
## 图像变换
### 傅里叶变换的理解

傅里叶变换是由法国的一位数学家 Joseph Fourier 在 18 世纪提出来的，他认为：**任何连续周期的信号都可以由一组适当的正弦曲线组合而成**。
**正弦波输入至任何线性系统中，不会产生新的频率成分，输出的仍是正弦波，改变的仅仅是幅值和相位**

### 傅里叶变换中相关概念

#### 时域和频域

傅里叶变换是将难以处理的时域信号转换成易于分析的频域信号
**时域**：时域是真实的世界，是唯一存在的域。从我们出生开始，所接触的这个世界就是随着时间在变化的，如花开花落，四季变换，生老病死等。以时间作为参照来分析动态世界的方法我们称其为时域分析。

**频域**：**频域它不是真实的，而是一个数学构造。**频域是一个遵循特定规则的数学范畴，也被一些学者称为上帝视角。结合上面对时域的理解，如果时域是运动永不停止的，那么频域就是静止的。
正弦波是频域中唯一存在的波形，这是频域中最重要的规则，**即正弦波是对频域的描述，因为频域中的任何波形都可用正弦波合成**。
####  傅里叶变换在图像中的应用    
$$
F(u,v) = \sum_{x=0}^{M-1}\sum_{y=0}^{N-1}f(x,y)e^{-i2\pi(\frac{ux}M+\frac{vy}N)}
$$

逆变换由下式给出：
$$
f(x,y) = \sum_{x=0}^{M-1}\sum_{y=0}^{N-1}F(u,v)e^{i2\pi(\frac{ux}M+\frac{vy}N)}
$$

dst = cv2.dft(src, dst=None, flags=None, 
nonzeroRows=None) 
 src 表示输入图像，需要通过 np.float32 转换格式
 dst 表示输出图像，包括输出大小和尺寸
 flags 表示转换标记，其中 DFT _INVERSE 执行反向一维或二维转换，而不是默认的正向转换；DFT _SCALE 表示缩放结果，由阵列元素的数量除以它；DFT _ROWS 执行正向或反向变换输入矩阵的每个单独的行，该标志可以同时转换多个矢量，并可用于减少开销以执行 3D 和更高维度的转换等；DFT _COMPLEX_OUTPUT 执行 1D 或 2D 实数组的正向转换，这是最快的选择，默认功能；DFT _REAL_OUTPUT 执行一维或二维复数阵列的逆变换，结果通常是相同大小的复数数组，但如果输入数组具有共轭复数对称性，则输出为真实数组
 nonzeroRows 表 示 当 参 数 不 为 零 时，函 数 假 定 只 有 nonzeroRows 输入数组的第一行（未设置）或者只有输出数组的第一个（设置）包含非零，因此函数可以处理其余的行更有效率，并节省一些时间；这种技术对计算阵列互相关或使用 DFT 卷积非常有用


####  在 opencv 中实现图像的傅里叶变换

在 OPenCV 中实现图像的傅里叶变换，使用的是：

正变换：

```python
dft = cv2.dft(src, dst=None)
```

参数：

- src: 输入图像，要转换成 np.float32 格式
- dst:参数是可选的，决定输出数组的大小。默认输出数组的大小和输入图像大小一样。如果输出结果比输入图像大，输入图像就需要在进行变换前补 0。如果输出结果比输入图像小的话，输入图像就会被切割。

返回：

- dft: 傅里叶变换后的结果，有两个通道，第一个通道是结果的实数部分，第二个通道是结果的虚数部分。我们需要在此基础上计算傅里叶变换的频谱和相位。

逆变换：

```python 
img = cv.idft(dft)
```

参数：

- dft: 图像的频域表示

返回：

- img: 图像的空域表示

实现：

#### 频域滤波
**高通滤波器**
高通滤波器是指通过高频的滤波器，衰减低频而通过高频，常用于增强尖锐的细节，但会导致图像的对比度会降低。
**低通滤波器**
低通滤波器是指通过低频的滤波器，衰减高频而通过低频，常用于模糊图像。低通滤波器与高通滤波器相反，当一个像素与周围像素的插值小于一个特定值时，平滑该像素的亮度，常用于去燥和模糊化处理。


#### 带通和带阻滤波器
们把高通和低通的一部分结合在模板中就形成了带通滤波器，它容许一定频率范围信号通过，但减弱 (或减少) 频率低于於下限截止频率和高于上限截止频率的信号的通过，如下图所示：

还是以理想的带通滤波器演示如下，将构建的滤波的代码修改如下：

```py
rows,cols = img.shape
mask1 = np.ones((rows,cols,2),np.uint8)
mask1[int(rows/2)-8:int(rows/2)+8,int(cols/2)-8:int(cols/2)+8] = 0
mask2 = np.zeros((rows,cols,2),np.uint8)
mask2[int(rows/2)-80:int(rows/2)+80,int(cols/2)-80:int(cols/2)+80] = 1
mask = mask1*mask2
```
### 霍夫变换
霍夫变换（Hough Transform）是一种特征检测（Feature Extraction），被广泛应用在图像分析、计算机视觉以及数位影像处理。

lines = HoughLines(image, rho, theta, threshold[, lines[, srn[, 
stn[, min_theta[, max_theta]]]]]) 
 image 表示输入的二值图像
 lines 表示经过霍夫变换检测到直线的输出矢量，每条直线为 (r,θ)
 rho 表示以像素为单位的累加器的距离精度
 theta 表示以弧度为单位的累加器角度精度
 threshold 表示累加平面的阈值参数，识别某部分为图中的一条直线时它在累加平面中必须达到的值，大于该值线段才能被检测返回
 srn 表示多尺度霍夫变换中 rho 的除数距离，默认值为 0。粗略的累加器进步尺寸为 rho，而精确的累加器进步尺寸为 rho/srn
 stn 表示多尺度霍夫变换中距离精度 theta 的除数，默认值为 0,。如果 srn 和 stn 同时为 0，使用标准霍夫变换
 min_theta 表示标准和多尺度的霍夫变换中检查线条的最小角度。必须介于 0 和 max_theta 之间
 max_theta 表示标准和多尺度的霍夫变换中要检查线条的最大角度。必须介于 min_theta 和π之间
## 图像分类
### 基于朴素贝叶斯
朴素贝叶斯分类（Naive Bayes Classifier）发源于古典数学理论，利用 Bayes 定理来预测一个未知类别的样本属于各个类别的可能性，选择其中可能性最大的一个类别作为该样本的最终类别。
### 基于 KNN 的图像分类
K 最近邻分类（K-Nearest Neighbor Classifier）算法是一种基于实例的分类方法，是数据挖掘分类技术中最简单常用的方法之一。
### 卷积神经网络
## 图像特效
### 毛玻璃特效
实现过程：该特效是用图像邻域内随机一个像素点的颜色来替代当前像素点颜色的过程，从而为图像增加一个毛玻璃模糊的特效。
```py
import cv2
import numpy as np
#读取原始图像
src = cv2.imread('luo.png')
#新建目标图像
dst = np.zeros_like(src)
#获取图像行和列
rows, cols = src.shape[:2]
#定义偏移量和随机数
offsets = 5
random_num = 0
#毛玻璃效果：像素点邻域内随机像素点的颜色替代当前像素点的颜色
for y in range(rows - offsets):
 for x in range(cols - offsets):
 random_num = np.random.randint(0,offsets)
 dst[y,x] = src[y + random_num,x + random_num]
#显示图像
cv2.imshow('src',src)
cv2.imshow('dst',dst)
cv2.waitKey()
cv2.destroyAllWindows()
```
### 浮雕特效
dst = filter2D(src, ddepth, kernel[, dst[, anchor[, delta[, 
borderType]]]]) 
 src 表示输入图像
 dst 表示输出的边缘图，其大小和通道数与输入图像相同
 ddepth 表示目标图像所需的深度
 kernel 表示卷积核，一个单通道浮点型矩阵
 anchor 表示内核的基准点，其默认值为（-1，-1），位于中心位置
 delta 表示在储存目标图像前可选的添加到像素的值，默认值为 0
 borderType 表示边框模式
### 油漆特效
图像油漆特效类似于油漆染色后的轮廓图形，
```py
import cv2
import numpy as np
#读取原始图像
src = cv2.imread('luo.png')
#图像灰度处理
gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
#自定义卷积核
kernel = np.array([[-1,-1,-1],[-1,10,-1],[-1,-1,-1]])
#图像浮雕效果
output = cv2.filter2D(gray, -1, kernel)
#显示图像
cv2.imshow('Original Image', src)
cv2.imshow('Emboss_1',output)
cv2.waitKey()
cv2.destroyAllWindows()
```
### 模糊特效

### 素描
```py
import cv2
import numpy as np
#读取原始图像
img = cv2.imread('luo.png')
#图像灰度处理
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#高斯滤波降噪
gaussian = cv2.GaussianBlur(gray, (5,5), 0)
#Canny 算子
canny = cv2.Canny(gaussian, 50, 150)
#阈值化处理
ret, result = cv2.threshold(canny, 100, 255, 
cv2.THRESH_BINARY_INV)
#显示图像
cv2.imshow('src', img)
cv2.imshow('result', result)
cv2.waitKey()
cv2.destroyAllWindows()
```
## 图像去雾
### ACE
### 暗通道
## 文字图像区域定位及提取分析
<img src="img\屏幕截图 2023-05-31 092207.png">

## 人脸检测及视频人脸动态识别 

## 颜色追踪

# 图像特征提取和描述
## Harris 和 Shi-Tomas 算法

### Harris 角点检测
Harris 角点检测的思想是通过图像的局部的小窗口观察图像，角点的特征是窗口沿任意方向移动都会导致图像灰度的明显变化
<img src="./img/屏幕截图 2023-03-31 171004.png">

### 实现
dst=cv.cornerHarris(src, blockSize, ksize, k)

- img：数据类型为 ﬂoat32 的输入图像。

- blockSize：角点检测中要考虑的邻域大小。

- ksize：sobel 求导使用的核大小

- k：角点检测方程中的自由参数，取值参数为 [0.04，0.06].

优点：

 - 旋转不变性，椭圆转过一定角度但是其形状保持不变（特征值保持不变）
 - 对于图像灰度的仿射变化具有部分的不变性，由于仅仅使用了图像的一介导数，对于图像灰度平移变化不变；对于图像灰度尺度变化不变
缺点：
 - 对尺度很敏感，不具备几何尺度不变性。
 - 提取的角点是像素级的
### Shi-Tomasi 角点检测
#### 原理
Shi-Tomasi 算法是对 Harris 角点检测算法的改进，一般会比 Harris 算法得到更好的角点。Harris 算法的角点响应函数是将矩阵 M 的行列式值与 M 的迹相减，利用差值判断是否为角点。后来 Shi 和 Tomasi 提出改进的方法是，若矩阵 M 的两个特征值中较小的一个大于阈值，则认为他是角点.
corners = cv2.goodFeaturesToTrack ( image, maxcorners, qualityLevel, minDistance )

- Image: 输入灰度图像
- maxCorners : 获取角点数的数目。
- qualityLevel：该参数指出最低可接受的角点质量水平，在 0-1 之间。
- minDistance：角点之间最小的欧式距离，避免得到相邻特征点。


Corners: 搜索到的角点，在这里所有低于质量水平的角点被排除掉，然后把合格的角点按质量排序，然后将质量较好的角点附近（小于最小欧式距离）的角点删掉，最后找到 maxCorners 个角点返回。

## SIFT/SURF算法
### SIFT/SURF算法
#### SIFT 原理
这两种算法具有旋转不变性，但不具有尺度不变性，以下图为例，在左侧小图中可以检测到角点，但是图像被放大后，在使用同样的窗口，就检测不到角点了。

1. 尺度空间极值检测：搜索所有尺度上的图像位置。通过高斯差分函数来识别潜在的对于尺度和旋转不变的关键点。
2. 关键点定位：在每个候选的位置上，通过一个拟合精细的模型来确定位置和尺度。关键点的选择依据于它们的稳定程度。
3. 关键点方向确定：基于图像局部的梯度方向，分配给每个关键点位置一个或多个方向。所有后面的对图像数据的操作都相对于关键点的方向、尺度和位置进行变换，从而保证了对于这些变换的不变性。
4. 关键点描述：在每个关键点周围的邻域内，在选定的尺度上测量图像局部的梯度。这些梯度作为关键点的描述符，它允许比较大的局部形状的变形或光照变化。
### SURF 原理
006 年 Bay 提出了 SURF 算法，是 SIFT 算法的增强版，它的计算量小，运算速度快，提取的特征与 SIFT 几乎相同.
sift = cv.xfeatures2d.SIFT_create()
kp,des = sift.detectAndCompute(gray,None)
cv.drawKeypoints(image, keypoints, outputimage, color, flags)

- image: 原始图像
- keypoints：关键点信息，将其绘制在图像上
- outputimage：输出图片，可以是原始图像
- color：颜色设置，通过修改（b,g,r）的值，更改画笔的颜色，b=蓝色，g=绿色，r=红色。
- flags：绘图功能的标识设置
   1. cv2.DRAW_MATCHES_FLAGS_DEFAULT：创建输出图像矩阵，使用现存的输出图像绘制匹配对和特征点，对每一个关键点只绘制中间点
   2. cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG：不创建输出图像矩阵，而是在输出图像上绘制匹配对
   3. cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS：对每一个特征点绘制带大小和方向的关键点图形
   4. cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS：单点的特征点不被绘制



## Fast 和 ORB 算法
### Fast 算法

####  原理

**FAST** (全称 Features from accelerated segment test) 是一种用于角点检测的算法，该算法的原理是取图像中检测点，以该点为圆心的周围邻域内像素点判断检测点是否为角点，通俗的讲就是**若一个像素周围有一定数量的像素与该点像素值不同，则认为其为角点**。

##### **FAST 算法的基本流程**

1. 在图像中选取一个像素点 p，来判断它是不是关键点。$$I_p$$等于像素点 p 的灰度值。

2. 以 r 为半径画圆，覆盖 p 点周围的 M 个像素，通常情狂下，设置 r=3，则 M=16，

3. 设置一个阈值 t，如果在这 16 个像素点中存在 n 个连续像素点的灰度值都高于$$I_p + t$$，或者低于$$I_p - t$$，那么像素点 p 就被认为是一个角点。

4. 由于在检测特征点时是需要对图像中所有的像素点进行检测，然而图像中的绝大多数点都不是特征点，如果对每个像素点都进行上述的检测过程，那显然会浪费许多时间，因此采用一种进行**非特征点判别**的方法：首先对候选点的周围每个 90 度的点：1，9，5，13 进行测试（先测试 1 和 19, 如果它们符合阈值要求再测试 5 和 13）。如果 p 是角点，那么这四个点中至少有 3 个要符合阈值要求，否则直接剔除。对保留下来的点再继续进行测试（是否有 12 的点符合阈值要求）。 

虽然这个检测器的效率很高，但它有以下几条缺点：

- 获得的候选点比较多
- 特征点的选取不是最优的，因为它的效果取决与要解决的问题和角点的分布情况。
- 进行非特征点判别时大量的点被丢弃
- 检测到的很多特征点都是相邻的

前 3 个问题可以通过机器学习的方法解决，最后一个问题可以使用非最大值抑制的方法解决。

##### **机器学习的角点检测器**

1. 选择一组训练图片（最好是跟最后应用相关的图片）

2. 使用 FAST 算法找出每幅图像的特征点，对图像中的每一个特征点，将其周围的 16 个像素存储构成一个向量 P。

3. 每一个特征点的 16 像素点都属于下列三类中的一种


4. 根据这些像素点的分类，特征向量 P 也被分为 3 个子集：Pd，Ps，Pb，

5. 定义一个新的布尔变量$$K_p$$，如果 p 是角点就设置为 Ture，如果不是就设置为 False。

6. 利用特征值向量 p，目标值是$K_p$，训练 ID3 树（决策树分类器）。

7. 将构建好的决策树运用于其他图像的快速的检测。

##### **非极大值抑制**

**在筛选出来的候选角点中有很多是紧挨在一起的，需要通过非极大值抑制来消除这种影响。**

为所有的候选角点都确定一个打分函数$$V $$ ， $$V $$的值可这样计算：先分别计算$$I_p$$与圆上 16 个点的像素值差值，取绝对值，再将这 16 个绝对值相加，就得到了$$V $$的值
$$
V = \sum_{i}^{16}|I_p-I_i|
$$
最后比较毗邻候选角点的 V 值，把 V 值较小的候选角点 pass 掉。

FAST 算法的思想与我们对角点的直观认识非常接近，化繁为简。FAST 算法比其它角点的检测算法快，但是在噪声较高时不够稳定，这需要设置合适的阈值。

#### 实现

OpenCV 中的 FAST 检测算法是用传统方法实现的，


```python
fast = =cv.FastFeatureDetector_create( threshold, nonmaxSuppression)
```

参数：

- threshold：阈值 t，有默认值 10
- nonmaxSuppression：是否进行非极大值抑制，默认值 True

返回：

- Fast：创建的 FastFeatureDetector 对象

利用 fast.detect 检测关键点，没有对应的关键点描述

```python
kp = fast.detect(grayImg, None)
```

参数：

- gray: 进行关键点检测的图像，注意是灰度图像

返回：

- kp: 关键点信息，包括位置，尺度，方向信息

将关键点检测结果绘制在图像上，与在 sift 中是一样的

```python
cv.drawKeypoints(image, keypoints, outputimage, color, flags)
```


```python
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
# 1 读取图像
img = cv.imread('./image/tv.jpg')
# 2 Fast 角点检测
# 2.1 创建一个 Fast 对象，传入阈值，注意：可以处理彩色空间图像
fast = cv.FastFeatureDetector_create(threshold=30)

# 2.2 检测图像上的关键点
kp = fast.detect(img,None)
# 2.3 在图像上绘制关键点
img2 = cv.drawKeypoints(img, kp, None, color=(0,0,255))

# 2.4 输出默认参数
print( "Threshold: {}".format(fast.getThreshold()) )
print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
print( "neighborhood: {}".format(fast.getType()) )
print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )


# 2.5 关闭非极大值抑制
fast.setNonmaxSuppression(0)
kp = fast.detect(img,None)

print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
# 2.6 绘制为进行非极大值抑制的结果
img3 = cv.drawKeypoints(img, kp, None, color=(0,0,255))

# 3 绘制图像
fig,axes=plt.subplots(nrows=1,ncols=2,figsize=(10,8),dpi=100)
axes[0].imshow(img2[:,:,::-1])
axes[0].set_title("加入非极大值抑制")
axes[1].imshow(img3[:,:,::-1])
axes[1].set_title("未加入非极大值抑制")
plt.show()
```

### ORB 算法

#### 原理
**ORB 算法流程**

ORB 算法结合了 Fast 和 Brief 算法，提出了构造金字塔，为 Fast 特征点添加了方向，从而使得关键点具有了尺度不变性和旋转不变性。具体流程描述如下：

- 构造尺度金字塔，金字塔共有 n 层，与 SIFT 不同的是，每一层仅有一幅图像。第 s 层的尺度为：
```py
$$
\sigma_s=\sigma_0^s
$$
$$\sigma_0$$是初始尺度，默认为1.2，原图在第0层。

第s层图像的大小：
$$
SIZE = (H*\frac{1}{\sigma_s})\times(W*\frac{1}{\sigma_s})
$$
```

- 在不同的尺度上利用 Fast 算法检测特征点，采用 Harris 角点响应函数，根据角点的响应值排序，选取前 N 个特征点，作为本尺度的特征点。

- 计算特征点的主方向，计算以特征点为圆心半径为 r 的圆形邻域内的灰度质心位置，将从特征点位置到质心位置的方向做特征点的主方向。

计算方法如下：
```py
$$
m_{pq}=\sum_{x,y}x^py^qI(x,y)
$$
质心位置：
$$
C=(\frac{m_{10}}{m_{00}},\frac{m_{01}}{m_{10}})
$$
主方向：
$$
\theta = arctan(m_{01},m_{10})
$$
```

## BRIEF 算法

###### 	BRIEF 是一种特征描述子提取算法，并非特征点的提取算法，一种生成**二值**化描述子的算法，不提取代价低，匹配只需要使用简单的汉明距离 (Hamming Distance) 利用比特之间的异或操作就可以完成。因此，时间代价低，空间代价低，效果还挺好是最大的优点。

**算法的步骤介绍如下**：

1. **图像滤波**：原始图像中存在噪声时，会对结果产生影响，所以需要对图像进行滤波，去除部分噪声。

2. **选取点对**：以特征点为中心，取 S*S 的邻域窗口，在窗口内随机选取 N 组点对，一般 N=128,256,512，默认是 256，关于如何选取随机点对，提供了五种形式，结果如下图所示：

   -  x,y 方向平均分布采样

   - x,y 均服从 Gauss(0,S^2/25) 各向同性采样

   -  x 服从 Gauss(0,S^2/25)，y 服从 Gauss(0,S^2/100) 采样

   -  x,y 从网格中随机获取

   -  x 一直在 (0,0)，y 从网格中随机选取

   图中一条线段的两个端点就是一组点对，其中第二种方法的结果比较好。

3. **构建描述符**：假设 x,y 是某个点对的两个端点，p(x),p(y) 是两点对应的像素值，则有：
   $$
   t(x,y)=\begin{cases}1	&if p(x)>p(y)\\
   0&	else\end{cases}
   $$
   对每一个点对都进行上述的二进制赋值，形成 BRIEF 的关键点的描述特征向量，该向量一般为 128-512 位的字符串，其中仅包含 1 和 0，如下图所示：



**实例化 ORB**

```python
orb = cv.xfeatures2d.orb_create(nfeatures)
```

参数：

- nfeatures: 特征点的最大数量

**利用 orb.detectAndCompute() 检测关键点并计算**

```python
kp,des = orb.detectAndCompute(gray,None)
```

参数：

- gray: 进行关键点检测的图像，注意是灰度图像

返回：

- kp: 关键点信息，包括位置，尺度，方向信息
- des: 关键点描述符，每个关键点 BRIEF 特征向量，二进制字符串，

**将关键点检测结果绘制在图像上**

```python
cv.drawKeypoints(image, keypoints, outputimage, color, flags)
```

**示例：**

```python
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
# 1 图像读取
img = cv.imread('./image/tv.jpg')

# 2 ORB 角点检测
# 2.1 实例化 ORB 对象
orb = cv.ORB_create(nfeatures=500)
# 2.2 检测关键点，并计算特征描述符
kp,des = orb.detectAndCompute(img,None)

print(des.shape)

# 3 将关键点绘制在图像上
img2 = cv.drawKeypoints(img, kp, None, color=(0,0,255), flags=0)

# 4. 绘制图像
plt.figure(figsize=(10,8),dpi=100)
plt.imshow(img2[:,:,::-1])
plt.xticks([]), plt.yticks([])
plt.show()
```


# 视频操作
## 视频读写
### 从文件中读取视频并播放
cap = cv.VideoCapture(filepath)
**修改视频的属性信息**

cap.set(propId，value)
参数：

proid: 属性的索引，与上面的表格相对应
value: 修改后的属性值

判断图像是否读取成功

isornot = cap.isOpened()
若读取成功则返回 true，否则返回 False
获取视频的一帧图像

ret, frame = cap.read()
参数：

ret: 若获取成功返回 True，获取失败，返回 False
Frame: 获取到的某一帧的图像
调用 cv.imshow() 显示图像，在显示图像时使用 cv.waitkey() 设置适当的持续时间，如果太低视频会播放的非常快，如果太高就会播放的非常慢，通常情况下我们设置 25ms 就可以了。

最后，调用 cap.realease() 将视频释放掉

```py

import numpy as np
import cv2 as cv
# 1.获取视频对象
cap = cv.VideoCapture('DOG.wmv')
# 2.判断是否读取成功
while(cap.isOpened()):
    # 3.获取每一帧图像
    ret, frame = cap.read()
    # 4. 获取成功显示图像
    if ret == True:
        cv.imshow('frame',frame)
    # 5.每一帧间隔为 25ms
    if cv.waitKey(25) & 0xFF == ord('q'):
        break
# 6.释放视频对象
cap.release()
cv.destoryAllwindows()
```
#### 保存视频
在 OpenCV 中我们保存视频使用的是 VedioWriter 对象，在其中指定输出文件的名称，如下所示：

**创建视频写入的对象**
out = cv2.VideoWriter(filename,fourcc, fps, frameSize)
参数：

- filename：视频保存的位置
- fourcc：指定视频编解码器的 4 字节代码
- fps：帧率
- frameSize：帧大小

retval = cv2.VideoWriter_fourcc( c1, c2, c3, c4 )
参数：

 - c1,c2,c3,c4: 是视频编解码器的 4 字节代码，在 fourcc.org 中找到可用代码列表，与平台紧密相关，常用的有：

 - 在 Windows 中：DIVX（.avi）
 - 在 OS 中：MJPG（.mp4），DIVX（.avi），X264（.mkv）。
利用 cap.read() 获取视频中的每一帧图像，并使用 out.write() 将某一帧图像写入视频中。

使用 cap.release() 和 out.release() 释放资源。

示例：
```py
import cv2 as cv
import numpy as np

# 1. 读取视频
cap = cv.VideoCapture("DOG.wmv")

# 2. 获取图像的属性（宽和高，）,并将其转换为整数
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# 3. 创建保存视频的对象，设置编码格式，帧率，图像的宽高等
out = cv.VideoWriter('outpy.avi',cv.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
while(True):
    # 4.获取视频中的每一帧图像
    ret, frame = cap.read()
    if ret == True: 
        # 5.将每一帧图像写入到输出文件中
        out.write(frame)
    else:
        break 

# 6.释放资源
cap.release()
out.release()
cv.destroyAllWindows()
```
## 视频追踪
### meanshift
#### 原理
meanshift 算法的原理很简单。假设你有一堆点集，还有一个小的窗口，这个窗口可能是圆形的，现在你可能要移动这个窗口到点集密度最大的区域当中。

首先在图像上选定一个目标区域

计算选定区域的直方图分布，一般是 HSV 色彩空间的直方图。

对下一帧图像 b 同样计算直方图分布。

计算图像 b 当中与选定区域直方图分布最为相似的区域，使用 meanshift 算法将选定区域沿着最为相似的部分进行移动，直到找到最相似的区域，便完成了在图像 b 中的目标追踪。

重复 3 到 4 的过程，就完成整个视频目标追踪。

通常情况下我们使用直方图反向投影得到的图像和第一帧目标对象的起始位置，当目标对象的移动会反映到直方图反向投影图中，meanshift 算法就把我们的窗口移动到反向投影图像中灰度密度最大的区域了
####   实现
cv.meanShift(probImage, window, criteria)
probImage: ROI 区域，即目标的直方图的反向投影

window：初始搜索窗口，就是定义 ROI 的 rect

criteria: 确定窗口搜索停止的准则，主要有迭代次数达到设置的最大值，窗口中心的漂移值大于某个设定的限值等。


probImage: ROI 区域，即目标的直方图的反向投影

window：初始搜索窗口，就是定义 ROI 的 rect

criteria: 确定窗口搜索停止的准则，主要有迭代次数达到设置的最大值，窗口中心的漂移值大于某个设定的限值等。

```py
import numpy as np
import cv2 as cv
# 1.获取图像
cap = cv.VideoCapture('DOG.wmv')

# 2.获取第一帧图像，并指定目标位置
ret,frame = cap.read()
# 2.1 目标位置（行，高，列，宽）
r,h,c,w = 197,141,0,208  
track_window = (c,r,w,h)
# 2.2 指定目标的感兴趣区域
roi = frame[r:r+h, c:c+w]

# 3. 计算直方图
# 3.1 转换色彩空间（HSV）
hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
# 3.2 去除低亮度的值
# mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
# 3.3 计算直方图
roi_hist = cv.calcHist([hsv_roi],[0],None,[180],[0,180])
# 3.4 归一化
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# 4. 目标追踪
# 4.1 设置窗口搜索终止条件：最大迭代次数，窗口中心漂移最小值
term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

while(True):
    # 4.2 获取每一帧图像
    ret ,frame = cap.read()
    if ret == True:
        # 4.3 计算直方图的反向投影
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # 4.4 进行 meanshift 追踪
        ret, track_window = cv.meanShift(dst, track_window, term_crit)

        # 4.5 将追踪的位置绘制在视频上，并进行显示
        x,y,w,h = track_window
        img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cv.imshow('frame',img2)

        if cv.waitKey(60) & 0xFF == ord('q'):
            break        
    else:
        break
# 5. 资源释放        
cap.release()
cv.destroyAllWindows()
```
#### Camshift
CamShift 算法全称是“Continuously Adaptive Mean-Shift”（连续自适应 MeanShift 算法），是对 MeanShift 算法的改进算法，可随着跟踪目标的大小变化实时调整搜索窗口的大小，具有较好的跟踪效果。
# 人脸案例
##  基础
首先需要大量的正样本图像（面部图像）和负样本图像（不含面部的图像）来训练分类器。我们需要从其中提取特征。下图中的 Haar 特征会被使用，就像我们的卷积核，每一个特征是一 个值，这个值等于黑色矩形中的像素值之后减去白色矩形中的像素值之和。
<img src="/img/屏幕截图 2023-03-31 210427.png">

Haar 特征值反映了图像的灰度变化情况。例如：脸部的一些特征能由矩形特征简单的描述，眼睛要比脸颊颜色要深，鼻梁两侧比鼻梁颜色要深，嘴巴比周围颜色要深等。

Haar 特征可用于于图像任意位置，大小也可以任意改变，所以矩形特征值是矩形模版类别、矩形位置和矩形大小这三个因素的函数。故类别、大小和位置的变化，使得很小的检测窗口含有非常多的矩形特征。