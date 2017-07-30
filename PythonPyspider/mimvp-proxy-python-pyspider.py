#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Project: mimvp_proxy_pyspider
#
# Python PySpider 支持 http、https
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2017-07-22
#
# 米扑博客示例详解 : 
# http://blog.mimvp.com/2017/08/python-pyspider-an-zhuang-yu-kai-fa/


############  方式1：pyspider crawl_config  ############

from pyspider.libs.base_handler import *

class Handler(BaseHandler):
    crawl_config = {
        'proxy' : 'http://188.226.141.217:8080',     # http
        'proxy' : 'https://182.253.32.65:3128'       # https
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://proxy.mimvp.com/exist.php', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
        
        
        
############  方式2：pyspider --phantomjs-proxy 启动  ############

# $ pyspider --help
# Usage: pyspider [OPTIONS] COMMAND [ARGS]...
# 
#   A powerful spider system in python.
# 
# Options:
#   -c, --config FILENAME           a json file with default values for
#                                   subcommands. {"webui": {"port":5001}}
#   --logging-config TEXT           logging config file for built-in python
#                                   logging module  [default: /Library/Framework
#                                   s/Python.framework/Versions/2.7/lib/python2.
#                                   7/site-packages/pyspider/logging.conf]
#   --debug                         debug mode
#   --queue-maxsize INTEGER         maxsize of queue
#   --taskdb TEXT                   database url for taskdb, default: sqlite
#   --projectdb TEXT                database url for projectdb, default: sqlite
#   --resultdb TEXT                 database url for resultdb, default: sqlite
#   --message-queue TEXT            connection url to message queue, default:
#                                   builtin multiprocessing.Queue
#   --amqp-url TEXT                 [deprecated] amqp url for rabbitmq. please
#                                   use --message-queue instead.
#   --beanstalk TEXT                [deprecated] beanstalk config for beanstalk
#                                   queue. please use --message-queue instead.
#   --phantomjs-proxy TEXT          phantomjs proxy ip:port
#   --data-path TEXT                data dir path
#   --add-sys-path / --not-add-sys-path
#                                   add current working directory to python lib
#                                   search path
#   --version                       Show the version and exit.
#   --help                          Show this message and exit.
   
pyspider --phantomjs-proxy "188.226.141.217:8080" all
