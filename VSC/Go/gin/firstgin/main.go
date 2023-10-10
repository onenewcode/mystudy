package main

import (
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"

    // "github.com/gorilla/sessions"
	//中间件限制post提交文件的大小
	limits "github.com/gin-contrib/size"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/testdata/protoexample"
)

// 定义接收数据的结构体
type Login struct {
    // binding:"required"修饰的字段，若接收为空值，则报错，是必须字段
    User    string `form:"username" json:"user" uri:"user" xml:"user" binding:"required"`
    Pssword string `form:"password" json:"password" uri:"password" xml:"password" binding:"required"`
 }
 //中间件
 func MiddleWare() gin.HandlerFunc {
    return func(c *gin.Context) {
        t := time.Now()
        fmt.Println("中间件开始执行了")
        // 设置变量到Context的key中，可以通过Get()取
        c.Set("request", "中间件")
        c.Next()
        // 中间件执行完后续的一些事情
        status := c.Writer.Status()
        fmt.Println("中间件执行完毕", status)
        t2 := time.Since(t)
        fmt.Println("time:", t2)
    }
}

//session
// 初始化一个cookie存储对象
// something-very-secret应该是一个你自己的密匙，只要不被别人知道就行
// var store = sessions.NewCookieStore([]byte("something-very-secret"))
// func SaveSession(w http.ResponseWriter, r *http.Request) {
//     // Get a session. We're ignoring the error resulted from decoding an
//     // existing session: Get() always returns a session, even if empty.

//     //　获取一个session对象，session-name是session的名字
//     session, err := store.Get(r, "session-name")
//     if err != nil {
//         http.Error(w, err.Error(), http.StatusInternalServerError)
//         return
//     }

//     // 在session中存储值
//     session.Values["foo"] = "bar"
//     session.Values[42] = 43
//     // 保存更改
//     session.Save(r, w)
// }
// func GetSession(w http.ResponseWriter, r *http.Request) {
//     session, err := store.Get(r, "session-name")
//     if err != nil {
//         http.Error(w, err.Error(), http.StatusInternalServerError)
//         return
//     }
//     foo := session.Values["foo"]
//     fmt.Println(foo)
// }

//Person ..
type Person struct {
    //不能为空并且大于10
    Age      int       `form:"age" binding:"required,gt=10"`
    Name     string    `form:"name" binding:"required"`
    Birthday time.Time `form:"birthday" time_format:"2006-01-02" time_utc:"1"`
}
func main() {
	// 1.创建路由
   // 默认使用了2个中间件Logger(), Recovery()
	r := gin.Default()
	// 2.绑定路由规则，执行的函数
	// gin.Context，封装了request和response
	r.GET("/", func(c *gin.Context) {
		c.String(http.StatusOK, "hello World!")
	})



	// 3.监听端口，默认在8080
	// Run("里面不指定端口号默认为8080")
    //提取name参数
	r.GET("/user/:name/*action", func(c *gin.Context) {
        name := c.Param("name")
        action := c.Param("action")
        //截取/
        action = strings.Trim(action, "/")
        c.String(http.StatusOK, name+" is "+action)
    })



    //访问http://localhost:8000/user?name=zs，返回hello zs
    r.GET("/user", func(c *gin.Context) {
        //指定默认值
        //http://localhost:8080/user 才会打印出来默认的值
        name := c.DefaultQuery("name", "枯藤")
        c.String(http.StatusOK, fmt.Sprintf("hello %s", name))
    })

    //获取表单数据
    r.POST("/form", func(c *gin.Context) {
        types := c.DefaultPostForm("type", "post")
        username := c.PostForm("username")
        password := c.PostForm("userpassword")
        // c.String(http.StatusOK, fmt.Sprintf("username:%s,password:%s,type:%s", username, password, types))
        c.String(http.StatusOK, fmt.Sprintf("username:%s,password:%s,type:%s", username, password, types))
    })

    //准确的说应该是限制每次处理文件所占用的最大内存，上传后的文件。
    r.MaxMultipartMemory = 8 << 20
    //限制文件传输的大小，后面跟的是字节大小
    r.Use(limits.RequestSizeLimiter(2<<22)) 
    r.POST("/upload", func(c *gin.Context) {
        
        file, err := c.FormFile("file")
        if err != nil {
            c.String(500, "上传图片出错")
        }
        // c.JSON(200, gin.H{"message": file.Header.Context})
        //获取文件传输的类型
        if file.Header.Get("Content-Type") != "image/png" {
            fmt.Println("只允许上传png图片")
            return
        }
        c.SaveUploadedFile(file, "./static/img/"+file.Filename)
        c.String(http.StatusOK, file.Filename)
    })

    //存大量文件
    r.POST("/uploadmultiple", func(c *gin.Context) {
       form, err := c.MultipartForm()
       if err != nil {
          c.String(http.StatusBadRequest, fmt.Sprintf("get err %s", err.Error()))
       }
       // 获取所有图片
       files := form.File["files"]
       // 遍历所有图片
       for _, file := range files {
          // 逐个存
          if err := c.SaveUploadedFile(file, "./static/img/"+file.Filename); err != nil {
             c.String(http.StatusBadRequest, fmt.Sprintf("upload err %s", err.Error()))
             return
          }
       }
       c.String(200, fmt.Sprintf("upload ok %d files", len(files)))
    })


//404界面设置
    r.NoRoute(func(c *gin.Context) {
        c.String(http.StatusNotFound, "404 not found2222")
    })


    //数据绑定jason
    r.POST("loginJSON", func(c *gin.Context) {
        // 声明接收的变量
        var json Login
        // 将request的body中的数据，自动按照json格式解析到结构体
        if err := c.ShouldBindJSON(&json); err != nil {
           // 返回错误信息
           // gin.H封装了生成json数据的工具
           c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
           return
        }
        // 判断用户名密码是否正确
        if json.User != "root" || json.Pssword != "admin" {
           c.JSON(http.StatusBadRequest, gin.H{"status": "304"})
           return
        }
        c.JSON(http.StatusOK, gin.H{"status": "200"})
     })



     //数据绑定表单
     r.POST("/loginForm", func(c *gin.Context) {
        // 声明接收的变量
        var form Login
        // Bind()默认解析并绑定form格式
        // 根据请求头中content-type自动推断
        if err := c.Bind(&form); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        // 判断用户名密码是否正确
        if form.User != "root" || form.Pssword != "admin" {
            c.JSON(http.StatusBadRequest, gin.H{"status": "304"})
            return
        }
        c.JSON(http.StatusOK, gin.H{"status": "200"})
    })

    // url绑定
    r.GET("/:user/:password", func(c *gin.Context) {
        // 声明接收的变量
        var login Login
        // Bind()默认解析并绑定form格式
        // 根据请求头中content-type自动推断
        if err := c.ShouldBindUri(&login); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }
        // 判断用户名密码是否正确
        if login.User != "root" || login.Pssword != "admin" {
            c.JSON(http.StatusBadRequest, gin.H{"status": "304"})
            return
        }
        c.JSON(http.StatusOK, gin.H{"status": "200"})
    })


    //1. json响应
    r.GET("/someJSON", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "someJSON", "status": 200})
    })


    // 2. 结构体响应
    r.GET("/someStruct", func(c *gin.Context) {
        var msg struct {
            Name    string
            Message string
            Number  int
        }
        msg.Name = "root"
        msg.Message = "message"
        msg.Number = 123
        c.JSON(200, msg)
    })
    // 3.XML
    r.GET("/someXML", func(c *gin.Context) {
        c.XML(200, gin.H{"message": "abc"})
    })
    // 4.YAML响应
    r.GET("/someYAML", func(c *gin.Context) {
        c.YAML(200, gin.H{"name": "zhangsan"})
    })
    // 5.protobuf格式,谷歌开发的高效存储读取的工具
    // 数组？切片？如果自己构建一个传输格式，应该是什么格式？
    r.GET("/someProtoBuf", func(c *gin.Context) {
        reps := []int64{int64(1), int64(2)}
        // 定义数据
        label := "label"
        // 传protobuf格式数据
        data := &protoexample.Test{
            Label: &label,
            Reps:  reps,
        }
        c.ProtoBuf(200, data)
    })

    //html渲染

    //加载文件夹
    r.LoadHTMLGlob("./static/html/*")
    r.GET("/index", func(c *gin.Context) {
        c.HTML(http.StatusOK, "index.html", gin.H{"title": "我是测试", "ce": "123456"})
    })

    //重定向
    r.GET("/index2", func(c *gin.Context) {
        c.Redirect(http.StatusMovedPermanently, "http://www.5lmh.com")
    })

    //同步异步处理
    r.GET("/long_async", func(c *gin.Context) {
        // 需要搞一个副本
        copyContext := c.Copy()
        // 异步处理
        go func() {
            time.Sleep(3 * time.Second)
            log.Println("异步执行：" + copyContext.Request.URL.Path)
        }()
    })
    // 2.同步
    r.GET("/long_sync", func(c *gin.Context) {
        time.Sleep(3 * time.Second)
        log.Println("同步执行：" + c.Request.URL.Path)
    })

    //局部中间件
    r.GET("/ce2", MiddleWare(), func(c *gin.Context) {
        // 取值
        req, _ := c.Get("request")
        fmt.Println("request:", req)
        // 页面接收
        c.JSON(200, gin.H{"request": req})
    })
    //中间件
    // 注册中间件
    r.Use(MiddleWare())
    // {}为了代码规范
    {
        r.GET("/ce", func(c *gin.Context) {
            // 取值
            req, _ := c.Get("request")
            fmt.Println("request:", req)
            // 页面接收
            c.JSON(200, gin.H{"request": req})
        })

    }

    //cookie
    r.GET("cookie", func(c *gin.Context) {
        // 获取客户端是否携带cookie
        cookie, err := c.Cookie("key_cookie")
        if err != nil {
           cookie = "NotSet"
           // 给客户端设置cookie
           //  maxAge int, 单位为秒
           // path,cookie所在目录
           // domain string,域名
           //   secure 是否智能通过https访问
           // httpOnly bool  是否允许别人通过js获取自己的cookie
           c.SetCookie("key_cookie", "value_cookie", 60, "/",
              "localhost", false, true)
        }
        fmt.Printf("cookie的值是： %s\n", cookie)
     })

     

     //结构体参数检验
     r.GET("/5lmh", func(c *gin.Context) {
        var person Person
        if err := c.ShouldBind(&person); err != nil {
            c.String(500, fmt.Sprint(err))
            return
        }
        c.String(200, fmt.Sprintf("%#v", person))
    })
	r.Run(":8000")
	return
}
