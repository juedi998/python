#coding:utf-8
from channel import channel_link  #引用列表文件
import multiprocessing,time  #引用多进程库
from page_parsing import get_links_from
def all_get(channel):
    for num in range(1,101): #num用于爬取指定页数
        get_links_from(channel,num)
if __name__=='__main__':
    try:
        pool = multiprocessing.Pool() #定义线程池
        pool.map(all_get,channel_link.split())
        print(channel_link.split())
    except IndexError or ConnectionError: #异常后自动进入休眠
        print('由于远端服务器积极拒绝，本程序将休眠20秒后重新启动！.....')
        time.sleep(20)
        pool = multiprocessing.Pool()
        pool.map(all_get, channel_link.split())
        print(channel_link.split())

