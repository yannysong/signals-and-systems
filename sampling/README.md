Sampling and reduction
===
0.Setup Environment
---
This project is running in Python3.x, and please enusre following packages are installed:
* numpy
* scipy
* matplotlib

1.How to run
---
Run directly.

2.Underlying principle
---
* Sampling
  * Nyquist–Shannon sampling theorem: establishes a sufficient condition for a sample rate that permits a discrete sequence of samples to capture all the information from a continuous-time signal of finite bandwidth. The sampling frequency should be larger than twice of the highest frequency.
  * Aliasing: Aliasing is an effect that causes different signals to become indistinguishable.
  * Downsampling: Producing an approximation of the sequence that would have been obtained by sampling the signal at a lower rate.
* Reconstruction
  * The determination of an original continuous signal from a sequence of equally spaced samples. 
  * Butterworth filter: The Butterworth filter is a type of signal processing filter designed to have a frequency response as flat as possible in the passband. 

3.Structure
---
>Waveform generator
>>Sampling
>>>Reconstruction

4.Primary formula
---
* Rec_wave()
* Fre_ampl()
* signal.iirdesign()

Author
---
Song Shuangyannan
