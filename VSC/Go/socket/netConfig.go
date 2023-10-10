package main

import (
    "fmt"
    "net"
)

func main() {
    interfaces, err := net.Interfaces()
    if err != nil {
        fmt.Println(err)
        return
    }
	for _, i := range interfaces {
        fmt.Printf("Interface: %v\n", i.Name)
        _, err := net.InterfaceByName(i.Name)
        if err != nil {
            fmt.Println(err)
        }
	}
}