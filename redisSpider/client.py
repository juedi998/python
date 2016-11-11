#coding:utf-8
import requests,time,random,multiprocessing
from redis import Redis
headers={ 'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36' }
link_redis = Redis(host="localhost",port='6379',password='password') #连接远端Redis服务器

def Down_img_url(url): #用于下载图片
    if url != None:
        name = int(time.time())
        File_path = 'D:/python工程/四周/01-02/img/' + str(name) + '.jpg'
        Down_img = requests.get(url,headers=headers,stream=True)
        try:
            with open(File_path,'wb')as df:
                for chunk in Down_img.iter_content(1024):
                    df.write(chunk)
                    df.flush()
        except IOError:
            print('远端服务器拒绝建立链接或请求超时，程序将启用代理访问.....')
    else:
        print('当前没有需处理的列队.....')

def Link_Server(): #获取远端服务器信息列队
    connection = link_redis
    print(connection.keys('*'))
    while (1):
        try:
            url = connection.lpop('meizitu')
            return_1 = Down_img_url(url)
            if return_1 == -1:
                return -1
            time.sleep(1)
            print(url)
        except:
            print("远端服务未能及时响应，正在等待重启中.....")
            time.sleep(10)
            continue
if __name__=='__main__':
    pool = multiprocessing.Pool(4) #多线程 ---- 可能网络缘故，未能正常使用！
    pool.apply(Link_Server)

