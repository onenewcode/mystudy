# 核心概念与安装配置
Docker 的三大核心概念：
- 镜像 (Image)
- 容器 (Container)
- 仓库 (Repository)

## 核心概念
1. Docker 镜像
Docker 镜像类似于虚拟机镜像，可以将它理解为一个只读的模板。
2. Docker 容器
Docker 容器类似千一个轻量级的沙箱， Docker利用容器来运行和隔离应用。
容器是从镜像创建的应用运行实例。它可以启动、开始、停止、删除，而这些容器都是彼此相互隔离、互不可见的。

**注意**:镜像自身是只读的。容器从镜像启动的时候，会在镜像的最上层创建一个可写层。
3. Docker 仓库
Docker仓库类似于代码仓库，是Docker 集中存放镜像文件的场所。

## 配置 Docker 服务
为了避免每次使用 Docker 命令时都需要切换到特权身份，可以将当前用户加入安装中自动创建的 docker 用户组，代码如下：
> sudo usermod -aG docker $USER

# 使用 Dockerfile 创建镜像
## 基本结构
般而言， Dockerfile 主体内容分为四部分：基础镜像信息、维护者信息、镜像操作指令和容器启动时执行指令。
一个简单的示例:

```shell
# escape=\ (backslash) 
# This dockerfile uses he ubuntu:xeniel image 
# VERSION 2 - EDITION 1 
# Author: docker_user 
# Command format: Ins ruc ion [arguments / command] 
# Base image use, 
FROM ubuntu:xeniel 

# Main ainer: docker user <docker user email.com>
LABEL main ainer docker user<docker user@email.com> 
# Commands upda he image 
RUN echo "deb http://archive.ubuntu.com/ubuntu/ xeniel main universe" >> /etc/apt/sources.list

RUN apt-get  && apt-get install -y nginx 
RUN echo "\ndaemon off;">> /etc/nginx/nginx.conf
# Commands when crea ing a new con ainer
CMD /usr/sbin/nginx 

```
首行可以通过注释来指定解析器命令，后续通过注释说明镜像的相关信息。主体部分首先使用 FROM 指令指明所基于的镜像名称，接下来一般是使用 LABEL 指令说明维护者信息。后面则是镜像操作指令，例如 RUN 指令将对镜像执行跟随的命令。每运行一条 RUN 指令，镜像添加新的一层，并提交。最后是 CMD 指令，来指定运行容器时的操作命令。

##  指令说明
|分类|指令|说明|
<table>
    <tr>
        <th>分类</th>
        <th >指令</th>
       <th >说明</th>
       <!-- <th colspan="2">Header 2 &amp; 3 Combined</th> -->
    </tr>
    <tr>
        <td rowspan="14">配置指令</td>
        <td>指令</td>
        <td>说明</td>
    </tr>
    <tr>
    <td>ARG</td>
    <td>定义创建镜像过程中使用的变橇</td>
    </tr>
    <tr>
    <td>FROM</td>
    <td>指定所创建镜像的基础镜像</td>
    </tr>
    <tr>
    <td>LABEL</td>
    <td>为生成的镜像添加元数据标签信息</td>
    </tr>
    <tr>
    <td>EXPOSE</td>
    <td>声明镜像内服务监听的端口</td>
    </tr>
    <tr>
    <td>ENV</td>
    <td>指定环境变最</td>
    </tr>
    <tr>
    <td>ENTRY POINT </td>
    <td>指定镜像的默认入口命令</td>
    </tr>
    <tr>
    <td>VOLUME</td>
    <td>创建一个数据卷挂载点</td>
    </tr>
    <tr>
    <td>USER</td>
    <td>指定运行容器时的用户名或 UID</td>
    </tr>
    <tr>
    <td>WORKDIR </td>
    <td>配置工作目录</td>
    </tr>
    <tr>
    <td>ONBUILD </td>
    <td>创建子镜像时指定自动执行的操作指令</td>
    </tr>
    <tr>
    <td>STOPSIGNAL </td>
    <td>指定退出的信号值</td>
    </tr>
    <tr>
    <td>HEALTHCHECK</td>
    <td>配置所启动容器如何进行健康检查</td>
    </tr>
    <td>SHELL</td>
    <td>指定默认 shell 类型</td>
    </tr>
       <tr>
        <td rowspan="4">操作指令</td>
        <td>RUN </td>
        <td>运行指定命令</td>
    </tr>
    </tr>
       <tr>
        <td>CMD</td>
        <td>启动容器时指定默认执行的命</td>
    </tr>
    </tr>
       <tr>
        <td>ADD</td>
        <td>添加内容到镜像</td>
    </tr>
    </tr>
       <tr>
        <td>COPY</td>
        <td>复制内容到镜像</td>
    </tr>
</table>

## 创建镜像
编写完成 Dockerfile 之后，可以通过 docker [image] build 命令来创建镜像。基本的格式为 docker build [OPT ONS] PATH | URL 

该命令将读取指定路径下（包括子目录）的 Dockerfile, 并将该路径下所有数据作为上下(Context) 发送给 Docker 服务端。 Docker 服务端在校验 Dockerfile 格式通过后，逐条执行其中定义的指令，碰到 ADD COPY RUN 指令会生成一层新的镜像。

# 为镜像添加SSH服务
## 使用 Dockerfile 创建
1. 创建工作目录
首先，创建一个 sshd_ubuntu 工作目录：
```shell
$ mkdir sshd ubuntu 
$ ls 
sshd ubuntu 
```

在其中，创建 Dockerfile run.sh 文件：
```shell
$ cd sshd ubun / 
$ touch Dockerfile run.sh 
$ ls 
Dockerfile run.sh 
```

2. 编写 run.sh 脚本和 au horized_keys 文件
脚本文件 run.sh 的内容与上一小节中一致：
```shell
#!/bin/bash 
/usr/sbin/sshd -D 
```
在宿主主机上生成 SSH 密钥对，并创建 au horized_:keys 文件：
```shell
$ ssh-keygen -t rsa
···
$ ca ~/.ssh/id_rsa.pub >authorized_keys
```
3. 编写 Dockerfile
下面是 Dockerfile 的内容及各部分的注释，可以对比上一节中利用 docker commit命令
```shell
# 设置继承镜像
FROM  ubuntu: 18.04 
# 提供一些作者的信息 
MAINTAINER docker user (user@docker.com) 
# 面开始运行命令，此处更改 ubun 的源为国内 16,3 的源 .. • ·• :,·,.·.' 
RUN echo "deb http://mirrors.163.com/ubuntu/ bionic main restricted multiverse" > /etc/apt/sources.list 
RUN echo "deb http://mirrors.163.com/ubuntu/ bionic-security main
restricted universe multiverse" >  /etc/apt/sources.list 
RUN echo "deb. http://mirrors.163.com/ubuntu/ bionic-updates main
restricted universe multiverse" >  /etc/apt/sources.list 
RUN echo "deb http://mirrors.163.com/ubuntu/ bionic-proposed main
restricted universe multiverse" > /etc/apt/sources.list 
RUN echo "deb http://mirrors.163.com/ubuntu/ bionic-backports ain
restricted universe multiverse" > /etc/apt/sources.list 
RUN zpt-update
# 安装 ssh 服务
RUN apt-update install -y openssh-server 
RUN mkdir -p /var/run/sshd 
RUN mkdir -p /root/.ssh
# 取消 pam 限制
RUN sed -ri `s/ session required pam_loginuid.so/#session required pam_loginuid.so/g` /etc/pam.d/sshd

# 复制配置文件到相应位置，并赋予脚本可执行权限
ADD authorized_keys /roo／.ssh/authorized_keys
ADD run.sh /run.sh 
RUN chmod 755 /run.sh 
#开放端口
EXPOSE 22 
#设置自启动命令
CMD ["/run.sh"]
```
4. 创建镜像
```shell
$ cd sshd_ubuntu
$ docker build -t sshd:dockerfile. 
```
