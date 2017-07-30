#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Selenium PhantomJS 支持 http、socks5
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2017-01-08


from selenium import webdriver


proxy_http = "http://138.68.165.154:3128"
proxy_socks5 = "socks5://209.151.135.126:11747"

mimvp_url = "http://proxy.mimvp.com/exist.php"
mimvp_url2 = "https://proxy.mimvp.com/exist.php"
mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js"



# urllib2 支持 http, https
def test_http(proxy, mimvp_url):
    
    proxy_type = proxy.split("://")[0]
    proxy_ip = proxy.split("://")[1].split(":")[0]
    proxy_port = int(proxy.split("://")[1].split(":")[1])
    
    # 使用PhantomJS命令，因PhantomJS仅支持http、socks5，所以Selenium Webdriver也只支持http、socks5
    service_args = [
            "--proxy-type=%(http)s" % {"http" : proxy_type},
            "--proxy=%(host)s:%(port)s" % {
                "host" : proxy_ip,
                "port" : proxy_port,
            },
    #         "--proxy-auth=%(user)s:%(pass)s" % {
    #             "user" : 'mimvp-user',
    #             "pass" : 'mimvp-pass',
    #         },
        ]
    
    phantomjs_path = r"/opt/phantomjs-2.1.1/bin/phantomjs"
    
    driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=service_args)
    driver.get(mimvp_url)
    
    print driver.title
    print driver.page_source.encode("utf-8")
    
    driver.quit()      



if __name__ == "__main__":
    # http, socks5
    test_http(proxy_http, mimvp_url)   
    test_http(proxy_socks5, mimvp_url)    
    