
What is mimvp-proxy-demo ?
----------

米扑代理示例（mimvp-proxy-demo）聚合了多种编程语言使用代理IP，由北京米扑科技有限公司([mimvp.com](http://mimvp.com))原创分享。

米扑代理示例，包含Python、Java、PHP、C#、Go、Perl、Ruby、Shell、NodeJS、PhantomJS、Groovy、Delphi等十多种编程语言或脚本，举证了大量的可运行实例，来讲解使用代理IP的正确方式，方便网页爬取、数据采集、自动化测试等领域。

米扑代理示例，测试使用的代理IP，全部来自于米扑代理：[http://proxy.mimvp.com](http://proxy.mimvp.com)


## 示例：

#### 米扑代理示例官网 : [http://proxy.mimvp.com/demo2.php](http://proxy.mimvp.com/demo2.php#demo-main-div)



编程语言之代理协议
----------

![sitemap.xml 示例](https://github.com/mimvp/mimvp-proxy-demo/blob/master/cssjs/mimvp-proxy-demo-1-lang-proxy-protocol.png)

![sitemap.xml 示例](https://github.com/mimvp/mimvp-proxy-demo/blob/master/cssjs/mimvp-proxy-demo-2-lang-proxy-demo.png)



编程语言之代理示例
----------

1. PHP 设置代理

```php
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

	
2. Python 设置代理

```python
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
```
	
3. Java 设置代理

```java
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

	
4. Shell设置代理

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
	

注意事项
----------

1. 指定


2. 排除


3. 递归

