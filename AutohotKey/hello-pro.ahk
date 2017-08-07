#0::
msgbox, 这是我的第一个AutoHotkey脚本 `n 我爱米扑科技
run, http://mimvp.com
return

#1::
run, http://proxy.mimvp.com/usercenter/login.php
WinActivate, Chrome ;防止窗口不激活
winwait, 米扑代理   ;等待网页加载成功（至少title显示出来）
sleep, 500          ;保险起见，再等0.5秒（视网速）
send, 'mimvp-user'{tab}'mimvp-pwd'{enter}  ;模拟键入米扑代理的登录用户名和密码、回车
return