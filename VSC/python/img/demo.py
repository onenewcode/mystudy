import cv2
import numpy  as np
#读取图片
img = cv2.imread(r"C:\Users\ztf\OneDrive\Desktop\mystudy\VSC\python\img\wallhaven.jpg")#相对路径指的是“相对于.exe文件的路径”
#显示图像
# cv2.imshow("Demo", img)
#等待显示
# cv2.waitKey(0)
# cv2.destroyAllWindows()

print(type(img))
#Numpy 读取像素
print(img.item(78, 100, 0))
print(img.item(78, 100, 1))
print(img.item(78, 100, 2))
#Numpy 修改像素
img.itemset((78, 100, 0), 100)
print(img.max(),img.min())
