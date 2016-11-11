#coding:utf-8
import time
from page_parsing import info
while True:  #文件仅用于遍历数据库
    print(info.find().count())
    time.sleep(5)
