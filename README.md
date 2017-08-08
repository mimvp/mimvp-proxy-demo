
米扑代理示例（mimvp-proxy-demo）
========

米扑代理示例（mimvp-proxy-demo）聚合了多种编程语言使用代理IP，由北京米扑科技有限公司([mimvp.com](http://mimvp.com))原创分享。

米扑代理示例，包含Python、Java、PHP、C#、Go、Perl、Ruby、Shell、NodeJS、PhantomJS、Groovy、Delphi、易语言等十多种编程语言或脚本，通过大量的可运行实例，详细讲解了使用代理IP的正确方法，方便网页爬取、数据采集、自动化测试等领域。

米扑代理示例，测试使用的代理IP，全部来自于米扑代理：<a target="_blank" href="http://proxy.mimvp.com">http://proxy.mimvp.com</a>
        
       
#### 米扑代理示例官网 : <a target="_blank" href="http://proxy.mimvp.com/demo2.php#demo-main-div">http://proxy.mimvp.com/demo2.php</a>
      
  
<br/>     
<br/>     

      
编程语言之代理协议
----------

![代理协议汇总](https://github.com/mimvp/mimvp-proxy-demo/blob/master/cssjs/mimvp-proxy-demo-1-lang-proxy-protocol.png)

![编程语言示例](https://github.com/mimvp/mimvp-proxy-demo/blob/master/cssjs/mimvp-proxy-demo-2-lang-proxy-demo.png)
     
  
<br/>     
<br/>     

     
编程语言之代理示例
----------

#### 1. PHP 设置代理

```php
$proxy_http = "http://138.68.165.154:3128";
$proxy_https = "https://202.53.169.199:3128";
$proxy_socks4 = "socks4://94.158.70.129:1080";
$proxy_socks5 = "socks5://173.230.95.147:45454";

$mimvp_url = "http://proxy.mimvp.com/exist.php";
$mimvp_url2 = "https://proxy.mimvp.com/exist.php";

// curl
proxy_curl($proxy_http, $mimvp_url);		// http
proxy_curl($proxy_https, $mimvp_url);		// https
proxy_curl($proxy_socks4, $mimvp_url);		// socks4
proxy_curl($proxy_socks5, $mimvp_url);		// socks5

// php curl 支持 http、https、socks4、socks5
function proxy_curl($proxy_uri, $mimvp_url) {
	$key = explode('://', $proxy_uri)[0];		// http
	$proxy= explode('://', $proxy_uri)[1];		// ip:port
	echo "proxy_uri :  $proxy_uri; key : $key, proxy : $proxy ";
	
	$ch = curl_init ();
	curl_setopt ( $ch, CURLOPT_URL, $mimvp_url);
	curl_setopt ( $ch, CURLOPT_HTTPPROXYTUNNEL, false );
	curl_setopt ( $ch, CURLOPT_PROXY, $proxy );
	
	if ($key == "http") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTP );		// http
	}
	elseif ($key == "https") {
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYHOST, 2 );	
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYPEER, false );
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTPS );	// https
	}
	elseif ($key == "socks4") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS4 );	// socks4
	}
	elseif ($key == "socks5") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5 );	// socks5
	}
	else {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTP );
	}
	
	curl_setopt ( $ch, CURLOPT_TIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_CONNECTTIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_HEADER, false );
	curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true );	// 返回网页内容
	
	$result = curl_exec ( $ch );
}
```
  
<br/>      
	
	
#### 2. Python 设置代理

```python
proxy_http = {"http":"http://138.68.165.154:3128"}
proxy_https = {"https":"http://191.252.103.93:8080"}
proxy_socks4 = {'socks4': '218.58.52.158:1088'} 
proxy_socks5 = {'socks5': '68.234.190.150:45454'}

mimvp_url = "http://proxy.mimvp.com/exist.php"
mimvp_url2 = "https://proxy.mimvp.com/exist.php"

# 全局取消ssl证书验证，防止打开未验证的https网址抛出异常
# urllib2.URLError: [urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:590)]
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
```
	
<br/>      
	
	
#### 3. Java 设置代理

```java
@SuppressWarnings({ "serial" })
public static HashMap proxyMap = new HashMap() {
	{
		put("http", "138.68.161.14:3128");
		put("https", "104.236.120.183:8080");
		put("socks4", "113.7.118.112:2346");
		put("socks5", "61.135.155.82:1080");
	}
};

final static String proxyUrl = "http://proxy.mimvp.com/exist.php";
final static String proxyUrl2 = "https://proxy.mimvp.com/exist.php";
	
// 设置系统代理，支持全部协议 http，https，socks4，socks5
private static int proxy_property(String proxyType, String proxyStr) {
	int dataLen = 0;

	String proxy_ip = proxyStr.split(":")[0];
	String proxy_port = proxyStr.split(":")[1];
	
	Properties prop = System.getProperties();
	
	// http
	if(proxyType.equals("http")){
		prop.setProperty("http.proxySet", "true");
		prop.setProperty("http.proxyHost", proxy_ip);
		prop.setProperty("http.proxyPort", proxy_port);
		prop.setProperty("http.nonProxyHosts", "localhost|192.168.0.*");
	}
	
	// https
	if (proxyType.equals("https")) {
		prop.setProperty("https.proxyHost", proxy_ip);
		prop.setProperty("https.proxyPort", proxy_port);
	}
    
    // socks
	if(proxyType.equals("socks4") || proxyType.equals("socks5")){
        prop.setProperty("socksProxySet", "true");
        prop.setProperty("socksProxyHost", proxy_ip);
        prop.setProperty("socksProxyPort", proxy_port);
	}
    
    // ftp
	if(proxyType.equals("ftp")){
        prop.setProperty("ftp.proxyHost", proxy_ip);
        prop.setProperty("ftp.proxyPort", proxy_port);
        prop.setProperty("ftp.nonProxyHosts", "localhost|192.168.0.*");
	}
    
//        // auth 设置登录代理服务器的用户名和密码
//        Authenticator.setDefault(new MyAuthenticator("user", "pwd"));
    
	try{
		URL url = new URL(proxyUrl2);		// http://proxy.mimvp.com
		URLConnection conn = url.openConnection();
		conn.setConnectTimeout(30 * 1000);
		
		InputStream in = conn.getInputStream();
		InputStreamReader reader = new InputStreamReader(in);
		char[] ch = new char[1024];
		int len = 0;
		String data = "";
		while((len = reader.read(ch)) > 0) {
			String newData = new String(ch, 0, len);
			data += newData;
		}
		System.out.println("data : " + data);
		dataLen = data.length();
		
	} catch(Exception e) {
		e.printStackTrace();
	}
    return dataLen;
}

static class MyAuthenticator extends Authenticator {
    private String user = "";
    private String password = "";
    public MyAuthenticator(String user, String password) {
        this.user = user;
        this.password = password;
    }
    protected PasswordAuthentication getPasswordAuthentication() {
        return new PasswordAuthentication(user, password.toCharArray());
    }
}
```
 
<br/>      
	
	
#### 4. Shell 设置代理

```sh
#!/bin/bash
#
# curl 支持 http、https、socks4、socks5
# wget 支持 http、https
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
#
# 米扑代理购买：
# http://proxy.mimvp.com
#
# mimvp.com
# 2015-11-09


# http代理格式 		http_proxy=http://IP:Port
# https代理格式 		https_proxy=http://IP:Port

{'http': 'http://120.77.176.179:8888'}
curl -m 30 --retry 3 -x http://120.77.176.179:8888 http://proxy.mimvp.com/exist.php        				# http_proxy
wget -T 30 --tries 3 -e "http_proxy=http://120.77.176.179:8888" http://proxy.mimvp.com/exist.php  		# http_proxy

{'https': 'http://46.105.214.133:3128'}
curl -m 30 --retry 3 --proxy-insecure -x http://46.105.214.133:3128 -k https://proxy.mimvp.com/exist.php        			# https_proxy
wget -T 30 --tries 3 --no-check-certificate -e "https_proxy=http://46.105.214.133:3128" https://proxy.mimvp.com/exist.php	# https_proxy

    
# curl  支持socks
{'socks4': '101.255.17.145:1080'}
curl -m 30 --retry 3 --socks4 101.255.17.145:1080 http://proxy.mimvp.com/exist.php
    
{'socks5': '82.164.233.227:45454'}
curl -m 30 --retry 3 --socks5 82.164.233.227:45454 http://proxy.mimvp.com/exist.php

# wget 不支持socks


################### wget配置文件设置代理 ###################

vim ~/.wgetrc

http_proxy=http://120.77.176.179:8888:8080
https_proxy=http://12.7.17.17:8888:8080
use_proxy = on
wait = 30

wget -T 30 --tries 3 http://proxy.mimvp.com


################### 设置临时局部代理 ###################

# proxy no auth
export http_proxy=http://120.77.176.179:8888:8080
export https_proxy=http://12.7.17.17:8888:8080

# proxy auth
export http_proxy=http://username:password@120.77.176.179:8888:8080
export https_proxy=http://username:password@12.7.17.17:8888:8080


# 取消设置
unset http_proxy
unset https_proxy


################### 设置系统全局代理 ###################

# 修改 /etc/profile，保存并重启服务器
sudo vim /etc/profile		# 所有人有效
或
sudo vim ~/.bashrc			# 所有人有效
或
vim ~/.bash_profile			# 个人有效
	
	
# proxy no auth
export http_proxy=http://120.77.176.179:8888:8080
export https_proxy=http://12.7.17.17:8888:8080

# proxy auth
export http_proxy=http://username:password@120.77.176.179:8888:8080
export https_proxy=http://username:password@12.7.17.17:8888:8080

source /etc/profile
或
source ~/.bashrc
或
source ~/.bash_profile


sudo reboot
```
	
<br/>      
	
	
#### 5. 易语言 设置代理

```php
' 易语言 支持 http
' 
' 米扑代理示例：
' http://proxy.mimvp.com/demo2.php
' 
' 米扑代理购买：
' http://proxy.mimvp.com
' 
' mimvp.com
' 2017-07-28
' 
' 易语言的安装与开发，请参考米扑博客：
' http://blog.mimvp.com/2017/08/yi-yu-yan-de-an-zhuang-yu-kai-fa/
' 
' 易语言的网络编程和代理示例，请参考米扑博客，附有源代码：
' http://blog.mimvp.com/2017/08/yi-yu-yan-de-wang-luo-bian-cheng-he-dai-li-shi-li/


' 变量声明（表格）
.局部变量 代理地址, 文本型
.局部变量 目标网址, 文本型
.局部变量 代理用户名, 文本型
.局部变量 代理密码, 文本型
 
 

' 获取目标网址
.如果 (目标网址编辑框.内容 ＝ “”)
    目标网址 ＝ “http://proxy.mimvp.com/exist.php”
.否则
    目标网址 ＝ 目标网址编辑框.内容
    
' 获取代理地址
.如果 (代理服务器编辑框.内容 ＝ “”)
    代理地址 ＝ “139.59.99.113:8080”
.否则
    代理地址 ＝ 代理服务器编辑框.内容
 
.如果结束
 
输出调试文本 (“代理地址： ” ＋ 代理地址)
 
' 设置代理方法1
网页_置浏览器代理 (代理地址)  ' 通过浏览器设置，一般只支持http代理
超文本浏览框.跳转 (目标网址编辑框.内容, , )
 
 
' 设置代理方法2
输出调试文本 (网页_访问S (目标网址, , , , , , , , , , 代理地址, , ))
 
 
' 设置代理方式3（用户名 +　密码）
输出调试文本 (网页_访问S (目标网址, , , , , , , , , , 代理地址, 代理用户名, 代理密码))
```

![易语言使用代理示例](https://github.com/mimvp/mimvp-proxy-demo/blob/master/cssjs/eyuyan-demo-1.png)

![易语言使用代理示例](https://github.com/mimvp/mimvp-proxy-demo/blob/master/cssjs/eyuyan-demo-2.png)

  
<br/>      
<br/>      
	

注意事项
----------

#### 1. 哪儿可找到代理使用示例里的引用包或依赖库？

解答：米扑代理示例的引用包或依赖库，已经放在了mimvp-proxy-demo开源项目里的目录下了，例如：Python2.7 使用socks4/5是引用了socks.py，已经放在了目录下：https://github.com/mimvp/mimvp-proxy-demo/tree/master/Python2/socks.py

  
<br/>     

#### 2. 如何安装配置编程语言的开发环境？

解答：米扑代理使用示例，全部由米扑科技编写代码、测试验证，因此米扑科技搭建了全部的开发测试环境，详细配置编程语言的开发环境，请参考米扑博客：[http://blog.mimvp.com](http://blog.mimvp.com)

* <a target="_blank" href="http://blog.mimvp.com/2017/09/autohotkey-an-zhuang-yu-kai-fa/">AutoHotkey 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/08/python-scrapy-an-zhuang-yu-kai-fa/">Python scrapy 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/08/python-requests-an-zhuang-yu-kai-fa/">Python requests 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/08/python-pyspider-an-zhuang-yu-kai-fa/">Python pyspider 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/08/python3-urllib-yong-fa-xiang-jie/">Python3 urllib 用法详解</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/10/phantomjs-an-zhuang-yu-kai-fa/">PhantomJS 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/10/phantomjs-selenium-she-zhi-dong-tai-dai-li/">PhantomJS Selenium 设置动态代理</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/10/node-js-an-zhuang-yu-kai-fa/">Node.js 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/10/nodejs-superagent-an-zhuang-yu-kai-fa/">Node.js SuperAgent 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/10/node-js-she-zhi-dai-li-de-liang-zhong-fang-shi-superagent-proxy-he-https-proxy-agent/">Node.js 设置代理的两种方式：superagent-proxy 和 https-proxy-agent</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/ruby-an-zhuang-yu-kai-fa/">Ruby 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/perl-an-zhuang-yu-kai-fa/">Perl 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/delphi-an-zhuang-yu-kai-fa/">Delphi 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/groovy-an-zhuang-yu-kai-fa/">Groovy 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/scala-an-zhuang-yu-kai-fa/">Scala 安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/r-yu-yan-de-an-zhuang-yu-kai-fa/">R语言的安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/go-yu-yan-xia-zai-an-zhuang-pei-zhi-shi-yong/">Go语言下载、安装、配置、使用</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/09/go-yu-yan-zhi-chi-http-httpssocks4socks4asocks5-yi-ji-qian-tao-dai-li/">Go语言支持 http、 https、socks4、socks4a、socks5，以及嵌套代理</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/10/httpie-gong-ju-shi-yong-ru-men/">HTTPie 工具使用入门</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/08/yi-yu-yan-de-an-zhuang-yu-kai-fa/">易语言的安装与开发</a>
* <a target="_blank" href="http://blog.mimvp.com/2017/08/yi-yu-yan-de-wang-luo-bian-cheng-he-dai-li-shi-li/">易语言的网络编程和代理示例</a>

  
<br/>     

#### 3. 代理使用示例里的代理从哪找？

解答：米扑代理使用示例（mimvp-proxy-demo）中的测试代理IP，全部来自米扑代理[http://proxy.mimvp.com](http://proxy.mimvp.com)，其支持http、https、socks4、socks5等全部协议的代理IP，而且米扑代理覆盖全球120多个国家，中国34个省市，代理非常丰富，为全球代理IP领导品牌，推荐！

  
<br/>      
<br/>      
	

米扑科技
----------

![mimvp-logo.png](https://github.com/mimvp/mimvp-proxy-demo/blob/master/cssjs/mimvp-logo.png)

<a href="http://mimvp.com" target="_blank">http://mimvp.com</a>

