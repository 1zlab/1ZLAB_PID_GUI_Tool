# -*- coding: utf-8 -*- 
'''
PID调参小工具 Python - Tkinter

TODO 添加串口连接的部分 （设备号列表框，PySerial 串口连接）
TODO 多个可视化波形
'''
import tkinter as tk

window = tk.Tk()
window.title('PID调参小工具-1Z实验室')
window.geometry('550x500')

l = tk.Label(window, bg='LightCyan', width=50, height=3, text='empty', font=('Arial', 15))
l.pack()

kp = 0
ki = 0
kd = 0

def update_pid_info():
    global kp
    global ki
    global kd
    global l
    l.config(text='KP=-{} ,  KI=-{} ,  KD = -{}'.format(kp, ki, kd))
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

# KP 滑动条
kp_scale = tk.Scale(window, label='KP', from_=0, to=50, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=10, resolution=0.01, command=update_kp)
kp_scale.pack()
# KI 滑动条
ki_scale = tk.Scale(window, label='KI', from_=0, to=50, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=10, resolution=0.01, command=update_ki)
ki_scale.pack()
# KD 滑动条
kd_scale = tk.Scale(window, label='KD', from_=0, to=50, orient=tk.HORIZONTAL,
             length=500, showvalue=0, tickinterval=10, resolution=0.01, command=update_kd)
kd_scale.pack()


# 更新图像
# 每隔0.05s执行一次
def update_figure():
    # 串口接收数据
    
    # 解析数据

    # 动态绘制在Canvas上面

    timer = threading.Timer(0.05, update_figure)
    timer.start()

'''按钮'''
def _quit():
    # 结束事件主循环，销毁应用程序窗口
    window._quit()
    window.destroy()
    exit(0)

button =Tk.Button(master=window, text='退出', command=_quit)
button.pack(side=Tk.BOTTOM)

# 定时器 0.01s （10ms）执行一次，
timer = threading.Timer(0.01, update_figure)
timer.start()

# 程序主循环
window.mainloop()
