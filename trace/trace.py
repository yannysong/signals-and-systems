import tkinter as tk
import tkinter.font as tkFont
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import math


# 定义函数is_number 判断一个字符串是不是数字。
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 定义函数callback 显示轨迹按键的界面响应。
def callback():
    plt.clf()
    if is_number(info[0].get()) and is_number(info[1].get()) and is_number(info[2].get()):
        fun_show()
    else:
        tk.messagebox.showerror("错误", "数据不符合要求，请重新输入")


# 定义函数fun_show 显示二阶状态轨迹的函数实现。
def fun_show():
    # 得到RLC电路的电阻，电感和电容。
    R = float(info[0].get())
    L = float(info[1].get())
    C = float(info[2].get())
    # 阻尼系数
    a = R / (2 * L)
    # 谐振角频率
    w0 = 1 / math.sqrt(L * C)
    # 定义时间和电源电压
    t = np.arange(0, 100, 0.01)
    ut = np.array([1 for i in t])
    # 过阻尼状态
    if a > w0 and a > 0:
        B = math.sqrt(a * a - w0 * w0)
        i_lt = ((1 / L) * np.exp(-a * t) * np.sinh(B * t)) / (B * ut)
        v_ct = (np.exp(-a * t) * (np.exp(-a * t) / (a + B) - np.exp(-a * t) / (a - B))) / (2 * B * L * C) + 1
        plt.subplot(4, 1, 1)
        plt.plot(t, i_lt)
        plt.xlabel("time/s")
        plt.ylabel("Il(t)/A")
        plt.subplot(4, 1, 2)
        plt.plot(t, v_ct)
        plt.xlabel("time/s")
        plt.ylabel("Vc(t)/V")
        plt.subplot(4, 1, 3)
        plt.plot(v_ct, i_lt)
        plt.xlabel("Vc(t)/V")
        plt.ylabel("Il(t)/A")
        img.draw()

        font1 = tkFont.Font(size=15, weight=tkFont.BOLD)
        title = tk.Label(ui, text="过阻尼状态", fg='black', font=font1)
        title.place(relx=0.62, rely=0.02, width=120, height=45)
    # 临界阻尼状态
    if a == w0 and a > 0:
        i_lt = (1 / L) * t * np.exp(-a * t)
        v_ct = (1 / (L * C * a * a)) * (1 - (a * t + 1) * np.exp(-a * t))
        plt.subplot(4, 1, 1)
        plt.plot(t, i_lt)
        plt.xlabel("time/s")
        plt.ylabel("Il(t)/A")
        plt.subplot(4, 1, 2)
        plt.plot(t, v_ct)
        plt.xlabel("time/s")
        plt.ylabel("Vc(t)/V")
        plt.subplot(4, 1, 3)
        plt.plot(v_ct, i_lt)
        plt.xlabel("Vc(t)/V")
        plt.ylabel("Il(t)/A")
        img.draw()

        font1 = tkFont.Font(size=13, weight=tkFont.BOLD)
        title = tk.Label(ui, text="临界阻尼状态", fg='black', font=font1)
        title.place(relx=0.62, rely=0.02, width=120, height=45)
    # 欠阻尼状态
    if a < w0 and a > 0:
        w1 = math.sqrt(w0 * w0 - a * a)
        i_lt = w1 * L * np.exp(-a * t) * np.sin(w1 * t)
        v_ct = 1 - np.exp(-a * t) * (np.cos(w1 * t) + np.sin(w1 * t))  # /(a*w1)
        plt.subplot(4, 1, 1)
        plt.plot(t, i_lt)
        plt.xlabel("time/s")
        plt.ylabel("Il(t)/A")
        plt.subplot(4, 1, 2)
        plt.plot(t, v_ct)
        plt.xlabel("time/s")
        plt.ylabel("Vc(t)/V")
        plt.subplot(4, 1, 3)
        plt.plot(v_ct, i_lt)
        plt.xlabel("Vc(t)/V")
        plt.ylabel("Il(t)/A")
        img.draw()

        font1 = tkFont.Font(size=15, weight=tkFont.BOLD)
        title = tk.Label(ui, text="欠阻尼状态", fg='black', font=font1)
        title.place(relx=0.62, rely=0.02, width=120, height=45)
    # 无阻尼状态
    if a == 0:
        i_lt = L * w0 * np.sin(w0 * t)
        v_ct = 1 - np.cos(w0 * t)
        plt.subplot(4, 1, 1)
        plt.plot(t, i_lt)
        plt.xlabel("time/s")
        plt.ylabel("Il(t)/A")
        plt.subplot(4, 1, 2)
        plt.plot(t, v_ct)
        plt.xlabel("time/s")
        plt.ylabel("Vc(t)/V")
        plt.subplot(4, 1, 3)
        plt.plot(v_ct, i_lt)
        plt.xlabel("Vc(t)/V")
        plt.ylabel("Il(t)/A")
        img.draw()

        font1 = tkFont.Font(size=15, weight=tkFont.BOLD)
        title = tk.Label(ui, text="无阻尼状态", fg='black', font=font1)
        title.place(relx=0.62, rely=0.02, width=120, height=45)


# 定义函数ui_init ui界面初始化，返回参数ui，以及输入框entry列表。
def ui_init():
    ui = tk.Tk()
    ui.resizable(False, False)  # 取小最大化的按键

    ui.title("exp3:二阶状态轨迹")
    ui.geometry("900x600+0+0")  # 设置界面大小


    ##设置输入界面
    label1 = tk.Label(ui, text='请输入R/Ω', fg='black')
    label1.place(relx=0.12, rely=0.1, width=120, height=30)
    label2 = tk.Label(ui, text='请输入L/H', fg='black')
    label2.place(relx=0.12, rely=0.3, width=120, height=30)
    label3 = tk.Label(ui, text='请输入C/F', fg='black')
    label3.place(relx=0.12, rely=0.5, width=120, height=30)

    R1 = tk.StringVar()
    R2 = tk.StringVar()
    R3 = tk.StringVar()

    entry1 = tk.Entry(ui, textvariable=R1)
    entry1.place(relx=0.12, rely=0.1, width=120, y=30)
    entry2 = tk.Entry(ui, textvariable=R2)
    entry2.place(relx=0.12, rely=0.3, width=120, y=30)
    entry3 = tk.Entry(ui, textvariable=R3)
    entry3.place(relx=0.12, rely=0.5, width=120, y=30)
    info = [entry1, entry2, entry3]

    ##设置按键及点击事件
    button1 = tk.Button(ui, text='显示轨迹', command=callback, relief='raised', bg='black', fg='white')
    button1.place(relx=0.12, rely=0.7, width=120, height=70)
    return ui, info


# 定义函数fig_init plot界面初始化，返回视图fig，以及画板img。
def fig_init(ui):
    matplotlib.use('TkAgg')
    fig = plt.figure(num=1)
    img = FigureCanvasTkAgg(fig, master=ui)
    img.draw()
    img.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
    toolbar = NavigationToolbar2Tk(img, ui)
    toolbar.update()
    img._tkcanvas.place(relx=0.52, rely=0.1, width=300, height=600)
    return fig, img


# 运行界面
ui, info = ui_init()
fig, img = fig_init(ui)
ui.mainloop()

