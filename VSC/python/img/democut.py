import cv2 
import matplotlib.pyplot as plt
import numpy as np 
#读取图片
img = cv2.imread(r"C:\Users\ztf\OneDrive\Desktop\mystudy\VSC\python\img\wallhaven.jpg")#相对路径指的是“相对于.exe文件的路径”
#图像各像素减 50
m = np.ones(img.shape, dtype="uint8")*50
#OpenCV 减法运算
result = cv2.subtract(img, m)
#显示图像
# cv2.imshow("original", img)
# cv2.imshow("result", result)
#等待显示
# cv2.waitKey(0)
# cv2.destroyAllWindows()
images=[img,result]
titles=["1","2"]
for i in range(2):
 plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
 plt.title(titles[i])
 plt.xticks([]),plt.yticks([])
plt.show()
