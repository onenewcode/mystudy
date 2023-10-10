package main

import (

	"fmt"
	"net"

)

func main() {
    conn, err := net.Dial("tcp", "127.0.0.1:20000")
    if err != nil {
        fmt.Println("err :", err)
        return
    }
    defer conn.Close() // 关闭连接
    // inputReader := bufio.NewReader(os.Stdin)//获取键盘输入
    for i := 0; i < 20; i++ {
        // input, _ := inputReader.ReadString('\n') // 读取用户输入
        // inputInfo := strings.Trim(input, "\r\n")
        // if strings.ToUpper(inputInfo) == "Q" { // 如果输入q就退出
        //     return
        // }
        msg:="dsfsdfdrfgdsfgds"
        _, err = conn.Write([]byte(msg)) // 发送数据
        if err != nil {
            return
        }
        // 可防止zhan'bao
        // buf := [1024]byte{}
        // n, err := conn.Read(buf[:])
        // if err != nil {
        //     fmt.Println("recv failed, err:", err)
        //     return
        // }
        // fmt.Println(string(buf[:n]))
    }
}   