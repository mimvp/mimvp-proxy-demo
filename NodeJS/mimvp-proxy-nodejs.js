/**
 * NodeJS 支持 http、https、socks4、socks5
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
 * 米扑博客示例详解 : 
 * http://blog.mimvp.com/2017/10/node-js-she-zhi-dai-li-de-liang-zhong-fang-shi-superagent-proxy-he-https-proxy-agent/
 * 
 * proxy-agent		 : https://www.npmjs.com/package/proxy-agent
 * superagent-proxy  : https://www.npmjs.com/package/superagent-proxy
 * http-proxy-agent  : https://www.npmjs.com/package/http-proxy-agent
 * https-proxy-agent : https://www.npmjs.com/package/https-proxy-agent
 * socks-proxy-agent : https://www.npmjs.com/package/socks-proxy-agent
 */

var proxy_http = "http://35.154.138.213:80";
var proxy_https = "http://103.247.154.105:8080";	
var proxy_socks4 = "socks4://202.159.8.243:1080";
var proxy_socks5 = "socks5://94.177.216.47:2016";

var mimvp_url = "http://proxy.mimvp.com/exist.php";
var mimvp_url2 = "https://proxy.mimvp.com/exist.php";
var mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js";



//http for http
function check_http(proxy_uri, mimvp_url) {
	var http = require('http');
	var url = require('url');
	
	console.log("proxy_uri : " + proxy_uri);
	
	var proxy_ip = proxy_uri.toString().split("://")[1].split(":")[0];		// IP
	var proxy_port = proxy_uri.toString().split("://")[1].split(":")[1];	// Port
	
	const options = {
		      host     : proxy_ip,
		      port     : proxy_port,
		      path     : mimvp_url,
		      method   : 'GET',
		      headers : {
		    	  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
		    	  "Host": "apps.bdimg.com",
		    	  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		      }
	};
	
	http
    .request(options, function(res) {
        console.log("got response code: " + res.statusCode);
        if (res.statusCode == 200) {
            res.setEncoding("utf-8");
            var resData = "";
            res.on("data", function(chunk) {
                resData += chunk;
            }).on("end", function() {
                console.log("got response text: " + resData);
            });
        } else {
            console.log("res.statusCode err " + res.statusCode);	// 请求失败
        }
    })
    .on("error", function(err) {
        console.log(err);
    })
    .end();   
};


// request http, https
function check_request(proxy_uri, mimvp_url) {
	var request = require('request');
	
	console.log("proxy_uri : " + proxy_uri);
	
	const proxiedRequest = request.defaults({'proxy': proxy_uri});
	const options = {
		      url     : mimvp_url,
		      headers : {
		    	  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
		    	  "Host": "apps.bdimg.com",
		    	  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		      }
	};
	
	proxiedRequest
    .get(options, function (err, res, body) {
        console.log("got response: " + res.statusCode);
        console.log("got body: " + body);
    })
    .on("error", function (err) {
        console.log(err);
    });          
};


// superagent-proxy http, https
function check_superagent(proxy_uri, mimvp_url) {
	var superagent = require('superagent');
	require('superagent-proxy')(superagent);
	
	console.log("proxy_uri : " + proxy_uri);
	
	superagent
	.get(mimvp_url)
	.proxy(proxy_uri)
	.buffer(true)
	.set('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
	.set('Host','apps.bdimg.com')
	.set('Accept','text/html,application/xhtml+xml,application/xml,application/x-javascript;q=0.9,image/webp,image/apng,*/*;q=0.8')
	.set('Accept-Encoding','gzip, deflate, br')
	.end(function onResponse(err, res) {
		if (err) {
			console.log(err);
		} else {
			console.log(res.status, res.headers);
			console.log(res.text);
		}
	});
};


// https-proxy-agent https
function check_httpsproxyagent(proxy_uri, mimvp_url) {
	var url = require('url');
	var https = require('https');
	var HttpsProxyAgent = require('https-proxy-agent');
	 
	console.log('using proxy server %j', proxy_uri);	// 'https://79.137.80.210:3128'
	
	var agent = new HttpsProxyAgent(proxy_uri);
	var endpoint = process.argv[2] || mimvp_url;
	var options = url.parse(endpoint);
	options.agent = agent;
	options.port = 443;
	options.secureProxy = true;
	
	headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
	"Host": "apps.bdimg.com",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	};
	options.headers = headers;
	console.log('options %j', options);
	 
	https.get(options, function (res) {
	  console.log('"response" event!', res.headers);
	  res.pipe(process.stdout);
	});
}


//socks-proxy-agent socks4, socks5
function check_socksproxyagent(proxy_uri, mimvp_url) {
	var url = require('url');
	var http = require('http');
	var SocksProxyAgent = require('socks-proxy-agent');
	 
	console.log('using proxy server %j', proxy_uri);	// 'socks://94.177.216.47:2016'
	
	var agent = new SocksProxyAgent(proxy_uri);
	var endpoint = process.argv[2] || mimvp_url;
	var options = url.parse(endpoint);
	options.agent = agent;
	options.port = 443;
	options.secureProxy = true;
	
	headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
	"Host": "apps.bdimg.com",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, br",
	};
	options.headers = headers;
	console.log('options %j', options);
	 
	http.get(options, function (res) {
	  console.log('"response" event!', res.headers);
	  res.pipe(process.stdout);
	});
}

// http
check_http(proxy_http, mimvp_url);					// http

// request
check_request(proxy_http, mimvp_url);				// http
check_request(proxy_https, mimvp_url3);				// https

// superagent
check_superagent(proxy_http, mimvp_url);			// http
check_superagent(proxy_https, mimvp_url3);			// https

// https_proxy_agent
check_httpsproxyagent(proxy_https, mimvp_url3);		// https

// socks_proxy_agent
check_socksproxyagent(proxy_socks4, mimvp_url);		// socks4
check_socksproxyagent(proxy_socks5, mimvp_url);		// socks5


// 执行命令：
// cd /usr/local/node/lib/node_modules/npm/
// sudo cp ~/Documents/workspace/MimvpProxyDemo/NodeJS/mimvp-proxy-nodejs.js .
// sudo node mimvp-proxy-nodejs.js | grep '<font color="red">'

