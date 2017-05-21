from GetHome import *
from  PIL import Image
from tqdm import tqdm
import json,urllib.parse
class GetDownPage():
    loadDownPage = GetHome()
    data = {}
    inputImgNum = None
    vcode = None
    Referer = None
    BDCLND = None
    url = r'https://pan.baidu.com/api/sharedownload?sign={}&timestamp={}&bdstoken={}&channel=chunlei&clienttype=0&web=1&app_id=250528'
    def getDownPage(self,url,data,datas = None):#这里的URL参数用于告诉服务器你已经取得前面网页的许可了
        if(self.loadDownPage.session.cookies.get('BDCLND')):
            self.BDCLND = urllib.parse.unquote(self.loadDownPage.session.cookies['BDCLND'])
            self.data = data
            self.Referer = url
            if datas == None:
                datas = {
                'encrypt': '0',
                'product': 'share',
                'uk': data[1],
                'primaryid': data[4],
                'fid_list': "[{}]".format(data[0]),
                'extra':'{{"sekey":"{}"}}'.format(self.BDCLND)
            }
            else:
                datas = {
                    'encrypt': '0',
                    'product': 'share',
                    'uk': data[1],
                    'primaryid': data[4],
                    'extra':'{{"sekey":"{}"}}'.format(self.BDCLND),
                    'fid_list': "[{}]".format(data[0]),
                    'vcode_input': self.inputImgNum,
                    'vcode_str': self.vcode
                }
        else:
            if datas == None:
                datas = {
                    'encrypt': '0',
                    'product': 'share',
                    'uk': data[1],
                    'primaryid': data[4],
                    'fid_list': "[{}]".format(data[0]),
                }
            else:
                datas = {
                    'encrypt': '0',
                    'product': 'share',
                    'uk': data[1],
                    'primaryid': data[4],
                    'fid_list': "[{}]".format(data[0]),
                    'vcode_input': self.inputImgNum,
                    'vcode_str': self.vcode
                }
        headers = {
            'Host': 'pan.baidu.com',
            'Connection': 'keep-alive',
            'Content-Length': '',
            'Origin': 'https://pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Referer': url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }
        wdata = self.loadDownPage.requesHomePage(self.url.format(data[5],data[3],data[2]),headers,"Post",'utf-8',datas)
        js = json.loads(wdata.text)
        if (js['errno'] != 0):
            return js['errno']
        else:
            return wdata.text

    def getVerCode(self,url):# 获取认证码
        RequesUrl = r'https://pan.baidu.com/api/getvcode?prod=pan'
        headers = {
            'Host': 'pan.baidu.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'DNT': '1',
            'Referer': url,
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }
        wdata = self.loadDownPage.requesHomePage(RequesUrl,headers,'Get','utf-8')
        js = json.loads(wdata.text)
        self.vcode = None
        self.ProcessIMG(js["vcode"])#传送vcode拉取验证码
    def ProcessIMG(self,vcode):
        self.vcode = vcode
        url = r'https://pan.baidu.com/genimage?{}'
        wdata = self.loadDownPage.requesHomePage(url.format(vcode),self.loadDownPage.session.headers,'Get','utf-8')
        with open('img.jpg', 'wb')as df:
            for check in wdata:
                df.write(check)
        self.opImg()#加载图片
    def opImg(self):#打开验证码图片
        img = Image.open('img.jpg','r')
        img.show()
        self.inputImgNum = None
        self.inputImgNum = input('请输入验证码：')

    def DownFile(self,url,fileName,filePath):#下载文件主函数，包括了显示下载的进度条。
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }
        proxies = {"http": 'http://127.0.0.1:8888'}
        wdata = self.loadDownPage.session.get(url,headers=headers,cookies = self.loadDownPage.session.cookies,timeout = 50,stream = True)
        total_length = int(wdata.headers.get('Content-Length')) / 1024
        print("总大小：{}/KB".format(total_length))
        with open(filePath + fileName, 'wb')as df:
            for chunk in tqdm(iterable=wdata.iter_content(1024), total=total_length, unit='k'):
                df.write(chunk)
            print('文件下载完毕！')
        input('按任意键退出程序，感谢您的使用......')
