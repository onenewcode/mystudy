# Linux 的文件权限与目录配置
### 目录介绍
<img src="img\屏幕截图 2022-11-04 092616.png">

| 目录 |  简介   |
|----------|----------|
| /bin |系统有很多放置可执行文件的目录，但/bin比较特殊。因为/bin放置的是在单人维护模式下还能够被操作的指令。 在/bin下面的指令可以被root与一般帐号所使用，主要有：cat, chmod, chown, date, mv,mkdir, cp, bash等等常用的指令。|
|/boot |这个目录主要在放置开机会使用到的文件，包括Linux核心文件以及开机菜单与开机所需配置文件等等。 Linux kernel常用的文件名vmlinuz，如果使用的是grub2这个开机管理程序， 则还会存在/boot/grub2/这个目录喔！|
|/dev |在Linux系统上，任何设备与周边设备都是以文件的型态存在于这个目录当中的。 你只要通过存取这个目录下面的某个文件，就等于存取某个设备啰～ 比要重要的文件有/dev/null, /dev/zero, /dev/tty, /dev/loop, /dev/sd等等|
|/etc |系统主要的配置文件几乎都放置在这个目录内，例如人员的帐号密码档、各种服务的启始档等等。一般来说，这个目录下的各文件属性是可以让一般使用者查阅的， 但是只有root有权力修改。FHS建议不要放置可可执行文件（binary）在这个目录中喔。比较重要的文件有： /etc/modprobe.d/,/etc/passwd, /etc/fstab, /etc/issue 等等。另外 FHS 还规范几个重要的目录最好要存在 /etc/ 目录下喔：/etc/opt（必要）：这个目录在放置第三方协力软件 /opt 的相关配置文件 /etc/X11/（建议）：与 X Window 有关的各种配置文件都在这里，尤其是 xorg.conf 这个 X Server 的配置文件。 /etc/sgml/（建议）：与 SGML 格式有关的各项配置文件 /etc/xml/（建议）：与 XML格式有关的各项配置文件 |
|/lib |系统的函数库非常的多，而/lib放置的则是在开机时会用到的函数库， 以及在/bin或/sbin下面的指令会调用的函数库而已。 什么是函数库呢？你可以将他想成是“外挂”，某些指令必须要有这些“外挂”才能够顺利完成|程序的执行之意。 另外 FSH 还要求下面的目录必须要存在：/lib/modules/：这个目录主要放置可抽换式的核心相关模块（驱动程序）喔！|
|/media |media是“媒体”的英文，顾名思义，这个/media下面放置的就是可移除的设备啦！ 包括软盘、光盘、DVD等等设备都暂时挂载于此。常见的文件名有：/media/floppy, /media/cdrom等等。|
|/mnt |如果你想要暂时挂载某些额外的设备，一般建议你可以放置到这个目录中。在古早时候，这个目录的用途与/media相同啦！只是有了/media之后，这个目录就用来暂时挂载用了。|
|/opt|这个是给第三方协力软件放置的目录。什么是第三方协力软件啊？ 举例来说，KDE这个桌面管理系统是一个独立的计划，不过他可以安装到Linux系统中，因此KDE的软件就建议放置到此目录下了。 另外，如果你想要自行安装额外的软件（非原本的distribution提供的），那么也能够将你的软件安装到这里来。不过，以前的Linux系统中，我们还是习惯放置在/usr/local目录下呢！|
|/run |早期的 FHS 规定系统开机后所产生的各项信息应该要放置到 /var/run 目录下，新版的 FHS 则规范到 /run 下面。 由于 /run 可以使用内存来仿真，因此性能上会好很多！|
|/srv|srv可以视为“service”的缩写，是一些网络服务启动之后，这些服务所需要取用的数据目录。 常见的服务例如WWW, FTP等等。举例来说，WWW服务器需要的网页数据就可以放置在/srv/www/里面。 不过，系统的服务数据如果尚未要提供给网际网络任何人浏览的话，默认还是建议放置到 /var/lib下面即可。|
|/tmp|这是让一般使用者或者是正在执行的程序暂时放置文件的地方。 这个目录是任何人都能够存取的，所以你需要定期的清理一下。当然，重要数据不可放置在此目录啊！ 因为FHS甚至建议在开机时，应该要将/tmp下的数据都删除唷！|
|/home|这是系统默认的使用者主文件夹（home directory）。在你新增一个一般使用者帐号时， 默认的使用者主文件夹都会规范到这里来。比较重要的是，主文件夹有两种代号喔：~：代表目前这个使用者的主文件夹 ~dmtsai ：则代表 dmtsai 的主文件夹！
|/lib<qual>| 用来存放与 /lib 不同的格式的二进制函数库，例如支持 64 位的 /lib64 函数库等|
|/root|系统管理员（root）的主文件夹。之所以放在这里，是因为如果进入单人维护模式而仅挂载根目录时， 该目录就能够拥有root的主文件夹|
|/lost+found|这个目录是使用标准的ext2/ext3/ext4文件系统格式才会产生的一个目录，目的在于当文件系统发生错误时， 将一些遗失的片段放置到这个目录下。不过如果使用的是 xfs 文件系统的话，就不会存在这个目录了！ |
|/proc|这个目录本身是一个“虚拟文件系统（virtual filesystem）”喔他放置的数据都是在内存当中， 例如系统核心、行程信息（process）、周边设备的状态及网络状态等等。因为这个目录下的数据都是在内存当中， 所以本身不占任何硬盘空间啊|

|/sys|这个目录其实跟/proc非常类似，也是一个虚拟的文件系统，主要也是记录核心与系统硬件信息较相关的信息。 包括目前已载入的核心模块与核心侦测到的硬件设备信息等等。这个目录同样不占硬盘容量喔！|
## 权限分组
    1.文件拥有者
    2.群组
    3. 其他人

```cmd
#切换用户
su
#或者 
sudo 
#查看权限
ls -l
#回到原来身份
exit
```
### 权限简介
<img src="img\屏幕截图 2022-11-04 083703.png">

**第一个字符代表这个文件是**“目录、文件或链接文件等等”：
当为[ d ]则是目录，例如上表文件名为“.config”的那一行；
当为[ - ]则是文件，例如上表文件名为“initial-setup-ks.cfg”那一行；
若是[ l ]则表示为链接文件（link file）；
若是[ b ]则表示为设备文件里面的可供储存的周边设备（可随机存取设备）；
若是[ c ]则表示为设备文件里面的序列埠设备，例如键盘、鼠标（一次性读取设
备）
数据输送档（FIFO, pipe）： FIFO也是一种特殊的文件类型，他主要的目的在解决多个
程序同时存取一个文件所造成的错误问题。 FIFO是first-in-first-out的缩写。第一个属性为
[ p ] 。
数据接口文件（sockets）： 既然被称为数据接口文件， 想当然尔，这种类型的文件通
常被用在网络上的数据承接了。我们可以启动一个程序来监听用户端的要求， 而用户端
就可以通过这个socket来进行数据的沟通了。第一个属性为 [ s ]， 最常在/run或/tmp这些个目录中看到这种文件类型了。

接下来的字符中，以三个为一组，且均为“rwx” 的三个参数的组合。其中，[ r ]代表可读
（read）、[ w ]代表可写（write）、[ x ]代表可执行（execute）。 要注意的是，这三个
权限的位置不会改变，如果没有权限，就会出现减号[ - ]而已。
**拓展名**
Linux文件扩展名：
基本上，Linux的文件是没有所谓的“扩展名”的，我们刚刚就谈过，一个Linux文件能不能被执
行，与他的第一栏的十个属性有关， 与文件名根本一点关系也没有。这个观念跟Windows的
情况不相同喔！在Windows下面， 能被执行的文件扩展名通常是 .com .exe .bat等等，而在
Linux下面，只要你的权限当中具有x的话，例如[ -rwxr-xr-x ] 即代表这个文件具有可以被执行
的能力喔！
*.sh ： 脚本或批处理文件 （scripts），因为批处理文件为使用shell写成的，所以扩展名
就编成 .sh 啰；
Z, .tar, .tar.gz, .zip, *.tgz： 经过打包的压缩文件。这是因为压缩软件分别为 gunzip, tar
等等的，由于不同的压缩软件，而取其相关的扩展名啰！
.html, .php：网页相关文件，分别代表 HTML 语法与 PHP 语法的网页文件啰！ .html 的
文件可使用网页浏览器来直接打开，至于 .php 的文件， 则可以通过 client 端的浏览器来
server 端浏览，以得到运算后的网页结果呢！
### 改变文件属性
    chgrp ：改变文件所属群组
    chown ：改变文件拥有者
    chmod ：改变文件的权限, SUID, SGID, SBIT等等的特性
chgrp
```cmd
[root@study ~]# chgrp [-R] dirname/filename ...
选项与参数：
-R : 进行递回（recursive）的持续变更，亦即连同次目录下的所有文件、目录
都更新成为这个群组之意。常常用在变更某一目录内所有的文件之情况。
范例：
[root@study ~]# chgrp users initial-setup-ks.cfg
[root@study ~]# ls -l
-rw-r--r--. 1 root users 1864 May 4 18:01 initial-setup-ks.cfg
[root@study ~]# chgrp testing initial-setup-ks.cfg
chgrp: invalid group: `testing' &lt;== 发生错误讯息啰～找不到这个群组名～

```   
chown
```cmd
[root@study ~]# chown [-R] 帐号名称 文件或目录
[root@study ~]# chown [-R] 帐号名称:群组名称 文件或目录
选项与参数：
-R : 进行递回（recursive）的持续变更，亦即连同次目录下的所有文件都变更
范例：将 initial-setup-ks.cfg 的拥有者改为bin这个帐号：
[root@study ~]# chown bin initial-setup-ks.cfg
[root@study ~]# ls -l
-rw-r--r--. 1 bin users 1864 May 4 18:01 initial-setup-ks.cfg
范例：将 initial-setup-ks.cfg 的拥有者与群组改回为root：
[root@study ~]# chown root:root initial-setup-ks.cfg
[root@study ~]# ls -l
-rw-r--r--. 1 root root 1864 May 4 18:01 initial-setup-ks.cfg
```

# 目录相关操作
## 创建删除转化
```cmd
. 代表此层目录
.. 代表上一层目录
- 代表前一个工作目录
~ 代表“目前使用者身份”所在的主文件夹
~account 代表 account 这个使用者的主文件夹（account是个帐号名称）
cd：变换目录
pwd：显示目前的目录
mkdir：创建一个新的目录
mkdir [-mp] 目录名称
选项与参数：
-m ：设置文件的权限喔！直接设置，不需要看默认权限 （umask） 的脸色～
-p ：帮助你直接将所需要的目录（包含上层目录）递回创建起来！

rmdir：删除一个空的目录
 rmdir [-p] 目录名称
选项与参数：
-p ：连同“上层”“空的”目录也一起删除

cd （change directory, 变换目录）
```
## 目录管理
### 查询
ls
```cmd
-a ：全部的文件，连同隐藏文件（ 开头为 . 的文件） 一起列出来（常用）
-A ：全部的文件，连同隐藏文件，但不包括 . 与 .. 这两个目录
-d ：仅列出目录本身，而不是列出目录内的文件数据（常用）
-f ：直接列出结果，而不进行排序 （ls 默认会以文件名排序！）
-F ：根据文件、目录等信息，给予附加数据结构，例如：
*:代表可可执行文件； /:代表目录； =:代表 socket 文件； &#124;:代表 FIFO 文件；
-h ：将文件大小以人类较易读的方式（例如 GB, KB 等等）列出来；
-i ：列出 inode 号码，inode 的意义下一章将会介绍；
-l ：长数据串行出，包含文件的属性与权限等等数据；（常用）
-n ：列出 UID 与 GID 而非使用者与群组的名称 （UID与GID会在帐号管理提到！）
-r ：将排序结果反向输出，例如：原本文件名由小到大，反向则为由大到小；
-R ：连同子目录内容一起列出来，等于该目录下的所有文件都会显示出来；
-S ：以文件大小大小排序，而不是用文件名排序；
-t ：依时间排序，而不是用文件名。
--color=never ：不要依据文件特性给予颜色显示；
--color=always ：显示颜色
--color=auto ：让系统自行依据设置来判断是否给予颜色
--full-time ：以完整时间模式 （包含年、月、日、时、分） 输出
--time={atime,ctime} ：输出 access 时间或改变权限属性时间 （ctime）
而非内容变更时间 （modification time）
```

 ### 复制，删除与移动
 **cp**
 ```cmd
# cp [-adfilprsu] 来源文件（source） 目标文件（destination）
[root@study ~]# cp [options] source1 source2 source3 .... directory
选项与参数：
-a ：相当于 -dr --preserve=all 的意思，至于 dr 请参考下列说明；（常用）
-d ：若来源文件为链接文件的属性（link file），则复制链接文件属性而非文件本身；
-f ：为强制（force）的意思，若目标文件已经存在且无法打开，则移除后再尝试一次；
-i ：若目标文件（destination）已经存在时，在覆盖时会先询问动作的进行（常用）
-l ：进行硬式链接（hard link）的链接文件创建，而非复制文件本身；
-p ：连同文件的属性（权限、用户、时间）一起复制过去，而非使用默认属性（备份常用）；
-r ：递回持续复制，用于目录的复制行为；（常用）
-s ：复制成为符号链接文件 （symbolic link），亦即“捷径”文件；
-u ：destination 比 source 旧才更新 destination，或 destination 不存在的情况下才复制。
--preserve=all ：除了 -p 的权限相关参数外，还加入 SELinux 的属性, links, xattr 等也复制了。
最后需要注意的，如果来源文件有两个以上，则最后一个目的文件一定要是“目录”才行！
 ```
**rm**
```cmd
[root@study ~]# rm [-fir] 文件或目录
选项与参数：
-f ：就是 force 的意思，忽略不存在的文件，不会出现警告讯息；
-i ：互动模式，在删除前会询问使用者是否动作
-r ：递回删除啊！最常用在目录的删除了！这是非常危险的选项！！！
范例一：将刚刚在 cp 的范例中创建的 bashrc 删除掉！
[root@study ~]# cd /tmp
[root@study tmp]# rm -i bashrc
rm: remove regular file `bashrc'? y
# 如果加上 -i 的选项就会主动询问喔，避免你删除到错误的文件名！
```
**mv**
```cmd
mv [-fiu] source destination
[root@study ~]# mv [options] source1 source2 source3 .... directory
选项与参数：
-f ：force 强制的意思，如果目标文件已经存在，不会询问而直接覆盖；
-i ：若目标文件 （destination） 已经存在时，就会询问是否覆盖！
-u ：若目标文件已经存在，且 source 比较新，才会更新 （update）
```
### 文件读取
cat 由第一行开始显示文件内容
tac 从最后一行开始显示，可以看出 tac 是 cat 的倒着写！
nl 显示的时候，顺道输出行号！
more 一页一页的显示文件内容
less 与 more 类似，但是比 more 更好的是，他可以往前翻页！
head 只看头几行
tail 只看尾巴几行
od 以二进制的方式读取文件内容！
### 修改文件时间或创建新文件： touch
modification time （mtime）： 当该文件的“内容数据”变更时，就会更新这个时间！内
容数据指的是文件的内容，而不是文件的属性或权限喔！
status time （ctime）： 当该文件的“状态 （status）”改变时，就会更新这个时间，举
例来说，像是权限与属性被更改了，都会更新这个时间啊。
access time （atime）： 当“该文件的内容被取用”时，就会更新这个读取时间
（access）。举例来说，我们使用 cat 去读取 /etc/man_db.conf ， 就会更新该文件的
atime 了。
### 文件特殊权限： SUID, SGID, SBIT
Set UID
当 s 这个标志出现在文件拥有者的 x 权限上时，例如刚刚提到的 /usr/bin/passwd 这个文件的
权限状态：“-rwsr-xr-x”，此时就被称为 Set UID，简称为 SUID 的特殊权限。 那么SUID的权
限对于一个文件的特殊功能是什么呢？基本上SUID有这样的限制与功能：
SUID 权限仅对二进制程序（binary program）有效；
执行者对于该程序需要具有 x 的可执行权限；
本权限仅在执行该程序的过程中有效 （run-time）；
执行者将具有该程序拥有者 （owner） 的权限。

### 指令文静名搜寻
which （寻找“可执行文件”）
```cmd
which [-a] command
选项或参数：
-a ：将所有由 PATH 目录中可以找到的指令均列出，而不止第一个被找到的指令名称
```
whereis [-bmsu] 文件或目录名
选项与参数：
-l :可以列出 whereis 会去查询的几个主要目录而已
-b :只找 binary 格式的文件
-m :只找在说明文档 manual 路径下的文件
-s :只找 source 来源文件
-u :搜寻不在上述三个项目当中的其他特殊文件


whereis （由一些特定的目录中寻找文件文件名）

```cmd
whereis [-bmsu] 文件或目录名
选项与参数：
-l :可以列出 whereis 会去查询的几个主要目录而已
-b :只找 binary 格式的文件
-m :只找在说明文档 manual 路径下的文件
-s :只找 source 来源文件
-u :搜寻不在上述三个项目当中的其他特殊文件

```

locate [-ir] keyword
选项与参数：
-i ：忽略大小写的差异；
-c ：不输出文件名，仅计算找到的文件数量
-l ：仅输出几行的意思，例如输出五行则是 -l 5
-S ：输出 locate 所使用的数据库文件的相关信息，包括该数据库纪录的文件/目录数量等
-r ：后面可接正则表达式的显示方式
# linux磁盘和文件管理系统
## 磁盘组成部分
 **整颗磁盘的组成主要有**
圆形的盘片（主要记录数据的部分）；
机械手臂，与在机械手臂上的磁头（可读写盘片上的数据）；
- 主轴马达，可以转动盘片，让机械手臂的磁头在盘片上读写数据。
- 扇区（Sector）为最小的物理储存单位，且依据磁盘设计的不同，目前主要有 512Bytes
与 4K 两种格式；
- 将扇区组成一个圆，那就是柱面（Cylinder）；
早期的分区主要以柱面为最小分区单位，现在的分区通常使用扇区为最小分区单位（每
个扇区都有其号码喔，就好像座位一样）；
- 磁盘分区表主要有两种格式，一种是限制较多的 MBR 分区表，一种是较新且限制较少的
GPT 分区表。
- MBR 分区表中，第一个扇区最重要，里面有：（1）主要开机区（Master boot record,
MBR）及分区表（partition table）， 其中 MBR 占有 446 Bytes，而 partition table 则占
有 64 Bytes。
- GPT 分区表除了分区数量扩充较多之外，支持的磁盘容量也可以超过 2TB
## 文件系统特性
文件系统通常会将这两部份的数据分别存放在不同
的区块，权限与属性放置到 inode 中，至于实际数据则放置到 data block 区块中。 另外，还
有一个超级区块 （superblock） 会记录整个文件系统的整体信息，包括 inode 与 block 的总
量、使用量、剩余量等。

由于每个 inode 与 block 都有编号，而每个文件都会占用一个 inode ，inode 内则有文件数据
放置的 block 号码。 因此，我们可以知道的是，如果能够找到文件的 inode 的话，那么自然
就会知道这个文件所放置数据的 block 号码，
<img src="img\屏幕截图 2022-11-04 202335.png">
这种数据存取的方法我们称为索引式文件系统（indexed allocation）

U盘使用的文件系统一般为 FAT 格式。FAT 这种格式的文件系统并没有 inode 存在，所以 FAT 没有办法将这个文件的所有 block 在一开始就读取出来。每个 block 号码都记录在前一个 block 当中， 他的读取方式有点像下面这样：U盘使用的文件系统一般
为 FAT 格式。FAT 这种格式的文件系统并没有 inode 存在，所以 FAT 没有办法将这个文件的
所有 block 在一开始就读取出来。每个 block 号码都记录在前一个 block 当中， 他的读取方
式有点像下面这样：

<img src="img\屏幕截图 2022-11-04 202826.png">

因此 Ext2 文件系统在格式化的时候基本上是区分为多个区块群组 （block
group） 的，
<img src="img\屏幕截图 2022-11-04 203108.png">
Ext2 文件系统的 block 还有什么限制呢？有的！基本限制如下：
原则上，block 的大小与数量在格式化完就不能够再改变了（除非重新格式化）；
- 每个 block 内最多只能够放置一个文件的数据；
- 承上，如果文件大于 block 的大小，则一个文件会占用多个 block 数量；
- 承上，若文件小于 block ，则该 block 的剩余容量就不能够再被使用了（磁盘空间会浪费）。
  
## inode able（inode 表格）
再来讨论一下 inode 这个玩意儿吧！如前所述 inode 的内容在记录文件的属性以及该文件实
际数据是放置在哪几号 block 内！ 基本上，inode 记录的文件数据至少有下面这些：[4]
该文件的存取模式（read/write/excute）；
该文件的拥有者与群组（owner/group）；
该文件的容量；
该文件创建或状态改变的时间（ctime）；
最近一次的读取时间（atime）；
最近修改的时间（mtime）；
定义文件特性的旗标（flag），如 SetUID...；
该文件真正内容的指向 （pointer）；
inode 的数量与大小也是在格式化时就已经固定了，除此之外 inode 还有些什么特色呢？
每个 inode 大小均固定为 128 Bytes （新的 ext4 与 xfs 可设置到 256 Bytes）；
每个文件都仅会占用一个 inode 而已；
承上，因此文件系统能够创建的文件数量与 inode 的数量有关；
系统读取文件时需要先找到 inode，并分析 inode 所记录的权限与使用者是否符合，若符
合才能够开始实际读取 block 的内容。
## Superblock （超级区块）
Superblock 是记录整个 filesystem 相关信息的地方， 没有 Superblock ，就没有这个
filesystem 了。他记录的信息主要有：
鸟哥的 Linux 私房菜：基础学习篇 第四版
7.1 认识 Linux 文件系统 349
block 与 inode 的总量；
未使用与已使用的 inode / block 数量；
block 与 inode 的大小 （block 为 1, 2, 4K，inode 为 128Bytes 或 256Bytes）；
filesystem 的挂载时间、最近一次写入数据的时间、最近一次检验磁盘 （fsck） 的时间
等文件系统的相关信息；

Filesystem Description （文件系统描述说明）
这个区段可以描述每个 block group 的开始与结束的 block 号码，以及说明每个区段
（superblock, bitmap, inodemap, data block） 分别介于哪一个 block 号码之间。这部份也能
够用 dumpe2fs 来观察的。
block bitmap （区块对照表）
如果你想要新增文件时总会用到 block 吧！那你要使用哪个 block 来记录呢？当然是选择“空
的 block ”来记录新文件的数据啰。 那你怎么知道哪个 block 是空的？这就得要通过 block
bitmap 的辅助了。从 block bitmap 当中可以知道哪些 block 是空的，因此我们的系统就能够
很快速的找到可使用的空间来处置文件啰。
同样的，如果你删除某些文件时，那么那些文件原本占用的 block 号码就得要释放出来， 此
时在 block bitmap 当中相对应到该 block 号码的标志就得要修改成为“未使用中”啰！这就是
bitmap 的功能。
inode bitmap （inode 对照表）
这个其实与 block bitmap 是类似的功能，只是 block bitmap 记录的是使用与未使用的 block
号码， 至于 inode bitmap 则是记录使用与未使用的 inode 号码啰！
dumpe2fs： 查询 Ext 家族 superblock 信息的指令
###  与目录树的关系
    当我们在 Linux 下的文件系统创建一个目录时，文件系统会分配一个 inode 与至少一块 block
给该目录。其中，inode 记录该目录的相关权限与属性，并可记录分配到的那块 block 号码；
而 block 则是记录在这个目录下的文件名与该文件名占用的 inode 号码数据
<img src="img\屏幕截图 2022-11-04 205037.png">

###  EXT2/EXT3/EXT4 文件的存取与日志式文件系统的功能
1. 先确定使用者对于欲新增文件的目录是否具有 w 与 x 的权限，若有的话才能新增；
2. 根据 inode bitmap 找到没有使用的 inode 号码，并将新文件的权限/属性写入；
3. 根据 block bitmap 找到没有使用中的 block 号码，并将实际的数据写入 block 中，且更
新 inode 的 block 指向数据；
4. 将刚刚写入的 inode 与 block 数据同步更新 inode bitmap 与 block bitmap，并更新
superblock 的内容。

**日志式文件系统 （Journaling filesystem）**
1. 预备：当系统要写入一个文件时，会先在日志记录区块中纪录某个文件准备要写入的信
息；
2. 实际写入：开始写入文件的权限与数据；开始更新 metadata 的数据；
3. 结束：完成数据与 metadata 的更新后，在日志记录区块当中完成该文件的纪录。
### 文件运行
**过一个称为非同步处理**
系统会将常用的文件数据放置到内存的缓冲区，以加速文件系统的读/写；
承上，因此 Linux 的实体内存最后都会被用光！这是正常的情况！可加速系统性能；
你可以手动使用 sync 来强迫内存中设置为 Dirty 的文件回写到磁盘中；
若正常关机时，关机指令会主动调用 sync 来将内存的数据回写入磁盘内；
但若不正常关机（如跳电、死机或其他不明原因），由于数据尚未回写到磁盘内， 因此
重新开机后可能会花很多时间在进行磁盘检验，甚至可能导致文件系统的损毁（非磁盘
损毁）。
### 挂载点的意义 （mount point）
重点是：挂载点一定是目录，该目录为进入该文件系统的入口。
因此并不是你有任何文件系统都能使用，必须要“挂载”到目录树的某个目录后，才能够使用该
文件系统的。
###  其他 Linux 支持的文件系统与 VFS
想要知道你的 Linux 支持的文件系统有哪些，可以察看下面这个目录：
[root@study ~]# ls -l /lib/modules/$（uname -r）/kernel/fs
系统目前已载入到内存中支持的文件系统则有：
[root@study ~]# cat /proc/filesystems
<img src="img\屏幕截图 2022-11-04 211319.png">

### XFS 文件系统简介
xfs 文件系统在数据的分佈上，主要规划为三个部份，一个数据区 （data section）、一个文
件系统活动登录区 （log section）以及一个实时运行区 （realtime section）。 这三个区域的
数据内容如下：
**数据区 （data section）**
基本上，数据区就跟我们之前谈到的 ext 家族一样，包括 inode/data block/superblock 等数
据，都放置在这个区块。 这个数据区与 ext 家族的 block group 类似，也是分为多个储存区群
组 （allocation groups） 来分别放置文件系统所需要的数据。 每个储存区群组都包含了
（1）整个文件系统的 superblock、 （2）剩余空间的管理机制、 （3）inode的分配与追踪。
此外，inode与 block 都是系统需要用到时， 这才动态配置产生，所以格式化动作超级快！
**文件系统活动登录区 （log section）**
在登录区这个区域主要被用来纪录文件系统的变化，其实有点像是日志区啦！文件的变化会
在这里纪录下来，直到该变化完整的写入到数据区后， 该笔纪录才会被终结。如果文件系统
因为某些缘故 （例如最常见的停电） 而损毁时，系统会拿这个登录区块来进行检验，看看系
统挂掉之前， 文件系统正在运行些啥动作，借以快速的修复文件系统
**实时运行区 （realtime section）**
当有文件要被创建时，xfs 会在这个区段里面找一个到数个的 extent 区块，将文件放置在这个
区块内，等到分配完毕后，再写入到 data section 的 inode 与 block 去！ 这个 extent 区块的
大小得要在格式化的时候就先指定，最小值是 4K 最大可到 1G。一般非磁盘阵列的磁盘默认
为 64K 容量，而具有类似磁盘阵列的 stripe 情况下，则建议 extent 设置为与 stripe 一样大较
佳。这个 extent 最好不要乱动，因为可能会影响到实体磁盘的性能喔。
##  文件系统简单操作
df：列出文件系统的整体磁盘使用量；
```cmd
df [-ahikHTm] [目录或文件名]
选项与参数：
-a ：列出所有的文件系统，包括系统特有的 /proc 等文件系统；
-k ：以 KBytes 的容量显示各文件系统；
-m ：以 MBytes 的容量显示各文件系统；
-h ：以人们较易阅读的 GBytes, MBytes, KBytes 等格式自行显示；
-H ：以 M=1000K 取代 M=1024K 的进位方式；
-T ：连同该 partition 的 filesystem 名称 （例如 xfs） 也列出；
-i ：不用磁盘容量，而以 inode 的数量来显示




du [-ahskm] 文件或目录名称
选项与参数：
-a ：列出所有的文件与目录容量，因为默认仅统计目录下面的文件量而已。
-h ：以人们较易读的容量格式 （G/M） 显示；
-s ：列出总量而已，而不列出每个各别的目录占用容量；
-S ：不包括子目录下的总计，与 -s 有点差别。
-k ：以 KBytes 列出容量显示；
-m ：以 MBytes 列出容量显示；
```
### 实体链接与符号链接
**Hard Link （实体链接, 硬式链接或实际链接）**
：hard link 只是在某个目录下新增一笔文件名链接到某 inode 号码的关连记录而已。（ps:除文件名不一样其他都一样）
<img src="img\屏幕截图 2022-11-05 090004.png">

 **Symbolic Link （符号链接，亦即是捷径）**
 Symbolic link 就是在创建一个
独立的文件，而这个文件会让数据的读取指向他 link 的那个文件的文件名！由于只是利用文
件来做为指向的动作， 所以，当来源文件被删除之后，symbolic link 的文件会“开不了”， 会
一直说“无法打开某文件！”
<img src="img\屏幕截图 2022-11-05 090321.png">

##  磁盘的分区、格式化、检验与挂载

1. 对磁盘进行分区，以创建可用的 partition ；
2. 对该 partition 进行格式化 （format），以创建系统可用的 filesystem；
3. 若想要仔细一点，则可对刚刚创建好的 filesystem 进行检验；
4. 在 Linux 系统上，需要创建挂载点 （亦即是目录），并将他挂载上来；
 ### 观察磁盘分区状态
  lsblk [-dfimpt] [device]
选项与参数：
-d ：仅列出磁盘本身，并不会列出该磁盘的分区数据
-f ：同时列出该磁盘内的文件系统名称
-i ：使用 ASCII 的线段输出，不要使用复杂的编码 （再某些环境下很有用）
-m ：同时输出该设备在 /dev 下面的权限数据 （rwx 的数据）
-p ：列出该设备的完整文件名！而不是仅列出最后的名字而已。
-t ：列出该磁盘设备的详细数据，包括磁盘伫列机制、预读写的数据量大小
# 文件与文件系统的压缩，打包与备份
## 打包 tar
```cmd
tar [-z&#124;-j&#124;-J] [tv] [-f 既有的 tar文件名] &lt;==察看文件名
[dmtsai@study ~]$ tar [-z&#124;-j&#124;-J] [xv] [-f 既有的 tar文件名] [-C 目录] &lt;==解压缩
选项与参数：
-c ：创建打包文件，可搭配 -v 来察看过程中被打包的文件名（filename）
-t ：察看打包文件的内容含有哪些文件名，重点在察看“文件名”就是了；
-x ：解打包或解压缩的功能，可以搭配 -C （大写） 在特定目录解开
特别留意的是， -c, -t, -x 不可同时出现在一串命令行中。
-z ：通过 gzip 的支持进行压缩/解压缩：此时文件名最好为 *.tar.gz
-j ：通过 bzip2 的支持进行压缩/解压缩：此时文件名最好为 *.tar.bz2
-J ：通过 xz 的支持进行压缩/解压缩：此时文件名最好为 *.tar.xz
特别留意， -z, -j, -J 不可以同时出现在一串命令行中
-v ：在压缩/解压缩的过程中，将正在处理的文件名显示出来！
-f filename：-f 后面要立刻接要被处理的文件名！建议 -f 单独写一个选项啰！（比较不会忘记）
-C 目录 ：这个选项用在解压缩，若要在特定目录解压缩，可以使用这个选项。
其他后续练习会使用到的选项介绍：
-p（小写） ：保留备份数据的原本权限与属性，常用于备份（-c）重要的配置文件
-P（大写） ：保留绝对路径，亦即允许备份数据中含有根目录存在之意；
--exclude=FILE：在压缩的过程中，不要将 FILE 打包！
```
# vim
##  vim 的暂存盘、救援回复与打开时的警告讯息
**救援回复**
当我们在使用 vim 编辑时， vim 会在与被编辑的文件的目录下，再创建一个名为
.filename.swp 的文件。 比如说我们在上一个小节谈到的编辑 /tmp/vitest/man_db.conf 这个文
件时， vim 会主动的创建 /tmp/vitest/.man_db.conf.swp 的暂存盘，你对 man_db.conf 做的动
作就会被记录到这个 .man_db.conf.swp 当中喔！
## vim额外功能
 **区块选择**
|按键| 区块选择的按键意义 |
|---------|-------------|
|v |字符选择，会将光标经过的地方反白选择！|
|V （大写）|列选择，会将光标经过的列反白选择！|
|[Ctrl]+v| 区块选择，可以用长方形的方式选择数据|
|y |将反白的地方复制起来|
| d |将反白的地方删除掉 |
| p | 将刚刚复制的区块，在光标所在处贴上！|
**多文件编辑**
| 按键|区块选择的按键意义|
|-----------|----------|
|:n |编辑下一个文件|
|:N| 编辑上一个文件|
|:files |列出目前这个 vim 的打开的所有文件 |
**多窗口功能**
|按键   |多窗口情况下的按键功能|
|----------|----------------|
|:sp[filename]|打开一个新窗口，如果有加filename， 表示在新窗口打开一个新文件，否则表示两个窗口为同一个文件内容（同步显示）。|
|[ctrl]+w+ j 或[ctrl]+w+↓|按键的按法是：先按下[ctrl] 不放， 再按下 w 后放开所有的按键，然后再按下 j （或向下方向键），则光标可移动到下方的窗口。|
|[ctrl]+w+ k或 [ctrl]+w+↑| 同上，不过光标移动到上面的窗口。|
|[ctrl]+w+q |其实就是 :q 结束离开啦！ 举例来说，如果我想要结束下方的窗口，那么利用 [ctrl]+w+↓ 移动到下方窗口后，按下 :q 即可离开， 也可以按下[ctrl]+w+q 啊！|

## 常用按键示意图
<img src="img\屏幕截图 2022-11-05 112445.png">


# bash 
## bash功能
- **命令编修能力 （history）：**
bash 的功能里头，鸟哥个人认为相当棒的一个就是“他能记忆使用过的指令！” 
- **命令别名设置功能： （alias）**
ls -al 这样的一个功能，嘿！那么要如何作呢？就使用 alias 即可！你可以在命令行输入 alias
就可以知道目前的命令别名有哪些了！也可以直接下达命令来设置别名呦：
*例子alias* lm='ls -al'
- **工作控制、前景背景控制： （job control, foreground, background）**
这使用前、背景的控制可以让工作进行的更为顺利！至于工作控制（jobs）的用途则更广， 可以让我们随时将工作丢到背景中执行！
- **程序化脚本： （shell scripts）**
在 Linux 下面的 shell scripts 则发挥更为强大的功能，可以将你平时管理系统常需要下达的连续指令写成一个文件， 该文件并且可以通过对谈互动式的方式来进行主机的侦测工作！也可以借由 shell 提供的环境变量及相关指令来进行设计。

- **万用字符： （Wildcard）**
bash 还支持许多的万用字符来帮助使用者查询与指令下达。 举例来说，想要知道 /usr/bin 下面有多少以 X 为开头的文件吗？使用：“ ls -l /usr/bin/X* ”就能够知道

**ps**
可以用type判断是否是shell内置命令
## shell变量功能

### 什么是变量 
**影响 bash 环境操作的变量**
某些特定变量会影响到 bash 的环境。 你能不能在任何目录下执行某个指令，与 PATH 这个变量有很大的关系。例如你下达ls 这个指令时，系统就是通过 PATH 这个变量里面的内容所记录的路径顺序来搜寻指令的呢！如果在搜寻完 PATH 变量内的路径还找不到 ls 这个指令时， 就会在屏幕上显示“command not found ”。
### 变量的取用与设置：echo, 变量设置规则, unset

**变量的取用: echo**
echo ${myname} 或 echo $myname
**设置**
**例子** myname=VBird
- 变量与变量内容以一个等号“=”来链接，如下所示：“myname=VBird”
- 等号两边不能直接接空白字符，如下所示为错误： “myname = VBird”或“myname=VBird sai”
- 变量名称只能是英文字母与数字，但是开头字符不能是数字
- 变量内容若有空白字符可使用双引号“"”或单引号“'”将变量内容结合起来，但双引号内的特殊字符如 $ 等，可以保有原本的特性，单引号内的特殊字符则仅为一般字符 （纯文本）
- 在一串指令的执行中，还需要借由其他额外的指令所提供的信息时，可以使用反单引号“ 指令 ”或 “$（指令）”。
-若该变量需要在其他子程序执行，则需要以 export 来使变量变成环境变量： “export PATH”
- 消变量的方法为使用 unset ：“unset 变量名称”例如取消 myname 的设置： “unset myname”

### 环境变量的功能
**env查看所有环境变量**
- HOME 代表使用者的主文件夹。还记得我们可以使用 cd ~ 去到自己的主文件夹吗
- SHELL 告知我们，目前这个环境使用的 SHELL 是哪支程序？ Linux 默认使用 /bin/bash
- MAIL 当我们使用 mail 这个指令在收信时，系统会去读取的邮件信箱文件 （mailbox）
- PATH 就是可执行文件搜寻的路径啦～目录与目录中间以冒号（:）分隔， 由于文件的搜寻是依序由 PATH 的变量内的目录来查询，所以，目录的顺序也是重要的喔。
- LANG 就是语系数据啰～很多讯息都会用到他， 举例来说，当我们在启动某些 perl 的程序语言文件时，他会主动的去分析语系数据文件， 如果发现有他无法解析的
编码语系，可能会产生错误喔！一般来说，我们中文编码通常是 zh_TW.Big5 或者是zh_TW.UTF-8，这两个编码偏偏不容易被解译出来，所以，有的时候，可能需要修订一
下语系数据。
- RANDOM 这个玩意儿就是“随机乱数”的变量啦
- 用 set 观察所有变量 （含环境变量与自订变量）
- PS1：（提示字符的设置）
按下 [Enter] 按键去执行某个指令后，最后要再次出现提示字符时， 就会主动去读取这个变量
值了。上头 PS1 内显示的是一些特殊符号，这些特殊符号可以显示不同的信息。你可以用 man bash [3]去查询一下 PS1 的相关说明，以理解下面的一些符号意
义。
\d ：可显示出“星期 月 日”的日期格式，如："Mon Feb 2"
\H ：完整的主机名称。举例来说，鸟哥的练习机为“study.centos.vbird”
\h ：仅取主机名称在第一个小数点之前的名字，如鸟哥主机则为“study”后面省略
\t ：显示时间，为 24 小时格式的“HH:MM:SS”
\T ：显示时间，为 12 小时格式的“HH:MM:SS”
\A ：显示时间，为 24 小时格式的“HH:MM”
\@ ：显示时间，为 12 小时格式的“am/pm”样式
\u ：目前使用者的帐号名称，如“dmtsai”；
\v ：BASH 的版本信息，如鸟哥的测试主机版本为 4.2.46（1）-release，仅取“4.2”显示
\w ：完整的工作目录名称，由根目录写起的目录名称。但主文件夹会以 ~ 取代；
\W ：利用 basename 函数取得工作目录名称，所以仅会列出最后一个目录名。
\# ：下达的第几个指令。
$ ：提示字符，如果是 root 时，提示字符为 # ，否则就是 $ 啰～
-$：（关于本 shell 的 PID）
钱字号本身也是个变量喔！目前这个 Shell 的线程代号”
PID （Process ID）。“ echo $$ ”出现的数字就是你的 PID 号码。
?：（关于上个执行指令的回传值）
这个变量是：“上一个执行的指令所回传的值”， 上面句话的重点是“上一个指令”与“回传值”两个地方。当我们执行某些指令时， 这些指令都会回传一个执行后的代码。一般来说，如果成功返回0，错误返回代码
-OSTYPE, HOSTTYPE, MACHTYPE：（主机硬件与核心的等级）
-export： 自订变量转成环境变量
环境变量与自订变量，这两者的差异在于“ 该变量是否会被子程序所继续引用“当你登陆 Linux 并取得一个 bash 之后，你的 bash 就是一个独立的程序，这个程序的识别使用的是一个称为程序识别码，被称为 PID 的就是。 接下来你在这个 bash 下面所下达的任何指令都是由这个 bash 所衍生出来的，那些被下达的指令就被称为子程序了。 
###  影响显示结果的语系变量 （locale）
```cmd
[dmtsai@study ~]$ locale -a
....（前面省略）....
zh_TW
zh_TW.big5 &lt;==大五码的中文编码
zh_TW.euctw
zh_TW.utf8 &lt;==万国码的中文编码
zu_ZA
zu_ZA.iso88591
zu_ZA.utf8
```
###  变量键盘读取、阵列与宣告： read, array, declare
**read**
```cmd
read [-pt] variable
选项与参数：
-p ：后面可以接提示字符！
-t ：后面可以接等待的“秒数！”这个比较有趣～不会一直等待使用者啦！

```
**declare / typeset**
declare 或 typeset 是一样的功能，就是在“宣告变量的类型”。如果使用 declare 后面并没有接任何参数，那么 bash 就会主动的将所有的变量名称与内容通通叫出来，就好像使用 set 一样.
```s
declare [-aixr] variable
选项与参数：
-a ：将后面名为 variable 的变量定义成为阵列 （array） 类型
-i ：将后面名为 variable 的变量定义成为整数数字 （integer） 类型
-x ：用法与 export 一样，就是将后面的 variable 变成环境变量；
-r ：将变量设置成为 readonly 类型，该变量不可被更改内容，也不能 unset
```
- 变量类型默认为“字串”，所以若不指定变量类型，则 1+2 为一个“字串”而不是“计算式”。

- bash 环境中的数值运算，默认最多仅能到达整数形态，所以 1/3 结果是 0；
**阵列 （array） 变量类型**
范例：设置上面提到的 var[1] ～ var[3] 的变量。
[dmtsai@study ~]$ var[1]="small min"
[dmtsai@study ~]$ var[2]="big min"
[dmtsai@study ~]$ var[3]="nice min"

###  与文件系统及程序的限制关系： ulimit
```cmd
 ulimit [-SHacdfltu] [配额]
选项与参数：
-H ：hard limit ，严格的设置，必定不能超过这个设置的数值；
-S ：soft limit ，警告的设置，可以超过这个设置值，但是若超过则有警告讯息。
-a ：后面不接任何选项与参数，可列出所有的限制额度；
-c ：当某些程序发生错误时，系统可能会将该程序在内存中的信息写成文件（除错用），
这种文件就被称为核心文件（core file）。此为限制每个核心文件的最大容量。
-f ：此 shell 可以创建的最大文件大小（一般可能设置为 2GB）单位为 KBytes
-d ：程序可使用的最大断裂内存（segment）容量；
-l ：可用于锁定 （lock） 的内存量
-t ：可使用的最大 CPU 时间 （单位为秒）
-u ：单一使用者可以使用的最大程序（process）数量。
```
###  变量内容的删除、取代与替换 （Optional）
**删除**
<img src="img\屏幕截图 2022-11-07 082749.png">

**取代**
<img src="img\屏幕截图 2022-11-07 082900.png">

## 命令别名和历史
**命令别名设置： alias, unalias**
**史命令：history**
```cmd
history [n]
[dmtsai@study ~]$ history [-c]
[dmtsai@study ~]$ history [-raw] histfiles
选项与参数：
n ：数字，意思是“要列出最近的 n 笔命令列表”的意思！
-c ：将目前的 shell 中的所有 history 内容全部消除
-a ：将目前新增的 history 指令新增入 histfiles 中，若没有加 histfiles ，
则默认写入 ~/.bash_history
-r ：将 histfiles 的内容读到目前这个 shell 的 history 记忆中；
-w ：将目前的 history 记忆内容写入 histfiles 中！
```
## bash shell操作环境
### 路径与指令搜寻顺序
1. 以相对/绝对路径执行指令，例如“ /bin/ls ”或“ ./ls ”；
2. 由 alias 找到该指令来执行；
3. 由 bash 内置的 （builtin） 指令来执行；
4. 通过 $PATH 这个变量的顺序搜寻到的第一个指令来执行。
### bash 环境配置文件
我们前几个小节谈到的命令别名啦、自订的变量啦，在你
登出 bash 后就会失效，所以你想要保留你的设置， 就得要将这些设置写入配置文件才行。
#### login 
login shell 其实只会读取这两个配置文件：
1. /etc/profile：这是系统整体的设置，你最好不要修改这个文件
2. ~/.bash_profile 或 ~/.bash_login 或 ~/.profile：属于使用者个人设置，你要改自己的数

**两个文件内容**
- /etc/profile （login shell 才会读）
（UID） 来决定很多重要的变量数据， 这也是每个使用者登陆取得 bash 时一定会读取的配置文件！
文件设置的变量主要有：
PATH：会依据 UID 决定 PATH 变量要不要含有 sbin 的系统指令目录；
MAIL：依据帐号设置好使用者的 mailbox 到 /var/spool/mail/帐号名；
USER：根据使用者的帐号设置此一变量内容；
HOSTNAME：依据主机的 hostname 指令决定此一变量内容；
HISTSIZE：历史命令记录笔数。CentOS 7.x 设置为 1000 ；
umask：包括 root 默认为 022 而一般用户为 002 等！
/etc/profile ，他还会去调用外部的设置数据喔！在 ，下面这些数据会依序的被调用进来：
/etc/profile.d/*.sh
其实这是个目录内的众多文件！只要在 /etc/profile.d/ 这个目录内且扩展名为 .sh ，另外，使用者能够具有 r 的权限， 那么该文件就会被 /etc/profile 调用进来。
/etc/locale.conf
这个文件是由 /etc/profile.d/lang.sh 调用进来的！这也是我们决定 bash 默认使用何种语系的
重要配置文件！ 文件里最重要的就是 LANG/LC_ALL 这些个变量的设置啦！我们在前面的
/usr/share/bash-completion/completions/*
记得我们上头谈过 [tab] 的妙用吧？除了命令补齐、文件名补齐之外，还可以进行指令的选项/
参数补齐功能！那就是从这个目录里面找到相对应的指令来处理的！ 其实这个目录下面的内容是由 /etc/profile.d/bash_completion.sh 这个文件载入的啦！
- ~/.bash_profile （login shell 才会读）
bash 在读完了整体环境设置的 /etc/profile 并借此调用其他配置文件后，接下来则是会读取使
用者的个人配置文件。 在 login shell 的 bash 环境中，所读取的个人偏好配置文件其实主要
有三个，依序分别是：
1. ~/.bash_profile
2. ~/.bash_login
3. ~/.profile
其实 bash 的 login shell 设置只会读取上面三个文件的其中一个， 而读取的顺序则是依照上面的顺序。

```c
[dmtsai@study ~]$ cat ~/.bash_profile
# .bash_profile
# Get the aliases and functions
if [ -f ~/.bashrc ]; then &lt;==下面这三行在判断并读取 ~/.bashrc
. ~/.bashrc
fi
# User specific environment and startup programs
PATH=$PATH:$HOME/.local/bin:$HOME/bin &lt;==下面这几行在处理个人化设置
export PATH
```
这个文件内有设置 PATH 这个变量喔！而且还使用了 export 将 PATH 变成环境变量呢！ 由于PATH 在 /etc/profile 当中已经设置过，所以在这里以累加的方式增加使用者主文件夹下的~/bin/ 。
一个指令“ source ”来读取的！ 也就是说 ~/.bash_profile 其实会再调用 ~/.bashrc 的设置内容
喔！最后，我们来看看整个 login shell 的读取流程：
图

<img src="img\屏幕截图 2022-11-07 103841.png">

source ：读入环境配置文件的指令
```cmd
dmtsai@study ~]$ source 配置文件文件名
范例：将主文件夹的 ~/.bashrc 的设置读入目前的 bash 环境中
[dmtsai@study ~]$ source ~/.bashrc &lt;==下面这两个指令是一样的！
[dmtsai@study ~]$ . ~/.bashrc
```
利用 source 或小数点 （.） 都可以将配置文件的内容读进来目前的 shell 环境中！ 
**non-login shell**
- ~/.bashrc （non-login shell 会读）
bash 配置文件仅会读取 ~/.bashrc 
```cmd
[root@study ~]# cat ~/.bashrc
# .bashrc
# User specific aliases and functions
alias rm='rm -i' &lt;==使用者的个人设置
alias cp='cp -i'
alias mv='mv -i'
# Source global definitions
if [ -f /etc/bashrc ]; then &lt;==整体的环境设置
. /etc/bashrc
fi
```
/etc/man_db.conf
！这的文件的内容“规范了使用 man 的时候， man page 的路径到哪里去寻找！”这个文件规定了下达 man 的时候，该去哪里查看数据的路径设置！那么什么时候要来修改这个文件呢？如果你是以 tarball 的方式来安装你的数据，那么你的
man page 可能会放置在 /usr/local/softpackage/man 里头，那个 softpackage 是你的套件名
称， 这个时候你就得以手动的方式将该路径加到 /etc/man_db.conf 里头，否则使用 man 的
~/.bash_history
还记得我们在历史命令提到过这个文件吧？默认的情况下， 我们的历史命令就记录在这里
~/.bash_logout
这个文件则记录了“当我登出 bash 后，系统再帮我做完什么动作后才离开”的意思。 你可以去
读取一下这个文件的内容，默认的情况下，登出时， bash 只是帮我们清掉屏幕的讯息而已。
不过，你也可以将一些备份或者是其他你认为重要的工作写在这个文件中 （例如清空暂存
盘），
###  bash 的进站与欢迎讯息： /etc/issue, /etc/motd
/etc/issue bash进站信息
/etc/motd  Linux进站信息
## 数据流重导向
1. 标准输入 （stdin） ：代码为 0 ，使用 < 或 << ；
2. 标准输出 （stdout）：代码为 1 ，使用 > 或 >> ；
3. 标准错误输出（stderr）：代码为 2 ，使用 2> 或 2>> ；

1> ：以覆盖的方法将“正确的数据”输出到指定的文件或设备上；
1>>：以累加的方法将“正确的数据”输出到指定的文件或设备上；
2> ：以覆盖的方法将“错误的数据”输出到指定的文件或设备上；
2>>：以累加的方法将“错误的数据”输出到指定的文件或设备上；

## 管线命令
###  撷取命令： cut, grep
**cut**
```cmd
 cut -d'分隔字符' -f fields &lt;==用于有特定分隔字符
[dmtsai@study ~]$ cut -c 字符区间 &lt;==用于排列整齐的讯息
选项与参数：
-d ：后面接分隔字符。与 -f 一起使用；
-f ：依据 -d 的分隔字符将一段讯息分区成为数段，用 -f 取出第几段的意思；
-c ：以字符 （characters） 的单位取出固定字符区间；
```
**grep**
刚刚的 cut 是将一行讯息当中，取出某部分我们想要的，而 grep 则是分析一行讯息， 若当中
有我们所需要的信息
```cmd
grep [-acinv] [--color=auto] '搜寻字串' filename
选项与参数：
-a ：将 binary 文件以 text 文件的方式搜寻数据
-c ：计算找到 '搜寻字串' 的次数
-i ：忽略大小写的不同，所以大小写视为相同
-n ：顺便输出行号
-v ：反向选择，亦即显示出没有 '搜寻字串' 内容的那一行！
--color=auto ：可以将找到的关键字部分加上颜色的显示喔！
```
###  排序命令： sort, wc, uniq
```cmd
$ sort [-fbMnrtuk] [file or stdin]
选项与参数：
-f ：忽略大小写的差异，例如 A 与 a 视为编码相同；
-b ：忽略最前面的空白字符部分；
-M ：以月份的名字来排序，例如 JAN, DEC 等等的排序方法；
-n ：使用“纯数字”进行排序（默认是以文字体态来排序的）；
-r ：反向排序；
-u ：就是 uniq ，相同的数据中，仅出现一行代表；
-t ：分隔符号，默认是用 [tab] 键来分隔；
-k ：以那个区间 （field） 来进行排序的意思
```
**uniq**
``` cmd
uniq [-ic]
选项与参数：
-i ：忽略大小写字符的不同；
-c ：进行计数
```
**wc**

```cmd
wc [-lwm]
选项与参数：
-l ：仅列出行；
-w ：仅列出多少字（英文单字）；
-m ：多少字符；
```
### 双重导向 tee
```cmd
$ tee [-a] file
选项与参数：
-a ：以累加 （append） 的方式，将数据加入 file 当中！$ tee [-a] file
选项与参数：
-a ：以累加 （append） 的方式，将数据加入 file 当中！
```
### 字符转换命令： tr, col, join, paste, expand
tr 可以用来删除一段讯息当中的文字，或者是进行文字讯息的替换！
# 学习 Shell Scripts
## shell命令执行顺序
1. 以相对/绝对路径执行指令，例如“ /bin/ls ”或“ ./ls ”；
2. 由 alias 找到该指令来执行；
3. 由 bash 内置的 （builtin） 指令来执行；
4. 通过 $PATH 这个变量的顺序搜寻到的第一个指令来执行。
## 第一个shell
```shell
#!/bin/bash
# Program:
# This program shows "Hello World!" in your screen.
# History:
# 2015/07/16 VBird First release
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
echo -e "Hello World! \a \n"
exit 0
```
1. 第一行 #!/bin/bash 在宣告这个 script 使用的 shell 名称： 因为我们使用的是 bash ，所以，必须要以“ #!/bin/bash ”来宣告这个文件内的语法使用 bash 的语法！那么当这个程序被执行时，他就能够载入 bash 的相关环境配置文件 （一般来说就是 non-login shell的 ~/.bashrc）， 并且执行 bash 来使我们下面的指令能够执行！
2. 程序内容的说明： 整个 script 当中，除了第一行的“ #! ”是用来宣告 shell 的之外，其他的# 都是“注解”用途！ 一般来说， 建议你一定要养成说明该 script 的：1. 内容与功能； 2. 版本信息； 3.作者与联络方式； 4. 创建日期；5. 历史纪录.
3. 主要环境变量的宣告： 建议务必要将一些重要的环境变量设置好，PATH 与 LANG （如果有使用到输出相关的信息时） 是当中最重要的！ 如此一来，则可让我们这支程序在进行时，可以直接下达一些外部指令.
4. 主要程序部分 就将主要的程序写好即可！
5. 执行成果告知 （定义回传值） 是否记得我们在第十章里面要讨论一个指令的执行成功与否，可以使用 $? 这个变量来观察～ 那么我们也可以利用 exit 这个指令来让程序中断，并且回传一个数值给系统。
## shell script练习
**加减乘除**
格式：var=$（（运算内容））
**小数运算**
例子：
[dmtsai@study bin]$ echo "123.123*55.9" &#124; bc
6882.575
### script执行方式差异（source, sh script, ./script）
**利用直接执行的方式来执行 script**
不论是绝对路径/相对路径还是 ${PATH} 内），或者是利用 bash （或 sh） 来下达脚本时， 该 script 都会使用一个新的 bash 环境来执行脚本内的指令！也就是说，使用这种执行方式时， 其实 script 是在子程序的 bash 内执行的！（父程序不会含有子程序变量）
**利用 source 来执行脚本：**
在父程序中执行
如果你使用 source 来执行指令那就不一样了！同样的脚本我们来执行看看：showname.sh 会在父程序中执行的，因此各项动作都会在原本的 bash 内生效！这也是为啥
你不登出系统而要让某些写入 ~/.bashrc 的设置生效时，需要使用“ source ~/.bashrc ”而不能
使用“ bash ~/.bashrc ”是一样的啊
## 善用判断式
### test指令测试功能
|测试的标志 |代表意义|
|----------|------------|
| 关于某个文件名的“文件类型”判断，如 test -e filename 表示存在否| |
|-e| 该“文件名”是否存在？（常用）|
|-f| 该“文件名”是否存在且为文件（file）？（常用）|
|-d| 该“文件名”是否存在且为目录（directory）？（常
用）|
|-b| 该“文件名”是否存在且为一个 block device 设备？|
|-c|该“文件名”是否存在且为一个 character device 设备？|
|-S |该“文件名”是否存在且为一个 Socket 文件？|
|-p |该“文件名”是否存在且为一个 FIFO （pipe） 文件？|
### 利用判断符号[]
我们还可以利用判断符号“ [ ] ”（就是中括号啦） 来
进行数据的判断呢！ 举例来说，如果我想要知道 ${HOME} 这个变量是否为空的，可以这样
做：
```cmd
[dmtsai@study ~]$ [ -z "${HOME}" ] ; echo $?
```
### Shell script 的默认变量（$0, $1...）
其实 script 针对参数已经有设置好一些变量名称了！对应如下：
/path/to/scriptname opt1 opt2 opt3 opt4
$0 $1 $2 $3 $4
```cmd
$# ：代表后接的参数“个数”，以上表为例这里显示为“ 4 ”；
$@ ：代表“ "$1" "$2" "$3" "$4" ”之意，每个变量是独立的（用双引号括起来）；
$* ：代表“ "$1<u>c</u>$2<u>c</u>$3<u>c</u>$4" ”，其中 <u>c</u> 为分隔字符，默
认为空白键， 所以本例中代表“ "$1 $2 $3 $4" ”之意。
```
## 条件判断式
### if...then
**格式**
if [ 条件判断式 ]; then
当条件判断式成立时，可以进行的指令工作内容；
fi &lt;==将 if 反过来写，就成为 fi 啦！结束 if 之意！
**多条件判断**
if [ 条件判断式一 ]; then
当条件判断式一成立时，可以进行的指令工作内容；
elif [ 条件判断式二 ]; then
当条件判断式二成立时，可以进行的指令工作内容；
else
当条件判断式一与二均不成立时，可以进行的指令工作内容；
fi

###  利用 case ..... esac 判断
**格式**
```cmd
case $变量名称 in &lt;==关键字为 case ，还有变量前有钱字号
"第一个变量内容"） &lt;==每个变量内容建议用双引号括起来，关键字则为小括号 ）
程序段
;; &lt;==每个类别结尾使用两个连续的分号来处理！
"第二个变量内容"）
程序段
;;
*） &lt;==最后一个变量内容都会用 * 来代表所有其他值
不包含第一个变量内容与第二个变量内容的其他程序执行段
exit 1
;;
esac &lt;==最终的 case 结尾！“反过来写”思考一下！
```
###  利用 function 功能
**格式**
function fname（） {
程序段
}
```cmd
[dmtsai@study bin]$ vim show123-2.sh
#!/bin/bash
# Program:
# Use function to repeat information.
# History:
# 2015/07/17 VBird First release
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
function printit（）{
echo -n "Your choice is " # 加上 -n 可以不断行继续在同一行显示
}
echo "This program will print your selection !"
case ${1} in
"one"）
**printit**; echo ${1} &#124; tr 'a-z' 'A-Z' # 将参数做大小写转换！
;;
"two"）
**printit**; echo ${1} &#124; tr 'a-z' 'A-Z'
;;
"three"）
**printit**; echo ${1} &#124; tr 'a-z' 'A-Z'
;;
*）
echo "Usage ${0} {one&#124;two&#124;three}"
;;
esac
```
## 循环
### while do done, until do done （不定循环）

while [ condition ] &lt;==中括号内的状态就是判断式
do &lt;==do 是循环的开始！
程序段落
done &lt;==done 是循环的结束


它说的是“当 condition 条件成立时，就终止循环， 否则就持续，进行循环的程序段
until [ condition ]
do
程序段落
done


### for...do...done （固定循环）
for var in con1 con2 con3 ...
do
程序段
done
```shell
[dmtsai@study bin]$ vim pingip.sh
#!/bin/bash
# Program
# Use ping command to check the network's PC state.
# History
# 2015/07/17 VBird first release
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
network="192.168.1" # 先定义一个网域的前面部分！
for sitenu in $（seq 1 100） # seq 为 sequence（连续） 的缩写之意
do
# 下面的程序在取得 ping 的回传值是正确的还是失败的！
ping -c 1 -w 1 ${network}.${sitenu} &&gt; /dev/null && result=0 &#124;&#124; result=1
# 开始显示结果是正确的启动 （UP） 还是错误的没有连通 （DOWN）
if [ "${result}" == 0 ]; then
echo "Server ${network}.${sitenu} is UP."
else
echo "Server ${network}.${sitenu} is DOWN."
fi
done
```
### for...do...done 的数值处理
**例子**
for （（ 初始值; 限制值; 执行步阶 ））
do
程序段
done
### 搭配乱数与阵列的实验
```cmd
[dmtsai@study bin]$ vim what_to_eat.sh
#!/bin/bash
# Program:
# Try do tell you what you may eat.
# History:
# 2015/07/17 VBird First release
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
eat[1]="卖当当漢堡包" # 写下你所收集到的店家！
eat[2]="肯爷爷炸鸡"
eat[3]="彩虹日式便当"
eat[4]="越油越好吃大雅"
eat[5]="想不出吃啥学餐"
eat[6]="太师父便当"
eat[7]="池上便当"
eat[8]="怀念火车便当"
eat[9]="一起吃方便面"
eatnum=9 # 需要输入有几个可用的餐厅数！
check=$（（ ${RANDOM} * ${eatnum} / 32767 + 1 ））
echo "your may eat ${eat[${check}]}"
```
### shell script 的追踪与 debug
scripts 在执行之前，最怕的就是出现语法错误的问题了！那么我们如何 debug 呢？有没有办
法不需要通过直接执行该 scripts 就可以来判断是否有问题呢？呵呵！当然是有的！我们就直
接以 bash 的相关参数来进行判断吧！
```cmd
[dmtsai@study ~]$ sh [-nvx] scripts.sh
选项与参数：
-n ：不要执行 script，仅查询语法的问题；
-v ：再执行 sccript 前，先将 scripts 的内容输出到屏幕上；
-x ：将使用到的 script 内容显示到屏幕上，这是很有用的参数！
```