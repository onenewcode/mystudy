package main

import "fmt"

func main() {
	slice := []int{0, 1, 2, 3}
	fmt.Println(cap(slice))
	s1 := slice[:]
	// p := append(s1, 1, 2)
	s1[1] = 3
	fmt.Println(cap(s1))
	// fmt.Println(p)
	fmt.Print(slice)
	fmt.Print(s1)
}
