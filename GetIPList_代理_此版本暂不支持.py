import requests,re,os,multiprocessing
class GetIPList():
    available = []
    unavailable  = []
    availablefilePath = None
    unavailableFilePath = None
    url = r'http://www.xicidaili.com/wt/{}'
    def requestIP(self,num):
        li = []
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        for item in range(1,num + 1):
            wdata = requests.get(self.url.format(num),headers = headers)
            pearm = r'(?<=<td>)\d+.\d+.\d+.\d+(?=</td>)'
            portPeam = r'(?<=<td>)\d{2,8}(?=</td>)'
            refind = re.findall(pearm,str(wdata.text))
            portfind = re.findall(portPeam,wdata.text)
            for item in range(0,len(refind)):
                li.append(refind[item] + ':' + portfind[item])
        return li
    def textIP(self,ip):
        url = r'http://www.baidu.com'
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        proxies = {"http": "http://{}".format(ip)}
        wdata = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        if (wdata.status_code == 200):
            self.available.append("{},".format(ip))
            print('该ip可用')
        else:
            self.unavailable.append("{},".format(ip))
            print('该ip不可用')


    def checkIPList(self,filePath):
        with open(filePath,'r',encoding='utf-8')as df:
            line = df.readlines()
            tmp = [i.split(',') for i in line]
            return tmp

    def writeIPList(self,filePath,Math):
        if(Math == 'w'):
            with open(filePath,Math,encoding='utf-8')as df:
                df.write(self.available)
        else:
            with open(filePath,Math,encoding= 'utf-8')as df:
                df.write(self.unavailable)

    def checkExist(self,FilePath):
        if(os.path.isfile(FilePath)):
            return True
        else:
            return False




if __name__ =='__main__':
    ipget = GetIPList()
    ipget.availablefilePath = r'ipList.txt'
    ipget.unavailableFilePath = r'unipList.txt'
    if(ipget.checkExist(ipget.availablefilePath)):
        localData = ipget.checkIPList(ipget.availablefilePath)
        for item in localData:
            try:
                ipget.textIP(item)
            except:
                print('质量太差.......')
                pass
    else:
        data = ipget.requestIP(4)
        for item in data:
            try:
                ipget.textIP(item)
            except:
                print('质量太差.......')
                pass
    if (len(ipget.available) < 10):
        print('当前可用ip低于10个，稍后将向服务器请求新的ip资源.....')
        ipget.requestIP(3)
    else:
        ipget.writeIPList(ipget.available, 'w')
        ipget.writeIPList(ipget.unavailable, 'a+')
        print('可用ip更新完毕......')


