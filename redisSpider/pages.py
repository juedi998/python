#coding:utf-8
import requests
import re
import time,random
from redis import Redis
from bs4 import BeautifulSoup

headers={ 'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36' }
link_redis = Redis(host="localhost",port='6379',password='password')#与远端Redis服务器建立联系
# def download(url):
#     number = random.random()
#     name = int(time.time())
#     File_path = 'D:/python工程/四周/01-02/img/' + str(name) + '.jpg'
#     Down_image = requests.get(url, headers=headers, stream=True)
#     try:
#         with open(File_path, 'wb')as df:
#             for chunk in Down_image.iter_content(1024):
#                 df.write(chunk)
#                 df.flush()
#     except OSError:
#         with open('D:/python工程/四周/01-02/img/' + str(number) + '.jpg', 'wb')as df:
#             for chunk in Down_image.iter_content(chunk_size=1024):
#                 df.write(chunk)
#                 df.flush()
# def get_big_img_url():
#     r = link_redis
#     print (r.keys('*'))
#     while(1):
#         try:
#             url = r.lpop('meizitu')
#             return_1 = download(url)
#             if return_1 == -1:
#                 return -1
#             time.sleep(1)
#             print (url)
#         except:
#             print ("远端服务未能及时响应，正在等待重启中.....")
#             time.sleep(10)
#             continue

def push_redis_list(num): #用于获取链接并推送至远端服务器
    r = link_redis
    print (r.keys('*'))
    for i in range(100):
        num = int(num)+i #抓取的取件仅在num+100--num+200之间
        url ='http://www.meizitu.com/a/list_1_'+ str(num) +'.html'
        img_url = requests.get(url,headers=headers)
        #print img_url.text
        #time.sleep(10)
        #img_url_list = re.findall('http://pic.meizitu.com/wp-content/uploads/201.*.jpg',img_url.text)
        img_url.encoding = 'gb2312'
        soup = BeautifulSoup(img_url.text,'lxml')
        img = soup.select('#maincontent > div.inWrap > ul > li > div > div > a > img')
        for temp_img_url in img:
                r.lpush('meizitu',temp_img_url.get('src'))
        #print (r.llen('meizitu'))
        # get_big_img_url()

if __name__ == '__main__':
    #url = 'http://www.meizitu.com/a/list_1_'
    print ("begin")
    push_redis_list(1)
