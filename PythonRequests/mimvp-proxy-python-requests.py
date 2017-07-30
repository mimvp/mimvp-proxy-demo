#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Python requests 支持 http、https、socks4、socks5
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2016-09-16


import requests
import ssl
import socks, socket    # 需要引入socks.py文件，请到米扑代理下载


mimvp_url = "http://proxy.mimvp.com/exist.php"
mimvp_url2 = "https://proxy.mimvp.com/exist.php"
mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js"
            
            
# 使用代理 http, https
proxies = { 
            "http"  : "http://120.77.155.249:8888", 
            "https" : "http://54.255.211.38:80", 
           }   
  
req = requests.get(mimvp_url2, proxies=proxies, timeout=30, verify=False) 
print("mimvp text : " + req.text)



# 使用代理 socks4
proxies = { 
            'socks4' : '163.121.188.2:4000',
           }   
 
socks4_ip = proxies['socks4'].split(":")[0]
socks4_port = int(proxies['socks4'].split(":")[1])
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, socks4_ip, socks4_port)
socket.socket = socks.socksocket
 
req = requests.get(mimvp_url2, timeout=30, verify=False) 
print("mimvp text : " + req.text)



# 使用代理 socks5
proxies = { 
            'socks5' : '190.9.58.211:45454',
           }   
  
socks5_ip = proxies['socks5'].split(":")[0]
socks5_port = int(proxies['socks5'].split(":")[1])
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks5_ip, socks5_port)
socket.socket = socks.socksocket
  
req = requests.get(mimvp_url2, timeout=30, verify=False) 
print("mimvp text : " + req.text)
 
 
 
 
 
 
################### requests 简单示例 ###################
 
# 爬取米扑科技首页
req = requests.get(url = 'http://mimvp.com')
print("status_code : " + str(req.status_code))
print("mimvp text : " + req.text)
  
  
# 爬取米扑代理（含请求参数）
req = requests.get(url='http://proxy.mimvp.com/free.php', params={'proxy':'out_tp','sort':'p_ping'})   
print("status_code : " + str(req.status_code))
print("mimvp text : " + req.text)
