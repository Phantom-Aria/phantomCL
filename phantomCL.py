import tkinter as tk
import sympy as sp
from tkinter import messagebox, filedialog, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkinter.scrolledtext import ScrolledText
import keyword
import time
import pandas as pd

root = tk.Tk()
root.title('phantomCL公式计算器v1.1')
root.resizable(0,0)

# 创建一个Tooltip类，接受一个widget和提示文本作为参数，暂时有bug，待修复
# class Tooltip:
#     def __init__(self, widget, text):
#         self.widget = widget
#         self.text = text
#         self.tooltip = None
#         self.enter_id = None
#         self.leave_id = None
#         self.widget.bind("<Enter>", self.delayed_show_tooltip)
#         self.widget.bind("<Leave>", self.hide_tooltip)

#     def delayed_show_tooltip(self, event):
#         self.enter_id = self.widget.after(500, self.show_tooltip)

#     def show_tooltip(self):
#         if self.enter_id:
#             self.widget.after_cancel(self.enter_id)
#             self.enter_id = None

#         x, y, cx, cy = self.widget.bbox("insert")
#         x += self.widget.winfo_rootx() + 25
#         y += self.widget.winfo_rooty() + 20

#         self.tooltip = tk.Toplevel(self.widget)
#         self.tooltip.wm_overrideredirect(True)
#         self.tooltip.wm_geometry("+%d+%d" % (x, y))

#         label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
#         label.pack(ipadx=1)

#     def hide_tooltip(self, event):
#         if self.enter_id:
#             self.widget.after_cancel(self.enter_id)
#             self.enter_id = None

#         if self.tooltip:
#             self.tooltip.destroy()

# 限制变量命名规则
def is_valid_variable_name(var_name):
    return var_name.isidentifier() and not keyword.iskeyword(var_name) and not var_name[0].isdigit() and not (len(var_name) == 1 and var_name.isupper())

# 变量名获取
def get_user_input():
    global var_list
    var_list = []
    try:
        num_times = int(var_number.get())
        if num_times <= 0:
            messagebox.showerror("错误", f"请输入大于0的整数哦(´・ω・`) ")
            write_log("ERROR:请指定整数个变量名")
        for i in range(num_times):
            root.update() # 强制刷新主窗口，使弹窗显示主窗口之上
            var_name = tk.simpledialog.askstring("变量名", f"请输入第{i+1}个变量名，不可以单个大写字母(´・ω・`):").strip()
            while var_name is not None and (not is_valid_variable_name(var_name)):
                root.update()
                var_name = tk.simpledialog.askstring("变量名", "请输入有效的变量名......\n不能是Python关键字\n不能以数字开头\n不能是单个大写字母\n咱也没办法，要符合python命名规范(´・ω・`):")
            if var_name is not None:
                var_list.append(var_name)
            else:
                break
        # 列举变量名，输出结果显示表头
        res_datatext.delete('1.0', tk.END)
        i = len(var_list)
        res_label = f'成功创建{i}个变量，变量名为 '
        var_string = ''
        for idx, var in enumerate(var_list):
            res_label += var
            var_string += var
            if idx < len(var_list) - 1:
                res_label += ', '
                var_string +='\t'
        result_label.config(text=res_label)
        var_string += '\t计算结果\n'
        res_datatext.insert(tk.END, var_string)
        formula_entry.focus_set()  # 鼠标聚焦到计算式输入框
        write_log("INFO:变量设置成功！请生成计算式")
    except ValueError as e:
        messagebox.showerror("错误", f"请输入大于0的整数哦(´・ω・`) ")
        write_log("ERROR:请重新设置变量")

# 计算式输出
def generate_formula():
    global expr, latex_formula
    try:
        formula = formula_entry.get()
        expr = sp.sympify(formula)  # 字符串转化表达式
        variable = expr.free_symbols
        symbols_as_strings = {str(symbol) for symbol in variable}
        # 判断计算式中的变量与获取的变量名是否相同
        if set(var_list) == symbols_as_strings:
            latex_formula = sp.latex(expr) # 表达式转化LaTeX公式字符串
            ax.clear()  # 清除旧的图形，渲染新的表达式图形
            ax.text(0.5, 0.5, r'$ %s $' % latex_formula, ha='center', va='center', fontsize=20)
            ax.axis('off')
            canvas.draw()  # 更新canvas上的图形
            write_log("INFO:计算式生成！请选择运算模式")
        else:
            messagebox.showerror("错误", f"计算式中的变量和第一步输入的变量不一致，请检查(´・ω・`) ")
            write_log("ERROR:请重新输入计算式")
    except Exception as e:
        messagebox.showerror("错误", f"无法解析计算式，请不要加入等号，检查是否缺少运算符(´・ω・`) ")
        write_log("ERROR:请重新输入计算式")

# 定义简单运算
def simple_calculate():
    global expr
    try:
        run_time = len(var_list)
        var_string = ''
        res_expr = expr
        for i in range(run_time):
            root.update()
            var_name = var_list[i]
            var_value = float(tk.simpledialog.askstring("值", f"请输入{var_name}变量值(´・ω・`):").strip())
            var_string = var_string + str(var_value) + '\t'
            res_expr = res_expr.subs(var_name, var_value).evalf()
        var_string += f'{res_expr}\n'
        res_datatext.insert(tk.END, var_string)
        write_log("INFO:简单运算完成！")
    except:
        messagebox.showerror("错误", f"请生成计算式后传值(´・ω・`) ")
        write_log("ERROR:请生成计算式后再运算")

# 定义批量运算
def batch_calculate():
    global expr
    try:
        input_file = filedialog.askopenfilename(title="选择文件", filetypes=[("Excel文件", "*.xlsx")])
        df = pd.read_excel(input_file)
        column_names_list = df.columns.tolist()
    except:
        messagebox.showerror("错误", f"文件无法读入，可能不是标准的excel文件(´・ω・`) ")
        write_log("ERROR:文件读取失败")
        return
    # 创建字典，检查数据是否都存在，并储存
    data_dict = {}
    length_dict = {}

    for var in var_list:
        column_name = var
        if var not in column_names_list:
            messagebox.showerror("错误", f"Excel文件的列 '{column_name}' 不存在，请检查(´・ω・`) ")
            write_log(f"ERROR:列 {column_name} 不存在")
            return
        numeric_data = pd.to_numeric(df[column_name], errors='coerce')
        if numeric_data.isnull().values.any():
            messagebox.showerror("错误", f"变量数目不一致或者有数字外的其他内容(´・ω・`) ")
            write_log(f"ERROR:变量数据不规范")
            return
        else:
            data_dict[var] = df[column_name].tolist()
            length_dict[var] = len(data_dict[var])

    # 校验存储的键长度是否一致，集合会去重
    lengths = list(length_dict.values())
    if len(set(lengths)) == 1:
        pairs = lengths[0]
        write_log(f"INFO:读取数据完成！一共有{pairs}组数据，开始运算......")
        try:
            runtime = len(var_list)
            for i in range(pairs):
                var_string = '' # 初始化
                res_expr = expr # 初始化
                for j in range(runtime):
                    var_name = var_list[j]
                    var_value = data_dict[var_name][i]
                    var_string = var_string + str(var_value) + '\t'
                    res_expr = res_expr.subs(var_name, var_value).evalf()
                var_string += f'{res_expr}\n'
                res_datatext.insert(tk.END, var_string)
            write_log("INFO:批量运算完成！")
        except:
            messagebox.showerror("错误", f"嗯？计算出错了，请联系作者解决(´・ω・`) ")
            write_log("ERROR:未知错误，请联系作者")
        
    else:
        messagebox.showerror("错误", f"出错了，导入的变量间数目不同哦(´・ω・`) ")
        write_log("ERROR:校验错误，请检查数据")

# 日志打印功能
def write_log(logmsg):
    current_time =time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    logmsg_in = str(current_time) + '\n' + str(logmsg) + '\n\n'
    log_text.insert("1.0", logmsg_in)

# 导出结果文件
def export_file():
    content = res_datatext.get('1.0', tk.END)
    if '结果' not in content:
        messagebox.showerror("错误", f"没有结果就无法保存哦(´・ω・`) ")
        write_log("ERROR:请生成运算结果后再保存")
    else:
        try:
            result_file = filedialog.asksaveasfilename()
            result_file = result_file + '.xls'
            with open(result_file, 'w') as f:
                f.write(f'LaTeX表达式\t{latex_formula}\n{content}')
                write_log("INFO:结果已保存！保存路径: %s" % (result_file))
        except:
            write_log('ERROR:导出失败，请检查是否有同名文件未关闭')

# 清除窗口
def clear_window():
    try:
        res_data = res_datatext.get('1.0', tk.END)
        first_newline_index = res_data.find('\n')
        if first_newline_index != -1:
            res_datatext.delete("1.0 + {} chars".format(first_newline_index + 1), tk.END)
            res_datatext.insert(tk.END, '\n')
        log_text.delete('1.0', tk.END)
    except:
        messagebox.showerror("错误", f"没有需要清除的输出内容和日志哦(´・ω・`) ")

def _quit():
    root.quit()
    root.destroy() 

root.protocol("WM_DELETE_WINDOW", _quit)

## 整体布局
left_flame = tk.Frame(root)
left_flame.pack(side='left', expand=True, fill=tk.BOTH)
right_flame = tk.Frame(root)
right_flame.pack(side='left', expand=True, fill=tk.BOTH)

### 步骤1
first_frame = tk.LabelFrame(left_flame, text="步骤1：设置变量")
first_frame.pack(pady=20, padx=10, fill=tk.BOTH)
frame_1 = tk.Frame(first_frame)
frame_1.pack(pady=10)
var_label = tk.Label(frame_1, text="请输入计算式的变量数目：")
var_label.pack(side='left')
var_number = tk.Entry(frame_1, width=10)
var_number.pack(side='left')
#var_number.focus_set()  # 打开程序时的鼠标聚焦
var_button = tk.Button(frame_1, text='确定', command=get_user_input)
var_button.pack(side='left', padx=10)
frame_2 = tk.Frame(first_frame)
frame_2.pack()
result_label = tk.Label(frame_2, text="请先输入待计算的变量数目和名称")
result_label.pack(padx=10, pady=20)

### 步骤2
second_frame = tk.LabelFrame(left_flame, text="步骤2：设置计算式")
second_frame.pack(pady=20,padx=10,expand=True,fill=tk.BOTH)
# 初始化matplotlib图形
fig, ax = plt.subplots(figsize=(5, 1))
ax.axis('off')
# 创建canvas并添加到result_frame中
canvas = FigureCanvasTkAgg(fig, master=second_frame)
result_frame = tk.Frame(second_frame)
result_frame.pack(pady=10,padx=10)
formula_label = tk.Label(second_frame, text="生成的计算式")
formula_label.pack(pady=5)
canvas.get_tk_widget().pack(padx=10)
frame_3 = tk.Frame(second_frame)
frame_3.pack(ipady=10)
generate_label = tk.Label(frame_3, text="输入计算式：")
generate_label.pack(side='left', pady=20)
formula_entry = tk.Entry(frame_3, width=50)
formula_entry.pack(side='left', pady=20)
formula_entry.bind("<Return>", generate_formula)
frame_4 = tk.Frame(second_frame)
frame_4.pack(pady=20)
exp_button = tk.Button(frame_4, text='自然数e', command=lambda: formula_entry.insert(tk.END, "exp(1)"))
pi_button = tk.Button(frame_4, text='圆周率Π', command=lambda: formula_entry.insert(tk.END, "pi"))
sqrt_button = tk.Button(frame_4, text='开根号√', command=lambda: formula_entry.insert(tk.END, "sqrt()"))
log_button = tk.Button(frame_4, text='取对数log', command=lambda: formula_entry.insert(tk.END, "log()"))
exp_button.pack(side="left", padx=10)
pi_button.pack(side="left", padx=10)
sqrt_button.pack(side="left", padx=10)
log_button.pack(side="left", padx=10)

# tooltip = Tooltip(exp_button, "用exp(1)函数表示，括号内数字代表几次方")
# tooltip = Tooltip(pi_button, "用pi表示，变量名不可用pi")
# tooltip = Tooltip(sqrt_button, "用sqrt()函数表示")
# tooltip = Tooltip(log_button, "log(x)表示ln(x)，log(x, 10)表示log10(x)")

generate_button = tk.Button(frame_4,borderwidth=5, text='生成计算式', command=generate_formula)
generate_button.pack(side="left",pady=10,padx=20)


### 步骤3
third_frame = tk.LabelFrame(left_flame, text="步骤3：传值运算")
third_frame.pack(pady=20,fill=tk.BOTH,padx=10)
frame_5 = tk.Frame(third_frame)
frame_5.pack(anchor="w",pady=10)
simple_calculate_button = tk.Button(frame_5, text='简单运算', command=simple_calculate)
# tooltip = Tooltip(simple_calculate_button, "点击后根据提示输入变量值运算")
simple_calculate_button.pack(side="left", pady=5, padx=60)
simple_calculate_label = tk.Label(frame_5, text="适用于数据量较少的情况，根据提示传值运算")
simple_calculate_label.pack(side="left")

frame_6 = tk.Frame(third_frame)
frame_6.pack(anchor="w")
batch_calculate_button = tk.Button(frame_6, text='批量运算', command=batch_calculate)
# tooltip = Tooltip(batch_calculate_button, "点击后根据提示传入数据文件运算")
batch_calculate_button.pack(side="left", pady=5, padx=60)
batch_calculate_label = tk.Label(frame_6, text="适用于数据量较大的情况，传入Excel数据文件运算")
batch_calculate_label.pack(side="left")

fram_7 = tk.Frame(third_frame)
fram_7.pack(ipady=20)
export_button = tk.Button(fram_7, text="保存结果", command=export_file)
export_button.pack(side="left", padx=10, pady=10)
# tooltip = Tooltip(export_button, "保存当前运算式与输出框中的结果")
clean_button = tk.Button(fram_7, text="清除窗口", command=clear_window)
clean_button.pack(side="left", padx=10, pady=10)
# tooltip = Tooltip(clean_button, "清除输出框中的结果和运行日志")


### 输出结果
output_frame = tk.LabelFrame(right_flame, text="输出结果")
output_frame.pack(pady=20,padx=10,expand=True,fill=tk.BOTH)
res_datatext = ScrolledText(output_frame, wrap="none", width=40,height=30)
res_datatext.bind('<KeyPress>', lambda f: 'break')
res_datatext.pack(pady=10,padx=10,expand=True,fill=tk.BOTH)

scrollbar_data = tk.Scrollbar(output_frame, orient="horizontal", command=res_datatext.xview)
res_datatext.config(xscrollcommand=scrollbar_data.set)
scrollbar_data.pack(side=tk.BOTTOM, fill=tk.X)


### 日志
log_frame = tk.LabelFrame(right_flame, text="运行日志")
log_frame.pack(pady=20,padx=10,expand=True, fill=tk.BOTH)
log_text = ScrolledText(log_frame, width=40,height=10)
log_text.bind('<KeyPress>', lambda f: 'break')
log_text.pack(pady=10,padx=10,expand=True,fill=tk.BOTH)

root.mainloop()