# slog 快速入门
让我们从探讨该包的设计和架构开始。它提供了三种您应该熟悉的主要类型:log/slog
- Logger：日志"前端"，提供了诸如 Info() 和 Error() 等级别方法来记录感兴趣的事件。
- Record：由 Logger 创建的每个独立日志对象的表示形式。
- Handler：一旦实现了这个接口，就可以决定每个  Record 的格式化和目的地。该包中包含两个内置处理程序：TextHandler 用于 key=value 输出，JSONHandler 用于 JSON 输出。
与大多数 Go 日志库一样， slog包公开了一个可通过包级别函数访问的默认 Logger。该 logger 产生的输出与旧的 log.Printf() 方法几乎相同，只是多了日志级别。

## 快速开始
slog 使用非常简单，导入 log/slog 后即可使用：
```go
package main

import "log/slog"

func main() {
    slog.Debug("debug message")
    slog.Info("info message")
    slog.Warn("warn message")
    slog.Error("error message")
}
```
执行示例代码，输出结果如下：
```shell
$ go run main.go
2024/07/28 10:20:38 INFO info message
2024/07/28 10:20:38 WARN warn message
2024/07/28 10:20:38 ERROR error message
```
slog 日志默认输出到 os.Stdout, 日志默认级别为 Info。

slog 默认仅支持 Debug、Info、Warn、Error 这 4 种日志级别

## 附加属性
slog 支持在 msg 后传入无限多个 key/value 键值对来附加额外的属性：
```go
slog.Debug("debug message", "hello", "world")
slog.Info("info message", "hello", "world")
slog.Warn("warn message", "hello", "world")
slog.Error("error message", "hello", "world")
```
执行示例代码，输出结果如下：
```shell
$ go run main.go
2024/07/28 10:25:33 INFO info message hello=world
2024/07/28 10:25:33 WARN warn message hello=world
2024/07/28 10:25:33 ERROR error message hello=world
```
可以发现，传递给日志方法的键值对会以 key=value 格式输出。

## 修改日志级别
我们可以将 slog 日志级别修改为 Debug：
```go
slog.SetLogLoggerLevel(slog.LevelDebug)
slog.Debug("debug message", "hello", "world")
slog.Info("info message", "hello", "world")
slog.Warn("warn message", "hello", "world")
slog.Error("error message", "hello", "world")
```

## 获取当前日志级别
既然可以修改日志级别，那么我们是否也可以获取当前日志级别呢？

很遗憾，slog 没有为我们提供一个方法可以便捷的获取日志级别。

不过，slog 的 Logger 对象有一个 Enabled 方法，可以用来判断给定的日志级别是否被开启。

那么我们就可以将日志级别由低到高依次传给 Enabled 方法来判断当前日志级别是否启用，只要当前日志级别已经启用，就说明 slog 开启的最低日志级别是当前日志级别。

示例代码如下：
```go
var currentLevel slog.Level = -10
for _, level := range []slog.Level{slog.LevelDebug, slog.LevelInfo, slog.LevelWarn, slog.LevelError} {
    r := slog.Default().Enabled(context.Background(), level)
    if r {
        currentLevel = level
        break
    }
}
fmt.Printf("current log level: %v\n", currentLevel)
```
代码中初始化 currentLevel 用来记录当前日志级别，类型为 slog.Level，初始值为 -10。这之所以能生效，是因为其实 slog.Level 本身就是 int 类型。

slog 默认支持的几种日志级别定义如下：
```go
type Level int

const (
    LevelDebug Level = -4
    LevelInfo  Level = 0
    LevelWarn  Level = 4
    LevelError Level = 8
)
```
## 结构化日志
虽然我们说 slog 是结构化的日志包，但其实前文示例中打印的日志结果，并不是结构化的。

### JSONHandler
slog 支持 JSON 结构化日志。
```go
l := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    AddSource:   true,            // 记录日志位置
    Level:       slog.LevelDebug, // 设置日志级别
    ReplaceAttr: nil,
}))
l.Debug("debug message", "hello", "world")
```

执行示例代码，输出结果如下：
```go
$ go run main.go
{"time":"2024-07-28T15:31:25.5883799+08:00","level":"DEBUG","source":{"function":"kis-flow/test.TestSlog","file":"D:/project/go/kis-flow/test/kis_test.go","line":62},"msg":"debug message","hello":"world"}
```
### TextHandler
slog 内置的另一个 slog.Handler 对象是 *slog.TextHandler，可以将日志输出为 key=value 结构：
```go
l := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
    AddSource:   true,            // 记录日志位置
    Level:       slog.LevelDebug, // 设置日志级别
    ReplaceAttr: nil,
}))
l.Debug("debug message", "hello", "world")
```
执行示例代码，输出结果如下：
```shell
$ go run main.go
time=2024-07-28T15:32:47.059+08:00 level=DEBUG source=D:/project/go/kis-flow/test/kis_test.go:62 msg="debug message" hello=world
```

## 属性分组
我们可以使用 slog.Group 为一组 key/value 属性进行分组。

### JSONHandler
这是使用 JSONHandler 的属性分组示例：
```go
l := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    AddSource:   true,            // 记录日志位置
    Level:       slog.LevelDebug, // 设置日志级别
    ReplaceAttr: nil,
}))

l.Info(
    "info message",
    slog.Group("user", "name", "root", slog.Int("age", 20)),
)
```
执行示例代码，输出结果如下：
```go
$ go run main.go
{"time":"2024-07-28T15:37:46.047114+08:00","level":"INFO","source":{"function":"kis-flow/test.TestSlog","file":"D:/project/go/kis-flow/test/kis_test.go","line":63},"msg":"info message","user":{"name":"root","age":20}}

```
可以发现，slog.Group 第一个参数为分组名称 user，接下来传递的属性键值对都属于这个分组。


## 使用子 logger
可以使用 With 方法附加自定义属性到一个新的 *slog.Logger 对象。

这个新得到的 *slog.Logger 对象使用方式不变，但其所有日志记录都会携带统一的附加属性，非常适合简化代码。
```go
l := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    AddSource:   true,            // 记录日志位置
    Level:       slog.LevelDebug, // 设置日志级别
    ReplaceAttr: nil,
}))
// 附加自定义属性
sl := l.With("requestId", "10191529-bc34-4efe-95e4-ecac7321773a")
sl.Debug("debug message")
sl.Info("info message")
```
我们为新的 *slog.Logger 对象 sl 附加了 requestId，这在 Web 开发中非常常用，可以用来追踪整个请求链。

接下来使用 sl 输出的日志都会携带这个 requestId 属性。

执行示例代码，输出结果如下：
```go
$ go run main.go
{
    "time": "2024-06-23T10:35:53.966953+08:00",
    "level": "DEBUG",
    "source": {
        "function": "main.main",
        "file": "/workspace/projects/blog-go-example/log/slog/main.go",
        "line": 195
    },
    "msg": "debug message",
    "requestId": "10191529-bc34-4efe-95e4-ecac7321773a"
}
{
    "time": "2024-06-23T10:35:53.966972+08:00",
    "level": "INFO",
    "source": {
        "function": "main.main",
        "file": "/workspace/projects/blog-go-example/log/slog/main.go",
        "line": 196
    },
    "msg": "info message",
    "requestId": "10191529-bc34-4efe-95e4-ecac7321773a"
}
```
## 为子 logger 属性分组
子 logger 对象同样支持属性分组，示例代码如下：
```go
l := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    AddSource:   true,            // 记录日志位置
    Level:       slog.LevelDebug, // 设置日志级别
    ReplaceAttr: nil,
}))

sl := l.WithGroup("user").With("requestId", "10191529-bc34-4efe-95e4-ecac7321773a")
sl.Debug("debug message", "name", "admin")
sl.Info("info message", "name", "admin")
```
使用 WithGroup 方法可以对子 logger 属性进行分组，这里同时使用了 With 又得到一个新的子 logger 对象。

执行示例代码，输出结果如下：
```shell
$ go run main.go
{"time":"2024-07-28T15:43:00.5474451+08:00","level":"DEBUG","source":{"function":"kis-flow/test.TestSlog","file":"D:/project/go/kis-flow/test/kis_test.go","line":64},"msg":"debug message","user":{"requestId":"10191529-bc34-4efe-95e4-ecac7321773a","name":"admin"}}
{"time":"2024-07-28T15:43:00.5711108+08:00","level":"INFO","source":{"function":"kis-flow/test.TestSlog","file":"D:/project/go/kis-flow/test/kis_test.go","line":65},"msg":"info message","user":{"requestId":"10191529-bc34-4efe-95e4-ecac7321773a","name":"admin"}}
```
可以发现，使用 With 附加的属性和调用 Debug、info 方法附加的属性都被分组到了 user 中。

## 实现 slog.LogValuer 接口，隐藏敏感信息
有时候，我们可能要在日志中记录某个模型。

比如这里有一个 User 模型：

type User struct {
    ID       int    `json:"id"`
    Name     string `json:"name"`
    Password string `json:"password"`
}
如果直接将 User 实例对象传给 slog 进行记录，那么 password 属性也会被记录，这通常并不是我们想要的。
slog 为我们提供了 slog.LogValuer 接口，一个对象只要实现这个接口，就可以直接传递给 slog 进行记录。

slog.LogValuer 接口定义如下：
```go
type LogValuer interface {
    LogValue() Value
}
```
所以，我们可以为 User 实现一个 LogValue 方法：
```go
func (u *User) LogValue() slog.Value {
    return slog.GroupValue(
        slog.Int("id", u.ID),
        slog.String("name", u.Name),
    )
}
```
# 自定义 Logger
具体案例
```go
package main

import (
	"context"
	"log/slog"
	"os"
	"runtime"
	"time"
)

type Level = slog.Level

// 设置自定义日志级别
const (
	LevelDebug = slog.LevelDebug
	LevelTrace = slog.Level(-2) // 自定义日志级别
	LevelInfo  = slog.LevelInfo
	LevelWarn  = slog.LevelWarn
	LevelError = slog.LevelError
)

type Logger struct {
	l   *slog.Logger
	lvl *slog.LevelVar // 用来动态调整日志级别
}

func New(level slog.Level) *Logger {
	var lvl slog.LevelVar
	lvl.Set(level)

	h := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
		AddSource: true,

		// Level:     level, // 静态设置日志级别
		Level: &lvl, // 支持动态设置日志级别

		// 修改日志中的 Attr 键值对（即日志记录中附加的 key/value）
		ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
			if a.Key == slog.LevelKey {
				level := a.Value.Any().(slog.Level)
				levelLabel := level.String()

				switch level {
				case LevelTrace:
					// NOTE: 如果不设置，默认日志级别打印为 "level":"DEBUG+2"
					levelLabel = "TRACE"
				}

				a.Value = slog.StringValue(levelLabel)
			}

			// NOTE: 可以在这里修改时间输出格式
			// if a.Key == slog.TimeKey {
			//     if t, ok := a.Value.Any().(time.Time); ok {
			//         a.Value = slog.StringValue(t.Format(time.DateTime))
			//     }
			// }

			return a
		},
	}))

	return &Logger{l: h, lvl: &lvl}
}

// SetLevel 动态调整日志级别
func (l *Logger) SetLevel(level Level) {
	l.lvl.Set(level)
}

func (l *Logger) Debug(msg string, args ...any) {
	l.l.Debug(msg, args...)
}

func (l *Logger) Info(msg string, args ...any) {
	l.Log(context.Background(), LevelInfo, msg, args...)
}

// Trace 自定义的日志级别
func (l *Logger) Trace(msg string, args ...any) {
	l.Log(context.Background(), LevelTrace, msg, args...)
}

func (l *Logger) Warn(msg string, args ...any) {
	l.Log(context.Background(), LevelWarn, msg, args...)
}

func (l *Logger) Error(msg string, args ...any) {
	l.Log(context.Background(), LevelError, msg, args...)
}

func (l *Logger) Log(ctx context.Context, level slog.Level, msg string, args ...any) {
	l.log(ctx, level, msg, args...)
}

// log是参数为…any的方法的低级日志方法。
// 它必须总是由导出的日志方法直接调用
// 或函数，因为它使用固定的调用深度来获取pc。
func (l *Logger) log(ctx context.Context, level slog.Level, msg string, args ...any) {
	if !l.l.Enabled(ctx, level) {
		return
	}
	var pc uintptr
	var pcs [1]uintptr
	// NOTE: 这里修改 skip 为 4，*slog.Logger.log 源码中 skip 为 3
	runtime.Callers(4, pcs[:])
	pc = pcs[0]
	r := slog.NewRecord(time.Now(), level, msg, pc)
	r.Add(args...)
	if ctx == nil {
		ctx = context.Background()
	}
	_ = l.l.Handler().Handle(ctx, r)
}
func main() {
	l := New(LevelDebug)
	l.Debug("custom debug message", "hello", "world")
	l.Trace("custom trace message", "hello", "world")
	l.Info("custom info message", "hello", "world")
}

```
结果
```shell
{"time":"2024-07-28T16:20:33.600095+08:00","level":"DEBUG","source":{"function":"main.(*Logger).Debug","file":"D:/project/go/kis-flow/main.go","line":73},"msg":"custom debug message","hello":"world"}
{"time":"2024-07-28T16:20:33.6175048+08:00","level":"TRACE","source":{"function":"main.main","file":"D:/project/go/kis-flow/main.go","line":120},"msg":"custom trace message","hello":"world"}
{"time":"2024-07-28T16:20:33.6175048+08:00","level":"INFO","source":{"function":"main.main","file":"D:/project/go/kis-flow/main.go","line":121},"msg":"custom info message","hello":"world"}
```

# 自定义 Handler
既然讲解了如何自定义 slog 的前端 Logger，我们不妨看一下如何自定义 slog 的后端 Handler。

```go
// A Handler handles log records produced by a Logger.
type Handler interface {
    // Enabled reports whether the handler handles records at the given level.
    Enabled(context.Context, Level) bool

    // Handle handles the Record.
    Handle(context.Context, Record) error

    // WithAttrs returns a new Handler whose attributes consist of
    // both the receiver's attributes and the arguments.
    WithAttrs(attrs []Attr) Handler

    // WithGroup returns a new Handler with the given group appended to
    // the receiver's existing groups.
    WithGroup(name string) Handler
}
```
例子
```go
package main

import (
	"context"
	"io"
	"log/slog"
	"os"
)

// Handler 自定义日志后端 slog.Handler
type Handler struct {
	slog.Handler
}

// NewHandler 创建新的日志后端 handler
func NewHandler(w io.Writer, opts *slog.HandlerOptions) *Handler {
	return &Handler{
		Handler: slog.NewJSONHandler(w, opts),
	}
}

// Enabled 当前日志级别是否开启
func (h *Handler) Enabled(ctx context.Context, level slog.Level) bool {
	return h.Handler.Enabled(ctx, level)
}

// Handle 处理日志记录，仅在 Enabled() 返回 true 时才会被调用
func (h *Handler) Handle(ctx context.Context, record slog.Record) error {
	record.Add("customlog", "handler")
	return h.Handler.Handle(ctx, record)
}

// WithAttrs 从现有的 handler 创建一个新的 handler，并将新增属性附加到新的 handler
func (h *Handler) WithAttrs(attrs []slog.Attr) slog.Handler {
	return h.Handler.WithAttrs(attrs)
}

// WithGroup 从现有的 handler 创建一个新的 handler，并将指定分组附加到新的 handler
func (h *Handler) WithGroup(name string) slog.Handler {
	return h.Handler.WithGroup(name)
}
func main() {
	l := slog.New(NewHandler(os.Stdout, nil))
	l.Info("info message", "hello", "world")
}
```
结果
```shell
{"time":"2024-07-28T16:46:02.5997431+08:00","level":"INFO","msg":"info message","hello":"world","customlog":"handler"}
```
