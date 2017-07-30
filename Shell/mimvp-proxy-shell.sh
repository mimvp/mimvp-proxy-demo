#!/bin/bash
#
# curl 支持 http、https、socks4、socks5
# wget 支持 http、https
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
#
# 米扑代理购买：
# http://proxy.mimvp.com
#
# mimvp.com
# 2015-11-09


# http代理格式 		http_proxy=http://IP:Port
# https代理格式 		https_proxy=http://IP:Port

{'http': 'http://120.77.176.179:8888'}
curl -m 30 --retry 3 -x http://120.77.176.179:8888 http://proxy.mimvp.com/exist.php        				# http_proxy
wget -T 30 --tries 3 -e "http_proxy=http://120.77.176.179:8888" http://proxy.mimvp.com/exist.php  		# http_proxy

{'https': 'http://46.105.214.133:3128'}
curl -m 30 --retry 3 --proxy-insecure -x http://46.105.214.133:3128 -k https://proxy.mimvp.com/exist.php        			# https_proxy
wget -T 30 --tries 3 --no-check-certificate -e "https_proxy=http://46.105.214.133:3128" https://proxy.mimvp.com/exist.php	# https_proxy

    
# curl  支持socks
{'socks4': '101.255.17.145:1080'}
curl -m 30 --retry 3 --socks4 101.255.17.145:1080 http://proxy.mimvp.com/exist.php
    
{'socks5': '82.164.233.227:45454'}
curl -m 30 --retry 3 --socks5 82.164.233.227:45454 http://proxy.mimvp.com/exist.php


# wget 不支持socks




################### wget配置文件设置代理 ###################

vim ~/.wgetrc

http_proxy=http://120.77.176.179:8888:8080
https_proxy=http://12.7.17.17:8888:8080
use_proxy = on
wait = 30

wget -T 30 --tries 3 http://proxy.mimvp.com




################### 设置临时局部代理 ###################

# proxy no auth
export http_proxy=http://120.77.176.179:8888:8080
export https_proxy=http://12.7.17.17:8888:8080

# proxy auth
export http_proxy=http://username:password@120.77.176.179:8888:8080
export https_proxy=http://username:password@12.7.17.17:8888:8080


# 取消设置
unset http_proxy
unset https_proxy




################### 设置系统全局代理 ###################

# 修改 /etc/profile，保存并重启服务器
sudo vim /etc/profile		# 所有人有效
或
sudo vim ~/.bashrc			# 所有人有效
或
vim ~/.bash_profile			# 个人有效
	
	
# proxy no auth
export http_proxy=http://120.77.176.179:8888:8080
export https_proxy=http://12.7.17.17:8888:8080

# proxy auth
export http_proxy=http://username:password@120.77.176.179:8888:8080
export https_proxy=http://username:password@12.7.17.17:8888:8080

source /etc/profile
或
source ~/.bashrc
或
source ~/.bash_profile


sudo reboot
