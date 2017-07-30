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
# 2009.10.1

# Python Scrapy 设置代理有两种方式，使用时两种方式选择一种即可
# 方式1： 直接在代码里设置，如 MimvpSpider ——> start_requests
# 方式2： 通过 middlewares.py + settings.py 配置文件设置，步骤：
#        2.1 middlewares.py 添加代理类 ProxyMiddleware，并添加代理
#        2.2 settings.py 开启 DOWNLOADER_MIDDLEWARES，并且添加 'mimvp_proxy_python_scrapy.middlewares.ProxyMiddleware': 100, 


# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

## 代理设置方式2： 通过 middlewares.py + settings.py 配置文件设置
## mimvp custom by yourself
class ProxyMiddleware(object):
    def process_request(self,request,spider):
    
        if request.url.startswith("http://"):
            request.meta['proxy']="http://180.96.27.12:88"          # http代理
        elif request.url.startswith("https://"):
            request.meta['proxy']="http://109.108.87.136:53281"         # https代理
                
#         # proxy authentication
#         proxy_user_pass = "USERNAME:PASSWORD"
#         encoded_user_pass = base64.encodestring(proxy_user_pass)
#         request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

            
            

class MimvpProxyPythonScrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        
        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
