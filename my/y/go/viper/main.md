# Viper简单介绍
## 什么是Viper

Viper是Go应用程序的完整配置解决方案，包括12-Factor应用程序。它旨在在应用程序中工作，并可以处理所有类型的配置需求和格式。Viper可以被认为是所有应用程序配置需求的注册表。它支持：


- 设置默认值
- 从JSON，TOML，YAML，HCL和Java属性配置文件中读取
- 实时观看和重新读取配置文件（可选）
- 从环境变量中读取
- 从远程配置系统（etcd或Consul）读取，并观察变化
- 从命令行标志读取
- 从缓冲区读取
- 设置显式值

## 为何选择Viper

- 以JSON，TOML，YAML，HCL或Java属性格式查找，加载和解组配置文件。
- 提供一种机制来为不同的配置选项设置默认值。
- 提供一种机制来为通过命令行标志指定的选项设置覆盖值。
- 提供别名系统，轻松重命名参数，而不会破坏现有代码。
- 可以很容易地区分用户提供命令行或配置文件与默认值相同的时间。

## 配置方式的优先级顺序

viper提供的配置方式的优先级顺序如下(由高到低)：
1.设置显示调用(explicit call to Set)
2.命令行标志(flag)
3.环境变量(env)
4.配置文件(config)
5.远程键/值存储(key/value store)
6.默认值(default)

# 安装及使用
##  安装依赖
```go
go get github.com/spf13/viper
```

## 设置默认值
```go
viper.SetDefault("ContentDir", "content")
viper.SetDefault("LayoutDir", "layouts")
viper.SetDefault("Taxonomies", map[string]string{"tag": "tags", "category": "categories"})
```
复制代码
2.3 读取配置文件

Viper需要最少的配置，因此它知道在哪里查找配置文件。Viper支持JSON，TOML，YAML，HCL和Java Properties文件。Viper可以搜索多个路径，但目前单个Viper实例仅支持单个配置文件。Viper不会默认使用任何配置搜索路径，而是将默认值决定应用于应用程序。
以下是如何使用Viper搜索和读取配置文件的示例,定义在config目录下新建一个appConfig.yaml文件，文件内容如下

#定义一个数据库连接的yaml配置文件测试
IpAddress: "127.0.0.1"
Port: 3306
UserName: "root"
Password: 123456
DataBaseName: "go_test" 
复制代码
package main

import (
	"fmt"
	"github.com/spf13/viper"
)

//定义接收配置文件的结构体
type DataBaseConnection struct {
	IpAddress    string
	Port         int
	UserName     string
	Password     int
	DataBaseName string
}

func main() {
	config := viper.New()
	//配置文件名（不带扩展名）
	config.SetConfigName("appConfig")
	//在项目中查找配置文件的路径，可以使用相对路径，也可以使用绝对路径
	config.AddConfigPath("D:/go_project/src/github.com/ourlang/demo/config")
	//多次调用以添加多个搜索路径
	//viper.AddConfigPath("D:/go_project/src/github.com/ourlang/demo/utils")
	//设置文件类型，这里是yaml文件
	config.SetConfigType("yaml")
	//定义用于接收配置文件的变量
	var configData DataBaseConnection
	//查找并读取配置文件
	err := config.ReadInConfig()
	if err != nil { // 处理读取配置文件的错误
		panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}

	if err := config.Unmarshal(&configData); err != nil { // 读取配置文件转化成对应的结构体错误
		panic(fmt.Errorf("read config file to struct err: %s \n", err))
	}
	//控制台打印输出配置文件读取的值
	fmt.Println(configData) //{127.0.0.1 3306 root 123456 go_test}
}
复制代码
2.4 监听并重新读取配置文件

Viper支持在运行时让应用程序实时读取配置文件。需要重新启动服务器以使配置生效的日子已经一去不复返了，viper驱动的应用程序可以在运行时读取配置文件的更新，而不会错过任何一个节拍。
只需告诉viper实例watchConfig即可。您可以选择为Viper提供每次发生更改时运行的功能。

确保在调用之前添加所有configPath WatchConfig()
config := viper.New()
config.WatchConfig()
config.OnConfigChange(func(e fsnotify.Event) {
     //viper配置发生变化了 执行响应的操作
	fmt.Println("Config file changed:", e.Name)
})
复制代码
2.5 从io.Reader读取配置

Viper预定义了许多配置源，例如文件，环境变量，标志和远程K/V存储，但您不受它们的约束。您还可以实现自己的必需配置源并将其提供给viper。

package main

import (
	"bytes"
	"fmt"
	"github.com/spf13/viper"
)

func main() {
	config := viper.New()

	config.SetConfigType("yaml") // 或viper.SetConfigType（“YAML”）
	//任何需要将此配置放入程序的方法
	var yamlExample = []byte(`
Hacker: true
name: steve
hobbies:
- skateboarding
- snowboarding
- go
clothing:
  jacket: leather
  trousers: denim
age: 35
eyes : brown
beard: true
`)
	//读取配置
	config.ReadConfig(bytes.NewBuffer(yamlExample))

	name := config.Get("name")
	fmt.Println(name)
}
复制代码
2.6 设置并覆盖配置值
config := viper.New()
config.Set("Verbose", true)
config.Set("LogFile", LogFile)
复制代码
2.7 注册和使用别名

别名允许多个键引用单个值

package main

import (
	"github.com/spf13/viper"
)

func main() {
	config := viper.New()
	config.RegisterAlias("loud", "Verbose")
	config.Set("verbose", true) // 结果与下一行相同
	config.Set("loud", true)    // 与上一行相同的结果
	config.GetBool("loud")      // true
	config.GetBool("verbose")   // true
}
复制代码
2.8 使用环境变量

Viper完全支持环境变量。有四种方法可以帮助使用环境变量：

//AutomaticEnv尤其是当与结合了强大的帮手 SetEnvPrefix。调用时，Viper将在任何viper.Get请求发出时检查环境变量。
//它将适用以下规则。它将检查一个环境变量，其名称与大写的键匹配，并以EnvPrefix前缀。
AutomaticEnv()
//BindEnv需要一个或两个参数。第一个参数是键名，第二个是环境变量的名称。
//环境变量的名称区分大小写。如果未提供ENV变量名，则Viper将自动假设密钥名称与ENV变量名称匹配，但ENV变量为IN ALL CAPS。
//当您明确提供ENV变量名称时，它不会自动添加前缀。
BindEnv(string...) : error
SetEnvPrefix(string)
//SetEnvKeyReplacer允许您使用strings.Replacer对象重写Env键到一定程度。如果要在Get()调用中使用或使用某些内容,
//但希望环境变量使用_分隔符，则此选项非常有用。可以在中找到使用它的示例viper_test.go 
SetEnvKeyReplacer(string...) *strings.Replacer
复制代码
ENV实例
SetEnvPrefix("spf")  //将自动大写
BindEnv("id")
os.Setenv("SPF_ID", "13") // 通常在应用以外完成
id := Get("id") // 13
复制代码
使用flag

Viper能够绑定到flag。就像BindEnv,在调用绑定方法时,不会设置该值。这意味着您可以尽早绑定,甚至可以在init()函数中绑定.
对于单个标志,该BindPFlag()方法提供此功能。

serverCmd.Flags().Int("port", 1138, "Port to run Application server on")
viper.BindPFlag("port", serverCmd.Flags().Lookup("port"))
复制代码
绑定一组现有的pflags
pflag.Int("flagname", 1234, "help message for flagname")
pflag.Parse()
viper.BindPFlags(pflag.CommandLine)
i := viper.GetInt("flagname") 
复制代码
flag接口

如果您不使用，Viper提供两个Go接口来绑定其他标志系统Pflags
FlagValue代表一个标志。这是一个关于如何实现此接口的非常简单的示例：

type myFlag struct {}
 func  （f  myFlag）HasChanged（）bool { return  false }
 func  （f  myFlag）Name（）string { return  “ my-flag-name ” }
 func  （f  myFlag）ValueString（）string { return  “ my -flag-value “ }
 func  （f  myFlag）ValueType（）string { return  “ string ” }
复制代码
一旦你的flag实现了这个接口，你可以告诉Viper绑定它：
viper.BindFlagValue("my-flag-name", myFlag{})
复制代码
2.9 远程key/value存储

Viper可以从例如etcd、Consul的远程Key/Value存储系统的一个路径上,读取一个配置字符串（JSON, TOML, YAML 或 HCL 格式）. 这些值优先于默认值，但会被从磁盘文件、命令行 flag、环境变量的配置所覆盖.要在Viper中启用远程支持，请对viper/remote 包进行空白导入：

import _ "github.com/spf13/viper/remote"
复制代码
远程key/value存储示例 - 未加密
viper.AddRemoteProvider("etcd", "http://127.0.0.1:4001","/config/hugo.json")
viper.SetConfigType("json") //因为字节流中没有文件扩展名，支持的扩展名是“json”，“toml”，“yaml”，“yml”，“properties”，“props”，“prop”
err := viper.ReadRemoteConfig()
复制代码
远程key/value存储示例 - 加密
viper.AddSecureRemoteProvider("etcd","http://127.0.0.1:4001","/config/hugo.json","/etc/secrets/mykeyring.gpg")
viper.SetConfigType("json") //因为字节流中没有文件扩展名，支持的扩展名是“json”，“toml”，“yaml”，“yml”，“properties”，“props”，“prop” 
err := viper.ReadRemoteConfig()
复制代码
监听etcd中的变化 - 未加密
//或者，您可以创建一个新的viper实例
var runtime_viper = viper.New()
 
runtime_viper.AddRemoteProvider("etcd", "http://127.0.0.1:4001", "/config/hugo.yml")
runtime_viper.SetConfigType("yaml")
 
// 第一次从远程配置中读取
err := runtime_viper.ReadRemoteConfig()
 
//解密配置
runtime_viper.Unmarshal(&runtime_conf)
 
// 打开一个goroutine来永远监听远程变化
go func(){
	for {
	    time.Sleep(time.Second * 5) // 每次请求后延迟
	    err := runtime_viper.WatchRemoteConfig()
	    if err != nil {
	        log.Errorf("unable to read remote config: %v", err)
	        continue
	    }
 
	    //将新配置解组到我们的运行时配置结构中。您还可以使用通道
        //实现信号以通知系统更改 
	    runtime_viper.Unmarshal(&runtime_conf)
	}
}()
复制代码
3 Viper获取值方法汇总

在Viper中，有几种方法可以根据值的类型获取值。如果找不到，每个Get函数都将返回零值。IsSet()方法检查给定密钥是否存在。
存在以下功能和方法：

Get(key string) : interface{}
GetBool(key string) : bool
GetFloat64(key string) : float64
GetInt(key string) : int
GetString(key string) : string
GetStringMap(key string) : map[string]interface{}
GetStringMapString(key string) : map[string]string
GetStringSlice(key string) : []string
GetTime(key string) : time.Time
GetDuration(key string) : time.Duration
IsSet(key string) : bool
AllSettings() : map[string]interface{}
复制代码
4 访问嵌套数据
4.1 JSON嵌套

访问器方法也接受深层嵌套键的格式化路径。Viper可以通过传递.分隔的键路径来访问嵌套字段。

{
    "host": {
        "address": "localhost",
        "port": 5799
    },
    "datastore": {
        "metric": {
            "host": "127.0.0.1",
            "port": 3099
        },
        "warehouse": {
            "host": "198.0.0.1",
            "port": 2112
        }
    }
}
复制代码
GetString("datastore.metric.host") // (returns "127.0.0.1")
复制代码
4.2 YAML嵌套示例一
yaml文件如下，使用4.1的Get方法获取数据
database:
  host: 127.0.0.1
  user: root
  dbname: test
  pwd: 123456
复制代码
package main
 
import (
	"fmt"
	"os"
 
	"github.com/spf13/viper"
)
 
func main() {
	//获取项目的执行路径
	path, err := os.Getwd()
	if err != nil {
		panic(err)
	}
	config := viper.New()
	config.AddConfigPath(path)     //设置读取的文件路径
	config.SetConfigName("config") //设置读取的文件名
	config.SetConfigType("yaml")   //设置文件的类型
	//尝试进行配置读取
	if err := config.ReadInConfig(); err != nil {
		panic(err)
	}
	//打印文件读取出来的内容:
	fmt.Println(config.Get("database.host"))
	fmt.Println(config.Get("database.user"))
	fmt.Println(config.Get("database.dbname"))
	fmt.Println(config.Get("database.pwd"))
}
--------------------------打印结果----------------------
127.0.0.1
root
test
123456
复制代码
4.3 YAML多层嵌套示例二

yaml文件如下，结构体嵌套的方式接受，特别注意：读取多层嵌套 字段首字母必须大写

dataConnection:
    userName: "root"
    password: "admin"
    ipAddress: "127.0.0.1"
    port: 3306
    nginx:
      port: 443
      logpath:  "/var/log//nginx/nginx.log"
复制代码
package main

import (
	"fmt"
	"github.com/spf13/viper"
)

type ConnectionConfig struct {
	DataConnection DataConnection //读取多层嵌套 字段首字母必须大写
}

type DataConnection struct {
	UserName  string
	Password  string
	IpAddress string
	Port      int
	Nginx     Nginx //读取多层嵌套 字段首字母必须大写
}
type Nginx struct {
	Port    int
	Logpath string //读取多层嵌套 字段首字母必须大写
}

func main() {
	config := viper.New()
	config.SetConfigName("ApplicationConfig")
	config.AddConfigPath("config")
	config.SetConfigType("yaml")
	var configData ConnectionConfig
	err := config.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("Fatal error config file: %s \n", err))
	}
	if err := config.Unmarshal(&configData); err != nil {
		panic(fmt.Errorf("read config file to struct err: %s \n", err))
	}

	fmt.Println(configData)
}
-------------------------输出结果-----------------
{{root admin 127.0.0.1 3306 {443 /var/log//nginx/nginx.log}}}

