# 黑马
<img src="img\屏幕截图 2023-05-23 155132.png">

<img src="img\屏幕截图 2023-05-23 155200.png">

<img src="img\屏幕截图 2023-05-23 160727.png">


## 进程与线程

### 进程
- 程序由指令和数据组成，但这些指令要运行，数据要读写，就必须将指令加载至 CPU，数据加载至内存。在指令运行过程中还需要用到磁盘、网络等设备。进程就是用来加载指令、管理内存、管理 IO 的
- 当一个程序被运行，从磁盘加载这个程序的代码至内存，这时就开启了一个进程。
- 进程就可以视为程序的一个实例。大部分程序可以同时运行多个实例进程（例如记事本、画图、浏览器等），也有的程序只能启动一个实例进程（例如网易云音乐、360 安全卫士等）
### 线程
一个进程之内可以分为一到多个线程。
一个线程就是一个指令流，将指令流中的一条条指令以一定的顺序交给 CPU 执行
Java 中，线程作为最小调度单位，进程作为资源分配的最小单位。 在 windows 中进程是不活动的，只是作
为线程的容器



## 应用
异步或者分块调用
## java 线程



### 创建和运行线程
#### 直接使用 Thread


```java
// 构造方法的参数是给线程指定名字，推荐
Thread t1 = new Thread("t1") {
 @Override
 // run 方法内实现了要执行的任务
 public void run() {
 log.debug("hello");
 }
};
t1.start();
```
#### 使用 Runnable 配合 Thread
```java
Runnable runnable = new Runnable() {
 public void run(){
 // 要执行的任务
 }
};
// 创建线程对象
Thread t = new Thread( runnable );
// 启动线程
t.start(); 
```
#### FutureTask 配合 Thread
```java
// 创建任务对象
FutureTask<Integer> task3 = new FutureTask<>(() -> {
 log.debug("hello");
 return 100;
});
// 参数1 是任务对象; 参数2 是线程名字，推荐
new Thread(task3, "t3").start();
// 主线程阻塞，同步等待 task 执行完毕的结果
Integer result = task3.get();
log.debug("结果是:{}", result);
```
### 观察多个线程同时运行

**windows**
- 任务管理器可以查看进程和线程数，也可以用来杀死进程
- tasklist 查看进程
- taskkill 杀死进程
**linux**
- ps -fe 查看所有进程
- ps -fT -p <PID> 查看某个进程（PID）的所有线程
- kill 杀死进程
- top 按大写 H 切换是否显示线程
- top -H -p <PID> 查看某个进程（PID）的所有线程
**Java**
- jps 命令查看所有 Java 进程
- jstack <PID> 查看某个 Java 进程（PID）的所有线程状态
- jconsole 来查看某个 Java 进程中线程的运行情况（图形界面）



**jconsole 远程监控配置**
- 需要以如下方式运行你的 java 类
```bash
java -Djava.rmi.server.hostname=`ip地址` -Dcom.sun.management.jmxremote -
Dcom.sun.management.jmxremote.port=`连接端口` -Dcom.sun.management.jmxremote.ssl=是否安全连接 -
Dcom.sun.management.jmxremote.authenticate=是否认证 java类
```
修改 /etc/hosts 文件将 127.0.0.1 映射至主机名
如果要认证访问，还需要做如下步骤
复制 jmxremote.password 文件
修改 jmxremote.password 和 jmxremote.access 文件的权限为 600 即文件所有者可读写
连接时填入 controlRole（用户名），R&D（密码）


### 原理之线程运行


#### 栈与栈帧
Java Virtual Machine Stacks （Java 虚拟机栈）
其实就是线程，每个线程启动后，虚拟机就会为其分配一块栈内存。
 - 每个栈由多个栈帧（Frame）组成，对应着每次方法调用时所占用的内存
 - 每个线程只能有一个活动栈帧，对应着当前正在执行的那个方法
**线程上下文切换（Thread Context Switch）**
因为以下一些原因导致 cpu 不再执行当前的线程，转而执行另一个线程的代码
- 线程的 cpu 时间片用完
- 垃圾回收
- 有更高优先级的线程需要运行
- 线程自己调用了 sleep、yield、wait、join、park、synchronized、lock 等方法
当 Context Switch 发生时，需要由操作系统保存当前线程的状态，并恢复另一个线程的状态，Java 中对应的概念
就是程序计数器（Program Counter Register），它的作用是记住下一条 jvm 指令的执行地址，是线程私有的
- 状态包括程序计数器、虚拟机栈中每个栈帧的信息，如局部变量、操作数栈、返回地址等
- Context Switch 频繁发生会影响性能

##  常见方法

|方法名 |static |功能说明 |注意|
|------------|-----------|--------|-------|--------|
|start()||启动一个新线程，在新的线程运行 run 方法中的代码|start 方法只是让线程进入就绪，里面代码不一定立刻运行（CPU 的时间片还没分给它）。每个线程对象的start方法只能调用一次，如果调用了多次会出现IllegalThreadStateException|
|run()||新线程启动后会调用的方法|如果在构造 Thread 对象时传递了 Runnable 参数，则线程启动后会调用 Runnable 中的 run 方法，否则默认不执行任何操作。但可以创建 Thread 的子类对象，来覆盖默认行为|
|join()||等待线程运行结束| | |
|join(long n)||等待线程运行结束,最多等待 n 毫秒||
|getId() ||获取线程长整型的 id |id 唯一|
|getName() |  |获取线程名setName(String)|   修改线程名||
|getPriority()||   获取线程优先级||
|setPriority(int)||   修改线程优先级 |java中规定线程优先级是1~10 的整数，较大的优先级能提高该线程被 CPU 调度的机率|
|getState()|| 获取线程状态|Java 中线程状态是用 6 个 enum 表示，分别为：NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED|

|isInterrupted()||   判断是否被打断，| 不会清除 打断标记|
|isAlive()||线程是否存活（还没有运行完毕）||
|interrupt()||   打断线程|如果被打断线程正在 sleep，wait，join 会导致被打断
的线程抛出 InterruptedException，并清除 打断标记 ；如果打断的正在运行的线程，则会设置 打断标记 ；park 的线程被打断，也会设置 打断标记|
|interrupted()| static| 判断当前线程是否被打断 |会清除 打断标记|
|currentThread()| static| 获取当前正在执行的线程||

|sleep(long n)| static|让当前执行的线程休眠n毫秒，休眠时让出 cpu的时间片给其线程||
|yield()| static|提示线程调度器让出当前线程对CPU的使用|主要是为了测试和调试|
### sleep 与 yield
**sleep**
1. 调用 sleep 会让当前线程从 Running 进入 Timed Waiting 状态（阻塞）
2. 其它线程可以使用 interrupt 方法打断正在睡眠的线程，这时 sleep 方法会抛出 InterruptedException
3. 睡眠结束后的线程未必会立刻得到执行
4. 建议用 TimeUnit 的 sleep 代替 Thread 的 sleep 来获得更好的可读性
**yield**
1. 调用 yield 会让当前线程从 Running 进入 Runnable 就绪状态，然后调度执行其它线程
2. 具体的实现依赖于操作系统的任务调度器
###  interrupt 方法详解

打断 sleep，wait，join 的线程asxASWERTRFQW

打断正常运行的线程
打断正常运行的线程, 不会清空打断状态


打断 park 线程
打断 park 线程, 不会清空打断状态

### 主线程与守护线程
默认情况下，Java 进程需要等待所有线程都运行结束，才会结束。有一种特殊的线程叫做守护线程，只要其它非守护线程运行结了，即使守护线程的代码没有执行完，也会强制结束。

### 五种状态

<IMG SRC="img\屏幕截图 2023-05-23 184435.png">


【初始状态】仅是在语言层面创建了线程对象，还未与操作系统线程关联
【可运行状态】（就绪状态）指该线程已经被创建（与操作系统线程关联），可以由 CPU 调度执行
【运行状态】指获取了 CPU 时间片运行中的状态
  - 当 CPU 时间片用完，会从【运行状态】转换至【可运行状态】，会导致线程的上下文切换
【阻塞状态】
  - 如果调用了阻塞 API，如 BIO 读写文件，这时该线程实际不会用到 CPU，会导致线程上下文切换，进入
【阻塞状态】
  - 等 BIO 操作完毕，会由操作系统唤醒阻塞的线程，转换至【可运行状态】
- 与【可运行状态】的区别是，对【阻塞状态】的线程来说只要它一直不唤醒，调度器就一直不会考虑
调度它们
【终止状态】表示线程已经执行完毕，生命周期已经结束，不会再转换为其它状态

###  六种状态

<img src="img\屏幕截图 2023-05-24 095305.png">

- NEW 线程刚被创建，但是还没有调用 start() 方法
- RUNNABLE 当调用了 start() 方法之后，注意，Java API 层面的 RUNNABLE 状态涵盖了 操作系统 层面的【可运行状态】、【运行状态】和【阻塞状态】（由于 BIO 导致的线程阻塞，在 Java 里无法区分，仍然认为
是可运行）
- BLOCKED ， WAITING ， TIMED_WAITING 都是 Java API 层面对【阻塞状态】的细分，
- TERMINATED 当线程代码运行结束



## 共享模型之管程
### 问题
```java
static int counter = 0;
public static void main(String[] args) throws InterruptedException {
 Thread t1 = new Thread(() -> {
 for (int i = 0; i < 5000; i++) {
 counter++;
 }
 }, "t1");
 Thread t2 = new Thread(() -> {
 for (int i = 0; i < 5000; i++) {
 counter--;
 }
 }, "t2");
 t1.start();
 t2.start();
 t1.join();
 t2.join();
 log.debug("{}",counter);
}
```
以上的结果可能是正数、负数、零。为什么呢？因为 Java 中对静态变量的自增，自减并不是原子操作，要彻底理解，必须从字节码来进行分析
### synchronized 解决方案

```java

synchronized(对象) // 线程1， 线程2(blocked)
{
 临界区
}



static int counter = 0;
static final Object room = new Object();
public static void main(String[] args) throws InterruptedException {
 Thread t1 = new Thread(() -> {
 for (int i = 0; i < 5000; i++) {
 synchronized (room) {
 counter++;
 }
 }
 }, "t1");
 Thread t2 = new Thread(() -> {
 for (int i = 0; i < 5000; i++) {
 synchronized (room) {
 counter--;
 }
 }
 }, "t2");
 t1.start();
 t2.start();
 t1.join();
 t2.join();
 log.debug("{}",counter);
}
```
###  变量的线程安全分析
- 成员变量和静态变量是否线程安全？
- 如果它们没有共享，则线程安全
- 如果它们被共享了，根据它们的状态是否能够改变，又分两种情况
  - 如果只有读操作，则线程安全
  - 如果有读写操作，则这段代码是临界区，需要考虑线程安全
- 局部变量是否线程安全？
- 局部变量是线程安全的
- 但局部变量引用的对象则未必
  - 如果该对象没有逃离方法的作用访问，它是线程安全的
  - 如果该对象逃离方法的作用范围，需要考虑线程安全

### Monitor 概念




### wait notify 的正确姿势
sleep 是 Thread 方法，而 wait 是 Object 的方法 
sleep 不需要强制和 synchronized 配合使用，但 wait 需要和 synchronized 一起用 
sleep 在睡眠的同时，不会释放对象锁的，但 wait 在等待的时候会释放对象锁  它们状态 TIMED_WAITING
















































































































































































# 线程安全
如果多线程访问同一一个变量，程序就会存在隐患，有三种方法解决它：
- 不要跨线程共享变量
- 使用状态变量为不可变
- 在任何访问状态变量的时候使用同步
## 什么是线程安全
对于 线程安全类的实例进行顺序或并发的一系列操作，都不会导致实例处于无效状态。
## 锁
### 内部锁
synchronized
synchronized块由两部分的：锁对象的引用，以及所锁保护的代码块。
内部锁在Java中扮演互斥锁的角色
### 重进入（Reentrancy）
重进入的实例实现通过为每个锁关联一个请求计数和一个占有他的线程。当计数为零时，认为锁是未被占有的。线程请求一个未被占有的的锁时，jvm将记录锁的战友者，并将请求技术值为1，如果同一线程再次请求这个锁，计数递增。每次占有线程退出同步块，计数器递减，直到计数器0为止线程释放锁。
## 用锁保护状态
操作共享状态的符合操作必须是原子的，以避免竞争，比如怎加递增命中计数器（读-改-写）或者惰性初始化（检查在运行）。
 
每个共享变量都需要唯一一个确定的锁保护，而维护者应该清楚这个锁。
# 共享对象
## 可见性
<img src="img\屏幕截图 2023-05-23 154532.png">

### 过期数据
