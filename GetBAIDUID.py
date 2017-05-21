from GetHome import *
#取得度娘的Cookies值
class GetBAIDUID():
    loadBID =  GetHome()
    url = r'http://www.baidu.com'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063"
    }
    def getID(self):
        self.loadBID.requesHomePage(self.url,self.headers,'Get','utf-8')

