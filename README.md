Build Status
功能

系统代理设置
PAC 模式和全局模式
GFWList 和用户规则
支持 HTTP 代理
支持多服务器切换
支持 UDP 代理
下载

下载 最新版。

从 2.5.8 开始你可以在 Releases 页面找到 exe 文件的 hash 值，你可以使用 fciv 等工具 校验 Shadowsocks.exe 文件. 例如 fciv.exe -both -add Shadowsocks.exe

基本使用

在任务栏找到 Shadowsocks 图标
在 服务器 菜单添加多个服务器
选择 启用系统代理 来启用系统代理。请禁用浏览器里的代理插件，或把它们设置为使用系统代理。
除了设为系统代理，你也可以直接自己配置浏览器代理。在 SwitchyOmega 中把代理设置为 SOCKS5 或 HTTP 的 127.0.0.1:1080。这个 1080 端口可以在服务器设置中设置。
PAC

可以编辑 PAC 文件来修改 PAC 设置。Shadowsocks 会监听文件变化，修改后会自动生效。
你也可以从 GFWList （由第三方维护）更新 PAC 文件。
你也可以使用在线 PAC URL
服务器自动切换

负载均衡：随机选择服务器
高可用：根据延迟和丢包率自动选择服务器
累计丢包率：通过定时 ping 来测速和选择。如果要使用本功能，请打开菜单里的统计可用性。
也可以实现 IStrategy 接口来自定义切换规则，然后给我们发一个 pull request。
UDP

对于 UDP，请使用 SocksCap 或 ProxyCap 强制你想使用的程序走代理。

多实例

如果想使用其它工具如 SwitchyOmega 管理多个服务器，可以启动多个 Shadowsocks。 为了避免配置产生冲突，把 Shadowsocks 复制到一个新目录里，并给它设置一个新的本地端口。

全局快捷键

如果重启 Shadowsocks 则必须重新注册，因为此时环境可能发生变化，而且如果多开 Shadowsocks 则需要为后来启动的实例设置不同的快捷键。

怎样键入快捷键?

点击想要设置的快捷键文本框。
按下想要设置的组合键。
当满足要求时释放全部按键。
这时你输入的快捷键字符会出现在文本框中。
如何修改快捷键?

点击想要设置的快捷键文本框。
按下 BackSpace（退格键）清除文本框内容。
重新键入新的组合键。
如何取消激活?

清除你想要取消激活快捷键的文本框内容，如果想要取消全部，则清除全部文本框中的内容。
点击确认按钮。
标签背景色含义

绿色: 此组合键未被其他程序占用，并且成功注册到系统里。
黄色: 此组合键已被其他程序占用，你需要更换其他组合。
透明无色: 初始状态
服务器配置

请访问 服务器 获取更多信息。

绿色模式

如果你想把所有临时文件放在 shadowsocks/temp 目录而不是系统的 temp 目录， 可以在 shadowsocks 所在目录创建一个 shadowsocks_portable_mode.txt 文件。

开发

Visual Studio 2015 & .NET Framework 4.6.2 Developer Pack are required.

授权

GPLv3
