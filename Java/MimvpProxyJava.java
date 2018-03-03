/**
 * Java 支持 http、https、socks4、socks5
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
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Authenticator;
import java.net.InetSocketAddress;
import java.net.PasswordAuthentication;
import java.net.Proxy;
import java.net.Socket;
import java.net.URL;
import java.net.URLConnection;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.X509Certificate;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Properties;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;


public class MimvpProxyJava {

	@SuppressWarnings({ "serial" })
	public static HashMap<String, String> proxyMap = new HashMap<String, String>() {
		{
			put("http", "138.68.161.14:3128");
			put("https", "61.216.1.23:3128");
			put("socks4", "115.238.247.205:1080");
			put("socks5", "122.146.58.135:16405");
		}
	};

	
	public static String PROXY_USERNAME = "username";
	public static String PROXY_PASSWORD = "password";
	@SuppressWarnings({ "serial" })
	public static HashMap<String, String> proxyAuthMap = new HashMap<String, String>() {
		{
			put("http", "120.24.177.37:6474");
			put("https", "120.24.177.37:6474");
			put("socks5", "120.24.177.37:6476");
		}
	};
	
	
	final static String proxyUrl = "http://proxy.mimvp.com/test_proxy2.php";		// http
	final static String proxyUrl2 = "https://proxy.mimvp.com/test_proxy2.php";	// https
	

	// 全局禁止ssl证书验证，防止访问非验证的https网址无法访问，例如：https://mimvp.com
	static {
	    disableSslVerification();
	}

	private static void disableSslVerification() {
	    try {
	        // Create a trust manager that does not validate certificate chains
	        TrustManager[] trustAllCerts = new TrustManager[] { new X509TrustManager() {
	            public java.security.cert.X509Certificate[] getAcceptedIssuers() {
	                return null;
	            }
	            public void checkClientTrusted(X509Certificate[] certs, String authType) {
	            }
	            public void checkServerTrusted(X509Certificate[] certs, String authType) {
	            }
	        }};

	        // Install the all-trusting trust manager
	        SSLContext sc = SSLContext.getInstance("SSL");
	        sc.init(null, trustAllCerts, new java.security.SecureRandom());
	        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());

	        // Create all-trusting host name verifier
	        HostnameVerifier allHostsValid = new HostnameVerifier() {
	            public boolean verify(String hostname, SSLSession session) {
	                return true;
	            }
	        };

	        // Install the all-trusting host verifier
	        HttpsURLConnection.setDefaultHostnameVerifier(allHostsValid);
	    } catch (NoSuchAlgorithmException e) {
	        e.printStackTrace();
	    } catch (KeyManagementException e) {
	        e.printStackTrace();
	    }
	}
	
	
	// 主入口函数
	public static void main(String args[]){
		spider_proxy();		// 通过API实时获取米扑代理
		proxy_no_auth();		// 代理无用户名密码授权
		proxy_auth();		// 代理需要用户名密码授权
	}
	
	
	// 通过API实时获取米扑代理
	public static void spider_proxy() {
		String proxy_url = "https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=868435221231212345&http_type=3";
		
		URL url = null;
		try {
			url = new URL(proxy_url);
			
			URLConnection conn = url.openConnection();
			conn.setDoOutput(true);
			conn.setReadTimeout(30 * 1000);		// 设置超时30秒
			conn.setConnectTimeout(30 * 1000);	// 连接超时30秒
			
			InputStream in = conn.getInputStream();
			InputStreamReader reader = new InputStreamReader(in);
			char[] ch = new char[1024];
			int len = 0;
			String data = "";
			while((len = reader.read(ch)) > 0) {
				String newData = new String(ch, 0, len);
				data += newData;
			}
			
			String[] proxy_list;
			proxy_list = data.split("\n");
			for (String proxy : proxy_list) {
				System.out.println(proxy);
			}
			in.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
	// 使用代理，无用户名密码授权
	public static void proxy_no_auth() {
		int dataLen = 0;

		// proxy protocol 只支持 http、socks5
		dataLen = proxy_protocol("http", MimvpProxyJava.proxyMap.get("http"));		// http
		System.out.println("http : " + MimvpProxyJava.proxyMap.get("http") + " --> " + dataLen);
		
		dataLen = proxy_protocol("socks5", MimvpProxyJava.proxyMap.get("socks5"));	// socks5
		System.out.println("socks5 : " + MimvpProxyJava.proxyMap.get("socks5") + " --> " + dataLen);

		
		// proxy property 支持http、https、socks4、socks5
		Iterator<String> it2 = MimvpProxyJava.proxyMap.keySet().iterator();
		while(it2.hasNext()){
			String proxyType = it2.next();
			String proxyIpPort = MimvpProxyJava.proxyMap.get(proxyType);
			dataLen = proxy_property(proxyType, proxyIpPort);
			System.out.println(proxyType + " : " + proxyIpPort + " --> " + dataLen);
		}

		
		// proxy socks
		Iterator<String> it3 = MimvpProxyJava.proxyMap.keySet().iterator();
		while(it3.hasNext()){
			String proxyType = it3.next();
			String proxyIpPort = MimvpProxyJava.proxyMap.get(proxyType);
			dataLen = proxy_socks(proxyType, proxyIpPort);
			System.out.println(proxyType + " : " + proxyIpPort + " --> " + dataLen);
		}
	}
	
	
	// 使用代理，需要用户名密码授权，请先取消授权的注释（代码里有注释说明）
	public static void proxy_auth() {
		int dataLen = 0;

		// proxy protocol 只支持 http、socks5
		dataLen = proxy_protocol("http", MimvpProxyJava.proxyAuthMap.get("http"));		// http
		System.out.println("http : " + MimvpProxyJava.proxyAuthMap.get("http") + " --> " + dataLen);
		
		dataLen = proxy_protocol("socks5", MimvpProxyJava.proxyAuthMap.get("socks5"));	// socks5
		System.out.println("socks5 : " + MimvpProxyJava.proxyAuthMap.get("socks5") + " --> " + dataLen);

		
		// proxy property 支持http、https、socks4、socks5
		Iterator<String> it2 = MimvpProxyJava.proxyAuthMap.keySet().iterator();
		while(it2.hasNext()){
			String proxyType = it2.next();
			String proxyIpPort = MimvpProxyJava.proxyAuthMap.get(proxyType);
			dataLen = proxy_property(proxyType, proxyIpPort);
			System.out.println(proxyType + " : " + proxyIpPort + " --> " + dataLen);
		}
	}
	
	
	// 设置系统代理，支持全部协议 http，https，socks4，socks5
	private static int proxy_property(String proxyType, String proxyIpPort) {
		int dataLen = 0;

		String proxy_ip = proxyIpPort.split(":")[0];
		String proxy_port = proxyIpPort.split(":")[1];
		
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
		
		// 支持同时代理 http和https 请求
		if (proxyType.equals("http") || proxyType.equals("https")) {
			prop.setProperty("proxyHost", proxy_ip);
			prop.setProperty("proxyPort", proxy_port);
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
        
//        // auth 代理需要用户名和密码授权时开启，取消此注释，米扑代理验证通过
//        Authenticator.setDefault(new MyAuthenticator(MimvpProxyJava.PROXY_USERNAME, MimvpProxyJava.PROXY_PASSWORD));
        
		try{
			URL url = new URL(proxyUrl);			// 默认访问http网页
			if(proxyType.equals("https")) {		// 若为https协议，则访问https网页
				url = new URL(proxyUrl2);
			}
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
			in.close();
			
			System.out.println("data : " + data);
			dataLen = data.length();
		} catch(Exception e) {
			e.printStackTrace();
		}
		prop.clear();	// 清空属性参数，防止下次设置代理时残留脏数据
		prop = null;
		
        return dataLen;
	}
	
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
	
	
	// 使用函数协议，仅支持 HTTP 和 SOCKS5
	private static int proxy_protocol(String proxyType, String proxyIpPort) {
		int dataLen = 0;

		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);
		
		try{
			URL url = new URL(proxyUrl);		// http://proxy.mimvp.com
			
//			// auth 代理需要用户名密码授权时开启，取消此注释，米扑代理验证通过
//			Authenticator.setDefault(new MyAuthenticator(MimvpProxyJava.PROXY_USERNAME, MimvpProxyJava.PROXY_PASSWORD));	
			
			InetSocketAddress addr = new InetSocketAddress(proxy_ip, proxy_port);
			Proxy proxy = new Proxy(Proxy.Type.HTTP, addr);
			if(proxyType.equals("socks4") || proxyType.equals("socks5")) {
				proxy = new Proxy(Proxy.Type.SOCKS, addr);
			}
			
			URLConnection conn = url.openConnection(proxy);
			conn.setConnectTimeout(30 * 1000);	// 连接超时30秒
			
			InputStream in = conn.getInputStream();
			InputStreamReader reader = new InputStreamReader(in);
			char[] ch = new char[1024];
			int len = 0;
			String data = "";
			while((len = reader.read(ch)) > 0) {
				String newData = new String(ch, 0, len);
				data += newData;
			}
			in.close();
			
			System.out.println("data : " + data);
			dataLen = data.length();
		} catch(Exception e) {
			e.printStackTrace();
		}
		return dataLen;
	}
	
	
	// proxy socket，测试用
	private static int proxy_socks(String proxyType, String proxyIpPort) {
		int dataLen = 0;
		Socket socket = null;
		
		String proxy_ip = proxyIpPort.split(":")[0];
		int proxy_port = Integer.parseInt(proxyIpPort.split(":")[1]);
		
		try {
			socket = new Socket(proxy_ip, proxy_port);
			
			byte[] ch = new String("GET http://www.mimvp.com/ HTTP/1.1\r\n\r\n").getBytes();
			socket.getOutputStream().write(ch);
			socket.setSoTimeout(30 * 1000);
			
			byte[] bt = new byte[1024];
			InputStream in = socket.getInputStream();
			int len = 0;
			String data = "";
			while((len = in.read(bt)) > 0) {
				String newData = new String(bt, 0, len);
				data += newData;
			}
			System.out.println("data : " + data);
			dataLen = data.length();
		}catch(Exception e) {
			e.printStackTrace();
		} finally{
			try {
				if(socket != null){
					socket.close();
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
			socket = null;
		}
		return dataLen;
	}
	
	
//	启动运用通过JVM参数走代理, 注意这种代理是全局的,设置以后全部会自动走代理,
//	如果需要单个请求走代理(在走代理失败的话, 会自动尝试本地直接访问), 请使用proxy_protocol()协议代理函数
//	-DproxySet=true
//	-Dhttp.proxyHost=proxyIp
//	-Dhttp.proxyPort=proxyPort
}
