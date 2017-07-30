/**
 * Java 支持 http、https、socks4、socks5
 * 
 * 米扑代理示例：
 * http://proxy.mimvp.com/demo2.php
 * 
 * 米扑代理购买：
 * http://proxy.mimvp.com
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
			put("https", "104.236.120.183:8080");
			put("socks4", "113.7.118.112:2346");
			put("socks5", "61.135.155.82:1080");
		}
	};
	
	final static String proxyUrl = "http://proxy.mimvp.com/exist.php";
	final static String proxyUrl2 = "https://proxy.mimvp.com/exist.php";
	final static String proxyUrl3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js";
	

	// 全局禁止ssl证书验证，防止访问非验证的https网址无法访问，例如：https://mimvp.com
	static {
	    disableSslVerification();
	}

	private static void disableSslVerification() {
	    try
	    {
	        // Create a trust manager that does not validate certificate chains
	        TrustManager[] trustAllCerts = new TrustManager[] {new X509TrustManager() {
	            public java.security.cert.X509Certificate[] getAcceptedIssuers() {
	                return null;
	            }
	            public void checkClientTrusted(X509Certificate[] certs, String authType) {
	            }
	            public void checkServerTrusted(X509Certificate[] certs, String authType) {
	            }
	        }
	        };

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
	
	
	public static void main(String args[]){
		int dataLen = 0;

		// proxy protocol 只支持 http、socks5
		System.out.println("+++++++++ proxy protocol +++++++++");			
		Iterator<String> it = MimvpProxyJava.proxyMap.keySet().iterator();
		while(it.hasNext()){
			String proxyType = it.next();
			String proxyStr = MimvpProxyJava.proxyMap.get(proxyType);
			dataLen = proxy_protocol(proxyType, proxyStr);
			System.out.println(proxyType + " : " + proxyStr + " --> " + dataLen);
		}

		// proxy property 支持http、https、socks4、socks5
		System.out.println("\n+++++++++ proxy property +++++++++");
		Iterator<String> it2 = MimvpProxyJava.proxyMap.keySet().iterator();
		while(it2.hasNext()){
			String proxyType = it2.next();
			String proxyStr = MimvpProxyJava.proxyMap.get(proxyType);
			dataLen = proxy_property(proxyType, proxyStr);
			System.out.println(proxyType + " : " + proxyStr + " --> " + dataLen);
		}

		// proxy socks
		System.out.println("\n++++++++ proxy socks +++++++++++");
		Iterator<String> it3 = MimvpProxyJava.proxyMap.keySet().iterator();
		while(it3.hasNext()){
			String proxyType = it3.next();
			String proxyStr = MimvpProxyJava.proxyMap.get(proxyType);
			dataLen = proxy_socks(proxyType, proxyStr);
			System.out.println(proxyType + " : " + proxyStr + " --> " + dataLen);
		}
	}
	
	
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
	
	
	// 使用函数协议，仅支持 HTTP 和 SOCKS5
	private static int proxy_protocol(String proxyType, String proxyStr){
		int dataLen = 0;

		String proxy_ip = proxyStr.split(":")[0];
		int proxy_port = Integer.parseInt(proxyStr.split(":")[1]);
		
		try{
			URL url = new URL(proxyUrl);		// http://proxy.mimvp.com
			
			InetSocketAddress addr = new InetSocketAddress(proxy_ip, proxy_port);
			Proxy proxy = new Proxy(Proxy.Type.HTTP, addr);
			if(proxyType.equals("socks4") || proxyType.equals("socks5")) {
				proxy = new Proxy(Proxy.Type.SOCKS, addr);
			}
			
			URLConnection conn = url.openConnection(proxy);
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
	
	
	// proxy socket，测试用
	private static int proxy_socks(String proxyType, String proxyStr){
		int dataLen = 0;
		Socket socket = null;
		
		String proxy_ip = proxyStr.split(":")[0];
		int proxy_port = Integer.parseInt(proxyStr.split(":")[1]);
		
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
