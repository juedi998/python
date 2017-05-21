from GetBAIDUID import *
from GetShareLink import *
class MainAPP():
    getBID = GetBAIDUID()
    getShareLink = GetShareLink()
    def Works(self,url):
        self.getBID.getID()
        self.getShareLink.getShareLink(url)

if __name__ == '__main__':
    mainapp = MainAPP()
    print('===========================================================')
    print('>>>>>>>>>>>>>>>>>欢迎使用机器猫百度云盘下载器<<<<<<<<<<<<<<')
    link = input('请输入百度网盘的共享链接（新版已支持加密共享文件下载）：')
    mainapp.Works(link)
    #w8i8