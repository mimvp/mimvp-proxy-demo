#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Python2 支持 http、https、socks4、socks5
#
# 米扑代理示例：
# https://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# https://proxy.mimvp.com
# 
# mimvp.com
# 2015-11-09


import urllib, urllib2
import base64
import socks, socket        # 需要引入socks.py文件，请到米扑代理示例下载

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 全局取消ssl证书验证，防止打开未验证的https网址抛出异常
# urllib2.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)>
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
         
     
mimvp_url = "http://proxy.mimvp.com/test_proxy2.php"
mimvp_url2 = "https://proxy.mimvp.com/test_proxy2.php"
     

# 爬取米扑代理API接口
def spider_proxy():
    proxy_url = 'https://proxyapi.mimvp.com/api/fetchopen.php?orderid=863196312334111234'
    req = urllib2.Request(proxy_url)
    content = urllib2.urlopen(req, timeout=60).read()
    proxy_list = content.split("\n")
    for proxy in proxy_list:
        print proxy
        
           
           
           
################### proxy no auth（代理无用户名密码验证）###################
  
proxy_http = {"http"     :  "http://111.199.144.207:8118"}
proxy_https = {"https"   :  "http://180.173.111.237:9797"}   
proxy_socks4 = {'socks4' :  '218.58.52.158:1088'} 
proxy_socks5 = {'socks5' :  '68.234.190.150:45454'}

# urllib2 支持 http
def test_http(proxy, mimvp_url):
    handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(handler, urllib2.HTTPHandler)     # http
    urllib2.install_opener(opener)
    req = urllib2.Request(mimvp_url)
    content = urllib2.urlopen(req, timeout=60).read()
    print len(content), content
    opener.close()
    
    
# urllib2 支持 https
def test_https(proxy, mimvp_url):
    handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(handler, urllib2.HTTPSHandler)    # https
    urllib2.install_opener(opener)
    req = urllib2.Request(mimvp_url)
    content = urllib2.urlopen(req, timeout=60).read()
    print len(content), content
    opener.close()
    
    
# urllib 支持 http, https
def test_http2(proxy, mimvp_url):
    opener = urllib.FancyURLopener(proxy)
    f = opener.open(mimvp_url)                
    content = f.read()
    print len(content), content
    f.close()
    opener.close()
    
    
# socks4
def test_socks4(socks4, mimvp_url):
    socks4_ip = socks4.split(":")[0]
    socks4_port = int(socks4.split(":")[1])
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, socks4_ip, socks4_port)
    socket.socket = socks.socksocket
    
    content = urllib2.urlopen(mimvp_url, timeout=30).read()
    print len(content), content
    
    
# socks5
def test_socks5(socks5, mimvp_url):
    socks5_ip = socks5.split(":")[0]
    socks5_port = int(socks5.split(":")[1])
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks5_ip, socks5_port)
    socket.socket = socks.socksocket
    
    content = urllib2.urlopen(mimvp_url, timeout=30).read()
    print len(content), content
    



################### proxy auth（代理有用户名密码验证）###################
  
proxy_noauth_http = {"http"     :  "http://120.24.177.37:3363"}
proxy_noauth_https = {"https"   :  "http://120.24.177.37:3363"}   

proxy_auth_http = {"http"     :  "http://username:password@120.24.177.37:3363"}
proxy_auth_https = {"https"   :  "http://username:password@120.24.177.37:3363"}   
proxy_auth_socks5 = {'socks5' :  '120.24.177.37:33634'}

# urllib2 支持 http
def test_auth_http(proxy, mimvp_url):
    handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(handler, urllib2.HTTPHandler)     # http
    urllib2.install_opener(opener)
    req = urllib2.Request(mimvp_url)
    content = urllib2.urlopen(req, timeout=60).read()
    print len(content), content
    opener.close()
    
    
# urllib2 支持 https
def test_auth_https(proxy, mimvp_url):
    handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(handler, urllib2.HTTPSHandler)    # https
    urllib2.install_opener(opener)
    req = urllib2.Request(mimvp_url)
    content = urllib2.urlopen(req, timeout=60).read()
    print len(content), content
    opener.close()
    

# urllib2 headers (注意：headers认证，只支持访问http网页，不支持访问https网页)
def test_auth_headers(proxy, mimvp_url):
    PROXY_USERNAME = 'username'
    PROXY_PASSWORD = 'password'

    proxy_type = ""
    proxy_ip_port = ""
    for proxy_type in proxy:
        proxy_value = proxy.get(proxy_type, '')
        proxy_ip_port = proxy_value.split("://")[1]

    req = urllib2.Request(mimvp_url)
    req.add_header("Proxy-Authorization", "Basic %s" % base64.b64encode(b'%s:%s' % (PROXY_USERNAME, PROXY_PASSWORD)))
    req.set_proxy(proxy_ip_port, proxy_type)
    content = urllib2.urlopen(req, timeout=60).read()
    print len(content), content


# urllib 支持 http, https
def test_auth_http2(proxy, mimvp_url):
    opener = urllib.FancyURLopener(proxy)
    f = opener.open(mimvp_url)                 
    content = f.read()
    print len(content), content
    f.close()
    opener.close()
    
    
# socks5
def test_auth_socks5(socks5, mimvp_url):
    PROXY_USERNAME = 'username'
    PROXY_PASSWORD = 'password'
    
    socks5_ip = socks5.split(":")[0]
    socks5_port = int(socks5.split(":")[1])
    rdns = False #是否在代理服务器上进行dns查询
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks5_ip, socks5_port, rdns, PROXY_USERNAME, PROXY_PASSWORD)
    socket.socket = socks.socksocket
    
    content = urllib2.urlopen(mimvp_url, timeout=30).read()
    print len(content), content
    



if __name__ == "__main__":
    spider_proxy()
     
    # proxy no auth
    test_http(proxy_http, mimvp_url)                    # http
    test_https(proxy_https, mimvp_url2)                 # https
      
    test_http2(proxy_http, mimvp_url)                   # http
    test_http2(proxy_https, mimvp_url2)                 # https
 
    test_socks4(proxy_socks4['socks4'], mimvp_url)      # socks4
    test_socks5(proxy_socks5['socks5'], mimvp_url)      # socks5
            
         
    # proxy auth   
    test_auth_http(proxy_auth_http, mimvp_url)                  # http
    test_auth_https(proxy_auth_https, mimvp_url2)               # https
     
    test_auth_headers(proxy_noauth_http, mimvp_url)             # http （不支持访问https网页）
    
    test_auth_http2(proxy_auth_http, mimvp_url)                 # http
    test_auth_http2(proxy_auth_https, mimvp_url2)               # https
 
    test_auth_socks5(proxy_auth_socks5['socks5'], mimvp_url)    # socks5
            
            
            