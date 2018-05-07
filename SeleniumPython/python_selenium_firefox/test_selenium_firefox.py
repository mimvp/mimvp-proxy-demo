#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Selenium + Firefox 支持 http、https (无密和加密两种方式)，不支持socks5
#
# 米扑代理示例：
# https://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# https://proxy.mimvp.com
# 
# mimvp.com
# 2017-01-08

# Python + Selenium + Firefox 设置密码时，需要使用到两个插件：
# 插件1： modify_headers-0.7.1.1-fx.xpi
# 下载地址：https://github.com/mimvp/mimvp-proxy-demo
#
# 方式2： close_proxy_authentication-1.1.xpi
# 下载地址：https://github.com/mimvp/mimvp-proxy-demo
#       
# Python + Selenium + Firefox 代理示例，详见米扑博客：
# https://blog.mimvp.com/article/25055.html
#         
# 本示例由米扑代理原创，测试代理来自于米扑代理
# 密码授权和白名单ip设置，请见米扑代理 - 会员中心：https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip


from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.proxy import *
from pyvirtualdisplay import Display
# from xvfbwrapper import Xvfb

import bs4, os
from base64 import b64encode

import sys
reload(sys)
sys.setdefaultencoding('utf8')


## webdriver + firefox （不使用代理，爬取网页）
def spider_url_firefox(url):
    browser = None
    display = None
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()       # 打开 FireFox 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()


## webdriver + firefox + proxy + whiteip （无密码，或白名单ip授权）
## 米扑代理：https://proxy.mimvp.com
def spider_url_firefox_by_whiteip(url):
    browser = None
    display = None
    
    ## 白名单ip，请见米扑代理会员中心： https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip
    mimvp_proxy = { 
                    'ip'            : '140.143.62.84',      # ip
                    'port_https'    : 19480,                # http, https
                    'port_socks'    : 19481,                # socks5
                    'username'      : 'mimvp-user',
                    'password'      : 'mimvp-pass'
                  }
    
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        profile = webdriver.FirefoxProfile()
        
        # add proxy
        profile.set_preference('network.proxy.type', 1)     # ProxyType.MANUAL = 1
        if url.startswith("http://"):
            profile.set_preference('network.proxy.http', mimvp_proxy['ip'])
            profile.set_preference('network.proxy.http_port', mimvp_proxy['port_https'])    # 访问http网站
        elif url.startswith("https://"):
            profile.set_preference('network.proxy.ssl', mimvp_proxy['ip'])
            profile.set_preference('network.proxy.ssl_port', mimvp_proxy['port_https'])     # 访问https网站
        else:
            profile.set_preference('network.proxy.socks', mimvp_proxy['ip'])
            profile.set_preference('network.proxy.socks_port', mimvp_proxy['port_socks'])
            profile.set_preference('network.proxy.ftp', mimvp_proxy['ip'])
            profile.set_preference('network.proxy.ftp_port', mimvp_proxy['port_https'])
            profile.set_preference('network.proxy.no_proxies_on', 'localhost,127.0.0.1')
        
        ## 不存在此用法，不能这么设置用户名密码 （舍弃）
#         profile.set_preference("network.proxy.username", 'mimvp-user')
#         profile.set_preference("network.proxy.password", 'mimvp-pass')
    
        profile.update_preferences()
        
        browser = webdriver.Firefox(profile)       # 打开 FireFox 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()


## webdriver + firefox + proxy + https （https密码授权）
## 米扑代理：https://proxy.mimvp.com
def spider_url_firefox_by_https(url):
    browser = None
    display = None
    
    ## 授权密码，请见米扑代理会员中心： https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip
    mimvp_proxy = { 
                    'ip'            : '140.143.62.84',      # ip
                    'port_https'    : 19480,                # http, https
                    'port_socks'    : 19481,                # socks5
                    'username'      : 'mimvp-user',
                    'password'      : 'mimvp-pass'
                  }

    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        profile = webdriver.FirefoxProfile()
        
        # add new header
        profile.add_extension("modify_headers-0.7.1.1-fx.xpi")
        profile.set_preference("extensions.modify_headers.currentVersion", "0.7.1.1-fx")
        profile.set_preference("modifyheaders.config.active", True)
        profile.set_preference("modifyheaders.headers.count", 1)
        profile.set_preference("modifyheaders.headers.action0", "Add")
        profile.set_preference("modifyheaders.headers.name0", "Proxy-Switch-Ip")
        profile.set_preference("modifyheaders.headers.value0", "yes")
        profile.set_preference("modifyheaders.headers.enabled0", True)

        # add proxy
        profile.set_preference('network.proxy.type', 1)     # ProxyType.MANUAL = 1
        if url.startswith("http://"):
            profile.set_preference('network.proxy.http', mimvp_proxy['ip'])
            profile.set_preference('network.proxy.http_port', mimvp_proxy['port_https'])    # 访问http网站
        elif url.startswith("https://"):
            profile.set_preference('network.proxy.ssl', mimvp_proxy['ip'])
            profile.set_preference('network.proxy.ssl_port', mimvp_proxy['port_https'])     # 访问https网站
 
        # Proxy auto login （自动填写密码，进行代理授权）
        profile.add_extension('close_proxy_authentication-1.1.xpi')
        credentials = '{username}:{password}'.format(username=mimvp_proxy['username'], password=mimvp_proxy['password'])    # auth
        credentials = b64encode(credentials.encode('ascii')).decode('utf-8')
        profile.set_preference('extensions.closeproxyauth.authtoken', credentials)

        profile.update_preferences()
        
        browser = webdriver.Firefox(profile)       # 打开 FireFox 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()


## webdriver + firefox + proxy + socks （socks密码授权）
## 米扑代理：https://proxy.mimvp.com
def spider_url_firefox_by_socks(url):
    browser = None
    display = None
    
    ## 授权密码，请见米扑代理会员中心： https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip
    mimvp_proxy = { 
                    'ip'            : '140.143.62.84',      # ip
                    'port_https'    : 62288,                # http, https
                    'port_socks'    : 62287,                # socks5
                    'username'      : 'mimvp-user',
                    'password'      : 'mimvp-pass'
                  }

    proxy_config = Proxy({
                    'proxyType'     : ProxyType.MANUAL,         # 1
                    'httpProxy'     : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_https']),
                    'sslProxy'      : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_https']),
                    'socksProxy'    : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_socks']),
                    'ftpProxy'      : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_https']),
                    'noProxy'       : 'localhost,127.0.0.1',
                    'socksUsername' : mimvp_proxy['username'],
                    'socksPassword' : mimvp_proxy['password'],
                  })
    
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        profile = webdriver.FirefoxProfile()
        
        # add new header
        profile.add_extension("modify_headers-0.7.1.1-fx.xpi")
        profile.set_preference("extensions.modify_headers.currentVersion", "0.7.1.1-fx")
        profile.set_preference("modifyheaders.config.active", True)
        profile.set_preference("modifyheaders.headers.count", 1)
        profile.set_preference("modifyheaders.headers.action0", "Add")
        profile.set_preference("modifyheaders.headers.name0", "Proxy-Switch-Ip")
        profile.set_preference("modifyheaders.headers.value0", "yes")
        profile.set_preference("modifyheaders.headers.enabled0", True)
        
        # auto save auth
        profile.set_preference("signon.autologin.proxy", 'true')
        profile.set_preference("network.websocket.enabled", 'false')
        profile.set_preference('network.proxy.share_proxy_settings', 'false')
        profile.set_preference('network.automatic-ntlm-auth.allow-proxies', 'false')
        profile.set_preference('network.auth.use-sspi', 'false')
        profile.update_preferences()
        
        browser = webdriver.Firefox(proxy=proxy_config, firefox_profile=profile)       # 打开 FireFox 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()


if __name__ == '__main__':
    url = 'https://ip.cn'
    url = 'https://mimvp.com'
    url = 'https://proxy.mimvp.com/ip.php'
    
    # 不使用代理，爬取网页
    spider_url_firefox(url)
     
    # 代理无密码，或设置白名单ip，成功
    spider_url_firefox_by_whiteip(url)
     
    # http, https 密码授权，成功
    spider_url_firefox_by_https(url)

    # socks5 密码授权，失败 （仍然是本机ip请求的，不是代理ip请求）
    spider_url_firefox_by_socks(url)
    

