# 数据操作
## pytorch基础操作
### 自定义数据集
```py
import os
import pandas as pd
from torchvision.io import read_image
class CustomImageDataset(Dataset):
    # 在实例化数据集对象时，__init__函数运行一次。我们初始化目录，目录中包括图像文件、标注文件和变换
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform
    # 返回我们数据集中的样本数。
    def __len__(self):
        return len(self.img_labels)
    # 在给定的索引idx处加载并返回数据集中的一个样本。基于索引，它确定图像在硬盘上的位置，使用read_image将其变换为tensor，从self.img_labels中的csv数据中获取相应的标签，对其调用变换函数（如果适用），并在一个元组中返回tensor图像和相应标签。
    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
```

## 数据预处理
# 线性神经网络
# 多层感知机
# 深度学习计算
# 卷积神经网络
# 现代神经网络
# 循环神经网络
# 现代循环神经网络
# 注意力机制