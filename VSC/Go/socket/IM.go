package main

import (
	"fmt"
	"net"
	"runtime"
	"strings"
	"time"
)
type Client struct{
	C chan string //管道
	Addr string  //地址
	Name string //用户名
}
// 储存在线人员信息
var onlineMap =make(map[string]Client)
var massage = make(chan string)  
func Manager(){
	for {
		msg := <-massage //读取Massage中的消息
		for _, data := range onlineMap {
			data.C <- msg //将消息广播到列表中的每一项
		}
	}

}
func MakeMsg(client Client,msg string )(buf string){
	return "["+client.Addr+"]  "+client.Name+" : "+msg
}
func Write2MsgClient(client Client,conn net.Conn){
	massage<-MakeMsg(client,"login")

	for data := range client.C {
		conn.Write([]byte(data + "\n"))
	}
	fmt.Println(client.Name, "子go程结束！")
}


func HandlerConnet(conn net.Conn) {
	defer conn.Close()
	clientAddr := conn.RemoteAddr().String()                    //获取网络地址
	client := Client{make(chan string),clientAddr, clientAddr} //创建客户端对应的地址
	onlineMap[clientAddr] = client                              //添加客户端到在线列表
	go Write2MsgClient(client, conn)                             //开启网络写 go程
	msgOnline := MakeMsg(client, "login")                   //上线信息
	massage <- msgOnline                                        //向Massage 全局变量写数据
	OnLineState := make(chan bool)                              //在线状态
	chatState := make(chan bool)                                //聊天状态
	go func() { // 开启新线程链接用户
		for {
			buffer := make([]byte, 4096)
			// 读取传来的信息
			n, err := conn.Read(buffer)
			if n == 0 {
				//	fmt.Println("客户端已经关闭！")
				OnLineState <- false
				return
			}
			if err != nil {
				fmt.Println(err)
				return
			}
			recMsg := string(buffer[:n-1]) // nc 命令最末尾为： /n  (其他测试根据实际情况)
			//查询在线用户
			if len(recMsg) == 3 && recMsg == "who" {
				for _, value := range onlineMap {
					senClient := value.Addr + value.Name + "\n"
					conn.Write([]byte(senClient))
				}
			} else if len(recMsg) >= 7 && recMsg[:7] == "rename|" { //重命名
				client.Name=strings.Split(recMsg,"|")[1]
				onlineMap[clientAddr] = client //存储修改信息到用户列表
				conn.Write([]byte("rename is OK!"))
			} else {
				sendMsg := MakeMsg(client, string(buffer[:n])) //发送数据信息
				massage <- sendMsg                                 //执行发送操作
			}
			chatState <- true
		}
	}()
	for {
		runtime.GC()
		// select 是 Go 中的一个控制结构，类似于 switch 语句。
		// select 语句只能用于通道操作，每个 case 必须是一个通道操作，要么是发送要么是接收。
		select {
		case <-OnLineState:
			delete(onlineMap, clientAddr)
			massage <- MakeMsg(client, " is Leaved")
			close(client.C) //结束子go程: WiriteToClient
			return
		case <-time.After(time.Second * 20)://定时器
			delete(onlineMap, clientAddr)
			massage <- MakeMsg(client, " is outtime")
			/*
			在子go程中开辟的新go程，新go程不会随着子go程的结束而结束。
			原因：go程共享堆，不共享栈。子go程退出，栈退出，但堆还在。
			在主go程中开辟的新go程，新go程会随着主go程的结束而结束。
			原因：go程共享堆，主go程退出，堆也会退出。所以新go程会被退出。
			*/
			close(client.C) //结束子go程: WiriteToClient   channel被关闭，对应的 for range会被退出。
			return
			/*
			//有用户信息 ，重置<-time.After(time.Second * 20)
			主要是select特性：有一个case执行，即退出，再次进入，从新开始，
			这时<-time.After(time.Second * 20)被重置
			*/
		case <-chatState:
		}
	}
}
func main() {
	//主go程
	listener, err := net.Listen("tcp", "127.0.0.1:8081")
	if err != nil {
		fmt.Println("net.Listen err:", err)
		return
	}
	defer listener.Close()
	go Manager()
	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("listener.Accept err:", err)
			continue
		}
		//defer conn.Close()
		go HandlerConnet(conn)
	}
}
