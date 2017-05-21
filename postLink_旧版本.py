import requests,re,json
from PIL import Image
from tqdm import tqdm
#
#  本程序用于下载百度云盘的文件，注：目前版本仅支持公开分享的文件下载
#  由于度娘限速的原因，我本地测试，最高下载速度仅仅100多KB/S真是坑逼，
#  代码可以任意修改，如果您有更好的方案的话，呵，带密码的版本将在下次更新。
#
class test():
    session = requests.session()
    proxies = {
            'http': 'http://127.0.0.1:8888'
        }
    inputImgNum = None
    vcode = None
    def getBAIDUID_Token(self):#用于获取Cookies
        url = r'https://www.baidu.com'
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
        }
        wdata = self.session.get(url,headers = headers)
        # , proxies = self.proxies, verify = 'FiddlerRoot.pem'
    def getShareLinks(self,url): #用于解析链接，提取相应的参数
        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'pan.baidu.com',
            'Connection': 'Keep-Alive'
        }
        wdata = self.session.get(url,headers = headers,cookies = self.session.cookies)
        wdata.encoding = 'utf-8'
        rePattem = r'(?<=sign":").*?(?=","public")|(?<=timestamp":).*?(?=,"timeline_status")|(?<="bdstoken":).*?(?=,"is_vip)|(?<="uk":).*?(?=,"task_key")|(?<="shareid":).*?(?=,"sign)|(?<="fs_id":).*?(?=,"app_id)'
        refind = re.findall(rePattem,wdata.text)
        #list依次表示：0、fid_list 1、uk 2、bdstoken 3、timestamp 4、primaryid 5、sign
        return refind
    def getZIP(self,data,PostUrl):#获取下载地址接口，真正的下载地址可以在respone里找到
        url = r'https://pan.baidu.com/api/sharedownload?sign={}&timestamp={}&bdstoken={}&channel=chunlei&clienttype=0&web=1&app_id=250528'
        datas = {
            'encrypt':'0',
            'product':'share',
            'uk':data[1],
            'primaryid':data[4],
            'fid_list':"[{}]".format(data[0])
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
            'Referer': PostUrl,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }
        wdata = self.session.post(url.format(data[5],data[3],data[2]),cookies = self.session.cookies,headers = headers,data = datas)
        js = json.loads(wdata.text)
        if(js['errno'] != 0):
            print('当前请求过于频繁，将在输入验证码后继续！')
            self.getVerCode(PostUrl)
        else:
            self.getZIP2(data, link)
    def getVerCode(self,PostUrl): #拉取验证码请求页面，并获取验证码的请求参数
        RequesUrl = r'https://pan.baidu.com/api/getvcode?prod=pan'
        headers = {
            'Host': 'pan.baidu.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'DNT': '1',
            'Referer': PostUrl,
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }
        wdata = self.session.get(RequesUrl,headers = headers,cookies = self.session.cookies)
        wdata.encoding = 'utf-8'
        js = json.loads(wdata.text)
        print(js["vcode"])
        self.vcode = None
        self.vcode = js["vcode"]
        self.requestImg(js["vcode"])
    def requestImg(self,vcode):#下载验证码图片
        url = r'https://pan.baidu.com/genimage?{}'
        wdata = self.session.get(url.format(vcode),headers = self.session.headers,cookies = self.session.cookies,stream=True,verify = self.session.verify)
        with open('img.jpg','wb')as df:
            for check in wdata:
                df.write(check)
        self.opImg()

    def opImg(self):#打开验证码图片
        img = Image.open('img.jpg','r')
        img.show()
        self.inputImgNum = None
        self.inputImgNum = input('请输入验证码：')
        self.getZIP2(data, link)
    #
    #用于转换文件大小的，可以选用
    # def convertBytes(self,bytes, lst=None):
    #     if lst is None:
    #         lst = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    #     i = int(math.floor(  # 舍弃小数点，取小
    #         math.log(bytes, 1024)  # 求对数(对数：若 a**b = N 则 b 叫做以 a 为底 N 的对数)
    #     ))
    #
    #     if i >= len(lst):
    #         i = len(lst) - 1
    #     return ('%.2f' + " " + lst[i]) % (bytes / math.pow(1024, i))

    def getZIP2(self,data,PostUrl): #用于二次判断，因出现验证码界面，导致需要重新访问一次，但第二次需带上验证码的参数，本函数可以与上面的getZIP合并
        url = r'https://pan.baidu.com/api/sharedownload?sign={}&timestamp={}&bdstoken={}&channel=chunlei&clienttype=0&web=1&app_id=250528'
        datas = {
            'encrypt': '0',
            'product': 'share',
            'uk': data[1],
            'primaryid': data[4],
            'fid_list': "[{}]".format(data[0]),
            'vcode_input':self.inputImgNum,
            'vcode_str':self.vcode
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
            'Referer': PostUrl,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }
        wdata = self.session.post(url.format(data[5], data[3], data[2]), cookies=self.session.cookies, headers=headers, data=datas)
        # pattem = r'(?<=md5":").*?(?=","file_key)|(?<=)'
        js = json.loads(wdata.text)
        print("文件下载链接：{}".format(js["list"][0]['dlink']))
        print("文件名：{}".format(js['list'][0]['server_filename']))
        print('文件已经正确解析，正在启动下载中，请耐心等候，这需要较长的时间......')
        self.downZIP(js["list"][0]['dlink'],js['list'][0]['server_filename'])
    def downZIP(self,url,fileName):#下载文件主函数，包括了显示下载的进度条。
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }

        wdata = self.session.get(url,headers = headers,cookies = self.session.cookies,timeout = 50,stream = True)
        total_length = int(wdata.headers.get('Content-Length'))/1024
        with open(fileName,'wb')as df:
            print("总大小：{}/KB".format(total_length))
            for chunk in tqdm(iterable = wdata.iter_content(1024),total = total_length,unit='k'):
                df.write(chunk)
            print('文件下载完毕！')

print('===========================================================')
print('>>>>>>>>>>>>>>>>>欢迎使用机器猫百度云盘下载器<<<<<<<<<<<<<<')
tests = test()
link = input('请输入未加密的分享链接地址：')
tests.getBAIDUID_Token()
print('正在解析文件链接中，请稍后，这需要一定的时间....')
data = tests.getShareLinks(link)
tests.getZIP(data, link)
