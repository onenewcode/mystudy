# Java GUI——Java图形用户界面
## AWT
#### AWT概述
抽象窗口工具包AWT（Abstract Window Toolkit）是java提供的建立图形用户界面GUI的开发包，AWT可用于Java的Applet 和 Application 中。java.awt包提供了基本的GUI设计工具，主要包括组件（Component）、容器（Container）和布局管理器（LayoutManager）三个概念。 java的图形用户界面的最基本组成部分是组件，组件是一个可以以图形化的方式显示在屏幕上并能与用户进行交互的对象，例如一个按钮、一个标签等。组件不能独立的显示出来，必须将组件放在一定的容器中才可以显示出来。 

#### 容器（Container）
   容器是Component的子类，一个容器可以容纳多个组件，并使他们成为一个整体。容器可以简化图形化界面的设计，以整体结构来布置界面，所有的组件都可以通过add()方法加入容器中。

    有三种类型的容器：Window、Panel、ScrollPane

    Window类：是不依赖其他容器而独立存在的容器他有两个子类分别是Frame类和Dialog类。Frame类用于创建一个具有标题栏的框架窗口作为程序的主要界面，Dialog类用于创建一个对话框，实现与用户的信息交换。

    Panel类：也是一个容器,但是他不能单独存在,只能存在于其他容器(window或其子类)中,一个panel对象代表了一个长方形的区域,在这个区域中可以容纳其他组件，在程序中通常会使panel来实现一些特殊的布局。

    ScrollPane类：用于实现单个子组件的自动水平和/或垂直滚动的容器类。因此该类创建的对象也是一个容器，称为滚动面板。

    常用的容器有：Panel、Frame、Applet

**窗口（Frame）**
import java.awt.Color;
import java.awt.Frame;
 
public class FirstFrame extends Frame{
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		FirstFrame fr = new FirstFrame("Hello"); //构造方法
		fr.setSize(240,240);  //设置Frame的大小
		fr.setBackground(Color.blue); //设置Frame的背景色
		fr.setVisible(true); //设置Frame为可见，默认不可见
	}
	
	public FirstFrame(String str){
		super(str);
	}
 
}

注：awt在实际运行过程中，是调用所在平台的图形系统，底层实现依赖操作系统,为此在Windows平台下运行，则显示Windows风格。

**面板（Panel）** 
    Panel是一种透明的容器，既没有标题，也没有边框。它不能作为最外层的容器单独存在，首先必须先作为一个组件放置在其他容器中，然后在把它当做容器。

import java.awt.Color;
import java.awt.Frame;
import java.awt.Panel;
 
public class FirstFrameDemo {
 
	public static void main(String[] args) {
		// TODO Auto-generated method stub
        Frame fr = new Frame("Hello"); 
        fr.setSize(240,240);
        fr.setBackground(Color.green);
        fr.setLayout(null); //取消默认的布局BorderLayout
        Panel pan = new Panel(); //创建面板
        pan.setSize(100,100);
        pan.setBackground(Color.yellow);
        fr.add(pan);
        fr.setVisible(true);
	}
 
}
#### 布局管理器（LayoutManager）
为了实现跨平台并获得动态的布局效果，java将容器内的所有组件安排给一个“布局管理器”负责管理，如：排列顺序、组件大小、位置、当窗口移动或调整大小后组件变化等功能授权给对应的容器布局管理器来管理。 布局管理器的相关类主要包括：java.awt.FlowLayout、java.awt.BorderLayout、java.awt.GridLayout、java.awt.GradLayout、java.awt.GridBagLayout。
**FlowLayout——流式布局管理器**
    组件从左到右、从上到下，一个挨一个的放在容器中。（Panel和Applet的默认容器布局）如果容器足够宽，第一个组件先添加到容器中第一行的最左边，后续的组件依次添加到上一个组件的右边，如果当前行已放置不下该组件，则放置到下一行的最左边。
```java    
import java.awt.Button;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.Frame;
 
public class FlowLayoutDemo {
 
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Frame frame = new Frame("FlowLayout"); //Frame默认的布局管理器为BorderLayout
        frame.setBounds(100, 100, 400, 300);
        frame.setLayout(new FlowLayout()); //设置布局管理器为FlowLayout
        
        Button but1 = new Button("button1");
        Button but2 = new Button("button2");
        Button but3 = new Button("button3");
        Button but4 = new Button("button4");
        Button but5 = new Button("button5");
        
        but1.setBackground(Color.blue);
        but2.setBackground(Color.yellow);
        but3.setBackground(Color.red);
        but4.setBackground(Color.green);
        but5.setBackground(Color.pink);
        
        frame.add(but1);
        frame.add(but2);
        frame.add(but3);
        frame.add(but4);
        frame.add(but5);
        
        frame.setVisible(true);
	}
 
}
```
FlowLayout的对齐方式默认为居中对齐，但是我们也可以自己指定对齐方式及横纵向间隔。

FlowLayout fl = new FlowLayout();
fl.setAlignment(FlowLayout.LEFT); //设置对齐方式
//也可以直接使用构造函数
//FlowLayout f1 = new FlowLayout(FlowLayout.LEFT,20,40); //三个参数，对齐方式（居左，横向间隔20像素，纵向间隔40像素）
frame.setLayout(fl);
**BorderLayout——边框布局管理器**
按照东、西、南、北、中放组件。（Window/Frame/Dialog的默认容器布局）BorderLayout布局管理器把容器分成5个区域：North，South，East，West和Center，每个区域只能放置一个组件。
```java
import java.awt.BorderLayout;
import java.awt.Button;
import java.awt.Color;
import java.awt.Frame;
 
public class BorderLayoutDemo {
 
	public static void main(String[] args) {
		Frame frame = new Frame("BorderLayt");
        frame.setBounds(100, 100, 400, 300);
        //frame.setLayout(new BorderLayout()); //设置 frame的布局为BorderLayout,默认也是此布局
        
        Button btn1 = new Button("button1");
        Button btn2 = new Button("button2");
        Button btn3 = new Button("button3");
        Button btn4 = new Button("button4");    
        Button btn5 = new Button("button5");
        
        btn1.setBackground(Color.blue);
        btn2.setBackground(Color.yellow);
        btn3.setBackground(Color.pink);
        btn4.setBackground(Color.green);
        btn5.setBackground(Color.red);
        
        frame.add(btn1,BorderLayout.EAST);
        frame.add(btn2,BorderLayout.NORTH);
        frame.add(btn3,BorderLayout.SOUTH);
        frame.add(btn4,BorderLayout.WEST);
        frame.add(btn5);
        
        frame.setVisible(true);
	}
 
}
```
**GridLayout——网格布局管理器**
    使容器中各个组件呈网格状布局，平均占据容器的空间。
```java
import java.awt.Button;
import java.awt.Color;
import java.awt.Frame;
import java.awt.GridLayout;
 
public class GridLayoutDemo {
 
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Frame frame = new Frame("GridLayout");
        frame.setBounds(100, 100, 400, 300);
        
        GridLayout gl = new GridLayout(3,2,5,5); //设置表格为3行两列排列，表格横向间距为5个像素，纵向间距为5个像素
        frame.setLayout(gl);
        
        Button but1 = new Button("button1");
        Button but2 = new Button("button2");
        Button but3 = new Button("button3");
        Button but4 = new Button("button4");
        Button but5 = new Button("button5");
        
        but1.setBackground(Color.blue);
        but2.setBackground(Color.yellow);
        but3.setBackground(Color.red);
        but4.setBackground(Color.green);
        but5.setBackground(Color.pink);
        
        frame.add(but1);
        frame.add(but2);
        frame.add(but3);
        frame.add(but4);
        frame.add(but5);
        
        frame.setVisible(true);
	}
 
}
```
**CardLayout——卡片布局管理器**
```java
import java.awt.BorderLayout;
import java.awt.Button;
import java.awt.CardLayout;
import java.awt.Frame;
import java.awt.Panel;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
 
public class CardLayoutDemo {
	Frame f = new Frame("测试窗口");
	String[] names = { "第一张", "第二张", "第三张", "第四张", "第五张" };
	Panel p1 = new Panel(); //显示的面板
 
	public void init() {
		final CardLayout c = new CardLayout(); //卡片局部
		p1.setLayout(c); //面板布局使用卡片布局
		for (int i = 0; i < names.length; i++) {
			p1.add(names[i], new Button(names[i])); //设置面板的名字和组件
		}
		Panel p = new Panel(); //创建一个放按钮的面板
 
		// 控制显示上一张的按钮
		Button previous = new Button("上一张");
		//为按钮添加监听
		previous.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				c.previous(p1);
			}
		});
 
		// 控制显示下一张的按钮
		Button next = new Button("下一张");
		next.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				c.next(p1);
			}
		});
 
		// 控制显示第一张的按钮
		Button first = new Button("第一张");
		first.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				c.first(p1);
			}
		});
 
		// 控制显示最后一张的按钮
		Button last = new Button("最后一张");
		last.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				c.last(p1);
			}
		});
 
		// 控制根据Card显示的按钮
		Button third = new Button("第三张");
		third.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				c.show(p1, "第三张");
			}
		});
 
		p.add(previous);
		p.add(next);
		p.add(first);
		p.add(last);
		p.add(third);
		f.add(p1);
		f.add(p, BorderLayout.SOUTH);
 
		f.pack(); //紧凑排列
		f.setVisible(true);
	}
 
	public static void main(String[] args) {
		new CardLayoutDemo().init();
	}
 
}
```
**GridBagLayout——网格包布局管理器**
```java
import java.awt.Button;
import java.awt.Frame;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
 
public class GridBagLayoutDemo {
 
	private Frame f = new Frame("GridBagLayout Test");
	private GridBagLayout gbl = new GridBagLayout();
	private GridBagConstraints gbc = new GridBagConstraints();
	
	private Button[] btns = new Button[10];
	
	private void addButton(Button btn) {
		gbl.setConstraints(btn, gbc);
		f.add(btn);
	}
	
	
	public void init() {
		for (int i = 0; i < 10; i++) { // 先初始化10个按钮
			btns[i] = new Button("button" + i);
		}
		f.setLayout(gbl); // 设定框架的布局模式
		
		//为了设置如果组件所在的区域比组件本身要大时的显示情况
		gbc.fill = GridBagConstraints.BOTH; // 使组件完全填满其显示区域
		//NONE：不调整组件大小。
        //HORIZONTAL：加宽组件，使它在水平方向上填满其显示区域，但是不改变高度。
        //VERTICAL：加高组件，使它在垂直方向上填满其显示区域，但是不改变宽度。
		//BOTH：使组件完全填满其显示区域。
		
		gbc.weighty = 1; // 该方法是设置组件水平所占用的格子数，如果为0，就说明该组件是该行的最后一个,为1则只占一格
		
		// 第1行的4个按钮
		gbc.weightx = 1; // 该方法设置组件水平的拉伸幅度，如果为0就说明不拉伸，不为0就随着窗口增大进行拉伸，0到1之间
		addButton(btns[0]);
		addButton(btns[1]);
		addButton(btns[2]);
		gbc.gridwidth = GridBagConstraints.REMAINDER; // 该组件是该行的最后一个，第4个添加后就要换行了
		addButton(btns[3]);
		
		// 第2行1个按钮，仍然保持REMAINDER换行状态
		addButton(btns[4]);
		
		//第3行
		gbc.gridwidth = 2; //按钮分别横跨2格
		gbc.weightx = 1;  //该方法设置组件水平的拉伸幅度
		addButton(btns[5]);
		gbc.gridwidth = GridBagConstraints.REMAINDER;
		addButton(btns[6]);
		
		// 按钮7纵跨2个格子，8、9一上一下
		gbc.gridheight = 2; //按钮7纵跨2格
		gbc.gridwidth = 1;  //横跨1格
		gbc.weightx = 1;    //该方法设置组件水平的拉伸幅度
		addButton(btns[7]); // 由于纵跨2格因此纵向伸缩比例不需要调整，默认为1*2格，比例刚好
		
		gbc.gridwidth = GridBagConstraints.REMAINDER;
		gbc.gridheight = 1;
		gbc.weightx = 1;
		addButton(btns[8]);
		addButton(btns[9]);
		
		f.pack();
		f.setVisible(true);
	}
	
	public static void main(String[] args) {
		new GridBagLayoutDemo().init();
	}
 
 
}
```
#### **组件（Component）**
awt组件库中还有很多比较常用的组件，如：按钮（Button）、复选框（Checkbox）、复选框组（CheckboxGroup）、下拉菜单（Choice）、单行文本输入框（TextField）、多行文本输入框（TextArea）、列表（List）、对话框（Dialog）、文件对话框（Filedialog）、菜单（Menu）、MenuBar、MenuItem、Canvas等；

**基本组件**
```java
import java.awt.Button;
import java.awt.Checkbox;
import java.awt.CheckboxGroup;
import java.awt.Choice;
import java.awt.FlowLayout;
import java.awt.Frame;
import java.awt.GridLayout;
import java.awt.List;
import java.awt.Panel;
import java.awt.TextArea;
import java.awt.TextField;
 
public class ComponentTest {
 
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Frame frame = new Frame("基本组件测试");
        frame.setBounds(100, 100, 600, 300);
        GridLayout gl = new GridLayout(4,2,5,5); //设置表格为3行两列排列，表格横向间距为5个像素，纵向间距为5个像素
        frame.setLayout(gl);
        
        //按钮组件
        Button but1 = new Button("测试按钮");
        Panel pn0 = new Panel();
        pn0.setLayout(new FlowLayout());
        pn0.add(but1);
        frame.add(pn0);
        
        //复选框组件
		Panel pn1 = new Panel();
		pn1.setLayout(new FlowLayout());
		pn1.add(new Checkbox("one",null,true));
		pn1.add(new Checkbox("two"));
		pn1.add(new Checkbox("three"));
		frame.add(pn1);
		
		//复选框组（单选）
		Panel pn2 = new Panel();
		CheckboxGroup cg = new CheckboxGroup();
		pn2.setLayout(new FlowLayout());
		pn2.add(new Checkbox("one",cg,true));
		pn2.add(new Checkbox("two",cg,false));
		pn2.add(new Checkbox("three",cg,false));
		frame.add(pn2);
        
		//下拉菜单
		Choice cC = new Choice();
		cC.add("red");
		cC.add("green");
		cC.add("yellow");
        frame.add(cC);
        
        //单行文本框
  		Panel pn3 = new Panel();
  		pn3.setLayout(new FlowLayout());
        TextField tf = new TextField("",30); //30列长度
        pn3.add(tf);
        frame.add(pn3);
        
        //多行文本框
        TextArea ta = new TextArea();
        frame.add(ta);
        
        //列表
        List ls = new List();
        ls.add("a");
        ls.add("b");
        ls.add("c");
        ls.add("d");
        frame.add(ls);
        frame.setVisible(true);
	}
 
}
```

  

**Menu组件**
```java
import java.awt.Frame;
import java.awt.Menu;
import java.awt.MenuBar;
import java.awt.MenuItem;
 
public class MenuDemo {
 
	private Frame f;
	public MenuDemo(){
		f = new Frame("测试菜单");
		f.setBounds(100, 100, 200, 200);
		//Menu无法直接添加到容器中，只能直接添加到菜单容器中
		MenuBar mb = new MenuBar(); //创建菜单容器
		f.setMenuBar(mb);
		//添加菜单
		Menu m1 = new Menu("File");
		Menu m2 = new Menu("Edit");
		Menu m3 = new Menu("Help");
		mb.add(m1);
		mb.add(m2);
		mb.add(m3);
		
		//添加菜单项
		MenuItem mi1 = new MenuItem("Save");
		MenuItem mi2 = new MenuItem("Load");
		MenuItem mi3 = new MenuItem("Quit");
		m1.add(mi1);
		m1.add(mi2);
		m1.addSeparator(); //添加分隔线
		m1.add(mi3);
		f.setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		MenuDemo md = new MenuDemo();
	}
	
}
```

 

#### 事件
    低级事件：

    1）ComponentEvent 构件事件，构件尺寸的变化以及移动·
    2）ContainerEvent 容器事件，构件增加，移动
    3）WindowEvent 窗口事件，关闭窗口，窗口闭合，图标化
    4）FocusEvent 焦点事件，焦点的获得与丢失
    5）KeyEvent 键盘事件，键按下，释放
    6）MouseEvent 鼠标事件，鼠标点击，移动

    高级事件（语义事件）：

    1）ActionEvent 动作事件，按键按下，TextField中按下Enter键
    2）AdjustmentEvent 调节事件，在滚动条上移动滑块以调节数值
    3）ItemEvent 项目事件，选择项目，不选择“项目改变”
·   4）TextEvent 文本事件，文本对象改变

**事件监听器**
    每类事件都有对应的事件监听器，AWT一共10类事件，11个接口。

事件类别	描述信息	接口名	方法
ActionEvent	激活组件	ActionListener	actionPerformrd(ActionEvent)
ItemEvent	选择了某些项目	ItemListener	itemStateChange(ItemEvent)
MouseEvent	鼠标移动/鼠标点击	
MouseMotionListener/

MouseListener

mouseDragged(MouseEvent)

mouseMoved(MouseEvent)/

mousePressed(MouseEvent)

mouseReleased(MouseEvent)

mouseEntered(MouseEvent)

mouseExited(MouseEvent)

mouseClicked(MouseEvent)

KeyEvent	键盘输入	KeyListener	
keyPressed(KeyEvent )

keyReleased(KeyEvent )

keyTyped(KeyEvent )

FocusEvent	收到或失去焦点	FocusListener	
focusGained(FocusEvent)

focusLost(FocusEvent)

AdjustmentEvent	滚动条上移动滑块以调节数值	AdjustmentListener	adjustmentValueChanged(AdjustmentEvent )
ComponentEvent	对象移动、缩放、显示、隐藏等	ComponentListener	
componentMoved(ComponentEvent )

componentHidden(ComponentEvent )

componentResized(ComponentEvent )

componentShown(ComponentEvent )

WindowEvent	窗口事件	WindowListener	
windowClosing(WindowEvent)

windowOpened(WindowEvent)

windowIconified(WindowEvent)

windowDeiconfied(WindowEvent)

windowClosed(WindowEvent)

windowActived(WindowEvent)

windowDeactivated(WindowEvent)

ContainerEvent	容器中增加或删除组件	ContainerListener	
componentAdded(ContainerEvent )

componentRemoved(ContainerEvent )

TextEvent	文本字段或区域发生变化	TextListener	testValueChanged(TextEvent)
```java
import java.awt.Button;
import java.awt.Color;
import java.awt.Frame;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
 
//使用接口的好处就是支持多继承，而接口中又必须实现父类的抽象方法
public class TestAddListenerDemo implements ActionListener,WindowListener{
 
	Frame f;
	Button b;
	public TestAddListenerDemo(){
		f = new Frame("Add Listener");
		b = new Button("press me");
		b.addActionListener(this);
		f.addWindowListener(this);
		f.add(b,"North");
		f.setSize(200,200);
		f.setVisible(true);
	}
	
	public static void main(String[] args) {
		TestAddListenerDemo ta = new TestAddListenerDemo();
	}
 
	@Override
	public void windowOpened(WindowEvent e) {}
 
	@Override
	public void windowClosing(WindowEvent e) {
		System.exit(1);
	}
 
	@Override
	public void windowClosed(WindowEvent e) {}
 
	@Override
	public void windowIconified(WindowEvent e) {}
 
	@Override
	public void windowDeiconified(WindowEvent e) {}
 
	@Override
	public void windowActivated(WindowEvent e) {}
 
	@Override
	public void windowDeactivated(WindowEvent e) {}
 
	@Override
	public void actionPerformed(ActionEvent e) {
		b.setBackground(Color.blue);
	}
 
}
```
    ActionListener,WindowListener均监听到了相应的操作。

**事件适配器**
java语言为一些Listener接口提供了适配器类。适配器类提供了一些简单的实现或空实现，可以缩短程序代码，有时候我们并不需要实现接口中所有的方法，但是类呢只支持单继承，对于多种监听器就无法采用事件适配器了，而接口支持多继承，则更大程度上给与我们自己发挥的空间。
```java
import java.awt.Button;
import java.awt.Color;
import java.awt.Frame;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
 
public class TestAddListenerDemo2 implements ActionListener{
 
	Frame f;
	Button b;
	public TestAddListenerDemo2(){
		f = new Frame("Add Listener");
		b = new Button("press me");
		b.addActionListener(this);
		f.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				System.exit(1);
			}
		});
		f.add(b,"North");
		f.setSize(200,200);
		f.setVisible(true);
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		TestAddListenerDemo2 ta = new TestAddListenerDemo2();
	}
 
	@Override
	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		b.setBackground(Color.blue);
	}
 
}
```
```java
import java.awt.FileDialog;
import java.awt.Frame;
import java.awt.Menu;
import java.awt.MenuBar;
import java.awt.MenuItem;
import java.awt.TextArea;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
 
public class TextEditor {
 
	private Frame f;
	private TextArea ted;
	public TextEditor(){
		f = new Frame("简单文本编辑器");
		f.setBounds(100, 100, 200, 200);
		//Menu无法直接添加到容器中，只能直接添加到菜单容器中
		MenuBar mb = new MenuBar(); //创建菜单容器
		f.setMenuBar(mb);
		//添加菜单
		Menu m1 = new Menu("File");
		Menu m2 = new Menu("Edit");
		Menu m3 = new Menu("Help");
		mb.add(m1);
		mb.add(m2);
		mb.add(m3);
		
		//添加菜单项
		MenuItem mi1 = new MenuItem("Save");
		MenuItem mi2 = new MenuItem("Load");
		MenuItem mi3 = new MenuItem("Quit");
		m1.add(mi1);
		m1.add(mi2);
		m1.addSeparator(); //添加分隔线
		m1.add(mi3);
		
		ted = new TextArea("",10,10);
		f.add("Center",ted);
		
		f.setVisible(true);
		
		//窗口事件监听-关闭
		f.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e){
				System.exit(1);
			}
		});
		//事件监听:如果直接在当前类上继承或实现监听，则此处使用this
		mi1.addActionListener(new MenuListener());
		mi2.addActionListener(new MenuListener());
		mi3.addActionListener(new MenuListener());
	}
	
	//菜单选项监听器
	class MenuListener implements ActionListener{
 
		@Override
		public void actionPerformed(ActionEvent e) {
			// 操作的组件是谁，就返回谁
			MenuItem i = (MenuItem) e.getSource();
			if("Quit".equals(i.getLabel())){
				System.exit(1);
			}else if("Save".equals(i.getLabel())){
				SaveFile();
			}else if("Load".equals(i.getLabel())){
				loadFile();
			}
		}
		
	}
	
	/**
	 * 保存文件方法
	 */
	void SaveFile(){
		FileDialog fd = new FileDialog(f,"请输入要保存的文件名",FileDialog.SAVE);
		fd.setVisible(true);
		if(fd==null || fd.getFile()==null || "".equals(fd.getFile())){
			return;
		}
		String fileName = fd.getFile();
		String filePath = fd.getDirectory()+fileName;
		try {
			FileOutputStream fos = new FileOutputStream(filePath);
			OutputStreamWriter ows = new OutputStreamWriter(fos);
			ows.write(ted.getText());
			ows.flush();
			ows.close();
			fos.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * 文件读取方法
	 */
	void loadFile(){
		FileDialog fd = new FileDialog(f,"请选择要读取的文件",FileDialog.LOAD);
		fd.setVisible(true);
		if(fd==null || fd.getFile()==null || "".equals(fd.getFile())){
			return;
		}
		ted.setText("");
		String fileName = fd.getFile();
		String filePath = fd.getDirectory()+fileName;
		try {
			BufferedReader in = new BufferedReader(new FileReader(filePath));
			String line = null;
            while ((line = in.readLine()) != null)
            {
               ted.setText(ted.getText() + line+ System.getProperty("line.separator"));
            }
            in.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		new TextEditor();
	}
 
}
```
## SWING 概述
Swing API 是一组可扩展的 GUI 组件，用来创建基于 JAVA 的前端/ GUI 应用程序。它是建立在 AWT API 之上，并且作为 AWT API 的替代者，因为它的几乎每一个控件都对应 AWT 控件。 Swing 组件遵循模型 - 视图 - 控制器架构来满足下面的准则。

#### SWING 控件

|序号	|类 & 描述|
|--------|------|
|Component|Container 是 SWING 的非菜单用户界面控件的一个抽象基类。组件代表一个用图形表示的对象|
|Container|Container 是一个组件，它可以包含其他 SWING 组件。|
|JComponent|JComponent 是一个所有 swing UI 组件的基类。为了使用继承自 JComponent 的一个 swing 组件，组件必须是一个包容层次结构，它的根是一个顶层的 Swing 容器。|
#### **SWING UI 元素:**
下列是当使用 SWING 来设计 GUI 时常用的控件列表。

| No.	|控件 & 描述|
|----------|--------|
|JLabel|JLabel 对象是一个在容器中放置文本的组件。
|JButton|该类创建一个有标签的的按钮。
|JColorChooser|JColorChooser 提供一个控制面板，设计允许用户操作和选择颜色。
|JCheck Box|JCheckBox 是一个图形化的组件，它的状态要么是 on（true）要么是 off（false）。
|JRadioButton|JRadioButton 类是一个图形化的组件，在一个组中，它的状态要么是 on（true）要么是off（false）。
|JList|JList 组件呈现给用户一个滚动的文本项列表。
|JComboBox|JComboBox 组件呈现给用户一个显示菜单的选择。
|JTextField|JTextField 对象是一个文本组件，它允许编辑单行文本。
|JPasswordField|JPasswordField 对象是一个专门用于密码输入的文本组件。
|JTextArea|JTextArea 对象是一个文本组件，它允许编辑多行文本。
|ImageIcon|ImageIcon 控件是一个图标界面的实现，它从图像描绘图标
|JScrollbar|Scrollbar 控件代表一个滚动条组件，为了让用户从值的范围中选择。
|JOptionPaneJOptionPane |提供了一组提示用户输入值的标准对话框，或者通知他们其他东西。
|JFileChooser|JFileChooser 控件代表一个对话框窗口，用户可以从该对话框窗口选择一个文件。
|JProgressBar|随着任务完成的进展，进度条显示任务完成的百分比。
|JSlider|JSlider 让用户在有界区间内通过滑动旋钮图形化地选择一个值。
|JSpinner|JSpinner 是一个单行输入字段，它让用户从一个有序序列中选择一个数字或者一个对象值。
#### SWING 事件类
EventObject 类
它是派生所有事件状态对象的根类。所有事件都是用对象，源的引用来构造的，即逻辑上认为是问题最初发生的事件的对象。这个类定义在 java.util 包中。
类声明
下面是 java.util.EventObject 类的声明：

public class EventObject
   extends Object
      implements Serializable
SWING 事件类：
下面是常用的事件类。

|Sr. No.|	控件 & 描述|
|----------|----------|
|AWTEvent|它是所有 SWING 事件的根事件类。这个类和它的子类取代了最初的 java.awt.Event 类。
|ActionEvent|当单击按钮或双点击列表的项时，生成 ActionEvent。
|InputEvent|InputEvent 类是所有组件层输入事件的根事件类。
|KeyEvent|在按下一个字符时，按键事件生成。
|MouseEvent|这个事件表明一个鼠标动作发生在一个组件中。
|WindowEvent|这个类的对象代表一个窗口状态的变化。
|AdjustmentEvent|这个类的对象代表由可调整的对象发出的调整事件。
|ComponentEvent|这个类的对象代表一个窗口状态的变化。
|ContainerEvent|这个类的对象代表一个窗口状态的变化。
|MouseMotionEvent|这个类的对象代表一个窗口状态的变化。
|PaintEvent|这个类的对象代表一个窗口状态的变化。
#### **SWING 事件监听器**
事件监听器代表负责处理事件的接口。Java 提供了各种事件监听器类，但我们将讨论更频繁使用的那些事件监听器类。一个事件监听器的每个方法有一个参数作为一个对象，该对象是 EventObject 类的子类。例如，鼠标事件监听器的方法将接受 MouseEvent 的实例，其中 MouseEvent 是 EventObject 派生的。

EventListner 接口
它是一个标记接口，每一个监听器接口必须扩展它。这个类定义在 java.util 包中。

类声明
下面是 java.util.EventListener 接口的声明：

public interface EventListener
SWING 事件监听器接口：
下面是常用的事件监听器列表。

|no	|控件 & 描述|
|-------|--------|
|ActionListener|这个接口用于接收动作事件。
|ComponentListener|这个接口用于接收组件事件。
|ItemListener这个接口用于接收项目事件。
|KeyListener|这个接口用于接收按键事件。
|MouseListener|这个接口用于接收鼠标事件。
|WindowListener|这个接口用于接收窗口事件。
|AdjustmentListener|这个接口用于接收调整事件。
|ContainerListener|这个接口用于接收容器事件。
|MouseMotionListener|这个接口用于接收鼠标移动事件。
|FocusListener|这个接口用于接收焦点事件。
#### SWING 事件适配器
适配器是用于接收各种事件的抽象类。这些类中的方法是空的。这些类的存在是为了方便创建监听器对象。


|Sr. No.|	适配器 & 描述|
|-----------|-------|
|FocusAdapter|用于接收焦点事件的抽象适配器类。
|KeyAdapter|用于接收按键事件的抽象适配器类。
|MouseAdapter|用于接收鼠标事件的抽象适配器类。
|MouseMotionAdapter|用于接收鼠标移动事件的抽象适配器类。
|WindowAdapter|用于接收窗口事件的抽象适配器类。
#### SWING 菜单类
正如我们所知道每个顶层窗口有一个菜单栏与它相关联。这个菜单栏包括各种菜单可用的选择给最终用户。而且每个选择包含被称为下拉菜单的选项列表。菜单和菜单项的控件都是 MenuComponent 类的子类。

|Sr. No.|	控件 & 描述|
|----------------------|--------------------|
|JMenuBar|JMenuBar 对象是与顶层窗口相关联的
|JMenuItem|菜单中的项目必须属于 JMenuItem 或任何它的子类。
|JMenu|JMenu 对象是从菜单栏中显示的一个下拉菜单组件。
|JCheckBoxMenuItem|JCheckBoxMenuItem 是 JMenuItem 的子类。
|JRadioButtonMenuItem|RadioButtonMenuItem 是 JMenuItem 的子类。
|JPopupMenu|JPopupMenu 可以在一个组件内的指定位置动态地弹出。
