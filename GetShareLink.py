from GetHome import *
from GetDownPage import *
import re,json,time

#打开并处理页面，如果分享链接需要密码，则提醒用户需输入密码，否则直接进入下载页面
class GetShareLink():
    loadShareLink = GetHome()
    loadDownPage = GetDownPage()
    ErrorCode = None
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'pan.baidu.com',
        'Connection': 'Keep-Alive'
    }
    def getShareLink(self,url):
        wdata = self.loadShareLink.requesHomePage(url,self.headers,'Get','utf-8')
        if('百度网盘 请输入提取密码' in wdata.text):
            inputPwd = input('该分享链接为非公开共享的链接类型，请输入共享者提供给您的密码：')
            splitPath = wdata.url.split('=')
            sid = splitPath[1].split('&')[0]
            uid = splitPath[2]
            self.verifyCode(sid,uid,inputPwd)
            DescData = self.getDescLink(sid,uid)
            rePattem = r'(?<=sign":").*?(?=","public")|(?<=timestamp":).*?(?=,"timeline_status")|(?<="bdstoken":).*?(?=,"is_vip)|(?<="uk":).*?(?=,"task_key")|(?<="shareid":).*?(?=,"sign)|(?<="fs_id":).*?(?=,"app_id)'
            refind = re.findall(rePattem, DescData.text)
            self.ErrorCode = self.loadDownPage.getDownPage(DescData.url, refind)
            while True:
                if (type(self.ErrorCode) != int):
                    js = json.loads(self.ErrorCode)
                    print("文件下载链接：{}".format(js["list"][0]['dlink']))
                    print("文件名：{}".format(js['list'][0]['server_filename']))
                    print('文件已经正确解析，正在启动下载中，请耐心等候，这需要较长的时间......')
                    filePath = input('请指定文件保存的路径：（格式如：D:\）请务必添加后面的斜杠:')
                    self.loadDownPage.DownFile(js["list"][0]['dlink'],js['list'][0]['server_filename'],filePath)
                    break
                if(self.ErrorCode == -20):
                    print('当前请求过于频繁，需要输入验证码，服务器返回的错误代码为：{}'.format(self.ErrorCode))
                    self.loadDownPage.getVerCode(DescData.url)
                    self.ErrorCode = self.loadDownPage.getDownPage(DescData.url,refind,True)
                else:
                    print('哎呀,本次请求出现异常啦，错误码为：{},将在50秒后重新请求.'.format(self.ErrorCode))
                    time.sleep(50)
                    self.ErrorCode = self.loadDownPage.getDownPage(DescData.url, refind, True)
        else:
            rePattem = r'(?<=sign":").*?(?=","public")|(?<=timestamp":).*?(?=,"timeline_status")|(?<="bdstoken":).*?(?=,"is_vip)|(?<="uk":).*?(?=,"task_key")|(?<="shareid":).*?(?=,"sign)|(?<="fs_id":).*?(?=,"app_id)'
            refind = re.findall(rePattem, wdata.text)
            self.ErrorCode = self.loadDownPage.getDownPage(url,refind,True)
            while True:
                if (type(self.ErrorCode) != int):
                    js = json.loads(self.ErrorCode)
                    print("文件下载链接：{}".format(js["list"][0]['dlink']))
                    print("文件名：{}".format(js['list'][0]['server_filename']))
                    print('文件已经正确解析，正在启动下载中，请耐心等候，这需要较长的时间......')
                    filePath = input('请指定文件保存的路径：（格式如：D:\）请务必添加后面的斜杠:')
                    self.loadDownPage.DownFile(js["list"][0]['dlink'],js['list'][0]['server_filename'],filePath)
                    break
                if(self.ErrorCode == -20):
                    print('当前请求过于频繁，需要输入验证码，服务器返回的错误代码为：{}'.format(self.ErrorCode))
                    self.loadDownPage.getVerCode(url)
                    self.ErrorCode = self.loadDownPage.getDownPage(url,refind,True)
                else:
                    print('哎呀,本次请求出现异常啦，错误码为：{},将在50秒后重新请求.'.format(self.ErrorCode))
                    time.sleep(50)
                    self.ErrorCode = self.loadDownPage.getDownPage(url, refind,True)


    def verifyCode(self,sid,uid,pwd):
        url = r'http://pan.baidu.com/share/verify?shareid={}&uk={}'.format(sid,uid)
        Referer = 'http://pan.baidu.com/share/init?shareid={}&uk={}'.format(sid,uid)
        headers = {
            'Host': 'pan.baidu.com',
            'Connection': 'keep-alive',
            'Content-Length': '',
            'Accept': '*/*',
            'Origin': 'http://pan.baidu.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '',
            'Referer': Referer,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6'
        }
        data = {'pwd':pwd}
        wdata = self.loadShareLink.requesHomePage(url,headers,'Post','utf-8',data)
        js = json.loads(wdata.text)
        if (js['errno'] != 0):
            print('请求失败....错误码为：{}'.format(js['errno']))
        else:
            return True

    def getDescLink(self,sid,uid):
        url = r'http://pan.baidu.com/share/link?shareid={}&uk={}'.format(sid,uid)
        Referer = 'http://pan.baidu.com/share/init?shareid={}&uk={}'.format(sid,uid)
        headers = {
            'Host': 'pan.baidu.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1',
            'Referer': Referer,
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        }
        wdata = self.loadShareLink.requesHomePage(url, headers, 'Get', 'utf-8')
        return wdata



