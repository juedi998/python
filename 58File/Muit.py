#coding:utf-8
from channel import channel_link
import multiprocessing,time
from page_parsing import get_links_from
def all_get(channel):
    for num in range(1,101):
        get_links_from(channel,num)
if __name__=='__main__':
    try:
        pool = multiprocessing.Pool()
        pool.map(all_get,channel_link.split())
        print(channel_link.split())
    except IndexError or ConnectionError:
        print('由于远端服务器积极拒绝，本程序将休眠20秒后重新启动！.....')
        time.sleep(20)
        pool = multiprocessing.Pool()
        pool.map(all_get, channel_link.split())
        print(channel_link.split())

