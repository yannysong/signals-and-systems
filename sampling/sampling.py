import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

##定义Rect wave函数 Rec_wav
# 第一个参数为方波时间对应的list，第二个参数为方波的幅度。
def Rec_wave(x, A):
    y = np.zeros(len(x))
    for i in range(1, 101, 2):
        y += 4 * A / np.pi * np.sin(2 * np.pi * i * x) / i
    return y


# 定义Frequece Amplitude函数 Fre_ampl
# 第一个参数为信号时间的list，第二个参数为信号对应时间的幅度的list
# 返回两个参数，第一个参数为frequecy的list(所得频率序列需除以总时长)，第二个参数为amplitude的list
def Fre_ampl(x, y):
    y_f = np.fft.fft(y)
    f = np.arange(len(x))
    abs_y = np.abs(y_f)
    normalization_y = abs_y / (len(x))
    half_x = f[range(int(len(x) / 2))]
    normalization_y = normalization_y[range(int(len(x) / 2))]
    return half_x, normalization_y


# 定义Show sin函数 Show_sin
def Show_sin():
    # 定义信号时间
    t = np.arange(0, 1, 0.001)
    # 定义正弦波
    y_sin = 3 * np.sin(12 * np.pi * t)
    plt.figure(num=1, figsize=(8, 6))
    plt.subplot(2, 2, 1)
    plt.axis([0, 1, -3.2, 3.2])
    plt.plot(t, y_sin, 'b')
    plt.xlabel('time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 正常采样
    y_sin1 = y_sin.copy()
    i = 0
    N = 7
    while i < N:
        y_sin1[i::N + 1] = 0
        i = i + 1
    plt.subplot(2, 2, 2)
    plt.axis([0, 1.05, -3.2, 3.2])
    plt.vlines(t, 0, y_sin1, 'r')
    plt.xlabel('Time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 欠采样
    y_sin2 = y_sin.copy()
    i = 0
    N = 150
    while i < N:
        y_sin2[i::N + 1] = 0
        i = i + 1
    plt.subplot(2, 2, 3)
    plt.axis([0, 1.05, -3.2, 3.2])
    plt.vlines(t, 0, y_sin2, 'g')
    plt.xlabel('Time/(s)')
    plt.ylabel('Amplitude/(V)')
    # 还原信号
    b, a = signal.iirdesign(0.08, 0.1, 1, 40)  # 设置低通滤波器
    y_sinh1 = signal.filtfilt(b, a, y_sin1)
    y_sinh2 = signal.filtfilt(b, a, y_sin2)
    plt.subplot(2, 2, 4)
    plt.axis([0, 1, -0.5, 0.5])
    plt.plot(t, y_sinh1, color='r', label='enough')
    plt.plot(t, y_sinh2, color='g', label='low')
    plt.legend(loc='best')
    plt.xlabel('Time/(s)')
    plt.ylabel('Amplitude/(V)')
    """各个信号频谱"""
    plt.figure(num=2, figsize=(8, 5))
    f_sin, am_sin = Fre_ampl(t, y_sin)
    f_sin1, am_sin1 = Fre_ampl(t, y_sin1)
    f_sin2, am_sin2 = Fre_ampl(t, y_sin2)
    f_sinh1, am_sinh1 = Fre_ampl(t, y_sinh1)
    f_sinh2, am_sinh2 = Fre_ampl(t, y_sinh2)

    plt.subplot(5, 1, 1)
    plt.axis([0, 10, 0, 3])
    plt.vlines(f_sin, 0, am_sin, 'b')
    plt.xlabel('Frequence/(Hz)')
    plt.ylabel('Amplitude/(V)')

    plt.subplot(5, 1, 2)
    plt.vlines(f_sin1, 0, am_sin1, 'r')
    plt.xlabel('Frequence/(Hz)')
    plt.ylabel('Amplitude/(V)')

    plt.subplot(5, 1, 3)
    plt.vlines(f_sin2, 0, am_sin2, 'c')
    plt.xlabel('Frequence/(Hz)')
    plt.ylabel('Amplitude/(V)')

    plt.subplot(5, 1, 4)
    plt.axis([0, 10, 0, 0.1])
    plt.vlines(f_sinh1, 0, am_sinh1, 'r')
    plt.xlabel('Frequence/(Hz)')
    plt.ylabel('Amplitude/(V)')

    plt.subplot(5, 1, 5)
    # plt.axis([0,10,0,3])
    plt.vlines(f_sinh2, 0, am_sinh2, 'c')
    plt.xlabel('Frequence/(Hz)')
    plt.ylabel('Amplitude/(V)')

Show_sin()
plt.tight_layout()
plt.show()

