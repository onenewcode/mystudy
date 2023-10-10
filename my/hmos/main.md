# OpenHarmony docker环境搭建
要求一台安装ubuntu的虚拟机,vscode软件
## 安装docker
在 Ubuntu 上安装 Docker 非常直接。我们将会启用 Docker 软件源，导入 GPG key，并且安装软件包。

首先，更新软件包索引，并且安装必要的依赖软件，来添加一个新的 HTTPS 软件源：
```shell
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

使用下面的 curl 导入源仓库的 GPG key：
```ssh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
将 Docker APT 软件源添加到你的系统：
```shell
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

现在，Docker 软件源被启用了，你可以安装软件源中任何可用的 Docker 版本。

01.想要安装 Docker 最新版本，运行下面的命令。如果你想安装指定版本，跳过这个步骤，并且跳到下一步。
```shell
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

02.想要安装指定版本，首先列出 Docker 软件源中所有可用的版本：
```ssh
sudo apt update
apt list -a docker-ce
```

可用的 Docker 版本将会在第二列显示。

docker-ce/focal 5:19.03.9~3-0~ubuntu-focal amd64
通过在软件包名后面添加版本=\<VERSION\>来安装指定版本：

sudo apt install docker-ce=\<VERSION\> docker-ce-cli=\<VERSION\> containerd.io
一旦安装完成，Docker 服务将会自动启动。你可以输入下面的命令，验证它：
sudo systemctl status docker
输出将会类似下面这样：
```shell
● docker.service - Docker Application Container Engine
     Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2020-05-21 14:47:34 UTC; 42s ago
...
```

当一个新的 Docker 发布时，你可以使用标准的sudo apt update && sudo apt upgrade流程来升级 Docker 软件包。
## 拉取镜像
运行 Docker 软件,打开 CMD 命令行或者 PowerShell 终端,使用指令下载
docker 官方镜像:

```shell
docker pull swr.cn-south-1.myhuaweicloud.com/openharmony-docker/openharmony-docker:1.0.0
```

等待下载完成之后,使用 docker images 可以查看到已下载的 docker 镜像
此时镜像名称太长不方便使用,可以使用重命名操作对镜像重命名:
```shell
docker image tag swr.cn-south-1.myhuaweicloud.com/openharmony-docker/openharmony-docker:1.0.0 openharmony-docker:1.0.0
```
此时使用 docker images 再次查看镜像,发现多出一个名为
openharmony-docker:1.0.0 的镜像
可以执行 
```shell
docker rmi swr.cn-south-1.myhuaweicloud.com/openharmony-docker/openharmony-docker:1.0.0
```
删除旧的镜像:
执行 
```shell
docker run -it openharmony-docker:1.0.0 
```
指令可以运行镜像可以看到系统直接进入到了/home/openharmony,但是此时仅是容器运行成功了,还没有代码,无法完成开发,接下来需要获取代码
## OpenHarmony 代码获取
### 通过git(不推荐,有时会卡死)
首先要设置git用户名和邮箱,否则拉去代码时会报错
```shell
git config --global user.name "Your Name"
git config --global user.email "youremail@yourdomain.com"
```
拉去代码
```shell
repo init -u git@gitee.com:openharmony/manifest.git -b OpenHarmony-3.2-Release -g ohos:mini
repo sync -c
repo forall -c 'git lfs pull'
```
### 通过http
```shell
repo init -u https://gitee.com/openharmony/manifest.git -b OpenHarmony-3.2-Release -g ohos:mini
repo sync -c
repo forall -c 'git lfs pull'
```


