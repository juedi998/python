58同城多线程信息采集器

概序

本采集程序基于Windows平台python3.5语言开发，适用于Windows All、Linux、MAC平台运行。

构架

本程序采用了python最新爬虫利器：Requests + BeautifulSoup + MongoDB组成，配合multiprocessing多线程技术，使程序跑起来更加省时！

功能

本程序运行后可采集58同城二手栏目处手机号类目以外的信息，并在主目录中创建一个img目录用于存放图片

优势

本程序已捕获了常见的IO错误，如遇到远程拒绝访问、403等，程序会自动进入休眠，时间可自定义，休眠一段时间后再度恢复，再次运行，支持断点续传！

本程序共有四个文件，其中channel为分类连接爬取文件（可省略...）counts文件为统计数据库总数用（可省略....）Muit文件为主程序文件，其它两个文件皆通过它调用，运行本程序前请确保您开启了MongoDB服务，然后再执行Muit文件即可！




