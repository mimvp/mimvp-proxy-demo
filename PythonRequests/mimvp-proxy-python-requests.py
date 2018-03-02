#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Python requests 支持 http、https、socks4、socks5
#
# requests不是Python原生库，需要安装：
#    pip install requests
#    pip install requests[socks]      # requests >= 2.10.0
#
# 米扑代理示例：
# https://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# https://proxy.mimvp.com
# 
# mimvp.com
# 2016-09-16


import requests
import base64
import socks, socket    # 需要引入socks.py文件，请到米扑代理示例下载

# 用于无用户名密码且访问https网址的代理
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context      


mimvp_url = "http://proxy.mimvp.com/test_proxy2.php"        # http
mimvp_url2 = "https://proxy.mimvp.com/test_proxy2.php"      # https
            
            
## proxy no auth （代理无用户名密码验证）
# 使用代理 http, https
proxies = { 
            "http"  : "http://91.121.162.173:80", 
            "https" : "http://190.24.131.250:3128", 
           }   
       
req = requests.get(mimvp_url, proxies=proxies, timeout=30)                  # http
print("mimvp text : " + req.text)
     
req = requests.get(mimvp_url2, proxies=proxies, timeout=30, verify=False)   # https
print("mimvp text : " + req.text)
  
   
  
# 使用代理 socks4
proxies = { 
            'socks4' : '222.83.247.90:1080',
           }   
     
socks4_ip = proxies['socks4'].split(":")[0]
socks4_port = int(proxies['socks4'].split(":")[1])
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, socks4_ip, socks4_port)
socket.socket = socks.socksocket
     
req = requests.get(mimvp_url, timeout=30)                   # http
print("mimvp text : " + req.text)
   
req = requests.get(mimvp_url2, timeout=30, verify=False)    # https
print("mimvp text : " + req.text)
   
   
   
# 方式1：使用代理 socks5
proxies = { 
            'socks5' : '121.40.195.151:9999',
           }   
     
socks5_ip = proxies['socks5'].split(":")[0]
socks5_port = int(proxies['socks5'].split(":")[1])
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks5_ip, socks5_port)
socket.socket = socks.socksocket
     
req = requests.get(mimvp_url, timeout=30)                   # http
print("mimvp text : " + req.text)
   
req = requests.get(mimvp_url2, timeout=30, verify=False)    # https
print("mimvp text : " + req.text)
  
 
 
# 方式2：使用代理 socks5 (需要安装 pip install requests[socks]  且要求 requests >= 2.10.0)
proxies = { 
            "http"  : "socks5://59.78.45.101:1080", 
            "https" : "socks5://59.78.45.101:1080", 
           }   
      
req = requests.get(mimvp_url, proxies=proxies, timeout=30)                  # http
print("mimvp text : " + req.text)
    
req = requests.get(mimvp_url2, proxies=proxies, timeout=30, verify=False)   # https
print("mimvp text : " + req.text)
 
 
 
 
## proxy auth （代理有用户名密码验证）
# 方式1：使用代理 http, https
proxies = { 
            "http"  : "http://username:password@139.199.22.226:4765", 
            "https" : "http://username:password@139.199.22.226:4765", 
           }   
       
req = requests.get(mimvp_url, proxies=proxies, timeout=30)      # http
print("mimvp text : " + req.text)
     
req = requests.get(mimvp_url2, proxies=proxies, timeout=30)     # https
print("mimvp text : " + req.text)
 
 
 
# 方式2：使用代理 http (注意：headers认证，只支持访问http网页，不支持访问https网页)
PROXY_USERNAME = 'username'
PROXY_PASSWORD = 'password'

proxies = { 
            "http"  : "http://111.230.100.182:3712", 
            "https" : "http://111.230.100.182:3712", 
           }   

headers = {
            "Host"                  : "proxy.mimvp.com", 
            "User-Agent"            : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36", 
            "Accept-Encoding"       : "Gzip", 
            "Proxy-Authorization"   : "Basic %s" % base64.b64encode(b'%s:%s' % (PROXY_USERNAME, PROXY_PASSWORD)), 
          }

req = requests.get(mimvp_url, proxies=proxies, headers=headers, timeout=30)      # http (经米扑验证，此方式不支持https)
print("mimvp text : " + req.text)
    
 
 
# 使用代理 socks5 (需要安装 pip install requests[socks]  且要求 requests >= 2.10.0)
proxies = { 
            "http"  : "socks5://username:password@123.53.118.23:1872", 
            "https" : "socks5://username:password@123.53.118.23:1872", 
           }   
       
req = requests.get(mimvp_url, proxies=proxies, timeout=30)                  # http
print("mimvp text : " + req.text)
     
req = requests.get(mimvp_url2, proxies=proxies, timeout=30, verify=False)   # https
print("mimvp text : " + req.text)
 
 
 
 
################### requests 简单示例 ###################
  
# 实时获取米扑代理API接口
mimvp_proxy_url = 'https://proxyapi.mimvp.com/api/fetchopen.php?orderid=863196322034111234'
req = requests.get(url=mimvp_proxy_url, timeout=30)
req_text = req.text
proxy_list = req_text.split("\n")
for proxy in proxy_list:
    print proxy
  
  
# 爬取米扑科技首页
req = requests.get(url = 'https://mimvp.com')
print("status_code : " + str(req.status_code))
print("mimvp text : " + req.text)
    
    
# 爬取米扑代理（含请求参数）
req = requests.get(url='https://proxy.mimvp.com/free.php', params={'proxy':'out_tp','sort':'p_ping'})   
print("status_code : " + str(req.status_code))
print("mimvp text : " + req.text)