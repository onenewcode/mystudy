import keras
from keras.datasets import mnist
(train_images,train_labels),(test_images,test_labels) = mnist.load_data() #加载数据
print('shape of train images is ',train_images.shape)
print('shape of train labels is ',train_labels.shape)
print('train labels is ',train_labels)
print('shape of test images is ',test_images.shape)
print('shape of test labels is',test_labels.shape)
print('test labels is',test_labels)