<<<<<<< HEAD
# phantomCL公式计算器_v1.1
=======
# phantomCL公式计算器_v1.0
>>>>>>> e1bd347dc6b1abee98b21939c290d990ec691e33

此项目基于`sympy`和`tkinter`开发，提供一个用户界面，在设置符号变量、生成LaTeX计算式后，可以进行数值运算以及保存结果，并支持从Excel文件中导入数据进行批量运算。

## 关于

是新手！借鉴了多个科学计算库，只花了一天时间构建，代码有很多优化空间，可以实现数值运算~~（也可以进行符号运算，只是我懒没有写）~~，后续会更新符号运算、矩阵运算、解方程和微积分等功能（大概）。

因为Rosmontis太可爱了因此用她做图标，如果该项目图片侵权请联系我删除！

QQ：1269035311

## 声明

此项目仅用于学习交流，请勿用于非法途径。



## 兼容性问题

windows可能因为屏幕分辨率问题导致窗口无法正常显示，字体过小。

请在安装目录，右击应用程序`phantomCL.exe`，选择**属性**——**兼容性**——**更改高DPI设置**——**替代高DPI缩放行为**，再次运行即可。

![](https://www.shelven.com/tuchuang/hp/111.jpg)



## 使用手册

请按照用户界面**步骤1**，**步骤2**，**步骤3**的顺序依次操作。

### 步骤1. 设置变量

仅需设置计算式**右边部分**的变量，输入变量个数后点击**确定**，按照提示设置计算式的变量名称。

以下变量名**无法**设置成功：

- 单个大写字母
- `for, in, as, try, except, if, else, return`等python关键字
- 数字开头的变量

成功设置变量后，会在步骤1下方出现设置的变量数和变量名，同时在右边的输出结果中会生成表头

![1](https://www.shelven.com/tuchuang/hp/hp1.jpg)

### 步骤2. 设置计算式

在输入框中输入计算式，点击右下方**生成计算式**按钮，生成**化简后**的的LaTeX表达式。

**注意**：只有生成计算式后才可以进行下一步运算操作，**不要加入等号**！

提供4个常数和运算符按钮：

 - 自然数e：`exp(1)`  括号内表示自然数的几次方
 - 圆周率Π：`pi`
 - 开根号√：`sqrt()`括号内为根号下的内容
 - 取对数log：`log(x)`表示ln(x)，`log(x,10)`表示log10(x)

 当然，对于三角函数`sin(), cos(), tan()`和绝对值函数`abs()`等常见的函数也都支持

![hp2](https://www.shelven.com/tuchuang/hp/hp2.jpg)

### 步骤3. 传值运算

#### 简单运算

点击按钮，输入对应的变量值。运算结果在右侧输出框自动输出。

#### 批量运算

点击按钮，传入**xlsx格式的Excel文件**（目前仅支持Excel），自动校验创建的变量名在Excel文件中是否存在，若存在则传入数值进行运算。运算结果在右侧输出框自动输出。

Excel文件要求如下：

- 第一步创建的变量名必须要在第一行出现（顺序不要求）
- Excel文件的变量名可以更多，但不能少于创建的变量名，重名的变量只取第一个

- 每个变量待传入的数值必须一样多
- 数值部分不允许出现其他字符

示例数据：

![hp3](https://www.shelven.com/tuchuang/hp/hp3.jpg)

传入后根据计算式自动运算：

![hp4](https://www.shelven.com/tuchuang/hp/hp4.jpg)

#### 保存结果

对输出结果框进行保存，默认`xls`格式，可以使用Excel打开。

#### 清空窗口

清空输出结果框（仅保留表头）和运行日志。



## 更新

**2024/4/13**

- 修复分辨率和缩放比例会导致窗口显示不完整的问题

**2024/4/12**

- `pyinstaller`打包，`NSIS`制作安装包

**2024/4/11**

- 修复清空窗口导致的输出结果错位
- 修复提示框未正常销毁导致的按钮失效bug，删除`Tooltip`类
- 修复`pyplot`强制更改`tkinter`窗口分辨率bug

**2024/4/10**

- 构建UI和功能函数
<<<<<<< HEAD

=======
>>>>>>> e1bd347dc6b1abee98b21939c290d990ec691e33
