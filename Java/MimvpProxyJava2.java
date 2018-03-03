/**
 * Java HttpClient 支持 http、https、socks5
 * 
 * HttpClient不是Java JDK默认的类，因此需要添加jar包
 *   HttpClient jar包下载：http://hc.apache.org/downloads.cgi
 *   
 * 米扑代理示例用的引用jar包如下：
 *   commons-codec-1.10.jar
 *   commons-logging-1.2.jar
 *   httpclient-4.5.5.jar
 *   httpcore-4.4.9.jar
 *   
 * 米扑代理，已开源此示例和依赖jar包，上传到了Gitub：
 *   https://github.com/mimvp/mimvp-proxy-demo
 * 
 * 米扑代理示例：
 * https://proxy.mimvp.com/demo2.php
 * 
 * 米扑代理购买：
 * https://proxy.mimvp.com
 * 
 * mimvp.com
 * 2015-11-09
 */


package com.mimvp;

import java.io.IOException;
import java.net.Authenticator;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.PasswordAuthentication;
import java.net.Proxy;
import java.net.Socket;
import java.net.URL;
import java.net.UnknownHostException;
import java.util.HashMap;

import javax.net.ssl.SSLContext;

import org.apache.http.HttpHost;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.HttpClient;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.protocol.HttpClientContext;
import org.apache.http.config.Registry;
import org.apache.http.config.RegistryBuilder;
import org.apache.http.conn.DnsResolver;
import org.apache.http.conn.socket.ConnectionSocketFactory;
import org.apache.http.conn.socket.PlainConnectionSocketFactory;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.DefaultProxyRoutePlanner;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.apache.http.protocol.HttpContext;
import org.apache.http.ssl.SSLContexts;
import org.apache.http.util.EntityUtils;

public class MimvpProxyJava2 {

	@SuppressWarnings({ "serial" })
	public static HashMap<String, String> proxyMap = new HashMap<String, String>() {
		{
			put("http", "138.68.161.14:3128");
			put("https", "39.137.37.8:80");
			put("socks4", "222.83.247.90:1080");
			put("socks5", "111.207.55.16:1080");
		}
	};

	
	public static String PROXY_USERNAME = "username";
	public static String PROXY_PASSWORD = "password";
	@SuppressWarnings({ "serial" })
	public static HashMap<String, String> proxyAuthMap = new HashMap<String, String>() {
		{
			put("http", "120.24.177.37:4821");
			put("https", "120.24.177.37:4821");
			put("socks5", "120.24.177.37:4825");
		}
	};
	
	
	final static String proxyUrl = "http://proxy.mimvp.com/test_proxy2.php";		// http
	final static String proxyUrl2 = "https://proxy.mimvp.com/test_proxy2.php";	// https
	

	// 主入口函数
	public static void main(String args[]){
		// 通过API实时获取米扑代理
		spider_proxy();		
		
		
		// 代理无用户名密码授权
		proxy_no_auth("http", MimvpProxyJava2.proxyMap.get("http"), proxyUrl);				// http（proxy）
		proxy_no_auth("https", MimvpProxyJava2.proxyMap.get("https"), proxyUrl2);				// https（proxy）
		proxy_no_auth2("http", MimvpProxyJava2.proxyMap.get("http"), proxyUrl);				// http（config）
		proxy_no_auth3("http", MimvpProxyJava2.proxyMap.get("http"), proxyUrl);				// http（routePlanner）
		
		proxy_no_auth_socks("socks5", MimvpProxyJava2.proxyMap.get("socks5"), proxyUrl);		// socks5支持访问http网址
		proxy_no_auth_socks("socks5", MimvpProxyJava2.proxyMap.get("socks5"), proxyUrl2);		// socks5支持访问https网址
		
		
		// 代理需要用户名密码授权
		proxy_auth("http", MimvpProxyJava2.proxyAuthMap.get("http"), proxyUrl);		// http
		proxy_auth("https", MimvpProxyJava2.proxyAuthMap.get("https"), proxyUrl2);		// https
		proxy_auth_socks("socks5", MimvpProxyJava2.proxyAuthMap.get("socks5"), proxyUrl);		// socks5支持访问http网址
		proxy_auth_socks("socks5", MimvpProxyJava2.proxyAuthMap.get("socks5"), proxyUrl2);		// socks5支持访问https网址
		
	}
	
	
	// 通过API实时获取米扑代理
	public static void spider_proxy() {
		String proxy_url = "https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=868435221231212345&http_type=3";

		try {
			@SuppressWarnings({ "resource", "deprecation" })		
			HttpClient client = new DefaultHttpClient();					// 舍弃的用法
			CloseableHttpClient client2 = HttpClients.createDefault();	// 推荐的用法
			
			HttpGet request = new HttpGet(proxy_url);
			HttpResponse response = client2.execute(request);
			
			if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				String result = EntityUtils.toString(response.getEntity());

				String[] proxy_list;
				proxy_list = result.split("\n");
				for (String proxy : proxy_list) {
					System.out.println(proxy);
				}
			}
			client2.close();
		} catch (Exception e) {
			System.out.println(e.toString());
		}
	}
	

	
	
	// ############################## 代理无授权 ##############################

	// 方法1：无密代理, 支持 http、https（proxy）
	public static void proxy_no_auth(String proxyType, String proxyIpPort, String webUrl) {
		System.out.println(proxyType + " , " + proxyIpPort + " , " + webUrl);
		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);
		
		try {
			CloseableHttpClient client = HttpClients.createDefault();
			HttpHost proxy = new HttpHost(proxy_ip, proxy_port);
			
			HttpGet request = new HttpGet(webUrl);
			request.addHeader("Host","proxy.mimvp.com");
			request.addHeader("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36");
			
			HttpResponse response = client.execute(proxy, request);
			if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				String result = EntityUtils.toString(response.getEntity());
				System.out.println(result);
			}
			client.close();
		} catch (Exception e) {
			System.out.println(e.toString());
		}
	}
	

	// 方法2：无密代理, 支持 http（config）
	public static void proxy_no_auth2(String proxyType, String proxyIpPort, String webUrl) {
		System.out.println(proxyType + " , " + proxyIpPort + " , " + webUrl);
		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);
		
		try {
			HttpClientBuilder builder = HttpClientBuilder.create();
			CloseableHttpClient client = builder.build();
			
			URL url = new URL(webUrl);
			HttpHost target = new HttpHost(url.getHost(), url.getDefaultPort(), url.getProtocol());
			if(proxyType.equals("https")) {
				target = new HttpHost(url.getHost(), 443, "https");
			}
			HttpHost proxy = new HttpHost(proxy_ip, proxy_port);
			
			RequestConfig config = RequestConfig.custom().setProxy(proxy).build();
			HttpGet request = new HttpGet(url.getPath());
			request.setConfig(config);
			request.addHeader("Host","proxy.mimvp.com");
			request.addHeader("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36");
			
			HttpResponse response = client.execute(target, request);
			if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				String result = EntityUtils.toString(response.getEntity());
				System.out.println(result);
			}
			client.close();
		} catch (Exception e) {
			System.out.println(e.toString());
		}
	}
	

	// 方法3：无密代理, 支持 http（routePlanner）
	public static void proxy_no_auth3(String proxyType, String proxyIpPort, String webUrl) {
		System.out.println(proxyType + " , " + proxyIpPort + " , " + webUrl);
		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);
		
		try {
			HttpHost proxy = new HttpHost(proxy_ip, proxy_port);
			DefaultProxyRoutePlanner routePlanner = new DefaultProxyRoutePlanner(proxy);

			CloseableHttpClient client = HttpClients.custom().setRoutePlanner(routePlanner).build();
			HttpGet request = new HttpGet(webUrl);
			request.addHeader("Host","proxy.mimvp.com");
			request.addHeader("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36");
			
			HttpResponse response = client.execute(request);
			if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				String result = EntityUtils.toString(response.getEntity());
				System.out.println(result);
			}
			client.close();
		} catch (Exception e) {
			System.out.println(e.toString());
		}
	}
	
	
	
	
	// ############################## 代理用户名密码授权 ##############################

	// HttpClient 支持socks5代理的自定义类
	static class MyConnectionSocketFactory extends PlainConnectionSocketFactory {
	    @Override
	    public Socket createSocket(final HttpContext context) throws IOException {
	        InetSocketAddress socksaddr = (InetSocketAddress) context.getAttribute("socks.address");
	        Proxy proxy = new Proxy(Proxy.Type.SOCKS, socksaddr);
	        return new Socket(proxy);
	    }

	    @Override
	    public Socket connectSocket(int connectTimeout, Socket socket, HttpHost host, InetSocketAddress remoteAddress,
	            InetSocketAddress localAddress, HttpContext context) throws IOException {
	        InetSocketAddress unresolvedRemote = InetSocketAddress.createUnresolved(host.getHostName(), remoteAddress.getPort());
	        return super.connectSocket(connectTimeout, socket, host, unresolvedRemote, localAddress, context);
	    }
	}

	static class MySSLConnectionSocketFactory extends SSLConnectionSocketFactory {
	    public MySSLConnectionSocketFactory(final SSLContext sslContext) {
//	        super(sslContext, ALLOW_ALL_HOSTNAME_VERIFIER);
	        super(sslContext);
	    }

	    @Override
	    public Socket createSocket(final HttpContext context) throws IOException {
	        InetSocketAddress socksaddr = (InetSocketAddress) context.getAttribute("socks.address");
	        Proxy proxy = new Proxy(Proxy.Type.SOCKS, socksaddr);
	        return new Socket(proxy);
	    }

	    @Override
	    public Socket connectSocket(int connectTimeout, Socket socket, HttpHost host, InetSocketAddress remoteAddress,
	            InetSocketAddress localAddress, HttpContext context) throws IOException {
	        InetSocketAddress unresolvedRemote = InetSocketAddress.createUnresolved(host.getHostName(), remoteAddress.getPort());
	        return super.connectSocket(connectTimeout, socket, host, unresolvedRemote, localAddress, context);
	    }
	}

	static class FakeDnsResolver implements DnsResolver {
	    @Override
	    public InetAddress[] resolve(String host) throws UnknownHostException {
	        // Return some fake DNS record for every request, we won't be using it
	        return new InetAddress[] { InetAddress.getByAddress(new byte[] { 1, 1, 1, 1 }) };
	    }
	}

	// 无密代理, 支持 socks5
	public static void proxy_no_auth_socks(String proxyType, String proxyIpPort, String webUrl) {
		System.out.println(proxyType + " , " + proxyIpPort + " , " + webUrl);
		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);
		
		try {
			Registry<ConnectionSocketFactory> reg = RegistryBuilder.<ConnectionSocketFactory> create()
		            .register("http", new MyConnectionSocketFactory())
		            .register("https", new MySSLConnectionSocketFactory(SSLContexts.createSystemDefault()))
		            .build();
		    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager(reg, new FakeDnsResolver());
		    CloseableHttpClient client = HttpClients.custom().setConnectionManager(cm).build();
			
			InetSocketAddress addr = new InetSocketAddress(proxy_ip, proxy_port);
			HttpClientContext context = HttpClientContext.create();
			context.setAttribute("socks.address", addr);
			
			HttpGet request = new HttpGet(webUrl);
			request.addHeader("Host","proxy.mimvp.com");
			request.addHeader("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36");
			
			HttpResponse response = client.execute(request, context);
			if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				String result = EntityUtils.toString(response.getEntity());
				System.out.println(result);
			}
		} catch (Exception e) {
			System.out.println(e.toString());
		}
	}
	
	
	
	// 有密代理，需要用户名密码授权，请先取消授权的注释（代码里有注释说明）
	public static void proxy_auth(String proxyType, String proxyIpPort, String webUrl) {
		System.out.println(proxyType + " , " + proxyIpPort + " , " + webUrl);
		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);
		
		CredentialsProvider provider = new BasicCredentialsProvider();
		provider.setCredentials(	new AuthScope(proxy_ip, proxy_port), 
								new UsernamePasswordCredentials(MimvpProxyJava2.PROXY_USERNAME, MimvpProxyJava2.PROXY_PASSWORD));
		
		CloseableHttpClient client = HttpClients.custom().setDefaultCredentialsProvider(provider).build();
		try {
			URL url = new URL(webUrl);
			HttpHost target = new HttpHost(url.getHost(),url.getDefaultPort(),url.getProtocol());
			HttpHost proxy = new HttpHost(proxy_ip, proxy_port);
			
			RequestConfig config = RequestConfig.custom().setProxy(proxy).build();
			HttpGet request = new HttpGet(url.getPath());
			request.setConfig(config);
			request.addHeader("Host","proxy.mimvp.com");
			request.addHeader("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36");
			
			HttpResponse response = client.execute(target, request);
			if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				String result = EntityUtils.toString(response.getEntity());
				System.out.println(result);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}


	// socks5代理的用户名密码授权
	static class MyAuthenticator extends Authenticator {
        private String username = "";
        private String password = "";
        public MyAuthenticator(String username, String password) {
            this.username = username;
            this.password = password;
        }
        protected PasswordAuthentication getPasswordAuthentication() {
            return new PasswordAuthentication(this.username, this.password.toCharArray());
        }
    }
	
	// 有密代理, 支持 socks5
	public static void proxy_auth_socks(String proxyType, String proxyIpPort, String webUrl) {
		System.out.println(proxyType + " , " + proxyIpPort + " , " + webUrl);
		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);

		try {
			Registry<ConnectionSocketFactory> reg = RegistryBuilder.<ConnectionSocketFactory> create()
		            .register("http", new MyConnectionSocketFactory())
		            .register("https", new MySSLConnectionSocketFactory(SSLContexts.createSystemDefault()))
		            .build();
		    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager(reg, new FakeDnsResolver());
		    CloseableHttpClient client = HttpClients.custom().setConnectionManager(cm).build();

			// auth 代理需要用户名密码授权时开启，取消此注释，米扑代理验证通过
			Authenticator.setDefault(new MyAuthenticator(MimvpProxyJava2.PROXY_USERNAME, MimvpProxyJava2.PROXY_PASSWORD));	
			
			InetSocketAddress addr = new InetSocketAddress(proxy_ip, proxy_port);
			HttpClientContext context = HttpClientContext.create();
			context.setAttribute("socks.address", addr);
			
			HttpGet request = new HttpGet(webUrl);
			request.addHeader("Host","proxy.mimvp.com");
			request.addHeader("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36");
			
			HttpResponse response = client.execute(request, context);
			if(response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
				String result = EntityUtils.toString(response.getEntity());
				System.out.println(result);
			}
		} catch (Exception e) {
			System.out.println(e.toString());
		}
	}
}
