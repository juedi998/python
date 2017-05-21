import sys
from cx_Freeze import setup, Executable

#自动检测依赖包，可能需要微调
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI 程序需将base设定为：win32gui，windows默认为控制台程序.
base = None
if sys.platform == "win32":
    base = "console"


setup(  name = "BaiduSiper", #自定义
    version = "1.0",#版本号
    description = "百度网盘下载器",#描述
    options = {"build_exe": build_exe_options},
    executables = [Executable("MainAPP.py", base = base)])