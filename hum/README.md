Get the music score from a humming audio record.
===
0.Setup Environment
---
This project is running in Python3.x, and please enusre following packages are installed:
* librosa
* numpy
* pandas
* matplotlib

1.How to run
---
* Change the code via to the path of your .wav file.

2.Underlying principle
---
Music signals in library->beat time extraction->beat feature->spectrum->notes

3.Structure
---
>Get the chroma
>>transfer to notes

4.Primary formula
---
* librosa.feature.chroma_cqt()#获取常数Q音色谱
* librosa.display.specshow()#显示频谱

5.Reference
---
https://github.com/librosa/librosa

Author
---
Song Shuangyannan
