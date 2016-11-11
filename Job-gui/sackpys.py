__author__ = 'acer'
#coding: utf-8
import requests,time,urllib
from bs4 import BeautifulSoup
def request(job,aeca):
    title = urllib.parse.quote('工作')
    q = urllib.parse.quote(job)
    l = urllib.parse.quote(aeca)
    url = 'http://cn.indeed.com/%s?q=%s&l=%s' % (title,q,l)
    headers = {
         'Accept': '*/*',
        'Connection':'keep-alive',
        'Host':'cn.indeed.com',
        'Origin':'http://cn.indeed.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }

    data = {
        'q':q,
        'l':l,
    }
    session = requests.session()
    get_job = session.get(url,data=data,headers=headers)
    soup = BeautifulSoup(get_job.text,'lxml')
    gangwei = []
    gongsi = []
    dizi = []
    xinxi = []
    fabu = []
    laiyuan = []
    laiyuan2 =[]
    for i in soup.select('.row'):
        if i.select('.jobtitle') != []:
            #print('招聘岗位：'+ i.select('.jobtitle')[0].text.strip('\n'))
            gangwei.append(i.select('.jobtitle')[0].text.strip('\n'))
        if i.select('.company') != []:
            #print('公司名称：'+ i.select('.company')[0].text.strip())
            gongsi.append(i.select('.company')[0].text.strip())
        if i.select('.location') != []:
           # print('地址：'+ i.select('.location')[0].text.strip('\n'))
            dizi.append(i.select('.location')[0].text.strip('\n'))
       # print(i.select('.summary')[0].text.strip('\n'))
        xinxi.append(i.select('.summary')[0].text.strip('\n'))
        if i.select('.date') != []:
          #  print('发布日期：'+ i.select('.date')[0].text.strip('\n'))
            fabu.append(i.select('.date')[0].text.strip('\n'))
        if i.select('.sdn') != []:
          #  print('信息来源：'+ i.select('.sdn')[0].text.strip('\n'))
            laiyuan.append(i.select('.sdn')[0].text.strip('\n'))
        if i.select('.result-link-source') != []:
         #   print('信息来自：'+ i.select('.result-link-source')[0].text.strip('\n'))
            laiyuan2.append(i.select('.result-link-source')[0].text.strip('\n'))

    return gangwei,gongsi,dizi,xinxi,fabu,laiyuan,laiyuan2
#request('python','广州')