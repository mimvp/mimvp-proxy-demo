#!/usr/bin/env ruby
#
# Ruby 支持 http
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2017-03-21


require 'rubygems' 
require 'net/http' 
require 'open-uri' 
require 'timeout' 


mimvp_url = "http://proxy.mimvp.com/exist.php"
mimvp_url2 = "https://proxy.mimvp.com/exist.php"
mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js"

$proxy = '183.222.102.95:8080'

$proxy_addr = $proxy.split(':')[0].strip
$proxy_port = $proxy.split(':')[1].strip

puts $proxy_addr
puts $proxy_port


begin 
  Timeout.timeout(30) {
    
    # mimvp_url = http://proxy.mimvp.com/exist.php
    # uri.host = proxy.mimvp.com
    # uri.port = 80
    # uri.path = /exist.php
    uri = URI.parse(mimvp_url)
    result = Net::HTTP.new(uri.host, nil, $proxy_addr, $proxy_port).start { |http|
      http.get(uri.path)
    }
    puts result.body
  

    # mimvp_url = http://proxy.mimvp.com/exist.php
    # uri.host = proxy.mimvp.com
    # uri.port = 80
    # uri.path = /exist.php
    # req = #<Net::HTTP::Get:0x007fafa594ff78>
    uri = URI.parse(mimvp_url)
    req = Net::HTTP::Get.new(uri.path)
    result = Net::HTTP::Proxy($proxy_addr, $proxy_port).start(uri.host, uri.port) {|http| 
      http.request(req)
    } 
    puts result.body
    
    
#    # proxy auth （NO TEST）
#    $proxy_addr = '<proxy addr>'
#    $proxy_port = '<proxy_port'
#    $proxy_user = '<username>'                # 代理用户名
#    $proxy_pass = '<password>'                # 代理密码
#    
#    $website_username = '<website_username>'  # 目标网站登录用户名
#    $website_password = '<website_password>'  # 目标网站登录密码
#    
#    uri = URI.parse(mimvp_url)
#    req = Net::HTTP::Get.new(uri.path)
#    req.basic_auth($website_username, $website_password)
#    
#    result = Net::HTTP::Proxy($proxy_addr, $proxy_port, $proxy_user, $proxy_pass).start(uri.host, uri.port) {|http| 
#      http.request(req)
#    } 
#    puts result.body
    
}
rescue => e  
    puts e.inspect  
    exit  
end   

## 运行命令： ruby mimvp-proxy-ruby.rb








#require 'net/http'
#
### 方式1
#h = Net::HTTP.new("mimvp.com",80)   # 必须为 mimvp.com，不可以为 http://mimvp.com
#resp,data = h.get("/")
#
#puts data         # 空
#puts resp         # #<Net::HTTPOK:0x007f99e18f2cf8>
#puts resp.body    # 网页正文
#
#
### 方式2
#resp = Net::HTTP.get_response(URI("http://mimvp.com"))  # 必须为 http://mimvp.com，不可以为 mimvp.com
#puts resp         # #<Net::HTTPOK:0x007fe04301a650>
#puts resp.body    # 网页正文  
#
#
### 方式3  运行时需传入参数： ruby mimvp-proxy-ruby.rb mimvp.com
#require 'uri'  
#require 'timeout'  
#require 'net/http'  
#  
#$resp = $data = nil  
#  
#begin  
#    timeout(5) {  
#        $resp = Net::HTTP.new(ARGV[0],80).get("/")                    # 方式1
#        $resp = Net::HTTP.get_response(URI("http://"+ARGV[0]+"/"))    # 方式2
#    }  
#rescue => e  
#    puts e.inspect  
#    exit  
#end   
#puts $resp.body  
#
## 运行命令： ruby mimvp-proxy-ruby.rb mimvp.com


