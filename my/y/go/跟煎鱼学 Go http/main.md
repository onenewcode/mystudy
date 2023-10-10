# http应用
## Gin搭建Blog API's
但是本系列选用 [go-ini/ini](https://ini.unknwon.io/)

### 初始化项目目录
在前一章节中，我们初始化了一个 go-gin-example 项目，接下来我们需要继续新增如下目录结构：

go-gin-example/
├── conf
├── middleware
├── models
├── pkg
├── routers
└── runtime
- conf：用于存储配置文件
- middleware：应用中间件
- models：应用数据库模型
- pkg：第三方包
- routers 路由逻辑处理
- runtime：应用运行时数据


### 初始项目数据库
新建 blog 数据库，编码为utf8_general_ci，在 blog 数据库下，新建以下表

1、 标签表
```sql
CREATE TABLE `blog_tag` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT '' COMMENT '标签名称',
  `created_on` int(10) unsigned DEFAULT '0' COMMENT '创建时间',
  `created_by` varchar(100) DEFAULT '' COMMENT '创建人',
  `modified_on` int(10) unsigned DEFAULT '0' COMMENT '修改时间',
  `modified_by` varchar(100) DEFAULT '' COMMENT '修改人',
  `deleted_on` int(10) unsigned DEFAULT '0',
  `state` tinyint(3) unsigned DEFAULT '1' COMMENT '状态 0为禁用、1为启用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章标签管理';
```
2、 文章表
```sql
CREATE TABLE `blog_article` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tag_id` int(10) unsigned DEFAULT '0' COMMENT '标签ID',
  `title` varchar(100) DEFAULT '' COMMENT '文章标题',
  `desc` varchar(255) DEFAULT '' COMMENT '简述',
  `content` text,
  `created_on` int(11) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT '' COMMENT '创建人',
  `modified_on` int(10) unsigned DEFAULT '0' COMMENT '修改时间',
  `modified_by` varchar(255) DEFAULT '' COMMENT '修改人',
  `deleted_on` int(10) unsigned DEFAULT '0',
  `state` tinyint(3) unsigned DEFAULT '1' COMMENT '状态 0为禁用1为启用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='文章管理';
```
3、 认证表
```sql
CREATE TABLE `blog_auth` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT '' COMMENT '账号',
  `password` varchar(50) DEFAULT '' COMMENT '密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `blog`.`blog_auth` (`id`, `username`, `password`) VALUES (null, 'test', 'test123456');
```
### 编写项目配置包
在 go-gin-example 应用目录下，拉取 go-ini/ini 的依赖包

接下来我们需要编写基础的应用配置文件，在 go-gin-example 的conf目录下新建app.ini文件，写入内容：
```ini
#debug or release
RUN_MODE = debug

[app]
PAGE_SIZE = 10
JWT_SECRET = 23347$040412

[server]
HTTP_PORT = 8000
READ_TIMEOUT = 60
WRITE_TIMEOUT = 60

[database]
TYPE = mysql
USER = 数据库账号
PASSWORD = 数据库密码
#127.0.0.1:3306
HOST = 数据库IP:数据库端口号
NAME = blog
TABLE_PREFIX = blog_
```
建立调用配置的setting模块，在go-gin-example的pkg目录下新建setting目录（注意新增 replace 配置），新建 setting.go 文件，写入内容：
```go
package setting

import (
    "log"
    "time"

    "github.com/go-ini/ini"
)

var (
    Cfg *ini.File

    RunMode string

    HTTPPort int
    ReadTimeout time.Duration
    WriteTimeout time.Duration

    PageSize int
    JwtSecret string
)

func init() {
    var err error
    Cfg, err = ini.Load("conf/app.ini")
    if err != nil {
        log.Fatalf("Fail to parse 'conf/app.ini': %v", err)
    }

    LoadBase()
    LoadServer()
    LoadApp()
}

func LoadBase() {
    RunMode = Cfg.Section("").Key("RUN_MODE").MustString("debug")
}

func LoadServer() {
    sec, err := Cfg.GetSection("server")
    if err != nil {
        log.Fatalf("Fail to get section 'server': %v", err)
    }

    HTTPPort = sec.Key("HTTP_PORT").MustInt(8000)
    ReadTimeout = time.Duration(sec.Key("READ_TIMEOUT").MustInt(60)) * time.Second
    WriteTimeout =  time.Duration(sec.Key("WRITE_TIMEOUT").MustInt(60)) * time.Second
}

func LoadApp() {
    sec, err := Cfg.GetSection("app")
    if err != nil {
        log.Fatalf("Fail to get section 'app': %v", err)
    }

    JwtSecret = sec.Key("JWT_SECRET").MustString("!@)*#)!@U#@*!@!)")
    PageSize = sec.Key("PAGE_SIZE").MustInt(10)
}
```
当前的目录结构：


### 编写 API 错误码包
建立错误码的e模块，在go-gin-example的pkg目录下新建e目录（注意新增 replace 配置），新建code.go和msg.go文件，写入内容：

1、 code.go：
```go
package e

const (
    SUCCESS = 200
    ERROR = 500
    INVALID_PARAMS = 400

    ERROR_EXIST_TAG = 10001
    ERROR_NOT_EXIST_TAG = 10002
    ERROR_NOT_EXIST_ARTICLE = 10003

    ERROR_AUTH_CHECK_TOKEN_FAIL = 20001
    ERROR_AUTH_CHECK_TOKEN_TIMEOUT = 20002
    ERROR_AUTH_TOKEN = 20003
    ERROR_AUTH = 20004
)
```
2、 msg.go：
```go
package e

var MsgFlags = map[int]string {
    SUCCESS : "ok",
    ERROR : "fail",
    INVALID_PARAMS : "请求参数错误",
    ERROR_EXIST_TAG : "已存在该标签名称",
    ERROR_NOT_EXIST_TAG : "该标签不存在",
    ERROR_NOT_EXIST_ARTICLE : "该文章不存在",
    ERROR_AUTH_CHECK_TOKEN_FAIL : "Token鉴权失败",
    ERROR_AUTH_CHECK_TOKEN_TIMEOUT : "Token已超时",
    ERROR_AUTH_TOKEN : "Token生成失败",
    ERROR_AUTH : "Token错误",
}

func GetMsg(code int) string {
    msg, ok := MsgFlags[code]
    if ok {
        return msg
    }

    return MsgFlags[ERROR]
}
```
### 编写工具包
在go-gin-example的pkg目录下新建util目录（注意新增 replace 配置），并拉取com的依赖包，如下：
```s
$ go get -u github.com/unknwon/com
```
编写分页页码的获取方法
在util目录下新建pagination.go，写入内容：
```go
package util

import (
    "github.com/gin-gonic/gin"
    "github.com/unknwon/com"

    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

func GetPage(c *gin.Context) int {
    result := 0
    page, _ := com.StrTo(c.Query("page")).Int()
    if page > 0 {
        result = (page - 1) * setting.PageSize
    }

    return result
}
```
### 编写 models init
拉取gorm的依赖包，如下：

$ go get -u github.com/jinzhu/gorm
拉取mysql驱动的依赖包，如下：

$ go get -u github.com/go-sql-driver/mysql
完成后，在go-gin-example的models目录下新建models.go，用于models的初始化使用
```go
package models

import (
    "log"
    "fmt"

    "github.com/jinzhu/gorm"
    _ "github.com/jinzhu/gorm/dialects/mysql"

    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

var db *gorm.DB

type Model struct {
    ID int `gorm:"primary_key" json:"id"`
    CreatedOn int `json:"created_on"`
    ModifiedOn int `json:"modified_on"`
}

func init() {
    var (
        err error
        dbType, dbName, user, password, host, tablePrefix string
    )

    sec, err := setting.Cfg.GetSection("database")
    if err != nil {
        log.Fatal(2, "Fail to get section 'database': %v", err)
    }

    dbType = sec.Key("TYPE").String()
    dbName = sec.Key("NAME").String()
    user = sec.Key("USER").String()
    password = sec.Key("PASSWORD").String()
    host = sec.Key("HOST").String()
    tablePrefix = sec.Key("TABLE_PREFIX").String()

    db, err = gorm.Open(dbType, fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8&parseTime=True&loc=Local",
        user,
        password,
        host,
        dbName))

    if err != nil {
        log.Println(err)
    }

    gorm.DefaultTableNameHandler = func (db *gorm.DB, defaultTableName string) string  {
        return tablePrefix + defaultTableName;
    }

    db.SingularTable(true)
    db.LogMode(true)
    db.DB().SetMaxIdleConns(10)
    db.DB().SetMaxOpenConns(100)
}

func CloseDB() {
    defer db.Close()
}
```
### 编写项目启动、路由文件
```go
package main

import (
    "fmt"
    "net/http"

    "github.com/gin-gonic/gin"

    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

func main() {
    router := gin.Default()
    router.GET("/test", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "test",
        })
    })

    s := &http.Server{
        Addr:           fmt.Sprintf(":%d", setting.HTTPPort),
        Handler:        router,
        ReadTimeout:    setting.ReadTimeout,
        WriteTimeout:   setting.WriteTimeout,
        MaxHeaderBytes: 1 << 20,
    }

    s.ListenAndServe()
}
```
执行go run main.go，查看命令行是否显示
```bash
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:    export GIN_MODE=release
 - using code:    gin.SetMode(gin.ReleaseMode)

[GIN-debug] GET    /test                     --> main.main.func1 (3 handlers)
在本机执行curl 127.0.0.1:8000/test，检查是否返回{"message":"test"}。
```
### 知识点


#### 标准库

**fmt**:实现了类似 C 语言 printf 和 scanf 的格式化 I/O。格式化动作（’verb’）源自 C 语言但更简单
**net/http**:提供了 HTTP 客户端和服务端的实现
#### Gin
**gin.Default()**：返回 Gin 的type Engine struct{...}，里面包含RouterGroup，相当于创建一个路由Handlers，可以后期绑定各类的路由规则和函数、中间件等
**router.GET(…){…}**：创建不同的 HTTP 方法绑定到Handlers中，也支持 POST、PUT、DELETE、PATCH、OPTIONS、HEAD 等常用的 Restful 方法
**gin.H{…}**：就是一个map[string]interface{}
**gin.Context**：Context是gin中的上下文，它允许我们在中间件之间传递变量、管理流、验证 JSON 请求、响应 JSON 请求等，在gin中包含大量Context的方法，例如我们常用的DefaultQuery、Query、DefaultPostForm、PostForm等等
####  &http.Server 和 ListenAndServe？
1、http.Server：
```go
type Server struct {
    Addr    string
    Handler Handler
    TLSConfig *tls.Config
    ReadTimeout time.Duration
    ReadHeaderTimeout time.Duration
    WriteTimeout time.Duration
    IdleTimeout time.Duration
    MaxHeaderBytes int
    ConnState func(net.Conn, ConnState)
    ErrorLog *log.Logger
}
```
**Addr**：监听的 TCP 地址，格式为:8000
**Handler**：http 句柄，实质为ServeHTTP，用于处理程序响应 HTTP 请求
**TLSConfig**：安全传输层协议（TLS）的配置
**ReadTimeout**：允许读取的最大时间
**ReadHeaderTimeout**：允许读取请求头的最大时间
**WriteTimeout**：允许写入的最大时间
**IdleTimeout**：等待的最大时间
**MaxHeaderBytes**：请求头的最大字节数
**ConnState**：指定一个可选的回调函数，当客户端连接发生变化时调用
**ErrorLog**：指定一个可选的日志记录器，用于接收程序的意外行为和底层系统错误；如果未设置或为nil则默认以日志包的标准日志记录器完成（也就是在控制台输出）
2、 ListenAndServe：
```go
func (srv *Server) ListenAndServe() error {
    addr := srv.Addr
    if addr == "" {
        addr = ":http"
    }
    ln, err := net.Listen("tcp", addr)
    if err != nil {
        return err
    }
    return srv.Serve(tcpKeepAliveListener{ln.(*net.TCPListener)})
}
```
开始监听服务，监听 TCP 网络地址，Addr 和调用应用程序处理连接上的请求。

我们在源码中看到Addr是调用我们在&http.Server中设置的参数，因此我们在设置时要用&，我们要改变参数的值，因为我们ListenAndServe和其他一些方法需要用到&http.Server中的参数，他们是相互影响的。

3、 http.ListenAndServe和 连载一 的r.Run()有区别吗？

我们看看r.Run的实现：
```go
func (engine *Engine) Run(addr ...string) (err error) {
    defer func() { debugPrintError(err) }()

    address := resolveAddress(addr)
    debugPrint("Listening and serving HTTP on %s\n", address)
    err = http.ListenAndServe(address, engine)
    return
}
```
通过分析源码，得知本质上没有区别，同时也得知了启动gin时的监听 debug 信息在这里输出。

4、 为什么 Demo 里会有WARNING？

首先我们可以看下Default()的实现
```go
// Default returns an Engine instance with the Logger and Recovery middleware already attached.
func Default() *Engine {
    debugPrintWARNINGDefault()
    engine := New()
    engine.Use(Logger(), Recovery())
    return engine
}
```
大家可以看到默认情况下，已经附加了日志、恢复中间件的引擎实例。并且在开头调用了debugPrintWARNINGDefault()，而它的实现就是输出该行日志
```go
func debugPrintWARNINGDefault() {
    debugPrint(`[WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.
`)
}
```
而另外一个Running in "debug" mode. Switch to "release" mode in production.，是运行模式原因，并不难理解，已在配置文件的管控下 :-)，运维人员随时就可以修改它的配置。

5、 Demo 的router.GET等路由规则可以不写在main包中吗？

我们发现router.GET等路由规则，在 Demo 中被编写在了main包中，感觉很奇怪，我们去抽离这部分逻辑！

在go-gin-example下routers目录新建router.go文件，写入内容：
```go
package routers

import (
    "github.com/gin-gonic/gin"

    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

func InitRouter() *gin.Engine {
    r := gin.New()

    r.Use(gin.Logger())

    r.Use(gin.Recovery())

    gin.SetMode(setting.RunMode)

    r.GET("/test", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "test",
        })
    })

    return r
}
```
修改main.go的文件内容：
```go
package main

import (
    "fmt"
    "net/http"

    "github.com/EDDYCJY/go-gin-example/routers"
    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

func main() {
    router := routers.InitRouter()

    s := &http.Server{
        Addr:           fmt.Sprintf(":%d", setting.HTTPPort),
        Handler:        router,
        ReadTimeout:    setting.ReadTimeout,
        WriteTimeout:   setting.WriteTimeout,
        MaxHeaderBytes: 1 << 20,
    }

    s.ListenAndServe()
}
```
当前目录结构：

go-gin-example/
├── conf
│   └── app.ini
├── main.go
├── middleware
├── models
│   └── models.go
├── pkg
│   ├── e
│   │   ├── code.go
│   │   └── msg.go
│   ├── setting
│   │   └── setting.go
│   └── util
│       └── pagination.go
├── routers
│   └── router.go
├── runtime

### 编写路由空壳
开始编写路由文件逻辑，在routers下新建api目录，我们当前是第一个 API 大版本，因此在api下新建v1目录，再新建tag.go文件，写入内容：
```go
package v1

import (
    "github.com/gin-gonic/gin"
)

//获取多个文章标签
func GetTags(c *gin.Context) {
}

//新增文章标签
func AddTag(c *gin.Context) {
}

//修改文章标签
func EditTag(c *gin.Context) {
}

//删除文章标签
func DeleteTag(c *gin.Context) {
}
```
### 注册路由
我们打开routers下的router.go文件，修改文件内容为：
```go
package routers

import (
    "github.com/gin-gonic/gin"

    "gin-blog/routers/api/v1"
    "gin-blog/pkg/setting"
)

func InitRouter() *gin.Engine {
    r := gin.New()

    r.Use(gin.Logger())

    r.Use(gin.Recovery())

    gin.SetMode(setting.RunMode)

    apiv1 := r.Group("/api/v1")
    {
        //获取标签列表
        apiv1.GET("/tags", v1.GetTags)
        //新建标签
        apiv1.POST("/tags", v1.AddTag)
        //更新指定标签
        apiv1.PUT("/tags/:id", v1.EditTag)
        //删除指定标签
        apiv1.DELETE("/tags/:id", v1.DeleteTag)
    }

    return r
}
```

### 下载依赖包
首先我们要拉取validation的依赖包，在后面的接口里会使用到表单验证
```go
$ go get -u github.com/astaxie/beego/validation
```
编写标签列表的 models 逻辑
创建models目录下的tag.go，写入文件内容：
```go
package models

type Tag struct {
    Model

    Name string `json:"name"`
    CreatedBy string `json:"created_by"`
    ModifiedBy string `json:"modified_by"`
    State int `json:"state"`
}

func GetTags(pageNum int, pageSize int, maps interface {}) (tags []Tag) {
    db.Where(maps).Offset(pageNum).Limit(pageSize).Find(&tags)

    return
}

func GetTagTotal(maps interface {}) (count int){
    db.Model(&Tag{}).Where(maps).Count(&count)

    return
}
```
我们创建了一个Tag struct{}，用于Gorm的使用。并给予了附属属性json，这样子在c.JSON的时候就会自动转换格式，非常的便利

可能会有的初学者看到return，而后面没有跟着变量，会不理解；其实你可以看到在函数末端，我们已经显示声明了返回值，这个变量在函数体内也可以直接使用，因为他在一开始就被声明了

有人会疑惑db是哪里来的；因为在同个models包下，因此db *gorm.DB是可以直接使用的

### 编写标签列表的路由逻辑
打开routers目录下 v1 版本的tag.go，第一我们先编写获取标签列表的接口

修改文件内容：
```go
package v1

import (
    "net/http"

    "github.com/gin-gonic/gin"
    //"github.com/astaxie/beego/validation"
    "github.com/Unknwon/com"

    "gin-blog/pkg/e"
    "gin-blog/models"
    "gin-blog/pkg/util"
    "gin-blog/pkg/setting"
)

//获取多个文章标签
func GetTags(c *gin.Context) {
    name := c.Query("name")

    maps := make(map[string]interface{})
    data := make(map[string]interface{})

    if name != "" {
        maps["name"] = name
    }

    var state int = -1
    if arg := c.Query("state"); arg != "" {
        state = com.StrTo(arg).MustInt()
        maps["state"] = state
    }

    code := e.SUCCESS

    data["lists"] = models.GetTags(util.GetPage(c), setting.PageSize, maps)
    data["total"] = models.GetTagTotal(maps)

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : data,
    })
}

//新增文章标签
func AddTag(c *gin.Context) {
}

//修改文章标签
func EditTag(c *gin.Context) {
}

//删除文章标签
func DeleteTag(c *gin.Context) {
}
```
- c.Query可用于获取?name=test&state=1这类 URL 参数，而c.DefaultQuery则支持设置一个默认值
- code变量使用了e模块的错误编码，这正是先前规划好的错误码，方便排错和识别记录
- util.GetPage保证了各接口的page处理是一致的
- c *gin.Context是Gin很重要的组成部分，可以理解为上下文，它允许我们在中间件之间传递变量、管理流、验证请求的 JSON 和呈现 JSON 响应


### 编写新增标签的 models 逻辑
接下来我们编写新增标签的接口

打开models目录下的tag.go，修改文件（增加 2 个方法）：

```go
func ExistTagByName(name string) bool {
    var tag Tag
    db.Select("id").Where("name = ?", name).First(&tag)
    if tag.ID > 0 {
        return true
    }

    return false
}

func AddTag(name string, state int, createdBy string) bool{
    db.Create(&Tag {
        Name : name,
        State : state,
        CreatedBy : createdBy,
    })

    return true
}
```
### 编写新增标签的路由逻辑
打开routers目录下的tag.go，修改文件（变动 AddTag 方法）：
```go
package v1

import (
    "log"
    "net/http"

    "github.com/gin-gonic/gin"
    "github.com/astaxie/beego/validation"
    "github.com/Unknwon/com"

    "gin-blog/pkg/e"
    "gin-blog/models"
    "gin-blog/pkg/util"
    "gin-blog/pkg/setting"
)

...

//新增文章标签
func AddTag(c *gin.Context) {
    name := c.Query("name")
    state := com.StrTo(c.DefaultQuery("state", "0")).MustInt()
    createdBy := c.Query("created_by")

    valid := validation.Validation{}
    valid.Required(name, "name").Message("名称不能为空")
    valid.MaxSize(name, 100, "name").Message("名称最长为100字符")
    valid.Required(createdBy, "created_by").Message("创建人不能为空")
    valid.MaxSize(createdBy, 100, "created_by").Message("创建人最长为100字符")
    valid.Range(state, 0, 1, "state").Message("状态只允许0或1")

    code := e.INVALID_PARAMS
    if ! valid.HasErrors() {
        if ! models.ExistTagByName(name) {
            code = e.SUCCESS
            models.AddTag(name, state, createdBy)
        } else {
            code = e.ERROR_EXIST_TAG
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : make(map[string]string),
    })
}
```
用Postman用 POST 访问http://127.0.0.1:8000/api/v1/tags?name=1&state=1&created_by=test，查看code是否返回200及blog_tag表中是否有值，有值则正确。

### 编写 models callbacks
但是这个时候大家会发现，我明明新增了标签，但created_on居然没有值，那做修改标签的时候modified_on会不会也存在这个问题？

为了解决这个问题，我们需要打开models目录下的tag.go文件，修改文件内容（修改包引用和增加 2 个方法）：
```go
package models

import (
    "time"

    "github.com/jinzhu/gorm"
)

...

func (tag *Tag) BeforeCreate(scope *gorm.Scope) error {
    scope.SetColumn("CreatedOn", time.Now().Unix())

    return nil
}

func (tag *Tag) BeforeUpdate(scope *gorm.Scope) error {
    scope.SetColumn("ModifiedOn", time.Now().Unix())

    return nil
}
```
重启服务，再在用Postman用 POST 访问http://127.0.0.1:8000/api/v1/tags?name=2&state=1&created_by=test，发现created_on已经有值了！

在这几段代码中，涉及到知识点：

这属于gorm的Callbacks，可以将回调方法定义为模型结构的指针，在创建、更新、查询、删除时将被调用，如果任何回调返回错误，gorm 将停止未来操作并回滚所有更改。

gorm所支持的回调方法：

创建：BeforeSave、BeforeCreate、AfterCreate、AfterSave
更新：BeforeSave、BeforeUpdate、AfterUpdate、AfterSave
删除：BeforeDelete、AfterDelete
查询：AfterFind
### 编写其余接口的路由逻辑
接下来，我们一口气把剩余的两个接口（EditTag、DeleteTag）完成吧

打开routers目录下 v1 版本的tag.go文件，修改内容：

```go
//修改文章标签
func EditTag(c *gin.Context) {
    id := com.StrTo(c.Param("id")).MustInt()
    name := c.Query("name")
    modifiedBy := c.Query("modified_by")

    valid := validation.Validation{}

    var state int = -1
    if arg := c.Query("state"); arg != "" {
        state = com.StrTo(arg).MustInt()
        valid.Range(state, 0, 1, "state").Message("状态只允许0或1")
    }

    valid.Required(id, "id").Message("ID不能为空")
    valid.Required(modifiedBy, "modified_by").Message("修改人不能为空")
    valid.MaxSize(modifiedBy, 100, "modified_by").Message("修改人最长为100字符")
    valid.MaxSize(name, 100, "name").Message("名称最长为100字符")

    code := e.INVALID_PARAMS
    if ! valid.HasErrors() {
        code = e.SUCCESS
        if models.ExistTagByID(id) {
            data := make(map[string]interface{})
            data["modified_by"] = modifiedBy
            if name != "" {
                data["name"] = name
            }
            if state != -1 {
                data["state"] = state
            }

            models.EditTag(id, data)
        } else {
            code = e.ERROR_NOT_EXIST_TAG
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : make(map[string]string),
    })
}

//删除文章标签
func DeleteTag(c *gin.Context) {
    id := com.StrTo(c.Param("id")).MustInt()

    valid := validation.Validation{}
    valid.Min(id, 1, "id").Message("ID必须大于0")

    code := e.INVALID_PARAMS
    if ! valid.HasErrors() {
        code = e.SUCCESS
        if models.ExistTagByID(id) {
            models.DeleteTag(id)
        } else {
            code = e.ERROR_NOT_EXIST_TAG
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : make(map[string]string),
    })
}
```
编写其余接口的 models 逻辑
打开models下的tag.go，修改文件内容：

```go

func ExistTagByID(id int) bool {
    var tag Tag
    db.Select("id").Where("id = ?", id).First(&tag)
    if tag.ID > 0 {
        return true
    }

    return false
}

func DeleteTag(id int) bool {
    db.Where("id = ?", id).Delete(&Tag{})

    return true
}

func EditTag(id int, data interface {}) bool {
    db.Model(&Tag{}).Where("id = ?", id).Updates(data)

    return true
}
```
### 验证功能
重启服务，用 Postman

PUT 访问 http://127.0.0.1:8000/api/v1/tags/1?name=edit1&state=0&modified_by=edit1 ，查看 code 是否返回 200
DELETE 访问 http://127.0.0.1:8000/api/v1/tags/1 ，查看 code 是否返回 200

### 编写路由逻辑
在routers的 v1 版本下，新建article.go文件，写入内容：
```go
package v1

import (
    "github.com/gin-gonic/gin"
)

//获取单个文章
func GetArticle(c *gin.Context) {
}

//获取多个文章
func GetArticles(c *gin.Context) {
}

//新增文章
func AddArticle(c *gin.Context) {
}

//修改文章
func EditArticle(c *gin.Context) {
}

//删除文章
func DeleteArticle(c *gin.Context) {
}
```
我们打开routers下的router.go文件，修改文件内容为：
```go
package routers

import (
    "github.com/gin-gonic/gin"

    "github.com/EDDYCJY/go-gin-example/routers/api/v1"
    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

func InitRouter() *gin.Engine {
    ...
    apiv1 := r.Group("/api/v1")
    {
        ...
        //获取文章列表
        apiv1.GET("/articles", v1.GetArticles)
        //获取指定文章
        apiv1.GET("/articles/:id", v1.GetArticle)
        //新建文章
        apiv1.POST("/articles", v1.AddArticle)
        //更新指定文章
        apiv1.PUT("/articles/:id", v1.EditArticle)
        //删除指定文章
        apiv1.DELETE("/articles/:id", v1.DeleteArticle)
    }

    return r
}
```
### 编写 models 逻辑
创建models目录下的article.go，写入文件内容：
```go
package models

import (
    "github.com/jinzhu/gorm"

    "time"
)

type Article struct {
    Model

    TagID int `json:"tag_id" gorm:"index"`
    Tag   Tag `json:"tag"`

    Title string `json:"title"`
    Desc string `json:"desc"`
    Content string `json:"content"`
    CreatedBy string `json:"created_by"`
    ModifiedBy string `json:"modified_by"`
    State int `json:"state"`
}


func (article *Article) BeforeCreate(scope *gorm.Scope) error {
    scope.SetColumn("CreatedOn", time.Now().Unix())

    return nil
}

func (article *Article) BeforeUpdate(scope *gorm.Scope) error {
    scope.SetColumn("ModifiedOn", time.Now().Unix())

    return nil
}
```
我们创建了一个Article struct {}，与Tag不同的是，Article多了几项，如下：

gorm:index，用于声明这个字段为索引，如果你使用了自动迁移功能则会有所影响，在不使用则无影响
Tag字段，实际是一个嵌套的struct，它利用TagID与Tag模型相互关联，在执行查询的时候，能够达到Article、Tag关联查询的功能
time.Now().Unix() 返回当前的时间戳
接下来，请确保已对上一章节的内容通读且了解，由于逻辑偏差不会太远，我们本节直接编写这五个接口

打开models目录下的article.go，修改文件内容：
```go
package models

import (
    "time"

    "github.com/jinzhu/gorm"
)

type Article struct {
    Model

    TagID int `json:"tag_id" gorm:"index"`
    Tag   Tag `json:"tag"`

    Title string `json:"title"`
    Desc string `json:"desc"`
    Content string `json:"content"`
    CreatedBy string `json:"created_by"`
    ModifiedBy string `json:"modified_by"`
    State int `json:"state"`
}


func ExistArticleByID(id int) bool {
    var article Article
    db.Select("id").Where("id = ?", id).First(&article)

    if article.ID > 0 {
        return true
    }

    return false
}

func GetArticleTotal(maps interface {}) (count int){
    db.Model(&Article{}).Where(maps).Count(&count)

    return
}

func GetArticles(pageNum int, pageSize int, maps interface {}) (articles []Article) {
    db.Preload("Tag").Where(maps).Offset(pageNum).Limit(pageSize).Find(&articles)

    return
}

func GetArticle(id int) (article Article) {
    db.Where("id = ?", id).First(&article)
    db.Model(&article).Related(&article.Tag)

    return
}

func EditArticle(id int, data interface {}) bool {
    db.Model(&Article{}).Where("id = ?", id).Updates(data)

    return true
}

func AddArticle(data map[string]interface {}) bool {
    db.Create(&Article {
        TagID : data["tag_id"].(int),
        Title : data["title"].(string),
        Desc : data["desc"].(string),
        Content : data["content"].(string),
        CreatedBy : data["created_by"].(string),
        State : data["state"].(int),
    })

    return true
}

func DeleteArticle(id int) bool {
    db.Where("id = ?", id).Delete(Article{})

    return true
}

func (article *Article) BeforeCreate(scope *gorm.Scope) error {
    scope.SetColumn("CreatedOn", time.Now().Unix())

    return nil
}

func (article *Article) BeforeUpdate(scope *gorm.Scope) error {
    scope.SetColumn("ModifiedOn", time.Now().Unix())

    return nil
}
```
在这里，我们拿出三点不同来讲，如下：

1、 我们的Article是如何关联到Tag？
```go
func GetArticle(id int) (article Article) {
    db.Where("id = ?", id).First(&article)
    db.Model(&article).Related(&article.Tag)

    return
}
```
能够达到关联，首先是gorm本身做了大量的约定俗成

Article有一个结构体成员是TagID，就是外键。gorm会通过类名+ID 的方式去找到这两个类之间的关联关系
Article有一个结构体成员是Tag，就是我们嵌套在Article里的Tag结构体，我们可以通过Related进行关联查询
2、 Preload是什么东西，为什么查询可以得出每一项的关联Tag？

func GetArticles(pageNum int, pageSize int, maps interface {}) (articles []Article) {
    db.Preload("Tag").Where(maps).Offset(pageNum).Limit(pageSize).Find(&articles)

    return
}
Preload就是一个预加载器，它会执行两条 SQL，分别是SELECT * FROM blog_articles;和SELECT * FROM blog_tag WHERE id IN (1,2,3,4);，那么在查询出结构后，gorm内部处理对应的映射逻辑，将其填充到Article的Tag中，会特别方便，并且避免了循环查询

那么有没有别的办法呢，大致是两种

gorm的Join
循环Related
综合之下，还是Preload更好，如果你有更优的方案，欢迎说一下 :)

3、 v.(I) 是什么？

v表示一个接口值，I表示接口类型。这个实际就是 Golang 中的类型断言，用于判断一个接口值的实际类型是否为某个类型，或一个非接口值的类型是否实现了某个接口类型

打开routers目录下 v1 版本的article.go文件，修改文件内容：
```go
package v1

import (
    "net/http"
    "log"

    "github.com/gin-gonic/gin"
    "github.com/astaxie/beego/validation"
    "github.com/unknwon/com"

    "github.com/EDDYCJY/go-gin-example/models"
    "github.com/EDDYCJY/go-gin-example/pkg/e"
    "github.com/EDDYCJY/go-gin-example/pkg/setting"
    "github.com/EDDYCJY/go-gin-example/pkg/util"
)

//获取单个文章
func GetArticle(c *gin.Context) {
    id := com.StrTo(c.Param("id")).MustInt()

    valid := validation.Validation{}
    valid.Min(id, 1, "id").Message("ID必须大于0")

    code := e.INVALID_PARAMS
    var data interface {}
    if ! valid.HasErrors() {
        if models.ExistArticleByID(id) {
            data = models.GetArticle(id)
            code = e.SUCCESS
        } else {
            code = e.ERROR_NOT_EXIST_ARTICLE
        }
    } else {
        for _, err := range valid.Errors {
            log.Printf("err.key: %s, err.message: %s", err.Key, err.Message)
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : data,
    })
}

//获取多个文章
func GetArticles(c *gin.Context) {
    data := make(map[string]interface{})
    maps := make(map[string]interface{})
    valid := validation.Validation{}

    var state int = -1
    if arg := c.Query("state"); arg != "" {
        state = com.StrTo(arg).MustInt()
        maps["state"] = state

        valid.Range(state, 0, 1, "state").Message("状态只允许0或1")
    }

    var tagId int = -1
    if arg := c.Query("tag_id"); arg != "" {
        tagId = com.StrTo(arg).MustInt()
        maps["tag_id"] = tagId

        valid.Min(tagId, 1, "tag_id").Message("标签ID必须大于0")
    }

    code := e.INVALID_PARAMS
    if ! valid.HasErrors() {
        code = e.SUCCESS

        data["lists"] = models.GetArticles(util.GetPage(c), setting.PageSize, maps)
        data["total"] = models.GetArticleTotal(maps)

    } else {
        for _, err := range valid.Errors {
            log.Printf("err.key: %s, err.message: %s", err.Key, err.Message)
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : data,
    })
}

//新增文章
func AddArticle(c *gin.Context) {
    tagId := com.StrTo(c.Query("tag_id")).MustInt()
    title := c.Query("title")
    desc := c.Query("desc")
    content := c.Query("content")
    createdBy := c.Query("created_by")
    state := com.StrTo(c.DefaultQuery("state", "0")).MustInt()

    valid := validation.Validation{}
    valid.Min(tagId, 1, "tag_id").Message("标签ID必须大于0")
    valid.Required(title, "title").Message("标题不能为空")
    valid.Required(desc, "desc").Message("简述不能为空")
    valid.Required(content, "content").Message("内容不能为空")
    valid.Required(createdBy, "created_by").Message("创建人不能为空")
    valid.Range(state, 0, 1, "state").Message("状态只允许0或1")

    code := e.INVALID_PARAMS
    if ! valid.HasErrors() {
        if models.ExistTagByID(tagId) {
            data := make(map[string]interface {})
            data["tag_id"] = tagId
            data["title"] = title
            data["desc"] = desc
            data["content"] = content
            data["created_by"] = createdBy
            data["state"] = state

            models.AddArticle(data)
            code = e.SUCCESS
        } else {
            code = e.ERROR_NOT_EXIST_TAG
        }
    } else {
        for _, err := range valid.Errors {
            log.Printf("err.key: %s, err.message: %s", err.Key, err.Message)
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : make(map[string]interface{}),
    })
}

//修改文章
func EditArticle(c *gin.Context) {
    valid := validation.Validation{}

    id := com.StrTo(c.Param("id")).MustInt()
    tagId := com.StrTo(c.Query("tag_id")).MustInt()
    title := c.Query("title")
    desc := c.Query("desc")
    content := c.Query("content")
    modifiedBy := c.Query("modified_by")

    var state int = -1
    if arg := c.Query("state"); arg != "" {
        state = com.StrTo(arg).MustInt()
        valid.Range(state, 0, 1, "state").Message("状态只允许0或1")
    }

    valid.Min(id, 1, "id").Message("ID必须大于0")
    valid.MaxSize(title, 100, "title").Message("标题最长为100字符")
    valid.MaxSize(desc, 255, "desc").Message("简述最长为255字符")
    valid.MaxSize(content, 65535, "content").Message("内容最长为65535字符")
    valid.Required(modifiedBy, "modified_by").Message("修改人不能为空")
    valid.MaxSize(modifiedBy, 100, "modified_by").Message("修改人最长为100字符")

    code := e.INVALID_PARAMS
    if ! valid.HasErrors() {
        if models.ExistArticleByID(id) {
            if models.ExistTagByID(tagId) {
                data := make(map[string]interface {})
                if tagId > 0 {
                    data["tag_id"] = tagId
                }
                if title != "" {
                    data["title"] = title
                }
                if desc != "" {
                    data["desc"] = desc
                }
                if content != "" {
                    data["content"] = content
                }

                data["modified_by"] = modifiedBy

                models.EditArticle(id, data)
                code = e.SUCCESS
            } else {
                code = e.ERROR_NOT_EXIST_TAG
            }
        } else {
            code = e.ERROR_NOT_EXIST_ARTICLE
        }
    } else {
        for _, err := range valid.Errors {
            log.Printf("err.key: %s, err.message: %s", err.Key, err.Message)
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : make(map[string]string),
    })
}

//删除文章
func DeleteArticle(c *gin.Context) {
    id := com.StrTo(c.Param("id")).MustInt()

    valid := validation.Validation{}
    valid.Min(id, 1, "id").Message("ID必须大于0")

    code := e.INVALID_PARAMS
    if ! valid.HasErrors() {
        if models.ExistArticleByID(id) {
            models.DeleteArticle(id)
            code = e.SUCCESS
        } else {
            code = e.ERROR_NOT_EXIST_ARTICLE
        }
    } else {
        for _, err := range valid.Errors {
            log.Printf("err.key: %s, err.message: %s", err.Key, err.Message)
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : make(map[string]string),
    })
}
```
当前目录结构：

go-gin-example/
├── conf
│   └── app.ini
├── main.go
├── middleware
├── models
│   ├── article.go
│   ├── models.go
│   └── tag.go
├── pkg
│   ├── e
│   │   ├── code.go
│   │   └── msg.go
│   ├── setting
│   │   └── setting.go
│   └── util
│       └── pagination.go
├── routers
│   ├── api
│   │   └── v1
│   │       ├── article.go
│   │       └── tag.go
│   └── router.go
├── runtime

## 使用 JWT 进行身份校验

在前面几节中，我们已经基本的完成了 API’s 的编写，但是，还存在一些非常严重的问题，例如，我们现在的 API 是可以随意调用的，这显然还不安全全，在本文中我们通过 jwt-go （GoDoc）的方式来简单解决这个问题。


### 编写 jwt 工具包
我们需要编写一个jwt的工具包，我们在pkg下的util目录新建jwt.go，写入文件内容：
```go
package util

import (
    "time"

    jwt "github.com/dgrijalva/jwt-go"

    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

var jwtSecret = []byte(setting.JwtSecret)

type Claims struct {
    Username string `json:"username"`
    Password string `json:"password"`
    jwt.StandardClaims
}

func GenerateToken(username, password string) (string, error) {
    nowTime := time.Now()
    expireTime := nowTime.Add(3 * time.Hour)

    claims := Claims{
        username,
        password,
        jwt.StandardClaims {
            ExpiresAt : expireTime.Unix(),
            Issuer : "gin-blog",
        },
    }

    tokenClaims := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    token, err := tokenClaims.SignedString(jwtSecret)

    return token, err
}

func ParseToken(token string) (*Claims, error) {
    tokenClaims, err := jwt.ParseWithClaims(token, &Claims{}, func(token *jwt.Token) (interface{}, error) {
        return jwtSecret, nil
    })

    if tokenClaims != nil {
        if claims, ok := tokenClaims.Claims.(*Claims); ok && tokenClaims.Valid {
            return claims, nil
        }
    }

    return nil, err
}
```
在这个工具包，我们涉及到

- NewWithClaims(method SigningMethod, claims Claims)，method对应着SigningMethodHMAC struct{}，其包含SigningMethodHS256、SigningMethodHS384、- SigningMethodHS512三种crypto.Hash方案
func (t *Token) SignedString(key interface{}) 该方法内部生成签名字符串，再用于获取完整、已签名的token
- func (p *Parser) ParseWithClaims 用于解析鉴权的声明，方法内部主要是具体的解码和校验的过程，最终返回 *Token
- func (m MapClaims) Valid() 验证基于时间的声明exp, iat, nbf，注意如果没有任何声明在令牌中，仍然会被认为是有效的。并且对于时区偏差没有计算方法
有了jwt工具包，接下来我们要编写要用于Gin的中间件，我们在middleware下新建jwt目录，新建jwt.go文件，写入内容：
```go
package jwt

import (
    "time"
    "net/http"

    "github.com/gin-gonic/gin"

    "github.com/EDDYCJY/go-gin-example/pkg/util"
    "github.com/EDDYCJY/go-gin-example/pkg/e"
)

func JWT() gin.HandlerFunc {
    return func(c *gin.Context) {
        var code int
        var data interface{}

        code = e.SUCCESS
        token := c.Query("token")
        if token == "" {
            code = e.INVALID_PARAMS
        } else {
            claims, err := util.ParseToken(token)
            if err != nil {
                code = e.ERROR_AUTH_CHECK_TOKEN_FAIL
            } else if time.Now().Unix() > claims.ExpiresAt {
                code = e.ERROR_AUTH_CHECK_TOKEN_TIMEOUT
            }
        }

        if code != e.SUCCESS {
            c.JSON(http.StatusUnauthorized, gin.H{
                "code" : code,
                "msg" : e.GetMsg(code),
                "data" : data,
            })

            c.Abort()
            return
        }

        c.Next()
    }
}
```
### 如何获取Token
那么我们如何调用它呢，我们还要获取Token呢？

1、 我们要新增一个获取Token的 API

在models下新建auth.go文件，写入内容：
```go
package models

type Auth struct {
    ID int `gorm:"primary_key" json:"id"`
    Username string `json:"username"`
    Password string `json:"password"`
}

func CheckAuth(username, password string) bool {
    var auth Auth
    db.Select("id").Where(Auth{Username : username, Password : password}).First(&auth)
    if auth.ID > 0 {
        return true
    }

    return false
}
```
在routers下的api目录新建auth.go文件，写入内容：
```go
package api

import (
    "log"
    "net/http"

    "github.com/gin-gonic/gin"
    "github.com/astaxie/beego/validation"

    "github.com/EDDYCJY/go-gin-example/pkg/e"
    "github.com/EDDYCJY/go-gin-example/pkg/util"
    "github.com/EDDYCJY/go-gin-example/models"
)

type auth struct {
    Username string `valid:"Required; MaxSize(50)"`
    Password string `valid:"Required; MaxSize(50)"`
}

func GetAuth(c *gin.Context) {
    username := c.Query("username")
    password := c.Query("password")

    valid := validation.Validation{}
    a := auth{Username: username, Password: password}
    ok, _ := valid.Valid(&a)

    data := make(map[string]interface{})
    code := e.INVALID_PARAMS
    if ok {
        isExist := models.CheckAuth(username, password)
        if isExist {
            token, err := util.GenerateToken(username, password)
            if err != nil {
                code = e.ERROR_AUTH_TOKEN
            } else {
                data["token"] = token

                code = e.SUCCESS
            }

        } else {
            code = e.ERROR_AUTH
        }
    } else {
        for _, err := range valid.Errors {
            log.Println(err.Key, err.Message)
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : data,
    })
}
```
我们打开routers目录下的router.go文件，修改文件内容（新增获取 token 的方法）：
```go
package routers

import (
    "github.com/gin-gonic/gin"

    "github.com/EDDYCJY/go-gin-example/routers/api"
    "github.com/EDDYCJY/go-gin-example/routers/api/v1"
    "github.com/EDDYCJY/go-gin-example/pkg/setting"
)

func InitRouter() *gin.Engine {
    r := gin.New()

    r.Use(gin.Logger())

    r.Use(gin.Recovery())

    gin.SetMode(setting.RunMode)

    r.GET("/auth", api.GetAuth)

    apiv1 := r.Group("/api/v1")
    {
        ...
    }

    return r
}
```
### 验证Token
获取token的 API 方法就到这里啦，让我们来测试下是否可以正常使用吧！

重启服务后，用GET方式访问http://127.0.0.1:8000/auth?username=test&password=test123456，查看返回值是否正确

{
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJleHAiOjE1MTg3MjAwMzcsImlzcyI6Imdpbi1ibG9nIn0.-kK0V9E06qTHOzupQM_gHXAGDB3EJtJS4H5TTCyWwW8"
  },
  "msg": "ok"
}
我们有了token的 API，也调用成功了

### 将中间件接入Gin
2、 接下来我们将中间件接入到Gin的访问流程中

我们打开routers目录下的router.go文件，修改文件内容（新增引用包和中间件引用）
```go
package routers

import (
    "github.com/gin-gonic/gin"

    "github.com/EDDYCJY/go-gin-example/routers/api"
    "github.com/EDDYCJY/go-gin-example/routers/api/v1"
    "github.com/EDDYCJY/go-gin-example/pkg/setting"
    "github.com/EDDYCJY/go-gin-example/middleware/jwt"
)

func InitRouter() *gin.Engine {
    r := gin.New()

    r.Use(gin.Logger())

    r.Use(gin.Recovery())

    gin.SetMode(setting.RunMode)

    r.GET("/auth", api.GetAuth)

    apiv1 := r.Group("/api/v1")
    apiv1.Use(jwt.JWT())
    {
        ...
    }

    return r
}
```

### 验证功能
我们来测试一下，再次访问

http://127.0.0.1:8000/api/v1/articles
http://127.0.0.1:8000/api/v1/articles?token=23131
正确的反馈应该是

{
  "code": 400,
  "data": null,
  "msg": "请求参数错误"
}

{
  "code": 20001,
  "data": null,
  "msg": "Token鉴权失败"
}
我们需要访问http://127.0.0.1:8000/auth?username=test&password=test123456，得到token

{
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJwYXNzd29yZCI6InRlc3QxMjM0NTYiLCJleHAiOjE1MTg3MjQ2OTMsImlzcyI6Imdpbi1ibG9nIn0.KSBY6TeavV_30kfmP7HWLRYKP5TPEDgHtABe9HCsic4"
  },
  "msg": "ok"
}
再用包含token的 URL 参数去访问我们的应用 API，

访问http://127.0.0.1:8000/api/v1/articles?token=eyJhbGci...，检查接口返回值
```json
{
  "code": 200,
  "data": {
    "lists": [
      {
        "id": 2,
        "created_on": 1518700920,
        "modified_on": 0,
        "tag_id": 1,
        "tag": {
          "id": 1,
          "created_on": 1518684200,
          "modified_on": 0,
          "name": "tag1",
          "created_by": "",
          "modified_by": "",
          "state": 0
        },
        "content": "test-content",
        "created_by": "test-created",
        "modified_by": "",
        "state": 0
      }
    ],
    "total": 1
  },
  "msg": "ok"
}
```
## 自定义 log。

### 新建logging包
我们在pkg下新建logging目录，新建file.go和log.go文件，写入内容：

编写file文件
### file.go：
```go
package logging

import (
    "os"
    "time"
    "fmt"
    "log"
)

var (
    LogSavePath = "runtime/logs/"
    LogSaveName = "log"
    LogFileExt = "log"
    TimeFormat = "20060102"
)

func getLogFilePath() string {
    return fmt.Sprintf("%s", LogSavePath)
}

func getLogFileFullPath() string {
    prefixPath := getLogFilePath()
    suffixPath := fmt.Sprintf("%s%s.%s", LogSaveName, time.Now().Format(TimeFormat), LogFileExt)

    return fmt.Sprintf("%s%s", prefixPath, suffixPath)
}

func openLogFile(filePath string) *os.File {
    _, err := os.Stat(filePath)
    switch {
        case os.IsNotExist(err):
            mkDir()
        case os.IsPermission(err):
            log.Fatalf("Permission :%v", err)
    }

    handle, err := os.OpenFile(filePath, os.O_APPEND | os.O_CREATE | os.O_WRONLY, 0644)
    if err != nil {
        log.Fatalf("Fail to OpenFile :%v", err)
    }

    return handle
}

func mkDir() {
    dir, _ := os.Getwd()
    err := os.MkdirAll(dir + "/" + getLogFilePath(), os.ModePerm)
    if err != nil {
        panic(err)
    }
}
os.Stat：返回文件信息结构描述文件。如果出现错误，会返回*PathError
type PathError struct {
    Op   string
    Path string
    Err  error
}
```
- os.IsNotExist：能够接受ErrNotExist、syscall的一些错误，它会返回一个布尔值，能够得知文件不存在或目录不存在
- os.IsPermission：能够接受ErrPermission、syscall的一些错误，它会返回一个布尔值，能够得知权限是否满足
- os.OpenFile：调用文件，支持传入文件名称、指定的模式调用文件、文件权限，返回的文件的方法可以用于 I/O。如果出现错误，则为*PathError。
const (
    // Exactly one of O_RDONLY, O_WRONLY, or O_RDWR must be specified.
    O_RDONLY int = syscall.O_RDONLY // 以只读模式打开文件
    O_WRONLY int = syscall.O_WRONLY // 以只写模式打开文件
    O_RDWR   int = syscall.O_RDWR   // 以读写模式打开文件
    // The remaining values may be or'ed in to control behavior.
    O_APPEND int = syscall.O_APPEND // 在写入时将数据追加到文件中
    O_CREATE int = syscall.O_CREAT  // 如果不存在，则创建一个新文件
    O_EXCL   int = syscall.O_EXCL   // 使用O_CREATE时，文件必须不存在
    O_SYNC   int = syscall.O_SYNC   // 同步IO
    O_TRUNC  int = syscall.O_TRUNC  // 如果可以，打开时
)
os.Getwd：返回与当前目录对应的根路径名
os.MkdirAll：创建对应的目录以及所需的子目录，若成功则返回nil，否则返回error
os.ModePerm：const定义ModePerm FileMode = 0777
编写log文件
### log.go
```go
package logging

import (
    "log"
    "os"
    "runtime"
    "path/filepath"
    "fmt"
)

type Level int

var (
    F *os.File

    DefaultPrefix = ""
    DefaultCallerDepth = 2

    logger *log.Logger
    logPrefix = ""
    levelFlags = []string{"DEBUG", "INFO", "WARN", "ERROR", "FATAL"}
)

const (
    DEBUG Level = iota
    INFO
    WARNING
    ERROR
    FATAL
)

func init() {
    filePath := getLogFileFullPath()
    F = openLogFile(filePath)

    logger = log.New(F, DefaultPrefix, log.LstdFlags)
}

func Debug(v ...interface{}) {
    setPrefix(DEBUG)
    logger.Println(v)
}

func Info(v ...interface{}) {
    setPrefix(INFO)
    logger.Println(v)
}

func Warn(v ...interface{}) {
    setPrefix(WARNING)
    logger.Println(v)
}

func Error(v ...interface{}) {
    setPrefix(ERROR)
    logger.Println(v)
}

func Fatal(v ...interface{}) {
    setPrefix(FATAL)
    logger.Fatalln(v)
}

func setPrefix(level Level) {
    _, file, line, ok := runtime.Caller(DefaultCallerDepth)
    if ok {
        logPrefix = fmt.Sprintf("[%s][%s:%d]", levelFlags[level], filepath.Base(file), line)
    } else {
        logPrefix = fmt.Sprintf("[%s]", levelFlags[level])
    }

    logger.SetPrefix(logPrefix)
}
```
log.New：创建一个新的日志记录器。out定义要写入日志数据的IO句柄。prefix定义每个生成的日志行的开头。flag定义了日志记录属性
```go
func New(out io.Writer, prefix string, flag int) *Logger {
    return &Logger{out: out, prefix: prefix, flag: flag}
}
```
log.LstdFlags：日志记录的格式属性之一，其余的选项如下
```go
const (
    Ldate         = 1 << iota     // the date in the local time zone: 2009/01/23
    Ltime                         // the time in the local time zone: 01:23:23
    Lmicroseconds                 // microsecond resolution: 01:23:23.123123.  assumes Ltime.
    Llongfile                     // full file name and line number: /a/b/c/d.go:23
    Lshortfile                    // final file name element and line number: d.go:23. overrides Llongfile
    LUTC                          // if Ldate or Ltime is set, use UTC rather than the local time zone
    LstdFlags     = Ldate | Ltime // initial values for the standard logger
)
```

打开routers目录下的article.go、tag.go、auth.go。
将log包的引用删除，修改引用我们自己的日志包为github.com/EDDYCJY/go-gin-example/pkg/logging。
将原本的log.Println(...)改为logging.Info(...)。
例如auth.go文件的修改内容：
```go
package api

import (
    "net/http"

    "github.com/gin-gonic/gin"
    "github.com/astaxie/beego/validation"

    "github.com/EDDYCJY/go-gin-example/pkg/e"
    "github.com/EDDYCJY/go-gin-example/pkg/util"
    "github.com/EDDYCJY/go-gin-example/models"
    "github.com/EDDYCJY/go-gin-example/pkg/logging"
)
...
func GetAuth(c *gin.Context) {
    ...
    code := e.INVALID_PARAMS
    if ok {
        ...
    } else {
        for _, err := range valid.Errors {
                logging.Info(err.Key, err.Message)
            }
    }

    c.JSON(http.StatusOK, gin.H{
        "code" : code,
        "msg" : e.GetMsg(code),
        "data" : data,
    })
}
```
### 验证功能
修改文件后，重启服务，我们来试试吧！

获取到 API 的 Token 后，我们故意传错误 URL 参数给接口，如：http://127.0.0.1:8000/api/v1/articles?tag_id=0&state=9999999&token=eyJhbG..
## 优雅的重启服务

### ctrl + c
内核在某些情况下发送信号，比如在进程往一个已经关闭的管道写数据时会产生SIGPIPE信号

在终端执行特定的组合键可以使系统发送特定的信号给此进程，完成一系列的动作

|命令	|信号	|含义|
|------------|-------------|-------------|
|ctrl + c	|SIGINT	|强制进程结束|
|ctrl + z	|SIGTSTP	任务中断，进程挂起|
|ctrl + \	|SIGQUIT	进程结束 和 dump core|
|ctrl + d|		|EOF|
|            |SIGHUP|	终止收到该信号的进程。若程序中没有捕捉该信号，当收到该信号时，进程就会退出（常用于 重启、重新加载进程）
因此在我们执行ctrl + c关闭gin服务端时，会强制进程结束，导致正在访问的用户等出现问题|

常见的 kill -9 pid 会发送 SIGKILL 信号给进程，也是类似的结果

### 信号
本段中反复出现信号是什么呢？

信号是 Unix 、类 Unix 以及其他 POSIX 兼容的操作系统中进程间通讯的一种有限制的方式

它是一种异步的通知机制，用来提醒进程一个事件（硬件异常、程序执行异常、外部发出信号）已经发生。当一个信号发送给一个进程，操作系统中断了进程正常的控制流程。此时，任何非原子操作都将被中断。如果进程定义了信号的处理函数，那么它将被执行，否则就执行默认的处理函数

所有信号
```bash
$ kill -l
 1) SIGHUP   2) SIGINT   3) SIGQUIT  4) SIGILL   5) SIGTRAP
 6) SIGABRT  7) SIGBUS   8) SIGFPE   9) SIGKILL 10) SIGUSR1
11) SIGSEGV 12) SIGUSR2 13) SIGPIPE 14) SIGALRM 15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD 18) SIGCONT 19) SIGSTOP 20) SIGTSTP
21) SIGTTIN 22) SIGTTOU 23) SIGURG  24) SIGXCPU 25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF 28) SIGWINCH    29) SIGIO   30) SIGPWR
31) SIGSYS  34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
63) SIGRTMAX-1  64) SIGRTMAX
```
### 怎样算优雅

- 不关闭现有连接（正在运行中的程序）
- 新的进程启动并替代旧进程
- 新的进程接管新的连接
- 连接要随时响应用户的请求，当用户仍在请求旧进程时要保持连接，新用户应请求新进程，不可以出现拒绝请求的情况
流程
1、替换可执行文件或修改配置文件

2、发送信号量 SIGHUP

3、拒绝新连接请求旧进程，但要保证已有连接正常

4、启动新的子进程

5、新的子进程开始 Accet

6、系统将新的请求转交新的子进程

7、旧进程处理完所有旧连接后正常结束

### 实现优雅重启
endless
Zero downtime restarts for golang HTTP and HTTPS servers. (for golang 1.3+)

我们借助 fvbock/endless 来实现 Golang HTTP/HTTPS 服务重新启动的零停机

endless server 监听以下几种信号量：

syscall.SIGHUP：触发 fork 子进程和重新启动
syscall.SIGUSR1/syscall.SIGTSTP：被监听，但不会触发任何动作
syscall.SIGUSR2：触发 hammerTime
syscall.SIGINT/syscall.SIGTERM：触发服务器关闭（会完成正在运行的请求）
endless 正正是依靠监听这些信号量，完成管控的一系列动作

安装
go get -u github.com/fvbock/endless
编写
打开 gin-blog 的 main.go文件，修改文件：
```go
package main

import (
    "fmt"
    "log"
    "syscall"

    "github.com/fvbock/endless"

    "gin-blog/routers"
    "gin-blog/pkg/setting"
)

func main() {
    endless.DefaultReadTimeOut = setting.ReadTimeout
    endless.DefaultWriteTimeOut = setting.WriteTimeout
    endless.DefaultMaxHeaderBytes = 1 << 20
    endPoint := fmt.Sprintf(":%d", setting.HTTPPort)

    server := endless.NewServer(endPoint, routers.InitRouter())
    server.BeforeBegin = func(add string) {
        log.Printf("Actual pid is %d", syscall.Getpid())
    }

    err := server.ListenAndServe()
    if err != nil {
        log.Printf("Server err: %v", err)
    }
}
endless.NewServer 返回一个初始化的 endlessServer 对象，在 BeforeBegin 时输出当前进程的 pid，调用 ListenAndServe 将实际“启动”服务

验证
编译
$ go build main.go
执行
$ ./main
[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
...
Actual pid is 48601
启动成功后，输出了pid为 48601；在另外一个终端执行 kill -1 48601 ，检验先前服务的终端效果

[root@localhost go-gin-example]# ./main
[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
 - using env:   export GIN_MODE=release
 - using code:  gin.SetMode(gin.ReleaseMode)

[GIN-debug] GET    /auth                     --> ...
[GIN-debug] GET    /api/v1/tags              --> ...
...

Actual pid is 48601

...

Actual pid is 48755
48601 Received SIGTERM.
48601 [::]:8000 Listener closed.
48601 Waiting for connections to finish...
48601 Serve() returning...
Server err: accept tcp [::]:8000: use of closed network connection
可以看到该命令已经挂起，并且 fork 了新的子进程 pid 为 48755

48601 Received SIGTERM.
48601 [::]:8000 Listener closed.
48601 Waiting for connections to finish...
48601 Serve() returning...
Server err: accept tcp [::]:8000: use of closed network connection
大致意思为主进程（pid为 48601）接受到 SIGTERM 信号量，关闭主进程的监听并且等待正在执行的请求完成；这与我们先前的描述一致

唤醒
这时候在 postman 上再次访问我们的接口，你可以惊喜的发现，他“复活”了！

Actual pid is 48755
48601 Received SIGTERM.
48601 [::]:8000 Listener closed.
48601 Waiting for connections to finish...
48601 Serve() returning...
Server err: accept tcp [::]:8000: use of closed network connection


$ [GIN] 2018/03/15 - 13:00:16 | 200 |     188.096µs |   192.168.111.1 | GET      /api/v1/tags...
这就完成了一次正向的流转了

你想想，每次更新发布、或者修改配置文件等，只需要给该进程发送SIGTERM 信号，而不需要强制结束应用，是多么便捷又安全的事！
```
问题
endless 热更新是采取创建子进程后，将原进程退出的方式，这点不符合守护进程的要求

### http.Server - Shutdown()
如果你的Golang >= 1.8，也可以考虑使用 http.Server 的 Shutdown 方法
```go
package main

import (
    "fmt"
    "net/http"
    "context"
    "log"
    "os"
    "os/signal"
    "time"


    "gin-blog/routers"
    "gin-blog/pkg/setting"
)

func main() {
    router := routers.InitRouter()

    s := &http.Server{
        Addr:           fmt.Sprintf(":%d", setting.HTTPPort),
        Handler:        router,
        ReadTimeout:    setting.ReadTimeout,
        WriteTimeout:   setting.WriteTimeout,
        MaxHeaderBytes: 1 << 20,
    }

    go func() {
        if err := s.ListenAndServe(); err != nil {
            log.Printf("Listen: %s\n", err)
        }
    }()

    quit := make(chan os.Signal)
    signal.Notify(quit, os.Interrupt)
    <- quit

    log.Println("Shutdown Server ...")

    ctx, cancel := context.WithTimeout(context.Background(), 5 * time.Second)
    defer cancel()
    if err := s.Shutdown(ctx); err != nil {
        log.Fatal("Server Shutdown:", err)
    }

    log.Println("Server exiting")
}
```
小结
在日常的服务中，优雅的重启（热更新）是非常重要的一环。而 Golang 在 HTTP 服务方面的热更新也有不少方案了，我们应该根据实际应用场景挑选最合适的


## Swagger
本文目标
一个好的 API's，必然离不开一个好的API文档，如果要开发纯手写 API 文档，不存在的（很难持续维护），因此我们要自动生成接口文档。

### 安装 swag
```go
go install github.com/swaggo/swag/cmd/swag@latest

$ swag -v
// 安装gins-swagger
$ go get -u github.com/swaggo/gin-swagger@v1.2.0 
$ go get -u github.com/swaggo/files


```
初始化
编写 API 注释
Swagger 中需要将相应的注释或注解编写到方法上，再利用生成器自动生成说明文件
```go
gin-swagger 给出的范例：

// @Summary Add a new pet to the store
// @Description get string by ID
// @Accept  json
// @Produce  json
// @Param   some_id     path    int     true        "Some ID"
// @Success 200 {string} string    "ok"
// @Failure 400 {object} web.APIError "We need ID!!"
// @Failure 404 {object} web.APIError "Can not find ID"
// @Router /testapi/get-string-by-int/{some_id} [get]
我们可以参照 Swagger 的注解规范和范例去编写

// @Summary 新增文章标签
// @Produce  json
// @Param name query string true "Name"
// @Param state query int false "State"
// @Param created_by query int false "CreatedBy"
// @Success 200 {string} json "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/tags [post]
func AddTag(c *gin.Context) {
// @Summary 修改文章标签
// @Produce  json
// @Param id path int true "ID"
// @Param name query string true "ID"
// @Param state query int false "State"
// @Param modified_by query string true "ModifiedBy"
// @Success 200 {string} json "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/tags/{id} [put]
func EditTag(c *gin.Context) {
```
编写完成后 运行 swag init

### 路由
在完成了注解的编写后，我们需要针对 swagger 新增初始化动作和对应的路由规则，才可以使用。打开 routers/router.go 文件，新增内容如下：
```go
package routers

import (
    ...

    _ "github.com/EDDYCJY/go-gin-example/docs"

    ...
)

// InitRouter initialize routing information
func InitRouter() *gin.Engine {
    ...
    r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
    ...
    apiv1 := r.Group("/api/v1")
    apiv1.Use(jwt.JWT())
    {
        ...
    }

    return r
}
```

### 验证
大功告成，访问一下 http://127.0.0.1:8000/swagger/index.html， 查看 API 文档生成是否正确

## 定制 GORM Callbacks


GORM 本身是由回调驱动的，所以我们可以根据需要完全定制 GORM，以此达到我们的目的，如下：

-注册一个新的回调
- 删除现有的回调
- 替换现有的回调
- 注册回调的顺序
在 GORM 中包含以上四类 Callbacks，我们结合项目选用 “替换现有的回调” 来解决一个小痛点。



解决
在这里我们通过 Callbacks 来实现功能，不需要一个个文件去编写

### 实现 Callbacks
打开 models 目录下的 models.go 文件，实现以下两个方法：

1、updateTimeStampForCreateCallback
```go
// updateTimeStampForCreateCallback will set `CreatedOn`, `ModifiedOn` when creating
func updateTimeStampForCreateCallback(scope *gorm.Scope) {
    if !scope.HasError() {
        nowTime := time.Now().Unix()
        if createTimeField, ok := scope.FieldByName("CreatedOn"); ok {
            if createTimeField.IsBlank {
                createTimeField.Set(nowTime)
            }
        }

        if modifyTimeField, ok := scope.FieldByName("ModifiedOn"); ok {
            if modifyTimeField.IsBlank {
                modifyTimeField.Set(nowTime)
            }
        }
    }
}
```
在这段方法中，会完成以下功能

检查是否有含有错误（db.Error）
scope.FieldByName 通过 scope.Fields() 获取所有字段，判断当前是否包含所需字段
```go
for _, field := range scope.Fields() {
    if field.Name == name || field.DBName == name {
        return field, true
    }
    if field.DBName == dbName {
        mostMatchedField = field
    }
}
```
field.IsBlank 可判断该字段的值是否为空
```go
func isBlank(value reflect.Value) bool {
    switch value.Kind() {
    case reflect.String:
        return value.Len() == 0
    case reflect.Bool:
        return !value.Bool()
    case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
        return value.Int() == 0
    case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
        return value.Uint() == 0
    case reflect.Float32, reflect.Float64:
        return value.Float() == 0
    case reflect.Interface, reflect.Ptr:
        return value.IsNil()
    }

    return reflect.DeepEqual(value.Interface(), reflect.Zero(value.Type()).Interface())
}
```
若为空则 field.Set 用于给该字段设置值，参数为 interface{}
2、updateTimeStampForUpdateCallback
```go
// updateTimeStampForUpdateCallback will set `ModifyTime` when updating
func updateTimeStampForUpdateCallback(scope *gorm.Scope) {
    if _, ok := scope.Get("gorm:update_column"); !ok {
        scope.SetColumn("ModifiedOn", time.Now().Unix())
    }
}
```
scope.Get(...) 根据入参获取设置了字面值的参数，例如本文中是 gorm:update_column ，它会去查找含这个字面值的字段属性
scope.SetColumn(...) 假设没有指定 update_column 的字段，我们默认在更新回调设置 ModifiedOn 的值
注册 Callbacks
在上面小节我已经把回调方法编写好了，接下来需要将其注册进 GORM 的钩子里，但其本身自带 Create 和 Update 回调，因此调用替换即可

在 models.go 的 init 函数中，增加以下语句
```go
db.Callback().Create().Replace("gorm:update_time_stamp", updateTimeStampForCreateCallback)
db.Callback().Update().Replace("gorm:update_time_stamp", updateTimeStampForUpdateCallback)
```
### 验证
访问 AddTag 接口，成功后检查数据库，可发现 created_on 和 modified_on 字段都为当前执行时间

访问 EditTag 接口，可发现 modified_on 为最后一次执行更新的时间

### 拓展
我们想到，在实际项目中硬删除是较少存在的，那么是否可以通过 Callbacks 来完成这个功能呢？

答案是可以的，我们在先前 Model struct 增加 DeletedOn 变量
```go
type Model struct {
    ID int `gorm:"primary_key" json:"id"`
    CreatedOn int `json:"created_on"`
    ModifiedOn int `json:"modified_on"`
    DeletedOn int `json:"deleted_on"`
}
```
### 实现 Callbacks
打开 models 目录下的 models.go 文件，实现以下方法：
```go
func deleteCallback(scope *gorm.Scope) {
    if !scope.HasError() {
        var extraOption string
        if str, ok := scope.Get("gorm:delete_option"); ok {
            extraOption = fmt.Sprint(str)
        }

        deletedOnField, hasDeletedOnField := scope.FieldByName("DeletedOn")

        if !scope.Search.Unscoped && hasDeletedOnField {
            scope.Raw(fmt.Sprintf(
                "UPDATE %v SET %v=%v%v%v",
                scope.QuotedTableName(),
                scope.Quote(deletedOnField.DBName),
                scope.AddToVars(time.Now().Unix()),
                addExtraSpaceIfExist(scope.CombinedConditionSql()),
                addExtraSpaceIfExist(extraOption),
            )).Exec()
        } else {
            scope.Raw(fmt.Sprintf(
                "DELETE FROM %v%v%v",
                scope.QuotedTableName(),
                addExtraSpaceIfExist(scope.CombinedConditionSql()),
                addExtraSpaceIfExist(extraOption),
            )).Exec()
        }
    }
}

func addExtraSpaceIfExist(str string) string {
    if str != "" {
        return " " + str
    }
    return ""
}
```
scope.Get("gorm:delete_option") 检查是否手动指定了 delete_option
scope.FieldByName("DeletedOn") 获取我们约定的删除字段，若存在则 UPDATE 软删除，若不存在则 DELETE 硬删除
scope.QuotedTableName() 返回引用的表名，这个方法 GORM 会根据自身逻辑对表名进行一些处理
scope.CombinedConditionSql() 返回组合好的条件 SQL，看一下方法原型很明了
```go
func (scope *Scope) CombinedConditionSql() string {
    joinSQL := scope.joinsSQL()
    whereSQL := scope.whereSQL()
    if scope.Search.raw {
        whereSQL = strings.TrimSuffix(strings.TrimPrefix(whereSQL, "WHERE ("), ")")
    }
    return joinSQL + whereSQL + scope.groupSQL() +
        scope.havingSQL() + scope.orderSQL() + scope.limitAndOffsetSQL()
}
```
scope.AddToVars 该方法可以添加值作为 SQL 的参数，也可用于防范 SQL 注入
```go
func (scope *Scope) AddToVars(value interface{}) string {
    _, skipBindVar := scope.InstanceGet("skip_bindvar")

    if expr, ok := value.(*expr); ok {
        exp := expr.expr
        for _, arg := range expr.args {
            if skipBindVar {
                scope.AddToVars(arg)
            } else {
                exp = strings.Replace(exp, "?", scope.AddToVars(arg), 1)
            }
        }
        return exp
    }

    scope.SQLVars = append(scope.SQLVars, value)

    if skipBindVar {
        return "?"
    }
    return scope.Dialect().BindVar(len(scope.SQLVars))
}
```
### 注册 Callbacks
在 models.go 的 init 函数中，增加以下删除的回调

db.Callback().Delete().Replace("gorm:delete", deleteCallback)
### 验证
重启服务，访问 DeleteTag 接口，成功后即可发现 deleted_on 字段有值

## Cron定时任务
知识点
完成定时任务的功能


### Cron 表达式格式
|字段名	|是否必填	|允许的值|	允许的特殊字符|
|--------|-----------|----------|-----------|
秒（Seconds）	|Yes	|0-59	|* / , -|
|分（Minutes）|	Yes	|0-59	|* / , -|
|时（Hours）|	Yes|	0-23|	* / , -|
|一个月中的某天|（Day of month）	|Yes	|1-31|	* / , - ?|
|月（Month）	|Yes	|1-12 or JAN-DEC|	* / , -|
|星期几（Day of week）|	Yes	|0-6 or SUN-SAT|	* / , - ?|
Cron 表达式表示一组时间，使用 6 个空格分隔的字段

可以留意到 Golang 的 Cron 比 Crontab 多了一个秒级，以后遇到秒级要求的时候就省事了

### Cron 特殊字符
1、星号 ( * )

星号表示将匹配字段的所有值

2、斜线 ( / )

斜线用户 描述范围的增量，表现为 “N-MAX/x”，first-last/x 的形式，例如 3-59/15 表示此时的第三分钟和此后的每 15 分钟，到 59 分钟为止。即从 N 开始，使用增量直到该特定范围结束。它不会重复

3、逗号 ( , )

逗号用于分隔列表中的项目。例如，在 Day of week 使用“MON，WED，FRI”将意味着星期一，星期三和星期五

4、连字符 ( - )

连字符用于定义范围。例如，9 - 17 表示从上午 9 点到下午 5 点的每个小时

5、问号 ( ? )

不指定值，用于代替 “ * ”，类似 “ _ ” 的存在，不难理解

### 预定义的 Cron 时间表
|输入|	简述|	相当于|
|--------------|-----------------|--------------------|
|@yearly (or @annually)|	1 月 1 日午夜运行一次	|0 0 0 1 1 *|
|@monthly	|每个月的午夜，每个月的第一个月运行一次	|0 0 0 1 * *|
|@weekly	|每周一次，周日午夜运行一次|	0 0 0 * * 0|
|@daily (or @midnight)|	每天午夜运行一次	|0 0 0 * * *|
|@hourly	|每小时运行一次	|0 0 * * * *|
安装


### 实践


就是我怎么硬删除，我什么时候硬删除？这个往往与业务场景有关系，大致为

另外有一套硬删除接口
定时任务清理（或转移、backup）无效数据
在这里我们选用第二种解决方案来进行实践

### 编写硬删除代码
打开 models 目录下的 tag.go、article.go 文件，分别添加以下代码

1、tag.go

func CleanAllTag() bool {
    db.Unscoped().Where("deleted_on != ? ", 0).Delete(&Tag{})

    return true
}
2、article.go

func CleanAllArticle() bool {
    db.Unscoped().Where("deleted_on != ? ", 0).Delete(&Article{})

    return true
}
注意硬删除要使用 Unscoped()，这是 GORM 的约定

### 编写 Cron
在 项目根目录下新建 cron.go 文件，用于编写定时任务的代码，写入文件内容
```go
package main

import (
    "time"
    "log"

    "github.com/robfig/cron"

    "github.com/EDDYCJY/go-gin-example/models"
)

func main() {
    log.Println("Starting...")

    c := cron.New()
    c.AddFunc("* * * * * *", func() {
        log.Println("Run models.CleanAllTag...")
        models.CleanAllTag()
    })
    c.AddFunc("* * * * * *", func() {
        log.Println("Run models.CleanAllArticle...")
        models.CleanAllArticle()
    })

    c.Start()

    t1 := time.NewTimer(time.Second * 10)
    for {
        select {
        case <-t1.C:
            t1.Reset(time.Second * 10)
        }
    }
}
```
在这段程序中，我们做了如下的事情

#### cron.New()
会根据本地时间创建一个新（空白）的 Cron job runner

func New() *Cron {
    return NewWithLocation(time.Now().Location())
}

// NewWithLocation returns a new Cron job runner.
func NewWithLocation(location *time.Location) *Cron {
    return &Cron{
        entries:  nil,
        add:      make(chan *Entry),
        stop:     make(chan struct{}),
        snapshot: make(chan []*Entry),
        running:  false,
        ErrorLog: nil,
        location: location,
    }
}
#### c.AddFunc()
AddFunc 会向 Cron job runner 添加一个 func ，以按给定的时间表运行

func (c *Cron) AddJob(spec string, cmd Job) error {
    schedule, err := Parse(spec)
    if err != nil {
        return err
    }
    c.Schedule(schedule, cmd)
    return nil
}
会首先解析时间表，如果填写有问题会直接 err，无误则将 func 添加到 Schedule 队列中等待执行

func (c *Cron) Schedule(schedule Schedule, cmd Job) {
    entry := &Entry{
        Schedule: schedule,
        Job:      cmd,
    }
    if !c.running {
        c.entries = append(c.entries, entry)
        return
    }

    c.add <- entry
}
#### c.Start()

在当前执行的程序中启动 Cron 调度程序。其实这里的主体是 goroutine + for + select + timer 的调度控制哦

func (c *Cron) Run() {
    if c.running {
        return
    }
    c.running = true
    c.run()
}
time.NewTimer + for + select + t1.Reset
如果你是初学者，大概会有疑问，这是干嘛用的？

*（1）time.NewTimer *

会创建一个新的定时器，持续你设定的时间 d 后发送一个 channel 消息

（2）for + select

阻塞 select 等待 channel

（3）t1.Reset

会重置定时器，让它重新开始计时

注：本文适用于 “t.C 已经取走，可直接使用 Reset”。

总的来说，这段程序是为了阻塞主程序而编写的，希望你带着疑问来想，有没有别的办法呢？

有的，你直接 select{} 也可以完成这个需求 :)

## 优化配置结构及实现图片上传

### 优化配置结构
一、讲解
在先前章节中，采用了直接读取 KEY 的方式去存储配置项，而本次需求中，需要增加图片的配置项，总体就有些冗余了

我们采用以下解决方法：

- 映射结构体：使用 MapTo 来设置配置参数
- 配置统管：所有的配置项统管到 setting 中
映射结构体（示例）
在 go-ini 中可以采用 MapTo 的方式来映射结构体，例如：
```go
type Server struct {
    RunMode string
    HttpPort int
    ReadTimeout time.Duration
    WriteTimeout time.Duration
}

var ServerSetting = &Server{}

func main() {
    Cfg, err := ini.Load("conf/app.ini")
    if err != nil {
        log.Fatalf("Fail to parse 'conf/app.ini': %v", err)
    }

    err = Cfg.Section("server").MapTo(ServerSetting)
    if err != nil {
        log.Fatalf("Cfg.MapTo ServerSetting err: %v", err)
    }
}
```
在这段代码中，可以注意 ServerSetting 取了地址，为什么 MapTo 必须地址入参呢？
```go
// MapTo maps section to given struct.
func (s *Section) MapTo(v interface{}) error {
    typ := reflect.TypeOf(v)
    val := reflect.ValueOf(v)
    if typ.Kind() == reflect.Ptr {
        typ = typ.Elem()
        val = val.Elem()
    } else {
        return errors.New("cannot map to non-pointer struct")
    }

    return s.mapTo(val, false)
}
```
在 MapTo 中 typ.Kind() == reflect.Ptr 约束了必须使用指针，否则会返回 cannot map to non-pointer struct 的错误。这个是表面原因

更往内探究，可以认为是 field.Set 的原因，当执行 val := reflect.ValueOf(v) ，函数通过传递 v 拷贝创建了 val，但是 val 的改变并不能更改原始的 v，要想 val 的更改能作用到 v，则必须传递 v 的地址

显然 go-ini 里也是包含修改原始值这一项功能的，你觉得是什么原因呢？

### 配置统管

在 Go 中，当存在多个 init 函数时，执行顺序为：

- 相同包下的 init 函数：按照源文件编译顺序决定执行顺序（默认按文件名排序）
- 不同包下的 init 函数：按照包导入的依赖关系决定先后顺序
- 所以要避免多 init 的情况，尽量由程序把控初始化的先后顺序

二、落实
修改配置文件
打开 conf/app.ini 将配置文件修改为大驼峰命名，另外我们增加了 5 个配置项用于上传图片的功能，4 个文件日志方面的配置项

[app]
PageSize = 10
JwtSecret = 233

RuntimeRootPath = runtime/

ImagePrefixUrl = http://127.0.0.1:8000
ImageSavePath = upload/images/
# MB
ImageMaxSize = 5
ImageAllowExts = .jpg,.jpeg,.png

LogSavePath = logs/
LogSaveName = log
LogFileExt = log
TimeFormat = 20060102

[server]
#debug or release
RunMode = debug
HttpPort = 8000
ReadTimeout = 60
WriteTimeout = 60

[database]
Type = mysql
User = root
Password = rootroot
Host = 127.0.0.1:3306
Name = blog
TablePrefix = blog_
优化配置读取及设置初始化顺序
第一步
将散落在其他文件里的配置都删掉，统一在 setting 中处理以及修改 init 函数为 Setup 方法

打开 pkg/setting/setting.go 文件，修改如下：

package setting

import (
    "log"
    "time"

    "github.com/go-ini/ini"
)

type App struct {
    JwtSecret string
    PageSize int
    RuntimeRootPath string

    ImagePrefixUrl string
    ImageSavePath string
    ImageMaxSize int
    ImageAllowExts []string

    LogSavePath string
    LogSaveName string
    LogFileExt string
    TimeFormat string
}

var AppSetting = &App{}

type Server struct {
    RunMode string
    HttpPort int
    ReadTimeout time.Duration
    WriteTimeout time.Duration
}

var ServerSetting = &Server{}

type Database struct {
    Type string
    User string
    Password string
    Host string
    Name string
    TablePrefix string
}

var DatabaseSetting = &Database{}

func Setup() {
    Cfg, err := ini.Load("conf/app.ini")
    if err != nil {
        log.Fatalf("Fail to parse 'conf/app.ini': %v", err)
    }

    err = Cfg.Section("app").MapTo(AppSetting)
    if err != nil {
        log.Fatalf("Cfg.MapTo AppSetting err: %v", err)
    }

    AppSetting.ImageMaxSize = AppSetting.ImageMaxSize * 1024 * 1024

    err = Cfg.Section("server").MapTo(ServerSetting)
    if err != nil {
        log.Fatalf("Cfg.MapTo ServerSetting err: %v", err)
    }

    ServerSetting.ReadTimeout = ServerSetting.ReadTimeout * time.Second
    ServerSetting.WriteTimeout = ServerSetting.WriteTimeout * time.Second

    err = Cfg.Section("database").MapTo(DatabaseSetting)
    if err != nil {
        log.Fatalf("Cfg.MapTo DatabaseSetting err: %v", err)
    }
}
在这里，我们做了如下几件事：

编写与配置项保持一致的结构体（App、Server、Database）
使用 MapTo 将配置项映射到结构体上
对一些需特殊设置的配置项进行再赋值
需要你去做的事：

将 models.go、setting.go、pkg/logging/log.go 的 init 函数修改为 Setup 方法
将 models/models.go 独立读取的 DB 配置项删除，改为统一读取 setting
将 pkg/logging/file 独立的 LOG 配置项删除，改为统一读取 setting
这几项比较基础，并没有贴出来，我希望你可以自己动手，有问题的话可右拐 项目地址

第二步
在这一步我们要设置初始化的流程，打开 main.go 文件，修改内容：

func main() {
    setting.Setup()
    models.Setup()
    logging.Setup()

    endless.DefaultReadTimeOut = setting.ServerSetting.ReadTimeout
    endless.DefaultWriteTimeOut = setting.ServerSetting.WriteTimeout
    endless.DefaultMaxHeaderBytes = 1 << 20
    endPoint := fmt.Sprintf(":%d", setting.ServerSetting.HttpPort)

    server := endless.NewServer(endPoint, routers.InitRouter())
    server.BeforeBegin = func(add string) {
        log.Printf("Actual pid is %d", syscall.Getpid())
    }

    err := server.ListenAndServe()
    if err != nil {
        log.Printf("Server err: %v", err)
    }
}
修改完毕后，就成功将多模块的初始化函数放到启动流程中了（先后顺序也可以控制）

验证
在这里为止，针对本需求的配置优化就完毕了，你需要执行 go run main.go 验证一下你的功能是否正常哦

顺带留个基础问题，大家可以思考下

ServerSetting.ReadTimeout = ServerSetting.ReadTimeout * time.Second
ServerSetting.WriteTimeout = ServerSetting.ReadTimeout * time.Second
若将 setting.go 文件中的这两行删除，会出现什么问题，为什么呢？

抽离 File
在先前版本中，在 logging/file.go 中使用到了 os 的一些方法，我们通过前期规划发现，这部分在上传图片功能中可以复用

第一步
在 pkg 目录下新建 file/file.go ，写入文件内容如下：

package file

import (
    "os"
    "path"
    "mime/multipart"
    "io/ioutil"
)

func GetSize(f multipart.File) (int, error) {
    content, err := ioutil.ReadAll(f)

    return len(content), err
}

func GetExt(fileName string) string {
    return path.Ext(fileName)
}

func CheckNotExist(src string) bool {
    _, err := os.Stat(src)

    return os.IsNotExist(err)
}

func CheckPermission(src string) bool {
    _, err := os.Stat(src)

    return os.IsPermission(err)
}

func IsNotExistMkDir(src string) error {
    if notExist := CheckNotExist(src); notExist == true {
        if err := MkDir(src); err != nil {
            return err
        }
    }

    return nil
}

func MkDir(src string) error {
    err := os.MkdirAll(src, os.ModePerm)
    if err != nil {
        return err
    }

    return nil
}

func Open(name string, flag int, perm os.FileMode) (*os.File, error) {
    f, err := os.OpenFile(name, flag, perm)
    if err != nil {
        return nil, err
    }

    return f, nil
}
在这里我们一共封装了 7 个 方法

GetSize：获取文件大小
GetExt：获取文件后缀
CheckNotExist：检查文件是否存在
CheckPermission：检查文件权限
IsNotExistMkDir：如果不存在则新建文件夹
MkDir：新建文件夹
Open：打开文件
在这里我们用到了 mime/multipart 包，它主要实现了 MIME 的 multipart 解析，主要适用于 HTTP 和常见浏览器生成的 multipart 主体

multipart 又是什么，rfc2388 的 multipart/form-data 了解一下

第二步
我们在第一步已经将 file 重新封装了一层，在这一步我们将原先 logging 包的方法都修改掉

1、打开 pkg/logging/file.go 文件，修改文件内容：

package logging

import (
    "fmt"
    "os"
    "time"

    "github.com/EDDYCJY/go-gin-example/pkg/setting"
    "github.com/EDDYCJY/go-gin-example/pkg/file"
)

func getLogFilePath() string {
    return fmt.Sprintf("%s%s", setting.AppSetting.RuntimeRootPath, setting.AppSetting.LogSavePath)
}

func getLogFileName() string {
    return fmt.Sprintf("%s%s.%s",
        setting.AppSetting.LogSaveName,
        time.Now().Format(setting.AppSetting.TimeFormat),
        setting.AppSetting.LogFileExt,
    )
}

func openLogFile(fileName, filePath string) (*os.File, error) {
    dir, err := os.Getwd()
    if err != nil {
        return nil, fmt.Errorf("os.Getwd err: %v", err)
    }

    src := dir + "/" + filePath
    perm := file.CheckPermission(src)
    if perm == true {
        return nil, fmt.Errorf("file.CheckPermission Permission denied src: %s", src)
    }

    err = file.IsNotExistMkDir(src)
    if err != nil {
        return nil, fmt.Errorf("file.IsNotExistMkDir src: %s, err: %v", src, err)
    }

    f, err := file.Open(src + fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        return nil, fmt.Errorf("Fail to OpenFile :%v", err)
    }

    return f, nil
}
我们将引用都改为了 file/file.go 包里的方法

2、打开 pkg/logging/log.go 文件，修改文件内容:

package logging

...

func Setup() {
    var err error
    filePath := getLogFilePath()
    fileName := getLogFileName()
    F, err = openLogFile(fileName, filePath)
    if err != nil {
        log.Fatalln(err)
    }

    logger = log.New(F, DefaultPrefix, log.LstdFlags)
}

...
由于原方法形参改变了，因此 openLogFile 也需要调整

实现上传图片接口
这一小节，我们开始实现上次图片相关的一些方法和功能

首先需要在 blog_article 中增加字段 cover_image_url，格式为 varchar(255) DEFAULT '' COMMENT '封面图片地址'

第零步
一般不会直接将上传的图片名暴露出来，因此我们对图片名进行 MD5 来达到这个效果

在 util 目录下新建 md5.go，写入文件内容：

package util

import (
    "crypto/md5"
    "encoding/hex"
)

func EncodeMD5(value string) string {
    m := md5.New()
    m.Write([]byte(value))

    return hex.EncodeToString(m.Sum(nil))
}
第一步
在先前我们已经把底层方法给封装好了，实质这一步为封装 image 的处理逻辑

在 pkg 目录下新建 upload/image.go 文件，写入文件内容：

package upload

import (
    "os"
    "path"
    "log"
    "fmt"
    "strings"
    "mime/multipart"

    "github.com/EDDYCJY/go-gin-example/pkg/file"
    "github.com/EDDYCJY/go-gin-example/pkg/setting"
    "github.com/EDDYCJY/go-gin-example/pkg/logging"
    "github.com/EDDYCJY/go-gin-example/pkg/util"
)

func GetImageFullUrl(name string) string {
    return setting.AppSetting.ImagePrefixUrl + "/" + GetImagePath() + name
}

func GetImageName(name string) string {
    ext := path.Ext(name)
    fileName := strings.TrimSuffix(name, ext)
    fileName = util.EncodeMD5(fileName)

    return fileName + ext
}

func GetImagePath() string {
    return setting.AppSetting.ImageSavePath
}

func GetImageFullPath() string {
    return setting.AppSetting.RuntimeRootPath + GetImagePath()
}

func CheckImageExt(fileName string) bool {
    ext := file.GetExt(fileName)
    for _, allowExt := range setting.AppSetting.ImageAllowExts {
        if strings.ToUpper(allowExt) == strings.ToUpper(ext) {
            return true
        }
    }

    return false
}

func CheckImageSize(f multipart.File) bool {
    size, err := file.GetSize(f)
    if err != nil {
        log.Println(err)
        logging.Warn(err)
        return false
    }

    return size <= setting.AppSetting.ImageMaxSize
}

func CheckImage(src string) error {
    dir, err := os.Getwd()
    if err != nil {
        return fmt.Errorf("os.Getwd err: %v", err)
    }

    err = file.IsNotExistMkDir(dir + "/" + src)
    if err != nil {
        return fmt.Errorf("file.IsNotExistMkDir err: %v", err)
    }

    perm := file.CheckPermission(src)
    if perm == true {
        return fmt.Errorf("file.CheckPermission Permission denied src: %s", src)
    }

    return nil
}
在这里我们实现了 7 个方法，如下：

GetImageFullUrl：获取图片完整访问 URL
GetImageName：获取图片名称
GetImagePath：获取图片路径
GetImageFullPath：获取图片完整路径
CheckImageExt：检查图片后缀
CheckImageSize：检查图片大小
CheckImage：检查图片
这里基本是对底层代码的二次封装，为了更灵活的处理一些图片特有的逻辑，并且方便修改，不直接对外暴露下层

第二步
这一步将编写上传图片的业务逻辑，在 routers/api 目录下 新建 upload.go 文件，写入文件内容:

package api

import (
    "net/http"

    "github.com/gin-gonic/gin"

    "github.com/EDDYCJY/go-gin-example/pkg/e"
    "github.com/EDDYCJY/go-gin-example/pkg/logging"
    "github.com/EDDYCJY/go-gin-example/pkg/upload"
)

func UploadImage(c *gin.Context) {
    code := e.SUCCESS
    data := make(map[string]string)

    file, image, err := c.Request.FormFile("image")
    if err != nil {
        logging.Warn(err)
        code = e.ERROR
        c.JSON(http.StatusOK, gin.H{
            "code": code,
            "msg":  e.GetMsg(code),
            "data": data,
        })
    }

    if image == nil {
        code = e.INVALID_PARAMS
    } else {
        imageName := upload.GetImageName(image.Filename)
        fullPath := upload.GetImageFullPath()
        savePath := upload.GetImagePath()

        src := fullPath + imageName
        if ! upload.CheckImageExt(imageName) || ! upload.CheckImageSize(file) {
            code = e.ERROR_UPLOAD_CHECK_IMAGE_FORMAT
        } else {
            err := upload.CheckImage(fullPath)
            if err != nil {
                logging.Warn(err)
                code = e.ERROR_UPLOAD_CHECK_IMAGE_FAIL
            } else if err := c.SaveUploadedFile(image, src); err != nil {
                logging.Warn(err)
                code = e.ERROR_UPLOAD_SAVE_IMAGE_FAIL
            } else {
                data["image_url"] = upload.GetImageFullUrl(imageName)
                data["image_save_url"] = savePath + imageName
            }
        }
    }

    c.JSON(http.StatusOK, gin.H{
        "code": code,
        "msg":  e.GetMsg(code),
        "data": data,
    })
}
所涉及的错误码（需在 pkg/e/code.go、msg.go 添加）：

// 保存图片失败
ERROR_UPLOAD_SAVE_IMAGE_FAIL = 30001
// 检查图片失败
ERROR_UPLOAD_CHECK_IMAGE_FAIL = 30002
// 校验图片错误，图片格式或大小有问题
ERROR_UPLOAD_CHECK_IMAGE_FORMAT = 30003
在这一大段的业务逻辑中，我们做了如下事情：

c.Request.FormFile：获取上传的图片（返回提供的表单键的第一个文件）
CheckImageExt、CheckImageSize 检查图片大小，检查图片后缀
CheckImage：检查上传图片所需（权限、文件夹）
SaveUploadedFile：保存图片
总的来说，就是 入参 -> 检查 -》 保存 的应用流程

第三步
打开 routers/router.go 文件，增加路由 r.POST("/upload", api.UploadImage) ，如：

func InitRouter() *gin.Engine {
    r := gin.New()
    ...
    r.GET("/auth", api.GetAuth)
    r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
    r.POST("/upload", api.UploadImage)

    apiv1 := r.Group("/api/v1")
    apiv1.Use(jwt.JWT())
    {
        ...
    }

    return r
}
验证
最后我们请求一下上传图片的接口，测试所编写的功能

image

检查目录下是否含文件（注意权限问题）

$ pwd
$GOPATH/src/github.com/EDDYCJY/go-gin-example/runtime/upload/images

$ ll
... 96a3be3cf272e017046d1b2674a52bd3.jpg
... c39fa784216313cf2faa7c98739fc367.jpeg
在这里我们一共返回了 2 个参数，一个是完整的访问 URL，另一个为保存路径

实现 http.FileServer
在完成了上一小节后，我们还需要让前端能够访问到图片，一般是如下：

CDN
http.FileSystem
在公司的话，CDN 或自建分布式文件系统居多，也不需要过多关注。而在实践里的话肯定是本地搭建了，Go 本身对此就有很好的支持，而 Gin 更是再封装了一层，只需要在路由增加一行代码即可

r.StaticFS
打开 routers/router.go 文件，增加路由 r.StaticFS("/upload/images", http.Dir(upload.GetImageFullPath()))，如：

func InitRouter() *gin.Engine {
    ...
    r.StaticFS("/upload/images", http.Dir(upload.GetImageFullPath()))

    r.GET("/auth", api.GetAuth)
    r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))
    r.POST("/upload", api.UploadImage)
    ...
}
它做了什么
当访问 $HOST/upload/images 时，将会读取到 $GOPATH/src/github.com/EDDYCJY/go-gin-example/runtime/upload/images 下的文件

而这行代码又做了什么事呢，我们来看看方法原型

// StaticFS works just like `Static()` but a custom `http.FileSystem` can be used instead.
// Gin by default user: gin.Dir()
func (group *RouterGroup) StaticFS(relativePath string, fs http.FileSystem) IRoutes {
    if strings.Contains(relativePath, ":") || strings.Contains(relativePath, "*") {
        panic("URL parameters can not be used when serving a static folder")
    }
    handler := group.createStaticHandler(relativePath, fs)
    urlPattern := path.Join(relativePath, "/*filepath")

    // Register GET and HEAD handlers
    group.GET(urlPattern, handler)
    group.HEAD(urlPattern, handler)
    return group.returnObj()
}
首先在暴露的 URL 中禁止了 * 和 : 符号的使用，通过 createStaticHandler 创建了静态文件服务，实质最终调用的还是 fileServer.ServeHTTP 和一些处理逻辑了

func (group *RouterGroup) createStaticHandler(relativePath string, fs http.FileSystem) HandlerFunc {
    absolutePath := group.calculateAbsolutePath(relativePath)
    fileServer := http.StripPrefix(absolutePath, http.FileServer(fs))
    _, nolisting := fs.(*onlyfilesFS)
    return func(c *Context) {
        if nolisting {
            c.Writer.WriteHeader(404)
        }
        fileServer.ServeHTTP(c.Writer, c.Request)
    }
}
http.StripPrefix
我们可以留意下 fileServer := http.StripPrefix(absolutePath, http.FileServer(fs)) 这段语句，在静态文件服务中很常见，它有什么作用呢？

http.StripPrefix 主要作用是从请求 URL 的路径中删除给定的前缀，最终返回一个 Handler

通常 http.FileServer 要与 http.StripPrefix 相结合使用，否则当你运行：

http.Handle("/upload/images", http.FileServer(http.Dir("upload/images")))
会无法正确的访问到文件目录，因为 /upload/images 也包含在了 URL 路径中，必须使用：

http.Handle("/upload/images", http.StripPrefix("upload/images", http.FileServer(http.Dir("upload/images"))))
/*filepath
到下面可以看到 urlPattern := path.Join(relativePath, "/*filepath")，/*filepath 你是谁，你在这里有什么用，你是 Gin 的产物吗?

通过语义可得知是路由的处理逻辑，而 Gin 的路由是基于 httprouter 的，通过查阅文档可得到以下信息

Pattern: /src/*filepath

 /src/                     match
 /src/somefile.go          match
 /src/subdir/somefile.go   match
*filepath 将匹配所有文件路径，并且 *filepath 必须在 Pattern 的最后

验证
重新执行 go run main.go ，去访问刚刚在 upload 接口得到的图片地址，检查 http.FileSystem 是否正常