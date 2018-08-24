# -*- coding: utf-8 -*- 
'''
PID调参小工具 Python - tkinter

TODO 设定整体的背景颜色
TODO 美化页面布局
'''
import sys
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

time_set = np.array([0]) # x轴数据，时间点
real_value_set = np.array([0]) # Y轴数据，实际值的集合
root_width = 1000 # 窗口的宽度


target_value = 0 # 目标值

matplotlib.use('TkAgg')

# tkinter组件
root = tk.Tk()
root.title('PID调参小工具-1Z实验室(1zlab.com)')
root.geometry('1000x600')

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
    # TODO 设定目标值， 串口发送指令
    global target_value
    global target_input
    # 更新target 取值
    target_value = target_input.get()
    pass

button =tk.Button(master=target_set_frame, text='设定目标值', command=set_target, width=10, height=2, font=('Arial', 12))
button.pack(side=tk.RIGHT)

target_set_frame.pack()



def update_pid_info():
    # 更新PID信息
    global kp
    global ki
    global kd
    global l
    pid_info_label.config(text='KP=-{} ,  KI=-{} ,  KD = -{}'.format(kp, ki, kd))
    # TODO 通过串口发送新的KP KI KD
    # TODO 通信协议确定 

# 回调函数 更新PID参数
def update_kp(new_pd):
    global kp
    kp = new_pd
    update_pid_info()

def update_ki(new_pi):
    global ki
    ki = new_pi
    update_pid_info()

def update_kd(new_pd):
    global kd
    kd = new_pd
    update_pid_info()

# 显示PID信息的Label
pid_info_label = tk.Label(left_frame, bg='LightCyan', width=50, height=3, text='empty', font=('Arial', 15))
pid_info_label.pack()

# KP 滑动条
kp_scale = tk.Scale(right_frame, label='KP', from_=0, to=50, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=10, resolution=0.01, command=update_kp)
kp_scale.pack()
# KI 滑动条
ki_scale = tk.Scale(right_frame, label='KI', from_=0, to=50, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=10, resolution=0.01, command=update_ki)
ki_scale.pack()
# KD 滑动条
kd_scale = tk.Scale(right_frame, label='KD', from_=0, to=50, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=10, resolution=0.01, command=update_kd)
kd_scale.pack()


# 更新图像
# 每隔0.05s执行一次
def update_figure():
    global canvas
    global bottom_frame
    # 串口接收数据
    print('update figure')
    # 解析数据

    # 动态绘制在Canvas上面

    bottom_frame.after(1, update_figure)
    # timer = threading.Timer(0.05, update_figure)
    # timer.start()

# 设置图形尺寸与质量
figure = Figure(figsize=(10,4), dpi=100)
axes = figure.add_subplot(111)
# 绘制图形
axes.plot(time_set, real_value_set)

# 把绘制的图形显示到tkinter窗口上
canvas = FigureCanvasTkAgg(figure, master=bottom_frame)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
toolbar = NavigationToolbar2TkAgg(canvas, bottom_frame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

bottom_frame.after(1, update_figure)

'''
按钮
'''
# def _quit():
#     # 结束事件主循环，销毁应用程序窗口
#     root._quit()
#     root.destroy()
#     exit(0)

# button =tk.Button(master=root, text='退出', command=_quit)
# button.pack(side=tk.BOTTOM)

# 定时器 0.01s （10ms）执行一次，
# timer = threading.Timer(0.01, update_figure)
# timer.start()

# 程序主循环
root.mainloop()
