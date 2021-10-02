import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as si

#定义谐波合成函数Har——synth
#参数i为奇数谐波的最高次数，x为信号时间的list
def Har_synth(i,x):
    length=len(x)
    tmp=np.zeros(length)
    y0=list(tmp)
    result=y0
    number=(i+1)/2
    while number>0:
        cof=i+2-number*2
        y=[math.sin(xx*cof)/cof for xx in x]
        tmp+=np.array(y)
        number =number - 1
    result=list(tmp)
    return result

#定义方波函数Rec_wave
#参数x为方波时间对应的list，参数A为方波幅值
def Rec_wave(x,A):
	y=np.zeros(len(x))
	for i in range(1,101,2):
		y+=4*A/np.pi*np.sin(2*np.pi*i*x)/i
	return y

#定义三角波函数Trg_wave
#参数x为方波信号时间的list，参数y为方波对应时间的幅度的list
def Trg_wave(x,y):
    length=len(x)
    tmp=np.zeros(length)
    y0=tmp
    result=list(y0)
    i=0
    tmp[i]=0
    #对方波信号进行积分
    while i<length-1:
        i=i+1
        x_frag=x[0:i]
        y_frag=y[0:i]
        y0[i]=si.simps(y_frag,x_frag)
    result=list(y0)
    return result

#定义频率幅度函数 Fre_ampl获取频谱图
#参数x为信号时间的list，参数y为信号对应时间的幅度的list
#返回两个参数，第一个参数为frequecy的list，第二个参数为amplitude的list
def Fre_ampl(x,y):
	y_f=np.fft.fft(y)
	f=np.arange(len(x))
	abs_y=np.abs(y_f)
	normalization_y=abs_y/(len(x))
	half_x=f[range(int(len(x)/2))]
	normalization_y=normalization_y[range(int(len(x)/2))]
	return half_x,normalization_y

#方波的合成
fig=plt.figure(num=1,figsize=(6,4))
plt.subplot(2,2,1)
plt.axis([0,10,-1.1,1.1])
#a.只考虑从 t=0s 到 t=10s 这段时间内的信号
x = np.arange(0, 10, 0.01)
#b.画出基波分量 y(t)=sin(t)
y1=[math.sin(xx) for xx in x]
#c.将三次谐波加到基波之上，并画出结果，并显示
y2=[math.sin(3*xx)/3 for xx in x]
tmp2=np.array(y1)+np.array(y2)
y2=list(tmp2)
#d.再将一次，三次，五次，七次，九次谐波加在一次。
y3=Har_synth(9,x)
#e.合并从基波到十九次谐波的各奇次谐波分量
#f.将上述波形分别画在一幅画中
y4=Har_synth(19,x)
plt.plot(x,y1,label='question b',color='g')
plt.plot(x,y2,label='question c',color='c')
plt.plot(x,y3,label='question d',color='b')
plt.plot(x,y4,label='question e',color='r')
plt.xlabel('Time / s')
plt.ylabel('Amplitude')
plt.legend(loc='best')

#三角波的合成
plt.subplot(2,2,2)
#a.只考虑从 t=0s 到 t=10s 这段时间内的信号
x = np.arange(0, 10, 0.01)
#b.画出基波分量 y(t)=sin(t)
y5=[math.sin(xx) for xx in x]
y5=Trg_wave(x,y5)
#c.将三次谐波加到基波之上，并画出结果，并显示
y6=Har_synth(3,x)
y6=Trg_wave(x,y6)
#d.再将一次，三次，五次，七次，九次谐波加在一次。
y7=Har_synth(9,x)
y7=Trg_wave(x,y7)
#e.合并从基波到十九次谐波的各奇次谐波分量
#f.将上述波形分别画在一幅画中
y8=Har_synth(19,x)
y8=Trg_wave(x,y8)
plt.axis([0,10,0,math.pi])
plt.plot(x,y5,label='question b',color='g')
plt.plot(x,y6,label='question c',color='c')
plt.plot(x,y7,label='question d',color='b')
plt.plot(x,y8,label='question e',color='r')
plt.xlabel('Time / s')
plt.ylabel('Amplitude')
plt.legend(loc='best')

#分析方波频谱
yr=Rec_wave(x,3)
plt.subplot(2,2,3)
plt.axis([0,100,0,2])
freq,ampl=Fre_ampl(x,yr)
plt.vlines(freq/10,0,ampl)
plt.xlabel('Frequence/Hz')
plt.ylabel('Amplitude/V')

#分析三角波频谱
yt=Trg_wave(x,yr)
plt.subplot(2,2,4)
plt.axis([0,100,0,0.3])
freq,ampl=Fre_ampl(x,yt)
plt.vlines(freq/10,0,ampl)
plt.xlabel('Frequence/Hz')
plt.ylabel('Amplitude/V')

plt.show()