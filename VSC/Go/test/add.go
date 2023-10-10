package main



func main() {
	x := 123
	n, s := 0x1234, "Hello, World!"
	var b = 123
	b := 1234 //会出现错误no new variables on left side of := 。因为在上一行已经定义过变量
	(x, n, s, b)
}
