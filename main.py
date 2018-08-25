# -*- coding: utf-8 -*- 
'''
PID调参小工具 Python - tkinter

TODO 设定整体的背景颜色
TODO 美化页面布局
TODO 纵轴的取值范围问题
TODO Target值 中间画一条红线
TODO Y轴随着Target取值范围取
'''
import sys
import serial
import struct
import time
import math
import tkinter as tk
import matplotlib
import numpy as np
# import threading
# import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg

from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# PID参数
kp = 0
ki = 0
kd = 0

real_value_set = [] # Y轴数据，实际值的集合
canvas_time_width = 100 # 窗口的宽度


target_value = 0 # 目标值

matplotlib.use('TkAgg')

'''
初始化串口通信相关
'''
# 串口号 默认为 /dev/ttyUSB0
ser_dev = '/dev/ttyUSB1'
# 创建一个串口实例
ser = serial.Serial(ser_dev, 115200, timeout=1, bytesize=8)


# tkinter组件
root = tk.Tk()
root.title('PID调参小工具-1Z实验室(1zlab.com)')
root.geometry('600x400')

pid_info_label = tk.Label(root, width=50, height=3, text='PID调参小工具-1Z实验室', font=('Arial', 15))
pid_info_label.pack(side = tk.TOP)

# 上位机上部
top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP)
# 上位机下部
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM)

# 创建左侧的Frame
left_frame = tk.Frame(top_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.NO)
# left_frame.geometry('500x250')
right_frame = tk.Frame(top_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.NO)
# right_frame.geometry('500x250')

target_set_frame = tk.Frame(left_frame)
# 目标值的输入框
target_input = tk.Entry(target_set_frame, width=10, font=('Arial', 20))
target_input.pack(side=tk.LEFT)

# 设定目标值按钮
def set_target():
    # TODO 对input的值进行检测
    global target_value
    global target_input
    try:
        target_value = float(target_input.get())
    except ValueError:
        print('[ERROR] 非法的目标值设定, 只能是浮点数')

    data_str = ','.join(['SET_TARGET', str(target_value)])
    data_str += '\n' # 添加换行符号
    data_byte = data_str.encode('utf-8')
    ser.write(data_byte)

button =tk.Button(master=target_set_frame, text='设定目标值', command=set_target, width=10, height=2, font=('Arial', 12))
button.pack(side=tk.RIGHT)

target_set_frame.pack()



def update_pid_info():
    # 更新PID信息
    global kp
    global ki
    global kd
    global pid_info_label
    global ser

    pid_info_label.config(text='KP={} ,  KI={} ,  KD = {}'.format(kp, ki, kd))
    data_str = ','.join(['SET_PID', str(kp), str(ki) , str(kd)])
    data_str += '\n' # 添加换行符号
    data_byte = data_str.encode('utf-8')
    ser.write(data_byte)

# 回调函数 更新PID参数
def update_kp(new_pd):
    global kp
    kp = -1 * float(new_pd)
    update_pid_info()

def update_ki(new_pi):
    global ki
    ki = -1 * float(new_pi)
    update_pid_info()

def update_kd(new_pd):
    global kd
    kd = -1 * float(new_pd)
    update_pid_info()

# 显示PID信息的Label
pid_info_label = tk.Label(left_frame, bg='LightCyan', width=50, height=3, text='empty', font=('Arial', 15))
pid_info_label.pack()

# KP 滑动条
kp_scale = tk.Scale(right_frame, label='KP', from_=0, to=15, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=3, resolution=0.01, command=update_kp)
kp_scale.pack()
# KI 滑动条
ki_scale = tk.Scale(right_frame, label='KI', from_=0, to=5, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=1, resolution=0.01, command=update_ki)
ki_scale.pack()
# KD 滑动条
kd_scale = tk.Scale(right_frame, label='KD', from_=0, to=10, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=2, resolution=0.01, command=update_kd)
kd_scale.pack()

def update_real_value(new_real_value):
    global canvas
    global bottom_frame
    global figure
    global real_value_set # Y轴数据，实际值的集合
    global canvas_time_width # 窗口的宽度

    new_real_value = float(new_real_value)
    # 更新实际值，并更新画面
    print('update real value {}'.format(new_real_value))
    real_value_set.append(new_real_value)
    
    while len(real_value_set) > canvas_time_width:
        real_value_set.pop(0)
    
    

def cmd_process(data_str):
    cmd_list = {
        'REAL_VALUE': update_real_value
    }

    params = data_str.split(',')
    cmd_name = params[0]
    if cmd_name in cmd_list:
        cmd_list[cmd_name](*params[1:])
    else:
        print("[ERROR] 非法指令 {}".format(cmd_name))

# 定时器回调
# 每隔0.05s执行一次
def timer_callback():
    global ser
    global canvas
    global figure
    global target_input

    # 串口接收数据
    while ser.in_waiting:
        # 判断串口是不是有数据读进来
        data_byte = ser.readline()
        data_str = data_byte.decode('utf-8')
        print('RECIEVE')
        print(data_str)
        cmd_process(data_str)

    if len(target_input.get()) == 0:
        target = 0
    else:
        target = float(target_input.get())

    # 更新图像
    figure.clf()
    axes = figure.add_subplot(111)
    axes.set_xlim(0, canvas_time_width)
    axes.set_xticks([])
    axes.set_ylim(-180 + target, target+180)
    axes.set_yticks([-180 + target, target, target+180])

    

    #绘制图形
    axes.plot(np.arange(0,len(real_value_set)), np.array(real_value_set))
    axes.plot([0, 100], [target, target], color='red')
    canvas.draw()
    # 100ms 更新一次
    bottom_frame.after(1, timer_callback)

# 设置图形尺寸与质量
figure = Figure(figsize=(10,4), dpi=100)
axes = figure.add_subplot(111)
# 绘制图形
axes.plot(np.arange(len(real_value_set)), real_value_set)

# 把绘制的图形显示到tkinter窗口上
canvas = FigureCanvasTkAgg(figure, master=bottom_frame)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
toolbar = NavigationToolbar2TkAgg(canvas, bottom_frame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

# 执行定时器
bottom_frame.after(1, timer_callback)


# 程序主循环
root.mainloop()
