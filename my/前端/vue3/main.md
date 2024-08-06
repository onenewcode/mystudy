# ES6模块化与异步编程高级用法

## ES6模块化
### node.js 中如何实现模块化
node.js 遵循了 CommonJS 的模块化规范。其中：
⚫ 导入其它模块使用 require() 方法
⚫ 模块对外共享成员使用 module.exports 对象
### Promise
Promise 的基本概念
① Promise 是一个构造函数
⚫ 我们可以创建 Promise 的实例 const p = new Promise()
⚫ new 出来的 Promise 实例对象，代表一个异步操作
② Promise.prototype 上包含一个 .then() 方法
⚫ 每一次 new Promise() 构造函数得到的实例对象，
⚫ 都可以通过原型链的方式访问到 .then() 方法，例如 p.then()
③ .then() 方法用来预先指定成功和失败的回调函数
⚫ p.then(成功的回调函数，失败的回调函数)
⚫ p.then(result => { }, error => { })
⚫ 调用 .then() 方法时，成功的回调函数是必选的、失败的回调函数是可选的
 then-fs 的基本使用
调用 then-fs 提供的 readFile() 方法，可以异步地读取文件的内容，它的返回值是 Promise 的实例对象。因此可以调用 .then() 方法为每个 Promise 异步操作指定成功和失败之后的回调函数。
**.then() 方法的特性**
如果上一个 .then() 方法中返回了一个新的 Promise 实例对象，则可以通过下一个 .then() 继续进行处理。

##### Promise.all() 方法
Promise.all() 方法会发起并行的 Promise 异步操作，等所有的异步操作全部结束后才会执行下一步的 .then 操作（等待机制）。
#####  Promise.race() 方法
Promise.race() 方法会发起并行的 Promise 异步操作，只要任何一个异步操作完成，就立即执行下一步的.then 操作（赛跑机制）
#### async/await
① 如果在 function 中使用了 await，则 function 必须被 async 修饰
② 在 async 方法中，第一个 await 之前的代码会同步执行，await 之后的代码会异步执行
#### EventLoop
为了防止某个耗时任务导致程序假死的问题，JavaScript 把待执行的任务分为了两类：
① 同步任务（synchronous）
⚫ 又叫做非耗时任务，指的是在主线程上排队执行的那些任务
⚫ 只有前一个任务执行完毕，才能执行后一个任务
② 异步任务（asynchronous）
⚫ 又叫做耗时任务，异步任务由 JavaScript 委托给宿主环境进行执行
⚫ 当异步任务执行完成后，会通知 JavaScript 主线程执行异步任务的回调函数
#### 宏任务和微任务
① 宏任务（macrotask）
⚫ 异步 Ajax 请求、
⚫ setTimeout、setInterval、
⚫ 文件操作
⚫ 其它宏任务
② 微任务（microtask）
⚫ Promise.then、.catch 和 .finally
⚫ process.nextTick
⚫ 其它微任务

# TS

## 第一个 TypeScript 程序
### 编写 TS 程序
src/helloworld.ts
```ts
function greeter (person) {
  return 'Hello, ' + person
}

let user = 'Yee'

console.log(greeter(user))
```
### 手动编译代码
我们使用了 .ts 扩展名，但是这段代码仅仅是 JavaScript 而已。

在命令行上，运行 TypeScript 编译器：
```s
tsc helloworld.ts
```
输出结果为一个 helloworld.js 文件，它包含了和输入文件中相同的 JavsScript 代码。

在命令行上，通过 Node.js 运行这段代码：
```s
node helloworld.js
```
控制台输出：

Hello, Yee
### vscode自动编译
1). 生成配置文件tsconfig.json
    tsc --init
2). 修改tsconfig.json配置
    "outDir": "./js",
    "strict": false,    
3). 启动监视任务: 
    终端 -> 运行任务 -> 监视tsconfig.json
### 类型注解
接下来让我们看看 TypeScript 工具带来的高级功能。 给 person 函数的参数添加 : string 类型注解，如下：
```ts
function greeter (person: string) {
  return 'Hello, ' + person
}

let user = 'Yee'

console.log(greeter(user))
```


### 接口
让我们继续扩展这个示例应用。这里我们使用接口来描述一个拥有 firstName 和 lastName 字段的对象。 在 TypeScript 里，只在两个类型内部的结构兼容，那么这两个类型就是兼容的。 这就允许我们在实现接口时候只要保证包含了接口要求的结构就可以，而不必明确地使用 implements 语句。
```ts
interface Person {
  firstName: string
  lastName: string
}

function greeter (person: Person) {
  return 'Hello, ' + person.firstName + ' ' + person.lastName
}

let user = {
  firstName: 'Yee',
  lastName: 'Huang'
}

console.log(greeter(user))
```
### 类
最后，让我们使用类来改写这个例子。 TypeScript 支持 JavaScript 的新特性，比如支持基于类的面向对象编程。

让我们创建一个 User 类，它带有一个构造函数和一些公共字段。因为类的字段包含了接口所需要的字段，所以他们能很好的兼容。

还要注意的是，我在类的声明上会注明所有的成员变量，这样比较一目了然。
```ts
class User {
  fullName: string
  firstName: string
  lastName: string

  constructor (firstName: string, lastName: string) {
    this.firstName = firstName
    this.lastName = lastName
    this.fullName = firstName + ' ' + lastName
  }
}

interface Person {
  firstName: string
  lastName: string
}

function greeter (person: Person) {
  return 'Hello, ' + person.firstName + ' ' + person.lastName
}

let user = new User('Yee', 'Huang')

console.log(greeter(user))
```
重新运行 tsc greeter.ts，你会看到 TypeScript 里的类只是一个语法糖，本质上还是 JavaScript 函数的实现。




## 使用webpack打包TS

### 下载依赖
**yarn**
```s
yarn add -D typescript
yarn add -D webpack webpack-cli
yarn add -D webpack-dev-server
yarn add -D html-webpack-plugin clean-webpack-plugin
yarn add -D ts-loader
yarn add -D cross-env
```
**npm**
```s
npm install -D typescript
npm install -D webpack webpack-cli
npm install -D webpack-dev-server
npm install -D html-webpack-plugin clean-webpack-plugin
npm install -D ts-loader
npm install -D cross-env
```
### 入口JS: src/main.ts
// import './01_helloworld'
```ts
document.write('Hello Webpack TS!')
```
### index页面: public/index.html
```ts
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>webpack & TS</title>
</head>
<body>
  
</body>
</html>
```

### build/webpack.config.js
```ts
const {CleanWebpackPlugin} = require('clean-webpack-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const path = require('path')

const isProd = process.env.NODE_ENV === 'production' // 是否生产环境

function resolve (dir) {
  return path.resolve(__dirname, '..', dir)
}

module.exports = {
  mode: isProd ? 'production' : 'development',
  entry: {
    app: './src/main.ts'
  },

  output: {
    path: resolve('dist'),
    filename: '[name].[contenthash:8].js'
  },

  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        include: [resolve('src')]
      }
    ]
  },

  plugins: [
    new CleanWebpackPlugin({
    }),

    new HtmlWebpackPlugin({
      template: './public/index.html'
    })
  ],

  resolve: {
    extensions: ['.ts', '.tsx', '.js']
  },

  devtool: isProd ? 'cheap-module-source-map' : 'cheap-module-eval-source-map',

  devServer: {
    host: 'localhost', // 主机名
    stats: 'errors-only', // 打包日志输出输出错误信息
    port: 8081,
    open: true
  },
}
```
### 配置打包命令
"dev": "cross-env NODE_ENV=development webpack-dev-server --config build/webpack.config.js",
"build": "cross-env NODE_ENV=production webpack --config build/webpack.config.js"
### 运行与打包
```
yarn dev
yarn build
```
```
npm run dev
```
## ts基本用法
### 基础类型
TypeScript 支持与 JavaScript 几乎相同的数据类型，此外还提供了实用的枚举类型方便我们使用。

#### 布尔值
最基本的数据类型就是简单的 true/false 值，在JavaScript 和 TypeScript 里叫做 boolean（其它语言中也一样）。
```ts
let isDone: boolean = false;
isDone = true;
// isDone = 2 // error
```
#### 数字
和 JavaScript 一样，TypeScript 里的所有数字都是浮点数。 这些浮点数的类型是 number。 除了支持十进制和十六进制字面量，TypeScript 还支持 ECMAScript 2015中引入的二进制和八进制字面量。
```ts
let a1: number = 10 // 十进制
let a2: number = 0b1010  // 二进制
let a3: number = 0o12 // 八进制
let a4: number = 0xa // 十六进制
```
#### 字符串
JavaScript 程序的另一项基本操作是处理网页或服务器端的文本数据。 像其它语言里一样，我们使用 string 表示文本数据类型。 和 JavaScript 一样，可以使用双引号（"）或单引号（'）表示字符串。
```ts
let name:string = 'tom'
name = 'jack'
// name = 12 // error
let age:number = 12
const info = `My name is ${name}, I am ${age} years old!`
```
#### undefined 和 null
TypeScript 里，undefined 和 null 两者各自有自己的类型分别叫做 undefined 和 null。 它们的本身的类型用处不是很大：
```ts
let u: undefined = undefined
let n: null = null
默认情况下 null 和 undefined 是所有类型的子类型。 就是说你可以把 null 和 undefined 赋值给 number 类型的变量。
```

#### 数组
TypeScript 像 JavaScript 一样可以操作数组元素。 有两种方式可以定义数组。 第一种，可以在元素类型后面接上[]，表示由此类型元素组成的一个数组：
```ts
let list1: number[] = [1, 2, 3]
第二种方式是使用数组泛型，Array<元素类型>：

let list2: Array<number> = [1, 2, 3]
```
#### 元组 Tuple
元组类型允许表示一个已知元素数量和类型的数组，各元素的类型不必相同。 比如，你可以定义一对值分别为 string 和 number 类型的元组。
```ts
let t1: [string, number]
t1 = ['hello', 10] // OK
t1 = [10, 'hello'] // Error
当访问一个已知索引的元素，会得到正确的类型：

console.log(t1[0].substring(1)) // OK
console.log(t1[1].substring(1)) // Error, 'number' 不存在 'substring' 方法
``` 
#### 枚举
enum 类型是对 JavaScript 标准数据类型的一个补充。 使用枚举类型可以为一组数值赋予友好的名字。
```ts
enum Color {
  Red,
  Green,
  Blue
}
// 枚举数值默认从0开始依次递增
// 根据特定的名称得到对应的枚举数值
let myColor: Color = Color.Green  // 0
console.log(myColor, Color.Red, Color.Blue)
默认情况下，从 0 开始为元素编号。 你也可以手动的指定成员的数值。 例如，我们将上面的例子改成从 1 开始编号：

enum Color {Red = 1, Green, Blue}
let c: Color = Color.Green
或者，全部都采用手动赋值：

enum Color {Red = 1, Green = 2, Blue = 4}
let c: Color = Color.Green
枚举类型提供的一个便利是你可以由枚举的值得到它的名字。 例如，我们知道数值为 2，但是不确定它映射到 Color 里的哪个名字，我们可以查找相应的名字：

enum Color {Red = 1, Green, Blue}
let colorName: string = Color[2]

console.log(colorName)  // 'Green'
```

#### any
有时候，我们会想要为那些在编程阶段还不清楚类型的变量指定一个类型。 这些值可能来自于动态的内容，比如来自用户输入或第三方代码库。 这种情况下，我们不希望类型检查器对这些值进行检查而是直接让它们通过编译阶段的检查。 那么我们可以使用 any 类型来标记这些变量：
```ts
let notSure: any = 4
notSure = 'maybe a string'
notSure = false // 也可以是个 boolean
在对现有代码进行改写的时候，any 类型是十分有用的，它允许你在编译时可选择地包含或移除类型检查。并且当你只知道一部分数据的类型时，any 类型也是有用的。 比如，你有一个数组，它包含了不同的类型的数据：

let list: any[] = [1, true, 'free']

list[1] = 100
```
#### void
某种程度上来说，void 类型像是与 any 类型相反，它表示没有任何类型。 当一个函数没有返回值时，你通常会见到其返回值类型是 void：
```ts
/* 表示没有任何类型, 一般用来说明函数的返回值不能是undefined和null之外的值 */
function fn(): void {
  console.log('fn()')
  // return undefined
  // return null
  // return 1 // error
}
声明一个 void 类型的变量没有什么大用，因为你只能为它赋予 undefined 和 null：

let unusable: void = undefined
```
#### object
object 表示非原始类型，也就是除 number，string，boolean之外的类型。

使用 object 类型，就可以更好的表示像 Object.create 这样的 API。例如：
```ts
function fn2(obj:object):object {
  console.log('fn2()', obj)
  return {}
  // return undefined
  // return null
}
console.log(fn2(new String('abc')))
// console.log(fn2('abc') // error
console.log(fn2(String))
```
#### 联合类型
联合类型（Union Types）表示取值可以为多种类型中的一种
需求1: 定义一个一个函数得到一个数字或字符串值的字符串形式值
```ts
function toString2(x: number | string) : string {
  return x.toString()
}
需求2: 定义一个一个函数得到一个数字或字符串值的长度

function getLength(x: number | string) {

  // return x.length // error

  if (x.length) { // error
    return x.length
  } else {
    return x.toString().length
  }
}
```
#### 类型断言
通过类型断言这种方式可以告诉编译器，“相信我，我知道自己在干什么”。 类型断言好比其它语言里的类型转换，但是不进行特殊的数据检查和解构。 它没有运行时的影响，只是在编译阶段起作用。 TypeScript 会假设你，程序员，已经进行了必须的检查。

类型断言有两种形式。 其一是“尖括号”语法, 另一个为 as 语法
```ts
/* 
类型断言(Type Assertion): 可以用来手动指定一个值的类型
语法:
    方式一: <类型>值
    方式二: 值 as 类型  tsx中只能用这种方式
*/

/* 需求: 定义一个函数得到一个字符串或者数值数据的长度 */
function getLength(x: number | string) {
  if ((<string>x).length) {
    return (x as string).length
  } else {
    return x.toString().length
  }
}
console.log(getLength('abcd'), getLength(1234))
```
#### 类型推断
类型推断: TS会在没有明确的指定类型的时候推测出一个类型有下面2种情况: 1. 定义变量时赋值了, 推断为对应的类型. 2. 定义变量时没有赋值, 推断为any类型
```ts
/* 定义变量时赋值了, 推断为对应的类型 */
let b9 = 123 // number
// b9 = 'abc' // error

/* 定义变量时没有赋值, 推断为any类型 */
let b10  // any类型
b10 = 123
b10 = 'abc'
```
### 接口
TypeScript 的核心原则之一是对值所具有的结构进行类型检查。我们使用接口（Interfaces）来定义对象的类型。接口是对象的状态(属性)和行为(方法)的抽象(描述)

#### 接口初探
```ts
/* 
在 TypeScript 中，我们使用接口（Interfaces）来定义对象的类型
接口: 是对象的状态(属性)和行为(方法)的抽象(描述)
接口类型的对象
    多了或者少了属性是不允许的
    可选属性: ?
    只读属性: readonly
*/



// 定义人的接口
interface IPerson {
  id: number
  name: string
  age: number
  sex: string
}

const person1: IPerson = {
  id: 1,
  name: 'tom',
  age: 20,
  sex: '男'
}
类型检查器会查看对象内部的属性是否与IPerson接口描述一致, 如果不一致就会提示类型错误。
```
```ts
interface IPerson {
  readonly id: number
  name: string
  age: number
  sex?: string
}
```
**readonly vs const**
最简单判断该用 readonly 还是 const 的方法是看要把它做为变量使用还是做为一个属性。 做为变量使用的话用 const，若做为属性则使用 readonly。

#### 函数类型
接口能够描述 JavaScript 中对象拥有的各种各样的外形。 除了描述带有属性的普通对象外，接口也可以描述函数类型。

为了使用接口表示函数类型，我们需要给接口定义一个调用签名。它就像是一个只有参数列表和返回值类型的函数定义。参数列表里的每个参数都需要名字和类型。
```ts
/* 
接口可以描述函数类型(参数的类型与返回的类型)
*/

interface SearchFunc {
  (source: string, subString: string): boolean
}
这样定义后，我们可以像使用其它接口一样使用这个函数类型的接口。 下例展示了如何创建一个函数类型的变量，并将一个同类型的函数赋值给这个变量。

const mySearch: SearchFunc = function (source: string, sub: string): boolean {
  return source.search(sub) > -1
}

console.log(mySearch('abcd', 'bc'))
```

#### 类实现接口
与 C# 或 Java 里接口的基本作用一样，TypeScript 也能够用它来明确的强制一个类去符合某种契约。
```ts
/* 
类类型: 实现接口
1. 一个类可以实现多个接口
2. 一个接口可以继承多个接口
*/

interface Alarm {
  alert(): any;
}

interface Light {
  lightOn(): void;
  lightOff(): void;
}

class Car implements Alarm {
  alert() {
      console.log('Car alert');
  }
}
```

#### 接口继承接口
和类一样，接口也可以相互继承。 这让我们能够从一个接口里复制成员到另一个接口里，可以更灵活地将接口分割到可重用的模块里。

interface LightableAlarm extends Alarm, Light {

}
### 类

#### 继承
在 TypeScript 里，我们可以使用常用的面向对象模式。 基于类的程序设计中一种最基本的模式是允许使用继承来扩展现有的类。

看下面的例子：
```ts
/* 
类的继承
*/

class Animal {
  run (distance: number) {
    console.log(`Animal run ${distance}m`)
  }
}

class Dog extends Animal {
  cry () {
    console.log('wang! wang!')
  }
}

const dog = new Dog()
dog.cry() 
dog.run(100) // 可以调用从父中继承得到的方法
```
#### 默认为 public
#### 理解 private
当成员被标记成 private 时，它就不能在声明它的类的外部访问。

#### 理解 protected
protected 修饰符与 private 修饰符的行为很相似，但有一点不同，protected成员在派生类中仍然可以访问。例如：

#### 参数属性
在上面的例子中，我们必须在 Person 类里定义一个只读成员 name 和一个参数为 name 的构造函数，并且立刻将 name 的值赋给 this.name，这种情况经常会遇到。 参数属性可以方便地让我们在一个地方定义并初始化一个成员。 下面的例子是对之前 Person 类的修改版，使用了参数属性：
```ts
class Person2 {
  constructor(readonly name: string) {
  }
}

const p = new Person2('jack')
console.log(p.name)
```
注意看我们是如何舍弃参数 name，仅在构造函数里使用 readonly name: string 参数来创建和初始化 name 成员。 我们把声明和赋值合并至一处。

参数属性通过给构造函数参数前面添加一个访问限定符来声明。使用 private 限定一个参数属性会声明并初始化一个私有成员；对于 public 和 protected 来说也是一样。

#### 存取器
TypeScript 支持通过 getters/setters 来截取对对象成员的访问。 它能帮助你有效的控制对对象成员的访问。

下面来看如何把一个简单的类改写成使用 get 和 set。 首先，我们从一个没有使用存取器的例子开始。
```ts
class Person {
  firstName: string = 'A'
  lastName: string = 'B'
  get fullName () {
    return this.firstName + '-' + this.lastName
  }
  set fullName (value) {
    const names = value.split('-')
    this.firstName = names[0]
    this.lastName = names[1]
  }
}

const p = new Person()
console.log(p.fullName)

p.firstName = 'C'
p.lastName =  'D'
console.log(p.fullName)

p.fullName = 'E-F'
console.log(p.firstName, p.lastName)
```
#### 静态属性
到目前为止，我们只讨论了类的实例成员，那些仅当类被实例化的时候才会被初始化的属性。 我们也可以创建类的静态成员，这些属性存在于类本身上面而不是类的实例上。 在这个例子里，我们使用 static 定义 origin，因为它是所有网格都会用到的属性。 每个实例想要访问这个属性的时候，都要在 origin 前面加上类名。 如同在实例属性上使用 this.xxx 来访问属性一样，这里我们使用 Grid.xxx 来访问静态属性。
```ts
/* 
静态属性, 是类对象的属性
非静态属性, 是类的实例对象的属性
*/

class Person {
  name1: string = 'A'
  static name2: string = 'B'
}

console.log(Person.name2)
console.log(new Person().name1)
```
#### 抽象类
抽象类做为其它派生类的基类使用。 它们不能被实例化。不同于接口，抽象类可以包含成员的实现细节。 abstract 关键字是用于定义抽象类和在抽象类内部定义抽象方法。

```ts
/* 
抽象类
  不能创建实例对象, 只有实现类才能创建实例
  可以包含未实现的抽象方法
*/

abstract class Animal {

  abstract cry ()

  run () {
    console.log('run()')
  }
}

class Dog extends Animal {
  cry () {
    console.log(' Dog cry()')
  }
}

const dog = new Dog()
dog.cry()
dog.run()
```

### 其它
#### 声明文件
当使用第三方库时，我们需要引用它的声明文件，才能获得对应的代码补全、接口提示等功能
假如我们想使用第三方库 jQuery，一种常见的方式是在 html 中通过 &lt;script&gt;标签引入 jQuery，然后就可以使用全局变量 $ 或 jQuery 了。
但是在 ts 中，编译器并不知道 $ 或 jQuery 是什么东西
```ts
/* 
当使用第三方库时，我们需要引用它的声明文件，才能获得对应的代码补全、接口提示等功能。
声明语句: 如果需要ts对新的语法进行检查, 需要要加载了对应的类型说明代码
  declare var jQuery: (selector: string) => any;
声明文件: 把声明语句放到一个单独的文件（jQuery.d.ts）中, ts会自动解析到项目中所有声明文件
下载声明文件: npm install @types/jquery --save-dev
*/

jQuery('#foo');
// ERROR: Cannot find name 'jQuery'.
这时，我们需要使用 declare var 来定义它的类型

declare var jQuery: (selector: string) => any;

jQuery('#foo');
declare var 并没有真的定义一个变量，只是定义了全局变量 jQuery 的类型，仅仅会用于编译时的检查，在编译结果中会被删除。它编译结果是：

jQuery('#foo');
一般声明文件都会单独写成一个 xxx.d.ts 文件

创建 01_jQuery.d.ts, 将声明语句定义其中, TS编译器会扫描并加载项目中所有的TS声明文件

declare var jQuery: (selector: string) => any;
很多的第三方库都定义了对应的声明文件库, 库文件名一般为 @types/xxx, 可以在 https://www.npmjs.com/package/package 进行搜索
```
有的第三库在下载时就会自动下载对应的声明文件库(比如: webpack),有的可能需要单独下载(比如jQuery/react)

#### 内置对象
JavaScript 中有很多内置对象，它们可以直接在 TypeScript 中当做定义好了的类型。

内置对象是指根据标准在全局作用域（Global）上存在的对象。这里的标准是指 ECMAScript 和其他环境（比如 DOM）的标准。

ECMAScript 的内置对象
Boolean
Number
String
Date
RegExp
Error
```ts
/* 1. ECMAScript 的内置对象 */
let b: Boolean = new Boolean(1)
let n: Number = new Number(true)
let s: String = new String('abc')
let d: Date = new Date()
let r: RegExp = /^1/
let e: Error = new Error('error message')
b = true
// let bb: boolean = new Boolean(2)  // error
BOM 和 DOM 的内置对象
Window
Document
HTMLElement
DocumentFragment
Event
NodeList

const div: HTMLElement = document.getElementById('test')
const divs: NodeList = document.querySelectorAll('div')
document.addEventListener('click', (event: MouseEvent) => {
  console.dir(event.target)
})
const fragment: DocumentFragment = document.createDocumentFragment()
```
# vue简介
## vue 的指令与过滤器
指令（Directives）是 vue 为开发者提供的模板语法，用于辅助开发者渲染页面的基本结构。
vue 中的指令按照不同的用途可以分为如下 6 大类：
① 内容渲染指令
② 属性绑定指令
③ 事件绑定指令
④ 双向绑定指令
⑤ 条件渲染指令
⑥ 列表渲染指令
###  内容渲染指令
#### v-text
v-text 指令会覆盖元素内默认的值
#### {{ }} 语法
vue 提供的 {{ }} 语法，专门用来解决 v-text 会覆盖默认文本内容的问题。这种 {{ }} 语法的专业名称是插值表达式（英文名为：Mustache）。
#### v-html
v-text 指令和插值表达式只能渲染纯文本内容。如果要把包含 HTML 标签的字符串渲染为页面的 HTML 元素，则需要用到 v-html 这个指令：
### 属性绑定指令
#### v-bind
由于 v-bind 指令在开发中使用频率非常高，因此，vue 官方为其提供了简写形式（简写为英文的 : ）

#### 使用 Javascript 表达
在 vue 提供的模板渲染语法中，除了支持绑定简单的数据值之外，还支持 Javascript 表达式的运算
### 事件绑定指令
vue 提供了 v-on 事件绑定指令，用来辅助程序员为 DOM 元素绑定事件监听。
通过 v-on 绑定的事件处理函数，需要在 methods 节点中进行声明：
由于 v-on 指令在开发中使用频率非常高，因此，vue 官方为其提供了简写形式（简写为英文的 @ ）
同样可以接收到事件对象 event，
在使用 v-on 指令绑定事件时，可以使用 ( ) 进行传参
##### $event
$event 是 vue 提供的特殊变量，用来表示原生的事件参数对象 event。$event 可以解决事件参数对象 event 被覆盖的问题
##### 事件修饰符
在事件处理函数中调用 preventDefault() 或 stopPropagation() 是非常常见的需求。因此，vue 提供了事件修饰符的概念，来辅助程序员更方便的对事件的触发进行控制。
##### 按键修饰符
在监听键盘事件时，我们经常需要判断详细的按键。此时，可以为键盘相关的事件添加按键修饰符

#### 双向绑定指令
vue 提供了 v-model 双向数据绑定指令，用来辅助开发者在不操作 DOM 的前提下，快速获取表单的数据
v-model 指令只能配合表单元素一起使用

##### v-model 指令的修饰符
为了方便对用户输入的内容进行处理，vue 为 v-model 指令提供了 3 个修饰符

####  条件渲染指令
条件渲染指令用来辅助开发者按需控制 DOM 的显示与隐藏。
##### 条件渲染指令用来辅助开发者按需控制 DOM 的显示与隐藏。

实现原理不同：
⚫ v-if 指令会动态地创建或移除 DOM 元素，从而控制元素在页面上的显示与隐藏；
⚫ v-show 指令会动态为元素添加或移除 style="display: none;" 样式，从而控制元素的显示与隐藏；
性能消耗不同：
v-if 有更高的切换开销，而 v-show 有更高的初始渲染开销。
⚫ 如果需要非常频繁地切换，则使用 v-show 较好
⚫ 如果在运行时条件很少改变，则使用 v-if 较好

#### 列表渲染指令
vue 提供了 v-for 指令，用来辅助开发者基于一个数组来循环渲染相似的 UI 结构。
v-for 指令需要使用 item in items 的特殊语法，其中：
⚫ items 是待循环的数组
⚫ item 是当前的循环项

### 过滤器
在创建 vue 实例期间，可以在 filters 节点中定义过滤器
过滤器（Filters）是 vue 为开发者提供的功能，常用于文本的格式化。过滤器可以用在两个地方：插值表达式和 v-bind 属性绑定。过滤器应该被添加在 JavaScript 表达式的尾部，由“管道符”进行调用


#### 私有过滤器和全局过滤器
在 filters 节点下定义的过滤器，称为“私有过滤器”，因为它只能在当前 vm 实例所控制的 el 区域内使用。如果希望在多个 vue 实例之间共享过滤器，则可以按照如下的格式定义全局过滤器




















#  创建vue3项目
## 使用 vue-cli 创建
文档: https://cli.vuejs.org/zh/guide/creating-a-project.html#vue-create

## 安装或者升级
```s
npm install -g @vue/cli
## 保证 vue cli 版本在 4.5.0 以上
vue --version
## 创建项目
vue create my-project
然后的步骤

Please pick a preset - 选择 Manually select features
Check the features needed for your project - 选择上 TypeScript ，特别注意点空格是选择，点回车是下一步
Choose a version of Vue.js that you want to start the project with - 选择 3.x (Preview)
Use class-style component syntax - 直接回车
Use Babel alongside TypeScript - 直接回车
Pick a linter / formatter config - 直接回车
Use history mode for router? - 直接回车
Pick a linter / formatter config - 直接回车
Pick additional lint features - 直接回车
Where do you prefer placing config for Babel, ESLint, etc.? - 直接回车
Save this as a preset for future projects? - 直接回车
```
##  使用 vite 创建
文档: https://v3.cn.vuejs.org/guide/installation.html

vite 是一个由原生 ESM 驱动的 Web 开发构建工具。在开发环境下基于浏览器原生 ES imports 开发，

它做到了***本地快速开发启动***, 在生产环境下基于 Rollup 打包。

快速的冷启动，不需要等待打包操作；
即时的热模块更新，替换性能和模块数量的解耦让更新飞起；
真正的按需编译，不再等待整个应用编译完成，这是一个巨大的改变。

npm init vite-app <project-name>
cd &lt;project-name&gt;
npm install
npm run dev

## 如果想早点开始 Vue 3 的世界，可以通过以下命令直接创建一个启动项目：

```bash
# 全局安装脚手架
npm install -g create-preset

# 使用 `vue3-ts-vite` 模板创建一个名为 `hello-vue3` 的项目
preset init hello-vue3 --template vue3-ts-vite
```
# 单组件编写
## setup
setup 函数，它是一个组件选项，在创建组件之前执行，一旦 props 被解析，并作为组合式 API 的入口点。
基本语法
```ts
// 这是一个基于 TypeScript 的 Vue 组件
import { defineComponent } from 'vue'

export default defineComponent({
  setup(props, context) {
    // 在这里声明数据，或者编写函数并在这里执行它

    return {
      // 需要给 `<template />` 用的数据或函数，在这里 `return` 出去
    }
  },
})
```
### setup 的参数使用
setup 函数包含了两个入参：
|参数       |	类型           |	含义        |	            是否必传|
|------------|---------------|--------------|--------------|
|props      |	object          |	由父组件传递下来的数据|	否|
|context	  |object           |	组件的执行上下文|	否|
第一个参数 props ：它是响应式的，当父组件传入新的数据时，它将被更新。


第二个参数 context ：context 只是一个普通的对象，它暴露三个组件的 Property ：
|属性	|类型	|作用|
|------|---------|--------|
|attrs	|非响应式对象	|未在 Props 里定义的属性都将变成 Attrs|
|slots	|非响应式对象	|组件插槽，用于接收父组件传递进来的模板内容|
|emit	|方法	|触发父组件绑定下来的事件|
因为 context 只是一个普通对象，所以可以直接使用 ES6 解构。

平时使用可以通过直接传入 { emit } ，即可用 emit('xxx') 来代替使用 context.emit('xxx')，另外两个功能也是如此。

但是 attrs 和 slots 请保持 attrs.xxx、slots.xxx 的方式来使用其数据，不要进行解构，虽然这两个属性不是响应式对象，但对应的数据会随组件本身的更新而更新。


## defineComponent 的作用
defineComponent 是 Vue 3 推出的一个全新 API ，可用于对 TypeScript 代码的类型推导，帮助开发者简化掉很多编码过程中的类型声明。

比如，原本需要这样才可以使用 setup 函数：

```ts
import { Slots } from 'vue'

// 声明 `props` 和 `return` 的数据类型
interface Data {
  [key: string]: unknown
}

// 声明 `context` 的类型
interface SetupContext {
  attrs: Data
  slots: Slots
  emit: (event: string, ...args: unknown[]) => void
}

// 使用的时候入参要加上声明， `return` 也要加上声明
export default {
  setup(props: Data, context: SetupContext): Data {
    // ...

    return {
      // ...
    }
  },
}
```
每个组件都这样进行类型声明，会非常繁琐，如果使用了 defineComponent ，就可以省略这些类型声明：

```ts
import { defineComponent } from 'vue'

// 使用 `defineComponent` 包裹组件的内部逻辑
export default defineComponent({
  setup(props, context) {
    // ...

    return {
      // ...
    }
  },
})
```
代码量瞬间大幅度减少，只要是 Vue 本身的 API ， defineComponent 都可以自动推导其类型，这样开发者在编写组件的过程中，只需要维护自己定义的数据类型就可以了，可专注于业务。

## 组件的生命周期
在了解了 Vue 3 组件的两个前置知识点后，不着急写组件，还需要先了解组件的生命周期，这个知识点非常重要，只有理解并记住组件的生命周期，才能够灵活的把控好每一处代码的执行，使程序的运行结果可以达到预期。

### 升级变化
Vue 2 的生命周期写法名称是 Options API （选项式 API ）， Vue 3 新的生命周期写法名称是 Composition API （组合式 API ）。
Vue 3 组件默认支持 Options API ，而 Vue 2 可以通过 @vue/composition-api 插件获得 Composition API 的功能支持（其中 Vue 2.7 版本内置了该插件， 2.6 及以下的版本需要单独安装）。

为了减少理解成本，笔者将从读者的使用习惯上，使用 “ Vue 2 的生命周期” 代指 Options API 写法，用 “ Vue 3 的生命周期” 代指 Composition API 写法。

关于 Vue 生命周期的变化，可以从下表直观地了解：
|----------|----------|-------------------|
|Vue 2 生命周期|	Vue 3 生命周期|	执行时间说明|
|beforeCreate	|setup	|组件创建前执行|
|created	|setup|	组件创建后执行|
|beforeMount|	onBeforeMount	|组件挂载到节点上之前执行|
|mounted	|onMounted	|组件挂载完成后执行|
|beforeUpdate|	onBeforeUpdate	|组件更新之前执行|
|updated	|onUpdated|	组件更新完成之后执行|
|beforeDestroy	|onBeforeUnmount	|组件卸载之前执行|
|destroyed	|onUnmounted|	组件卸载完成后执行|
|errorCaptured	|onErrorCaptured|	当捕获一个来自子孙组件的异常时激活钩子函数|



|Vue 2 生命周期	|Vue 3 生命周期	|执行时间说明|
|activated	|onActivated	|被激活时执行|
|deactivated	|onDeactivated	|切换组件后，原组件消失前执行|
### 使用 3.x 的生命周期
在 Vue 3 的 Composition API 写法里，每个生命周期函数都要先导入才可以使用，并且所有生命周期函数统一放在 setup 里运行。

如果需要达到 Vue 2 的 beforeCreate 和 created 生命周期的执行时机，直接在 setup 里执行函数即可。

以下是几个生命周期的执行顺序对比：

```ts
import { defineComponent, onBeforeMount, onMounted } from 'vue'

export default defineComponent({
  setup() {
    console.log(1)

    onBeforeMount(() => {
      console.log(2)
    })

    onMounted(() => {
      console.log(3)
    })

    console.log(4)
  },
})
```
最终将按照生命周期的顺序输出：

js
// 1
// 4
// 2
// 3
## 组件的基本写法

### 了解 Vue 3
在 Vue 3 ，至少有以下六种写法可以声明 TypeScript 组件：

其中 defineComponent + Composition API + Template 的组合是 Vue 官方最为推荐的组件声明方式，本书接下来的内容都会以这种写法作为示范案例，也推荐开发者在学习的过程中，使用该组合进行入门。

下面看看如何使用 Composition API 编写一个最简单的 Hello World 组件：
```ts
<!-- Template 代码和 Vue 2 一样 -->
<template>
  <p class="msg">{{ msg }}</p>
</template>

<!-- Script 代码需要使用 Vue 3 的新写法-->
<script lang="ts">
// Vue 3 的 API 需要导入才能使用
import { defineComponent } from 'vue'

// 使用 `defineComponent` 包裹组件代码
// 即可获得完善的 TypeScript 类型推导支持
export default defineComponent({
  setup() {
    // 在 `setup` 方法里声明变量
    const msg = 'Hello World!'

    // 将需要在 `<template />` 里使用的变量 `return` 出去
    return {
      msg,
    }
  },
})
</>

<!-- CSS 代码和 Vue 2 一样 -->
<style scoped>
.msg {
  font-size: 14px;
}
</style>
```
可以看到 Vue 3 的组件也是 &lt;template /&gt; + &lt;script /&gt; +&lt;style /&gt; 的三段式组合，上手非常简单。

其中 Template 沿用了 Vue 2 时期类似 HTML 风格的模板写法， Style 则是使用原生 CSS 语法或者 Less 等 CSS 预处理器编写。

但需要注意的是，在 Vue 3 的 Composition API 写法里，数据或函数如果需要在 &lt;template /&gt; 中使用，就必须在 setup 里将其 return 出去，而仅在 &lt;script /&gt; 里被调用的函数或变量，不需要渲染到模板则无需 return 。

## 响应式数据的变化
响应式数据是 MVVM 数据驱动编程的特色， Vue 的设计也是受 MVVM 模型的启发，相信大部分开发者选择 MVVM 框架都是因为数据驱动编程比传统的事件驱动编程要来得方便，而选择 Vue ，则是方便中的方便。



**Model-View-ViewModel** （简称 MVVM ） 是一种软件架构模式，将视图 UI 和业务逻辑分开，通过对逻辑数据的修改即可驱动视图 UI 的更新，因此常将这种编程方式称为 “数据驱动” ，与之对应的需要操作 DOM 才能完成视图更新的编程方式则称为 “事件驱动” 。

### 设计上的变化
作为最重要的一个亮点， Vue 3 的响应式数据在设计上和 Vue 2 有着很大的不同。
Vue 3 是使用了 Proxy API 的 getter/setter 来实现数据的响应性，这个方法的具体用法可以参考 MDN 的文档： Proxy - MDN 。

同样的，也来实现一个简单的双向绑定 demo ，这次使用 Proxy 来实现：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Proxy Demo</title>
  </head>
  <body>
    <!-- 输入框和按钮 -->
    <div>
      <input type="text" id="input" />
      <button onclick="vm.text = 'Hello World'">设置为 Hello World</button>
    </div>
    <!-- 输入框和按钮 -->

    <!-- 文本展示 -->
    <div id="output"></div>
    <!-- 文本展示 -->

    <script>
      // 声明一个响应式数据
      const vm = new Proxy(
        {},
        {
          set(obj, key, value) {
            document.querySelector('#input').value = value
            document.querySelector('#output').innerText = value
          },
        }
      )

      // 处理输入行为
      document.querySelector('#input').oninput = function (e) {
        vm.text = e.target.value
      }
    </script>
  </body>
</html>
```



### 用法上的变化
本书只使用 Composition API 编写组件，这是使用 Vue 3 的最大优势。



相对于 Vue 2 在 data 里声明后即可通过 this.xxx 调用响应式数据，在 Vue 3 的生命周期里没有了 Vue 实例的 this 指向，需要导入 ref 、reactive 等响应式 API 才能声明并使用响应式数据。

```ts
// 这里导入的 `ref` 是一个响应式 API
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
    // 通过响应式 API 创建的变量具备了响应性
    const msg = ref<string>('Hello World!')
  },
})
```
## 响应式 API 之 ref
ref 是最常用的一个响应式 API，它可以用来定义所有类型的数据，包括 Node 节点和组件。



### 类型声明
在开始使用 API 之前，需要先了解在 TypeScript 中如何声明 Ref 变量的类型。

**API 本身的类型**
先看 API 本身， ref API 是一个函数，通过接受一个泛型入参，返回一个响应式对象，所有的值都通过 .value 属性获取，这是 API 本身的 TS 类型：

```ts
// `ref` API 的 TS 类型
function ref<T>(value: T): Ref<UnwrapRef<T>>

// `ref` API 的返回值的 TS 类型
interface Ref<T> {
  value: T
}
```
因此在声明变量时，是使用尖括号 <> 包裹其 TS 类型，紧跟在 ref API 之后：

```ts
// 显式指定 `msg.value` 是 `string` 类型
const msg = ref<string>('Hello World!')
```
再回看该 API 本身的类型，其中使用了 T 泛型，这表示在传入函数的入参时，可以不需要手动指定其 TS 类型， TypeScript 会根据这个 API 所返回的响应式对象的 .value 属性的类型，确定当前变量的类型。

因此也可以省略显式的类型指定，像下面这样声明变量，其类型交给 TypeScript 去自动推导：

```ts
// TypeScript 会推导 `msg.value` 是 `string` 类型
const msg = ref('Hello World')
```
对于声明时会赋予初始值，并且在使用过程中不会改变其类型的变量，是可以省略类型的显式指定的。

而如果有显式的指定的类型，那么在一些特殊情况下，初始化时可以不必赋值，这样 TypeScript 会自动添加 undefined 类型：

```ts
const msg = ref<string>()
console.log(msg.value) // undefined

msg.value = 'Hello World!'
console.log(msg.value) // Hello World!
```
因为入参留空时，虽然指定了 string 类型，但实际上此时的值是 undefined ，因此实际上这个时候的 msg.value 是一个 string | undefined 的联合类型。

对于声明时不知道是什么值，在某种条件下才进行初始化的情况，就可以省略其初始值，但是切记在调用该变量的时候对 .value 值进行有效性判断。

而如果既不显式指定类型，也不赋予初始值，那么会被默认为 any 类型，除非真的无法确认类型，否则不建议这么做。

### API 返回值的类型
细心的开发者还会留意到 ref API 类型里面还标注了一个返回值的 TS 类型：

```ts
interface Ref<T> {
  value: T
}
```
它是代表整个 Ref 变量的完整类型：

上文声明 Ref 变量时，提到的 string 类型都是指 msg.value 这个 .value 属性的类型
而 msg 这个响应式变量，其本身是 Ref&lt;string&gt; 类型
如果在开发过程中需要在函数里返回一个 Ref 变量，那么其 TypeScript 类型就可以这样写（请留意 Calculator 里的 num 变量的类型）：

```ts
// 导入 `ref` API
import { ref } from 'vue'
// 导入 `ref` API 的返回值类型
import type { Ref } from 'vue'

// 声明 `useCalculator` 函数的返回值类型
interface Calculator {
  // 这里包含了一个 Ref 变量
  num: Ref<number>
  add: () => void
}

// 声明一个 “使用计算器” 的函数
function useCalculator(): Calculator {
  const num = ref<number>(0)

  function add() {
    num.value++
  }

  return {
    num,
    add,
  }
}

// 在执行使用计算器函数时，可以获取到一个 Ref 变量和其他方法
const { num, add } = useCalculator()
add()
console.log(num.value) // 1
```
上面这个简单的例子演示了如何手动指定 Ref 变量的类型，对于逻辑复用时的函数代码抽离、插件开发等场景非常有用！当然大部分情况下可以交给 TypeScript 自动推导，但掌握其用法，在必要的时候就派得上用场了！
### 基本类型
对字符串、布尔值等基本类型的定义方式，比较简单：
```ts
// 字符串
const msg = ref<string>('Hello World!')

// 数值
const count = ref<number>(1)

// 布尔值
const isVip = ref<boolean>(false)
```
### 引用类型
对于对象、数组等引用类型也适用，比如要定义一个对象：

```ts
// 先声明对象的格式
interface Member {
  id: number
  name: string
}

// 在定义对象时指定该类型
const userInfo = ref<Member>({
  id: 1,
  name: 'Tom',
})
```
定义一个普通数组：

```ts
// 数值数组
const uids = ref<number[]>([1, 2, 3])

// 字符串数组
const names = ref<string[]>(['Tom', 'Petter', 'Andy'])
```
定义一个对象数组：
```ts
// 声明对象的格式
interface Member {
  id: number
  name: string
}

// 定义一个对象数组
const memberList = ref<Member[]>([
  {
    id: 1,
    name: 'Tom',
  },
  {
    id: 2,
    name: 'Petter',
  },
])
```
## DOM 元素与子组件
除了可以定义数据，ref 也有熟悉的用途，就是用来挂载节点，也可以挂在子组件上，也就是对应在 Vue 2 时常用的 this.$refs.xxx 获取 DOM 元素信息的作用。

模板部分依然是熟悉的用法，在要引用的 DOM 上添加一个 ref 属性：

```vue
<template>
  <!-- 给 DOM 元素添加 `ref` 属性 -->
  <p ref="msg">请留意该节点，有一个 ref 属性</p>

  <!-- 子组件也是同样的方式添加 -->
  <Child ref="child" />
</template>
```
请保证视图渲染完毕后再执行 DOM 或组件的相关操作（需要放到生命周期的 onMounted 或者 nextTick 函数里，这一点在 Vue 2 也是一样）；

该 Ref 变量必须 return 出去才可以给到 &lt;template /&gt;使用，这一点是 Vue 3 生命周期的硬性要求，子组件的数据和方法如果要给父组件操作，也要 return 出来才可以。

```ts
import { defineComponent, onMounted, ref } from 'vue'
import Child from '@cp/Child.vue'

export default defineComponent({
  components: {
    Child,
  },
  setup() {
    // 定义挂载节点，声明的类型详见下方附表
    const msg = ref<HTMLElement>()
    const child = ref<typeof Child>()

    // 请保证视图渲染完毕后再执行节点操作 e.g. `onMounted` / `nextTick`
    onMounted(() => {
      // 比如获取 DOM 的文本
      console.log(msg.value.innerText)

      // 或者操作子组件里的数据
      child.value.isShowDialog = true
    })

    // 必须 `return` 出去才可以给到 `<template />` 使用
    return {
      msg,
      child,
    }
  },
})
```
## 响应式 API 之 reactive
reactive 是继 ref 之后最常用的一个响应式 API 了，相对于 ref ，它的局限性在于只适合对象、数组。



### 类型声明与定义
reactive 变量的声明方式没有 ref 的变化那么大，基本上和普通变量一样，它的 TS 类型如下：

```ts
function reactive<T extends object>(target: T): UnwrapNestedRefs<T>
```
可以看到其用法还是比较简单的，下面是一个 Reactive 对象的声明方式：

```ts
// 声明对象的类型
interface Member {
  id: number
  name: string
}

// 定义一个对象
const userInfo: Member = reactive({
  id: 1,
  name: 'Tom',
})
```
下面是 Reactive 数组的声明方式：

```ts
const uids: number[] = reactive([1, 2, 3])
```
还可以声明一个 Reactive 对象数组：

```ts
// 对象数组也是先声明其中的对象类型
interface Member {
  id: number
  name: string
}

// 再定义一个为对象数组
const userList: Member[] = reactive([
  {
    id: 1,
    name: 'Tom',
  },
  {
    id: 2,
    name: 'Petter',
  },
  {
    id: 3,
    name: 'Andy',
  },
])
```
### 变量的读取与赋值
虽然 reactive API 在使用上没有像 ref API 一样有 .value 的心智负担，但也有一些注意事项要留意。

#### 处理对象
Reactive 对象在读取字段的值，或者修改值的时候，与普通对象是一样的，这部分没有太多问题。

```ts
// 声明对象的类型
interface Member {
  id: number
  name: string
}

// 定义一个对象
const userInfo: Member = reactive({
  id: 1,
  name: 'Tom',
})

// 读取用户名
console.log(userInfo.name)

// 修改用户名
userInfo.name = 'Petter'
```
### 处理数组
但是对于 Reactive 数组，和普通数组会有一些区别。

普通数组在 “重置” 或者 “修改值” 时都是可以直接操作：

```ts
// 定义一个普通数组
let uids: number[] = [1, 2, 3]

// 从另外一个对象数组里提取数据过来
uids = api.data.map((item: any) => item.id)

// 合并另外一个数组
let newUids: number[] = [4, 5, 6]
uids = [...uids, ...newUids]

// 重置数组
uids = []
```

笔者刚开始接触时，按照原来的思维去处理 reactive 数组，于是遇到了 “数据变了，但模板不会更新的问题” ，如果开发者在学习的过程中也遇到了类似的情况，可以从这里去入手排查问题所在。

举个例子，比如要从服务端 API 接口获取翻页数据时，通常要先重置数组，再异步添加数据，如果使用常规的重置，会导致这个变量失去响应性：

```ts
let uids: number[] = reactive([1, 2, 3])

/**
 * 不推荐使用这种方式，会丢失响应性
 * 异步添加数据后，模板不会响应更新
 */
uids = []

// 异步获取数据后，模板依然是空数组
setTimeout(() => {
  uids.push(1)
}, 1000)
要让数据依然保持响应性，则必须在关键操作时，不破坏响应性 API ，以下是推荐的操作方式，通过重置数组的 length 长度来实现数据的重置：

ts
const uids: number[] = reactive([1, 2, 3])

/**
 * 推荐使用这种方式，不会破坏响应性
 */
uids.length = 0

// 异步获取数据后，模板可以正确的展示
setTimeout(() => {
  uids.push(1)
}, 1000)
```

## 响应式 API 之 toRef 与 toRefs
相信各位开发者看到这里时，应该已经对 ref 和 reactive API 都有所了解了，为了方便开发者使用， Vue 3 还推出了两个与之相关的 API ： toRef 和 toRefs ，都是用于 reactive 向 ref 转换。

### 各自的作用
这两个 API 在拼写上非常接近，顾名思义，一个是只转换一个字段，一个是转换所有字段，转换后将得到新的变量，并且新变量和原来的变量可以保持同步更新。

|API	|作用|
|--------------|-----------------|
|toRef	|创建一个新的 Ref 变量，转换 Reactive 对象的某个字段为 Ref 变量|
|toRefs	|创建一个新的对象，它的每个字段都是 Reactive 对象各个字段的 Ref 变量|
光看概念可能不容易理解，来看下面的例子，先声明一个 reactive 变量：

```ts
interface Member {
  id: number
  name: string
}

const userInfo: Member = reactive({
  id: 1,
  name: 'Petter',
})
```
然后分别看看这两个 API 应该怎么使用。

#### 使用 toRef
先看这个转换单个字段的 toRef API ，了解了它的用法之后，再去看 toRefs 就很容易理解了。

##### API 类型和基本用法
toRef API 的 TS 类型如下：

```ts
// `toRef` API 的 TS 类型
function toRef<T extends object, K extends keyof T>(
  object: T,
  key: K,
  defaultValue?: T[K]
): ToRef<T[K]>

// `toRef` API 的返回值的 TS 类型
type ToRef<T> = T extends Ref ? T : Ref<T>
```
通过接收两个必传的参数（第一个是 reactive 对象, 第二个是要转换的 key ），返回一个 Ref 变量，在适当的时候也可以传递第三个参数，为该变量设置默认值。

以上文声明好的 userInfo 为例，如果想转换 name 这个字段为 Ref 变量，只需要这样操作：

```ts
const name = toRef(userInfo, 'name')
console.log(name.value) // Petter
```
所以之后在读取和赋值时，就需要使用 name.value 来操作，在重新赋值时会同时更新 name 和 userInfo.name 的值：

```ts
// 修改前先查看初始值
const name = toRef(userInfo, 'name')
console.log(name.value) // Petter
console.log(userInfo.name) // Petter

// 修改 Ref 变量的值，两者同步更新
name.value = 'Tom'
console.log(name.value) // Tom
console.log(userInfo.name) // Tom

// 修改 Reactive 对象上该属性的值，两者也是同步更新
userInfo.name = 'Jerry'
console.log(name.value) // Jerry
console.log(userInfo.name) // Jerry
```
这个 API 也可以接收一个 Reactive 数组，此时第二个参数应该传入数组的下标：

```ts
// 这一次声明的是数组
const words = reactive(['a', 'b', 'c'])

// 通过下标 `0` 转换第一个 item
const a = toRef(words, 0)
console.log(a.value) // a
console.log(words[0]) // a

// 通过下标 `2` 转换第三个 item
const c = toRef(words, 2)
console.log(c.value) // c
console.log(words[2]) // c
```
##### 设置默认值
如果 Reactive 对象上有一个属性本身没有初始值，也可以传递第三个参数进行设置（默认值仅对 Ref 变量有效）：

```ts
interface Member {
  id: number
  name: string
  // 类型上新增一个属性，因为是可选的，因此默认值会是 `undefined`
  age?: number
}

// 声明变量时省略 `age` 属性
const userInfo: Member = reactive({
  id: 1,
  name: 'Petter',
})

// 此时为了避免程序运行错误，可以指定一个初始值
// 但初始值仅对 Ref 变量有效，不会影响 Reactive 字段的值
const age = toRef(userInfo, 'age', 18)
console.log(age.value)  // 18
console.log(userInfo.age) // undefined

// 除非重新赋值，才会使两者同时更新
age.value = 25
console.log(age.value)  // 25
console.log(userInfo.age) // 25
```
数组也是同理，对于可能不存在的下标，可以传入默认值避免项目的逻辑代码出现问题：

```ts
const words = reactive(['a', 'b', 'c'])

// 当下标对应的值不存在时，也是返回 `undefined`
const d = toRef(words, 3)
console.log(d.value) // undefined
console.log(words[3]) // undefined

// 设置了默认值之后，就会对 Ref 变量使用默认值， Reactive 数组此时不影响
const e = toRef(words, 4, 'e')
console.log(e.value) // e
console.log(words[4]) // undefined
```
##### 其他用法
这个 API 还有一个特殊用法，但不建议在 TypeScript 里使用。

在 toRef 的过程中，如果使用了原对象上面不存在的 key ，那么定义出来的 Ref 变量的 .value 值将会是 undefined 。

```ts
// 众所周知， Petter 是没有女朋友的
const girlfriend = toRef(userInfo, 'girlfriend')
console.log(girlfriend.value) // undefined
console.log(userInfo.girlfriend) // undefined

// 此时 Reactive 对象上只有两个 Key
console.log(Object.keys(userInfo)) // ['id', 'name']
```
如果对这个不存在的 key 的 Ref 变量进行赋值，那么原来的 Reactive 对象也会同步增加这个 key，其值也会同步更新。

```ts
// 赋值后，不仅 Ref 变量得到了 `Marry` ， Reactive 对象也得到了 `Marry`
girlfriend.value = 'Marry'
console.log(girlfriend.value) // 'Marry'
console.log(userInfo.girlfriend) // 'Marry'

// 此时 Reactive 对象上有了三个 Key
console.log(Object.keys(userInfo)) // ['id', 'name', 'girlfriend']
```
为什么强调不要在 TypeScript 里使用呢？因为在编译时，无法通过 TypeScript 的类型检查：

#### 使用 toRefs
##### API 类型和基本用法
先看看它的 TS 类型：

```ts
function toRefs<T extends object>(
  object: T
): {
  [K in keyof T]: ToRef<T[K]>
}

type ToRef = T extends Ref ? T : Ref<T>
```
与 toRef 不同， toRefs 只接收了一个参数，是一个 reactive 变量。

```ts
interface Member {
  id: number
  name: string
}

// 声明一个 Reactive 变量
const userInfo: Member = reactive({
  id: 1,
  name: 'Petter',
})

// 传给 `toRefs` 作为入参
const userInfoRefs = toRefs(userInfo)
```
此时这个新的 userInfoRefs 变量，它的 TS 类型就不再是 Member 了，而应该是：

```ts
// 导入 `toRefs` API 的类型
import type { ToRefs } from 'vue'

// 上下文代码省略...

// 将原来的类型传给 API 的类型
const userInfoRefs: ToRefs<Member> = toRefs(userInfo)
```
也可以重新编写一个新的类型来指定它，因为每个字段都是与原来关联的 Ref 变量，所以也可以这样声明：

```ts
// 导入 `ref` API 的类型
import type { Ref } from 'vue'

// 上下文代码省略...

// 新声明的类型每个字段都是一个 Ref 变量的类型
interface MemberRefs {
  id: Ref<number>
  name: Ref<string>
}

// 使用新的类型进行声明
const userInfoRefs: MemberRefs = toRefs(userInfo)
```

和 toRef API 一样，这个 API 也是可以对数组进行转换：

```ts
const words = reactive(['a', 'b', 'c'])
const wordsRefs = toRefs(words)
```
此时新数组的类型是 Ref<string>[] ，不再是原来的 string[] 类型。

##### 解构与赋值
转换后的 Reactive 对象或数组支持 ES6 的解构，并且不会失去响应性，因为解构后的每一个变量都具备响应性。

```ts
// 为了提高开发效率，可以直接将 Ref 变量直接解构出来使用
const { name } = toRefs(userInfo)
console.log(name.value) // Petter

// 此时对解构出来的变量重新赋值，原来的变量也可以同步更新
name.value = 'Tom'
console.log(name.value) // Tom
console.log(userInfo.name) // Tom
```
这一点和直接解构 Reactive 变量有非常大的不同，直接解构 Reactive 变量，得到的是一个普通的变量，不再具备响应性。

这个功能在使用 Hooks 函数非常好用（在 Vue 3 里也叫可组合函数， Composable Functions ），还是以一个计算器函数为例，这一次将其修改为内部有一个 Reactive 的数据状态中心，在函数返回时解构为多个 Ref 变量：

```ts
import { reactive, toRefs } from 'vue'

// 声明 `useCalculator` 数据状态类型
interface CalculatorState {
  // 这是要用来计算操作的数据
  num: number
  // 这是每次计算时要增加的幅度
  step: number
}

// 声明一个 “使用计算器” 的函数
function useCalculator() {
  // 通过数据状态中心的形式，集中管理内部变量
  const state: CalculatorState = reactive({
    num: 0,
    step: 10,
  })

  // 功能函数也是通过数据中心变量去调用
  function add() {
    state.num += state.step
  }

  return {
    ...toRefs(state),
    add,
  }
}
```
这样在调用 useCalculator 函数时，可以通过解构直接获取到 Ref 变量，不需要再进行额外的转换工作。

```ts
// 解构出来的 `num` 和 `step` 都是 Ref 变量
const { num, step, add } = useCalculator()
console.log(num.value) // 0
console.log(step.value) // 10

// 调用计算器的方法，数据也是会得到响应式更新
add()
console.log(num.value) // 10
```
#### 为什么要进行转换
关于为什么要出这么两个 API ，官方文档没有特别说明，不过经过笔者在业务中的一些实际使用感受，以及在写上一节 reactive 的 特别注意，可能知道一些使用理由。

关于 ref 和 reactive 这两个 API 的好处就不重复了，但是在使用的过程中，各自都有不方便的地方：

ref API 虽然在 <template /> 里使用起来方便，但是在 <script /> 里进行读取 / 赋值的时候，要一直记得加上 .value ，否则 BUG 就来了。

reactive API 虽然在使用的时候，因为知道它本身是一个对象，所以不会忘记通过 foo.bar 这样的格式去操作，但是在 <template /> 渲染的时候，又因此不得不每次都使用 foo.bar 的格式去渲染。

那么有没有办法，既可以在编写 <script /> 的时候不容易出错，在写 <template /> 的时候又比较简单呢？

于是， toRef 和 toRefs 因此诞生。
## 函数声明
在 Vue 3 则灵活了很多，可以使用普通函数、 Class 类、箭头函数、匿名函数等等进行声明，可以将其写在 setup 里直接使用，也可以抽离在独立的 .js / .ts 文件里再导入使用。

需要在组件创建时自动执行的函数，其执行时机需要遵循 Vue 3 的生命周期，需要在模板里通过 @click、@change 等行为触发，和变量一样，需要把函数名在 setup 里进行 return 出去。

下面是一个简单的例子，方便开发者更直观地了解：

```vue
<template>
  <p>{{ msg }}</p>

  <!-- 在这里点击执行 `return` 出来的方法 -->
  <button @click="updateMsg">修改MSG</button>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'

export default defineComponent({
  setup() {
    const msg = ref<string>('Hello World!')

    // 这个要暴露给模板使用，必须 `return` 才可以使用
    function updateMsg() {
      msg.value = 'Hi World!'
    }

    // 这个要在页面载入时执行，无需 `return` 出去
    const init = () => {
      console.log('init')
    }

    onMounted(() => {
      init()
    })

    return {
      msg,
      updateMsg,
    }
  },
})
</script>
```
### 数据的侦听
```ts
import { watch } from 'vue'

// 一个用法走天下
watch(
  source, // 必传，要侦听的数据源
  callback // 必传，侦听到变化后要执行的回调函数
  // options // 可选，一些侦听选项
)
```
|参数	|是否可选	|含义|
|---------------|----------------|-----------------|---------------|
|source	|必传	|数据源（详见：要侦听的数据源）|
|callback|	必传|	侦听到变化后要执行的回调函数（详见：侦听后的回调函数）|
|options	|可选|	一些侦听选项（详见：侦听的选项）|

```ts
// 不要忘了导入要用的 API
import { defineComponent, reactive, watch } from 'vue'

export default defineComponent({
  setup() {
    // 定义一个响应式数据
    const userInfo = reactive({
      name: 'Petter',
      age: 18,
    })

    // 2s后改变数据
    setTimeout(() => {
      userInfo.name = 'Tom'
    }, 2000)

    /**
     * 可以直接侦听这个响应式对象
     * callback 的参数如果不用可以不写
     */
    watch(userInfo, () => {
      console.log('侦听整个 userInfo ', userInfo.name)
    })

    /**
     * 也可以侦听对象里面的某个值
     * 此时数据源需要写成 getter 函数
     */
    watch(
      // 数据源，getter 形式
      () => userInfo.name,
      // 回调函数 callback
      (newValue, oldValue) => {
        console.log('只侦听 name 的变化 ', userInfo.name)
        console.log('打印变化前后的值', { oldValue, newValue })
      }
    )
  },
})
```
```ts
import { defineComponent, ref, watch } from 'vue'

export default defineComponent({
  setup() {
    // 定义多个数据源
    const message = ref<string>('')
    const index = ref<number>(0)

    // 2s后改变数据
    setTimeout(() => {
      message.value = 'Hello World!'
      index.value++
    }, 2000)

    watch(
      // 数据源改成了数组
      [message, index],
      // 回调的入参也变成了数组，每个数组里面的顺序和数据源数组排序一致
      ([newMessage, newIndex], [oldMessage, oldIndex]) => {
        console.log('message 的变化', { newMessage, oldMessage })
        console.log('index 的变化', { newIndex, oldIndex })
      }
    )
  },
})

```
## 指令
### 内置指令
```ts
<template>
  <!-- 渲染一段文本 -->
  <span v-text="msg"></span>

  <!-- 渲染一段 HTML -->
  <div v-html="html"></div>

  <!-- 循环创建一个列表 -->
  <ul v-if="items.length">
    <li v-for="(item, index) in items" :key="index">
      <span>{{ item }}</span>
    </li>
  </ul>

  <!-- 一些事件（ `@` 等价于 `v-on` ） -->
  <button @click="hello">Hello</button>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup() {
    const msg = ref<string>('Hello World!')
    const html = ref<string>('<p>Hello World!</p>')
    const items = ref<string[]>(['a', 'b', 'c', 'd'])

    function hello() {
      console.log(msg.value)
    }

    return {
      msg,
      html,
      items,
      hello,
    }
  },
})
</script>

```
### 自定义指令
自定义指令有两种实现形式，一种是作为一个对象，其中的写法比较接近于 Vue 组件，除了 getSSRProps 和 deep 选项 外，其他的每一个属性都是一个 钩子函数 ，下一小节会介绍钩子函数的内容。
```ts
export declare interface ObjectDirective<T = any, V = any> {
  created?: DirectiveHook<T, null, V>
  beforeMount?: DirectiveHook<T, null, V>
  mounted?: DirectiveHook<T, null, V>
  beforeUpdate?: DirectiveHook<T, VNode<any, T>, V>
  updated?: DirectiveHook<T, VNode<any, T>, V>
  beforeUnmount?: DirectiveHook<T, null, V>
  unmounted?: DirectiveHook<T, null, V>
  getSSRProps?: SSRDirectiveHook
  deep?: boolean
}
```

## 插槽
Vue 在使用子组件的时候，子组件在 template 里类似一个 HTML 标签，可以在这个子组件标签里传入任意模板代码以及 HTML 代码，这个功能就叫做 “插槽” 。
```ts
<template>
  <Child>
    <!-- 传给标题插槽 -->
    <template #title>
      <h1>这是标题</h1>
    </template>

    <!-- 传给作者插槽 -->
    <template #author>
      <h1>这是作者信息</h1>
    </template>

    <!-- 传给默认插槽 -->
    <p>这是插槽内容</p>
  </Child>
</template>
```
# 路由的使用
### vue3
Vue 3 的引入方式如下（其中 RouteRecordRaw 是路由项目的 TS 类型）
```ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  // ...
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
```
### 路由树的配置
在 TypeScript 里，路由文件的基础格式由三个部分组成：类型声明、数组结构、模块导出。
```ts
// src/router/routes.ts

// 使用 TypeScript 时需要导入路由项目的类型声明
import type { RouteRecordRaw } from 'vue-router'

// 使用路由项目类型声明一个路由数组
const routes: Array<RouteRecordRaw> = [
  // ...
]

// 将路由数组导出给其他模块使用
export default routes
```
### 公共基础路径
以 Vite 项目的配置文件 vite.config.ts 为例，里面有一个选项 base ，其实就是用来控制路由的公共基础路径，那么它有什么用呢？base 的默认值是 /，也就是说，如果不配置它，那么所有的资源文件都是从域名根目录读取，如果项目部署在域名根目录那当然好，但是如果不是呢？那么就必须来配置它了。
### 一级路由
```ts
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@views/home.vue'),
  },
]
```
### 同步组件
字段 component 接收一个变量，变量的值就是对应的模板组件。在打包的时候，会把组件的所有代码都打包到一个文件里，对于大项目来说，这种方式的首屏加载是个灾难，要面对文件过大带来等待时间变长的问题。
```ts
import Home from '@views/home.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
]
```
### 异步组件
字段 component 接收一个函数，在 return 的时候返回模板组件，同时组件里的代码在打包的时候都会生成独立的文件，并在访问到对应路由的时候按需引入。
```ts
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@views/home.vue'),
  },
]
```
### 多级路由
```ts
const routes: Array<RouteRecordRaw> = [
  // 注意：这里是一级路由
  {
    path: '/lv1',
    name: 'lv1',
    component: () => import('@views/lv1.vue'),
    // 注意：这里是二级路由，在 `path` 的前面没有 `/`
    children: [
      {
        path: 'lv2',
        name: 'lv2',
        component: () => import('@views/lv2.vue'),
        // 注意：这里是三级路由，在 `path` 的前面没有 `/`
        children: [
          {
            path: 'lv3',
            name: 'lv3',
            component: () => import('@views/lv3.vue'),
          },
        ],
      },
    ],
  },
]
```
### 路由的渲染
所有路由组件，要在访问后进行渲染，都必须在父级组件里带有 <router-view /> 标签。
<router-view /> 在哪里，路由组件的代码就渲染在哪个节点上，一级路由的父级组件，就是 src/App.vue 这个根组件。
其中最基础的配置就是 <template /> 里面直接就是写一个 <router-view /> ，整个页面就是路由组件。
```vue
<template>
  <router-view />
</template>
```
如果站点带有全局公共组件，比如有全站统一的页头、页脚，只有中间区域才是路由，那么可以这样配置
```vue
<template>
  <!-- 全局页头 -->
  <Header />

  <!-- 路由 -->
  <router-view />

  <!-- 全局页脚 -->
  <Footer />
</template>
```
如果有一部分路由带公共组件，一部分没有，比如大部分页面都需要有侧边栏，但登录页、注册页不需要，就可以这么处理：

```vue
<template>
  <!-- 登录 -->
  <Login v-if="route.name === 'login'" />

  <!-- 注册 -->
  <Register v-else-if="route.name === 'register'" />

  <!-- 带有侧边栏的其他路由 -->
  <div v-else>
    <!-- 固定在左侧的侧边栏 -->
    <Sidebar />

    <!-- 路由 -->
    <router-view />
  </div>
</template>
```
### 使用 route 获取路由信息
要牢记一个事情就是，Vue 3 用啥都要导入，所以获取当前路由信息的正确用法是先导入路由 API ：

```ts
import { useRoute } from 'vue-router'
```
再在 setup 里定义一个变量来获取当前路由：

```ts
const route = useRoute()
```

### 使用 router 操作路由
```ts
// 跳转首页
router.push({
  name: 'home',
})

// 返回上一页
router.back()
```
### 使用 router-link 标签跳转
#### 基础跳转
```vue
<template>
  <router-link to="/home">首页</router-link>
</template>

<template>
  <div
    class="link"
    @click="
      router.push({
        name: 'home',
      })
    "
  >
    <span>首页</span>
  </div>
</template>

```
#### 带参数的跳转
使用 router 的时候，可以轻松的带上参数去那些有 ID 的内容页、用户资料页、栏目列表页等等。
```ts
router.push({
  name: 'article',
  params: {
    id: 123,
  },
})
<template>
  <router-link
    class="link"
    :to="{
      name: 'article',
      params: {
        id: 123,
      },
    }"
  >
    这是文章的标题
  </router-link>
</template>

```
#### 不生成 a 标签
router-link 默认是被转换为一个 a 标签，但根据业务场景，也可以把它指定为生成其他标签，比如 span 、 div 、 li 等等，这些标签因为不具备 href 属性，所以在跳转时都是通过 Click 事件去执行。
```vue
<template>
  <router-link to="/home" custom v-slot="{ navigate }">
    <span class="link" @click="navigate"> 首页 </span>
  </router-link>
</template>
```
### 路由元信息配置
```ts
const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@views/login.vue'),
    meta: {
      title: '登录',
      isDisableBreadcrumbLink: true,
      isShowBreadcrumb: false,
      addToSidebar: false,
      sidebarIcon: '',
      sidebarIconAlt: '',
      isNoLogin: true,
    },
  },
]

```
### 路由重定向
#### 路由重定向
```ts
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'home',
    component: () => import('@views/home.vue'),
    meta: {
      title: 'Home',
    },
  },
  // 访问这个路由会被重定向到首页
  {
    path: '/error',
    redirect: '/',
  },
]

```
### 配置为 route
```ts
const routes: Array<RouteRecordRaw> = [
  // 重定向到 `/home` ，并带上一个 `query` 参数
  {
    path: '/',
    redirect: {
      name: 'home',
      query: {
        from: 'redirect',
      },
    },
  },
  // 真正的首页
  {
    path: '/home',
    name: 'home',
    component: () => import('@views/home.vue'),
  },
]
```
### 配置为 function
 ```ts
 const routes: Array<RouteRecordRaw> = [
  // 访问主域名时，根据用户的登录信息，重定向到不同的页面
  {
    path: '/',
    redirect: () => {
      // `loginInfo` 是当前用户的登录信息
      // 可以从 `localStorage` 或者 `Pinia` 读取
      const { groupId } = loginInfo

      // 根据组别 ID 进行跳转
      switch (groupId) {
        // 管理员跳去仪表盘
        case 1:
          return '/dashboard'

        // 普通用户跳去首页
        case 2:
          return '/home'

        // 其他都认为未登录，跳去登录页
        default:
          return '/login'
      }
    },
  },
]

```
### 路由别名配置
```ts
const routes: Array<RouteRecordRaw> = [
  {
    path: '/home',
    alias: '/index',
    name: 'home',
    component: () => import('@views/home.vue'),
  },
]
```
### 404 路由页面配置
```ts
const routes: Array<RouteRecordRaw> = [
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    component: () => import('@views/404.vue'),
  },
]
```
### 导航守卫
#### 路由里的全局钩子
```ts
import { createRouter } from 'vue-router'

// 创建路由
const router = createRouter({ ... })

// 在这里调用导航守卫的钩子函数
router.beforeEach((to, from) => {
  // ...
})

// 导出去
export default router
```
比如在进入路由之前，根据 Meta 路由元信息 的配置，设定路由的网页标题
```ts
router.beforeEach((to, from) => {
  const { title } = to.meta
  document.title = title || '默认标题'
})
// 或者判断是否需要登录
router.beforeEach((to, from) => {
  const { isNoLogin } = to.meta
  if (!isNoLogin) return '/login'
})

const routes: Array<RouteRecordRaw> = [
  // 这是一个配置了 `params` ，访问的时候必须带 `id` 的路由
  {
    path: '/article/:id',
    name: 'article',
    component: () => import('@views/article.vue'),
  },
  // ...
]

router.beforeEach((to) => {
  if (to.name === 'article' && to.matched.length === 0) {
    return '/'
  }
})


// https://router.vuejs.org/zh/guide/advanced/navigation-guards.html

router.beforeResolve(async (to) => {
  // 如果路由配置了必须调用相机权限
  if (to.meta.requiresCamera) {
    // 正常流程，咨询是否允许使用照相机
    // 全局解析守卫，它会在每次导航时触发，但是在所有组件内守卫和异步路由组件被解析之后，将在确认导航之前被调用。
    try {
      await askForCameraPermission()
    } catch (error) {
      // 容错
      if (error instanceof NotAllowedError) {
        // ... 处理错误，然后取消导航
        return false
      } else {
        // 如果出现意外，则取消导航并抛出错误
        throw error
      }
    }
  }
})

```
### afterEach
全局后置守卫，这也是导航守卫里面用的比较多的一个钩子函数。


### 在组件内使用全局钩子
```ts
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    // 定义路由
    const router = useRouter()

    // 调用全局钩子
    router.beforeEach((to, from) => {
      // ...
    })
  },
})
```
### 路由里的独享钩子
```ts
const routes: Array<RouteRecordRaw> = [
  {
    path: '/home',
    name: 'home',
    component: () => import('@views/home.vue'),
    // 在这里添加单独的路由守卫
    beforeEnter: (to, from) => {
      document.title = '程沛权 - 养了三只猫'
    },
  },
]
```
### 组件内单独使用
```ts
import { defineComponent, onMounted } from 'vue'
import { useRoute, onBeforeRouteUpdate } from 'vue-router'

export default defineComponent({
  setup() {
    // 其他代码略...

    // 查询文章详情
    async function queryArticleDetail(id: number) {
      // 请求接口数据
      const res = await axios({
        url: `/article/${id}`,
      })
      // ...
    }

    // 组件挂载完成后执行文章内容的请求
    // 注意这里是获取 `route` 的 `params`
    onMounted(async () => {
      const id = Number(route.params.id) || 0
      await queryArticleDetail(id)
    })

    // 组件被复用时重新请求新的文章内容
    onBeforeRouteUpdate(async (to, from) => {
      // ID 不变时减少重复请求
      if (to.params.id === from.params.id) return

      // 注意这里是获取 `to` 的 `params`
      const id = Number(to.params.id) || 0
      await queryArticleDetail(id)
    })
  },
})
```
### 路由侦听
#### 侦听整个路由
```ts
import { defineComponent, watch } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent({
  setup() {
    const route = useRoute()

    // 侦听整个路由
    watch(route, (to, from) => {
      // 处理一些事情
      // ...
    })
  },
})
```
#### 侦听路由的某个数据
```ts
import { defineComponent, watch } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent({
  setup() {
    const route = useRoute()

    // 侦听路由参数的变化
    watch(
      () => route.query.id,
      () => {
        console.log('侦听到 ID 变化')
      }
    )
  },
})
```
#### watchEffect
```ts
import { defineComponent, watchEffect } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent({
  setup() {
    const route = useRoute()

    // 从接口查询文章详情
    async function queryArticleDetail() {
      const id = Number(route.params.id) || 0
      console.log('文章 ID 是：', id)

      const res = await axios({
        url: `/article/${id}`,
      })
      // ...
    }

    // 直接侦听包含路由参数的那个函数
    watchEffect(queryArticleDetail)
  },
})
```
# 插件的开发和使用
## 全局插件的使用
```ts
// main.ts
import plugin1 from 'plugin1'
import plugin2 from 'plugin2'
import plugin3 from 'plugin3'
import plugin4 from 'plugin4'

createApp(App)
  .use(plugin1)
  .use(plugin2)
  .use(plugin3, {
    // plugin3's options
  })
  .use(plugin4)
  .mount('#app')
```
## 基本结构
当导出为一个函数时， Vue 会直接调用这个函数，此时插件内部是这样子：
```ts
export default function (app, options) {
  // 逻辑代码...
}
```
当导出为一个对象时，对象上面需要有一个 install 方法给 Vue ， Vue 通过调用这个方法来启用插件，此时插件内部是这样子：
```ts
export default {
  install: (app, options) => {
    // 逻辑代码...
  },
```  
|参数|	作用|	类型|
|------------|--------------|----------|

|app	|createApp 生成的实例|	App （从 'vue' 里导入该类型），见下方的案例演示|
|options	插件初始化时的选项	|undefined 或一个对象，对象的 TS 类型由插件的选项决定|
## 编写插件
```ts
// src/plugins/directive.ts
import type { App } from 'vue'

// 插件选项的类型
interface Options {
  // 文本高亮选项
  highlight?: {
    // 默认背景色
    backgroundColor: string
  }
}

/**
 * 自定义指令
 * @description 保证插件单一职责，当前插件只用于添加自定义指令
 */
export default {
  install: (app: App, options?: Options) => {
    /**
     * 权限控制
     * @description 用于在功能按钮上绑定权限，没权限时会销毁或隐藏对应 DOM 节点
     * @tips 指令传入的值是管理员的组别 id
     * @example <div v-permission="1" />
     */
    app.directive('permission', (el, binding) => {
      // 假设 1 是管理员组别的 id ，则无需处理
      if (binding.value === 1) return

      // 其他情况认为没有权限，需要隐藏掉界面上的 DOM 元素
      if (el.parentNode) {
        el.parentNode.removeChild(el)
      } else {
        el.style.display = 'none'
      }
    })

    /**
     * 文本高亮
     * @description 用于给指定的 DOM 节点添加背景色，搭配文本内容形成高亮效果
     * @tips 指令传入的值需要是合法的 CSS 颜色名称或者 Hex 值
     * @example <div v-highlight="`cyan`" />
     */
    app.directive('highlight', (el, binding) => {
      // 获取默认颜色
      let defaultColor = 'unset'
      if (
        Object.prototype.toString.call(options) === '[object Object]' &&
        options?.highlight?.backgroundColor
      ) {
        defaultColor = options.highlight.backgroundColor
      }

      // 设置背景色
      el.style.backgroundColor =
        typeof binding.value === 'string' ? binding.value : defaultColor
    })
  },
}

```
## 启用插件
```ts
// src/main.ts
import { createApp } from 'vue'
import App from '@/App.vue'
import directive from '@/plugins/directive' // 导入插件

createApp(App)
   // 自定义插件
  .use(directive, {
    highlight: {
      backgroundColor: '#ddd',
    },
  })
  .mount('#app')
```
## 全局 API 挂载
### 定义全局 API
如上，在配置全局变量之前，可以把初始化时的 createApp 定义为一个变量（假设为 app ），然后把需要设置为全局可用的变量或方法，挂载到 app 的 config.globalProperties 上面。
```ts
import md5 from 'md5'

// 创建 Vue 实例
const app = createApp(App)

// 把插件的 API 挂载全局变量到实例上
app.config.globalProperties.$md5 = md5

// 也可以自己写一些全局函数去挂载
app.config.globalProperties.$log = (text: string): void => {
  console.log(text)
}

app.mount('#app')
```
## npm 包的开发与发布
 

# 组件之间的通信
## 父子组件通信
### props / emits
1. 父组件 Father.vue 通过 props 向子组件 Child.vue 传值
2. 子组件 Child.vue 则可以通过 emits 向父组件 Father.vue 发起事件通知
最常见的场景就是统一在父组件发起 AJAX 请求，拿到数据后，再根据子组件的渲染需要传递不同的 props 给不同的子组件使用。

下发的过程是在 Father.vue 里完成的，父组件在向子组件下发 props 之前，需要导入子组件并启用它作为自身的模板，然后在 setup 里处理好数据并 return 给 <template /> 用。
#### 下发 props
```ts
// Father.vue
import { defineComponent } from 'vue'
import Child from '@cp/Child.vue'

interface Member {
  id: number
  name: string
}

export default defineComponent({
  // 需要启用子组件作为模板
  components: {
    Child,
  },

  // 定义一些数据并 `return` 给 `<template />` 用
  setup() {
    const userInfo: Member = {
      id: 1,
      name: 'Petter',
    }

    // 不要忘记 `return` ，否则 `<template />` 拿不到数据
    return {
      userInfo,
    }
  },
})



<!-- Father.vue -->
<template>
  <Child
    title="用户信息"
    :index="1"
    :uid="userInfo.id"
    :user-name="userInfo.name"
  />
</template>

```
#### 接收 props
接收的过程是在 Child.vue 里完成的，在 <script /> 部分，子组件通过与 setup 同级的 props 来接收数据。

它可以是一个 string[] 数组，把要接受的变量名放到这个数组里，直接放进来作为数组的 item ：

```ts
// Child.vue
export default defineComponent({
  props: ['title', 'index', 'userName', 'uid'],
})
```
# 全局状态管理
```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia' // 导入 Pinia
import App from '@/App.vue'

createApp(App)
  .use(createPinia()) // 启用 Pinia
  .mount('#app')
```
## 创建 Store
```ts
// src/stores/index.ts
import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  // Store 选项...
})


// src/stores/index.ts
import { defineStore } from 'pinia'

export const useStore = defineStore({
  id: 'main',
  // Store 选项...
})

```
## 管理 state
### 给 Store 添加 state
```ts
// src/stores/index.ts
import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  // 先定义一个最基本的 message 数据
  state: () => ({
    message: 'Hello World',
  }),
  // ...
})
// 需要注意一点的是，如果不显式 return ，箭头函数的返回值需要用圆括号 () 套起来，这个是箭头函数的要求（详见：返回对象字面量）。
// ...
export const useStore = defineStore('main', {
  state: () => {
    return {
      message: 'Hello World',
    }
  },
  // ...
})
// 指定类型
// ...
export const useStore = defineStore('main', {
  state: () => {
    return {
      message: 'Hello World',
      // 通过 as 关键字指定 TS 类型
      randomMessages: [] as string[],
      //  randomMessages: <string[]>[],
    }
  },
  // ...
})
```

## 使用 store 实例
```ts
import { defineComponent } from 'vue'
import { useStore } from '@/stores'

export default defineComponent({
  setup() {
    // 像 useRouter 那样定义一个变量拿到实例
    const store = useStore()

    // 直接通过实例来获取数据
    console.log(store.message)

    // 这种方式需要把整个 store 给到 template 去渲染数据
    return {
      store,
    }
  },
})
```
### 使用 computed API
```vue
<script lang="ts">
import { computed, defineComponent } from 'vue'
import { useStore } from '@/stores'

export default defineComponent({
  setup() {
    // 像 useRouter 那样定义一个变量拿到实例
    const store = useStore()

    // 通过计算拿到里面的数据
    const message = computed(() => store.message)
    console.log('message', message.value)

    // 传给 template 使用
    return {
      message,
    }
  },
})
</script>
```
### 使用 storeToRefs API
```ts
import { defineComponent } from 'vue'
import { useStore } from '@/stores'

// 记得导入这个 API
import { storeToRefs } from 'pinia'

export default defineComponent({
  setup() {
    const store = useStore()

    // 通过 storeToRefs 来拿到响应性的 message
    const { message } = storeToRefs(store)
    console.log('message', message.value)

    return {
      message,
    }
  },
})
```
### 使用 toRefs API
```ts
// 注意 toRefs 是 vue 的 API ，不是 Pinia
import { defineComponent, toRefs } from 'vue'
import { useStore } from '@/stores'

export default defineComponent({
  setup() {
    const store = useStore()

    // 跟 storeToRefs 操作都一样，只不过用 Vue 的这个 API 来处理
    const { message } = toRefs(store)
    console.log('message', message.value)

    return {
      message,
    }
  },
})
```
### 批量更新 state
```ts
// 继续用前面的数据，这里会打印出修改前的值
console.log(JSON.stringify(store.$state))
// 输出 {"message":"Hello World","randomMessages":[]}

/**
 * 注意这里，传入了一个对象
 */
store.$patch({
  message: 'New Message',
  randomMessages: ['msg1', 'msg2', 'msg3'],
})

// 这里会打印出修改后的值
console.log(JSON.stringify(store.$state))
// 输出 {"message":"New Message","randomMessages":["msg1","msg2","msg3"]}


// 这里会打印出修改前的值
console.log(JSON.stringify(store.$state))
// 输出 {"message":"Hello World","randomMessages":[]}

/**
 * 注意这里，这次是传入了一个函数
 */
store.$patch((state) => {
  state.message = 'New Message'

  // 数组改成用追加的方式，而不是重新赋值
  for (let i = 0; i < 3; i++) {
    state.randomMessages.push(`msg${i + 1}`)
  }
})

// 这里会打印出修改后的值
console.log(JSON.stringify(store.$state))
// 输出 {"message":"New Message","randomMessages":["msg1","msg2","msg3"]}

```

## 全量更新 state
```ts
store.$state = {
  message: 'New Message',
  randomMessages: ['msg1', 'msg2', 'msg3'],
}
```
## 订阅 state
```ts
// $subscribe 部分的 TS 类型
// ...
$subscribe(
  callback: SubscriptionCallback<S>,
  options?: { detached?: boolean } & WatchOptions
): () => void


// 添加订阅
// 可以在 state 出现变化时，更新本地持久化存储的数据
store.$subscribe((mutation, state) => {
  localStorage.setItem('store', JSON.stringify(state))
})

// 移除订阅
// 定义一个退订变量，它是一个函数
const unsubscribe = store.$subscribe(
  (mutation, state) => {
    // ...
  },
  { detached: true }
)

// 在合适的时期调用它，可以取消这个订阅
unsubscribe()

```
## 管理 getters
```ts
// src/stores/index.ts
import { defineStore } from 'pinia'

export const useStore = defineStore('main', {
  state: () => ({
    message: 'Hello World',
  }),
  // 定义一个 fullMessage 的计算数据
  getters: {
    fullMessage: (state) => `The message is "${state.message}".`,
  },
  // ...
})
//  添加引用 getter 的 getter
export const useStore = defineStore('main', {
  state: () => ({
    message: 'Hello World',
  }),
  getters: {
    fullMessage: (state) => `The message is "${state.message}".`,
    // 这个 getter 返回了另外一个 getter 的结果
    emojiMessage(): string {
      return `🎉🎉🎉 ${this.fullMessage}`
    },
  },
})


```
# 高效开发
## script-setup
```ts
<!-- 使用 script-setup 格式 -->
<template>
  <p>{{ msg }}</p>
</template>

<script setup lang="ts">
const msg = 'Hello World!'
</script>
```
### props 的接收方式变化
```ts
const props = defineProps(['name', 'userInfo', 'tags'])
console.log(props.name)
```
### withDefaults 的基础用法
这个新的 withDefaults API 可以让在使用 TS 类型系统时，也可以指定 props 的默认值。
```ts
withDefaults(
  // 这是第一个参数，声明 props
  defineProps<{
    size?: number
    labels?: string[]
  }>(),
  // 这是第二个参数，设置默认值
  {
    size: 3,
    labels: () => ['default label'],
  }
)
```
### emits 的接收方式变化
```ts
// 获取 emit
const emit = defineEmits(['update-name'])

// 调用 emit
emit('update-name', 'Tom')
```
### attrs 的接收方式变化
```ts
// 标准组件的写法
export default defineComponent({
  setup(props, { attrs }) {
    // attrs 是个对象，每个 Attribute 都是它的 key
    console.log(attrs.class)

    // 如果传下来的 Attribute 带有短横线，需要通过这种方式获取
    console.log(attrs['data-hash'])
  },
})

```
### attrs 的接收方式变化
```ts
// 标准组件的写法
export default defineComponent({
  setup(props, { attrs }) {
    // attrs 是个对象，每个 Attribute 都是它的 key
    console.log(attrs.class)

    // 如果传下来的 Attribute 带有短横线，需要通过这种方式获取
    console.log(attrs['data-hash'])
  },
})
```
### slots 的接收方式变化
slots 是 Vue 组件的插槽数据，也是在父子通信里的一个重要成员。
```ts
<template>
  <div>
    <!-- 插槽数据 -->
    <slot />
    <!-- 插槽数据 -->
  </div>
</template>
```
### defineExpose 的基础用法
```ts
<script setup lang="ts">
const msg = 'Hello World!'

// 通过该 API 显式暴露的数据，才可以在父组件拿到
defineExpose({
  msg,
})
</script>

<script setup lang="ts">
const res = await fetch(`https://example.com/api/foo`)
const json = await res.json()
console.log(json)
</script>

```