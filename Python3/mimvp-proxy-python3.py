#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Python3 支持 http、https、socks4、socks5
#
# Python3使用socks4/5，需安装PySocks
#   pip3 install PySocks
# 
# 米扑代理示例：
# https://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# https://proxy.mimvp.com
# 
# mimvp.com
# 2016-10-22


import urllib.request   # Python3将urllib和urllib2合二为一，并重组了下包结构
import socket
import socks            # 安装 pip3 install PySocks


mimvp_url = "http://proxy.mimvp.com/test_proxy2.php"
mimvp_url2 = "https://proxy.mimvp.com/test_proxy2.php"


# 全局取消ssl证书验证，防止打开未验证的https网址抛出异常
# urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:749)>
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
            
            
# 通过API提供米扑代理
def spider_proxy():
    proxy_url = 'https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=863196312334111234&http_type=3'
    req = urllib.request.Request(proxy_url)
    content = urllib.request.urlopen(req, timeout=30).read()
    proxy_list = content.decode().split("\n")
    for proxy in proxy_list:
        print(proxy)



################### proxy no auth（代理无用户名密码验证）###################
  
proxy_http = {"http"    : "http://47.94.230.42:9999"}
proxy_https = {"https"  : "http://221.180.204.144:80"}
proxy_socks4 = {'socks4': '61.234.37.3:1080'} 
proxy_socks5 = {'socks5': '183.156.71.161:1080'}

# urllib 支持 http, https
def test_http(proxy, mimvp_url):
    socket.setdefaulttimeout(60)
    handler = urllib.request.ProxyHandler(proxy)  
    opener = urllib.request.build_opener(handler)  
    urllib.request.install_opener(opener)
    content = urllib.request.urlopen(mimvp_url, timeout=60).read().decode("utf8")
    print(len(content), content)
    opener.close()


# socks4
def test_socks4(socks4, mimvp_url):
    socks4_ip = socks4.split(":")[0]
    socks4_port = int(socks4.split(":")[1])
    socks.set_default_proxy(socks.SOCKS4, socks4_ip, socks4_port)
    socket.socket = socks.socksocket
    content = urllib.request.urlopen(mimvp_url, timeout=30).read().decode("utf8")
    print(len(content), content)
    
    
# socks5
def test_socks5(socks5, mimvp_url):
    socks5_ip = socks5.split(":")[0]
    socks5_port = int(socks5.split(":")[1])
    socks.set_default_proxy(socks.SOCKS5, socks5_ip, socks5_port)
    socket.socket = socks.socksocket
    content = urllib.request.urlopen(mimvp_url, timeout=30).read().decode("utf8")
    print(len(content), content)
    



################### proxy auth（代理有用户名密码验证）###################
  
proxy_noauth_http = {"http"     :  "http://120.24.77.37:1056"}
proxy_noauth_https = {"https"   :  "http://120.24.77.37:1056"}    
proxy_auth_socks5 = {'socks5'   :  '120.24.177.37:10545'} 

proxy_auth_http = {"http"     :  "http://username:password@120.24.77.37:1056"}
proxy_auth_https = {"https"   :  "http://username:password@120.24.77.37:1056"} 

# urllib 支持 http, https
def test_auth_http(proxy, mimvp_url):
    socket.setdefaulttimeout(30)
    handler = urllib.request.ProxyHandler(proxy)  
    opener = urllib.request.build_opener(handler)  
    urllib.request.install_opener(opener)
    content = urllib.request.urlopen(mimvp_url, timeout=60).read().decode("utf8")
    print(len(content), content)
    opener.close()


# socks5
def test_auth_socks5(socks5, mimvp_url):
    PROXY_USERNAME = 'username'
    PROXY_PASSWORD = 'password'
    
    socks5_ip = socks5.split(":")[0]
    socks5_port = int(socks5.split(":")[1])
    rdns = False        # 是否在代理服务器上进行dns查询
    socks.set_default_proxy(socks.SOCKS5, socks5_ip, socks5_port, rdns, PROXY_USERNAME, PROXY_PASSWORD)
    socket.socket = socks.socksocket
    content = urllib.request.urlopen(mimvp_url, timeout=30).read().decode("utf8")
    print(len(content), content)
    


if __name__ == "__main__":
    spider_proxy()      # 通过API获取米扑代理
    
    # proxy no auth
    test_http(proxy_http, mimvp_url)        # http
    test_http(proxy_https, mimvp_url2)      # https
 
    test_socks4(proxy_socks4['socks4'], mimvp_url)      # socks4 访问http网页
    test_socks4(proxy_socks4['socks4'], mimvp_url2)     # socks4 访问https网页
 
    test_socks5(proxy_socks5['socks5'], mimvp_url)      # socks5 访问http网页
    test_socks5(proxy_socks5['socks5'], mimvp_url2)     # socks5 访问https网页
            
         
    # proxy auth   
    test_auth_http(proxy_auth_http, mimvp_url)                  # http
    test_auth_http(proxy_auth_https, mimvp_url2)                # https
     
    test_auth_socks5(proxy_auth_socks5['socks5'], mimvp_url)    # socks5 访问http网页
    test_auth_socks5(proxy_auth_socks5['socks5'], mimvp_url2)   # socks5 访问https网页
            