import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import csv
import re
import json
from cnocr import CnOcr
from aip import AipOcr
import os
import time
import xlwt
import pymysql


# APP_ID = "24872907"
# API_KEY = "qe3mFWNIQ8qGcf7jCKDcyo4N"
# SECRET_KEY = "6E39Zt58dGGlyAQl7bTuR1zkox3iHich"
APP_ID = '24850420'
API_KEY = 'YAm0QVqTV7lYV9lyTzhbGT5W'
SECRET_KEY = 'hlcIwGf0Sqrp6bVITiwhOOEIzESQwSAe'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def parse_pic_to_excel_data(src):
    raw = cv2.imread(src, 1)
    cv2.imshow("original_picture", raw)
    cv2.imwrite("/Users/songshuang/Desktop/ocr/original.png",raw)
    # 灰度图片
    gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    # 二值化
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    cv2.imwrite("/Users/songshuang/Desktop/ocr/binary.png",binary)
    # 展示图片
    cv2.imshow("binary_picture", binary)
    rows, cols = binary.shape
    scale = 40
    # 自适应获取核值 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated_col = cv2.dilate(eroded, kernel, iterations=5)
    cv2.imshow("excel_horizontal_line", dilated_col)
    cv2.imwrite("/Users/songshuang/Desktop/ocr/horizontal.png",dilated_col)
    # 识别竖线
    scale = 20
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilated_row = cv2.dilate(eroded, kernel, iterations=7)
    cv2.imshow("excel_vertical_line", dilated_row)
    cv2.imshow("/Users/songshuang/Desktop/ocr/vertical.png",dilated_row)
    # 标识交点
    bitwise_and = cv2.bitwise_and(dilated_col, dilated_row)
    cv2.imshow("excel_bitwise_and", bitwise_and)
    cv2.imwrite("/Users/songshuang/Desktop/ocr/dots.png",bitwise_and)
    # 标识表格
    merge = cv2.add(dilated_col, dilated_row)
    cv2.imshow("entire_excel_contour", merge)
    cv2.imwrite("/Users/songshuang/Desktop/ocr/merge.png",merge)
    # 两张图片进行减法运算，去掉表格框线
    merge2 = cv2.subtract(binary, merge)
    cv2.imshow("binary_sub_excel_rect", merge2)
    cv2.imwrite("/Users/songshuang/Desktop/ocr/merge2.png", merge2)

    new_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    erode_image = cv2.morphologyEx(merge2, cv2.MORPH_OPEN, new_kernel)
    # cv2.imshow('erode_image2', erode_image)
    merge3 = cv2.add(erode_image, bitwise_and)
    cv2.imshow('merge3', merge3)
    cv2.imwrite("/Users/songshuang/Desktop/ocr/merge3.png", merge3)
    # cv2.waitKey(0)
    # 识别黑白图中的白色交叉点，将横纵坐标取出
    ys, xs = np.where(bitwise_and > 0)
    # 纵坐标
    y_point_arr = []
    # 横坐标
    x_point_arr = []
    # 通过排序，获取跳变的x和y的值，说明是交点，否则交点会有好多像素值值相近，我只取相近值的最后一点
    # 这个10的跳变不是固定的，根据不同的图片会有微调，基本上为单元格表格的高度（y坐标跳变）和长度（x坐标跳变）
    i = 0
    sort_x_point = np.sort(xs)
    for i in range(len(sort_x_point) - 1):
        if sort_x_point[i + 1] - sort_x_point[i] > 10:
            x_point_arr.append(sort_x_point[i])
        i = i + 1
    x_point_arr.append(sort_x_point[i])  # 要将最后一个点加入

    i = 0
    sort_y_point = np.sort(ys)
    for i in range(len(sort_y_point) - 1):
        if (sort_y_point[i + 1] - sort_y_point[i] > 10):
            y_point_arr.append(sort_y_point[i])
        i = i + 1
    # 要将最后一个点加入
    y_point_arr.append(sort_y_point[i])
    print('y_point_arr', y_point_arr)
    print('x_point_arr', x_point_arr)

    # 循环y坐标，x坐标分割表格
    data = [[] for i in range(len(y_point_arr))]
    n = len(y_point_arr) - 2
    m = len(x_point_arr) - 1
    res = [[''] * m for i in range(n)]
    for i in range(len(y_point_arr) - 2):
        for j in range(len(x_point_arr) - 1):
            # 在分割时，第一个参数为y坐标，第二个参数为x坐标
            cell = raw[y_point_arr[i]:y_point_arr[i + 1], x_point_arr[j]:x_point_arr[j + 1]]
            # cv2.imshow("sub_pic" + str(i) + str(j), cell)
            cv2.imwrite("sub_pic/img"+str(i)+"_"+str(j)+".png",cell)
            # cv2.waitKey(0)

            # # 读取文字(利用tesseract)
            # # text1 = pytesseract.image_to_string(cell, lang="chi_sim")
            # #利用cnocr
            # # ocr = CnOcr()
            # # res1 = ocr.ocr(cell)
            # # list1 = list(res1[0])
            # # print(''.join(list1[0]))
            #利用百度aip
            cell = np.array(cv2.imencode('.png', cell)[1]).tobytes()
            time.sleep(2)
            text1 = client.general(cell)
            for k in range(len(text1['words_result'])):
                res[i][j] = res[i][j] + text1['words_result'][k]['words']

            # 去除特殊字符
            text2=res[i][j]
            text2 = re.findall(r'[^\*"/:?\\|<>″′‖ 〈\n]', text2, re.S)
            text2 = "".join(res[i][j])
            print('单元格图片信息：'+text2 )
            data[i].append(text2)
            j = j + 1
        i = i + 1
    # xls_wirte(res)
    # cv2.waitKey(0)
    return data

def xls_wirte(res):
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True  # 黑体
    font.underline = True  # 下划线
    font.italic = True  # 斜体字
    style.font = font  # 设定样式
    for i in range(len(res)):
        for j in range(len(res[0])):
            worksheet.write(i, j, res[i][j])
    workbook.save('xls/formatting1.xls')

def write_csv(path, data):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        print("行数："+ len(data))
        print("列数："+ len(data[0]))
        writer.writerows(data)
        for i in range(len(data)):#行数
            # for j in range(len(data[0])):#列数
                writer.writerow(data[i])
        for index, item in enumerate(data):
            writer.writerows([[item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7] ,item[8],item[9],item[10]]])


if __name__ == '__main__':
    file = "1.jpg"
    # 解析数据
    datas = parse_pic_to_excel_data(file)
    # print(data)
    # 写入excel
    # write_csv(file.replace("1.jpg", ".csv"), data)
    # 写入MySQL数据库
    db = pymysql.connect(host="localhost", port=3306, user='root', passwd='nrxxybnx99', db="formdata", charset='utf8',
                         local_infile=1)
    cursor = db.cursor()

    #建立数据库
    sql_createTb = """
            create table medicine5(
            id INT NOT NULL AUTO_INCREMENT,
            序号 char(15),
            药品名称 char(15),
            药品规格 char(15),
            单位 char(15),
            生产厂家 char(30),
            数量 char(15),
            单价 char(15),
            金额 char(15),
            批号 char(15),
            有效期至 char(15),
            批准文号 char(30),
            PRIMARY KEY(id)
            )
            """
    cursor.execute(sql_createTb)

    sql = "insert into medicine5 (序号,药品名称,药品规格,单位,生产厂家,数量,单价,金额,批号,有效期至,批准文号) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for data in datas:
        print(data)
        print(data[0])
        insert = cursor.execute(sql, (
        data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]))
    cursor.close()
    db.commit()
    db.close()
