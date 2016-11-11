#coding:utf-8
from bs4 import BeautifulSoup
import requests,time,pymongo,random
start_url = r'http://gz.58.com/sale.shtml'
client = pymongo.MongoClient('localhost',27017) #连接数据库
tongcheng = client['tongcheng']
info = tongcheng['info']
url = tongcheng['url']
#spider 1
def get_links_from(channel,pages): #获取分页的所有链接信息
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    }
    #http://gz.58.com/ibm/pn2
    list_view = '{}pn{}/'.format(str(channel),str(pages))
    temp = list(url.find({'url': list_view}))
    if not temp:
        url.insert_one({'url': list_view})
        web_data = requests.get(list_view, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(web_data.text, 'lxml')
        link = soup.select('#infolist > div.infocon > table > tbody > tr > td.t > a')
        if soup.find('td', 't'):
            for i in link:
                url_item = i.get('href').split('?')[0]
                get_item_info(url_item)
        else:
            pass  # Nothing
    try:
        if list_view != temp[0]['url']:
            url.insert_one({'url':list_view})
            web_data = requests.get(list_view, headers=headers)
            time.sleep(2)
            soup = BeautifulSoup(web_data.text, 'lxml')
            link = soup.select('#infolist > div.infocon > table > tbody > tr > td.t > a')
            if soup.find('td', 't'):
                for i in link:
                    url_item = i.get('href').split('?')[0]
                    get_item_info(url_item)
            else:
                pass  # Nothing
        else:
            pass
    except IndexError or requests.ConnectionError: #出错将自动进入休眠期
        print('由于远端服务器积极拒绝，本程序将休眠20秒后重新启动！.....')
        time.sleep(120)
def get_item_info(url): #获取详情页信息
    web_data = requests.get(url)
    time.sleep(2)
    soup = BeautifulSoup(web_data.text,'lxml')
    title = soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.box_left_top > h1')
    price = soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.info_massege.left > div.price_li > span > i')
    acre = soup.select('body > div.content > div > div.box_left > div.info_lubotu.clearfix > div.info_massege.left > div.palce_li > span > i')
    name = soup.select('body > div.content > div > div.box_right > div.personal.jieshao_div > div.personal_jieshao > p.personal_name')
    img = soup.select('body > div.content > div > div.box_right > div.personal.jieshao_div > div.personal_jieshao > div > img')
    for titles,prices,acres,names,imgs in zip(title,price,acre,name,img):
        print('商品名：' + titles.get_text())
        print('价格：' + prices.get_text() + '元')
        print('地区：' + acres.get_text())
        print('卖家昵称：' + names.get_text())
        print('卖家头像地址：' + imgs.get('src'))
        info.insert_one({'title':titles.get_text(),'price':prices.get_text(),'acre':acres.get_text(),'name':names.get_text(),'img':imgs.get('src')})
        Download_imgFile(imgs.get('src'),names.get_text())
def Download_imgFile(img_url,name): #用于下载图片
    number = random.random()
    File_path = 'D:/python工程/四周/01-02/img/'+ name + '.jpg'
    Down_image = requests.get(img_url,stream=True)
    try:
        with open(File_path,'wb')as df:
            for chunk in Down_image.iter_content(chunk_size=1024):
                df.write(chunk)
                df.flush()
    except OSError:
        with open('D:/python工程/四周/01-02/img/'+ str(number) + '.jpg','wb')as df:
            for chunk in Down_image.iter_content(chunk_size=1024):
                df.write(chunk)
                df.flush()
