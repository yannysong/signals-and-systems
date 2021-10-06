import wave
import pyaudio
import numpy
from pyaudio import PyAudio
import matplotlib.pyplot as plt

#定义sound recoding 函数,其参数为录音时间t
def sound_rec(t):
    # 定义数据流块
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    '''
    此处的频道数根据自身电脑调整
    作者使用的是Macbook Pro 2018版，仅支持单声道采集
    支持双声道采集的电脑可将频道数改为2
    '''
    CHANNELS = 1
    RATE = 44100
    # 录音时间
    RECORD_SECONDS = t
    # 要写入的文件名
    WAVE_OUTPUT_FILENAME = "Output.wav"
    # 创建PyAudio对象
    p = pyaudio.PyAudio()
    # 打开数据流
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    print("Start recording")
    # 开始录音
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Done recording")
    # 停止数据流
    stream.stop_stream()
    stream.close()
    # 关闭PyAudio
    p.terminate()
    # 写入录音文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#定义wav文件读取函数，其参数为wav文件的路径path
#返回值为:声道的波形数组wave_data,采样率framerate，采样率*时间nframes
def wave_read(path):
    wf = wave.open(path, 'rb')
    # 创建PyAudio对象
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = wf.getframerate(),
    output = True)
    nframes = wf.getnframes()
    framerate = wf.getframerate()
    # 读取完整的帧数据到str_data中，这是一个string类型的数据
    str_data = wf.readframes(nframes)
    wf.close()
    # 将波形数据转换成数组
    wave_data = numpy.frombuffer(str_data, dtype=numpy.short)
    # 将wave_data数组改为1列，行数自动匹配
    wave_data.shape = -1,1
    #双声道将wave_data数组改为2列，行数自动匹配
    #wave_date.shape = -1,2
    # 将数组转置
    wave_data = wave_data.T
    return wave_data,framerate,nframes

#定义画出时域上的波形图函数time plot
#第一个参数为采样率，第二个参数为采样率*时间,第三个参数为声道的数据wave data list
def time_plt(frames,nframes,wave):
    # time也是一个数组，与wave_data[0]或wave_data[1]配对形成系列点坐标
    time = numpy.arange(0, nframes)*(1.0/frames)
    # 绘制波形图
    plt.figure(num=1,figsize=(6,4))
    plt.plot(time, wave.T, c='b')
    #双声道将两个声道分别制图
    # plt.subplot(211)
    # plt.plot(time, wave[0], c='b')
    # plt.subplot(212)
    # plt.plot(time, wave[1], c='g')
    plt.xlabel('time (seconds)')
    plt.ylabel('ampliude')

#定义画出信号频域上的波形函数frequence plot
#第一个参数为采样率，第二个参数为左右声道的数据wave data list
def freq_plt(frames,wave):
    # 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
    N = 44100
    start = 0  # 开始采样位置
    df = frames/(N-1)  # 分辨率
    freq = [df*n for n in range(0, N)]  # N个元素
    wave_data2 = wave[0][start:start+N]
    c = numpy.fft.fft(wave_data2)*2/N
    # 常规显示采样频率一半的频谱
    d = int(len(c)/2)
    # 仅显示频率在4000以下的频谱
    while freq[d] > 4000:
        d -= 10
    plt.figure(num=2,figsize=(6,4))
    plt.plot(freq[:d-1], abs(c[:d-1]), 'b')

sound_rec(5)
wave,frames,nframes=wave_read('Output.wav')
time_plt(frames,nframes,wave)
freq_plt(frames,wave)
plt.show()

