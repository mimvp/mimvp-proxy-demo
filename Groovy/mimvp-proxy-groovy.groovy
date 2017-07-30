/**
 * Groovy 支持 http
 *
 * 米扑代理示例：
 * http://proxy.mimvp.com/demo2.php
 *
 * 米扑代理购买：
 * http://proxy.mimvp.com
 *
 * mimvp.com
 * 2017-07-18
 * 
 * Groovy 爬取网页示例：
 * http://blog.mimvp.com/2017/09/groovy-tong-guo-dai-li-zhua-qu-wang-ye/
 */

 
@Grab(group='org.codehaus.groovy.modules.http-builder', module='http-builder', version='0.7.1' )

import groovyx.net.http.HTTPBuilder
import static groovyx.net.http.ContentType.*
import static groovyx.net.http.Method.*
import org.apache.http.auth.*


class MimvpSpider {
	static def proxy_http = "http://208.92.93.218:1080"
	
	static def mimvp_url = "http://proxy.mimvp.com/exist.php"
	static def mimvp_url2 = "https://proxy.mimvp.com/exist.php"
	

	static main(args) {
		spider_proxy(MimvpSpider.mimvp_url, MimvpSpider.proxy_http)		// http
		spider_proxy(MimvpSpider.mimvp_url2, MimvpSpider.proxy_http)	// https
	}


	static spider_proxy(mimvp_url, proxy) {
		def http = new HTTPBuilder(mimvp_url)

//		http.client.getCredentialsProvider().setCredentials(
//		    new AuthScope("myproxy.com", 8080),
//		    new UsernamePasswordCredentials("proxy-username", "proxy-password")
//		)
		
		def proxy_type = proxy.split("://")[0]
		def proxy_ip = proxy.split("://")[1].split(":")[0]
		def proxy_port = proxy.split("://")[1].split(":")[1]
		proxy_port = proxy_port.toInteger()
		
		println proxy_type
		println proxy_ip
		println proxy_port
		
		
//		http.setProxy('myproxy.com', 8080, 'http')
		http.setProxy(proxy_ip, proxy_port, proxy_type)
		http.ignoreSSLIssues()		// 访问https网站，不需验证， module='http-builder', version='0.7.1'

		http.request( GET, TEXT ){ req ->
			response.success = { resp, reader ->
				println "Response: ${reader.text}"
			}
		}
	}
}



