# minikube
## 安装
### 乌班图安装
科学上网是我你们安装的前提。
```shell
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
## 测试
首先我已将安装了docker，我们接下来以docker为虚拟化环境来运行minikube。

然后运行以下命令来测试运行。
```shell
minikube start --driver=docker --force
```
第一次运行会比较慢，因为我们第一次会下载一个比较大的镜像。
