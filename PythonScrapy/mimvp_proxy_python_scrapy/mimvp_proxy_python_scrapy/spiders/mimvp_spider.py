#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Python scrapy 支持 http、https
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2016.10.1

# Python Scrapy 设置代理有两种方式，使用时两种方式选择一种即可
# 方式1： 直接在代码里设置，如 MimvpSpider ——> start_requests
# 方式2： 通过 middlewares.py + settings.py 配置文件设置，步骤：
#        2.1 middlewares.py 添加代理类 ProxyMiddleware，并添加代理
#        2.2 settings.py 开启 DOWNLOADER_MIDDLEWARES，并且添加 'mimvp_proxy_python_scrapy.middlewares.ProxyMiddleware': 100, 


import scrapy
 
class MimvpSpider(scrapy.spiders.Spider):
    name = "mimvp"
    allowed_domains = ["mimvp.com"]
    start_urls = [
        "http://proxy.mimvp.com/exist.php",
        "https://proxy.mimvp.com/exist.php",
    ]
 
    ## 代理设置方式1：直接在代理里设置
    def start_requests(self):
        urls = [
            "http://proxy.mimvp.com/exist.php",
            "https://proxy.mimvp.com/exist.php",
        ]
        for url in urls:
            meta_proxy = ""
            if url.startswith("http://"):
                meta_proxy = "http://180.96.27.12:88"           # http代理
            elif url.startswith("https://"):
                meta_proxy = "http://109.108.87.136:53281"      # https代理
                
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': meta_proxy})


    def parse(self, response):
        mimvp_url = response.url                    # 爬取时请求的url
        body = response.body                        # 返回网页内容
        
        print("mimvp_url : " + str(mimvp_url))
        print("body : " + str(body))
        
#         unicode_body = response.body_as_unicode()   # 返回的html unicode编码
#         print("unicode_body : " + str(unicode_body))
