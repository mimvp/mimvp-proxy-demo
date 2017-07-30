#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Python2 支持 http、https、socks4、socks5
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2015-11-09


import urllib, urllib2
import socks, socket        # 需要引入socks.py文件，请到米扑代理下载
import ssl

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


proxy_http = {"http"     :  "http://138.68.165.154:3128"}
proxy_https = {"https"   :  "http://191.252.103.93:8080"}
proxy_socks4 = {'socks4' :  '218.58.52.158:1088'} 
proxy_socks5 = {'socks5' :  '68.234.190.150:45454'}

mimvp_url = "http://proxy.mimvp.com/exist.php"
mimvp_url2 = "https://proxy.mimvp.com/exist.php"
mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js"

# 全局取消ssl证书验证，防止打开未验证的https网址抛出异常
# urllib2.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)>
ssl._create_default_https_context = ssl._create_unverified_context
            
            
# urllib2 支持 http, https
def test_http(proxy, mimvp_url):
    handler = urllib2.ProxyHandler(proxy)
    opener = urllib2.build_opener(handler)
    f = opener.open(mimvp_url, timeout=30)
    content = f.read()
    print content
    print len(content)
    f.close()
    opener.close()
    
    
# urllib 支持 http, https
def test_http2(proxy, mimvp_url):
    opener = urllib.FancyURLopener(proxy)
    f = opener.open(mimvp_url)                 #### mimvp_url 只能是http网页，不能是https网页
    content = f.read()
    print content
    print len(content)
    f.close()
    opener.close()
    
    
# socks4
def test_socks4(socks4, mimvp_url):
    socks4_ip = socks4.split(":")[0]
    socks4_port = int(socks4.split(":")[1])
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, socks4_ip, socks4_port)
    socket.socket = socks.socksocket
    
    content = urllib2.urlopen(mimvp_url, timeout=30).read()
    print content
    print len(content)
    
    
# socks5
def test_socks5(socks5, mimvp_url):
    socks5_ip = socks5.split(":")[0]
    socks5_port = int(socks5.split(":")[1])
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, socks5_ip, socks5_port)
    socket.socket = socks.socksocket
    
    content = urllib2.urlopen(mimvp_url, timeout=30).read()
    print content
    print len(content)
    


if __name__ == "__main__":
    # http, https
    test_http(proxy_http, mimvp_url)   
    test_http(proxy_https, mimvp_url2)    
    
    # http
    test_http2(proxy_http, mimvp_url)   
      
    # socks4
    test_socks4(proxy_socks4['socks4'], mimvp_url)
     
    # socks5
    test_socks5(proxy_socks5['socks5'], mimvp_url)
            