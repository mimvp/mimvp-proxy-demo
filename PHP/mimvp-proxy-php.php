<?php
/**
 * PHP 支持 http、https、socks4、socks5、tcp
 *
 * curl不是php原生库，需要安装库:
 * Ubuntu系统：sudo apt-get -y install php5-curl
 * CentOS系统：yum -y install php-curl
 * MacOS 系统：brew install php-curl
 *
 * 米扑代理示例：
 * https://proxy.mimvp.com/demo2.php
 *
 * 米扑代理购买：
 * https://proxy.mimvp.com
 *
 * mimvp.com
 * 2017.5.25
 *
 * CURLOPT_PROXYTYPE :
 * 	CURLPROXY_HTTP,    CURLPROXY_HTTP_1_0
 * 	CURLPROXY_SOCKS4,  CURLPROXY_SOCKS4A
 * 	CURLPROXY_SOCKS5,  CURLPROXY_SOCKS5_HOSTNAME
 */


$mimvp_url = "http://proxy.mimvp.com/test_proxy2.php";		// http
$mimvp_url2 = "https://proxy.mimvp.com/test_proxy2.php";		// https


# 实时爬取米扑代理API接口 (curl)
function spider_proxy_by_curl() {
	$proxy_url = "https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=868435225671251234&http_type=3";
	
	$ch = curl_init ();
	curl_setopt($ch, CURLOPT_URL, $proxy_url);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
	curl_setopt($ch, CURLOPT_TIMEOUT, 30);
	curl_setopt($ch, CURLOPT_HEADER, false);			// 不返回头信息
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);	// 返回网页内容
	
	$result = curl_exec($ch);
	curl_close($ch);
	var_dump($result);
	
	$proxy_list = explode("\n", $result);
	foreach ($proxy_list as $proxy) {
		echo "<br> $proxy";
	}
}



# 实时爬取米扑代理API接口 (stream)
function spider_proxy_by_stream() {
	$proxy_url = "https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=868435225671251234&http_type=3";
	
	$header_array = array(	"Accept-Language:zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
							"Referer:http://proxy.mimvp.com/fetch.php",
							"Host:proxy.mimvp.com",
							"User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36");
	
	$options = array("http" => array(
					"header" => $header_array,
					"method" => "GET")
				);
	
	$context = stream_context_create($options);
	$result = file_get_contents($proxy_url, false, $context);
	var_dump($result);
	
	$proxy_list = explode("\n", $result);
	foreach ($proxy_list as $proxy) {
		echo "<br> $proxy";
	}
}



######################### php curl 支持 http、https、socks4、socks5（代理无密码）#########################

$proxy_http = "http://118.89.57.38:8080";
$proxy_https = "https://39.134.108.92:8080";
$proxy_socks4 = "socks4://59.37.163.176:1080";
$proxy_socks5 = "socks5://183.156.71.161:1080";

function proxy_curl($proxy_uri, $mimvp_url) {
	$proxy_type = explode('://', $proxy_uri)[0];			// http, https, socks4, socks5
	$proxy_ip_port = explode('://', $proxy_uri)[1];		// ip:port
	echo "proxy_uri:  $proxy_uri ;  proxy_type: $proxy_type ,  proxy_ip_port: $proxy_ip_port <br>";
	
	$ch = curl_init ();
	curl_setopt ( $ch, CURLOPT_URL, $mimvp_url);
	curl_setopt ( $ch, CURLOPT_HTTPPROXYTUNNEL, false );
	curl_setopt ( $ch, CURLOPT_PROXY, $proxy_ip_port );
	
	if ($proxy_type == "http") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTP );		// http
	}
	elseif ($proxy_type == "https") {
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYHOST, 2 );
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYPEER, false );			// https
	}
	elseif ($proxy_type == "socks4") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS4 );		// socks4
	}
	elseif ($proxy_type == "socks5") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5 );		// socks5
	}
	
	curl_setopt ( $ch, CURLOPT_TIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_CONNECTTIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_HEADER, false );
	curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true );	// 返回网页内容
	
	$result = curl_exec ( $ch );
	print_r($result);					// 打印网页正文
	
	$curl_info = curl_getinfo($ch);		// 打印网页信息
	var_dump($curl_info);
	echo $curl_info['size_download'] . "<br><br>";
	
	curl_close ( $ch );
}




######################### php curl 支持 http、https、socks5（代理有密码）#########################

$proxy_auth_http = "http://username:password@125.121.168.231:5140";
$proxy_auth_https = "https://username:password@125.121.168.231:5140";
$proxy_auth_socks5 = "socks5://username:password@125.121.168.231:5141";

function proxy_auth_curl($proxy_uri, $mimvp_url) {
	$proxy_type = explode('://', $proxy_uri)[0];			// http, https, socks4, socks5
	$proxy_ip_port = explode('://', $proxy_uri)[1];		// ip:port
	echo "proxy_uri:  $proxy_uri ;  proxy_type: $proxy_type ,  proxy_ip_port: $proxy_ip_port <br>";
	
	$ch = curl_init ();
	curl_setopt ( $ch, CURLOPT_URL, $mimvp_url);
	curl_setopt ( $ch, CURLOPT_HTTPPROXYTUNNEL, false );
	curl_setopt ( $ch, CURLOPT_PROXY, $proxy_ip_port );
	
	if ($proxy_type == "http") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTP );		// http
	}
	elseif ($proxy_type == "https") {
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYHOST, 2 );
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYPEER, false );			// https
	}
	elseif ($proxy_type == "socks5") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5 );		// socks5
	}
	
	curl_setopt ( $ch, CURLOPT_TIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_CONNECTTIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_HEADER, false );
	curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true );	// 返回网页内容
	
	$result = curl_exec ( $ch );
	print_r($result);					// 打印网页正文
	
	$curl_info = curl_getinfo($ch);		// 打印网页信息
	var_dump($curl_info);
	echo $curl_info['size_download'] . "<br><br>";
	
	curl_close ( $ch );
}




######################### php curl 支持 http、https、socks5（代理有密码）#########################

$proxy_noauth_http = "http://125.121.168.231:5140";
$proxy_noauth_https = "https://125.121.168.231:5140";
$proxy_noauth_socks5 = "socks5://125.121.168.231:5141";

$PROXY_USERNAME = 'username';
$PROXY_PASSEORD = 'password';

function proxy_noauth_curl($proxy_uri, $mimvp_url) {
	global $PROXY_USERNAME;
	global $PROXY_PASSEORD;
	
	$proxy_type = explode('://', $proxy_uri)[0];			// http, https, socks4, socks5
	$proxy_ip_port = explode('://', $proxy_uri)[1];		// ip:port
	echo "proxy_uri:  $proxy_uri ;  proxy_type: $proxy_type ,  proxy_ip_port: $proxy_ip_port <br>";
	
	$ch = curl_init ();
	curl_setopt ( $ch, CURLOPT_URL, $mimvp_url);
	curl_setopt ( $ch, CURLOPT_HTTPPROXYTUNNEL, false );
	curl_setopt ( $ch, CURLOPT_PROXY, $proxy_ip_port );
	
	# 设置代理授权
	curl_setopt($ch, CURLOPT_PROXYAUTH, CURLAUTH_BASIC);
	curl_setopt($ch, CURLOPT_PROXYUSERPWD, "{$PROXY_USERNAME}:{$PROXY_PASSEORD}");
	
	if ($proxy_type == "http") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_HTTP );		// http
	}
	elseif ($proxy_type == "https") {
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYHOST, 2 );
		curl_setopt ( $ch, CURLOPT_SSL_VERIFYPEER, false );			// https
	}
	elseif ($proxy_type == "socks5") {
		curl_setopt ( $ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5 );		// socks5
	}
	
	curl_setopt ( $ch, CURLOPT_TIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_CONNECTTIMEOUT, 60 );
	curl_setopt ( $ch, CURLOPT_HEADER, false );
	curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true );	// 返回网页内容
	
	$result = curl_exec ( $ch );
	print_r($result);					// 打印网页正文
	
	$curl_info = curl_getinfo($ch);		// 打印网页信息
	var_dump($curl_info);
	echo $curl_info['size_download'] . "<br><br>";
	
	curl_close ( $ch );
}




######################### php stream 支持 tcp, 含http和https代理 #########################

$proxy_tcp = "tcp://118.89.57.38:8080";				// 支持http
$proxy_tcp = "tcp://39.134.108.92:8080";				// 支持https

function proxy_stream($proxy_uri, $mimvp_url) {
	$proxy_type = explode('://', $proxy_uri)[0];			// http, https
	$proxy_ip_port = explode('://', $proxy_uri)[1];		// ip:port
	echo "proxy_uri:  $proxy_uri ;  proxy_type: $proxy_type ,  proxy_ip_port: $proxy_ip_port <br>";
	
	$header_array = array(	"Accept-Language:zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
							"Referer:http://proxy.mimvp.com/fetch.php",
							"Host:proxy.mimvp.com",
							"User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36");
	
	$options = array("http" => array(
					"proxy"  => $proxy_uri,
					"header" => $header_array,
					"method" => "GET")
			);
	
	$context = stream_context_create($options);
	$result = file_get_contents($mimvp_url, false, $context);
	
	print_r($result);
}


// 通过API获取米扑代理
spider_proxy_by_curl();
spider_proxy_by_stream();


// curl proxy no proxy
proxy_curl($proxy_http, $mimvp_url);			// http
proxy_curl($proxy_https, $mimvp_url);		// https
proxy_curl($proxy_socks4, $mimvp_url);		// socks4
proxy_curl($proxy_socks5, $mimvp_url);		// socks5


// 授权方法1： curl proxy proxy
proxy_auth_curl($proxy_auth_http, $mimvp_url);		// http
proxy_auth_curl($proxy_auth_https, $mimvp_url);		// https
proxy_auth_curl($proxy_auth_socks5, $mimvp_url);		// socks5 访问http
proxy_auth_curl($proxy_auth_socks5, $mimvp_url2);		// socks5 访问https


// 授权方法2： curl proxy proxy
proxy_noauth_curl($proxy_noauth_http, $mimvp_url);		// http
proxy_noauth_curl($proxy_noauth_https, $mimvp_url);		// https
proxy_noauth_curl($proxy_noauth_socks5, $mimvp_url);		// socks5 访问http
proxy_noauth_curl($proxy_noauth_socks5, $mimvp_url2);		// socks5 访问https


// stream
proxy_stream($proxy_tcp, $mimvp_url);		// tcp http
proxy_stream($proxy_tcp, $mimvp_url2);		// tcp https

?>