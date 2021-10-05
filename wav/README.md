Record and analysis its spectrum
===
0.Setup Environment
---
This project is running in Python3.x, and please enusre following packages are installed:
* wave
* pyaudio
* numpy
* matplotlib

1.How to run
---
* Get to know the amount of your computer's channels.
* Define the variable 'CHANNEL' according to your computer.
* Refer to the annotation, rewrite the codes via to the CHANNEL.
* Run the project.

2.Underlying principle
---
  Fast Fourier Transform(FFT):A FFT is is an algorithm that computes the DFT of a sequence, or its inverse. Fourier analysis converts a signal from its original domain (often time or space) to a representation in the frequency domain and vice versa. 

3.Structure
---
>Record
>>covert the wav signal into array
>>>compute the FFT of the signal

4.Primary formula
---
* sound_rec()
* wave_read()
* time_plt()
* freq_plt()

5.Reference
---
https://github.com/tyiannak/pyAudioAnalysis

https://github.com/thedevdojo/wave

Author
---
Song Shuangyannan
