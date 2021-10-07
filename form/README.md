Medicine form recognization
===
0.Setup environment
---
This project is running in Python3.x, and please enusre following packages are installed:
* cv2
* numpy
* csv
* re
* aip
* time
* pymysql

1.How to run
---
* Apply for your own Baidu API account, and enter your information at 'APP_ID', 'API_KEY' and 'SECRET_KEY'.
* Set up the path of the picture to be recognized as well as the path for the cropped picture and .csv file.
* Enter your own MySQL information at 'host', 'port', 'passwd', 'user' and 'db'.
* Connect the database.

2.Underlying principle
---
* Image binarization
* image structuring and erosion
* OCR

3.Structure
---
>Pre-process the image
>>recognize the form
>>>crop the image according to the crossing dots
>>>>OCR
>>>>>create and fill the database

4.Primary formula
---
* binary = cv2.adaptiveThreshold()#图像二值化
* kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))

  eroded = cv2.erode(binary, kernel, iterations=1)
  
  #图像的腐蚀膨胀
* text1 = client.general(cell)#OCR
* cursor.execute(sql_createTb)#创建数据库

5.Reference
---
https://github.com/abidrahmank/OpenCV2-Python

https://github.com/thephpleague/csv

https://github.com/mysqljs/mysql

https://github.com/aave/aip

Author
---
Song Shuangyannan
