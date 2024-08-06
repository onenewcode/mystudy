# WebAssembly 概念

WebAssembly 是一种运行在现代网络浏览器中的新型代码，并且提供新的性能特性和效果。它设计的目的不是为了手写代码而是为诸如 C、C++和 Rust 等低级源语言提供一个高效的编译目标。

对于网络平台而言，这具有巨大的意义——这为客户端 app 提供了一种在网络平台以接近本地速度的方式运行多种语言编写的代码的方式；在这之前，客户端 app 是不可能做到的。

**优点**
- 性能高：WASM被设计为一种高效的字节码格式，这意味着它可以非常快地加载和解析，并且可以在不牺牲性能的情况下运行计算密集型任务。
- 跨平台：WASM代码可以在各种操作系统和设备上运行，包括桌面应用程序、移动应用程序和Web应用程序。
- 更好的开发体验：开发人员可以使用他们熟悉的编程语言来编写高性能的Web应用程序。
**缺点**
- 学习成本高：WASM需要更多的学习和理解，因为它涉及到底层字节码和虚拟机的概念。
- 在某些情况下，可能不如JavaScript灵活：虽然WASM性能更高，但是在某些情况下，JavaScript可能更加灵活，因为它可以编写更动态的代码。

# 编译 Rust 为 WebAssembly
## 安装 Rust 环境
可以参考这篇文章

## wasm-pack
要构建我们的包，我们需要一个额外工具 wasm-pack。它会帮助我们把我们的代码编译成 WebAssembly 并制造出正确的 npm 包。使用下面的命令可以下载并安装它：
wasm-pack 使用另一个工具 wasm-bindgen 来提供 JavaScript 和 Rust 类型之间的桥梁。它允许 JavaScript 使用字符串调用 Rust API，或调用 Rust 函数来捕获 JavaScript 异常。
```rs
cargo install wasm-pack
```

## 构建WebAssembly npm 包
创建一个新的 Rust 包吧。打开你用来存放你私人项目的目录，做这些事：
```shell
cargo new --lib hello-wasm
```

这里会在名为 hello-wasm 的子目录里创建一个新的库，里面有下一步之前你所需要的一切：
```shell
+-- Cargo.toml
+-- src
    +-- lib.rs
```

首先，我们有一个 Cargo.toml 文件，这是我们配置构建的方式。如果你用过 Bundler 的 Gemfile 或者 npm 的 package.json，你应该会感到很熟悉。Cargo 的用法和它们类似。


## Rust
让我们在 src/lib.rs 写一些代码替换掉原来的：
```rs
// 引入外部库
extern crate wasm_bindgen;
// 引入 wasm_bindgen::prelude的全部模块
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
extern {
    pub fn alert(s: &str);
}

#[wasm_bindgen]
pub fn greet(name: &str) {
    alert(&format!("Hello, {}!", name));
}
```
### 调用来自 JavaScript 的外部函数
```rs
#[wasm_bindgen]
extern {
    pub fn alert(s: &str);
}
```
在 #[] 中的内容叫做 "属性"，并以某种方式改变下面的语句。这个属性告诉我们 "wasm-bindgen 知道如何找到这些函数"。
### JavaScript 中调用的 Rust 函数
```rs
#[wasm_bindgen]
pub fn greet(name: &str) {
    alert(&format!("Hello, {}!", name));
}
```
我们又看到了 #[wasm_bindgen] 属性。在这里，它并非定义一个 extern 块，而是 fn，这代表我们希望能够在 JavaScript 中使用这个 Rust 函数。这和 extern 正相反：我们并非引入函数，而是要把函数给外部世界使用。

这个函数的名字是 greet，它需要一个参数，一个字符串（写作 &str）。它调用了我们前面在 extern 块中引入的 alert 函数。它传递了一个让我们串联字符串的 format! 宏的调用。

## 编译
为了能够正确的编译我们的代码，首先我们需要配置 Cargo.toml。打开这个文件，将内容改为如下所示：
```toml
[package]
name = "hello-wasm"
version = "0.1.0"
authors = ["Your Name <you@example.com>"]
description = "A sample project with wasm-pack"
license = "MIT/Apache-2.0"
repository = "https://github.com/yourgithubusername/hello-wasm"

[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"
```
### 构建包
现在我们已经完成了所有配置项，开始构建吧！在命令行输入以下命令：
```shell
wasm-pack build --scope mynpmusername

```
wasm-pack build 将做以下几件事：
- 将你的 Rust 代码编译成 WebAssembly。
- 在编译好的 WebAssembly 代码基础上运行 wasm-bindgen，生成一个 JavaScript 文件将 WebAssembly 文件包装成一个模块以便 npm 能够识别它。
- 创建一个 pkg 文件夹并将 JavaScript 文件和生成的 WebAssembly 代码移到其中。
- 读取你的 Cargo.toml 并生成相应的 package.json。
- 复制你的 README.md (如果有的话) 到文件夹中。