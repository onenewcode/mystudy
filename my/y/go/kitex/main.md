# 概述
Kitex字节跳动内部的 Golang 微服务 RPC 框架，具有高性能、强可扩展的特点，在字节内部已广泛使用。如果对微服务性能有要求，又希望定制扩展融入自己的治理体系，Kitex 会是一个不错的选择。
## 架构设计
![alt text](image.png)
## 框架特点
- 高性能
使用自研的高性能网络库 Netpoll，性能相较 go net 具有显著优势。
- 扩展性
提供了较多的扩展接口以及默认扩展实现，使用者也可以根据需要自行定制扩展，具体见下面的框架扩展。
- 多消息协议
RPC 消息协议默认支持 Thrift、Kitex Protobuf、gRPC。Thrift 支持 Buffered 和 Framed 二进制协议；Kitex Protobuf 是 Kitex 自定义的 Protobuf 消息协议，协议格式类似 Thrift；gRPC 是对 gRPC 消息协议的支持，可以与 gRPC 互通。除此之外，使用者也可以扩展自己的消息协议。
- 多传输协议
传输协议封装消息协议进行 RPC 互通，传输协议可以额外透传元信息，用于服务治理，Kitex 支持的传输协议有 TTHeader、HTTP2。TTHeader 可以和 Thrift、Kitex Protobuf 结合使用；HTTP2 目前主要是结合 gRPC 协议使用，后续也会支持 Thrift。
- 多种消息类型
支持 PingPong、Oneway、双向 Streaming。其中 Oneway 目前只对 Thrift 协议支持，双向 Streaming 只对 gRPC 支持，后续会考虑支持 Thrift 的双向 Streaming。
- 服务治理
支持服务注册/发现、负载均衡、熔断、限流、重试、监控、链路跟踪、日志、诊断等服务治理模块，大部分均已提供默认扩展，使用者可选择集成。
- 代码生成
Kitex 内置代码生成工具，可支持生成 Thrift、Protobuf 以及脚手架代码。

# 环境
## 代码生成工具
确保已经安装GoLang环境。

Kitex 中使用到的代码生成工具包括 IDL 编译器, protobuf 编译器,kitex tool。

### IDL 编译器
IDL 编译器能够解析 IDL 并生成对应的序列化和反序列化代码，Kitex 支持 Thrift 和 protobuf 这两种 IDL，这两种 IDL 的解析分别依赖于 thriftgo 与 protoc。

#### 安装IDL编译器
安装 thriftgo，执行以下命令即可：
>go install github.com/cloudwego/thriftgo@latest

安装成功后，执行 thriftgo --version 可以看到具体版本号的输出：

>thriftgo --version

thriftgo 0.3.6

protobuf 执行以下命令即可：
>go install  github.com/golang/protobuf/proto

安装成功后，执行 protoc --version  可以看到具体版本号的输出：
>protoc --version  

libprotoc 23.0

#### kitex tool
kitex 是 Kitex 框架提供的用于生成代码的一个命令行工具。目前，kitex 支持 thrift 和 protobuf 的 IDL，并支持生成一个服务端项目的骨架。kitex 的使用需要依赖于 IDL 编译器确保你已经完成 IDL 编译器的安装。

执行以下命令：

go install github.com/cloudwego/kitex/tool/cmd/kitex@latest
安装成功后，执行 kitex --version 可以看到具体版本号的输出：

>kitex --version

v0.8.0
# 基础教程
首先我们我们创建一个名叫mykitex的文件，然后在命令行运行以下命令初始化模块。
>go mod init mykitex

然后在根目录创建idl文件夹。
然后创建以下文件添加以下内容。

一般不同的服务都会使用不同的 IDL，所以我们这里创建 item.thrift 与 stock.thrift 分别定义商品服务与库存服务的接口，同时创建 base.thrift 定义公共数据结构。

>base.proto
```proto
syntax = "proto3";
// 设置生成类的包路径
package base;

// 输出路径；
option go_package = "example/shop/base";



// 设置基础结构体
message BaseResp{
    string code=1;
    string msg=2;
}
```

item.proto
```proto
syntax = "proto3";
package item;
// 第一个分割参数，输出路径；第二个设置生成类的包路径

option go_package = "example/shop/item";
// 引入公共文件
import "idl/base.proto";
// 所有字段默认必填，

message Item {
int64 id=1;
string title=2;
string description=3;
int64 stock=4;
}

message GetItemReq {
  int64 id=1;
}

message GetItemResp {
 Item item=1;
base.BaseResp baseResp=255;
}

service ItemService{
   rpc GetItem(GetItemReq) returns (GetItemResp);
}


```

stock.proto
```proto
syntax = "proto3";
package item;
// 第一个分割参数，输出路径；第二个设置生成类的包路径
option go_package = "example/shop/stock";
// 引入公共文件
import "idl/base.proto";

// 设置服务名称
message GetItemStockReq {
  int64 item_id = 1;
}

message GetItemStockResp {
  int64 stock = 1;

  base.BaseResp base_resp = 255; // 在 protobuf 中，字段名应遵循小写字母和下划线的命名规范
}

service StockService {
  rpc GetItemStock(GetItemStockReq) returns (GetItemStockResp);
}
```

## 代码生成
有了 IDL 以后我们便可以通过 kitex 工具生成项目代码了，我们在先回到项目的根目录即 example_shop。因为我们有两个 IDL 定义了服务，所以执行两次 kitex 命令：
```shell
kitex -module mykitex idl/item.proto

kitex -module mykitex idl/stock.proto
```
生成的代码分两部分，一部分是结构体的编解码序列化代码，由 IDL 编译器生成；另一部分由 kitex 工具在前者产物上叠加，生成用于创建和发起 RPC 调用的桩代码。它们默认都在 kitex_gen 目录下。

上面生成的代码并不能直接运行，需要自己完成 NewClient 和 NewServer 的构建。kitex 命令行工具提供了 -service 参数能直接生成带有脚手架的代码，接下来让我们为商品服务和库存服务分别生成脚手架。

首先为两个 RPC 服务分别单独创建目录。
>mkdir -p rpc/item rpc/stock

再分别进入各自的目录中，执行如下命令生成代码：
```shell
// item 目录下执行
kitex -module mykitex -service example.shop.item -use mykitex/kitex_gen -I ../../  ../../idl/item.proto  

// stock 目录下执行
kitex -module mykitex -service example.shop.item -use mykitex/kitex_gen -I ../../  ../../idl/stock.proto
```

kitex 默认会将代码生成到执行命令的目录下，kitex 的命令中：
- -module 参数表明生成代码的 go mod 中的 module name，在本例中为 example_shop
- -service 参数表明我们要生成脚手架代码，后面紧跟的 example.shop.item 或 example.shop.stock 为该服务的名字。
- -use 参数表示让 kitex 不生成 kitex_gen 目录，而使用该选项给出的 import path。在本例中因为第一次已经生成 kitex_gen 目录了，后面都可以复用。
- 最后一个参数则为该服务的 IDL 文件


```shell
│  go.mod // go module 文件
│  go.sum
│
├─.idea
│      .gitignore
│      modules.xml
│      mykitex.iml
│      workspace.xml
│
├─idl        // 示例 idl 存放的目录
│      base.proto
│      item.proto
│      stock.proto
│
├─kitex_gen
│  └─example
│      └─shop
│          ├─base  // 根据 IDL 生成的编解码文件，由 IDL 编译器生成
│          │      base.pb.fast.go
│          │      base.pb.go
│          │
│          ├─item
│          │  │  item.pb.fast.go
│          │  │  item.pb.go
│          │  │
│          │  └─itemservice
│          │          client.go
│          │          invoker.go
│          │          itemservice.go
│          │          server.go
│          │
│          └─stock
│              │  stock.pb.fast.go
│              │  stock.pb.go
│              │
│              └─stockservice
│                      client.go
│                      invoker.go
│                      server.go
│                      stockservice.go
│
└─rpc
    ├─item
    │  │  build.sh    // 用来编译的脚本，一般情况下不需要更改
    │  │  handler.go   // 服务端的业务逻辑都放在这里，这也是我们需要更改和编写的文件
    │  │  kitex_info.yaml
    │  │  main.go  // 服务启动函数，一般在这里做一些资源初始化的工作，可以更改
    │  │
    │  └─script
    │          bootstrap.sh
    │
    └─stock
        │  build.sh
        │  handler.go
        │  kitex_info.yaml
        │  main.go
        │
        └─script
                bootstrap.sh

```

## 拉取依赖
完成代码生成后，我们回到项目根目录。 使用 go mod tidy 命令拉取项目依赖
## 编写商品服务逻辑
我们需要编写的服务端逻辑都在 handler.go 这个文件中，目前我们有两个服务，对应了两个 handler.go，他们的结构都是类似的，我们先看看商品服务的服务端逻辑 rpc/item/handler.go

```go
package main

import (
	"context"
	item "example_shop/kitex_gen/example/shop/item"
)

// ItemServiceImpl implements the last service interface defined in the IDL.
type ItemServiceImpl struct{}

// GetItem implements the ItemServiceImpl interface.
func (s *ItemServiceImpl) GetItem(ctx context.Context, req *item.GetItemReq) (resp *item.GetItemResp, err error) {
	// TODO: Your code here...
	return
}
```
这里的 GetItem 函数就对应了我们之前在 item.thrift IDL 中定义的 GetItem 方法。

现在让我们修改一下服务端逻辑，本项目仅仅演示使用方法，重点不在于业务逻辑，故简单处理后返回。
```go
package main

import (
	"context"
	item "mykitex/kitex_gen/example/shop/item"
)

// ItemServiceImpl implements the last service interface defined in the IDL.
type ItemServiceImpl struct{}

// GetItem implements the ItemServiceImpl interface.
func (s *ItemServiceImpl) GetItem(ctx context.Context, req *item.GetItemReq) (resp *item.GetItemResp, err error) {
	resp = &item.GetItemResp{}
	resp.Item = &item.Item{}
	resp.Item.Id = req.GetId()
	resp.Item.Title = "Kitex"
	resp.Item.Description = "Kitex is an excellent framework!"
	return
}

```
除了 handler.go 外，我们还需关心 main.go 文件，我可以看看 main.go 中做了什么事情：
>rpc/item/main.go
```go
package main

import (
	"log"
	item "mykitex/kitex_gen/example/shop/item/itemservice"
)

func main() {
	svr := item.NewServer(new(ItemServiceImpl))

	err := svr.Run()

	if err != nil {
		log.Println(err.Error())
	}
}
```

### 运行商品服务
```shell
2024/03/01 19:36:03.685752 server.go:83: [Info] KITEX: server listen at addr=[::]:8888

```

在上面的日志输出中，addr=[::]:8888 代表我们的服务运行在本地的 8888 端口，此参数可以在创建 server 时传入 option 配置来修改，更多服务端配置见 Server Option。

## 创建 client
在生成的代码中，kitex_gen 目录下，Kitex 已经为我们封装了创建客户端的代码，我们只需要使用即可.
>client/client.go
```go
package main

import (
	"context"
	"github.com/cloudwego/kitex/client"
	"log"
	"mykitex/kitex_gen/example/shop/item"
	"mykitex/kitex_gen/example/shop/item/itemservice"
	"time"
)

func main() {
	client, err := itemservice.NewClient("hello", client.WithHostPorts("0.0.0.0:8888"))
	if err != nil {
		log.Fatal(err)
	}
	for {
		req := &item.GetItemReq{Id: 1}
		resp, err := client.GetItem(context.Background(), req)
		if err != nil {
			log.Fatal(err)
		}
		log.Println(resp)
		time.Sleep(time.Second)
	}
}

```
我们上述代码直接调用我们kitex工具自动生成的代码，

## 暴露 HTTP 接口
你可以使用 net/http 或其他框架来对外提供 HTTP 接口，此处使用 Hertz 做一个简单演示，有关 Hertz 用法参见 Hertz 文档

完整代码如下：
>main.go
```go
package main

import (
	"context"
	"mykitex/kitex_gen/example/shop/item"

	"github.com/cloudwego/hertz/pkg/app"
	"github.com/cloudwego/hertz/pkg/app/server"
	"github.com/cloudwego/kitex/client"
	"github.com/cloudwego/kitex/client/callopt"
	"log"
	"mykitex/kitex_gen/example/shop/item/itemservice"
	"time"
)

var (
	cli itemservice.Client
)

func main() {
	c, err := itemservice.NewClient("example.shop.item", client.WithHostPorts("0.0.0.0:8888"))
	if err != nil {
		log.Fatal(err)
	}
	cli = c

	hz := server.New(server.WithHostPorts("localhost:8889"))

	hz.GET("/api/item", Handler)

	if err := hz.Run(); err != nil {
		log.Fatal(err)
	}
}

func Handler(ctx context.Context, c *app.RequestContext) {
	req := &item.GetItemReq{Id: 1}
	req.Id = 1024
	resp, err := cli.GetItem(context.Background(), req, callopt.WithRPCTimeout(3*time.Second))
	if err != nil {
		log.Fatal(err)
	}

	c.String(200, resp.String())
}

```

接下来另启一个终端，执行 go run . 命令即可启动 API 服务，监听 8889 端口，请求 localhost:8889/api/item 即可发起 RPC 调用商品服务提供的 GetItem 接口，并获取到响应结果。

### 测试接口
打开游览器访问 localhost:8889/api/item，看到如下信息，代表请求成功。
>item:{id:1024 title:"Kitex" description:"Kitex is an excellent framework!"}
