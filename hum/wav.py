import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

y, sr = librosa.load(r"/Users/songshuang/Desktop/Hum.wav")
print(y.shape)
print(sr)

# 音色谱
chroma_stft = librosa.feature.chroma_stft(y=y, sr=44100, n_chroma=12, n_fft=4096)
# 另一种常数Q音色谱
chroma_cq = librosa.feature.chroma_cqt(y=y, sr=44100)
# 功率归一化音色谱
chroma_cens = librosa.feature.chroma_cens(y=y, sr=44100)
print(chroma_cens.shape)

c = pd.DataFrame(chroma_cq)
c0 = (c == 1)
c1 = c0.astype(int)
labels = np.array(range(1, 13))
note_values = labels.dot(c1)

plt.figure(figsize=(15, 20))
plt.subplots_adjust(wspace=1, hspace=0.2)

plt.subplot(312)
librosa.display.specshow(chroma_cq, y_axis='chroma', x_axis='time')
plt.xlabel('note')
plt.ylabel('beat')
note_values = labels.dot(c1)

plt.subplot(311)
librosa.display.waveplot(y, sr=sr)
plt.xlabel('second')
plt.ylabel('amplitude')

plt.subplot(313)
plt.grid(linewidth=0.5)
plt.xticks(range(0, 600, 50))
plt.yticks(range(1, 13), ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
plt.scatter(range(len(note_values)), note_values, marker="s", s=1, color="red")

plt.show()