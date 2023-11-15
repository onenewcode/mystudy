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



# Stream
##  介绍
Java Stream 的主要作用有以下几个方面：

- 简化集合操作：使用传统的 for 循环或迭代器来处理集合数据可能会导致冗长而复杂的代码。
- 延迟计算：流式操作允许你在处理数据之前定义一系列的操作步骤，但只在需要结果时才会实际执行。这种延迟计算的特性意味着可以根据需要动态调整数据处理的操作流程，提升效率。
- 并行处理：Java Stream 提供了并行流的支持，可以将数据分成多个块进行并行处理，从而充分利用多核处理器的性能优势，提高代码的执行速度。
- 函数式编程风格：流式编程鼓励使用函数式编程的思想，通过传递函数作为参数或使用 Lambda 表达式来实现代码的简化和灵活性。

**为什么使用流式编程可以提高代码可读性和简洁性**
- 声明式编程风格：流式编程采用了一种声明式的编程风格，你只需描述你想要对数据执行的操作，而不需要显式地编写迭代和控制流语句。

- 链式调用：流式编程使用方法链式调用的方式，将多个操作链接在一起。每个方法都返回一个新的流对象，这样你可以像“流水线”一样在代码中顺序地写下各种操作，使代码逻辑清晰明了。

- 操作的组合：流式编程提供了一系列的操作方法，如过滤、映射、排序、聚合等，这些方法可以按照需要进行组合使用。你可以根据具体的业务需求将这些操作串联起来，形成一个复杂的处理流程，而不需要编写大量的循环和条件语句。

- 减少中间状态：传统的迭代方式通常需要引入中间变量来保存中间结果，这样会增加代码的复杂度和维护成本。而流式编程将多个操作链接在一起，通过流对象本身来传递数据，避免了中间状态的引入。

- 减少循环和条件：流式编程可以替代传统的循环和条件语句的使用。

### 什么是 Stream？
Stream（流）是一个来自数据源的元素队列并支持聚合操作
- 元素是特定类型的对象，形成一个队列。 Java中的Stream并不会存储元素，而是按需计算。
- 数据源 流的来源。 可以是集合，数组，I/O channel， 产生器generator 等。
- 聚合操作 类似SQL语句一样的操作， 比如filter, map, reduce, find, match, sorted等。
- 不可变性：Stream 是不可变的，它不会修改原始数据源，也不会产生中间状态或副作用。每个操作都会返回一个新的流对象，以保证数据的不可变性。
和以前的Collection操作不同， Stream操作还有两个基础的特征：
- Pipelining: 中间操作都会返回流对象本身。 这样多个操作可以串联成一个管道， 如同流式风格（fluent style）。 这样做可以对操作进行优化， 比如延迟执行(laziness)和短路( short-circuiting)。
- 内部迭代： 以前对集合遍历都是通过Iterator或者For-Each的方式, 显式的在集合外部进行迭代， 这叫做外部迭代。 Stream提供了内部迭代的方式， 通过访问者模式(Visitor)实现。

**Stream中的操作大体可以分为两类**
- **中间操作**：将流一层层的进行处理，并向下一层进行传递，如 filter map sorted等。
中间操作又分为有状态(stateful)及无状态(stateless)
	- 有状态：必须等上一步操作完拿到全部元素后才可操作，如sorted
	- 无状态：该操作的数据不收上一步操作的影响，如filter map
- **终止操作**：触发数据的流动，并收集结果，如collect findFirst forEach等。终止操作又分为短路操作(short-circuiting)及非短路操作(non-short-circuiting)
	- 短路操作：会在适当的时刻终止遍历，类似于break，如anyMatch findFirst等
	- 非短路操作：会遍历所有元素，如collect max等
## Stream中间操作

### 过滤操作（filter）
过滤操作（filter），它接受一个 Predicate 函数作为参数，用于过滤 Stream 中的元素。只有满足 Predicate 条件的元素会被保留下来，而不满足条件的元素将被过滤掉。

过滤操作的语法如下
```java
Stream<T> filter(Predicate<? super T> predicate)
```

其中，T 表示 Stream 元素的类型，predicate 是一个函数式接口 Predicate 的实例，它的泛型参数和 Stream 元素类型一致,并且predicate返回的值必须是boolean类型，因为需要通过真假值判断是否要过滤该值。

使用过滤操作可以根据自定义的条件来筛选出符合要求的元素，从而对 Stream 进行精确的数据过滤。

下面是一个示例，演示如何使用过滤操作筛选出一个整数流中的大于三的数：
```java
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
//        生成流式对象
//        Stream<Integer> stream = numbers.stream();
        List<Integer> list=numbers.stream().filter(
                (x)->{return x>3;}  //lambda表达式 可简化成下面的写法
//                x->x>3
        ).toList();
        System.out.println("number中大于3的数: "+list.toString());

```




### 映射操作（map）
映射操作（map），它接受一个 Function 函数作为参数，用于对 Stream 中的每个元素进行映射转换，生成一个新的 Stream。

映射操作的语法如下：
```java
<R> Stream<R> map(Function<? super T, ? extends R> mapper)
```

其中，T 表示原始 Stream 的元素类型，R 表示映射后的 Stream 的元素类型，mapper 是一个函数式接口 Function 的实例，可以进行不同的映射操作.



下面是一个示例，演示如何使用映射操作将一个字符串流中的每个字符串转换为其长度：
```java
        List<String> numbers = Arrays.asList("apple", "banana", "cherry");
//        生成流式对象
//        Stream<Integer> stream = numbers.stream();
        numbers.stream().map(
                String::length
        ).forEach(System.out::println);
```
在这个示例中，我们首先创建了一个包含字符串的 Stream，并调用 map() 方法传入String::length，表示要将每个字符串转换为其长度。然后通过 forEach() 方法遍历输出结果。


**注意**: 映射操作可能引发空指针异常（NullPointerException），因此在执行映射操作时，应确保原始 Stream 中不包含空值，并根据具体情况进行空值处理。

### 排序操作（sorted）

排序操作（sorted）是 Stream API 中的一种常用操作方法，它用于对 Stream 中的元素进行排序。排序操作可以按照自然顺序或者使用自定义的比较器进行排序。

排序操作的语法如下：
```java
Stream<T> sorted() Stream<T> sorted(Comparator<? super T> comparator)
```

- **第一种**语法形式中，sorted() 方法会根据元素的自然顺序进行排序。如果元素实现了 Comparable 接口并且具备自然顺序，那么可以直接调用该方法进行排序。

- **第二种**语法形式中，sorted(Comparator<? super T> comparator) 方法接受一个比较器（Comparator）作为参数，用于指定元素的排序规则。通过自定义比较器，可以对非 Comparable 类型的对象进行排序。

下面是一个示例，演示如何使用排序操作对一个字符串流进行排序：
```java
        List<String> numbers = Arrays.asList("apple", "banana", "cherry");
//        生成流式对象
//        Stream<Integer> stream = numbers.stream();
        numbers.stream().sorted().forEach(System.out::println);

```
输出
```shell
apple
banana
cherry
```
**注意**: 排序操作可能会影响程序的性能，特别是对于大型数据流或者复杂的排序规则。因此，在实际应用中，需要根据具体情况进行权衡和优化，选择合适的算法和数据结构来提高排序的效率。

### 截断操作（limit 和 skip）
截断操作（limit和skip），用于在处理流的过程中对元素进行截断。

1. limit(n)：保留流中的前n个元素，返回一个包含最多n个元素的新流。如果流中元素少于n个，则返回原始流。
2. skip(n)：跳过流中的前n个元素，返回一个包含剩余元素的新流。如果流中元素少于n个，则返回一个空流。
下面分别详细介绍这两个方法的使用。


**注意**: 在使用截断操作时需要注意流的有界性。如果流是无界的（例如 Stream.generate()），那么使用 limit() 方法可能导致程序陷入无限循环，而使用 skip() 方法则没有意义。

## Stream 的终止操作
### forEach 和 peek
forEach和peek都是Stream API中用于遍历流中元素的操作方法，它们在处理流的过程中提供了不同的功能和使用场景。

**forEach**： forEach是一个终端操作方法，它接受一个Consumer函数作为参数，对流中的每个元素执行该函数。forEach会遍历整个流，对每个元素执行相同的操作。

示例代码：
```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
names.stream()
     .forEach(System.out::println);
```

**peek**： peek是一个中间操作方法，它接受一个Consumer函数作为参数，对流中的每个元素执行该函数。与forEach不同的是，peek方法会返回一个新的流，该流中的元素和原始流中的元素相同。

示例代码：
```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
List<String> upperCaseNames = names.stream()
                                   .map(String::toUpperCase)
                                   .peek(System.out::println)
                                   .toList();
```



### 聚合操作（reduce）
reduce和collect都是Stream API中用于聚合操作的方法，它们可以将流中的元素进行汇总、计算和收集。

**reduce**： reduce是一个终端操作方法，它接受一个BinaryOperator函数作为参数，对流中的元素逐个进行合并操作，最终得到一个结果。该方法会将流中的第一个元素作为初始值，然后将初始值与下一个元素传递给BinaryOperator函数进行计算，得到的结果再与下一个元素进行计算，以此类推，直到遍历完所有元素。

示例代码：
```java
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        numbers.stream().reduce(Integer::sum).ifPresent(System.out::println);//输出结果15
```

在这个示例中，我们创建了一个包含整数的List，并通过stream()方法将其转换为流。然后使用reduce方法对流中的元素进行求和操作，将每个元素依次相加，得到结果15。



### 匹配操作（allMatch、anyMatch 和 noneMatch）
在 Stream API 中，allMatch、anyMatch 和 noneMatch 是用于进行匹配操作的方法，它们可以用来检查流中的元素是否满足特定的条件。

**allMatch**： allMatch 方法用于判断流中的所有元素是否都满足给定的条件。当流中的所有元素都满足条件时，返回 true；如果存在一个元素不满足条件，则返回 false。




**anyMatch**： anyMatch 方法用于判断流中是否存在至少一个元素满足给定的条件。当流中至少有一个元素满足条件时，返回 true；如果没有元素满足条件，则返回 false。



在这个示例中，我们创建了一个包含整数的 List，并通过 stream() 方法将其转换为流。然后使用 anyMatch 方法判断流中是否存在偶数。由于列表中存在偶数，所以返回 true。

***noneMatch***： noneMatch 方法用于判断流中的所有元素是否都不满足给定的条件。当流中没有元素满足条件时，返回 true；如果存在一个元素满足条件，则返回 false。

示例代码：
```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
boolean allEven = numbers.stream()
                         .allMatch(n -> n % 2 == 0);
System.out.println(allEven); // 输出结果: false
boolean hasEven = numbers.stream()
                         .anyMatch(n -> n % 2 == 0);
System.out.println(hasEven); // 输出结果: true
boolean noneNegative = numbers.stream()
                             .noneMatch(n -> n < 0);
System.out.println(noneNegative); // 输出结果: true

```

### 查找操作（findFirst 和 findAny）
在 Stream API 中，findFirst 和 findAny 是用于查找操作的方法，它们可以用来从流中获取满足特定条件的元素。

**findFirst**： findFirst 方法用于返回流中的第一个元素。它返回一个 Optional 对象，如果流为空，则返回一个空的 Optional；如果流非空，则返回流中的第一个元素的 Optional。

**findAny**： findAny 方法用于返回流中的任意一个元素。它返回一个 Optional 对象，如果流为空，则返回一个空的 Optional；如果流非空，则返回流中的任意一个元素的 Optional。在顺序流中，通常会返回第一个元素；而在并行流中，由于多线程的处理，可能返回不同的元素。

**示例代码**：
```java

List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
Optional<String> first = names.stream()
                              .findFirst();
first.ifPresent(System.out::println); // 输出结果: Alice

List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
Optional<Integer> any = numbers.stream()
                               .filter(n -> n % 2 == 0)
                               .findAny();
any.ifPresent(System.out::println); // 输出结果: 2 或 4（取决于并行处理的结果）
```



### 统计操作（count、max 和 min）
在 Stream API 中，count、max 和 min 是用于统计操作的方法，它们可以用来获取流中元素的数量、最大值和最小值。

**count**： count 方法用于返回流中元素的数量。它返回一个 long 类型的值，表示流中的元素个数。


**max**： max 方法用于返回流中的最大值。





**min**： min 方法用于返回流中的最小值。它返回一个 Optional 对象，如果流为空，则返回一个空的 Optional；如果流非空，则返回流中的最小值的 Optional。

**示例代码**：
```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
long count = numbers.stream()
                    .count();
System.out.println(count); // 输出结果: 5

Optional<Integer> max = numbers.stream()
                               .max(Integer::compareTo);
max.ifPresent(System.out::println); // 输出结果: 5

Optional<Integer> min = numbers.stream()
                               .min(Integer::compareTo);
min.ifPresent(System.out::println); // 输出结果: 1
```

# Java Lambda 表达式
Lambda 表达式，也可称为闭包.
Lambda 允许把函数作为一个方法的参数（函数作为参数传递进方法中）。

**Lambda表达式的主要特点包括**：
- **匿名性**：Lambda表达式没有显式的名称，因此可以被当做一种匿名函数使用。
- **简洁性**：Lambda表达式可以大大减少代码的冗余，使代码更加简洁。
- **传递性**：Lambda表达式可以作为参数传递给方法，从而实现更灵活的代码组织。

## 语法
lambda 表达式的语法格式如下：
```java
(parameters) -> expression
或
(parameters) ->{ statements; }
```

**以下是lambda表达式的重要特征**:
- **可选类型声明**：不需要声明参数类型，编译器可以统一识别参数值。
- **可选的参数圆括号**：一个参数无需定义圆括号，但多个参数需要定义圆括号。
- **可选的大括号**：如果主体包含了一个语句，就不需要使用大括号。
- **可选的返回关键字**：如果主体只有一个表达式返回值则编译器会自动返回值，大括号需要指定表达式返回了一个数值。

**使用 Lambda 表达式需要注意以下两点**：
- Lambda 表达式主要用来定义行内执行的方法类型接口（例如，一个简单方法接口）。在上面例子中，我们使用各种类型的 Lambda 表达式来定义 MathOperation 接口的方法，然后我们定义了 operation 的执行。

- Lambda 表达式免去了使用匿名方法的麻烦，并且给予 Java 简单但是强大的函数化的编程能力。

## Lambda 表达式实例
Lambda 表达式的简单例子:
```java
// 1. 不需要参数,返回值为 5  
() -> 5  
  
// 2. 接收一个参数(数字类型),返回其2倍的值  
x -> 2 * x  
  
// 3. 接受2个参数(数字),并返回他们的差值  
(x, y) -> x – y  
  
// 4. 接收2个int型整数,返回他们的和  
(int x, int y) -> x + y  
  
// 5. 接受一个 string 对象,并在控制台打印,不返回任何值(看起来像是返回void)  
(String s) -> System.out.print(s)
```

## Lambda表达式与函数式接口
Lambda表达式通常与函数式接口（Functional Interface）一起使用。函数式接口是一个只包含一个抽象方法的接口。Lambda表达式可以使用这个抽象方法的签名来实现该接口，从而简化代码。

例如，Java标准库中的java.lang.Runnable就是一个函数式接口，它只包含一个void run()方法。我们可以使用Lambda表达式来创建Runnable对象：
```java
Arrays.sort(arrays,
	(first,second)->first.length()-second.length());
```
## 方法引用
方法引用：使用操作符::将方法名和对象或类的名字分隔开来，三种主要使用情况为：
- 对象::实例方法
- 类::静态方法
- 类::实例方法
```java
// 实例方法引用
list.forEach(e->{System.out.println(e);});
list.forEach(System.out::println);

// 静态方法
list.stream().reduce(Math::max);

// 实例方法
people=stream.toArray(Person[]::new);
```
## 处理lambda表达式的接口

|函数式接口|参数类型|返回类型|抽象方法名|描述|其他方法|
|--------|----------|----------|--------|-------|---------|
|Runnable|无|void|run|作为无参数或返回值的动作执行||
|Supplier&lt;T>|无|T|get|提供一个T类型的值||
|Consumer&lt;T>|T|void|accept|处理一个T类型的值|addThen|
|BiConsumer&lt;T,U>|T,U|void|accept|处理T和U类型的值|addThen|
|Function&lt;T,R>|T|R|apply|有一个T类型参数的函数|compose,addThen,idenity|
|BiFunction<T,U,R>|T,U|R|apply|有T和U类型参数的函数|addThen|
|UnaryOperator&lt;T>|T|T|apply|类型T上的一元操作符|compose,addThen,identity|
|BinaryOperator&lt;T>|T,T|T|apply|类型T上的二元操作符|addThen,maxBy,minBy|
|PreDicate&lt;T>|T|boolean|test|布尔值函数|add,or,negate,isEqual|
|BiPredicate|T,U|boolean|test|有两个参数的布尔值函数|add,or,negate|

