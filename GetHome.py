import requests
class GetHome():
    session = requests.session()
    proxies = {"http":'http://127.0.0.1:8888'}
    def requesHomePage(self,url,headers,method,prassCode,data=None):
        if method == 'Get':
            wdata = self.session.get(url,headers=headers,data = data)
            wdata.encoding = prassCode
            return wdata
        else:
            wdata = self.session.post(url, headers=headers, data=data)
            wdata.encoding = prassCode
            return wdata
