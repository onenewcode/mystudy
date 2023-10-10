package main

import (
	"fmt"
	"time"
)
func main(){
	names:=[]string{"sf","dv","dvx","dxv"}
	for _,name :=range names{//go语句被封装在一个函数内，在for语句执行完之后执行
		go func(who string){
			fmt.Printf("hello, %s\n",who)
		}(name)//
		
	}
	time.Sleep(time.Millisecond)
}