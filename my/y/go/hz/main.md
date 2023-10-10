# 基本特性
## Engine
server.Hertz 是 Hertz 的核心类型，它由 route.Engine 以及 signalWaiter 组成，Hertz 服务器的启动、路由注册、中间件注册以及退出等重要方法均包含在 server.Hertz 中。以下是 server.Hertz 的定义：
```go
type Hertz struct {
    *route.Engine 
    // 用于接收信号以实现优雅退出 
    signalWaiter func (err chan error) error
}
```
### 配置信息
|配置项|	默认值|	说明|
|-----------------|----------------------|-------------------------|
|WithTransport|	network.NewTransporter|	更换底层 transport|
|WithHostPorts	|:8888	|指定监听的地址和端口|
|WithKeepAliveTimeout|	1min|	tcp 长连接保活时间，一般情况下不用修改，更应该关注 idleTimeout|
|WithReadTimeout	|3min	|底层读取数据超时时间|
|WithIdleTimeout|	3min|	长连接请求链接空闲超时时间|
|WithMaxRequestBodySize|	4 * 1024 * 1024|	配置最大的请求体大小|
|WithRedirectTrailingSlash|	true|	自动根据末尾的 / 转发，例如：如果 router 只有 /foo/，那么 /foo 会重定向到 /foo/ ；如果只有 /foo，那么 /foo/ 会重定向到 /foo|
|WithRemoveExtraSlash	|false	|RemoveExtraSlash 当有额外的 / 时也可以当作参数。如：user/:name，如果开启该选项 user//xiaoming 也可匹配上参数|
|WithUnescapePathValues|	true|	如果开启，请求路径会被自动转义（eg. ‘%2F’ -> ‘/'）。如果 UseRawPath 为 false（默认情况），则 UnescapePathValues 实际上为 true，因为 .URI().Path() 将被使用，它已经是转义后的。设置该参数为 false，需要配合 WithUseRawPath(true)|
|WithUseRawPath	|false	|如果开启，会使用原始 path 进行路由匹配|
|WithHandleMethodNotAllowed|	false|	如果开启，当当前路径不能被匹配上时，server 会去检查其他方法是否注册了当前路径的路由，如果存在则会响应"Method Not Allowed"，并返回状态码 405; 如果没有，则会用 NotFound 的 handler 进行处理|
|WithDisablePreParseMultipartForm|	false|	如果开启，则不会预处理 multipart form。可以通过 ctx.Request.Body() 获取到 body 后由用户处理|
|WithStreamBody	|false|	如果开启，则会使用流式处理 body|
|WithNetwork|	“tcp”|	设置网络协议，可选：tcp，udp，unix（unix domain socket），默认为 tcp|
|WithExitWaitTime|	5s|	设置优雅退出时间。Server 会停止建立新的连接，并对关闭后的每一个请求设置 Connection: Close 的 header，当到达设定的时间关闭 Server。当所有连接已经关闭时，Server 可以提前关闭|
|WithTLS|	nil	|配置 server tls 能力，详情可见 TLS|
|WithListenConfig|	nil|	设置监听器配置，可用于设置是否允许 reuse port 等|
|WithALPN	|false	|是否开启 ALPN|
|WithTracer|	[]interface{}{}|	注入 tracer 实现，如不注入 Tracer 实现，默认关闭|
|WithTraceLevel	|LevelDetailed	|设置 trace level|
|WithWriteTimeout|	无限长|	写入数据超时时间|
|WithRedirectFixedPath|	false|	如果开启，当当前请求路径不能匹配上时，server 会尝试修复请求路径并重新进行匹配，如果成功匹配并且为 GET 请求则会返回状态码 301 进行重定向，其他请求方式返回 308 进行重定向|
|WithBasePath|	/	|设置基本路径，前缀和后缀必须为 / |
|WithMaxKeepBodySize|	4 * 1024 * 1024|	设置回收时保留的请求体和响应体的最大大小。单位：字节|
|WithGetOnly	|false	|如果开启则只接受 GET 请求|
|WithKeepAlive|	true|	如果开启则使用 HTTP 长连接|
|WithAltTransport	|network.NewTransporter	|设置备用 transport|
|WithH2C|	|false|	设置是否开启 H2C|
|WithReadBufferSize	|4 * 1024|	设置读缓冲区大小，同时限制 HTTP header 大小|
|WithRegistry|	registry.NoopRegistry, nil	|设置注册中心配置，服务注册信息|
|WithAutoReloadRender|	false, 0	|设置自动重载渲染配置|
|WithDisablePrintRoute|	false	|设置是否禁用 debugPrintRoute|
|WithOnAccept|	nil|	设置在 netpoll 中当一个连接被接受但不能接收数据时的回调函数，在 go net 中在转换 TLS 连接之前被调用|
|WithOnConnect	|nil	|设置 onConnect 函数。它可以接收来自 netpoll 连接的数据。在 go net 中，它将在转换 TLS 连接后被调用|
|WithDisableHeaderNamesNormalizing|	false|	设置是否禁用 Request 和 Response Header 名字的规范化 (首字母和破折号后第一个字母大写)|

### 初始化服务
```go
// Default 用于初始化服务，默认使用了 Recovery 中间件以保证服务在运行时不会因为 panic 导致服务崩溃。
func Default(opts ...config.Option) *Hertz 
// New 用于初始化服务，没有使用默认的 Recovery 中间件。
func New(opts ...config.Option) *Hertz
```
**例子**：
```go
func main() {
    h := server.New()
    h.Spin()
}
```
### 服务运行与退出
```go
// Spin 函数用于运行 Hertz 服务器，接收到退出信号后可退出服务。
// 在使用 服务注册发现 的功能时，Spin 会在服务启动时将服务注册进入注册中心，并使用 signalWaiter 监测服务异常。
func (h *Hertz) Spin()
// Run 函数用于运行 Hertz 服务器，接收到退出信号后可退出服务。该函数不支持服务的优雅退出，除非有特殊需求，不然一般使用 Spin 函数用于运行服务。
func (engine *Engine) Run() (err error)
// SetCustomSignalWaiter 函数用于自定义服务器接收信号后的处理函数，若没有设置自定义函数，Hertz 使用 waitSignal 函数作为信号处理的默认实现方式，
func (h *Hertz) SetCustomSignalWaiter(f func(err chan error) error)
```

### 中间件
```go
func (engine *Engine) Use(middleware ...app.HandlerFunc) IRoutes
```

Use 函数用于将中间件注册进入路由。

Hertz 支持用户自定义中间件，Hertz 已经实现了一些常用的中间件，详情见 hertz-contrib。

Hertz 支持的中间件的使用方法包括全局注册、路由组级别和单一路由级别的注册。

Use 函数中 middleware 的形参必须为 app.HandlerFunc 的 http 处理函数：
```go
type HandlerFunc func (ctx context.Context, c *app.RequestContext)
```

函数签名：
```go
func (engine *Engine) Use(middleware ...app.HandlerFunc) IRoutes

```
示例代码：
```go
func main() {
    h := server.New()
    // 将内置的 Recovery 中间件注册进入路由
    h.Use(recovery.Recovery())
    // 使用自定义的中间件
    h.Use(exampleMiddleware())
    h.Spin()
}

func exampleMiddleware() app.HandlerFunc {
    return func(ctx context.Context, c *app.RequestContext) {
        // 在 Next 中的函数执行之前打印日志
        hlog.Info("print before...")
        // 使用 Next 使得路由匹配的函数执行
        c.Next(ctx)
    }
}
```
### 流式处理
Hertz 支持 Server 的流式处理，包括流式读和流式写。

注意：由于 netpoll 和 go net 触发模式不同，netpoll 流式为 “伪” 流式（由于 LT 触发，会由网络库将数据读取到网络库的 buffer 中），在大包的场景下（如：上传文件等）可能会有内存问题，推荐使用 go net
#### 流式读
**代码实例**
```go
func main() {
	h := server.Default(server.WithHostPorts("127.0.0.1:8080"), server.WithStreamBody(true), server.WithTransport(standard.NewTransporter))

	h.POST("/bodyStream", handler)

	h.Spin()
}

func handler(ctx context.Context, c *app.RequestContext) {
	// Acquire body streaming
	bodyStream := c.RequestBodyStream()
	// Read half of body bytes
	p := make([]byte, c.Request.Header.ContentLength()/2)
	r, err := bodyStream.Read(p)
	if err != nil {
		panic(err)
	}
	left, _ := ioutil.ReadAll(bodyStream)
	c.String(consts.StatusOK, "bytes streaming_read: %d\nbytes left: %d\n", r, len(left))
}

```
#### 流式写

1. 用户在 handler 中通过 ctx.SetBodyStream 函数传入一个 io.Reader，然后按与示例代码（利用 channel 控制数据分块及读写顺序）类似的方式分块读写数据。注意，数据需异步写入。

若用户事先知道传输数据的总长度，可以在 ctx.SetBodyStream 函数中传入该长度进行流式写，示例代码如 /streamWrite1。

若用户事先不知道传输数据的总长度，可以在 ctx.SetBodyStream 函数中传入 -1 以 Transfer-Encoding: chunked 的方式进行流式写，示例代码如 /streamWrite2。

示例代码：
```go

func main() {
    h := server.Default(server.WithHostPorts("127.0.0.1:8080"), server.WithStreamBody(true), server.WithTransport(standard.NewTransporter))

    h.GET("/streamWrite1", func(c context.Context, ctx *app.RequestContext) {
        rw := newChunkReader()
        line := []byte("line\r\n")
        ctx.SetBodyStream(rw, 500*len(line))

        go func() {
            for i := 1; i <= 500; i++ {
                // For each streaming_write, the upload_file prints
                rw.Write(line)
                fmt.Println(i)
                time.Sleep(10 * time.Millisecond)
            }
            rw.Close()
        }()

        go func() {
            <-ctx.Finished()
            fmt.Println("request process end")
        }()
    })

    h.GET("/streamWrite2", func(c context.Context, ctx *app.RequestContext) {
        rw := newChunkReader()
        // Content-Length may be negative:
        // -1 means Transfer-Encoding: chunked.
        ctx.SetBodyStream(rw, -1)

        go func() {
            for i := 1; i < 1000; i++ {
                // For each streaming_write, the upload_file prints
                rw.Write([]byte(fmt.Sprintf("===%d===\n", i)))
                fmt.Println(i)
                time.Sleep(100 * time.Millisecond)
            }
            rw.Close()
        }()

        go func() {
            <-ctx.Finished()
            fmt.Println("request process end")
        }()
    })

    h.Spin()
}

type ChunkReader struct {
    rw  bytes.Buffer
    w2r chan struct{}
    r2w chan struct{}
}

func newChunkReader() *ChunkReader {
    var rw bytes.Buffer
    w2r := make(chan struct{})
    r2w := make(chan struct{})
    cr := &ChunkReader{rw, w2r, r2w}
    return cr
}

var closeOnce = new(sync.Once)

func (cr *ChunkReader) Read(p []byte) (n int, err error) {
    for {
        _, ok := <-cr.w2r
        if !ok {
            closeOnce.Do(func() {
                close(cr.r2w)
            })
            n, err = cr.rw.Read(p)
            return
        }

        n, err = cr.rw.Read(p)

        cr.r2w <- struct{}{}

        if n == 0 {
            continue
        }
        return
    }
}

func (cr *ChunkReader) Write(p []byte) (n int, err error) {
    n, err = cr.rw.Write(p)
    cr.w2r <- struct{}{}
    <-cr.r2w
    return
}

func (cr *ChunkReader) Close() {
    close(cr.w2r)
}
```


2. 用户可以在 handler 中使用 pkg/protocol/http1/resp/writer 下提供的 NewChunkedBodyWriter 方法劫持 response 的 writer，然后使用 ctx.Write 函数将分块数据写入 Body 并将分块数据使用 ctx.Flush 函数立即发送给客户端。

示例代码：
```go
h.GET("/flush/chunk", func(c context.Context, ctx *app.RequestContext) {
	// Hijack the writer of response
	ctx.Response.HijackWriter(resp.NewChunkedBodyWriter(&ctx.Response, ctx.GetWriter()))

	for i := 0; i < 10; i++ {
        ctx.Write([]byte(fmt.Sprintf("chunk %d: %s", i, strings.Repeat("hi~", i)))) // nolint: errcheck
        ctx.Flush()                                                                 // nolint: errcheck
        time.Sleep(200 * time.Millisecond)
	}
})
```
这两种方式的区别：第一种在执行完 handler 逻辑后再将数据按分块发送给客户端，第二种在 handler 逻辑中就可以将分块数据发送出去。
### Panic 处理函数
用于设置当程序发生 panic 时的处理函数，默认为 nil。
```go
func main() {
    h := server.New()
    // 在 panic 时，会触发 PanicHandler 中的函数，返回 500 状态码并携带错误信息
    h.PanicHandler = func(c context.Context, ctx *app.RequestContext) {
        ctx.JSON(500, utils.H{
            "message": "panic",
        })
    }
    h.GET("/hello", func(c context.Context, ctx *app.RequestContext) {
        panic("panic")
    })
    h.Spin()
}

```
### 路由信息
```go
func (engine *Engine) Routes() (routes RoutesInfo)

```

#### Routes
Routes 函数返回一个按 HTTP 方法划分的包含路由信息（HTTP 方法名，路由路径，请求处理函数名）的切片。

函数签名：
```go

func getHandler() app.HandlerFunc {
	return func(c context.Context, ctx *app.RequestContext) {
		ctx.String(consts.StatusOK, "get handler")
	}
}

func postHandler() app.HandlerFunc {
	return func(c context.Context, ctx *app.RequestContext) {
		ctx.String(consts.StatusOK, "post handler")
	}
}

func main() {
	h := server.Default()
    // 浏览器访问localhost:8080/get
	h.GET("/get", getHandler())
	h.POST("/post", postHandler())
	routesInfo := h.Routes()
	fmt.Printf("%v\n", routesInfo)
    h.Spin()
	// [{GET /get main.getHandler.func1 0xb2afa0} {POST /post main.postHandler.func1 0xb2b060}]
}
```
![Alt text](image.png)

### 底层网络库
```go
func (engine *Engine) GetTransporterName() (tName string)
func SetTransporter(transporter func (options *config.Options) network.Transporter)
```
#### GetTransporterName
获取当前使用的网络库名称，现在有原生的 go net 和 netpoll 两种。

linux 默认使用 netpoll, windows 只能使用 go net。

如果对如何使用对应的网络库有疑惑，请查看 此处。

函数签名:
```go
func (engine *Engine) GetTransporterName() (tName string)
```

示例代码：
```go
h := server.New()
tName := h.GetTransporterName()
```

#### SetTransporter
SetTransporter 用于设置网络库。

注意：SetTransporter 只设置 Engine 的全局默认值，所以在初始化 Engine 时使用 WithTransporter 来设置网络库会覆盖掉 SetTransporter 的设置。

函数签名:
```go
func SetTransporter(transporter func (options *config.Options) network.Transporter)
```

示例代码：
```go
route.SetTransporter(standard.NewTransporter)
```

## 路由

### 路由注册
Hertz 提供了 GET、POST、PUT、DELETE、ANY 等方法用于注册路由。
|方法|	介绍|
|-------------|---------------------|
|Hertz.GET	|用于注册 HTTP Method 为 GET 的方法|
|Hertz.POST|	用于注册 HTTP Method 为 POST 的方法|
|Hertz.DELETE|	用于注册 HTTP Method 为 DELETE 的方法|
|Hertz.PUT|	用于注册 HTTP Method 为 PUT 的方法|
|Hertz.PATCH|	用于注册 HTTP Method 为 PATCH 的方法|
|Hertz.HEAD|	用于注册 HTTP Method 为 HEAD 的方法|
|Hertz.OPTIONS|	用于注册 HTTP Method 为 OPTIONS 的方法|
|Hertz.Handle	|这个方法支持用户手动传入 HTTP Method 用来注册方法，当用于注册普通的 HTTP Method 方法时和上述的方法作用是一致的，并且这个方法同时也支持用于注册自定义 HTTP Method 方法|
|Hertz.Any|	用于注册所有 HTTP Method 方法|
|Hertz.StaticFile/Static/StaticFS|	用于注册静态文件|
**实例代码**：
```go
package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main(){
	h := server.Default(server.WithHostPorts("127.0.0.1:8080"))

	h.StaticFS("/", &app.FS{Root: "./", GenerateIndexPages: true})

	h.GET("/get", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "get")
	})
	h.POST("/post", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "post")
	})
	h.PUT("/put", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "put")
	})
	h.DELETE("/delete", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "delete")
	})
	h.PATCH("/patch", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "patch")
	})
	h.HEAD("/head", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "head")
	})
	h.OPTIONS("/options", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "options")
	})
	h.Any("/ping_any", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "any")
	})
	h.Handle("LOAD","/load", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "load")
	})
	h.Spin()
}

```

### 路由组
Hertz 提供了路由组 ( Group ) 的能力，用于支持路由分组的功能，同时中间件也可以注册到路由组上。

**示例代码:**
```go

package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main(){
	h := server.Default(server.WithHostPorts("127.0.0.1:8080"))
	v1 := h.Group("/v1")
	v1.GET("/get", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "get")
	})
	v1.POST("/post", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "post")
	})
	v2 := h.Group("/v2")
	v2.PUT("/put", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "put")
	})
	v2.DELETE("/delete", func(ctx context.Context, c *app.RequestContext) {
		c.String(consts.StatusOK, "delete")
	})
	h.Spin()
}
```




### 在路由组中使用中间件

如下示例在路由组中使用 BasicAuth 中间件。

示例代码 1:
```go
package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/middlewares/server/basic_auth"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main() {
	h := server.Default(server.WithHostPorts("127.0.0.1:8080"))
	// use middleware
	v1 := h.Group("/v1", basic_auth.BasicAuth(map[string]string{"test": "test"}))

	v1.GET("/ping", func(c context.Context, ctx *app.RequestContext) {
		ctx.String(consts.StatusOK,"ping")
	})
	h.Spin()
}

```

示例代码 2:
```go
package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/middlewares/server/basic_auth"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main() {
	h := server.Default(server.WithHostPorts("127.0.0.1:8080"))
	v1 := h.Group("/v1")
	// use `Use` method
	v1.Use(basic_auth.BasicAuth(map[string]string{"test": "test"}))
	v1.GET("/ping", func(c context.Context, ctx *app.RequestContext) {
		ctx.String(consts.StatusOK,"ping")
	})
	h.Spin()
}
```
### 路由类型
Hertz 支持丰富的路由类型用于实现复杂的功能，包括静态路由、参数路由 (命名参数、通配参数)。

路由的优先级:静态路由 > 命名参数路由 > 通配参数路由


### 命名参数路由
Hertz 支持使用 :name 这样的命名参数设置路由，并且命名参数只匹配单个路径段。

如果我们设置/user/:name路由，匹配情况如下

|路径	|是否匹配|
|----------|------------|
|user/gordon	|匹配|
|/user/you	|匹配|
|/user/gordon/profile|	不匹配|
|/user/|	不匹配|

通过使用 RequestContext.Param 方法，我们可以获取路由中携带的参数。

示例代码:
```go
package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main(){
	h := server.Default(server.WithHostPorts("127.0.0.1:8080"))
	// This handler will match: "/hertz/version", but will not match : "/hertz/" or "/hertz"
	h.GET("/hertz/:version", func(ctx context.Context, c *app.RequestContext) {
		version := c.Param("version")
		c.String(consts.StatusOK, "Hello %s", version)
	})
	h.Spin()
}
```



### 通配参数路由
Hertz 支持使用 *path 这样的通配参数设置路由，并且通配参数会匹配所有内容。

如果我们设置/src/*path路由，匹配情况如下

|路径|	是否匹配|
|-------------|------------------|
|/src/	|匹配|
|/src/somefile.go|	匹配|
|/src/subdir/somefile.go	|匹配|
通过使用 RequestContext.Param 方法，我们可以获取路由中携带的参数。

示例代码:
```go
package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main(){
	h := server.Default(server.WithHostPorts("127.0.0.1:8080"))
	// However, this one will match "/hertz/v1/" and "/hertz/v2/send"
	h.GET("/hertz/:version/*action", func(ctx context.Context, c *app.RequestContext) {
		version := c.Param("version")
		action := c.Param("action")
		message := version + " is " + action
		c.String(consts.StatusOK, message)
	})
	h.Spin()
}

```
在浏览器访问http://localhost:8080/hertz/my/study的结果





### 使用匿名函数与装饰器注册路由
在使用匿名函数或装饰器注册路由时，如果我们使用 RequestContext.HandlerName() 获取 handler 名称则会获取到错误的名称。

这里需要使用 Hertz 提供的 GETEX、POSTEX、PUTEX、DELETEEX、HEADEX、AnyEX、HandleEX 方法并手动传入 handler 名称注册路由，使用 app.GetHandlerName 获取 handler 名称。

示例代码:
```go
package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main() {
	h := server.Default()
	h.AnyEX("/ping", func(c context.Context, ctx *app.RequestContext) {
		ctx.String(consts.StatusOK, app.GetHandlerName(ctx.Handler()))
	}, "ping_handler")
	h.Spin()
}
```

### 获取路由注册信息
Hertz 提供了 Routes 获取注册的路由信息供用户使用。

路由信息结构:
```go
// RouteInfo represents a request route's specification which contains method and path and its handler.
type RouteInfo struct {
    Method      string   // http method
    Path        string   // url path
    Handler     string   // handler name
    HandlerFunc app.HandlerFunc
}

// RoutesInfo defines a RouteInfo array.
type RoutesInfo []RouteInfo
示例代码:

package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/common/hlog"
	"github.com/cloudwego/hertz/pkg/common/utils"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main() {
	h := server.Default()
	h.GET("/ping", func(c context.Context, ctx *app.RequestContext) {
		ctx.JSON(consts.StatusOK, utils.H{"ping": "pong"})
	})
	routeInfo := h.Routes()
	hlog.Info(routeInfo)
	h.Spin()
}
```

### NoRoute 与 NoMethod 使用
Hertz 提供了 NoRoute 与 NoMethod 方法用于全局处理 HTTP 404 与 405 请求。 当使用 NoMethod 时需要与 WithHandleMethodNotAllowed 配合使用。

示例代码：
```go
package main

import (
	"context"
	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/common/utils"
	"github.com/cloudwego/hertz/pkg/protocol/consts"
)

func main() {
	h := server.Default(server.WithHandleMethodNotAllowed(true))
	h.POST("/ping", func(c context.Context, ctx *app.RequestContext) {
		ctx.JSON(consts.StatusOK, utils.H{"ping": "pong"})
	})
	// set NoRoute handler
	h.NoRoute(func(c context.Context, ctx *app.RequestContext) {
		ctx.String(consts.StatusOK, "no route")
	})
	// set NoMethod handler
	h.NoMethod(func(c context.Context, ctx *app.RequestContext) {
		ctx.String(consts.StatusOK, "no method")
	})

	h.Spin()
}
```


### 重定向尾斜杠
Hertz 在默认情况下会根据请求 path 末尾的 / 自动进行转发。如果 router 中只有 /foo/，那么请求 /foo 会被自动重定向到 /foo/；如果 router 中只有 /foo，那么 /foo/ 会被重定向到 /foo。

这样的请求除 GET 以外的请求方法都会触发 307 Temporary Redirect 状态码，而 GET 请求会触发 301 Moved Permanently 状态码。

可以在配置中取消，如下：
```go
package main

import "github.com/cloudwego/hertz/pkg/app/server"

func main() {
    h := server.New(server.WithRedirectTrailingSlash(false))
	...
}
```
## 请求上下文
请求上下文 RequestContext 是用于保存 HTTP 请求和设置 HTTP 响应的上下文，它提供了许多方便的 API 接口帮助用户开发。

Hertz 在 HandlerFunc 设计上，同时提供了一个标准 context.Context 和一个 RequestContext 作为函数的入参。 handler/middleware 函数签名为：
```go
type HandlerFunc func(c context.Context, ctx *RequestContext)
```
context.Context 与 RequestContext 都有存储值的能力，具体选择使用哪一个上下文有个简单依据：所储存值的生命周期和所选择的上下文要匹配。

ctx 主要用来存储请求级别的变量，请求结束就回收了，特点是查询效率高（底层是 map），协程不安全，且未实现 context.Context 接口。

c 作为上下文在中间件 /handler 之间传递，协程安全。所有需要 context.Context 接口作为入参的地方，直接传递 c 即可。

### 请求
#### URI
```go
func (ctx *RequestContext) Host() []byte 
func (ctx *RequestContext) FullPath() string 
func (ctx *RequestContext) SetFullPath(p string)
func (ctx *RequestContext) Path() []byte 
func (ctx *RequestContext) Param(key string) string
func (ctx *RequestContext) Query(key string) string
func (ctx *RequestContext) DefaultQuery(key, defaultValue string) string
func (ctx *RequestContext) GetQuery(key string) (string, bool) 
func (ctx *RequestContext) QueryArgs() *protocol.Args
func (ctx *RequestContext) URI() *protocol.URI 
```

##### Host
获取请求的主机地址。

函数签名:
```go
func (ctx *RequestContext) Host() []byte 
```
示例:
```go
// GET http://example.com
h.GET("/", func(c context.Context, ctx *app.RequestContext) {
    host := ctx.Host() // host == []byte("example.com")
})
```

##### FullPath
获取匹配的路由完整路径，对于未匹配的路由返回空字符串。

函数签名:
```go
func (ctx *RequestContext) FullPath() string 
```

示例:
```go
h := server.Default(server.WithHandleMethodNotAllowed(true))

// GET http://example.com/user/bar
h.GET("/user/:name", func(c context.Context, ctx *app.RequestContext) {
    fpath := ctx.FullPath() // fpath == "/user/:name"
})

// GET http://example.com/bar
h.NoRoute(func(c context.Context, ctx *app.RequestContext) {
    fpath := ctx.FullPath() // fpath == ""
})

// POST http://example.com/user/bar
h.NoMethod(func(c context.Context, ctx *app.RequestContext) {
    fpath := ctx.FullPath() // fpath == ""
})
```

##### SetFullPath
设置 FullPath 的值。

注意：FullPath 由路由查找时分配，通常你不需要使用 SetFullPath 去覆盖它。

函数签名:
```go
func (ctx *RequestContext) SetFullPath(p string)
```

示例:
```go
h.GET("/user/:name", func(c context.Context, ctx *app.RequestContext) {
    ctx.SetFullPath("/v1/user/:name")
    fpath := ctx.FullPath() // fpath == "/v1/user/:name"
})
```

##### Path
获取请求的路径。

注意：出现参数路由时 Path 给出命名参数匹配后的路径，而 FullPath 给出原始路径。

函数签名:
```go
func (ctx *RequestContext) Path() []byte 
```

示例:
```go
// GET http://example.com/user/bar
h.GET("/user/:name", func(c context.Context, ctx *app.RequestContext) {
    path := ctx.Path() // path == []byte("/user/bar")
})
```

##### Param
获取路由参数的值。

函数签名:
```go
func (ctx *RequestContext) Param(key string) string 
```

示例:
```go
// GET http://example.com/user/bar
h.GET("/user/:name", func(c context.Context, ctx *app.RequestContext) {
    name := ctx.Param("name") // name == "bar"
    id := ctx.Param("id") // id == ""
})
```

##### Query
获取路由 Query String 参数中指定属性的值，如果没有返回空字符串。

函数签名:
```go
func (ctx *RequestContext) Query(key string) string
```

示例:
```go
// GET http://example.com/user?name=bar
h.GET("/user", func(c context.Context, ctx *app.RequestContext) {
    name := ctx.Query("name") // name == "bar"
    id := ctx.Query("id") // id == ""
})
```

##### DefaultQuery
获取路由 Query String 参数中指定属性的值，如果没有返回设置的默认值。

函数签名:
```go
func (ctx *RequestContext) DefaultQuery(key, defaultValue string) string

```

示例:
```go
// GET http://example.com/user?name=bar&&age=
h.GET("/user", func(c context.Context, ctx *app.RequestContext) {
    name := ctx.DefaultQuery("name", "tom") // name == "bar"
    id := ctx.DefaultQuery("id", "123") // id == "123"
    age := ctx.DefaultQuery("age", "45") // age == ""
})

```

##### GetQuery
获取路由 Query String 参数中指定属性的值以及属性是否存在。

函数签名:
```go
func (ctx *RequestContext) GetQuery(key string) (string, bool)
```

示例:
```go
// GET http://example.com/user?name=bar&&age=
h.GET("/user", func(c context.Context, ctx *app.RequestContext) {
    name, hasName := ctx.GetQuery("name") // name == "bar", hasName == true
    id, hasId := ctx.GetQuery("id") // id == "", hasId == false
    age, hasAge := ctx.GetQuery("age") // age == "", hasAge == true
})
```

##### QueryArgs
获取路由 Query String 参数对象。

函数签名:
```go
func (ctx *RequestContext) QueryArgs() *protocol.Args
```

##### Args 对象
Args 对象提供了以下方法获取/设置 Query String 参数。

|函数签名	|说明|
|--------------|------------------|
|func (a *Args) Set(key, value string)	|设置 Args 对象 key 的值|
|func (a *Args) Reset()	|重置 Args 对象|
|func (a *Args) CopyTo(dst *Args)	|将 Args 对象拷贝到 dst|
|func (a *Args) Del(key string)|	删除 Args 对象 key 的键值对|
|func (a *Args) DelBytes(key []byte)|	删除 Args 对象字节数组类型 key 的键值对|
|func (a *Args) Has(key string) bool|	获取 Args 对象是否存在 key 的键值对|
|func (a *Args) String() string|	将 Args 对象转换为字符串类型的 Query String|
|func (a *Args) QueryString() []byte	|将 Args 对象转换为字节数组类型的 Query String|
|func (a *Args) ParseBytes(b []byte)	|解析字节数组并将键值对存入 Args 对象|
|func (a *Args) Peek(key string) []byte	|获取 Args 对象 key 的值|
|func (a *Args) PeekExists(key string) (string, bool)	|获取 Args 对象 key 的值以及是否存在|
|func (a *Args) Len() int	|获取 Args 对象键值对数量|
|func (a *Args) AppendBytes(dst []byte) []byte|	将 Args 对象 Query String 附加到 dst 中并返回|
|func (a *Args) VisitAll(f func(key, value []byte))|	遍历 Args 对象所有的键值对|
|func (a *Args) WriteTo(w io.Writer) (int64, error)	|将 Args 对象 Query String 写入 io.Writer 中|
|func (a *Args) Add(key, value string)	|添加 Args 对象键为 key 的值|
示例：
```go
// GET http://example.com/user?name=bar&&age=&&pets=dog&&pets=cat
h.GET("/user", func(c context.Context, ctx *app.RequestContext) {
    args := ctx.QueryArgs()

    // get information from args
    s := args.String()                    // s == "name=bar&age=&pets=dog&pets=cat"
    qs := args.QueryString()              // qs == []byte("name=bar&age=&pets=dog&pets=cat")
    cpqs := args.AppendBytes([]byte(nil)) // cpqs == []byte("name=bar&age=&pets=dog&pets=cat")
    name := args.Peek("name")             // name == []byte("bar")
    hasName := args.Has("name")           // hasName == true
    age, hasAge := args.PeekExists("age") // age == "", hasAge == true
    len := args.Len()                     // len == 4

    args.VisitAll(func(key, value []byte) {
        // 1. key == []byte("name"), value == []byte("bar")
        // 2. key == []byte("age"), value == nil
        // 3. key == []byte("pets"), value == []byte("dog")
        // 4. key == []byte("pets"), value == []byte("cat")
    })

    // send information to io.Writer
    req := protocol.AcquireRequest()
	n, err := args.WriteTo(req.BodyWriter())
    // n == 31 err == nil
	s := req.BodyBuffer().String()
    // s == "name=bar&age=&pets=dog&pets=cat"
	
    // change args
    var newArgs protocol.Args
    args.CopyTo(&newArgs)

    newArgs.Set("version", "v1")
    version := newArgs.Peek("version") //version == []byte("v1")

    newArgs.Del("age")
    hasAgeAfterDel := newArgs.Has("age") // hasAgeAfterDel == false

    newArgs.DelBytes([]byte("name"))
    hasNameAfterDel := newArgs.Has("name") // hasNameAfterDel == false

    newArgs.Add("name", "foo")
    newName := newArgs.Peek("name") //newName == []byte("foo")

    newArgs.Reset()
    empty := newArgs.String() // empty == ""

    // parse args
    var newArgs2 protocol.Args
    newArgs2.ParseBytes([]byte("name=bar&age=20"))
    nqs2 := newArgs2.String() // nqs2 == "name=bar&age=20"
})
```

##### URI
返回请求的 URI 对象。

函数签名:
```go
func (ctx *RequestContext) URI() *protocol.URI 
```

URI 对象提供了以下方法获取/设置 URI。

|函数签名	|说明|
|-------------------|----------------|
|func (u *URI) CopyTo(dst *URI)	|拷贝 URI 对象的副本到 dst|
|func (u *URI) QueryArgs() | *Args	获取 Args 对象|
|func (u *URI) Hash() []byte	|获取 Hash 值，比如 http://example.com/user?baz=123#qwe 的 Hash 是 qwe|
|func (u *URI) SetHash(hash string)	|设置 Hash|
|func (u *URI) SetHashBytes(hash []byte)	|设置 []byte 类型 Hash|
|func (u *URI) Username() []byte	|获取 Username|
|func (u *URI) SetUsername(username string)	|设置 Username|
|func (u *URI) SetUsernameBytes(username []byte)	|设置 []byte 类型 Username|
|func (u *URI) Password() []byte	|获取 Password|
|func (u *URI) SetPassword(password string)|	设置 Password|
|func (u *URI) SetPasswordBytes(password []byte)	|设置 []byte 类型 Password|
|func (u *URI) QueryString() []byte	|获取 Query String，比如 http://example.com/user?baz=123 的 Query String 是 baz=123|
|func (u *URI) SetQueryString(queryString string)	|设置 Query String|
|func (u *URI) SetQueryStringBytes(queryString []byte)	|设置 []byte 类型的 Query String|
|func (u *URI) Path() []byte	|获取 Path，比如 http://example.com/user/he%20rtz 的 Path 是 /user/he rtz|
|func (u *URI) PathOriginal() []byte	|获取未转义的 Path，比如 http://example.com/user/he%20rtz 的 Path 是 /user/he%20rtz|
|func (u *URI) SetPath(path string)	|设置 Path|
|func (u *URI) SetPathBytes(path []byte)	|设置 []byte 类型 Path|
|func (u *URI) String() string	|获取完整 URI 比如 http://example.com/user?baz=123 的完整 URI 是 http://example.com/user?baz=123|
|func (u *URI) FullURI() []byte	|获取 []byte 类型的完整 URI|
|func (u *URI) Scheme() []byte	|获取协议，如 http|
|func (u *URI) SetScheme(scheme string)	|设置协议|
|func (u *URI) SetSchemeBytes(scheme []byte)	|设置 []byte 类型的协议|
|func (u *URI) Host() []byte	|获取 Host，比如 http://example.com/user 的 Host 是 example.com|
|func (u *URI) SetHost(host string)	|设置 Host|
|func (u *URI) SetHostBytes(host []byte)	|设置 []byte 类型 Host|
|func (u *URI) LastPathSegment() []byte	|获取 Path 的最后一部分，比如 Path /foo/bar/baz.html 的最后一部分是 baz.html|
|func (u *URI) Update(newURI string)	|更新 URI|
|func (u *URI) UpdateBytes(newURI []byte)	|更新 []byte 类型的 URI|
|func (u *URI) Parse(host, uri []byte)	|初始化 URI|
|func (u *URI) AppendBytes(dst []byte) []byte	|将完整的 URI 赋值到 dst 中并返回 dst|
|func (u *URI) RequestURI() []byte	|获取 RequestURI，比如 http://example.com/user?baz=123 的 RequestURI 是 /user?baz=123|
|func (u *URI) Reset()|	重置 URI|

#### Header 
```go
// RequestHeader
func (h *RequestHeader) Add(key, value string)
func (h *RequestHeader) Set(key, value string)
func (h *RequestHeader) Header() []byte
func (h *RequestHeader) String() string
func (h *RequestHeader) VisitAll(f func(key, value []byte))

// RequestContext
func (ctx *RequestContext) IsGet() bool 
func (ctx *RequestContext) IsHead() bool
func (ctx *RequestContext) IsPost() bool
func (ctx *RequestContext) Method() []byte
func (ctx *RequestContext) ContentType() []byte
func (ctx *RequestContext) IfModifiedSince(lastModified time.Time) bool 
func (ctx *RequestContext) Cookie(key string) []byte
func (ctx *RequestContext) UserAgent() []byte
func (ctx *RequestContext) GetHeader(key string) []byte
```
##### Add
添加或设置键为 key 的 Header。

注意：Add 通常用于为同一个 Key 设置多个 Header，若要为同一个 Key 设置单个 Header 请使用 Set。当作用于 Content-Type, Content-Length, Connection, Cookie, Transfer-Encoding, Host, User-Agent 这些 Header 时，使用多个 Add 会覆盖掉旧值。

函数签名：
```go
func (h *RequestHeader) Add(key, value string)
```

示例：
```go
hertz.GET("/example", func(c context.Context, ctx *app.RequestContext) {
	ctx.Request.Header.Add("hertz1", "value1")
	ctx.Request.Header.Add("hertz1", "value2")
	ctx.Request.Header.SetContentTypeBytes([]byte("application/x-www-form-urlencoded"))
	contentType1 := ctx.Request.Header.ContentType() 
    // contentType1 == []byte("application/x-www-form-urlencoded")
	ctx.Request.Header.Add("Content-Type", "application/json; charset=utf-8")
	hertz1 := ctx.Request.Header.GetAll("hertz1") 
    // hertz1 == []string{"value1", "value2"}
	contentType2 := ctx.Request.Header.ContentType() 
    // contentType2 == []byte("application/json; charset=utf-8")
	})
```

##### Set
设置 Header 键值。

注意：Set 通常用于为同一个 Key 设置单个 Header，若要为同一个 Key 设置多个 Header 请使用 Add。

函数签名：
```go
func (h *RequestHeader) Set(key, value string)
```

示例：
```go
hertz.GET("/example", func(c context.Context, ctx *app.RequestContext) {
	ctx.Request.Header.Set("hertz1", "value1")
	ctx.Request.Header.Set("hertz1", "value2")
	ctx.Request.Header.SetContentTypeBytes([]byte("application/x-www-form-urlencoded"))
	contentType1 := ctx.Request.Header.ContentType() 
    // contentType1 == []byte("application/x-www-form-urlencoded")
	ctx.Request.Header.Set("Content-Type", "application/json; charset=utf-8")
	hertz1 := ctx.Request.Header.GetAll("hertz1")    
    // hertz1 == []string{"value2"}
	contentType2 := ctx.Request.Header.ContentType() 
    // contentType2 == []byte("application/json; charset=utf-8")
	})
```

##### Header
获取 []byte 类型的完整的 Header。

函数签名：
```go
func (h *RequestHeader) Header() []byte
```

示例：
```go
 hertz.GET("/example", func(c context.Context, ctx *app.RequestContext) {
	ctx.Request.Header.Set("hertz1", "value1")
	ctx.Request.Header.Set("hertz1", "value2")
	ctx.Request.Header.SetContentTypeBytes([]byte("application/x-www-form-urlencoded"))
	contentType1 := ctx.Request.Header.ContentType() 
    // contentType1 == []byte("application/x-www-form-urlencoded")
	ctx.Request.Header.Set("Content-Type", "application/json; charset=utf-8")
	hertz1 := ctx.Request.Header.GetAll("hertz1")    
    // hertz1 == []string{"value2"}
	contentType2 := ctx.Request.Header.ContentType() 
    // contentType2 == []byte("application/json; charset=utf-8")
	})
```

##### String
获取完整的 Header。

函数签名：
```go
func (h *RequestHeader) String() string
```

示例：
```go
hertz.GET("/example", func(c context.Context, ctx *app.RequestContext) {
		ctx.Request.Header.Set("hertz1", "value1")
		header := ctx.Request.Header.String()
		// header == "GET /example HTTP/1.1
		//User-Agent: PostmanRuntime-ApipostRuntime/1.1.0
		//Host: localhost:8888
		//Cache-Control: no-cache
		//Accept: */*
		//Accept-Encoding: gzip, deflate, br
		//Connection: keep-alive
		//Hertz1: value1"
	})
```

##### 遍历 Header
遍历所有 Header 的键值并执行 f 函数。

函数签名：
```go
func (h *RequestHeader) VisitAll(f func(key, value []byte))
```

示例：
```go
hertz.GET("/example", func(c context.Context, ctx *app.RequestContext) {
	ctx.Request.Header.Add("Hertz1", "value1")
	ctx.Request.Header.Add("Hertz1", "value2")

	var hertzString []string
	ctx.Request.Header.VisitAll(func(key, value []byte) {
		if string(key) == "Hertz1" {
			hertzString = append(hertzString, string(value))
		}
	})
	// hertzString == []string{"value1", "value2"}
	})
```

##### ethod
获取请求方法的类型。

函数签名:
```go
func (ctx *RequestContext) Method() []byte
```

示例:
```go
// POST http://example.com/user
h.Any("/user", func(c context.Context, ctx *app.RequestContext) {
    method := ctx.Method() // method == []byte("POST")
})

```

##### ContentType
获取请求头 Content-Type 的值。

函数签名:
```go
func (ctx *RequestContext) ContentType() []byte
```

示例:
```go

// POST http://example.com/user
// Content-Type: application/json
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    contentType := ctx.ContentType() // contentType == []byte("application/json")
})
```

##### IfModifiedSince
判断时间是否超过请求头 If-Modified-Since 的值。

注意：如果请求头不包含 If-Modified-Since 也返回 true。

函数签名:
```go
func (ctx *RequestContext) IfModifiedSince(lastModified time.Time) bool
```

示例:
```go
// POST http://example.com/user
// If-Modified-Since: Wed, 21 Oct 2023 07:28:00 GMT
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    t2022, _ := time.Parse(time.RFC1123, "Wed, 21 Oct 2022 07:28:00 GMT")
    ifModifiedSince := ctx.IfModifiedSince(t2022) // ifModifiedSince == false

    t2024, _ := time.Parse(time.RFC1123, "Wed, 21 Oct 2024 07:28:00 GMT")
    ifModifiedSince = ctx.IfModifiedSince(t2024) // ifModifiedSince == true
})
```

##### Cookie
获取请求头 Cookie 中 key 的值。

函数签名:
```go
func (ctx *RequestContext) Cookie(key string) []byte
```

示例:
```go

// POST http://example.com/user
// Cookie: foo_cookie=choco; bar_cookie=strawberry
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    fCookie := ctx.Cookie("foo_cookie")     // fCookie == []byte("choco")
    bCookie := ctx.Cookie("bar_cookie")     // bCookie == []byte("strawberry")
    noneCookie := ctx.Cookie("none_cookie") // noneCookie == nil
})
```

##### UserAgent
获取请求头 User-Agent 的值。

函数签名:
```go
func (ctx *RequestContext) UserAgent() []byte
```

示例:
```go
// POST http://example.com/user
// User-Agent: Chrome/51.0.2704.103 Safari/537.36
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    ua := ctx.UserAgent() // ua == []byte("Chrome/51.0.2704.103 Safari/537.36")
})
```

##### GetHeader
获取请求头中 key 的值。

函数签名:
```go
func (ctx *RequestContext) GetHeader(key string) []byte
```

示例:
```go
// POST http://example.com/user
// Say-Hello: hello
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    customHeader := ctx.GetHeader("Say-Hello") // customHeader == []byte("hello")
})
```
#### Body
```go
func (ctx *RequestContext) GetRawData() []byte
func (ctx *RequestContext) Body() ([]byte, error) 
func (ctx *RequestContext) RequestBodyStream() io.Reader
func (ctx *RequestContext) MultipartForm() (*multipart.Form, error)
func (ctx *RequestContext) PostForm(key string) string
func (ctx *RequestContext) DefaultPostForm(key, defaultValue string) string 
func (ctx *RequestContext) GetPostForm(key string) (string, bool) 
func (ctx *RequestContext) PostArgs() *protocol.Args
func (ctx *RequestContext) FormValue(key string) []byte 
func (ctx *RequestContext) SetFormValueFunc(f FormValueFunc)
```
  
#### Body
获取请求的 body 数据，如果发生错误返回 error。

函数签名:
```go
func (ctx *RequestContext) Body() ([]byte, error) 
```

示例:
```go
// POST http://example.com/pet
// Content-Type: application/json
// {"pet":"cat"}
h.Post("/pet", func(c context.Context, ctx *app.RequestContext) {
    data, err := ctx.Body() // data == []byte("{\"pet\":\"cat\"}") , err == nil
})

```

##### RequestBodyStream
获取请求的 BodyStream。

函数签名:
```go
func (ctx *RequestContext) RequestBodyStream() io.Reader
```

示例:
```go

// POST http://example.com/user
// Content-Type: text/plain
// abcdefg
h := server.Default(server.WithStreamBody(true))
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    sr := ctx.RequestBodyStream()
    data, _ := io.ReadAll(sr) // data == []byte("abcdefg")
})
```

##### MultipartForm
获取 multipart.Form 对象，(详情请参考 multipart#Form)

注意：此函数既可以获取普通值也可以获取文件，此处给出了获取普通值的示例代码，获取文件的示例代码可参考 MultipartForm。

函数签名:
```go
func (ctx *RequestContext) MultipartForm() (*multipart.Form, error)
```

示例:
```go
// POST http://example.com/user
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="name"
// tom
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    form, err := ctx.MultipartForm()
    name := form.Value["name"][0] // name == "tom"
})
```

##### PostForm
按名称检索 multipart.Form.Value，返回给定 name 的第一个值。

注意：该函数支持从 application/x-www-form-urlencoded 和 multipart/form-data 这两种类型的 content-type 中获取 value 值，且不支持获取文件值。

函数签名:
```go
func (ctx *RequestContext) PostForm(key string) string

```

示例:
```go
// POST http://example.com/user
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="name"
// tom
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    name := ctx.PostForm("name") // name == "tom"
})
```

##### DefaultPostForm
按名称检索 multipart.Form.Value，返回给定 name 的第一个值，如果不存在返回 defaultValue。

注意：该函数支持从 application/x-www-form-urlencoded 和 multipart/form-data 这两种类型的 content-type 中获取 value 值，且不支持获取文件值。

函数签名:
```go
func (ctx *RequestContext) DefaultPostForm(key, defaultValue string) string 
```

示例:
```go
// POST http://example.com/user
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="name"
// tom
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    name := ctx.PostForm("name", "jack") // name == "tom"
    age := ctx.PostForm("age", "10") // age == "10"
})
```

##### PostArgs
获取 application/x-www-form-urlencoded 参数对象。(详情请参考 Args 对象)

函数签名:
```go
func (ctx *RequestContext) PostArgs() *protocol.Args
```

示例:
```go
// POST http://example.com/user
// Content-Type: application/x-www-form-urlencoded
// name=tom&pet=cat&pet=dog
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    args := ctx.PostArgs()
    name := args.Peek("name") // name == "tom"

    var pets []string
    args.VisitAll(func(key, value []byte) {
        if string(key) == "pet" {
        pets = append(pets, string(value))
        }
    })
    // pets == []string{"cat", "dog"}
})

```

###### FormValue
按照以下顺序获取 key 的值。

从 QueryArgs 中获取值。
从 PostArgs 中获取值。
从 MultipartForm 中获取值。
函数签名:
```go
func (ctx *RequestContext) FormValue(key string) []byte 
```

示例:
```go
// POST http://example.com/user?name=tom
// Content-Type: application/x-www-form-urlencoded
// age=10
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    name := ctx.FormValue("name") // name == []byte("tom"), get by QueryArgs
    age := ctx.FormValue("age") // age == []byte("10"), get by PostArgs
})

// POST http://example.com/user
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="name"
// tom
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    name := ctx.FormValue("name") // name == []byte("tom"), get by MultipartForm
})
```

##### SetFormValueFunc
若 FormValue 函数提供的默认获取 key 的值的方式不满足需求，用户可以使用该函数自定义获取 key 的值的方式。

函数签名:
```go

func (ctx *RequestContext) SetFormValueFunc(f FormValueFunc) 
```

示例:
```go
// POST http://example.com/user?name=tom
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="age"
// 10
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    // only return multipart form value
    ctx.SetFormValueFunc(func(rc *app.RequestContext, s string) []byte {
        mf, err := rc.MultipartForm()
        if err == nil && mf.Value != nil {
            vv := mf.Value[s]
            if len(vv) > 0 {
                return []byte(vv[0])
            }
        }
        return nil
    })

    name := ctx.FormValue("name") // name == nil
    age := ctx.FormValue("age")   // age == []byte("10")
})
```

#### 文件操作
```go
func (ctx *RequestContext) MultipartForm() (*multipart.Form, error)
func (ctx *RequestContext) FormFile(name string) (*multipart.FileHeader, error) 
func (ctx *RequestContext) SaveUploadedFile(file *multipart.FileHeader, dst string) error 
```

##### MultipartForm
获取 multipart.Form 对象。(详情请参考 multipart#Form)

注意：此函数既可以获取普通值也可以获取文件，此处给出了获取文件值的示例代码，获取普通值的示例代码可参考 MultipartForm。

函数签名:
```go
func (ctx *RequestContext) MultipartForm() (*multipart.Form, error)
```

示例:
```go
// POST http://example.com/user
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="avatar"; filename="abc.jpg"
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    form, err := ctx.MultipartForm()
    avatarFile := form.File["avatar"][0] // avatarFile.Filename == "abc.jpg"
})

```

##### FormFile
按名称检索 multipart.Form.File，返回给定 name 的第一个 multipart.FileHeader。(详情请参考 multipart#FileHeader)

函数签名:
```go
func (ctx *RequestContext) FormFile(name string) (*multipart.FileHeader, error)
```
 
示例:
```go
// POST http://example.com/user
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="avatar"; filename="abc.jpg"
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    avatarFile, err := ctx.FormFile("avatar") // avatarFile.Filename == "abc.jpg", err == nil
})

```

##### SaveUploadedFile
保存 multipart 文件到磁盘。

函数签名:
```go
func (ctx *RequestContext) SaveUploadedFile(file *multipart.FileHeader, dst string) error 
```

示例:
```go
// POST http://example.com/user
// Content-Type: multipart/form-data; 
// Content-Disposition: form-data; name="avatar"; filename="abc.jpg"
h.Post("/user", func(c context.Context, ctx *app.RequestContext) {
    avatarFile, err := ctx.FormFile("avatar") // avatarFile.Filename == "abc.jpg", err == nil
    // save file
    ctx.SaveUploadedFile(avatarFile, avatarFile.Filename) // save file "abc.jpg"
})
```

#### Handler
```go
func (ctx *RequestContext) Next(c context.Context) 
func (ctx *RequestContext) Handlers() HandlersChain 
func (ctx *RequestContext) Handler() HandlerFunc 
func (ctx *RequestContext) SetHandlers(hc HandlersChain) 
func (ctx *RequestContext) HandlerName() string 
func (ctx *RequestContext) GetIndex() int8 
func (ctx *RequestContext) Abort() 
func (ctx *RequestContext) IsAborted() bool

```

##### Next
执行下一个 handler，该函数通常用于中间件 handler 中。

函数签名:
```go
func (ctx *RequestContext) Next(c context.Context)
```

示例:
```go

h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    ctx.Next(c)
    v := ctx.GetString("version") // v == "v1"
}, func(c context.Context, ctx *app.RequestContext) {
    ctx.Set("version", "v1")
})
```

##### Handlers
获取 handlers chain。

函数签名:
```go
func (ctx *RequestContext) Handlers() HandlersChain

```

示例:
```go
middleware1 := func(c context.Context, ctx *app.RequestContext) {
}

handler1 := func(c context.Context, ctx *app.RequestContext) {
    handlers := ctx.Handlers() // []Handler{middleware1, handler1}
}

h.POST("/user", middleware1, handler1)
```

##### Handler
获取 handlers chain 的最后一个 handler，一般来说，最后一个 handler 是 main handler。

函数签名:
```go
func (ctx *RequestContext) Handler() HandlerFunc
```

示例:
```go
middleware1 := func(c context.Context, ctx *app.RequestContext) {
    lastHandler := ctx.Handler() // lastHandler == handler1
}

handler1 := func(c context.Context, ctx *app.RequestContext) {
}

h.POST("/user", middleware1, handler1)

```

##### SetHandlers
设置 handlers chain。

函数签名:
```go
func (ctx *RequestContext) SetHandlers(hc HandlersChain)
```

示例:
```go
handler1 := func(c context.Context, ctx *app.RequestContext) {
    ctx.Set("current", "handler1")
}

handler := func(c context.Context, ctx *app.RequestContext) {
    hc := app.HandlersChain{ctx.Handlers()[0], handler1} // append handler1 into handlers chain
    ctx.SetHandlers(hc)
    ctx.Next(c)
    current := ctx.GetString("current") // current == "handler1"
    ctx.String(consts.StatusOK, current)
}

h.POST("/user", handler)
```

##### HandlerName
获取最后一个 handler 的函数名称。

函数签名:
```go
func (ctx *RequestContext) HandlerName() string
```

示例:
```go
package main

func main() {
    h := server.New()
    h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
        hn := ctx.HandlerName() // hn == "main.main.func1"
    })
}
```

##### GetIndex
获取当前执行的 handler 在 handlers chain 中的 index。

函数签名:
```go
func (ctx *RequestContext) GetIndex() int8
```

示例:
```go

h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    index := ctx.GetIndex() // index == 0
}, func(c context.Context, ctx *app.RequestContext) {
    index := ctx.GetIndex() // index == 1
})
```

##### Abort
终止后续的 handler 执行。

函数签名:
```go
func (ctx *RequestContext) Abort()
```

示例:
```go
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    ctx.Abort()
}, func(c context.Context, ctx *app.RequestContext) {
    // will not execute
})
```

##### IsAborted
获取后续的 handler 执行状态是否被终止。

函数签名:
```go
func (ctx *RequestContext) IsAborted() bool
```

示例:
```go
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    ctx.Abort()
    isAborted := ctx.IsAborted() // isAborted == true
}, func(c context.Context, ctx *app.RequestContext) {
    // will not execute
})
```

#### 参数绑定与校验
```go
func (ctx *RequestContext) Bind(obj interface{}) error 
func (ctx *RequestContext) Validate(obj interface{}) error 
func (ctx *RequestContext) BindAndValidate(obj interface{}) error
```


#### 获取 ClientIP
```go
func (ctx *RequestContext) ClientIP() string 
func (ctx *RequestContext) SetClientIPFunc(f ClientIP) 
```

##### ClientIP
获取客户端 IP 的地址。

该函数的默认行为：若 X-Forwarded-For 或 X-Real-IP Header 中存在 ip，则从这两个 Header 中读 ip 并返回（优先级 X-Forwarded-For 大于 X-Real-IP），否则返回 remote address。

函数签名:
```go
func (ctx *RequestContext) ClientIP() string 
```

示例:
```go
// X-Forwarded-For: 20.20.20.20, 30.30.30.30
// X-Real-IP: 10.10.10.10
h.Use(func(c context.Context, ctx *app.RequestContext) {
    ip := ctx.ClientIP() // 20.20.20.20
})
```

##### SetClientIPFunc
若 ClientIP 函数提供的默认方式不满足需求，用户可以使用该函数自定义获取客户端 ip 的方式。

用户可以自己实现自定义函数，也可以通过设置 app.ClientIPOptions 实现。

注意：在设置 app.ClientIPOptions 时，TrustedCIDRs 需用户自定义（若不设置则固定返回 remote address），代表可信任的路由。若 remote address 位于可信任的路由范围内，则会选择从 RemoteIPHeaders 中获取 ip，否则返回 remote address。

函数签名:
```go
func (ctx *RequestContext) SetClientIPFunc(f ClientIP) 
```

示例:
```go

// POST http://example.com/user
// X-Forwarded-For: 30.30.30.30
h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    // method 1
    customClientIPFunc := func(ctx *app.RequestContext) string {
			return "127.0.0.1"
	}
	ctx.SetClientIPFunc(customClientIPFunc)
	ip := ctx.ClientIP() // ip == "127.0.0.1"

    // method 2
    _, cidr, _ := net.ParseCIDR("127.0.0.1/32")
	opts := app.ClientIPOptions{
		RemoteIPHeaders: []string{"X-Forwarded-For", "X-Real-IP"},
		TrustedCIDRs:    []*net.IPNet{cidr},
	}
	ctx.SetClientIPFunc(app.ClientIPWithOption(opts))

	ip = ctx.ClientIP() // ip == "30.30.30.30"
})
```

##### 并发安全
```go
func (ctx *RequestContext) Copy() *RequestContext
```

Copy
拷贝 RequestContext 副本，提供协程安全的访问方式。

函数签名:
```go
func (ctx *RequestContext) Copy() *RequestContext 
示例:

h.POST("/user", func(c context.Context, ctx *app.RequestContext) {
    ctx1 := ctx.Copy()
    go func(context *app.RequestContext) {
        // safely
    }(ctx1)
})
```

##### RequestHeader 对象
使用 RequestContext.Request.Header 获取 RequestHeader 对象，该对象提供了以下方法获取/设置请求头部。

# 各种中间件
## 跨源资源共享

```go
package main

import (
    "time"

    "github.com/cloudwego/hertz/pkg/app/server"
    "github.com/hertz-contrib/cors"
)

func main() {
    h := server.Default()
    // CORS for https://foo.com and https://github.com origins, allowing:
    // - PUT and PATCH methods
    // - Origin header
    // - Credentials share
    // - Preflight requests cached for 12 hours
    h.Use(cors.New(cors.Config{
        AllowOrigins:     []string{"https://foo.com"},
        AllowMethods:     []string{"PUT", "PATCH"},
        AllowHeaders:     []string{"Origin"},
        ExposeHeaders:    []string{"Content-Length"},
        AllowCredentials: true,
        AllowOriginFunc: func(origin string) bool {
            return origin == "https://github.com"
        },
        MaxAge: 12 * time.Hour,
    }))
    h.Spin()
}
```
## JWT 认证
```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/cloudwego/hertz/pkg/app"
    "github.com/cloudwego/hertz/pkg/app/server"
    "github.com/cloudwego/hertz/pkg/common/utils"
    "github.com/hertz-contrib/jwt"
)

type login struct {
    Username string `form:"username,required" json:"username,required"`
    Password string `form:"password,required" json:"password,required"`
}

var identityKey = "id"

func PingHandler(c context.Context, ctx *app.RequestContext) {
    user, _ := ctx.Get(identityKey)
    ctx.JSON(200, utils.H{
        "message": fmt.Sprintf("username:%v", user.(*User).UserName),
    })
}

// User demo
type User struct {
    UserName  string
    FirstName string
    LastName  string
}

func main() {
    h := server.Default()

    // the jwt middleware
    authMiddleware, err := jwt.New(&jwt.HertzJWTMiddleware{
        Realm:       "test zone",
        Key:         []byte("secret key"),
        Timeout:     time.Hour,
        MaxRefresh:  time.Hour,
        IdentityKey: identityKey,
        PayloadFunc: func(data interface{}) jwt.MapClaims {
            if v, ok := data.(*User); ok {
                return jwt.MapClaims{
                    identityKey: v.UserName,
                }
            }
            return jwt.MapClaims{}
        },
        IdentityHandler: func(ctx context.Context, c *app.RequestContext) interface{} {
            claims := jwt.ExtractClaims(ctx, c)
            return &User{
                UserName: claims[identityKey].(string),
            }
        },
        Authenticator: func(ctx context.Context, c *app.RequestContext) (interface{}, error) {
            var loginVals login
            if err := c.BindAndValidate(&loginVals); err != nil {
                return "", jwt.ErrMissingLoginValues
            }
            userID := loginVals.Username
            password := loginVals.Password

            if (userID == "admin" && password == "admin") || (userID == "test" && password == "test") {
                return &User{
                    UserName:  userID,
                    LastName:  "Hertz",
                    FirstName: "CloudWeGo",
                }, nil
            }

            return nil, jwt.ErrFailedAuthentication
        },
        Authorizator: func(data interface{}, ctx context.Context, c *app.RequestContext) bool {
            if v, ok := data.(*User); ok && v.UserName == "admin" {
                return true
            }

            return false
        },
        Unauthorized: func(ctx context.Context, c *app.RequestContext, code int, message string) {
            c.JSON(code, map[string]interface{}{
                "code":    code,
                "message": message,
            })
        },
    })
    if err != nil {
        log.Fatal("JWT Error:" + err.Error())
    }

    // When you use jwt.New(), the function is already automatically called for checking,
    // which means you don't need to call it again.
    errInit := authMiddleware.MiddlewareInit()

    if errInit != nil {
        log.Fatal("authMiddleware.MiddlewareInit() Error:" + errInit.Error())
    }

    h.POST("/login", authMiddleware.LoginHandler)

    h.NoRoute(authMiddleware.MiddlewareFunc(), func(ctx context.Context, c *app.RequestContext) {
        claims := jwt.ExtractClaims(ctx, c)
        log.Printf("NoRoute claims: %#v\n", claims)
        c.JSON(404, map[string]string{"code": "PAGE_NOT_FOUND", "message": "Page not found"})
    })

    auth := h.Group("/auth")
    // Refresh time can be longer than token timeout
    auth.GET("/refresh_token", authMiddleware.RefreshHandler)
    auth.Use(authMiddleware.MiddlewareFunc())
    {
        auth.GET("/ping", PingHandler)
    }

    h.Spin()
}
```
|参数|	介绍|
|---------|-------------|
|Realm|	用于设置所属领域名称，默认为 hertz jwt|
|SigningAlgorithm|	用于设置签名算法，可以是 HS256、HS384、HS512、RS256、RS384 或者 RS512 等，默认为 HS256|
|Key	|用于设置签名密钥（必要配置）|
|KeyFunc	|用于设置获取签名密钥的回调函数，设置后 token 解析时将从 KeyFunc 获取 jwt 签名密钥|
|Timeout	|用于设置 token 过期时间，默认为一小时|
|MaxRefresh	|用于设置最大 token 刷新时间，允许客户端在 TokenTime + MaxRefresh 内刷新 token 的有效时间，追加一个 Timeout 的时长|
|Authenticator	|用于设置登录时认证用户信息的函数（必要配置）|
|Authorizator	|用于设置授权已认证的用户路由访问权限的函数|
|PayloadFunc	|用于设置登陆成功后为向 token 中添加自定义负载信息的函数|
|Unauthorized	|用于设置 jwt 验证流程失败的响应函数|
|LoginResponse	|用于设置登录的响应函数|
|LogoutResponse	|用于设置登出的响应函数|
|RefreshResponse	|用于设置 token 有效时长刷新后的响应函数|
|IdentityHandler	|用于设置获取身份信息的函数，默认与 IdentityKey 配合使用|
|IdentityKey	|用于设置检索身份的键，默认为 identity|
|TokenLookup	|用于设置 token 的获取源，可以选择 header、query、cookie、param、form，默认为 header:Authorization|
|TokenHeadName	|用于设置从 header 中获取 token 时的前缀，默认为 Bearer|
|WithoutDefaultTokenHeadName	|用于设置 TokenHeadName 为空，默认为 false|
|TimeFunc	|用于设置获取当前时间的函数，默认为 time.Now()|
|HTTPStatusMessageFunc	|用于设置 jwt 校验流程发生错误时响应所包含的错误信息|
|SendCookie	|用于设置 token 将同时以 cookie 的形式返回，下列 cookie 相关配置生效的前提是该值为 true，默认为 false|
|CookieMaxAge	|用于设置 cookie 的有效期，默认为 Timeout 定义的一小时|
|SecureCookie	|用于设置允许不通过 HTTPS 传递 cookie 信息，默认为 false|
|CookieHTTPOnly	|用于设置允许客户端访问 cookie 以进行开发，默认为 false|
|CookieDomain	|用于设置 cookie 所属的域，默认为空|
|SendAuthorization	|用于设置为所有请求的响应头添加授权的 token 信息，默认为 false|
|DisabledAbort	|用于设置在 jwt 验证流程出错时，禁止请求上下文调用 abort()，默认为 false|
|CookieName	|用于设置 cookie 的 name 值|
|CookieSameSite	|用于设置使用 protocol.CookieSameSite 声明的参数设置 cookie 的 SameSite 属性值|
|ParseOptions	|用于设置使用 jwt.ParserOption 声明的函数选项式参数配置 jwt.Parser 的属性值|
## Gzip 压缩
```go
package main

import (
	"context"
	"fmt"
	"net/http"
	"time"

	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/hertz-contrib/gzip"
)

func main() {
	h := server.Default(server.WithHostPorts(":8080"))
	// BestCompression option
	h.Use(gzip.Gzip(gzip.BestCompression))
	// BestSpeed option
	h.Use(gzip.Gzip(gzip.BestSpeed))
	// DefaultCompression option
	h.Use(gzip.Gzip(gzip.DefaultCompression))
	// NoCompression option
	h.Use(gzip.Gzip(gzip.NoCompression))
	h.GET("/api/book", func(ctx context.Context, c *app.RequestContext) {
		c.String(http.StatusOK, "pong "+fmt.Sprint(time.Now().Unix()))
	})
	h.Spin()
}

```
|选项|	描述|
|---------|----------|----------------|
|BestCompression	|提供最佳的文件压缩率|
|BestSpeed	|提供了最佳的压缩速度|
|DefaultCompression	|默认压缩率|
|NoCompression	|不进行压缩|



gzip 提供 WithExcludeExtensions 用于帮助用户设置不需要 gzip 压缩的文件后缀，默认值为.png, .gif, .jpeg, .jpg
func WithExcludedPaths(args []string) Option
gzip 提供了 WithExcludedPaths用于帮助用户设置其不需要进行 gzip 压缩的文件路径
func WithExcludedPaths(args []string) Option
gzip 提供了WithExcludedPathRegexes用于帮助用户设置自定义的正则表达式来过滤掉不需要 gzip 压缩的文件
func WithExcludedPathRegexes(args []string) Option

## 国际化
```go
package main

import (
    "context"
    _ "embed"
    "time"

    "github.com/cloudwego/hertz/pkg/app"
    "github.com/cloudwego/hertz/pkg/app/server"
    hertzI18n "github.com/hertz-contrib/i18n"
    "github.com/nicksnyder/go-i18n/v2/i18n"
    "golang.org/x/text/language"
    "gopkg.in/yaml.v3"
)

func main() {
    h := server.New(
        server.WithHostPorts(":3000"),
        server.WithExitWaitTime(time.Second),
    )
    h.Use(hertzI18n.Localize(
        hertzI18n.WithBundle(&hertzI18n.BundleCfg{
            RootPath:         "./localize",
            AcceptLanguage:   []language.Tag{language.Chinese, language.English},
            DefaultLanguage:  language.Chinese,
            FormatBundleFile: "yaml",
            UnmarshalFunc:    yaml.Unmarshal,
        }),
    ))
    h.GET("/:name", func(c context.Context, ctx *app.RequestContext) {
        ctx.String(200, hertzI18n.MustGetMessage(&i18n.LocalizeConfig{
            MessageID: "welcomeWithName",
            TemplateData: map[string]string{
                "name": ctx.Param("name"),
            },
        }))
    })
    h.GET("/", func(c context.Context, ctx *app.RequestContext) {
        ctx.String(200, hertzI18n.MustGetMessage("welcome"))
    })

    h.Spin()
}
```

**Localize**
用于将 i18n 扩展集成进 hertz server
func Localize(opts ...Option) app.HandlerFunc
**MustGetMessage**
MustGetMessage 用于获取 i18n 信息，但不做错误处理。
func MustGetMessage(param interface{}) string
**WithBundle**
WithBundle用于将自定义配置加载进入中间件
|配置项	|类型	|默认值|	描述|
|----------------|-----------------|-----------------|----------------|
|DefaultLanguage	|language.Tag|	language.English	|默认转换语言类型|
|FormatBundleFile	|string	“yaml”	|转换文件模板类型，例如：yaml, json|
|AcceptLanguage	|[]language.Tag	[]language.Tag{defaultLanguage,language.Chinese}|	接收转换类型|
|RootPath	|string|	defaultRootPat|h	模板文件目录|
|UnmarshalFunc|	i18n.UnmarshalFunc|	yaml.Unmarshal|	模板文件解码函数，例如：yaml.Unmarshal|
|Loader	Loader	|LoaderFunc(ioutil.ReadFile)	|文件读取函数，例如 LoaderFunc(ioutil.ReadFile)

**WithGetLangHandle**
WithGetLangHandle 用于配置 i18n 模板触发条件，可以通过从参数，请求头中取出信息


func WithGetLangHandle(handler GetLangHandler)

## 访问日志
```go
package main

import (
	"context"

	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/hertz/pkg/common/utils"
	"github.com/hertz-contrib/logger/accesslog"
)

func main() {
	h := server.Default(
		server.WithHostPorts(":8080"),
	)
	h.Use(accesslog.New(accesslog.WithFormat("[${time}] ${status} - ${latency} ${method} ${path} ${queryParams}")))
	h.GET("/ping", func(ctx context.Context, c *app.RequestContext) {
		c.JSON(200, utils.H{"msg": "pong"})
	})
	h.Spin()
}



```

**WithTimeFormat**
使用 WithTimeFormat 自定义时间格式，默认时间格式为 15:04:05，具体格式可以参考该 链接 或者 go 的 time 包。
func WithTimeFormat(s string) Option 

**WithTimeInterval**
使用 WithTimeInterval 配置时间戳的刷新间隔，默认值为 500ms

**WithAccessLogFunc**
使用 WithAccessLogFunc 自定义日志打印函数

func WithAccessLogFunc(f func(ctx context.Context, format string, v ...interface{})) Option 

**WithTimeZoneLocation**
使用 WithTimeZoneLocation 自定义时区，默认使用当地时区。
func WithTimeZoneLocation(loc *time.Location) Option 

## Casbin
Casbin 是⼀个强⼤的、⾼效的开源访问控制框架，其权限管理机制支持常用的多种 访问控制模型，如 ACL/RBAC/ABAC 等。可以实现灵活的访问权限控制
```go
package main

import (
    "context"
    "log"
    
    "github.com/cloudwego/hertz/pkg/app"
    "github.com/cloudwego/hertz/pkg/app/server"
    "github.com/hertz-contrib/casbin"
    "github.com/hertz-contrib/sessions"
    "github.com/hertz-contrib/sessions/cookie"
)

func main() {
    h := server.Default()
    
    // 使用 session 存储用户信息.
    store := cookie.NewStore([]byte("secret"))
    h.Use(sessions.New("session", store))
    auth, err := casbin.NewCasbinMiddleware("example/config/model.conf", "example/config/policy.csv", subjectFromSession)
    if err != nil {
        log.Fatal(err)
    }
    
    h.POST("/login", func(ctx context.Context, c *app.RequestContext) {
        // 校验用户名和密码.
        // ...
    
        // 存储用户名 (casbin 访问实体)
        session := sessions.Default(c)
        session.Set("name", "alice")
        err := session.Save()
        if err != nil {
            log.Fatal(err)
        }
        c.String(200, "you login successfully")
    })
    
    h.GET("/book", auth.RequiresPermissions("book:read", casbin.WithLogic(casbin.AND)), func(ctx context.Context, c *app.RequestContext) {
        c.String(200, "you read the book successfully")
    })
    
    h.POST("/book", auth.RequiresRoles("user", casbin.WithLogic(casbin.AND)), func(ctx context.Context, c *app.RequestContext) {
        c.String(200, "you posted a book successfully")
    })
    
    h.Spin()
}

// subjectFromSession 从 session 中获取访问实体.
func subjectFromSession(ctx context.Context, c *app.RequestContext) string {
    // 获取访问实体
    session := sessions.Default(c)
    if subject, ok := session.Get("name").(string); !ok {
        return ""
    } else {
        return subject
    }
}
```

74