<?php
/**
 * PHP 支持 http、https、socks4、socks5、tcp
 *
 * 米扑代理示例：
 * http://proxy.mimvp.com/demo2.php
 *
 * 米扑代理购买：
 * http://proxy.mimvp.com
 *
 * mimvp.com
 * 2017.5.25
 *
 * CURLOPT_PROXYTYPE :
 * 	CURLPROXY_HTTP,    CURLPROXY_HTTP_1_0
 * 	CURLPROXY_SOCKS4,  CURLPROXY_SOCKS4A
 * 	CURLPROXY_SOCKS5,  CURLPROXY_SOCKS5_HOSTNAME
 */


$proxy_http = "http://138.68.165.154:3128";
$proxy_https = "https://202.53.169.199:3128";
$proxy_socks4 = "socks4://94.158.70.129:1080";
$proxy_socks5 = "socks5://173.230.95.147:45454";

$proxy_tcp = "tcp://138.68.165.154:3128";

$mimvp_url = "http://proxy.mimvp.com/exist.php";
$mimvp_url2 = "https://proxy.mimvp.com/exist.php";
$mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js";


// curl
proxy_curl($proxy_http, $mimvp_url);			// http
proxy_curl($proxy_https, $mimvp_url);		// https
proxy_curl($proxy_socks4, $mimvp_url);		// socks4
proxy_curl($proxy_socks5, $mimvp_url);		// socks5

// stream
proxy_stream($proxy_tcp, $mimvp_url);			// tcp



// php curl 支持 http、https、socks4、socks5
function proxy_curl($proxy_uri, $mimvp_url) {
	$key = explode('://', $proxy_uri)[0];		// http
	$proxy= explode('://', $proxy_uri)[1];		// ip:port
	echo "proxy_uri :  $proxy_uri; key : $key, proxy : $proxy <br>";
	
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
	
	// 打印网页正文
	print_r($result);
	
	// 打印网页大小
	$curl_info = curl_getinfo($ch);
	echo $curl_info['size_download'] . "<br><br>";
	
	curl_close ( $ch );
}



// php stream 支持 tcp
function proxy_stream($proxy_uri, $mimvp_url) {
	
	$key = explode('://', $proxy_uri)[0];		// http
	$proxy= explode('://', $proxy_uri)[1];		// ip:port
	echo "proxy_uri :  $proxy_uri; key : $key, proxy : $proxy <br>";
	
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

?>