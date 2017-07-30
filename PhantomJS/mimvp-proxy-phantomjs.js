/**
 * PhantomJS 支持 http、socks5
 * 
 * 米扑代理示例：
 * http://proxy.mimvp.com/demo2.php
 * 
 * 米扑代理购买：
 * http://proxy.mimvp.com
 * 
 * mimvp.com
 * 2017.5.22
 */

//http代理格式	：	phantomjs --proxy-type=http --proxy=IP:Port
//socks代理格式	：	phantomjs --proxy-type=socks5 --proxy=IP:Port


/**
 $ phantomjs -h  
 --ignore-ssl-errors=            Ignores SSL errors (expired/self-signed certificate errors): 'true' or 'false' (default)
 --proxy=                        Sets the proxy server, e.g. '--proxy=http://proxy.company.com:8080'
 --proxy-auth=                   Provides authentication information for the proxy, e.g. ''-proxy-auth=username:password'
 --proxy-type=                   Specifies the proxy type, 'http' (default), 'none' (disable completely), or 'socks5'
 --script-encoding=              Sets the encoding used for the starting script, default is 'utf8'
 --web-security=                 Enables web security, 'true' (default) or 'false'
 --ssl-protocol=                 Selects a specific SSL protocol version to offer.
 --ssl-ciphers=                  Sets supported TLS/SSL ciphers. 
 --ssl-certificates-path=        Sets the location for custom CA certificates 
 --ssl-client-certificate-file=  Sets the location of a client certificate
 --ssl-client-key-file=          Sets the location of a clients' private key
 --ssl-client-key-passphrase=    Sets the passphrase for the clients' private key
 */


var mimvp_url = "http://proxy.mimvp.com/exist.php";
var mimvp_url2 = "https://proxy.mimvp.com/exist.php";
var mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js";

var page = require('webpage').create();
page.settings.userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36';

page.open(mimvp_url, {}, function(status) { 		// http
//page.open(mimvp_url2, {}, function(status) { 		// socks5
	console.log('status : ' + status);
	if (status == "success") {
		console.log("set proxy success");
		console.log('page.content : ' + page.content);
		console.log('page.content length : ' + page.content.length);
	} else {
		console.log("set proxy fail");
	}
	phantom.exit();
});

// 执行命令：
// http    : phantomjs --proxy-type=http --proxy=23.94.65.132:1080 mimvp-proxy-phantomjs.js
// socks5  : phantomjs --proxy-type=socks5 --proxy=78.63.194.59:35844 --ignore-ssl-errors=true mimvp-proxy-phantomjs.js
