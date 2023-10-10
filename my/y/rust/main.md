# 坑
## 交叉编译
ming64 必须是seh，版本未13 网址 https://github.com/niXman/mingw-builds-binaries/releases
# 基础
## 变量
### 遮蔽变量 
mut 变量的使用是不同的，第二个 let 生成了完全不同的新变量，两个变量只是恰好拥有同样的名称，涉及一次内存对象的再分配 ，而 mut 声明的变量，可以修改同一个内存地址上的值，并不会发生内存对象的再分配，性能要更好。
```rs
fn main() {
    let x = 5;
    // 在main函数的作用域内对之前的x进行遮蔽
    let x = x + 1;

    {
        // 在当前的花括号作用域内，对之前的x进行遮蔽
        let x = x * 2;
        println!("The value of x in the inner scope is: {}", x);
    }

    println!("The value of x is: {}", x);
}
```
## 基本类型
### 整数类型
在当使用 --release 参数进行 release 模式构建时，Rust 不检测溢出。相反，当检测到整型溢出时，Rust 会按照补码循环溢出（two’s complement wrapping）的规则处理。简而言之，大于该类型最大值的数值会被补码转换成该类型能够支持的对应数字的最小值。比如在 u8 的情况下，256 变成 0，257 变成 1，依此类推。程序不会 panic，但是该变量的值可能不是你期望的值。依赖这种默认行为的代码都应该被认为是错误的代码。

- 使用 wrapping_* 方法在所有模式下都按照补码循环溢出规则处理，例如 wrapping_add
- 如果使用 checked_* 方法时发生溢出，则返回 None 值
- 使用 overflowing_* 方法返回该值和一个指示是否存在溢出的布尔值
- 使用 saturating_* 方法使值达到最小值或最大值
```rs
fn main() {
    let a : u8 = 255;
    let b = a.wrapping_add(20);
    println!("{}", b);  // 19
}
```
### 浮点类型
浮点数往往是你想要数字的近似表达 浮点数类型是基于二进制实现的，但是我们想要计算的数字往往是基于十进制，例如 0.1 在二进制上并不存在精确的表达形式，但是在十进制上就存在。这种不匹配性导致一定的歧义性，更多的，虽然浮点数能代表真实的数值，但是由于底层格式问题，它往往受限于定长的浮点数精度，如果你想要表达完全精准的真实数字，只有使用无限精度的浮点数才行

浮点数在某些特性上是反直觉的 例如大家都会觉得浮点数可以进行比较,是的，它们确实可以使用 >，>= 等进行比较，但是在某些场景下，这种直觉上的比较特性反而会害了你。因为 f32 ， f64 上的比较运算实现的是 std::cmp::PartialEq 特征(类似其他语言的接口)，但是并没有实现 std::cmp::Eq 特征，但是后者在其它数值类型上都有定义
```rs
fn main() {
  // 断言0.1 + 0.2与0.3相等
  assert!(0.1 + 0.2 == 0.3);
}
```
你可能以为，这段代码没啥问题吧，实际上它会 panic(程序崩溃，抛出异常)，因为二进制精度问题，导致了 0.1 + 0.2 并不严格等于 0.3，它们可能在小数点 N 位后存在误差。
### 有理数和复数

Rust 的标准库相比其它语言，准入门槛较高，因此有理数和复数并未包含在标准库中：
    - 有理数和复数
    - 任意大小的整数和任意精度的浮点数
    - 固定精度的十进制小数，常用于货币相关的场景
好在社区已经开发出高质量的 Rust 数值库：num。

### 字符
注意，我们还没开始讲字符串，但是这里提前说一下，和一些语言不同，Rust 的字符只能用 '' 来表示， "" 是留给字符串的。
```rs
fn main() {
    let c = 'z';
    let z = 'ℤ';
    let g = '国';
    let heart_eyed_cat = '😻';
}
```

### 单元类型
 main 函数就返回这个单元类型 ()，你不能说 main 函数无返回值，因为没有返回值的函数在 Rust 中是有单独的定义的：发散函数( diverge function )，顾名思义，无法收敛的函数。

例如常见的 println!() 的返回值也是单元类型 ()。

再比如，你可以用 () 作为 map 的值，表示我们不关注具体的值，只关注 key。 这种用法和 Go 语言的 struct{} 类似，可以作为一个值用来占位，但是完全不占用任何内存。
### 语句

## 所有权和借用
### 所有权原则
- Rust 中每一个值都被一个变量所拥有，该变量被称为值的所有者
- 一个值同时只能被一个变量所拥有，或者说一个值只能拥有一个所有者
- 当所有者(变量)离开作用域范围时，这个值将被丢弃(drop)

### 变量绑定背后的数据交互
```rs
let s1 = String::from("hello");
let s2 = s1;

```
实际上， String 类型是一个复杂类型，由存储在栈中的堆指针、字符串长度、字符串容量共同组成，其中堆指针是最重要的，它指向了真实存储字符串内容的堆内存，至于长度和容量，如果你有 Go 语言的经验，这里就很好理解：容量是堆内存分配空间的大小，长度是目前已经使用的大小。
```rs
let s1 = String::from("hello");
let s2 = s1;

println!("{}, world!", s1);

```
- Rust 中每一个值都被一个变量所拥有，该变量被称为值的所有者
- 一个值同时只能被一个变量所拥有，或者说一个值只能拥有一个所有者
- 当所有者(变量)离开作用域范围时，这个值将被丢弃(drop)
### 函数传值与返回
```rs
fn main() {
    let s = String::from("hello");  // s 进入作用域

    takes_ownership(s);             // s 的值移动到函数里 ...
                                    // ... 所以到这里不再有效

    let x = 5;                      // x 进入作用域

    makes_copy(x);                  // x 应该移动函数里，
                                    // 但 i32 是 Copy 的，所以在后面可继续使用 x

} // 这里, x 先移出了作用域，然后是 s。但因为 s 的值已被移走，
  // 所以不会有特殊操作

fn takes_ownership(some_string: String) { // some_string 进入作用域
    println!("{}", some_string);
} // 这里，some_string 移出作用域并调用 `drop` 方法。占用的内存被释放

fn makes_copy(some_integer: i32) { // some_integer 进入作用域
    println!("{}", some_integer);
} // 这里，some_integer 移出作用域。不会有特殊操作
```
####  引用与借用
不过可变引用并不是随心所欲、想用就用的，它有一个很大的限制： 同一作用域，特定数据只能有一个可变引用：

可变引用与不可变引用不能同时存在
```rs
let mut s = String::from("hello");

let r1 = &s; // 没问题
let r2 = &s; // 没问题
let r3 = &mut s; // 大问题

println!("{}, {}, and {}", r1, r2, r3);

```

**悬垂引用(Dangling References)**
```rs

fn main() {
    let reference_to_nothing = dangle();
}

fn dangle() -> &String {
    let s = String::from("hello");

    &s
}
```

## 复合类型
### 字符串
#### 切片(slice)
切片并不是 Rust 独有的概念，在 Go 语言中就非常流行，它允许你引用集合中部分连续的元素序列，而不是引用整个集合。
```rs
let s = String::from("hello world");

let hello = &s[0..5];
let world = &s[6..11];

```
### 元组
```rs
fn main() {
    let tup: (i32, f64, u8) = (500, 6.4, 1);
}
```
### 结构体
```rs

// 最简
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}
fn main() {
    let u1 = User {
        email: String::from("someone@example.com"),
        username: String::from("sunface"),
        active: true,
        sign_in_count: 1,
    };

    let u2 = set_email(u1);
} 

fn set_email(u: User) -> User {
    User {
        email: String::from("contact@im.dev"),
        ..u
    
    }
}

```

```rs
// 我们可以使用 #[derive(Debug)] 让结构体变成可打印的.
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

fn main() {
    let scale = 2;
    let rect1 = Rectangle {
        width: dbg!(30 * scale), // print debug info to stderr and assign the value of  `30 * scale` to `width`
        height: 50,
    };

    dbg!(&rect1); // print debug info to stderr

    println!("{:?}", rect1); // print debug info to stdout
}
```
### 枚举
<!-- 枚举变体可以通过“as”转换为整数 -->
```rs
enum PokerSuit {
  Clubs,
  Spades,
  Diamonds,
  Hearts,
}
```

```RS
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::Move { x: 1, y: 1 };  // 创建一个Move变体的Message枚举实例，包含x和y字段的值
// 你使用if let语法来进行模式匹配。如果msg是Message::Move变体，并将其解构为x: a和y: b，那么就进入if条件分支。此
    if let Message::Move { x: a, y: b } = msg {
        // 使用模式匹配解构Message枚举
        // 如果msg是Move变体，并将x和y字段解构为a和b变量
        // 进入if条件分支
        assert_eq!(a, b);
    } else {
        panic!("NEVER LET THIS RUN！");
    }
}
```

处理空值
```RS
fn main() {
    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);

    if let Some(n) = six {
        println!("{}", n);
        return
    } 
    
    panic!("NEVER LET THIS RUN！");
} 

fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}
```
### 数组

## 流程控制
### if else
```rs
fn main() {
    let n = 6;

    if n % 4 == 0 {
        println!("number is divisible by 4");
    } else if n % 3 == 0 {
        println!("number is divisible by 3");
    } else if n % 2 == 0 {
        println!("number is divisible by 2");
    } else {
        println!("number is not divisible by 4, 3, or 2");
    }
}
```
### for
|使用方法|	等价使用方式|	所有权|
|------|-------|-------|
|for item in collection	|for item in IntoIterator::into_iter(collection)	|转移所有权|
|for item in &collection	|for item in collection.iter()|	不可变借用|
|for item in &mut collection	|for item in collection.iter_mut()|	可变借用|

在循环获取元素
```rs
fn main() {
    let a = [4, 3, 2, 1];
    // `.iter()` 方法把 `a` 数组变成一个迭代器
    for (i, v) in a.iter().enumerate() {
        println!("第{}个元素是{}", i + 1, v);
    }
}
```
### loop 循环
```rs
fn main() {
    loop {
        println!("again!");
    }
}
```
## 模式匹配
### match 和 if let
#### match
```rs
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny =>  {
            println!("Lucky penny!");
            1
        },
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}

```

绑定匹配

```rs
enum Action {
    Say(String),
    MoveTo(i32, i32),
    ChangeColorRGB(u16, u16, u16),
}

fn main() {
    let actions = [
        Action::Say("Hello Rust".to_string()),
        Action::MoveTo(1,2),
        Action::ChangeColorRGB(255,255,0),
    ];
    for action in actions {
        match action {
            Action::Say(s) => {
                println!("{}", s);
            },
            Action::MoveTo(x, y) => {
                println!("point from (0, 0) move to ({}, {})", x, y);
            },
            Action::ChangeColorRGB(r, g, _) => {
                println!("change color into '(r:{}, g:{}, b:0)', 'b' has been ignored",
                    r, g,
                );
            }
        }
    }
}
```

```rs
v.iter().filter(|x| matches!(x, MyEnum::Foo));
```

#### if let 匹配
```rs
if let Some(3) = v {
    println!("three");
}

```
### 解构 Option
```rs
enum Option<T> {
    Some(T),
    None,
}

```
### 模式适用场景
模式是 Rust 中的特殊语法，它用来匹配类型中的结构和数据，它往往和 match 表达式联用，以实现强大的模式匹配能力。模式一般由以下内容组合而成：
    - 字面值
    - 解构的数组、枚举、结构体或者元组
    - 变量
    - 通配符
    - 占位符
### 全模式列表
####      解构结构体
```rs
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7 };

    let Point { x: a, y: b } = p;
    assert_eq!(0, a);
    assert_eq!(7, b);
}



fn main() {
    let p = Point { x: 0, y: 7 };

    match p {
        Point { x, y: 0 } => println!("On the x axis at {}", x),
        Point { x: 0, y } => println!("On the y axis at {}", y),
        Point { x, y } => println!("On neither axis: ({}, {})", x, y),
    }
}



enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::ChangeColor(0, 160, 255);

    match msg {
        Message::Quit => {
            println!("The Quit variant has no data to destructure.")
        }
        Message::Move { x, y } => {
            println!(
                "Move in the x direction {} and in the y direction {}",
                x,
                y
            );
        }
        Message::Write(text) => println!("Text message: {}", text),
        Message::ChangeColor(r, g, b) => {
            println!(
                "Change the color to red {}, green {}, and blue {}",
                r,
                g,
                b
            )
        }
    }
}




enum Color {
   Rgb(i32, i32, i32),
   Hsv(i32, i32, i32),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(Color),
}

fn main() {
    let msg = Message::ChangeColor(Color::Hsv(0, 160, 255));

    match msg {
        Message::ChangeColor(Color::Rgb(r, g, b)) => {
            println!(
                "Change the color to red {}, green {}, and blue {}",
                r,
                g,
                b
            )
        }
        Message::ChangeColor(Color::Hsv(h, s, v)) => {
            println!(
                "Change the color to hue {}, saturation {}, and value {}",
                h,
                s,
                v
            )
        }
        _ => ()
    }
}
```

### @前绑定后解构(Rust 1.56 新增)
```rs
#[derive(Debug)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    // 绑定新变量 `p`，同时对 `Point` 进行解构
    let p @ Point {x: px, y: py } = Point {x: 10, y: 23};
    println!("x: {}, y: {}", px, py);
    println!("{:?}", p);


    let point = Point {x: 10, y: 5};
    if let p @ Point {x: 10, y} = point {
        println!("x is 10 and y is {} in {:?}", y, p);
    } else {
        println!("x was not 10 :(");
    }
}
```
## 方法
定义方法
- self 表示 Rectangle 的所有权转移到该方法中，这种形式用的较少
- &self 表示该方法对 Rectangle 的不可变借用
- &mut self 表示可变借用(域内对可变数据进行临时修改的机制)
```rs
struct Circle {
    x: f64,
    y: f64,
    radius: f64,
}

impl Circle {
    // new是Circle的关联函数，因为它的第一个参数不是self，且new并不是关键字
    // 这种方法往往用于初始化当前结构体的实例
    fn new(x: f64, y: f64, radius: f64) -> Circle {
        Circle {
            x: x,
            y: y,
            radius: radius,
        }
    }

    // Circle的方法，&self表示借用当前的Circle结构体
    fn area(&self) -> f64 {
        std::f64::consts::PI * (self.radius * self.radius)
    }
}
```

### 为枚举实现方法
```rs
#![allow(unused)]
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

impl Message {
    fn call(&self) {
        // 在这里定义方法体
    }
}

fn main() {
    let m = Message::Write(String::from("hello"));
    m.call();
}

```
##  泛型和特征
### 泛型 Generics
```rs
fn display_array<T: std::fmt::Debug>(arr: &[T]) {
    println!("{:?}", arr);
}
fn main() {
    let arr: [i32; 3] = [1, 2, 3];
    display_array(&arr);

    let arr: [i32;2] = [1,2];
    display_array(&arr);
}
```
####  const
```rs
fn display_array<T: std::fmt::Debug, const N: usize>(arr: [T; N]) {
    println!("{:?}", arr);
}
fn main() {
    let arr: [i32; 3] = [1, 2, 3];
    display_array(arr);

    let arr: [i32; 2] = [1, 2];
    display_array(arr);
}
```
如上所示，我们定义了一个类型为 [T; N] 的数组，其中 T 是一个基于类型的泛型参数，这个和之前讲的泛型没有区别，而重点在于 N 这个泛型参数，它是一个基于值的泛型参数！因为它用来替代的是数组的长度。
### 特征 Trait
```rs
pub trait Summary {
    fn summarize(&self) -> String;
}
pub struct Post {
    pub title: String, // 标题
    pub author: String, // 作者
    pub content: String, // 内容
}

impl Summary for Post {
    fn summarize(&self) -> String {
        format!("文章{}, 作者是{}", self.title, self.author)
    }
}

pub struct Weibo {
    pub username: String,
    pub content: String
}

impl Summary for Weibo {
    fn summarize(&self) -> String {
        format!("{}发表了微博{}", self.username, self.content)
    }
}
```

#### 特征定义与实现的位置(孤儿规则)
关于特征实现与定义的位置，有一条非常重要的原则：如果你想要为类型 A 实现特征 T，那么 A 或者 T 至少有一个是在当前作用域中定义的！
#### 使用特征作为函数参数
```rs
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}
```

impl Summary，只能说想出这个类型的人真的是起名鬼才，简直太贴切了，顾名思义，它的意思是 实现了Summary特征 的 item 参数。

你可以使用任何实现了 Summary 特征的类型作为该函数的参数，同时在函数体内，还可以调用该特征的方法，例如 summarize 方法。具体的说，可以传递 Post 或 Weibo 的实例来作为参数，而其它类如 String 或者 i32 的类型则不能用做该函数的参数，因为它们没有实现 Summary 特征。

#### 特征约束(trait bound)
```rs
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

pub fn notify(item: &(impl Summary + Display)) {}


pub fn notify<T: Summary + Display>(item: &T) {}


fn some_function<T, U>(t: &T, u: &U) -> i32
    where T: Display + Clone,
          U: Clone + Debug
{}




use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self {
            x,
            y,
        }
    }
}

impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("The largest member is x = {}", self.x);
        } else {
            println!("The largest member is y = {}", self.y);
        }
    }
}
```
#### 函数返回中的 impl Trait
```rs
fn returns_summarizable() -> impl Summary {
    Weibo {
        username: String::from("sunface"),
        content: String::from(
            "m1 max太厉害了，电脑再也不会卡",
        )
    }
}
```
#### 通过 derive 派生特征
形如 #[derive(Debug)] 的代码已经出现了很多次，这种是一种特征派生语法，被 derive 标记的对象会自动实现对应的默认特征代码，继承相应的功能。

例如 Debug 特征，它有一套自动实现的默认代码，当你给一个结构体标记后，就可以使用 println!("{:?}", s) 的形式打印该结构体的对象。

再如 Copy 特征，它也有一套自动实现的默认代码，当标记到一个类型上时，可以让这个类型自动实现 Copy 特征，进而可以调用 copy 方法，进行自我复制。

总之，derive 派生出来的是 Rust 默认给我们提供的特征，在开发过程中极大的简化了自己手动实现相应特征的需求，当然，如果你有特殊的需求，还可以自己手动重载该实现。

#### 调用方法需要引入特征
```rs
use std::convert::TryInto;

fn main() {
  let a: i32 = 10;
  let b: u16 = 100;

  let b_ = b.try_into()
            .unwrap();

  if a < b_ {
    println!("Ten is less than one hundred.");
  }
}
```

### 特征对象
```rs
pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self) {
        // 绘制按钮的代码
    }
}

struct SelectBox {
    width: u32,
    height: u32,
    options: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        // 绘制SelectBox的代码
    }
}



```
### 深入了解特征

## 集合类型
### 动态数组 Vector

### KV 存储 HashMap
```rs
use std::collections::HashMap;

// 创建一个HashMap，用于存储宝石种类和对应的数量
let mut my_gems = HashMap::new();

// 将宝石类型和对应的数量写入表中
my_gems.insert("红宝石", 1);
my_gems.insert("蓝宝石", 2);
my_gems.insert("河边捡的误以为是宝石的破石头", 18);






fn main() {
    use std::collections::HashMap;

    let teams_list = vec![
        ("中国队".to_string(), 100),
        ("美国队".to_string(), 10),
        ("日本队".to_string(), 50),
    ];

    let teams_map: HashMap<_,_> = teams_list.into_iter().collect();
    
    println!("{:?}",teams_map)
}


fn main() {
    use std::collections::HashMap;

    let mut scores = HashMap::new();

    scores.insert("Blue", 10);

    // 覆盖已有的值
    let old = scores.insert("Blue", 20);
    assert_eq!(old, Some(10));

    // 查询新插入的值
    let new = scores.get("Blue");
    assert_eq!(new, Some(&20));

    // 查询Yellow对应的值，若不存在则插入新值
    let v = scores.entry("Yellow").or_insert(5);
    assert_eq!(*v, 5); // 不存在，插入5

    // 查询Yellow对应的值，若不存在则插入新值
    let v = scores.entry("Yellow").or_insert(50);
    assert_eq!(*v, 5); // 已经存在，因此50没有插入
}
```
## 认识生命周期
在存在多个引用时，编译器有时会无法自动推导生命周期，此时就需要我们手动去标注，通过为参数标注合适的生命周期来帮助编译器进行借用检查的分析。

```rs
{
    let r;

    {
        let x = 5;
        r = &x;
    }

    println!("r: {}", r);
}
```
- let r; 的声明方式貌似存在使用 null 的风险，实际上，当我们不初始化它就使用时，编译器会给予报错
- r 引用了内部花括号中的 x 变量，但是 x 会在内部花括号 \} 处被释放，因此回到外部花括号后，r 会引用一个无效的 x

&i32        // 一个引用
&'a i32     // 具有显式生命周期的引用
&'a mut i32 // 具有显式生命周期的可变引用


```rs
fn main() {
    let string1 = String::from("abcd");
    let string2 = "xyz";

    let result = longest(string1.as_str(), string2);
    println!("The longest string is {}", result);
}


// 在存在多个引用时，编译器有时会无法自动推导生命周期，此时就需要我们手动去标注，通过为参数标注合适的生命周期来帮助编译器进行借用检查的分析。
fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// 正确代码
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

```
错误代码会出现下面的报错
```cmd
  --> main.rs:11:33
   |
11 | fn longest(x: &str, y: &str) -> &str {
   |               ----     ----     ^ expected named lifetime parameter
   |
   = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `x` or `y`
help: consider introducing a named lifetime parameter
   |
11 | fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
   |           ++++     ++          ++          ++
```

### 结构体中的生命周期
```rs
struct ImportantExcerpt<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().expect("Could not find a '.'");
    let i = ImportantExcerpt {
        part: first_sentence,
    };
}
```
该生命周期标注说明，结构体 ImportantExcerpt 所引用的字符串 str 必须比该结构体活得更久。
### 生命周期消除
- 每一个引用参数都会获得独自的生命周期

例如一个引用参数的函数就有一个生命周期标注: fn foo<'a>(x: &'a i32)，两个引用参数的有两个生命周期标注:fn foo<'a, 'b>(x: &'a i32, y: &'b i32), 依此类推。

- 若只有一个输入生命周期(函数参数中只有一个引用类型)，那么该生命周期会被赋给所有的输出生命周期，也就是所有返回值的生命周期都等于该输入生命周期

例如函数 fn foo(x: &i32) -> &i32，x 参数的生命周期会被自动赋给返回值 &i32，因此该函数等同于 fn foo<'a>(x: &'a i32) -> &'a i32

- 若存在多个输入生命周期，且其中一个是 &self 或 &mut self，则 &self 的生命周期被赋给所有的输出生命周期
拥有 &self 形式的参数，说明该函数是一个 方法，该规则让方法的使用便利度大幅提升。
```rs
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }
}
```
- impl 中必须使用结构体的完整名称，包括 <'a>，因为生命周期标注也是结构体类型的一部分！
- 方法签名中，往往不需要标注生命周期，得益于生命周期消除的第一和第三规则

## 返回值和错误处理
### panic 深入剖析
#### 主动调用
```rs
fn main() {
    panic!("crash and burn");
}
```
#### backtrace 栈展开

#### panic 时的两种终止方式
当出现 panic! 时，程序提供了两种方式来处理终止流程：栈展开和直接终止

#### 何时该使用 panic!
先来一点背景知识，在前面章节我们粗略讲过 Result<T, E> 这个枚举类型，它是用来表示函数的返回结果：
```rs
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```
当没有错误发生时，函数返回一个用 Result 类型包裹的值 Ok(T)，当错误时，返回一个 Err(E)。对于 Result 返回我们有很多处理方法，最简单粗暴的就是 unwrap 和 expect，这两个函数非常类似，我们以 unwrap 举例：
```rs
use std::net::IpAddr;
let home: IpAddr = "127.0.0.1".parse().unwrap();
```


### 可恢复的错误 Result
```rs
use std::fs::File;
use std::io::ErrorKind;

fn main() {
    let f = File::open("hello.txt");

    let f = match f {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,
                Err(e) => panic!("Problem creating the file: {:?}", e),
            },
            other_error => panic!("Problem opening the file: {:?}", other_error),
        },
    };
}
```
expect 跟 unwrap 很像，也是遇到错误直接 panic, 但是会带上自定义的错误提示信息，相当于重载了错误打印的函数：
```rs
use std::fs::File;

fn main() {
    let f = File::open("hello.txt").expect("Failed to open hello.txt");
}



use std::fs::File;
use std::io;
use std::io::Read;

fn read_username_from_file() -> Result<String, io::Error> {
    let mut s = String::new()

    File::open("hello.txt")?.read_to_string(&mut s)?;

    Ok(s)
}

```
## 包和模块
### 包和 Crate
#### 包 Crate

对于 Rust 而言，包是一个独立的可编译单元，它编译后会生成一个可执行文件或者一个库。

一个包会将相关联的功能打包在一起，使得该功能可以很方便的在多个项目中分享。例如标准库中没有提供但是在三方库中提供的 rand 包，它提供了随机数生成的功能，我们只需要将该包通过 use rand; 引入到当前项目的作用域中，就可以在项目中使用 rand 的功能：rand::XXX。
#### 项目 Package
由于 Package 就是一个项目，因此它包含有独立的 Cargo.toml 文件，以及因为功能性被组织在一起的一个或多个包。一个 Package 只能包含一个库(library)类型的包，但是可以包含多个二进制可执行类型的包。


只要你牢记 Package 是一个项目工程，而包只是一个编译单元，基本上也就不会混淆这个两个概念了：src/main.rs 和 src/lib.rs 都是编译单元，因此它们都是包。


### 模块 Module
```rs
// 餐厅前厅，用于吃饭
mod front_of_house {
    mod hosting {
        fn add_to_waitlist() {}

        fn seat_at_table() {}
    }

    mod serving {
        fn take_order() {}

        fn serve_order() {}

        fn take_payment() {}
    }
}
```
- 使用 mod 关键字来创建新模块，后面紧跟着模块名称
- 模块可以嵌套，这里嵌套的原因是招待客人和服务都发生在前厅，因此我们的代码模拟了真实场景
- 模块中可以定义各种 Rust 类型，例如函数、结构体、枚举、特征等
- 所有模块均定义在同一个文件中
### 使用 use 及受限可见性

## 注释和文档
### 文档注释
cargo doc --open

Rust 提供了 cargo doc 的命令，可以用于把这些文档注释转换成 HTML 网页文件，最终展示给用户浏览，这样用户就知道这个包是做什么的以及该如何使用。

```rs
/// `add_one` 将指定值加1
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}

```
- 文档注释需要位于 lib 类型的包中，例如 src/lib.rs 中
- 文档注释可以使用 markdown语法！例如 # Examples 的标题，以及代码块高亮
- 被注释的对象需要使用 pub 对外可见，记住：文档注释是给用户看的，内部实现细节不应该被暴露出去
### 文档测试(Doc Test)
```rs
/// `add_one` 将指定值加1
///
/// # Examples11
///
/// ```
/// let arg = 5;
/// let answer = world_hello::compute::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}

```
以上的注释不仅仅是文档，还可以作为单元测试的用例运行，使用 cargo test 运行测试：

## 格式化输出


 # 自动化测试
## 编写测试及控制执行
### 测试函数
当使用 Cargo 创建一个 lib 类型的包时，它会为我们自动生成一个测试模块。先来创建一个 lib 类型的 adder 包：
```cmd
$ cargo new adder --lib
     Created library `adder` project 
$ cd adder
```
**cargo test可以执行包下面全部的测试**
创建成功后，在 src/lib.rs 文件中可以发现如下代码:
```rs
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
```
### 自定义失败信息
```rs
pub fn greeting(name: &str) -> String {
    format!("Hello {}!", name)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn greeting_contains_name() {
    let result = greeting("Sunface");
    let target = "孙飞";
    assert!(
        result.contains(target),
        "你的问候中并没有包含目标姓名 {} ，你的问候是 `{}`",
        target,
        result
    );
}

}

```
### 测试 panic
```rs
pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 || value > 100 {
            panic!("Guess value must be between 1 and 100, got {}.", value);
        }

        Guess { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic]
    fn greater_than_100() {
        Guess::new(200);
    }
}
```
### 测试panic
```rs
pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 || value > 100 {
            panic!("Guess value must be between 1 and 100, got {}.", value);
        }

        Guess { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic]
    fn greater_than_100() {
        Guess::new(200);
    }
}

```


```rs
// --snip--
impl Guess {
    pub fn new(value: i32) -> Guess {
        if value < 1 {
            panic!(
                "Guess value must be greater than or equal to 1, got {}.",
                value
            );
        } else if value > 100 {
            panic!(
                "Guess value must be less than or equal to 100, got {}.",
                value
            );
        }

        Guess { value }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "Guess value must be less than or equal to 100")]
    fn greater_than_100() {
        Guess::new(200);
    }
}
```
### 使用 Result<T, E>
```rs
#[cfg(test)]
mod tests {
    #[test]
    fn it_works() -> Result<(), String> {
        if 2 + 2 == 4 {
            Ok(())
        } else {
            Err(String::from("two plus two does not equal four"))
        }
    }
}

```
## 单元测试、集成测试
### 单元测试
条件编译 #[cfg(test)]
上面代码中的 #[cfg(test)] 标注可以告诉 Rust 只有在 cargo test 时才编译和运行模块 tests，其它时候当这段代码是空气即可，例如在 cargo build 时。这么做有几个好处：

### 集成测试
tests 目录
一个标准的 Rust 项目，在它的根目录下会有一个 tests 目录，大名鼎鼎的 ripgrep 也不能免俗。

# 进阶
## 生命周期
### 深入生命周期


## 函数式编程
### 闭包
```rs
use std::thread;
use std::time::Duration;

fn workout(intensity: u32, random_number: u32) {
    let action = || {
        println!("muuuu.....");
        thread::sleep(Duration::from_secs(2));
        intensity
    };

    if intensity < 25 {
        println!(
            "今天活力满满，先做 {} 个俯卧撑!",
            action()
        );
        println!(
            "旁边有妹子在看，俯卧撑太low，再来 {} 组卧推!",
            action()
        );
    } else if random_number == 3 {
        println!("昨天练过度了，今天还是休息下吧！");
    } else {
        println!(
            "昨天练过度了，今天干干有氧，跑步 {} 分钟!",
            action()
        );
    }
}

fn main() {
    // 动作次数
    let intensity = 10;
    // 随机值用来决定某个选择
    let random_number = 7;
FnOnce，该类型的闭包会拿走被捕获变量的所有权。Once 顾名思义，说明该闭包只能运行一次：
    // 开始健身
    workout(intensity, random_number);
}
```
#### 闭包的类型推导
```rs
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

#### 结构体中的闭包
```rs
struct Cacher<T>
where
    T: Fn(u32) -> u32,
{
    query: T,
    value: Option<u32>,
}
```
标准库提供的 Fn 系列特征，再结合特征约束，就能很好的解决了这个问题. T: Fn(u32) -> u32 意味着 query 的类型是 T，该类型必须实现了相应的闭包特征 Fn(u32) -> u32。从


#### 三种 Fn 特征
1. **FnOnce**，该类型的闭包会拿走被捕获变量的所有权。Once 顾名思义，说明该闭包只能运行一次：
```rs
fn fn_once<F>(func: F)
where
    F: FnOnce(usize) -> bool,
{
    println!("{}", func(3));
    println!("{}", func(4));
}

fn main() {
    let x = vec![1, 2, 3];
    fn_once(|z|{z == x.len()})
}
```
2. **FnMut**，它以可变借用的方式捕获了环境中的值，因此可以修改该值：
```rs
fn main() {
    let mut s = String::new();

    let update_string =  |str| s.push_str(str);
    update_string("hello");

    println!("{:?}",s);
}
```
3. **Fn** 特征，它以不可变借用的方式捕获环境中的值 让我们把上面的代码中 exec 的 F 泛型参数类型修改为 Fn(&'a str)：
```rs
fn main() {
    let mut s = String::new();

    let update_string =  |str| s.push_str(str);

    exec(update_string);

    println!("{:?}",s);
}

fn exec<'a, F: Fn(&'a str)>(mut f: F)  {
    f("hello")
}
```
### 迭代器 Iterator

## 深入类型
### 类型转换
```rs
let mut values: [i32; 2] = [1, 2];
let p1: *mut i32 = values.as_mut_ptr();
let first_address = p1 as usize; // 将p1内存地址转换为一个整数
let second_address = first_address + 4; // 4 == std::mem::size_of::<i32>()，i32类型占用4个字节，因此将内存地址 + 4
let p2 = second_address as *mut i32; // 访问该地址指向的下一个整数p2
unsafe {
    *p2 += 1;
}
assert_eq!(values[1], 3);

```
#### TryInto 转换
```rs
fn main() {
    let b: i16 = 1500;

    let b_: u8 = match b.try_into() {
        Ok(b1) => b1,
        Err(e) => {
            println!("{:?}", e.to_string());
            0
        }
    };
}
```
####  通用类型转换
```rs
struct Foo {
    x: u32,
    y: u16,
}

struct Bar {
    a: u32,
    b: u16,
}

fn reinterpret(foo: Foo) -> Bar {
    let Foo { x, y } = foo;
    Bar { a: x, b: y }
}
```
### newtype和类型名称

#### 类型别名(Type Alias)
type Meters = u32;

!永不返回类型
### Sized 和不定长类型 DST
### 整数转换为枚举

## 智能指针
### Box<T> 堆对象分配
因为 Box<T> 允许你将一个值分配到堆上，然后在栈上保留一个智能指针指向堆上的数据。

当栈上数据转移所有权时，实际上是把数据拷贝了一份，最终新旧变量各自拥有不同的数据，因此所有权并未转移。
```rs
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

Box 中还提供了一个非常有用的关联函数：Box::leak，它可以消费掉 Box 并且强制目标值从内存中泄漏，读者可能会觉得，这有啥用啊？
```rs
fn main() {
   let s = gen_static_str();
   println!("{}", s);
}

fn gen_static_str() -> &'static str{
    let mut s = String::new();
    s.push_str("hello, world");

    Box::leak(s.into_boxed_str())
}
```
### Deref 解引用
#### 为智能指针实现 Deref 特征
```rs
use std::ops::Deref;

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
```

### Drop 释放资源

### Rc 与 Arc
引用计数(reference counting)，顾名思义，通过记录一个数据被引用的次数来确定该数据是否正在被使用。当引用次数归零时，就代表该数据不再被使用，因此可以被清理释放。

Arc 是 Atomic Rc 的缩写，顾名思义：原子化的 Rc<T> 智能指针。原子化是一种并发原语，我们在后续章节会进行深入讲解，这里你只要知道它能保证我们的数据能够安全的在线程间共享即可。

### Cell 和 RefCell
Cell 和 RefCell 在功能上没有区别，区别在于 Cell<T> 适用于 T 实现 Copy 的情况

#### RefCell

|Rust 规则|	智能指针带来的额外规则|
|-------------|------------------|

|一个数据只有一个所有者|	Rc/Arc让一个数据可以拥有多个所有者|
要么多个不可变借用，要么一个可变借用|	RefCell实现编译期可变、不可变引用共存|
|违背规则导致编译错误	|违背规则导致运行时panic|

## 循环引用与自引用

### Weak
|Weak|	Rc|
|---------------|-----------------------|
|不计数	|引用计数|
|不拥有所有权	|拥有值的所有权|
|不阻止值被释放(drop)|	所有权计数归零，才能 drop|
|引用的值存在返回 Some，不存在返回 None|	引用的值必定存在|
|通过 upgrade 取到 Option<Rc<T>>，然后再取值|	通过 Deref 自动解引用，取值无需任何操作|

## 多线程并发编程
### 使用多线程
```rs
use std::thread;
use std::time::Duration;

fn main() {
    thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {} from the spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    for i in 1..5 {
        println!("hi number {} from the main thread!", i);
        thread::sleep(Duration::from_millis(1));
    }
}
```
有几点值得注意：

- 线程内部的代码使用闭包来执行
- main 线程一旦结束，程序就立刻结束，因此需要保持它的存活，直到其它子线程完成自己的任务
- thread::sleep 会让当前线程休眠指定的时间，随后其它线程会被调度运行，因此就算你的电脑只有一个 CPU 核心，该程序也会表现的如同多 CPU 核心一般，这就是并发！
#### 在线程闭包中使用 move
 move 关键字在闭包中的使用可以让该闭包拿走环境中某个值的所有权，同样地，你可以使用 move 来将所有权从一个线程转移到另外一个线程。
```rust
use std::thread;

fn main() {
    let v = vec![1, 2, 3];

    let handle = thread::spawn(move || {
        println!("Here's a vector: {:?}", v);
    });

    handle.join().unwrap();

    // 下面代码会报错borrow of moved value: `v`
    // println!("{:?}",v);
}
```
#### 线程局部变量(Thread Local Variable)
##### 标准库
```rust
use std::cell::RefCell;
use std::thread;

thread_local!(static FOO: RefCell<u32> = RefCell::new(1));

FOO.with(|f| {
    assert_eq!(*f.borrow(), 1);
    *f.borrow_mut() = 2;
});

// 每个线程开始时都会拿到线程局部变量的FOO的初始值
let t = thread::spawn(move|| {
    FOO.with(|f| {
        assert_eq!(*f.borrow(), 1);
        *f.borrow_mut() = 3;
    });
});

// 等待线程完成
t.join().unwrap();

// 尽管子线程中修改为了3，我们在这里依然拥有main线程中的局部值：2
FOO.with(|f| {
    assert_eq!(*f.borrow(), 2);
});

```
##### 第三方库
```rust
use thread_local::ThreadLocal;
use std::sync::Arc;
use std::cell::Cell;
use std::thread;

let tls = Arc::new(ThreadLocal::new());

// 创建多个线程
for _ in 0..5 {
    let tls2 = tls.clone();
    thread::spawn(move || {
        // 将计数器加1
        let cell = tls2.get_or(|| Cell::new(0));
        cell.set(cell.get() + 1);
    }).join().unwrap();
}

// 一旦所有子线程结束，收集它们的线程局部变量中的计数器值，然后进行求和
let tls = Arc::try_unwrap(tls).unwrap();
let total = tls.into_iter().fold(0, |x, y| x + y.get());

// 和为5
assert_eq!(total, 5);

```
### 线程间的消息传递
```rs
use std::sync::mpsc;
use std::thread;

fn main() {
    // 创建一个消息通道, 返回一个元组：(发送者，接收者)
    let (tx, rx) = mpsc::channel();

    // 创建线程，并发送消息
    thread::spawn(move || {
        // 发送一个数字1, send方法返回Result<T,E>，通过unwrap进行快速错误处理
        tx.send(1).unwrap();

        // 下面代码将报错，因为编译器自动推导出通道传递的值是i32类型，那么Option<i32>类型将产生不匹配错误
        // tx.send(Some(1)).unwrap()
    });

    // 在主线程中接收子线程发送的消息并输出
    println!("receive {}", rx.recv().unwrap());
}
```

- 若值的类型实现了Copy特征，则直接复制一份该值，然后传输过去，例如之前的i32类型
- 若值没有实现Copy，则它的所有权会被转移给接收端，在发送端继续使用该值将报错
#### 使用多发送者
```rs
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let tx1 = tx.clone();
    thread::spawn(move || {
        tx.send(String::from("hi from raw tx")).unwrap();
    });

    thread::spawn(move || {
        tx1.send(String::from("hi from cloned tx")).unwrap();
    });

    for received in rx {
        println!("Got: {}", received);
    }
}
```
以上代码并不复杂，但仍有几点需要注意：

- tx,rx对应发送者和接收者，它们的类型由编译器自动推导: tx.send(1)发送了整数，因此它们分别是mpsc::Sender<i32>和mpsc::Receiver<i32>类型，需要注意，由于内部是泛型实现，一旦类型被推导确定，该通道就只能传递对应类型的值, 例如此例中非i32类型的值将导致编译错误
- 接收消息的操作rx.recv()会阻塞当前线程，直到读取到值，或者通道被关闭
- 需要使用move将tx的所有权转移到子线程的闭包中
#### 同步和异步通道
##### 异步通道
```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;
fn main() {
    let (tx, rx)= mpsc::channel();

    let handle = thread::spawn(move || {
        println!("发送之前");
        tx.send(1).unwrap();
        println!("发送之后");
    });

    println!("睡眠之前");
    thread::sleep(Duration::from_secs(3));
    println!("睡眠之后");

    println!("receive {}", rx.recv().unwrap());
    handle.join().unwrap();
}
```
##### 同步通道
```rs
use std::sync::mpsc;
use std::thread;
use std::time::Duration;
fn main() {
    // 设置消息队列大小
    let (tx, rx)= mpsc::sync_channel(0);

    let handle = thread::spawn(move || {
        println!("发送之前");
        tx.send(1).unwrap();
        println!("发送之后");
    });

    println!("睡眠之前");
    thread::sleep(Duration::from_secs(3));
    println!("睡眠之后");

    println!("receive {}", rx.recv().unwrap());
    handle.join().unwrap();
}
```

#### 传输多种类型的数据
```rs
use std::sync::mpsc::{self, Receiver, Sender};

enum Fruit {
    Apple(u8),
    Orange(String)
}

fn main() {
    let (tx, rx): (Sender<Fruit>, Receiver<Fruit>) = mpsc::channel();

    tx.send(Fruit::Orange("sweet".to_string())).unwrap();
    tx.send(Fruit::Apple(2)).unwrap();

    for _ in 0..2 {
        match rx.recv().unwrap() {
            Fruit::Apple(count) => println!("received {} apples", count),
            Fruit::Orange(flavor) => println!("received {} oranges", flavor),
        }
    }
}
```
### 线程同步：锁、Condvar 和信号量
共享内存可以说是同步的灵魂，因为消息传递的底层实际上也是通过共享内存来实现，两者的区别如下：

- 共享内存相对消息传递能节省多次内存拷贝的成本
- 共享内存的实现简洁的多
- 共享内存的锁竞争更多
消息传递适用的场景很多，我们下面列出了几个主要的使用场景:

- 需要可靠和简单的(简单不等于简洁)实现时
- 需要模拟现实世界，例如用消息去通知某个目标执行相应的操作时
- 需要一个任务处理流水线(管道)时，等等
#### 互斥锁 Mutex
```rs
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();

            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```
#### 读写锁 RwLock
```rs
use std::sync::RwLock;

fn main() {
    let lock = RwLock::new(5);

    // 同一时间允许多个读
    {
        let r1 = lock.read().unwrap();
        let r2 = lock.read().unwrap();
        assert_eq!(*r1, 5);
        assert_eq!(*r2, 5);
    } // 读锁在此处被drop

    // 同一时间只允许一个写
    {
        let mut w = lock.write().unwrap();
        *w += 1;
        assert_eq!(*w, 6);

        // 以下代码会panic，因为读和写不允许同时存在
        // 写锁w直到该语句块结束才被释放，因此下面的读锁依然处于`w`的作用域中
        // let r1 = lock.read();
        // println!("{:?}",r1);
    }// 写锁在此处被drop
}
```
同时允许多个读，但最多只能有一个写
读和写不能同时存在
读可以使用read、try_read，写write、try_write, 在实际项目中，try_xxx会安全的多
### 线程同步：Atomic 原子类型与内存顺序
原子指的是一系列不可被 CPU 上下文交换的机器指令，这些指令组合在一起就形成了原子操作。在多核 CPU 下，当某个 CPU 核心开始运行原子操作时，会先暂停其它 CPU 内核对内存的操作，以保证原子操作不会被其它 CPU 内核所干扰。
```rs
use std::ops::Sub;
use std::sync::atomic::{AtomicU64, Ordering};
use std::thread::{self, JoinHandle};
use std::time::Instant;

const N_TIMES: u64 = 10000000;
const N_THREADS: usize = 10;

static R: AtomicU64 = AtomicU64::new(0);

fn add_n_times(n: u64) -> JoinHandle<()> {
    thread::spawn(move || {
        for _ in 0..n {
            R.fetch_add(1, Ordering::Relaxed);
        }
    })
}

fn main() {
    let s = Instant::now();
    let mut threads = Vec::with_capacity(N_THREADS);

    for _ in 0..N_THREADS {
        threads.push(add_n_times(N_TIMES));
    }

    for thread in threads {
        thread.join().unwrap();
    }

    assert_eq!(N_TIMES * N_THREADS as u64, R.load(Ordering::Relaxed));

    println!("{:?}",Instant::now().sub(s));
}
```
#### Atomic 能替代锁吗
对于复杂的场景下，锁的使用简单粗暴，不容易有坑
std::sync::atomic包中仅提供了数值类型的原子操作：AtomicBool, AtomicIsize, AtomicUsize, AtomicI8, AtomicU16等，而锁可以应用于各种类型
在有些情况下，必须使用锁来配合，例如上一章节中使用Mutex配合Condvar

### 基于 Send 和 Sync 的线程安全
## 全局变量
- 关键字是const而不是let
- 定义常量必须指明类型（如 i32）不能省略
- 定义常量时变量的命名规则一般是全部大写
- 常量可以在任意作用域进行定义，其生命周期贯穿整个程序的生命周期。编译时编译器会尽可能将其内联到代码中，所以在不同地方对同一常量的引用并不能保证引用到相同的内存地址
- 常量的赋值只能是常量表达式/数学表达式，也就是说必须是在编译期就能计算出的值，如果需要在运行时才能得出结果的值比如函数，则不能赋值给常量表达式
- 对于变量出现重复的定义(绑定)会发生变量遮盖，后面定义的变量会遮住前面定义的变量，常量则不允许出现重复的定义



想要全局计数器、状态控制等功能，又想要线程安全的实现，原子类型是非常好的办法。
```rs
use std::sync::atomic::{AtomicUsize, Ordering};
static REQUEST_RECV: AtomicUsize  = AtomicUsize::new(0);
fn main() {
    for _ in 0..100 {
        REQUEST_RECV.fetch_add(1, Ordering::Relaxed);
    }

    println!("当前用户请求数{:?}",REQUEST_RECV);
}
```
### lazy_static
lazy_static是社区提供的非常强大的宏，用于懒初始化静态变量，之前的静态变量都是在编译期初始化的，因此无法使用函数调用进行赋值，而lazy_static允许我们在运行期初始化静态变量！
```rs
use std::sync::Mutex;
use lazy_static::lazy_static;
lazy_static! {
    static ref NAMES: Mutex<String> = Mutex::new(String::from("Sunface, Jack, Allen"));
}

fn main() {
    let mut v = NAMES.lock().unwrap();
    v.push_str(", Myth");
    println!("{}",v);
}
```
### Box::leak
```rs
#[derive(Debug)]
struct Config {
    a: String,
    b: String
}
static mut CONFIG: Option<&mut Config> = None;

fn main() {
    let c = Box::new(Config {
        a: "A".to_string(),
        b: "B".to_string(),
    });

    unsafe {
        // 将`c`从内存中泄漏，变成`'static`生命周期
        CONFIG = Some(Box::leak(c));
        println!("{:?}", CONFIG);
    }
}
```
## 错误处理

### filter
filter 用于对 Option 进行过滤：
```rs

fn main() {
    let s1 = Some(3);
    let s2 = Some(6);
    let n = None;

    let fn_is_even = |x: &i8| x % 2 == 0;

    assert_eq!(s1.filter(fn_is_even), n);  // Some(3) -> 3 is not even -> None
    assert_eq!(s2.filter(fn_is_even), s2); // Some(6) -> 6 is even -> Some(6)
    assert_eq!(n.filter(fn_is_even), n);   // None -> no value -> None
}
```

### map() 和 map_err()
```rs
map 可以将 Some 或 Ok 中的值映射为另一个：


fn main() {
    let s1 = Some("abcde");
    let s2 = Some(5);

    let n1: Option<&str> = None;
    let n2: Option<usize> = None;

    let o1: Result<&str, &str> = Ok("abcde");
    let o2: Result<usize, &str> = Ok(5);

    let e1: Result<&str, &str> = Err("abcde");
    let e2: Result<usize, &str> = Err("abcde");

    let fn_character_count = |s: &str| s.chars().count();

    assert_eq!(s1.map(fn_character_count), s2); // Some1 map = Some2
    assert_eq!(n1.map(fn_character_count), n2); // None1 map = None2

    assert_eq!(o1.map(fn_character_count), o2); // Ok1 map = Ok2
    assert_eq!(e1.map(fn_character_count), e2); // Err1 map = Err2
}
```
### Box &lt;dyn Error>
```rs
use std::fs::read_to_string;
use std::error::Error;
fn main() -> Result<(), Box<dyn Error>> {
  let html = render()?;
  println!("{}", html);
  Ok(())
}

fn render() -> Result<String, Box<dyn Error>> {
  let file = std::env::var("MARKDOWN")?;
  let source = read_to_string(file)?;
  Ok(source)
}
```
## unsafe 简介

### 解引用裸指针
裸指针长这样: *const T 和 *mut T，它们分别代表了不可变和可变。
**作用**：
- 可以绕过 Rust 的借用规则，可以同时拥有一个数据的可变、不可变指针，甚至还能拥有多个可变的指针
- 并不能保证指向合法的内存
- 可以是 null
- 没有实现任何自动的回收 (drop)
#### 基于引用创建裸指针
创建裸指针是安全的行为，而解引用裸指针才是不安全的行为 :
```rs
fn main() {
    let mut num = 5;

    let r1 = &num as *const i32;

    unsafe {
        println!("r1 is: {}", *r1);
    }
}
```

### FFI
FFI（Foreign Function Interface）可以用来与其它语言进行交互，但是并不是所有语言都这么称呼，例如 Java 称之为 JNI（Java Native Interface）。

FFI 之所以存在是由于现实中很多代码库都是由不同语言编写的，如果我们需要使用某个库，但是它是由其它语言编写的，那么往往只有两个选择：

- 对该库进行重写或者移植
- 使用 FFI
unsafe 的另一个重要目的就是对 FFI 提供支持，它的全称是 Foreign Function Interface，顾名思义，通过 FFI , 我们的 Rust 代码可以跟其它语言的外部代码进行交互。
下面的例子演示了如何调用 C 标准库中的 abs 函数：
```rs
extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
    }
}
```
#### ABI
在 extern "C" 代码块中，我们列出了想要调用的外部函数的签名。其中 "C" 定义了外部函数所使用的应用二进制接口ABI (Application Binary Interface)：ABI 定义了如何在汇编层面来调用该函数。在所有 ABI 中，C 语言的是最常见的。

#### 在其它语言中调用 Rust 函数
我们可以使用 extern 来创建一个接口，其它语言可以通过该接口来调用相关的 Rust 函数。但是此处的语法与之前有所不同，之前用的是语句块，而这里是在函数定义时加上 extern 关键字，当然，别忘了指定相应的 ABI：
```rs
#[no_mangle]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```
### 内联汇编


上面的代码可以让 call_from_c 函数被 C 语言的代码调用，当然，前提是将其编译成一个共享库，然后链接到 C 语言中。

这里还有一个比较奇怪的注解 #[no_mangle]，它用于告诉 Rust 编译器：不要乱改函数的名称。 Mangling 的定义是：当 Rust 因为编译需要去修改函数的名称，例如为了让名称包含更多的信息，这样其它的编译部分就能从该名称获取相应的信息，这种修改会导致函数名变得相当不可读。因此，为了让 Rust 函数能顺利被其它语言调用，我们必须要禁止掉该功能。
## Macro 宏编程
在 Rust 中宏分为两大类：声明式宏( declarative macros ) macro_rules! 和三种过程宏( procedural macros ):

    - #[derive]，在之前多次见到的派生宏，可以为目标结构体或枚举派生指定的代码，例如 Debug 特征
    - 类属性宏(Attribute-like macro)，用于为目标添加自定义的属性
    - 类函数宏(Function-like macro)，看上去就像是函数调用
### 宏和函数的区别
元编程
从根本上来说，宏是通过一种代码来生成另一种代码，如果大家熟悉元编程，就会发现两者的共同点。
可变参数
Rust 的函数签名是固定的：定义了两个参数，就必须传入两个参数，多一个少一个都不行，对于从 JS/TS 过来的同学，这一点其实是有些恼人的。
宏展开
由于宏会被展开成其它代码，且这个展开过程是发生在编译器对代码进行解释之前。因此，宏可以为指定的类型实现某个特征：先将宏展开成实现特征的代码后，再被编译。
相对函数来说，由于宏是基于代码再展开成代码，因此实现相比函数来说会更加复杂，再加上宏的语法更为复杂，最终导致定义宏的代码相当地难读，也难以理解和维护。
```rs
#[macro_export]
macro_rules! vec {
    ( $( $x:expr ),* ) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}
```

## 异步编程
### Async 编程简介
- OS 线程, 它最简单，也无需改变任何编程模型(业务/代码逻辑)，因此非常适合作为语言的原生并发模型，我们在多线程章节也提到过，Rust 就选择了原生支持线程级的并发编程。但是，这种模型也有缺点，例如线程间的同步将变得更加困难，线程间的上下文切换损耗较大。使用线程池在一定程度上可以提升性能，但是对于 IO 密集的场景来说，线程池还是不够。
- 事件驱动(Event driven), 这个名词你可能比较陌生，如果说事件驱动常常跟回调( Callback )一起使用，相信大家就恍然大悟了。这种模型性能相当的好，但最大的问题就是存在回调地狱的风险：非线性的控制流和结果处理导致了数据流向和错误传播变得难以掌控，还会导致代码可维护性和可读性的大幅降低，大名鼎鼎的 JavaScript 曾经就存在回调地狱。
- 协程(Coroutines) 可能是目前最火的并发模型，Go 语言的协程设计就非常优秀，这也是 Go 语言能够迅速火遍全球的杀手锏之一。协程跟线程类似，无需改变编程模型，同时，它也跟 async 类似，可以支持大量的任务并发运行。但协程抽象层次过高，导致用户无法接触到底层的细节，这对于系统编程语言和自定义异步运行时是难以接受的
- actor 模型是 erlang 的杀手锏之一，它将所有并发计算分割成一个一个单元，这些单元被称为 actor , 单元之间通过消息传递的方式进行通信和数据传递，跟分布式系统的设计理念非常相像。由于 actor 模型跟现实很贴近，因此它相对来说更容易实现，但是一旦遇到流控制、失败重试等场景时，就会变得不太好用
- async/await， 该模型性能高，还能支持底层编程，同时又像线程和协程那样无需过多的改变编程模型，但有得必有失，async 模型的问题就是内部实现机制过于复杂，对于用户来说，理解和使用起来也没有线程和协程简单，好在前者的复杂性开发者们已经帮我们封装好，而理解和使用起来不够简单，正是本章试图解决的问题。

对于长时间运行的 CPU 密集型任务，例如并行计算，使用线程将更有优势。 这种密集任务往往会让所在的线程持续运行，任何不必要的线程切换都会带来性能损耗，因此高并发反而在此时成为了一种多余。同时你所创建的线程数应该等于 CPU 核心数，充分利用 CPU 的并行能力，甚至还可以将线程绑定到 CPU 核心上，进一步减少线程上下文切换。

而高并发更适合 IO 密集型任务，例如 web 服务器、数据库连接等等网络服务，因为这些任务绝大部分时间都处于等待状态，如果使用多线程，那线程大量时间会处于无所事事的状态，再加上线程上下文切换的高昂代价，让多线程做 IO 密集任务变成了一件非常奢侈的事。而使用async，既可以有效的降低 CPU 和内存的负担，又可以让大量的任务并发的运行，一个任务一旦处于IO或者其他等待(阻塞)状态，就会被立刻切走并执行另一个任务，而这里的任务切换的性能开销要远远低于使用多线程时的线程上下文切换。
#### async/.await 简单入门
async/.await 是 Rust 内置的语言特性，可以让我们用同步的方式去编写异步的代码。
通过 async 标记的语法块会被转换成实现了Future特征的状态机。 与同步调用阻塞当前线程不同，当Future执行并遇到阻塞时，它会让出当前线程的控制权，这样其它的Future就可以在该线程中运行，这种方式完全不会导致当前线程的阻塞。
下面我们来通过例子学习 async/.await 关键字该如何使用，在开始之前，需要先引入 futures 包。编辑 Cargo.toml 文件并添加以下内容:
```toml
[dependencies]
futures = "0.3"
```
```rs
// `block_on`会阻塞当前线程直到指定的`Future`执行完成，这种阻塞当前线程以等待任务完成的方式较为简单、粗暴，
// 好在其它运行时的执行器(executor)会提供更加复杂的行为，例如将多个`future`调度到同一个线程上执行。
use futures::executor::block_on;

async fn hello_world() {
    hello_cat().await;
    println!("hello, world!");
}

async fn hello_cat() {
    println!("hello, kitty!");
}
fn main() {
    let future = hello_world(); // 返回一个Future, 因此不会打印任何输出
    block_on(future); // 执行`Future`并等待其运行完成，此时"hello, world!"会被打印输出
}
```
总之，在async fn函数中使用.await可以等待另一个异步调用的完成。但是与block_on不同，.await并不会阻塞当前的线程，而是异步的等待Future A的完成，在等待的过程中，该线程还可以继续执行其它的Future B，最终实现了并发处理的效果。
### 底层探秘: Future 执行器与任务调度
#### Future 特征
首先，来给出 Future 的定义：它是一个能产出值的异步计算(虽然该值可能为空，例如 () )。光看这个定义，可能会觉得很空洞，我们来看看一个简化版的 Future 特征:
```rs
trait SimpleFuture {
    type Output;
    fn poll(&mut self, wake: fn()) -> Poll<Self::Output>;
}

enum Poll<T> {
    Ready(T),
    Pending,
}
```



### 定海神针 Pin 和 Unpin
```rs
#[derive(Debug)]
struct Test {
    a: String,
    b: *const String,
}

impl Test {
    fn new(txt: &str) -> Self {
        Test {
            a: String::from(txt),
            b: std::ptr::null(),
        }
    }

    fn init(&mut self) {
        let self_ref: *const String = &self.a;
        self.b = self_ref;
    }

    fn a(&self) -> &str {
        &self.a
    }

    fn b(&self) -> &String {
        assert!(!self.b.is_null(), "Test::b called without Test::init being called first");
        unsafe { &*(self.b) }
    }
}

```
### async/await 和 Stream 流处理
#### async/await 和 Stream 流处理
async 允许我们使用 move 关键字来将环境中变量的所有权转移到语句块内，就像闭包那样，好处是你不再发愁该如何解决借用生命周期的问题，坏处就是无法跟其它代码实现对变量的共享:

### 使用 join! 和 select! 同时运行多个 Future
#### join!
futures 包中提供了很多实用的工具，其中一个就是 join! 宏， 它允许我们同时等待多个不同 Future 的完成，且可以并发地运行这些 Future。
```rs
use futures::{
    future::TryFutureExt,
    try_join,
};

async fn get_book() -> Result<Book, ()> { /* ... */ Ok(Book) }
async fn get_music() -> Result<Music, String> { /* ... */ Ok(Music) }

async fn get_book_and_music() -> Result<(Book, Music), String> {
    let book_fut = get_book().map_err(|()| "Unable to get book".to_string());
    let music_fut = get_music();
    try_join!(book_fut, music_fut)
}

```
#### select!
```rs
use futures::{
    future::FutureExt, // for `.fuse()`
    pin_mut,
    select,
};

async fn task_one() { /* ... */ }
async fn task_two() { /* ... */ }

async fn race_tasks() {
    let t1 = task_one().fuse();
    let t2 = task_two().fuse();

    pin_mut!(t1, t2);

    select! {
        () = t1 => println!("任务1率先完成"),
        () = t2 => println!("任务2率先完成"),
    }
}
```

```rs
use futures::{
    future::FutureExt, // for `.fuse()`
    pin_mut,
    select,
};

async fn task_one() { /* ... */ }
async fn task_two() { /* ... */ }

async fn race_tasks() {
    let t1 = task_one().fuse();
    let t2 = task_two().fuse();

    pin_mut!(t1, t2);

    select! {
        () = t1 => println!("任务1率先完成"),
        () = t2 => println!("任务2率先完成"),
    }
}
```

# 宏编程
## 语法拓展
### 源代码解析方式
#### 标识化 (Tokenization)
Rust程序编译过程的第一阶段是 标记解析。 在这一过程中，源代码将被转换成一系列的标记 (token)。

某些语言的宏系统正扎根于这一阶段。Rust并非如此。 举例来说，从效果来看，C/C++的宏就是在这里得到处理的。3 这也正是下列代码能够运行的原因: 4
```c
#define SUB void
#define BEGIN {
#define END }

SUB main() BEGIN
    printf("Oh, the horror!\n");
END
```
#### 语法解析 (Parsing)

这一过程中，一系列的 token 将被转换成一棵抽象语法树 (AST: Abstract Syntax Tree)。 此过程将在内存中建立起程序的语法结构。

举例来说，标记序列 1+2 将被转换成某种类似于:
```
┌─────────┐   ┌─────────┐
│ BinOp   │ ┌╴│ LitInt  │
│ op: Add │ │ │ val: 1  │
│ lhs: ◌  │╶┘ └─────────┘
│ rhs: ◌  │╶┐ ┌─────────┐
└─────────┘ └╴│ LitInt  │
              │ val: 2  │
              └─────────┘
```

AST 将包含 整个 程序的结构，但这一结构仅包含词法信息。

举例来讲，在这个阶段编译器虽然可能知道某个表达式提及了某个名为 a 的变量， 但它并 没有办法知道 a 究竟是什么，或者它从哪来。

在 AST 生成之后，宏处理过程才开始。
#### 标记树 (Token Trees)
标记树是介于 标记 (token) 与 AST 之间的东西。

首先明确一点，几乎所有标记都构成标记树。 具体来说，它们可被看作标记树叶节点。 还有另一类事物也可被看作标记树叶节点，我们将在稍后提到它。

仅有的一种基础标记不是标记树叶节点——“分组”标记：(...)， [...] 和 {...}。 这三者属于标记树内的节点，正是它们给标记树带来了树状的结构。

给个具体的例子，这列标记：


a + b + (c + d[0]) + e
将被解析为这样的标记树：


«a» «+» «b» «+» «(   )» «+» «e»
          ╭────────┴──────────╮
           «c» «+» «d» «[   ]»
                        ╭─┴─╮
                         «0»
注意它跟最后生成的 AST 并 没有关联。 AST 将仅有一个根节点，而这棵标记树有 七 个。 作为参考，最后生成的 AST 应该是这样：


              ┌─────────┐
              │ BinOp   │
              │ op: Add │
            ┌╴│ lhs: ◌  │
┌─────────┐ │ │ rhs: ◌  │╶┐ ┌─────────┐
│ Var     │╶┘ └─────────┘ └╴│ BinOp   │
│ name: a │                 │ op: Add │
└─────────┘               ┌╴│ lhs: ◌  │
              ┌─────────┐ │ │ rhs: ◌  │╶┐ ┌─────────┐
              │ Var     │╶┘ └─────────┘ └╴│ BinOp   │
              │ name: b │                 │ op: Add │
              └─────────┘               ┌╴│ lhs: ◌  │
                            ┌─────────┐ │ │ rhs: ◌  │╶┐ ┌─────────┐
                            │ BinOp   │╶┘ └─────────┘ └╴│ Var     │
                            │ op: Add │                 │ name: e │
                          ┌╴│ lhs: ◌  │                 └─────────┘
              ┌─────────┐ │ │ rhs: ◌  │╶┐ ┌─────────┐
              │ Var     │╶┘ └─────────┘ └╴│ Index   │
              │ name: c │               ┌╴│ arr: ◌  │
              └─────────┘   ┌─────────┐ │ │ ind: ◌  │╶┐ ┌─────────┐
                            │ Var     │╶┘ └─────────┘ └╴│ LitInt  │
                            │ name: d │                 │ val: 0  │
                            └─────────┘                 └─────────┘
理解 AST 与 标记树 (token tree) 之间的区别至关重要。 写宏时，你将同时与这两者打交道。

还有一条需要注意：不可能 出现不匹配的小/中/大括号，也不可能存在包含错误嵌套结构的标记树。
### AST 中的宏
Rust 语法包含数种“语法扩展”的形式。具体来说有以下四种（顺便给出例子）：
```rs
# [ $arg ] 形式：比如 #[derive(Clone)], #[no_mangle]
# ! [ $arg ] 形式：比如 #![allow(dead_code)], #![crate_name="blang"]
$name ! $arg 形式：比如 println!("Hi!"), concat!("a", "b"),
$name ! $arg0 $arg1 形式：比如 macro_rules! dummy { () => {}; }.
```

头两种形式被称作“属性” (attributes)。属性用来给条目 (items) 、表达式、语句加上注解。属性有三类：

- 内置的属性 (built-in attributes)
- 过程宏属性 (proc-macro attributes)
- 派生属性 (derive attributes)
内置的属性由编译器实现。过程宏属性和派生属性在 Rust 第二类宏系统 —— 过程宏 (procedural macros) —— 中实现。


注意第 3 种形式的函数式宏是一种一般的语法拓展形式，并非仅用 macro_rules! 写出。 比如 format! 是一个 macro_rules! 宏，而用来实现 format! 的 format_args! 不是这里谈论的宏（因为它由编译器实现，是内置的属性）。

第四种形式本质上是宏的变种。其实，这种形式的唯一用例只有 macro_rules!。




知道这一点后，语法解析器如何理解如下调用形式，就变得显而易见了：
```rs
bitflags! {
    struct Color: u8 {
        const RED    = 0b0001,
        const GREEN  = 0b0010,
        const BLUE   = 0b0100,
        const BRIGHT = 0b1000,
    }
}

lazy_static! {
    static ref FIB_100: u32 = {
        fn fib(a: u32) -> u32 {
            match a {
                0 => 0,
                1 => 1,
                a => fib(a-1) + fib(a-2)
            }
        }

        fib(100)
    };
}

fn main() {
    use Color::*;
    let colors = vec![RED, GREEN, BLUE];
    println!("Hello, World!");
}
```


虽然上述调用看起来包含了各式各样的 Rust 代码，但对语法解析器来说，它们仅仅是堆无实际意义的标记树。

为了说明问题，我们把所有这些句法“黑盒”用 ⬚ 代替，仅剩下：

```rs
bitflags! ⬚

lazy_static! ⬚

fn main() {
    let colors = vec! ⬚;
    println! ⬚;
}
```

再次重申，语法解析器对 ⬚ 不作任何假设；它记录黑盒所包含的标记，但并不尝试理解它们。

这意味着 ⬚ 可以是任何东西，甚至是无效的 Rust 语法。

以下几点很重要：

Rust 包含多种语法扩展。
- 当遇见形如 $name! $arg 的结构时，它可能是其它语法扩展，比如 macro_rules! 宏、过程宏甚至内置宏。
- 所有 ! 宏（即第 3 种形式）的输入都是非叶节点的单个标记树。
- 语法扩展都将作为抽象语法树 (AST) 的一部分被解析。

最后一点最为重要，它带来了一些深远的影响。由于语法拓展将被解析进 AST 中，它们只能出现在那些明确支持它们出现的位置。具体来说，语法拓展能在如下位置出现：
- 模式 (pattern)
- 语句 (statement)
- 表达式 (expression)
- 条目 (item) （包括 impl 块）
- 类型

一些并不支持的位置包括：

- 标识符 (identifier)
- match 分支

### 展开
展开相对简单。在生成 AST 之后，和编译器对程序进行语义理解之前，编译器将会对所有语法拓展进行展开。

这一过程包括：遍历 AST，确定所有语法拓展调用的位置，并把它们替换成展开的内容。

每当编译器遇见一个语法扩展，都会根据上下文解析成有限语法元素集中的一个。

事实上，一个语义扩展的展开结果会变成以下一种情况：

- 一个表达式
- 一个模式
- 一个类型
- 零或多个条目（包括的 impl 块）
- 零或多个语句
换句话讲，语法拓展调用所在的位置，决定了该语法拓展展开结果被解读的方式。

编译器会操作 AST 节点，把语法拓展调用处的节点完全替换成输出的节点。这一替换是结构性 (structural) 的，而非织构性 (textural) 的。
```rs
let eight = 2 * four!();
```
┌─────────────┐
│ Let         │
│ name: eight │   ┌─────────┐
│ init: ◌     │╶─╴│ BinOp   │
└─────────────┘   │ op: Mul │
                ┌╴│ lhs: ◌  │
     ┌────────┐ │ │ rhs: ◌  │╶┐ ┌────────────┐
     │ LitInt │╶┘ └─────────┘ └╴│ Macro      │
     │ val: 2 │                 │ name: four │
     └────────┘                 │ body: ()   │
                                └────────────┘

根据上下文，four!() 必须展开成一个表达式（initializer 只可能是表达式）。因此，无论实际展开的结果如何，它都将被解读成一个完整的表达式。
此处假设 four! 成其展开结果为表达式 1 + 3。故而，展开后将 AST 变为：
┌─────────────┐
│ Let         │
│ name: eight │   ┌─────────┐
│ init: ◌     │╶─╴│ BinOp   │
└─────────────┘   │ op: Mul │
                ┌╴│ lhs: ◌  │
     ┌────────┐ │ │ rhs: ◌  │╶┐ ┌─────────┐
     │ LitInt │╶┘ └─────────┘ └╴│ BinOp   │
     │ val: 2 │                 │ op: Add │
     └────────┘               ┌╴│ lhs: ◌  │
                   ┌────────┐ │ │ rhs: ◌  │╶┐ ┌────────┐
                   │ LitInt │╶┘ └─────────┘ └╴│ LitInt │
                   │ val: 1 │                 │ val: 3 │
                   └────────┘                 └────────┘

这又能被重写成：

```rs
let eight = 2 * (1 + 3);
```
语法拓展被当作 AST 节点展开，这一观点非常重要，它造成两大影响：

- 语法拓展不仅调用位置有限制，其展开结果也只能跟语法解析器在该位置所预期的 AST 节点种类一致。
- 因此，语法拓展必定无法展开成不完整或不合语法的结构。
### 卫生性
卫生性 (hygiene) 是宏的一个重要概念。它描述了宏在其语法上下文中工作的能力：不影响或不受其周围环境的影响。

简而言之，如果由语法扩展创建的标识符不能被调用该语法扩展的环境访问，那么它对于该标识符是卫生的。

同样，如果语法扩展中使用的标识符不能引用到在语法扩展之外定义的内容，则被认为是卫生的。

```rs
macro_rules! make_local {
    () => { let local = 0; }
}
fn main() {
    make_local!();
    assert_eq!(local, 0);
}
```
如果 assert_eq!(local, 0); 中的 local 被解析为语法扩展所定义的 local，则语法扩展不是卫生的（至少在 local 这个名称/绑定方面不是卫生的）。
### 调试
rustc 通过不稳定的 -Zunpretty=expanded 参数来提供查看展开代码的功能。
```rs
// Shorthand for initializing a `String`.
macro_rules! S {
    ($e:expr) => {String::from($e)};
}

fn main() {
    let world = S!("World");
    println!("Hello, {}!", world);
}
```
rustc +nightly -Zunpretty=expanded hello.rs
```rs
#![feature(prelude_import)]
#[prelude_import]
use std::prelude::rust_2018::*;
#[macro_use]
extern crate std;
// Shorthand for initializing a `String`.
macro_rules! S { ($e : expr) => { String :: from($e) } ; }

fn main() {
    let world = String::from("World");
    {
        ::std::io::_print(
            ::core::fmt::Arguments::new_v1(
                &["Hello, ", "!\n"],
                &match (&world,) {
                    (arg0,) => [
                        ::core::fmt::ArgumentV1::new(arg0, ::core::fmt::Display::fmt)
                    ],
                }
            )
        );
    };
}
```
## 声明宏
### 思路介绍
#### macro_rules!
macro_rules! 本身就是一个语法扩展，也就是从技术上说，它并不是 Rust 语法的一部分。它的形式如下：
```rs
macro_rules! $name {
    $rule0 ;
    $rule1 ;
    // …
    $ruleN ;
}
```
至少得有一条规则，每条“规则”都形如：
```rs
($matcher) => {$expansion}
```
#### 匹配
对每条规则，它都将尝试将输入标记树的内容与该规则的 matcher 进行匹配。某个 matcher 2 必须与输入完全匹配才被认为是一次匹配。
最简单的例子是空 matcher：
```rs
macro_rules! four {
    () => { 1 + 3 };
}
```
当且仅当匹配到空的输入时，匹配成功，即 four!()、four![] 或 four!{} 三种方式调用是匹配成功的 。
注意所用的分组标记并不需要匹配定义时采用的分组标记，因为实际上分组标记并未传给调用。
比如，要匹配标记序列 4 fn ['spang "whammo"] @_@ ，我们可以这样写：
```rs
macro_rules! gibberish {
    (4 fn ['spang "whammo"] @_@) => {...};
}

使用 gibberish!(4 fn ['spang "whammo"] @_@]) 即可成功匹配和调用。
```

#### 元变量
matcher 还可以包含捕获 (captures)。即基于某种通用语法类别来匹配输入，并将结果捕获到元变量 (metavariable) 中，然后将替换元变量到输出。
捕获的书写方式是：先写美元符号 $，然后跟一个标识符，然后是冒号 :，最后是捕获方式，比如 $e:expr。

捕获方式又被称作“片段分类符” (fragment-specifier)，必须是以下一种：

- block：一个块（比如一块语句或者由大括号包围的一个表达式）
- expr：一个表达式 (expression)
- ident：一个标识符 (identifier)，包括关键字 (keywords)
- item：一个条目（比如函数、结构体、模块、impl 块）
- lifetime：一个生命周期注解（比如 'foo、'static）
- literal：一个字面值（比如 "Hello World!"、3.14、'🦀'）
- meta：一个元信息（比如 #[...] 和 #![...] 属性内部的东西）
- pat：一个模式 (pattern)
- path：一条路径（比如 foo、::std::mem::replace、transmute::<_, int>）
- stmt：一条语句 (statement)
- tt：单棵标记树
- ty：一个类型
- vis：一个可能为空的可视标识符（比如 pub、pub(in crate)）
```rs
macro_rules! multiply_add {
    ($a:expr, $b:expr, $c:expr) => { $a * ($b + $c) };
}
```
#### 反复
matcher 可以有反复捕获 (repetition)，这使得匹配一连串标记 (token) 成为可能。反复捕获的一般形式为 $ ( ... ) sep rep。

- $ 是字面上的美元符号标记
- ( ... ) 是被反复匹配的模式，由小括号包围。
- sep 是可选的分隔标记。它不能是括号或者反复操作符 rep。常用例子有 , 和 ; 。
- rep 是必须的重复操作符。当前可以是：
- ?：表示最多一次重复，所以此时不能前跟分隔标记。
- *：表示零次或多次重复。
- +：表示一次或多次重复。 
在 expansion 中，使用被反复捕获的内容时，也采用相同的语法。而且被反复捕获的元变量只能存在于反复语法内。
```rs
macro_rules! vec_strs {
    (
        // 开始反复捕获
        $(
            // 每个反复必须包含一个表达式
            $element:expr
        )
        // 由逗号分隔
        ,
        // 0 或多次
        *
    ) => {
        // 在这个块内用大括号括起来，然后在里面写多条语句
        {
            let mut v = Vec::new();

            // 开始反复捕获
            $(
                // 每个反复会展开成下面表达式，其中 $element 被换成相应被捕获的表达式
                v.push(format!("{}", $element));
            )*

            v
        }
    };
}

fn main() {
    let s = vec_strs![1, "a", true, 3.14159f32];
    assert_eq!(s, &["1", "a", "true", "3.14159"]);
}
```
#### 元变量表达式
transcriber4 可以包含所谓的元变量表达 (metavariable expressions)。
可以使用以下表达式（其中 ident 是所绑定的元变量的名称，而 depth 是整型字面值）：
```rs
${count(ident)}：最里层反复 $ident 的总次数，相当于 ${count(ident, 0)}
${count(ident，depth)}：第 depth 层反复 $ident 的次数
${index()}：最里层反复的当前反复的索引，相当于 ${index(0)}
${index(depth)}：在第 depth 层处当前反复的索引，向外计数
${length()}：最里层反复的重复次数，相当于 ${length(0)}
${length(depth)}：在第 depth 层反复的次数，向外计数
${ignore(ident)}：绑定 $ident 进行重复，并展开成空
$$：展开为单个 $，这会有效地转义 $ 标记，因此它不会被展开（转写）

```

### 实战篇
#### 构建过程
```rs
let fib = recurrence![a[n] = 0, 1, ..., a[n-1] + a[n-2]];

for e in fib.take(10) { println!("{}", e) }
```
以此为基点，我们可以向宏的定义迈出第一步， 即便在此时我们尚不了解该宏的展开部分究竟是什么样子。 此步骤的用处在于，如果在此处无法明确如何解析输入语法， 那就可能意味着，整个宏的构思需要改变。
```rs
macro_rules! recurrence {
    ( a[n] = $($inits:expr),+ , ... , $recur:expr ) => { /* ... */ };
}

```
- 一段字面标记序列，a [ n ] = ；
- 一段 重复 的序列（$( ... )），其内元素由,分隔，允许重复一或多次（ + ）； 重复的内容允许：一个有效的 表达式，它将被捕获至 元变量 inits ($inits:expr)
- 又一段字面标记序列 , ... ,；
- 一个有效的 表达式，将被捕获至 元变量 recur ($recur:expr)。

#### 导出宏
```rs
#[macro_export]
macro_rules! count_exprs { /* */  }

#[macro_export]
macro_rules! recurrence { /* */ }
```
### 细节
#### 片段分类符
- block
- expr
- ident
- item
- lifetime
- literal
- meta
- pat
- pat_param
- path
- stmt
- tt
- ty
- vis
##### block
块 (block) 由 { 开始，接着是一些语句，最后是可选的表达式，然后以 } 结束。 块的类型要么是最后的值表达式类型，要么是 () 类型。
```rs
macro_rules! blocks {
    ($($block:block)*) => ();
}

blocks! {
    {}
    {
        let zig;
    }
    { 2 }
}
fn main() {}
```
##### expr
expr 分类符用于匹配任何形式的表达式 (expression)。
```rs
macro_rules! expressions {
    ($($expr:expr)*) => ();
}

expressions! {
    "literal"
    funcall()
    future.await
    break 'foo bar
}
fn main() {}
```
##### ident
ident 分类符用于匹配任何形式的标识符 (identifier) 或者关键字。 。
```rs
macro_rules! idents {
    ($($ident:ident)*) => ();
}

idents! {
    // _ <- `_` 不是标识符，而是一种模式
    foo
    async
    O_________O
    _____O_____
}
fn main() {}
```
##### item
item 分类符只匹配 Rust 的 item 的 定义 (definitions) ， 不会匹配指向 item 的标识符 (identifiers)。例子：
```rs
macro_rules! items {
    ($($item:item)*) => ();
}

items! {
    struct Foo;
    enum Bar {
        Baz
    }
    impl Foo {}
    /*...*/
}
fn main() {}
```

##### lifetime
lifetime 分类符用于匹配生命周期注解或者标签 (lifetime or label)。 它与 ident 很像，但是 lifetime 会匹配到前缀 '' 。
```rs
macro_rules! lifetimes {
    ($($lifetime:lifetime)*) => ();
}

lifetimes! {
    'static
    'shiv
    '_
}
fn main() {}
```
##### literal
literal 分类符用于匹配字面表达式 (literal expression)。
```rs
macro_rules! literals {
    ($($literal:literal)*) => ();
}

literals! {
    -1
    "hello world"
    2.3
    b'b'
    true
}
fn main() {}
```
##### meta
meta 分类符用于匹配属性 (attribute)， 准确地说是属性里面的内容。通常你会在 #[$meta:meta] 或 #![$meta:meta] 模式匹配中 看到这个分类符。
```rs
macro_rules! metas {
    ($($meta:meta)*) => ();
}

metas! {
    ASimplePath
    super::man
    path = "home"
    foo(bar)
}
fn main() {}
```
##### pat
pat 分类符用于匹配任何形式的模式 (pattern)，包括 2021 edition 开始的 or-patterns。

```rs
macro_rules! patterns {
    ($($pat:pat)*) => ();
}

patterns! {
    "literal"
    _
    0..5
    ref mut PatternsAreNice
    0 | 1 | 2 | 3 
}
fn main() {}
```
##### pat_param
or-patterns 模式开始应用，这让 pat 分类符不再允许跟随 |。
```rs
macro_rules! patterns {
    (pat: $pat:pat) => {
        println!("pat: {}", stringify!($pat));
    };
    (pat_param: $($pat:pat_param)|+) => {
        $( println!("pat_param: {}", stringify!($pat)); )+
    };
}
fn main() {
    patterns! {
       pat: 0 | 1 | 2 | 3
    }
    patterns! {
       pat_param: 0 | 1 | 2 | 3
    }
}
```
##### path
path 分类符用于匹配类型中的路径 (TypePath)。这包括函数式的 trait 形式。
```rs
macro_rules! paths {
    ($($path:path)*) => ();
}

paths! {
    ASimplePath
    ::A::B::C::D
    G::<eneri>::C
    FnMut(u32) -> ()
}
fn main() {}
```
##### stmt
stmt 分类符只匹配的 语句 (statement)。 除非 item 语句要求结尾有分号，否则 不会 匹配语句最后的分号。
```rs
macro_rules! statements {
    ($($stmt:stmt)*) => ($($stmt)*);
}

fn main() {
    statements! {
        struct Foo;
        fn foo() {}
        let zig = 3
        if true {} else {}
        {}
    }
}
```
##### tt
tt 分类符用于匹配标记树 (TokenTree)。 如果你是新手，对标记树不了解，那么需要回顾本书 标记树 一节。tt 分类符是最有作用的分类符之一，因为它能匹配几乎所有东西， 而且能够让你在使用宏之后检查 (inspect) 匹配的内容。

##### ty
ty 分类符用于匹配任何形式的类型表达式 (type expression)。
```rs
macro_rules! types {
    ($($type:ty)*) => ();
}

types! {
    foo::bar
    bool
    [u8]
    impl IntoIterator<Item = u32>
}
fn main() {}
```
##### vis
vis 分类符会匹配 可能为空 可见性修饰符 (Visibility qualifier)。
```rs
macro_rules! visibilities {
    //         ∨~~注意这个逗号，`vis` 分类符自身不会匹配到逗号
    ($($vis:vis,)*) => ();
}

visibilities! {
    , // 没有 vis 也行，因为 $vis 隐式包含 `?` 的情况
    pub,
    pub(crate),
    pub(in super),
    pub(in some_path),
}
fn main() {}
```
#### 再谈元变量与宏展开

#### 元变量表达式
##### Dollar Dollar ($$)

```rs
$$ 表达式展开为单个 $，实际上使其成为转义的 $。这让声明宏宏生成新的声明宏。
#![feature(macro_metavar_expr)]

macro_rules! foo {
    () => {
        macro_rules! bar {
            ( $$( $$any:tt )* ) => { $$( $$any )* };
        }
    };
}

foo!();
bar!();
```

##### count(ident, depth)

count 表达式展开成元变量 $ident 在给定反复深度的反复次数。

- ident 参数必须是规则作用域中声明的元变量
- depth 参数必须是值小于或等于元变量 $ident 出现的最大反复深度的整型字面值
- count(ident, depth) 展开成不带后缀的整型字面值标记
- count(ident) 是 count(ident, 0) 的简
```rs
#![feature(macro_metavar_expr)]

macro_rules! foo {
    ( $( $outer:ident ( $( $inner:ident ),* ) ; )* ) => {
        println!("count(outer, 0): $outer repeats {} times", ${count(outer)});
        println!("count(inner, 0): The $inner repetition repeats {} times in the outer repetition", ${count(inner, 0)});
        println!("count(inner, 1): $inner repeats {} times in the inner repetitions", ${count(inner, 1)});
    };
}

fn main() {
    foo! {
        outer () ;
        outer ( inner , inner ) ;
        outer () ;
        outer ( inner ) ;
    };
}
```

##### index(depth)
index(depth) 表达式展开为给定反复深度下，当前的迭代索引。

- depth 参数表明在第几层反复，这个数字从最内层反复调用表达式开始向外计算
- index(depth) 展开成不带后缀的整型字面值标记
- index() 是 index(0) 的简写
```rs

#![feature(macro_metavar_expr)]

macro_rules! attach_iteration_counts {
    ( $( ( $( $inner:ident ),* ) ; )* ) => {
        ( $(
            $((
                stringify!($inner),
                ${index(1)}, // 这指的是外层反复
                ${index()}  // 这指的是内层反复，等价于 `index(0)`
            ),)*
        )* )
    };
}

fn main() {
    let v = attach_iteration_counts! {
        ( hello ) ;
        ( indices , of ) ;
        () ;
        ( these, repetitions ) ;
    };
    println!("{v:?}");
}
```
##### length(depth)
length(depth) 表达式展开为在给定反复深度的迭代次数。

- depth 参数表示在第几层反复，这个数字从最内层反复调用表达式开始向外计算
- length(depth) 展开成不带后缀的整型字面值标记
- length() 是 length(0) 的简写
```rs

#![feature(macro_metavar_expr)]

macro_rules! lets_count {
    ( $( $outer:ident ( $( $inner:ident ),* ) ; )* ) => {
        $(
            $(
                println!(
                    "'{}' in inner iteration {}/{} with '{}' in outer iteration {}/{} ",
                    stringify!($inner), ${index()}, ${length()},
                    stringify!($outer), ${index(1)}, ${length(1)},
                );
            )*
        )*
    };
}

fn main() {
    lets_count!(
        many (small , things) ;
        none () ;
        exactly ( one ) ;
    );
}
```

##### ignore(ident)

ignore(ident) 表达式展开为空，这使得在无需实际展开元变量的时候，像元变量反复展开相同次数的某些内容。
```rs
#![feature(macro_metavar_expr)]

macro_rules! repetition_tuples {
    ( $( ( $( $inner:ident ),* ) ; )* ) => {
        ($(
            $(
                (
                    ${index()},
                    ${index(1)}
                    ${ignore(inner)} // without this metavariable expression, compilation would fail
                ),
            )*
        )*)
    };
}

fn main() {
    let tuple = repetition_tuples!(
        ( one, two ) ;
        () ;
        ( one ) ;
        ( one, two, three ) ;
    );
    println!("{tuple:?}");
}
```

#### 调试
##### trace_macros!
最有用的是 trace_macros!，在每次声明宏展开前，它指示编译器记录下声明宏的调用信息。
```rs
#![feature(trace_macros)]

macro_rules! each_tt {
    () => {};
    ($_tt:tt $($rest:tt)*) => {each_tt!($($rest)*);};
}

each_tt!(foo bar baz quux);
trace_macros!(true);
each_tt!(spim wak plee whum);
trace_macros!(false);
each_tt!(trom qlip winp xod);

```

##### log_syntax!

另一有用的宏是 log_syntax!。它将使得编译器输出所有经过编译器处理的标记。

```rs
#![feature(log_syntax)]

macro_rules! sing {
    () => {};
    ($tt:tt $($rest:tt)*) => {log_syntax!($tt); sing!($($rest)*);};
}

sing! {
    ^ < @ < . @ *
    '\x08' '{' '"' _ # ' '
    - @ '$' && / _ %
    ! ( '\t' @ | = >
    ; '\x08' '\'' + '$' ? '\x7f'
    , # '"' ~ | ) '\x07'
}

```

###### macro_railroad lib

#### 作用域

与 Rust 语言其余所有部分都不同的是，函数式宏在子模块中仍然可见。
宏在定义之后可见
```rs
mod a {
    // X!(); // undefined
}
macro_rules! X { () => {}; }
mod a {
    X!(); // defined
}
mod b {
    X!(); // defined
}
mod c {
    X!(); // defined
}
fn main() {}
```
##### #[macro_use] 属性

这个属性放置在宏定义所在的模块前 或者 extern crate 语句前。

在模块前加上 #[macro_use] 属性：导出该模块内的所有宏， 从而让导出的宏在所定义的模块结束之后依然可用。

#### 导入/导出

### 模式
#### 回调
```rs
macro_rules! call_with_larch {
    ($callback:ident) => { $callback!(larch) };
}

macro_rules! expand_to_larch {
    () => { larch };
}

macro_rules! recognize_tree {
    (larch) => { println!("#1, the Larch.") };
    (redwood) => { println!("#2, the Mighty Redwood.") };
    (fir) => { println!("#3, the Fir.") };
    (chestnut) => { println!("#4, the Horse Chestnut.") };
    (pine) => { println!("#5, the Scots Pine.") };
    ($($other:tt)*) => { println!("I don't know; some kind of birch maybe?") };
}

fn main() {
    recognize_tree!(expand_to_larch!()); // 无法直接使用 `expand_to_larch!` 的展开结果
    call_with_larch!(recognize_tree);    // 回调就是给另一个宏传入宏的名称 (`ident`)，而不是宏的结果
}

// 打印结果：
// I don't know; some kind of birch maybe?
// #1, the Larch. 
```

####  增量式 TT “撕咬机”
```rs
macro_rules! mixed_rules {
    () => {};
    (trace $name:ident; $($tail:tt)*) => {
        {
            println!(concat!(stringify!($name), " = {:?}"), $name);
            mixed_rules!($($tail)*);
        }
    };
    (trace $name:ident = $init:expr; $($tail:tt)*) => {
        {
            let $name = $init;
            println!(concat!(stringify!($name), " = {:?}"), $name);
            mixed_rules!($($tail)*);
        }
    };
}

```
“标记树撕咬机” (TT muncher) 是一种递归宏，其工作机制有赖于对输入的顺次、逐步处理 (incrementally processing) 。处理过程的每一步中，它都将匹配并移除（“撕咬”掉）输入头部 (start) 的一列标记 (tokens)，得到一些中间结果，然后再递归地处理输入剩下的尾部。

- 你只能匹配 macro_rules! 捕获到的字面值和语法结构。
- 你无法匹配不成对的标记组 (unbalanced group) 。

#### 内用规则

### 构件

#### AST 强制转换
在替换 tt 时，Rust 的解析器并不十分可靠。 当它期望得到某类特定的语法结构时， 如果摆在它面前的是一坨替换后的 tt 标记，就有可能出现问题。 解析器常常直接选择放弃解析，而非尝试去解析它们。 在这类情况中，就要用到 AST 强制转换（简称“强转”）。
```rs
#![allow(dead_code)]

macro_rules! as_expr { ($e:expr) => {$e} }
macro_rules! as_item { ($i:item) => {$i} }
macro_rules! as_pat  { ($p:pat)  => {$p} }
macro_rules! as_stmt { ($s:stmt) => {$s} }
macro_rules! as_ty   { ($t:ty)   => {$t} }

fn main() {
    as_item!{struct Dummy;}

    as_stmt!(let as_pat!(_): as_ty!(_) = as_expr!(42));
}
```
#### 计数
##### 反复替换
在宏中计数是一项让人吃惊的难搞的活儿。 最简单的方式是采用反复替换
```rs
macro_rules! replace_expr {
    ($_t:tt $sub:expr) => {$sub};
}

macro_rules! count_tts {
    ($($tts:tt)*) => {0usize $(+ replace_expr!($tts 1usize))*};
}

fn main() {
    assert_eq!(count_tts!(0 1 2), 3);
}
```
##### 递归
```rs
macro_rules! count_tts {
    () => {0usize};
    ($_head:tt $($tail:tt)*) => {1usize + count_tts!($($tail)*)};
}

fn main() {
    assert_eq!(count_tts!(0 1 2), 3);
}
```
##### 切片长度
第三种方法，是帮助编译器构建一个深度较小的 AST ，以避免栈溢出。 可以通过构造数组，并调用其 len 方法来做到。(slice length)
```rs
macro_rules! replace_expr {
    ($_t:tt $sub:expr) => {$sub};
}

macro_rules! count_tts {
    ($($tts:tt)*) => {<[()]>::len(&[$(replace_expr!($tts ())),*])};
}

fn main() {
    assert_eq!(count_tts!(0 1 2), 3);

    const N: usize = count_tts!(0 1 2);
    let array = [0; N];
    println!("{:?}", array);
}
```
##### 枚举计数
当你需要统计 互不相同的标识符 的数量时， 可以利用枚举体的 numeric cast 功能来达到统计成员（即标识符）个数。
```rs
macro_rules! count_idents {
    ($($idents:ident),* $(,)*) => {
        {
            #[allow(dead_code, non_camel_case_types)]
            enum Idents { $($idents,)* __CountIdentsLast } 
            const COUNT: u32 = Idents::__CountIdentsLast as u32;
            COUNT
        }
    };
}

fn main() {
    const COUNT: u32 = count_idents!(A, B, C);
    assert_eq!(COUNT, 3);
}
```

##### bit twiddling

```rs
macro_rules! count_tts {
    () => { 0 };
    ($odd:tt $($a:tt $b:tt)*) => { (count_tts!($($a)*) << 1) | 1 };
    ($($a:tt $even:tt)*) => { count_tts!($($a)*) << 1 };
}

fn main() {
    assert_eq!(count_tts!(0 1 2), 3);
}
```
#### 解析 Rust

重点在于宏的匹配方式 (matchers) ；展开的部分 （ Reference 里使用的术语叫做 transcribers ）

```rs
macro_rules! function_item_matcher {
    (

        $( #[$meta:meta] )*
    //  ^~~~attributes~~~~^
        $vis:vis fn $name:ident ( $( $arg_name:ident : $arg_ty:ty ),* $(,)? )
    //                          ^~~~~~~~~~~~~~~~argument list!~~~~~~~~~~~~~~^
            $( -> $ret_ty:ty )?
    //      ^~~~return type~~~^
            { $($tt:tt)* }
    //      ^~~~~body~~~~^
    ) => {
        $( #[$meta] )*
        $vis fn $name ( $( $arg_name : $arg_ty ),* ) $( -> $ret_ty )? { $($tt)* }
    }
}

function_item_matcher!(
   #[inline]
   #[cold]
   pub fn foo(bar: i32, baz: i32, ) -> String {
       format!("{} {}", bar, baz)
   }
);

fn main() {
    assert_eq!(foo(13, 37), "13 37");
}
```
##### 结构体

```rs
macro_rules! struct_item_matcher {
    // Unit-Struct
    (
        $( #[$meta:meta] )*
    //  ^~~~attributes~~~~^
        $vis:vis struct $name:ident;
    ) => {
        $( #[$meta] )*
        $vis struct $name;
    };

    // Tuple-Struct
    (
        $( #[$meta:meta] )*
    //  ^~~~attributes~~~~^
        $vis:vis struct $name:ident (
            $(
                $( #[$field_meta:meta] )*
    //          ^~~~field attributes~~~~^
                $field_vis:vis $field_ty:ty
    //          ^~~~~~a single field~~~~~~^
            ),*
        $(,)? );
    ) => {
        $( #[$meta] )*
        $vis struct $name (
            $(
                $( #[$field_meta] )*
                $field_vis $field_ty
            ),*
        );
    };

    // Named-Struct
    (
        $( #[$meta:meta] )*
    //  ^~~~attributes~~~~^
        $vis:vis struct $name:ident {
            $(
                $( #[$field_meta:meta] )*
    //          ^~~~field attributes~~~!^
                $field_vis:vis $field_name:ident : $field_ty:ty
    //          ^~~~~~~~~~~~~~~~~a single field~~~~~~~~~~~~~~~^
            ),*
        $(,)? }
    ) => {
        $( #[$meta] )*
        $vis struct $name {
            $(
                $( #[$field_meta] )*
                $field_vis $field_name : $field_ty
            ),*
        }
    }
}

struct_item_matcher!(
   #[allow(dead_code)]
   #[derive(Copy, Clone)]
   pub(crate) struct Foo { 
      pub bar: i32,
      baz: &'static str,
      qux: f32
   }
);
struct_item_matcher!(
   #[derive(Copy, Clone)]
   pub(crate) struct Bar;
);
struct_item_matcher!(
   #[derive(Clone)]
   pub(crate) struct Baz (i32, pub f32, String);
);
fn main() {
   let _: Foo = Foo { bar: 42, baz: "macros can be nice", qux: 3.14, };
   let _: Bar = Bar;
   let _: Baz = Baz(2, 0.1234, String::new());
}
```

##### 枚举体
```rs
macro_rules! enum_item_matcher {
    // tuple variant
    (@variant $variant:ident (
        $(
            $( #[$field_meta:meta] )*
    //      ^~~~field attributes~~~~^
            $field_vis:vis $field_ty:ty
    //      ^~~~~~a single field~~~~~~^
        ),* $(,)?
    //∨~~rest of input~~∨
    ) $(, $($tt:tt)* )? ) => {

        // process rest of the enum
        $( enum_item_matcher!(@variant $( $tt )*); )?
    };

    // named variant
    (@variant $variant:ident {
        $(
            $( #[$field_meta:meta] )*
    //      ^~~~field attributes~~~!^
            $field_vis:vis $field_name:ident : $field_ty:ty
    //      ^~~~~~~~~~~~~~~~~a single field~~~~~~~~~~~~~~~^
        ),* $(,)?
    //∨~~rest of input~~∨
    } $(, $($tt:tt)* )? ) => {
        // process rest of the enum
        $( enum_item_matcher!(@variant $( $tt )*); )?
    };

    // unit variant
    (@variant $variant:ident $(, $($tt:tt)* )? ) => {
        // process rest of the enum
        $( enum_item_matcher!(@variant $( $tt )*); )?
    };

    // trailing comma
    (@variant ,) => {};
    // base case
    (@variant) => {};

    // entry point
    (
        $( #[$meta:meta] )*
        $vis:vis enum $name:ident {
            $($tt:tt)*
        }
    ) => {
        enum_item_matcher!(@variant $($tt)*);
    };
}

enum_item_matcher!(
    #[derive(Copy, Clone)]
    pub(crate) enum Foo {
        Bar,
        Baz,
    }
);
enum_item_matcher!(
    #[derive(Copy, Clone)]
    pub(crate) enum Bar {
        Foo(i32, f32),
        Bar,
        Baz(),
    }
);
enum_item_matcher!(
    #[derive(Clone)]
    pub(crate) enum Baz {}
);

fn main() {}
```
## 过程宏
### 思路
过程宏采用 Rust 函数的形式，接受一个（或两个）标记流并输出一个标记流。
过程宏的核心只是一个从 proc-macro crate type 这种类型的库中所导出的公有函数，因此当编写多个过程宏时，你可以将它们全部放在一个 crate 中
```toml
[lib]
proc-macro = true

```

proc-macro 类型的 crate 会隐式链接到编译器提供的 proc_macro 库， proc_macro 库包含了开发过程宏所需的所有内容，并且它公开了两个最重要的类型：
1. TokenStream：它表示我们所熟知的标记树
2. Span：它表示源代码的一部分，主要用于错误信息的报告和卫生性，更多信息请阅读 卫生性和 Spans 一章



过程宏实际上存在三种不同的类型，每种类型的性质都略有不同。1

- 函数式：实现 $name！$input 功能的宏
```rs
#[proc_macro]
pub fn name(input: TokenStream) -> TokenStream {
    TokenStream::new()
}
```
- 属性式：实现 #[$input] 功能的属性
```rs
#[proc_macro_attribute]
pub fn name(attr: TokenStream, input: TokenStream) -> TokenStream {
    TokenStream::new()
}
```
- derive 式：实现 #[derive($name)] 功能的属性
```rs
#[proc_macro_derive(Name)]
pub fn my_derive(input: TokenStream) -> TokenStream {
    TokenStream::new()
} 
```
#### 函数式过程宏
```rs
use proc_macro::TokenStream;

#[proc_macro]
pub fn tlborm_fn_macro(input: TokenStream) -> TokenStream {
    input
}

```

过程宏更强大，因为它们可以任意修改其输入，并生成任何所需的输出，只要输出在 Rust 的语法范围内。
```rs
use tlborm_proc::tlborm_attribute;

fn foo() {
    tlborm_attribute!(be quick; time is mana);
}

```
#### 属性式过程宏
属性式过程宏定义了可添加到条目的的新外部属性。这种宏通过 #[attr] 或 #[attr(…)] 方式调用，其中 … 是任意标记树。
```rs
use proc_macro::TokenStream;

#[proc_macro_attribute]
pub fn tlborm_attribute(input: TokenStream, annotated_item: TokenStream) -> TokenStream {
    annotated_item
}

```

- 第一个参数是属性名称后面的带分隔符的标记树，不包括它周围的分隔符。如果只有属性名称（其后不带标记树，比如 #[attr]），则这个参数的值为空。
- 第二个参数是添加了该过程宏属性的条目，但不包括该过程宏所定义的属性。因为这是一个 active 属性，在传递给过程宏之前，该属性将从条目中剥离出来。

#### derive 式过程宏
derive 式过程宏1为 derive 属性定义了新的输入。这种宏通过将其名称提供给 derive 属性的输入来调用，例如 #[derive(TlbormDerve)]。
```rs
use proc_macro::TokenStream;

#[proc_macro_derive(TlbormDerive)]
pub fn tlborm_derive(input: TokenStream) -> TokenStream {
    TokenStream::new()
}

```

derive 宏又有一点特殊，因为它可以添加仅在条目定义范围内可见的附加属性。

这些属性被称为派生宏辅助属性 (derive macro helper attributes) ，并且是惰性的(inert)。

辅助属性的目的是在每个结构体字段或枚举体成员的基础上为 derive 宏提供额外的可定制性。