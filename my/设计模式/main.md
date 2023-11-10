# 总结
## 创建型模式
这类模式提供创建对象的机制， 能够提升已有代码的灵活性和可复⽤性
<img src="./img/2023-09-11 105701.png">

## 结构型模式
这类模式介绍如何将对象和类组装成较⼤的结构， 并同时保持结构的灵活和⾼效。
<img src="./img/2023-09-11 105935.png">

## ⾏为模式
这类模式负责对象间的⾼效沟通和职责委派。
<img src="./img/2023-09-11 110149.png">

<img src="./img/2023-09-11 110311.png" >


# 创建型模式

## 工厂模式
工厂模式（Factory Pattern）是最常用的设计模式之一。这种类型的设计模式属于创建型模式，它提供了一种创建对象的最佳方式。

工厂模式提供了一种将对象的实例化过程封装在工厂类中的方式。通过使用工厂模式，可以将对象的创建与使用代码分离，提供一种统一的接口来创建不同类型的对象。
### 特点介绍

**应用实例**： 1、您需要一辆汽车，可以直接从工厂里面提货，而不用去管这辆汽车是怎么做出来的，以及这个汽车里面的具体实现。 2、Hibernate 换数据库只需换方言和驱动就可以。

**优点**： 1、一个调用者想创建一个对象，只要知道其名称就可以了。 2、扩展性高，如果想增加一个产品，只要扩展一个工厂类就可以。 3、屏蔽产品的具体实现，调用者只关心产品的接口。

**缺点**：每次增加一个产品时，都需要增加一个具体类和对象实现工厂，使得系统中类的个数成倍增加，在一定程度上增加了系统的复杂度，同时也增加了系统具体类的依赖。这并不是什么好事。

**使用场景**： 1、日志记录器：记录可能记录到本地硬盘、系统事件、远程服务器等，用户可以选择记录日志到什么地方。 2、数据库访问，当用户不知道最后系统采用哪一类数据库，以及数据库可能有变化时。 3、设计一个连接服务器的框架，需要三个协议，"POP3"、"IMAP"、"HTTP"，可以把这三个作为产品类，共同实现一个接口。



### 工厂模式包含以下几个核心角色：

- **抽象产品（Abstract Product）**：定义了产品的共同接口或抽象类。它可以是具体产品类的父类或接口，规定了产品对象的共同方法。
**具体产品（Concrete Product）**：实现了抽象产品接口，定义了具体产品的特定行为和属性。
**抽象工厂（Abstract Factory）**：声明了创建产品的抽象方法，可以是接口或抽象类。它可以有多个方法用于创建不同类型的产品。
**具体工厂（Concrete Factory）**：实现了抽象工厂接口，负责实际创建具体产品的对象。

### 实现架构
我们将创建一个 Shape 接口和实现 Shape 接口的实体类。下一步是定义工厂类 ShapeFactory。

FactoryPatternDemo 类使用 ShapeFactory 来获取 Shape 对象。它将向 ShapeFactory 传递信息（CIRCLE / RECTANGLE / SQUARE），以便获取它所需对象的类型。
![Alt text](image-11.png)
### java 实现
**步骤 1**
创建一个接口:
```rust
Shape.java
public interface Shape {
   void draw();
}
```

**步骤 2**
创建实现接口的实体类。
```java
Rectangle.java
public class Rectangle implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Rectangle::draw() method.");
   }
}
Square.java
public class Square implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Square::draw() method.");
   }
}
Circle.java
public class Circle implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Circle::draw() method.");
   }
}

```

**步骤 3**
创建一个工厂，生成基于给定信息的实体类的对象。
```rust
ShapeFactory.java
public class ShapeFactory {
    
   //使用 getShape 方法获取形状类型的对象
   public Shape getShape(String shapeType){
      if(shapeType == null){
         return null;
      }        
      if(shapeType.equalsIgnoreCase("CIRCLE")){
         return new Circle();
      } else if(shapeType.equalsIgnoreCase("RECTANGLE")){
         return new Rectangle();
      } else if(shapeType.equalsIgnoreCase("SQUARE")){
         return new Square();
      }
      return null;
   }
}

```

**步骤 4**
使用该工厂，通过传递类型信息来获取实体类的对象。
```java
FactoryPatternDemo.java
public class FactoryPatternDemo {
 
   public static void main(String[] args) {
      ShapeFactory shapeFactory = new ShapeFactory();
 
      //获取 Circle 的对象，并调用它的 draw 方法
      Shape shape1 = shapeFactory.getShape("CIRCLE");
 
      //调用 Circle 的 draw 方法
      shape1.draw();
 
      //获取 Rectangle 的对象，并调用它的 draw 方法
      Shape shape2 = shapeFactory.getShape("RECTANGLE");
 
      //调用 Rectangle 的 draw 方法
      shape2.draw();
 
      //获取 Square 的对象，并调用它的 draw 方法
      Shape shape3 = shapeFactory.getShape("SQUARE");
 
      //调用 Square 的 draw 方法
      shape3.draw();
   }
}
```

### rust实现
由于设计思想是一致的，关于rust的实现就不再赘述上述的步骤，直接贴上完整的代码。
```rust

// 定义接口
pub  trait Shape {
    fn draw(&self);  
}
// 创建实体类
struct Rectangle;
struct Square;
struct  Circle;
impl Shape for Rectangle {
    fn draw(&self) {
        println!("Inside Rectangle::draw() method.");
    }
}
impl Shape for Square {
    fn draw(&self) {
        println!("Inside Square::draw() method.");
    }
}
impl Shape for Circle {
    fn draw(&self) {
        println!("Inside Circle::draw() method.");
    }
}
struct ShapeFactory ;
impl ShapeFactory {
    fn get_shape(shape_type: &str)->Box<dyn Shape>{
        if shape_type=="CIRCLE" {
            Box::new(Circle{})
        }else if shape_type=="RECTANGLE" {
            Box::new(Rectangle{})
        }else if  shape_type=="SQUARE"{
            Box::new(Square{})
        }else {
            panic!("输入的类型不存在");
        }
  
    }

}

fn main() {

    let shape1=ShapeFactory::get_shape("CIRCLE");
    shape1.draw();
    let shape2=ShapeFactory::get_shape("RECTANGLE");
    shape2.draw();
    let shape3=ShapeFactory::get_shape("SQUARE");
    shape3.draw();
}

```
## 抽象工厂模式
抽象工厂模式（Abstract Factory Pattern）是围绕一个超级工厂创建其他工厂。该超级工厂又称为其他工厂的工厂。

在抽象工厂模式中，接口是负责创建一个相关对象的工厂，不需要显式指定它们的类。每个生成的工厂都能按照工厂模式提供对象。

抽象工厂模式提供了一种创建一系列相关或相互依赖对象的接口，而无需指定具体实现类。通过使用抽象工厂模式，可以将客户端与具体产品的创建过程解耦，使得客户端可以通过工厂接口来创建一族产品。
### 介绍
**意图**：提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类。

**主要解决**：主要解决接口选择的问题。

**何时使用**：系统的产品有多于一个的产品族，而系统只消费其中某一族的产品。

如何解决：在一个产品族里面，定义多个产品。

关键代码：在一个工厂里聚合多个同类产品。

**应用实例**：工作了，为了参加一些聚会，肯定有两套或多套衣服吧，比如说有商务装（成套，一系列具体产品）、时尚装（成套，一系列具体产品），甚至对于一个家庭来说，可能有商务女装、商务男装、时尚女装、时尚男装，这些也都是成套的，即一系列具体产品。假设一种情况（现实中是不存在的，但有利于说明抽象工厂模式），在您的家中，某一个衣柜（具体工厂）只能存放某一种这样的衣服（成套，一系列具体产品），每次拿这种成套的衣服时也自然要从这个衣柜中取出了。用 OOP 的思想去理解，所有的衣柜（具体工厂）都是衣柜类的（抽象工厂）某一个，而每一件成套的衣服又包括具体的上衣（某一具体产品），裤子（某一具体产品），这些具体的上衣其实也都是上衣（抽象产品），具体的裤子也都是裤子（另一个抽象产品）。

**优点**：当一个产品族中的多个对象被设计成一起工作时，它能保证客户端始终只使用同一个产品族中的对象。

**缺点**：产品族扩展非常困难，要增加一个系列的某一产品，既要在抽象的 Creator 里加代码，又要在具体的里面加代码。

**使用场景**： 1、皮肤系统，一整套一起换。 



### 抽象工厂模式包含以下几个核心角色：
**抽象工厂（Abstract Factory）**：声明了一组用于创建产品对象的方法，每个方法对应一种产品类型。抽象工厂可以是接口或抽象类。
**具体工厂（Concrete Factory）**：实现了抽象工厂接口，负责创建具体产品对象的实例。
**抽象产品（Abstract Product）**：定义了一组产品对象的共同接口或抽象类，描述了产品对象的公共方法。
**具体产品（Concrete Product）**：实现了抽象产品接口，定义了具体产品的特定行为和属性。
抽象工厂模式通常涉及一族相关的产品，每个具体工厂类负责创建该族中的具体产品。客户端通过使用抽象工厂接口来创建产品对象，而不需要直接使用具体产品的实现类。

### 实现架构图
我们将创建 Shape 和 Color 接口和实现这些接口的实体类。下一步是创建抽象工厂类 AbstractFactory。接着定义工厂类 ShapeFactory 和 ColorFactory，这两个工厂类都是扩展了 AbstractFactory。然后创建一个工厂创造器/生成器类 FactoryProducer。

AbstractFactoryPatternDemo 类使用 FactoryProducer 来获取 AbstractFactory 对象。它将向 AbstractFactory 传递形状信息 Shape（CIRCLE / RECTANGLE / SQUARE），以便获取它所需对象的类型。同时它还向 AbstractFactory 传递颜色信息 Color（RED / GREEN / BLUE），以便获取它所需对象的类型。

抽象工厂模式的 UML 图
![Alt text](image-12.png)
### java实现
**步骤 1**
为形状创建一个接口。
```java
Shape.java
public interface Shape {
   void draw();
}
```

**步骤 2**
创建实现接口的实体类。
```java
Rectangle.java

Rectangle.java
public class Rectangle implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Rectangle::draw() method.");
   }
}
Square.java
public class Square implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Square::draw() method.");
   }
}
Circle.java
public class Circle implements Shape {
 
   @Override
   public void draw() {
      System.out.println("Inside Circle::draw() method.");
   }
}
```

**步骤 3**
为颜色创建一个接口。
```java
Color.java
public interface Color {
   void fill();
}
```

**步骤4**
创建实现接口的实体类。
```java
Red.java
public class Red implements Color {
 
   @Override
   public void fill() {
      System.out.println("Inside Red::fill() method.");
   }
}
Green.java
public class Green implements Color {
 
   @Override
   public void fill() {
      System.out.println("Inside Green::fill() method.");
   }
}
Blue.java
public class Blue implements Color {
 
   @Override
   public void fill() {
      System.out.println("Inside Blue::fill() method.");
   }
}
```
**步骤 5**
为 Color 和 Shape 对象创建抽象类来获取工厂。
```java
AbstractFactory.java
public abstract class AbstractFactory {
   public abstract Color getColor(String color);
   public abstract Shape getShape(String shape);
}
```

**步骤 6**
创建扩展了 AbstractFactory 的工厂类，基于给定的信息生成实体类的对象。
```java

ShapeFactory.java
public class ShapeFactory extends AbstractFactory {
    
   @Override
   public Shape getShape(String shapeType){
      if(shapeType == null){
         return null;
      }        
      if(shapeType.equalsIgnoreCase("CIRCLE")){
         return new Circle();
      } else if(shapeType.equalsIgnoreCase("RECTANGLE")){
         return new Rectangle();
      } else if(shapeType.equalsIgnoreCase("SQUARE")){
         return new Square();
      }
      return null;
   }
   
   @Override
   public Color getColor(String color) {
      return null;
   }
}
ColorFactory.java
public class ColorFactory extends AbstractFactory {
    
   @Override
   public Shape getShape(String shapeType){
      return null;
   }
   
   @Override
   public Color getColor(String color) {
      if(color == null){
         return null;
      }        
      if(color.equalsIgnoreCase("RED")){
         return new Red();
      } else if(color.equalsIgnoreCase("GREEN")){
         return new Green();
      } else if(color.equalsIgnoreCase("BLUE")){
         return new Blue();
      }
      return null;
   }
}
```

**步骤 7**
创建一个工厂创造器/生成器类，通过传递形状或颜色信息来获取工厂。
```java
FactoryProducer.java
public class FactoryProducer {
   public static AbstractFactory getFactory(String choice){
      if(choice.equalsIgnoreCase("SHAPE")){
         return new ShapeFactory();
      } else if(choice.equalsIgnoreCase("COLOR")){
         return new ColorFactory();
      }
      return null;
   }
}
```

**步骤 8**
使用 FactoryProducer 来获取 AbstractFactory，通过传递类型信息来获取实体类的对象。
```java
AbstractFactoryPatternDemo.java
public class AbstractFactoryPatternDemo {
   public static void main(String[] args) {
 
      //获取形状工厂
      AbstractFactory shapeFactory = FactoryProducer.getFactory("SHAPE");
 
      //获取形状为 Circle 的对象
      Shape shape1 = shapeFactory.getShape("CIRCLE");
 
      //调用 Circle 的 draw 方法
      shape1.draw();
 
      //获取形状为 Rectangle 的对象
      Shape shape2 = shapeFactory.getShape("RECTANGLE");
 
      //调用 Rectangle 的 draw 方法
      shape2.draw();
      
      //获取形状为 Square 的对象
      Shape shape3 = shapeFactory.getShape("SQUARE");
 
      //调用 Square 的 draw 方法
      shape3.draw();
 
      //获取颜色工厂
      AbstractFactory colorFactory = FactoryProducer.getFactory("COLOR");
 
      //获取颜色为 Red 的对象
      Color color1 = colorFactory.getColor("RED");
 
      //调用 Red 的 fill 方法
      color1.fill();
 
      //获取颜色为 Green 的对象
      Color color2 = colorFactory.getColor("GREEN");
 
      //调用 Green 的 fill 方法
      color2.fill();
 
      //获取颜色为 Blue 的对象
      Color color3 = colorFactory.getColor("BLUE");
 
      //调用 Blue 的 fill 方法
      color3.fill();
   }
}
```


**步骤 9**
执行程序，输出结果：
```shell
Inside Circle::draw() method.
Inside Rectangle::draw() method.
Inside Square::draw() method.
Inside Red::fill() method.
Inside Green::fill() method.
Inside Blue::fill() method.

```
### rust实现
```rust
// 定义接口

// 创建实体类
struct Rectangle;
struct Square;
struct  Circle;
struct ShapeFactory ;
struct ColorFactory ;
struct  FactoryProducer ;
struct Red;
struct Blue;
struct  Green;
pub trait Color{
    fn fill(&self);  
}
impl Color for Red {
    fn fill(&self) {
        println!("Inside Red::fill() method.");
    }
}
impl Color for Blue {
    fn fill(&self) {
        println!("Inside Blue::fill() method.");
    }
}
impl Color for Green {
    fn fill(&self) {
        println!("Inside Green::fill() method.");
    }
}


pub  trait Shape {
    fn draw(&self);  
}
impl Shape for Rectangle {
    fn draw(&self) {
        println!("Inside Rectangle::draw() method.");
    }
}
impl Shape for Square {
    fn draw(&self) {
        println!("Inside Square::draw() method.");
    }
}
impl Shape for Circle {
    fn draw(&self) {
        println!("Inside Circle::draw() method.");
    }
}
pub trait AbstractFactory {
    fn get_color(&self,color: &str)->Result<Box<dyn Color>>;
    fn get_shape(&self,shape: &str)->Box<dyn Shape>;
 }

impl AbstractFactory for ShapeFactory {
    fn get_shape(&self,shape_type: &str)->Box<dyn Shape>{
        if shape_type=="CIRCLE" {
            Box::new(Circle{})
        }else if shape_type=="RECTANGLE" {
            Box::new(Rectangle{})
        }else if  shape_type=="SQUARE"{
            Box::new(Square{})
        }else {
            panic!("输入的类型不存在");
        }
  
    }
    fn get_color(&self,_shape_type: &str)->Box<dyn Color>{

        panic!("输入的类型不存在");
  
    }
}
impl AbstractFactory for ColorFactory {
    fn get_color(&self,shape_type: &str)->Box<dyn Color>{
        if shape_type=="RED" {
            Box::new(Red{})
        }else if shape_type=="BLUE" {
            Box::new(Blue{})
        }else if  shape_type=="GREEN"{
            Box::new(Green{})
        }else {
            panic!("输入的类型不存在");
        }
    }
    fn get_shape(&self,_shape_type: &str)->Box<dyn Shape>{

        panic!("输入的类型不存在");
    }

}

impl  FactoryProducer {
    fn get_factory(choice: &str)-> Box<dyn AbstractFactory>{
        if choice=="COLOR" {
            Box::new(ColorFactory{})
        }else if choice=="SHAPE" {
            Box::new(ShapeFactory{})
        }else {
            panic!("输入的类型不存在");
        }
    }
}

fn main() {
    let shape=FactoryProducer::get_factory("SHAPE");
    let shape1=shape.get_shape("CIRCLE");
    shape1.draw();
    let shape2=shape.get_shape("RECTANGLE");
    shape2.draw();
    let shape3=shape.get_shape("SQUARE");
    shape3.draw();
    let color=FactoryProducer::get_factory("COLOR");
    let color1=color.get_color("RED");
    color1.fill();
    let color2=color.get_color("BLUE");
    color2.fill();
    let color3=color.get_color("GREEN");
    color3.fill();
}
```
## 单例模式
**单例模式**（Singleton Pattern）是最简单的设计模式之一。这种类型的设计模式属于创建型模式，它提供了一种创建对象的最佳方式。

这种模式涉及到一个单一的类，该类负责创建自己的对象，同时确保只有单个对象被创建。这个类提供了一种访问其唯一的对象的方式，可以直接访问，不需要实例化该类的对象。

单例模式是一种创建型设计模式，它确保一个类只有一个实例，并提供了一个全局访问点来访问该实例。

**注意**：

1. 单例类只能有一个实例。
2. 单例类必须自己创建自己的唯一实例。
3. 单例类必须给所有其他对象提供这一实例。

### 介绍
**意图**：保证一个类仅有一个实例，并提供一个访问它的全局访问点。

**主要解决**：一个全局使用的类频繁地创建与销毁。

**何时使用**：当您想控制实例数目，节省系统资源的时候。

**如何解决**：判断系统是否已经有这个单例，如果有则返回，如果没有则创建。

**关键代码**：构造函数是私有的。

####  应用实例：
1. 一个班级只有一个班主任。
2. Windows 是多进程多线程的，在操作一个文件的时候，就不可避免地出现多个进程或线程同时操作一个文件的现象，所以所有文件的处理必须通过唯一的实例来进行。
3. 一些设备管理器常常设计为单例模式，比如一个电脑有两台打印机，在输出的时候就要处理不能两台打印机打印同一个文件。

#### 优点
1. 在内存里只有一个实例，减少了内存的开销，尤其是频繁的创建和销毁实例（比如管理学院首页页面缓存）。
2. 避免对资源的多重占用（比如写文件操作）。
缺点：没有接口，不能继承，与单一职责原则冲突，一个类应该只关心内部逻辑，而不关心外面怎么样来实例化。

#### 使用场景

1. 要求生产唯一序列号。
2. WEB 中的计数器，不用每次刷新都在数据库里加一次，用单例先缓存起来。
3. 创建的一个对象需要消耗的资源过多，比如 I/O 与数据库的连接等。


### 架构图
我们将创建一个 SingleObject 类。SingleObject 类有它的私有构造函数和本身的一个静态实例。

SingleObject 类提供了一个静态方法，供外界获取它的静态实例。SingletonPatternDemo 类使用 SingleObject 类来获取 SingleObject 对象。

**单例模式的 UML 图**
![Alt text](image-13.png)
**步骤 1**
### JAVA 实现
创建一个 Singleton 类。
SingleObject.java
```java
public class SingleObject {
 
   //创建 SingleObject 的一个对象
   private static SingleObject instance = new SingleObject();
 
   //让构造函数为 private，这样该类就不会被实例化
   private SingleObject(){}
 
   //获取唯一可用的对象
   public static SingleObject getInstance(){
      return instance;
   }
 
   public void showMessage(){
      System.out.println("Hello World!");
   }
}
```


***步骤 2***
从 singleton 类获取唯一的对象。

SingletonPatternDemo.java
```java
public class SingletonPatternDemo {
   public static void main(String[] args) {
 
      //不合法的构造函数
      //编译时错误：构造函数 SingleObject() 是不可见的
      //SingleObject object = new SingleObject();
 
      //获取唯一可用的对象
      SingleObject object = SingleObject.getInstance();
 
      //显示消息
      object.showMessage();
   }
}
```

**步骤 3**
执行程序，输出结果：

Hello World!
#### 单例模式的几种实现方式
单例模式的实现有多种方式，如下所示：

1、**懒汉式**，线程不安全
- 是否 Lazy 初始化：是
- 是否多线程安全：否
- 实现难度：易
- 描述：这种方式是最基本的实现方式，这种实现最大的问题就是不支持多线程。因为没有加锁 synchronized，所以严格意义上它并不算单例模式。
这种方式 lazy loading 很明显，不要求线程安全，在多线程不能正常工作。

**实例**
```java
public class Singleton {  
    private static Singleton instance;  
    private Singleton (){}  
  
    public static Singleton getInstance() {  
        if (instance == null) {  
            instance = new Singleton();  
        }  
        return instance;  
    }  
}
```

接下来介绍的几种实现方式都支持多线程，但是在性能上有所差异。

2、**懒汉式**，线程安全
- 是否 Lazy 初始化：是
- 是否多线程安全：是
- 实现难度：易
- 描述：这种方式具备很好的 lazy loading，能够在多线程中很好的工作，但是，效率很低，99% 情况下不需要同步。
- 优点：第一次调用才初始化，避免内存浪费。
- 缺点：必须加锁 synchronized 才能保证单例，但加锁会影响效率。


**实例**
```java
public class Singleton {  
    private static Singleton instance;  
    private Singleton (){}  
    public static synchronized Singleton getInstance() {  
        if (instance == null) {  
            instance = new Singleton();  
        }  
        return instance;  
    }  
}
```

3、**饿汉式**
- 是否 Lazy 初始化：否
- 是否多线程安全：是
- 实现难度：易
- 描述：这种方式比较常用，但容易产生垃圾对象。
- 优点：没有加锁，执行效率会提高。
- 缺点：类加载时就初始化，浪费内存。

它基于 classloader 机制避免了多线程的同步问题，不过，instance 在类装载时就实例化，虽然导致类装载的原因有很多种，在单例模式中大多数都是调用 getInstance 方法， 但是也不能确定有其他的方式（或者其他的静态方法）导致类装载，这时候初始化 instance 显然没有达到 lazy loading 的效果。

**实例**
```java
public class Singleton {  
    private static Singleton instance = new Singleton();  
    private Singleton (){}  
    public static Singleton getInstance() {  
    return instance;  
    }  
}
```

4、**双检锁/双重校验锁（DCL，即 double-checked locking）**
- 是否 Lazy 初始化：是
- 是否多线程安全：是
- 实现难度：较复杂
- 描述：这种方式采用双锁机制，安全且在多线程情况下能保持高性能。

实例
```java
public class Singleton {  
    private volatile static Singleton singleton;  
    private Singleton (){}  
    public static Singleton getSingleton() {  
    if (singleton == null) {  
        synchronized (Singleton.class) {  
            if (singleton == null) {  
                singleton = new Singleton();  
            }  
        }  
    }  
    return singleton;  
    }  
}

```

5、**登记式/静态内部类**
- 是否 Lazy 初始化：是
- 是否多线程安全：是
- 实现难度：一般
- 描述：这种方式能达到双检锁方式一样的功效，但实现更简单。对静态域使用延迟初始化，应使用这种方式而不是双检锁方式。这种方式只适用于静态域的情况，双检锁方式可在实例域需要延迟初始化时使用。

这种方式同样利用了 classloader 机制来保证初始化 instance 时只有一个线程，它跟第 3 种方式不同的是：第 3 种方式只要 Singleton 类被装载了，那么 instance 就会被实例化（没有达到 lazy loading 效果），而这种方式是 Singleton 类被装载了，instance 不一定被初始化。因为 SingletonHolder 类没有被主动使用，只有通过显式调用 getInstance 方法时，才会显式装载 SingletonHolder 类，从而实例化 instance。想象一下，如果实例化 instance 很消耗资源，所以想让它延迟加载，另外一方面，又不希望在 Singleton 类加载时就实例化，因为不能确保 Singleton 类还可能在其他的地方被主动使用从而被加载，那么这个时候实例化 instance 显然是不合适的。这个时候，这种方式相比第 3 种方式就显得很合理。

**实例**
```java
public class Singleton {  
    private static class SingletonHolder {  
    private static final Singleton INSTANCE = new Singleton();  
    }  
    private Singleton (){}  
    public static final Singleton getInstance() {  
        return SingletonHolder.INSTANCE;  
    }  
}
```

6、**枚举**
- 是否 Lazy 初始化：否
- 是否多线程安全：是
- 实现难度：易
- 描述：这种实现方式还没有被广泛采用，但这是实现单例模式的最佳方法。它更简洁，自动支持序列化机制，绝对防止多次实例化。
这种方式是 Effective Java 作者 Josh Bloch 提倡的方式，它不仅能避免多线程同步问题，而且还自动支持序列化机制，防止反序列化重新创建新的对象，绝对防止多次实例化。不过，由于 JDK1.5 之后才加入 enum 特性，用这种方式写不免让人感觉生疏，在实际工作中，也很少用。
**实例**
```java
public enum Singleton {  
    INSTANCE;  
    public void whateverMethod() {  
    }  
}
```
### rust实现
在用rust进行懒加载时，最方便的还是用第三方库，本人运用的是`lazy_static`库，在用这社区库时，需要引入在Cargo.toml文件下的`[dependencies]`项目下引lazy_static = "1.4.0"。如图
![Alt text](image-14.png)

```rust
use std::sync::{Arc, Mutex};
use lazy_static::lazy_static;
 struct Singleton;
 impl Singleton {
    //关联方法， 获取单例实例的方法
    fn get_instance() -> Arc<Mutex<Singleton>> {
        // 使用懒加载创建单例实例
        // 这里使用了 Arc 和 Mutex 来实现线程安全的单例
        // 只有第一次调用 get_instance 时会创建实例，之后都会返回已创建的实例
        static mut INSTANCE: Option<Arc<Mutex<Singleton>>> = None;//静态初始化，只运行一次
         unsafe {
            // get_or_insert_with ,如果是 None ，则将从data计算的值插入选项中，然后返回对包含值的可变引用。
            INSTANCE.get_or_insert_with(|| {
                Arc::new(Mutex::new(Singleton {}))}).clone()
        }
    }
    fn show_message(&self){
        println!("Hello World!");
     }
}

// 使用lazy_static的懒加载
struct SingletonL;
impl SingletonL {
    fn show_message(&self){
        println!("Hello World!");
     }
}
lazy_static! {
    static ref INSTANCE: Mutex<SingletonL> = Mutex::new(SingletonL {   });
}

fn main() {
  // 获取单例实例,自定义
  let instance1 = Singleton::get_instance();
  
   // 修改单例数据
  {
      let instance = instance1.lock().unwrap();
      instance.show_message();
  }
  // 获取单例实例,社区lazy_static
  let instance = INSTANCE.lock().unwrap();
  instance.show_message();
}
```                                                         
## 建造者模式
建造者模式（Builder Pattern）使用多个简单的对象一步一步构建成一个复杂的对象。

一个 Builder 类会一步一步构造最终的对象。该 Builder 类是独立于其他对象的。

### 介绍
- **意图**：将一个复杂的构建与其表示相分离，使得同样的构建过程可以创建不同的表示。
- **主要解决**：主要解决在软件系统中，有时候面临着"一个复杂对象"的创建工作，其通常由各个部分的子对象用一定的算法构成；由于需求的变化，这个复杂对象的各个部分经常面临着剧烈的变化，但是将它们组合在一起的算法却相对稳定。
- **关键代码**：建造者：创建和提供实例，导演：管理建造出来的实例的依赖关系。
- **应用实例**： 1、去肯德基，汉堡、可乐、薯条、炸鸡翅等是不变的，而其组合是经常变化的，生成出所谓的"套餐"。
#### 优点
- 分离构建过程和表示，使得构建过程更加灵活，可以构建不同的表示。
- 可以更好地控制构建过程，隐藏具体构建细节。
- 代码复用性高，可以在不同的构建过程中重复使用相同的建造者。
#### 缺点
- 如果产品的属性较少，建造者模式可能会导致代码冗余。
- 建造者模式增加了系统的类和对象数量。

#### 使用场景
- 需要生成的对象具有复杂的内部结构。 
- 需要生成的对象内部属性本身相互依赖。

建造者模式在创建复杂对象时非常有用，特别是当对象的构建过程涉及多个步骤或参数时。它可以提供更好的灵活性和可维护性，同时使得代码更加清晰可读。


### 实现
我们假设一个快餐店的商业案例，其中，一个典型的套餐可以是一个汉堡（Burger）和一杯冷饮（Cold drink）。汉堡（Burger）可以是素食汉堡（Veg Burger）或鸡肉汉堡（Chicken Burger），它们是包在纸盒中。冷饮（Cold drink）可以是可口可乐（coke）或百事可乐（pepsi），它们是装在瓶子中。

我们将创建一个表示食物条目（比如汉堡和冷饮）的 Item 接口和实现 Item 接口的实体类，以及一个表示食物包装的 Packing 接口和实现 Packing 接口的实体类，汉堡是包在纸盒中，冷饮是装在瓶子中。

然后我们创建一个 Meal 类，带有 Item 的 ArrayList 和一个通过结合 Item 来创建不同类型的 Meal 对象的 MealBuilder。BuilderPatternDemo 类使用 MealBuilder 来创建一个 Meal。

建造者模式的 UML 图
![Alt text](image-15.png)
### java
**步骤 1**
创建一个表示食物条目和食物包装的接口。
Item.java
```java
public interface Item {
   public String name();
   public Packing packing();
   public float price();    
}
Packing.java
public interface Packing {
   public String pack();
}

```
**步骤 2**
创建实现 Packing 接口的实体类,方便进行不同的包装。
Wrapper.java
```java
public class Wrapper implements Packing {
 
   @Override
   public String pack() {
      return "Wrapper";
   }
}
```

Bottle.java
```java
public class Bottle implements Packing {
 
   @Override
   public String pack() {
      return "Bottle";
   }
}
```

**步骤 3**
创建实现 Item 接口的抽象类，该类提供了默认的功能,实现汉堡抽象和冷饮抽象的包装类。

Burger.java
```java
public abstract class Burger implements Item {
 
   @Override
   public Packing packing() {
      return new Wrapper();
   }
 
   @Override
   public abstract float price();
}
```

ColdDrink.java
```java
public abstract class ColdDrink implements Item {
 
    @Override
    public Packing packing() {
       return new Bottle();
    }
 
    @Override
    public abstract float price();
}
```

**步骤 4**
创建扩展了 Burger 和 ColdDrink 的实体类。

VegBurger.java
```java
public class VegBurger extends Burger {
 
   @Override
   public float price() {
      return 25.0f;
   }
 
   @Override
   public String name() {
      return "Veg Burger";
   }
}
```

ChickenBurger.java
```java
public class ChickenBurger extends Burger {
 
   @Override
   public float price() {
      return 50.5f;
   }
 
   @Override
   public String name() {
      return "Chicken Burger";
   }
}
```

Coke.java
```java

public class Coke extends ColdDrink {
 
   @Override
   public float price() {
      return 30.0f;
   }
 
   @Override
   public String name() {
      return "Coke";
   }
}
```
Pepsi.java
```java

public class Pepsi extends ColdDrink {
 
   @Override
   public float price() {
      return 35.0f;
   }
 
   @Override
   public String name() {
      return "Pepsi";
   }
}
```

**步骤 5**
创建一个 Meal 类，带有上面定义的 Item 对象。

Meal.java
```java
import java.util.ArrayList;
import java.util.List;
 
public class Meal {
   private List<Item> items = new ArrayList<Item>();    
 
   public void addItem(Item item){
      items.add(item);
   }
 
   public float getCost(){
      float cost = 0.0f;
      for (Item item : items) {
         cost += item.price();
      }        
      return cost;
   }
 
   public void showItems(){
      for (Item item : items) {
         System.out.print("Item : "+item.name());
         System.out.print(", Packing : "+item.packing().pack());
         System.out.println(", Price : "+item.price());
      }        
   }    
}

```

**步骤 6**
创建一个 MealBuilder 类，实际的 builder 类负责创建 Meal 对象。

MealBuilder.java
```java
public class MealBuilder {
 
   public Meal prepareVegMeal (){
      Meal meal = new Meal();
      meal.addItem(new VegBurger());
      meal.addItem(new Coke());
      return meal;
   }   
 
   public Meal prepareNonVegMeal (){
      Meal meal = new Meal();
      meal.addItem(new ChickenBurger());
      meal.addItem(new Pepsi());
      return meal;
   }
}
```

**步骤 7**
BuiderPatternDemo 使用 MealBuilder 来演示建造者模式（Builder Pattern）。

BuilderPatternDemo.java
```java
public class BuilderPatternDemo {
   public static void main(String[] args) {
      MealBuilder mealBuilder = new MealBuilder();
 
      Meal vegMeal = mealBuilder.prepareVegMeal();
      System.out.println("Veg Meal");
      vegMeal.showItems();
      System.out.println("Total Cost: " +vegMeal.getCost());
 
      Meal nonVegMeal = mealBuilder.prepareNonVegMeal();
      System.out.println("\n\nNon-Veg Meal");
      nonVegMeal.showItems();
      System.out.println("Total Cost: " +nonVegMeal.getCost());
   }
}
```

**步骤 8**
执行程序，输出结果：
```shell

Veg Meal
Item : Veg Burger, Packing : Wrapper, Price : 25.0
Item : Coke, Packing : Bottle, Price : 30.0
Total Cost: 55.0


Non-Veg Meal
Item : Chicken Burger, Packing : Wrapper, Price : 50.5
Item : Pepsi, Packing : Bottle, Price : 35.0
Total Cost: 85.5
```
### rust
因为rust的类支持组合式而不支持继承，在进行建造者构件时比java更加容易，rust的trait是支持继承的。
```rust
// rsut trait不支持重名
pub trait Item {
    fn name(&self)->String;   
    fn price(&self)->f32;   
    fn packing(&self)->String;
}

// 汉堡实体类
struct ChickenBurger;
impl Item for ChickenBurger {
    fn name(&self)->String {
        String::from("ChickenBurger")
    }
    fn price(&self)->f32 {
        35.0
    }
    fn packing(&self)->String {
        String::from("Wrappper")
    }
   
}  
struct VegBurger;
impl Item for VegBurger {
    fn name(&self)->String {
        String::from("Pepsi")
    }
    fn price(&self)->f32 {
        35.0
    }
    fn packing(&self)->String {
        String::from("Wrappper")
    }
}  

// 饮料实体类
struct Pepsi;

impl Item for Pepsi {
    fn name(&self)->String {
        String::from("Pesi")
    }
    fn price(&self)->f32 {
        35.0
    }
    fn packing(&self)->String {
        String::from("Bottle")
    }
}  
struct Coke;

impl Item for Coke {
    fn name(&self)->String {
        String::from("Coke")
    }
    fn price(&self)->f32 {
        35.0
    }
    fn packing(&self)->String {
        String::from("Bottle")
    }
}  

struct Meal {
    items:Vec<Box<dyn Item>>,
}
impl Meal {
    fn add_item<T>(&mut self,item:Box<dyn Item>) 
    {
        self.items.push(item)
    }
    fn get_cost(&self)->f32{
        // 普通函数实现
        // let mut sum:f32=0.0; 
        // for i in self.items.iter()  {
        //     let price = i.price();
        //     sum+=price;
        // }
        // sum

        // 函数sji
        self.items.iter().fold(0.0, |acc, x| acc + x.price())
    }
    fn  show_items(&self){
        for  i in self.items.iter() {
            println!("{}",i.name());
            println!("{}",i.packing());
            println!("{}",i.price());
        }
    }
}
// 添加建造者
struct MealBuilder {}
impl  MealBuilder {
    fn prepareVegMeal()->Meal{
        let mut meal=Meal{items:Vec::new()};
        meal.add_item::<Box<dyn Item>>(Box::new(VegBurger{}));
        meal.add_item::<Box<dyn Item>>(Box::new(Coke{}));
        meal
    }
    fn prepareNonVegMeal()->Meal{
        let mut meal=Meal{items:Vec::new()};
        meal.add_item::<Box<dyn Item>>(Box::new(ChickenBurger{}));
        meal.add_item::<Box<dyn Item>>(Box::new(Pepsi{}));
        meal
    }
}
fn main() {
    let m=MealBuilder::prepareVegMeal();
    println!(" Veg Meal");
    m.show_items();
    println!("Total Cost : {}",m.get_cost());
    let m=MealBuilder::prepareNonVegMeal();
    println!(" \n\nNon-Veg Meal");
    m.show_items();
    println!("Total Cost : {}",m.get_cost());
}
```

## 原型模式
原型模式（Prototype Pattern）是用于创建重复的对象，同时又能保证性能。

这种模式是实现了一个原型接口，该接口用于创建当前对象的克隆。当直接创建对象的代价比较大时，则采用这种模式。例如，一个对象需要在一个高代价的数据库操作之后被创建。我们可以缓存该对象，在下一个请求时返回它的克隆，在需要的时候更新数据库，以此来减少数据库调用。

### 介绍
- **意图**：用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。
- **主要解决**：在运行期建立和删除原型。
- **何时使用**： 1、当一个系统应该独立于它的产品创建，构成和表示时。 2、当要实例化的类是在运行时刻指定时，例如，通过动态装载。 3、为了避免创建一个与产品类层次平行的工厂类层次时。 4、当一个类的实例只能有几个不同状态组合中的一种时。建立相应数目的原型并克隆它们可能比每次用合适的状态手工实例化该类更方便一些。
- 如何解决：利用已有的一个原型对象，快速地生成和原型对象一样的实例。
- **关键代码**： 1、实现克隆操作，在 JAVA 实现 Cloneable 接口，重写 clone()，在 rust中可以使用clone（） 方法来实现对象的深拷贝。 2、原型模式同样用于隔离类对象的使用者和具体类型（易变类）之间的耦合关系，它同样要求这些"易变类"拥有稳定的接口。
- **应用实例**： 1、细胞分裂。 2、考试中为每个考生分发相同的试卷。
####  优点
1、性能提高。 
2、逃避构造函数的约束。
#### 缺点
1、配备克隆方法需要对类的功能进行通盘考虑，这对于全新的类不是很难，但对于已有的类不一定很容易，特别当一个类引用不支持串行化的间接对象，或者引用含有循环结构的时候。 

####  使用场景
1、资源优化场景。
2、类初始化需要消化非常多的资源，这个资源包括数据、硬件资源等。 3、性能和安全要求的场景。 
4、通过 new 产生一个对象需要非常繁琐的数据准备或访问权限，则可以使用原型模式。 5、一个对象多个修改者的场景。 
6、一个对象需要提供给其他对象访问，而且各个调用者可能都需要修改其值时，可以考虑使用原型模式拷贝多个对象供调用者使用。 
7、在实际项目中，原型模式很少单独出现，一般是和工厂方法模式一起出现，通过 clone 的方法创建一个对象，然后由工厂方法提供给调用者。



### 实现
我们将创建一个抽象类 Shape 和扩展了 Shape 类的实体类。下一步是定义类 ShapeCache，该类把 shape 对象存储在一个 Hashtable 中，并在请求的时候返回它们的克隆。

PrototypePatternDemo 类使用 ShapeCache 类来获取 Shape 对象。

原型模式的 UML 图
![Alt text](image-16.png)
### java 实现
**步骤 1**
创建一个实现了 Cloneable 接口的抽象类。
Shape.java
```java
public abstract class Shape implements Cloneable {
   
   private String id;
   protected String type;
   
   abstract void draw();
   
   public String getType(){
      return type;
   }
   
   public String getId() {
      return id;
   }
   
   public void setId(String id) {
      this.id = id;
   }
   
   public Object clone() {
      Object clone = null;
      try {
         clone = super.clone();
      } catch (CloneNotSupportedException e) {
         e.printStackTrace();
      }
      return clone;
   }
}
```

**步骤 2**
创建扩展了上面抽象类的实体类。
Rectangle.java
```java
public class Rectangle extends Shape {
 
   public Rectangle(){
     type = "Rectangle";
   }
 
   @Override
   public void draw() {
      System.out.println("Inside Rectangle::draw() method.");
   }
}
```


Square.java
```java
public class Square extends Shape {
 
   public Square(){
     type = "Square";
   }
 
   @Override
   public void draw() {
      System.out.println("Inside Square::draw() method.");
   }
}
```

Circle.java
```java
public class Circle extends Shape {
 
   public Circle(){
     type = "Circle";
   }
 
   @Override
   public void draw() {
      System.out.println("Inside Circle::draw() method.");
   }
}
```
**步骤 3**
创建一个类，从数据库获取实体类，并把它们存储在一个 Hashtable 中。
ShapeCache.java
```java
import java.util.Hashtable;
 
public class ShapeCache {
    
   private static Hashtable<String, Shape> shapeMap 
      = new Hashtable<String, Shape>();
 
   public static Shape getShape(String shapeId) {
      Shape cachedShape = shapeMap.get(shapeId);
      return (Shape) cachedShape.clone();
   }
 
   // 对每种形状都运行数据库查询，并创建该形状
   // shapeMap.put(shapeKey, shape);
   // 例如，我们要添加三种形状
   public static void loadCache() {
      Circle circle = new Circle();
      circle.setId("1");
      shapeMap.put(circle.getId(),circle);
 
      Square square = new Square();
      square.setId("2");
      shapeMap.put(square.getId(),square);
 
      Rectangle rectangle = new Rectangle();
      rectangle.setId("3");
      shapeMap.put(rectangle.getId(),rectangle);
   }
}
```

**步骤 4**
PrototypePatternDemo 使用 ShapeCache 类来获取存储在 Hashtable 中的形状的克隆。

PrototypePatternDemo.java
```java
public class PrototypePatternDemo {
   public static void main(String[] args) {
      ShapeCache.loadCache();
 
      Shape clonedShape = (Shape) ShapeCache.getShape("1");
      System.out.println("Shape : " + clonedShape.getType());        
 
      Shape clonedShape2 = (Shape) ShapeCache.getShape("2");
      System.out.println("Shape : " + clonedShape2.getType());        
 
      Shape clonedShape3 = (Shape) ShapeCache.getShape("3");
      System.out.println("Shape : " + clonedShape3.getType());        
   }
}
```
**步骤 5**
执行程序，输出结果：
```shell
Shape : Circle
Shape : Square
Shape : Rectangle
```
### rust 实现
```rs
#[derive(Clone)]
struct Shape{
    id:String,
    mtype:String
}
impl Shape{
    fn set_id(&mut self,id:String){
        self.id=id;
    }
    fn get_id(&self)->&str{
        &self.id
    }
}
#[derive(Clone)]
struct  Rectangle{
    shape:Shape
}
impl Rectangle {
    fn new()->Rectangle {
        Rectangle{shape:Shape{
            id:String::from("value"),
            mtype:String::from("Rectangle")
        }}
    }
    fn draw() {
        println!("Inside Rectangle::draw() method.");
    }
}
#[derive(Clone)]
struct  Square {
    shape:Shape
}
impl Square  {
    fn new()->Square  {
        Square {shape:Shape{
            id:String::from("value"),
            mtype:String::from("Square ")
        }}
    }
    fn draw() {
        println!("Inside Square ::draw() method.");
    }
}
#[derive(Clone)]
struct  Circle {
    shape:Shape
}
impl Circle  {
    fn new()->Circle {
        Circle {shape:Shape{
            id:String::from("value"),
            mtype:String::from("Square ")
        }}
    }
    fn draw() {
        println!("Inside Circle ::draw() method.");
    }
}

fn main(){
    let s=Circle::new();
    let mut s1=s.clone();
    s1.shape.set_id(String::from("dsf"));
    println!("{}",s.shape.id);
    println!("{}",s1.shape.id);

}
```
# 结构型模式
## 适配器模式
适配器模式（Adapter Pattern）是作为两个不兼容的接口之间的桥梁。这种类型的设计模式属于结构型模式，它结合了两个独立接口的功能。

这种模式涉及到一个单一的类，该类负责加入独立的或不兼容的接口功能。举个真实的例子，读卡器是作为内存卡和笔记本之间的适配器。您将内存卡插入读卡器，再将读卡器插入笔记本，这样就可以通过笔记本来读取内存卡。



### 介绍
- **意图**：将一个类的接口转换成客户希望的另外一个接口。适配器模式使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。
- **主要解决**：主要解决在软件系统中，常常要将一些"现存的对象"放到新的环境中，而新环境要求的接口是现对象不能满足的。
- **关键代码**：适配器继承或依赖已有的对象，实现想要的目标接口。

#### 何时使用
1、系统需要使用现有的类，而此类的接口不符合系统的需要。
2、想要建立一个可以重复使用的类，用于与一些彼此之间没有太大关联的一些类，包括一些可能在将来引进的类一起工作，这些源类不一定有一致的接口。 
3、通过接口转换，将一个类插入另一个类系中。（比如老虎和飞禽，现在多了一个飞虎，在不增加实体的需求下，增加一个适配器，在里面包容一个虎对象，实现飞的接口。）



#### 应用实例
1、美国电器 110V，中国 220V，就要有一个适配器将 110V 转化为 220V。 
2、在 LINUX 上运行 WINDOWS 程序。 
3、JAVA 中的 jdbc。

####  优点
1、可以让任何两个没有关联的类一起运行。 
2、提高了类的复用。 
3、增加了类的透明度。 
4、灵活性好。

#### 缺点
1、过多地使用适配器，会让系统非常零乱，不易整体进行把握。比如，明明看到调用的是 A 接口，其实内部被适配成了 B 接口的实现，一个系统如果太多出现这种情况，无异于一场灾难。因此如果不是很有必要，可以不使用适配器，而是直接对系统进行重构。 
2.由于 JAVA 至多继承一个类，所以至多只能适配一个适配者类，而且目标类必须是抽象类。

#### 使用场景
有动机地修改一个正常运行的系统的接口，这时应该考虑使用适配器模式。



### 实现
我们有一个 MediaPlayer 接口和一个实现了 MediaPlayer 接口的实体类 AudioPlayer。默认情况下，AudioPlayer 可以播放 mp3 格式的音频文件。

我们还有另一个接口 AdvancedMediaPlayer 和实现了 AdvancedMediaPlayer 接口的实体类。该类可以播放 vlc 和 mp4 格式的文件。

我们想要让 AudioPlayer 播放其他格式的音频文件。为了实现这个功能，我们需要创建一个实现了 MediaPlayer 接口的适配器类 MediaAdapter，并使用 AdvancedMediaPlayer 对象来播放所需的格式。

AudioPlayer 使用适配器类 MediaAdapter 传递所需的音频类型，不需要知道能播放所需格式音频的实际类。AdapterPatternDemo 类使用 AudioPlayer 类来播放各种格式。

适配器模式的 UML 图
![Alt text](image-17.png)
### java实现
**步骤 1**
为媒体播放器和更高级的媒体播放器创建接口。

MediaPlayer.java
```java
public interface MediaPlayer {
   public void play(String audioType, String fileName);
}
AdvancedMediaPlayer.java
public interface AdvancedMediaPlayer { 
   public void playVlc(String fileName);
   public void playMp4(String fileName);
}
```

**步骤 2**
创建实现了 AdvancedMediaPlayer 接口的实体类。

VlcPlayer.java
```java
public class VlcPlayer implements AdvancedMediaPlayer{
   @Override
   public void playVlc(String fileName) {
      System.out.println("Playing vlc file. Name: "+ fileName);      
   }
 
   @Override
   public void playMp4(String fileName) {
      //什么也不做
   }
}
```

Mp4Player.java
```java
public class Mp4Player implements AdvancedMediaPlayer{
 
   @Override
   public void playVlc(String fileName) {
      //什么也不做
   }
 
   @Override
   public void playMp4(String fileName) {
      System.out.println("Playing mp4 file. Name: "+ fileName);      
   }
}
```

**步骤 3**
创建实现了 MediaPlayer 接口的适配器类。

MediaAdapter.java
```java
public class MediaAdapter implements MediaPlayer {
 
   AdvancedMediaPlayer advancedMusicPlayer;
 
   public MediaAdapter(String audioType){
      if(audioType.equalsIgnoreCase("vlc") ){
         advancedMusicPlayer = new VlcPlayer();       
      } else if (audioType.equalsIgnoreCase("mp4")){
         advancedMusicPlayer = new Mp4Player();
      }  
   }
 
   @Override
   public void play(String audioType, String fileName) {
      if(audioType.equalsIgnoreCase("vlc")){
         advancedMusicPlayer.playVlc(fileName);
      }else if(audioType.equalsIgnoreCase("mp4")){
         advancedMusicPlayer.playMp4(fileName);
      }
   }
}
```

**步骤 4**
创建实现了 MediaPlayer 接口的实体类。

AudioPlayer.java
```java
public class AudioPlayer implements MediaPlayer {
   MediaAdapter mediaAdapter; 
 
   @Override
   public void play(String audioType, String fileName) {    
 
      //播放 mp3 音乐文件的内置支持
      if(audioType.equalsIgnoreCase("mp3")){
         System.out.println("Playing mp3 file. Name: "+ fileName);         
      } 
      //mediaAdapter 提供了播放其他文件格式的支持
      else if(audioType.equalsIgnoreCase("vlc") 
         || audioType.equalsIgnoreCase("mp4")){
         mediaAdapter = new MediaAdapter(audioType);
         mediaAdapter.play(audioType, fileName);
      }
      else{
         System.out.println("Invalid media. "+
            audioType + " format not supported");
      }
   }   
}
```

**步骤 5**
使用 AudioPlayer 来播放不同类型的音频格式。

AdapterPatternDemo.java
```java
public class AdapterPatternDemo {
   public static void main(String[] args) {
      AudioPlayer audioPlayer = new AudioPlayer();
 
      audioPlayer.play("mp3", "beyond the horizon.mp3");
      audioPlayer.play("mp4", "alone.mp4");
      audioPlayer.play("vlc", "far far away.vlc");
      audioPlayer.play("avi", "mind me.avi");
   }
}
```

**步骤 6**
执行程序，输出结果：
```shell
Playing mp3 file. Name: beyond the horizon.mp3
Playing mp4 file. Name: alone.mp4
Playing vlc file. Name: far far away.vlc
Invalid media. avi format not supported
```

### rust 实现
```rust

use std::error::Error;
// 播放器接口
trait  MediaPlayer{
    fn paly(&mut self,audio_type:String, file_name:String);
}
// 适配器接口
trait AdvancedMediaPlayer {
    fn play_vlc(&self ,file_name:String);
    fn play_mp4(&self,file_name:String );
}
// vlc播器放实体类
struct  VlcPlayer {}
impl AdvancedMediaPlayer for VlcPlayer {
    fn play_vlc(&self ,file_name:String) {
        println!("Playing vlc file. Name: {}",file_name)
    }

    fn play_mp4(&self,file_name:String ) {
        todo!()
    }
}
// MP4播放器实体类
struct  Mp4Player {}
impl AdvancedMediaPlayer for Mp4Player {
    fn play_mp4(&self ,file_name:String) {
        println!("Playing mp4 file. Name: {}",file_name)
    }

    fn play_vlc(&self,file_name:String ) {
        todo!()
    }
}
// 播放器适配器实体类
struct MediaAdapter{
    advanced_music_player:Box<dyn AdvancedMediaPlayer>
}
impl MediaPlayer for MediaAdapter {
    fn paly(&mut self,audio_type:String, file_name:String) {
        match &audio_type as &str{
            "vlc"=> self.advanced_music_player.play_vlc(file_name),
            "mp4"=>self.advanced_music_player.play_mp4(file_name),
            _ =>println!("不支持此格式文件")
        }
    }
}
impl MediaAdapter {
    fn new (audio_type:String )->Result<MediaAdapter,Box<dyn Error>>{
        //进行字符产匹配
        match &audio_type as &str{
            "vlc"=> Ok(MediaAdapter{advanced_music_player:Box::new(VlcPlayer{})}),
            "mp4"=>Ok(MediaAdapter{advanced_music_player:Box::new(Mp4Player{})}),
            _ =>Err(panic!("输入运行格式错误"))
        }
    }
}
struct AudioPlayer{
    media_adapter:MediaAdapter 
}
impl AudioPlayer {
    fn new()->AudioPlayer{
        AudioPlayer{media_adapter:MediaAdapter { advanced_music_player:Box::new(Mp4Player{})}}
    }
}
impl  MediaPlayer for AudioPlayer {
    fn paly(&mut self,audio_type:String, file_name:String) {
        match &audio_type as &str{
            "vlc"|"mp4"=>{
                self.media_adapter=MediaAdapter::new(audio_type.clone()).unwrap();
                self.media_adapter.paly(audio_type, file_name);
            },
            _ =>println!("不支持此格式文件")
        }
    }
}
    
fn main() {
    let mut audioPlayer =AudioPlayer::new();
    // 进行不同文件的播放测试
    audioPlayer.paly(String::from("mp3"), String::from("beyond the horizon.mp3"));
    audioPlayer.paly(String::from("mp4"), String::from("alone.mp4"));
    audioPlayer.paly(String::from("mp4"), String::from("far far away.vlc"));
}
```
# 模板方法
**模板方法**定义一个操作中的算法的骨架，而将这一些步骤延迟到子类中。模板方式使得子类可以不改变一个算法的结构可重新定义该算法的某些特定步骤。
# 迪米特法则
**迪米特法则**如果两个类不必彼此直接通信，那么这两个类就不应当发生直接的相互作用。如果其中一个类需要调用另一个类的某一个方法的话，可以通过第三者转发这个调用。

# 外观
**外观模式**：为子系统中的一组接口提供一个一致的界面，此模式定义了一个高层接口，这个接口使得这一子系统更加容易使用。

## 何时使用外观模式

首先，在设计初期阶段，应该要有意识的将不同的两个层分离，其次，开发阶段，子系统往往因为不断地重构演化而变得越来越复杂，增加外观Facade可以提供一个及暗淡的接口，减少它们之间的依赖，第三，在维护一个遗留的大型系统时，可能这个系统已经非常难以维护和拓展了，可以为新系统开发一个外观Facade类，来提供设计粗糙或者高度复杂的遗留代码的比较清晰简单的接口，让新系统与Facade对象交互，Facade与遗留代码交互所有复杂的工作。


# 建造者模式
 
**建造者模式**将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的的表示。

# 观察者模式
**观察者模式**又叫发布-订阅模式： 定义了一种一对多的依赖关系，让多个观察对象同时监听某一个主题对象，这个主题对象在状态发生变化时，会通知所有观察者对象，使他们能够自动更新自己，

## 事件委托
委托就是一种引用方法的类型。一旦为委托分配了方法，委托将于该方法具有完全相同的行为，委托方法的使用，可以像其他任何方法一样，具有参数和返回值。委托可以看作是对函数的抽象，是函数的“类”，委托的实例将代表一个具体的函数。  




# 状态模式
**状态模式**，当一个对象的内在状态改变时允许改变其行为，这个对象看起来是改变了其类。
"状态模式主要解决的是当时控制一个对象的状态转换的条件表达式过于复杂的情况。把状态的判断逻辑转移到表示不同的一系列类中，可以把复杂的判断逻辑简化。

# 设配器模式
**适配器模式**： 将一个类的接口转换成客户希望的另外一个接口，Adaper模式使得原本不兼容而不能一起工作的那些类可以一起工作。
![Alt text](image.png)

# 备忘录
**备忘录**：在不破坏封装性的前提下，捕获一个对家的内部状态，并在该对象之外保存这个状态。这样以后就可将该对象恢复到原先保存的状态。
![Alt text](image-1.png)

# 组合模式
**组合模式**：将对象组合成树形结构以表示‘部分-整体’的层次结构，组合模式使得用户对单个对象和组合对象的使用具有一致性。
![Alt text](image-2.png)

# 迭代器模式
**迭代器模式**：提供一种方法顺序访问一个聚合对象中各个元素，而又不暴露该对象的内部表示。

![Alt text](image-3.png)

# 单例模式
保证一个类只有一个实例，并提供一个访问它的全局访问点。


# 桥接模式
**合成/聚合复用原则** 尽量使用合成/聚合，尽量不要使用类继承。


**桥接模式**；将抽象部分与他的实现部分分离，使他们都可以独立的变化。
![Alt text](image-4.png)

# 命令模式、
**命令行模式**：将一个请求对象封装成一个对象，从而使你可用不同的请求对客户进行参数化，对请求排队或记录请求日志，以及支持可撤销的操作。
![Alt text](image-5.png)

# 职责链模式

**职责链模式**：使多个对象都有机会处理请求，从而避免发送者和接收者之间的耦合关系。将这个对象连成一条链，并沿着这条链传递该请求，直到有一个对象处理它为止。
![Alt text](image-6.png)

# 中介者模式
**中介者模式**：用中介对象封装一系列对象交互。中介者使各对象不需要显式的互相引用，从而使其耦合松散，而且可以独立的改变他们之间的交互。
![Alt text](image-7.png)

# 享元模式
**享元模式**：运用共享技术有效的支持大量细粒度的对象。
![Alt text](image-8.png)

享元模式可以避免大量非常相似类的开销。在程序设计中，有时需要生成大量细粒度的类实例来表示数据。如果能发现这些实例除了几个参数外基本上都是相同的，有时就能够受大幅度的减少需要实例化的类的数量。如果能把能发现这些实例除了几个参数外基本都是相同的，有时就能够受大幅度的减少需要实例化类的数量。如果能把那些参数移到类实例外面，在方法调用时将他们传递进来吗，就可以通过共享大幅度地减少单个实例的数目。

# 解释器模式

**解释器模式**：给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。

![Alt text](image-9.png)

如果一种特定的的问题发生的频率足够高，那么可能就值得将该的=问题的各个实例表述未一个简单语言中的句子。

# 访问者模式

**访问者模式**:表示一个作用于某对象结构中的各元素的操作。它使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。

![Alt text](image-10.png)