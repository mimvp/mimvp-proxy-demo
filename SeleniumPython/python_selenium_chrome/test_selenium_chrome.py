#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Selenium + Chrome 支持 http、https (无密和加密两种方式)，不支持socks5
#
# 米扑代理示例：
# https://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# https://proxy.mimvp.com
# 
# mimvp.com
# 2017-01-08

# Python + Selenium + Chrome 代理示例，详见米扑博客：
# https://blog.mimvp.com/article/25076.html
#        
# 本示例由米扑代理原创，测试代理来自于米扑代理
# 密码授权和白名单ip设置，请见米扑代理 - 会员中心：https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip


from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
# from xvfbwrapper import Xvfb

import bs4, os, re, time, zipfile
from base64 import b64encode

import sys
from posix import unlink
reload(sys)
sys.setdefaultencoding('utf8')


## webdriver + chrome （不使用代理，爬取网页）
def spider_url_chrome(url):
    browser = None
    display = None
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        chromedriver = '/usr/local/bin/chromedriver'
        browser = webdriver.Chrome(executable_path=chromedriver)        # 打开 Chrome 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()


## webdriver + chrome + proxy + whiteip （无密码，或白名单ip授权）
## 米扑代理：https://proxy.mimvp.com
def spider_url_chrome_by_whiteip(url):
    browser = None
    display = None
    
    ## 白名单ip，请见米扑代理会员中心： https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip
    mimvp_proxy = { 
                    'ip'            : '140.143.62.84',      # ip
                    'port_https'    : 62288,                # http, https
                    'port_socks'    : 62287,                # socks5
                    'username'      : 'mimvp-user',
                    'password'      : 'mimvp-pass'
                  }
    
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        chrome_options = Options()                      # ok
        chrome_options = webdriver.ChromeOptions()      # ok
        proxy_https_argument = '--proxy-server=http://{ip}:{port}'.format(ip=mimvp_proxy['ip'], port=mimvp_proxy['port_https'])     # http, https (无密码，或白名单ip授权，成功)
        chrome_options.add_argument(proxy_https_argument)
#         proxy_socks_argument = '--proxy-server=socks5://{ip}:{port}'.format(ip=mimvp_proxy['ip'], port=mimvp_proxy['port_socks'])   # socks5 (无密码，或白名单ip授权，失败)
#         chrome_options.add_argument(proxy_socks_argument)
        
        chromedriver = '/usr/local/bin/chromedriver'
        browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)        # 打开 Chrome 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()



## webdriver + chrome + proxy + https （https密码授权）
## 米扑代理：https://proxy.mimvp.com
def spider_url_chrome_by_https(url):
    browser = None
    display = None
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        chrome_options = Options()                      # ok
        chrome_options = webdriver.ChromeOptions()      # ok
        chrome_options.add_extension("proxy.zip")      ## 手动打zip包，包含 background.js 和 manifest.json 两个文件
        
        chromedriver = '/usr/local/bin/chromedriver'
        browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)        # 打开 Chrome 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()



## 自动打zip包，包含 background.js 和 manifest.json 两个文件
def get_chrome_proxy_extension(proxy):
    """获取一个Chrome代理扩展,里面配置有指定的代理(带用户名密码认证)
        proxy - 指定的代理,格式: username:password@ip:port
    """
    
    # Chrome代理插件的参考模板 https://github.com/RobinDev/Selenium-Chrome-HTTP-Private-Proxy
    CHROME_PROXY_HELPER_DIR = 'Chrome-proxy-helper'     # 自定义目录名，放在代理项目的当前同一级目录
    
    # 存储自定义Chrome代理扩展文件的目录，一般为当前同一级目录
    # 生成的zip路径为：chrome-proxy-extensions/mimvp-user_mimvp-pass@140.143.62.84_19480.zip
    CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = 'chrome-proxy-extensions'  

    m = re.compile('([^:]+):([^\@]+)\@([\d\.]+):(\d+)').search(proxy)
    if m:
        # 提取代理的各项参数
        username = m.groups()[0]
        password = m.groups()[1]
        ip = m.groups()[2]
        port = m.groups()[3]
        # 创建一个定制Chrome代理扩展(zip文件)
        if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
            os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
        extension_file_path = os.path.join(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR, '{}.zip'.format(proxy.replace(':', '_')))
        
        # 扩展文件不存在，则创建配置文件，并写入zip文件
        if not os.path.exists(extension_file_path):
            zf = zipfile.ZipFile(extension_file_path, mode='w')
            zf.write(os.path.join(CHROME_PROXY_HELPER_DIR, 'manifest.json'), 'manifest.json')
            # 替换模板中的代理参数
            background_content = open(os.path.join(CHROME_PROXY_HELPER_DIR, 'background.js')).read()
            background_content = background_content.replace('mimvp_proxy_host', ip)
            background_content = background_content.replace('mimvp_proxy_port', port)
            background_content = background_content.replace('mimvp_username', username)
            background_content = background_content.replace('mimvp_password', password)
            zf.writestr('background.js', background_content)
            zf.close()
        return extension_file_path
    else:
        raise Exception('Invalid proxy format. Should be username:password@ip:port')


## webdriver + chrome + proxy + https （https密码授权，自动打包zip）
## 米扑代理：https://proxy.mimvp.com
def spider_url_chrome_by_https2(url):
    browser = None
    display = None
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        proxy = 'mimvp-user:mimvp-pass@118.24.232.74:53681'
        proxy_zip = get_chrome_proxy_extension(proxy)   # 打包代理zip文件
        
        chrome_options = Options()                      # ok
        chrome_options = webdriver.ChromeOptions()      # ok
        chrome_options.add_extension(proxy_zip)
        
        chromedriver = '/usr/local/bin/chromedriver'
        browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)        # 打开 Chrome 浏览器
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
        
        unlink(proxy_zip)   # 使用代理后，删除代理zip文件
    finally:
        if browser: browser.quit()
        if display: display.stop()



## webdriver + chrome + proxy + socks （socks密码授权）
## 米扑代理：https://proxy.mimvp.com
def spider_url_chrome_by_socks(url):
    browser = None
    display = None
    
    ## 白名单ip，请见米扑代理会员中心： https://proxy.mimvp.com/usercenter/userinfo.php?p=whiteip
    mimvp_proxy = { 
                    'ip'            : '140.143.62.84',      # ip
                    'port_https'    : 62288,                # http, https
                    'port_socks'    : 62289,                # socks5
                    'username'      : 'mimvp-user',
                    'password'      : 'mimvp-pass'
                  }
    
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        capabilities = dict(DesiredCapabilities.CHROME)
        capabilities['proxy'] = {
                                    'proxyType'    : 'MANUAL',
#                                     'httpProxy'    : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_https']),
#                                     'sslProxy'     : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_https']),
                                    'socksProxy'   : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_socks']),
                                    'ftpProxy'     : mimvp_proxy['ip'] + ":" + str(mimvp_proxy['port_https']),
                                    'noProxy'      : 'localhost,127.0.0.1',
                                    'class'        : "org.openqa.selenium.Proxy",
                                    'autodetect'   : False
                                }
        
        capabilities['proxy']['socksUsername'] = mimvp_proxy['username']
        capabilities['proxy']['socksPassword'] = mimvp_proxy['password']
        
        chromedriver = '/usr/local/bin/chromedriver'
        browser = webdriver.Chrome(chromedriver, desired_capabilities=capabilities)
        browser.get(url)     
        content = browser.page_source
        print("content: " + str(content))
    finally:
        if browser: browser.quit()
        if display: display.stop()



if __name__ == '__main__':
    url = 'https://mimvp.com/'
    url = 'https://proxy.mimvp.com/ip.php'
    
    # 不使用代理，爬取网页
    spider_url_chrome(url)
     
    # 代理无密码，或设置白名单ip，成功
    spider_url_chrome_by_whiteip(url)   
     
    # http, https 密码授权，成功
    spider_url_chrome_by_https(url)
    spider_url_chrome_by_https2(url)
 
    # socks5 密码授权，失败 （仍然是本机ip请求的，不是代理ip请求）
    spider_url_chrome_by_socks(url)
    

