#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Python3 支持 http、https、socks4、socks5
# 
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2016-10-22


import urllib.request   # Python3将urllib和urllib2合二为一，并重组了下包结构
import socket
import socks            # 安装 pip3 install PySocks
import ssl


proxy_http = {"http":"http://183.222.102.98:80"}
proxy_https = {"https":"http://191.252.103.93:8080"}
proxy_socks4 = {'socks4': '186.121.206.241:1080'} 
proxy_socks5 = {'socks5': '68.180.33.124:45454'}

mimvp_url = "http://proxy.mimvp.com/exist.php"
mimvp_url2 = "https://proxy.mimvp.com/exist.php"
mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js"


# 全局取消ssl证书验证，防止打开未验证的https网址抛出异常
# urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:749)>
ssl._create_default_https_context = ssl._create_unverified_context
            
            
# 不用代理，直接爬取网页
def test_url(mimvp_url):
    socket.setdefaulttimeout(30)
    req = urllib.request.Request(mimvp_url)
    content = urllib.request.urlopen(req).read()
    print(content)


# urllib 支持 http, https
def test_http(proxy, mimvp_url):
    socket.setdefaulttimeout(30)
    handler = urllib.request.ProxyHandler(proxy)  
    
#     auth_handler = urllib.request.ProxyBasicAuthHandler()  
#     opener = request.build_opener(handler, auth_handler, request.HTTPHandler)
    
    opener = urllib.request.build_opener(handler)  
    urllib.request.install_opener(opener)
    f = urllib.request.urlopen(mimvp_url)

    content = f.read()
    print(content)
    print(len(content))
    f.close()
    opener.close()


# socks4
def test_socks4(socks4, mimvp_url):
    socks4_ip = socks4.split(":")[0]
    socks4_port = int(socks4.split(":")[1])
    socks.set_default_proxy(socks.SOCKS4, socks4_ip, socks4_port)
    socket.socket = socks.socksocket
    
    content = urllib.request.urlopen(mimvp_url, timeout=30).read()
    print(content)
    print(len(content))
    
    
# socks5
def test_socks5(socks5, mimvp_url):
    socks5_ip = socks5.split(":")[0]
    socks5_port = int(socks5.split(":")[1])
    socks.set_default_proxy(socks.SOCKS5, socks5_ip, socks5_port)
    socket.socket = socks.socksocket
    
    content = urllib.request.urlopen(mimvp_url, timeout=30).read()
    print(content)
    print(len(content))
    


if __name__ == "__main__":
    test_url(mimvp_url)
    
    # http, https
    test_http(proxy_http, mimvp_url)   
    test_http(proxy_https, mimvp_url2)    

    # socks4
    test_socks4(proxy_socks4['socks4'], mimvp_url2)
      
    # socks5
    test_socks5(proxy_socks5['socks5'], mimvp_url2)
            