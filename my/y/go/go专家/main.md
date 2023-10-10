# 常见数据结构实现原理
## chan
```go
 type hchan struct {
qcount uint // 当前队列中剩余元素个数
dataqsiz uint // 环形队列长度，即可以存放的元素个数
buf unsafe.Pointer // 环形队列指针
elemsize uint16 // 每个元素的大小
closed uint32 // 标识关闭状态
elemtype *_type // 元素类型
sendx uint // 队列下标，指示元素写入时存放到队列中的位置   
recvx uint // 队列下标，指示元素从队列的该位置读出
recvq waitq // 等待读消息的goroutine队列
sendq waitq // 等待写消息的goroutine队列
lock mutex // 互斥锁，chan不允许并发读写
}
```

<img src="img\屏幕截图 2023-05-22 092541.png">

dataqsiz指示了队列长度为6，即可缓存6个元素；
buf指向队列的内存，队列中还剩余两个元素；
qcount表示队列中还有两个元素；
sendx指示后续写入的数据存储的位置，取值[0, 6)；
recvx指示从该位置读取数据, 取值[0, 6)；

因读阻塞的goroutine会被向channel写入数据的goroutine唤醒；
因写阻塞的goroutine会被从channel读数据的goroutine唤醒；

一个channel只能传递一种类型的值，类型信息存储在hchan数据结构中。
<img src="img/屏幕截图 2023-05-22 133002.png">

<img src="img/屏幕截图 2023-05-22 133412.png">

### 关闭channel
关闭channel时会把recvq中的G全部唤醒，本该写入G的数据位置为nil。把sendq中的G全部唤醒，但这些G会panic。
1. 关闭值为nil的channel
2. 关闭已经被关闭的channel
3. 向已经关闭的channel写数据
### 常见用法
#### 单向channel
func readChan(chanName <-chan int)： 通过形参限定函数内部只能从channel中读取数据
func writeChan(chanName chan<- int)： 通过形参限定函数内部只能向channel中写入数据
##### select
```go
package main
import (
"fmt"
"time"
)
func addNumberToChan(chanName chan int) {
for {
 chanName <- 1
 time.Sleep(1 * time.Second)
 }
 }

 func main() {
 var chan1 = make(chan int, 10)
 var chan2 = make(chan int, 10)

 go addNumberToChan(chan1)
 go addNumberToChan(chan2)

 for {
 select {
 case e := <- chan1 :
 fmt.Printf("Get element from chan1: %d\n", e)
 case e := <- chan2 :
 fmt.Printf("Get element from chan2: %d\n", e)
 default:
 fmt.Printf("No element in chan1 and chan2.\n")
 time.Sleep(1 * time.Second)
 }
 }
 }
```
### range
```go
func chanRange(chanName chan int) {
 for e := range chanName {
 fmt.Printf("Get element from chan: %d\n", e)
 }
 }
 ```
 ### Slice
 #### Slice实现原理
 ```go
 type slice struct {
array unsafe.Pointer
len int
cap int
}
```