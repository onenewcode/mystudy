## 开启远程连接root用户
**一、检查是否开启SSH服务**
因为Ubuntu默认是不安装SSH服务的，所以在安装之前可以查看目前系统是否安装，通过以下命令：
 ps -e|grep ssh 

输出的结果ssh-agent表示ssh-client启动，sshd表示ssh-server启动。我们是需要安装服务端所以应该看是否有sshd，如果没有则说明没有安装。

**二、安装SSH服务**

 sudo apt-get install openssh-client 客户端

 sudo apt-get install openssh-server 服务器

　　或者

 apt-get install ssh

**三、启动SSH服务** 

 sudo /etc/init.d/ssh start

**四、修改SSH配置文件**

可以通过SSH配置文件更改包括端口、是否允许root登录等设置，配置文件位置：

 /etc/ssh/sshd_config

 默认是不允许root远程登录的，可以再配置文件开启。

 sudo vi /etc/ssh/sshd_config

 找到PermitRootLogin without-password 修改为PermitRootLogin yes

**五、重启SSH服务**

 service ssh restart

 即可通过winscp 、putty使用ROOT权限远程登录。

 启用root用户：sudo passwd root      //修改密码后就启用了。

 客户端如果是ubuntu的话，则已经安装好ssh client,可以用下面的命令连接远程服务器。
 

简单介绍下SSH：

SSH：是一种安全通道协议，主要用来实现字符界面的远程登录，远程复制等功能(使用TCP的22号端口)。SSH协议对通信双方的数据传输进行了加密处理，其中包括用户登录时输入的用户口令。

在RHEL 5系统中使用的是OpenSSH服务器由openssh，openssh-server等软件包提供的(默认已经安装)，并以将sshd添加为标准的系统服务。

SSH提供一下两种方式的登录验证：

1、密码验证：以服务器中本地系统用户的登录名称，密码进行验证。

2、秘钥对验证：要求提供相匹配的秘钥信息才能通过验证。通常先在客户机中创建一对秘钥文件(公钥和私钥)，然后将公钥文件放到服务器中的指定位置。

注意：当密码验证和私钥验证都启用时，服务器将优先使用秘钥验证。

SSH的配置文件：

sshd服务的配置文件默认在/etc/ssh/sshd_config，正确调整相关配置项，可以进一步提高sshd远程登录的安全性。

配置文件的内容可以分为以下三个部分：

1、常见SSH服务器监听的选项如下：

Port 22                    //监听的端口为22

Protocol 2                //使用SSH V2协议

ListenAdderss 0.0.0.0    //监听的地址为所有地址

UseDNS no                //禁止DNS反向解析

2、常见用户登录控制选项如下：

PermitRootLogin no            //禁止root用户登录

PermitEmptyPasswords no        //禁止空密码用户登录

LoginGraceTime 2m            //登录验证时间为2分钟

MaxAuthTries 6                //最大重试次数为6

AllowUsers user            //只允许user用户登录，与DenyUsers选项相反

3、常见登录验证方式如下：

PasswordAuthentication yes                //启用密码验证

PubkeyAuthentication yes                    //启用秘钥验证

AuthorsizedKeysFile .ssh/authorized_keys    //指定公钥数据库文件



# 安装第三方软件
## docker
**step 1: 安装必要的一些系统工具**
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
**step 2: 安装GPG证书**
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
**Step 3: 写入软件源信息**
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
**Step 4: 更新并安装 Docker-CE**
sudo apt-get -y update
sudo apt-get -y install docker-ce

 安装指定版本的Docker-CE:
 Step 1: 查找Docker-CE的版本:
 apt-cache madison docker-ce
 docker-ce | 17.03.1~ce-0~ubuntu-xenial | http://mirrors.aliyun.com/docker-ce/linux/ubuntu xenial/stable amd64 Packages
 docker-ce | 17.03.0~ce-0~ubuntu-xenial | http://mirrors.aliyun.com/docker-ce/linux/ubuntu xenial/stable amd64 Packages
 Step 2: 安装指定版本的Docker-CE: (VERSION 例如上面的 17.03.1~ce-0~ubuntu-xenial)
sudo apt-get -y install docker-ce=[VERSION]


**添加用户到docker**
sudo groupadd docker     #添加docker用户组
sudo gpasswd -a $USER docker     #将登陆用户加入到docker用户组中
newgrp docker     #更新用户组
docker ps    #测试docker命令是否可以使用sudo正常使用







```cmd
上传文件必须是root用户
 su -
vi /etc/ssh/sshd_config
复制代码
# Authentication:
#将这个下面的配置修改为如下内容
LoginGraceTime 120
PermitRootLogin yes
StrictModes yes
#LoginGraceTime 2m
#PermitRootLogin prohibit-password
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10
复制代码
然后:wb保存

接下来重新启动ssh服务

sudo systemctl restart ssh
```
## lua
```cmd
#下载编译文件
curl -R -O http://www.lua.org/ftp/lua-5.2.4.tar.gz
#解压缩
tar -xvf lua-5.2.4.tar.gz
#转到相应的包
cd lua-5.2.4
# 编译
make linux test
# 安装
make install
```
进入lua-5.2.4目录后使用make linux && sudo make install进行编译并安装 。注意，这里安装到了/usr/loca/bin目录下

# 安装vim
sudo apt-get install vim-gtk
# 安装ufw 

sudo apt update
sudo apt install ufw

安装过程不会自动激活防火墙，以避免服务器被锁住。可以检查 UFW 的状态，输入：

sudo ufw status verbose


ufw命令行示例：

ufw enable/disable：打开/关闭防火墙
ufw reload：重启防火墙
ufw status：查看已经定义的ufw规则
ufw default allow/deny：外来访问默认允许/拒绝
ufw allow/deny 20：允许/拒绝访问20端口，20后可跟/tcp或/udp，表示tcp或udp封包。
sudo ufw allow proto tcp from 192.168.0.0/24 to any port 22：允许自192.168.0.0/24的tcp封包访问本机的22端口。
ufw delete allow/deny 20：删除以前定义的"允许/拒绝访问20端口"的规则
ufw打开或关闭某个端口，例如：
sudo ufw allow 9200 允许外部访问9200端口(tcp/udp)
sudo ufw allow 3690 允许外部访问3690端口(svn)
sudo ufw allow from 192.168.25.125 允许此IP访问所有的本机端口
sudo ufw allow proto tcp from 192.168.0.0/24 to any port 22 允许指定的IP段访问特定端口
sudo ufw delete allow smtp 删除上面建立的某条规则，比如删除svn端口就是 sudo ufw delete allow 3690 

方式二：iptables
第一步：安装iptables
sudo apt-get install iptables

第二步：添加规则
iptables -I INPUT -p tcp --dport 9200 -j ACCEPT

第三步：保存规则
iptables-save

至此为止就完成了开放指定的端口，但是如果此时服务器重启，上述规则就没有了，所以我们需要对规则进行一下持续化操作

第一步：安装iptables-persistent
sudo apt-get install iptables-persistent

第二步：保存或载入规则：
sudo netfilter-persistent save
sudo netfilter-persistent reload

生成的规则将被存储在以下文件中:

/etc/iptables/rules.v4
/etc/iptables/rules.v6
————————————————
版权声明：本文为CSDN博主「梁云亮」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/lianghecai52171314/article/details/113813826