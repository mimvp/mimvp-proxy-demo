/**
 * Selenum HtmlUnitDriver 支持 http、socks5
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

import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.Platform;
import org.openqa.selenium.Proxy;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.remote.CapabilityType;
import org.openqa.selenium.remote.DesiredCapabilities;

import com.gargoylesoftware.htmlunit.DefaultCredentialsProvider;
import com.gargoylesoftware.htmlunit.WebClient;

public class MimvpProxy_HtmlUnitDriver {
	final static String proxyUri = "183.222.102.98:8080";				// 代理服务器（HTTP）
	final static String proxySocks = "103.14.27.174:1080";				// 代理服务器（Socks5）
	final static String mimvpUrl = "http://proxy.mimvp.com/exist.php";	// 爬取网址

	public static void main(String[] args) {
		getNoProxy();
		getHttpProxy();
		getSocksProxy();
		getAuthProxy();
		getBaiduSearch("米扑科技");
	}

	// 不用代理爬取网页
	public static void getNoProxy() {
		HtmlUnitDriver driver = new HtmlUnitDriver(true);	// enable javascript
		driver.setJavascriptEnabled(true);
		driver.get(mimvpUrl);
		String title = driver.getTitle();
		System.out.println(title);			// 检测收录 - 米扑代理
	}
	
	
	// HTTP代理爬取网页
	public static void getHttpProxy() {
		HtmlUnitDriver driver = new HtmlUnitDriver(true);	// enable javascript
		
		// 方法1
		driver.setProxy(proxyUri.split(":")[0], Integer.parseInt(proxyUri.split(":")[1]));		// proxyUri = "183.222.102.98:8080"
		
		// 方式2
		driver.setHTTPProxy(proxyUri.split(":")[0], Integer.parseInt(proxyUri.split(":")[1]), null);	// proxyUri = "183.222.102.98:8080"

		// 方法3
		Proxy proxy = new Proxy();
		proxy.setHttpProxy(proxyUri);		// 设置代理服务器地址, proxyUri = "183.222.102.98:8080"
		driver.setProxySettings(proxy);
		
		driver.get(mimvpUrl);
		
		String html = driver.getPageSource();
		System.out.println(html);
		String title = driver.getTitle();
		System.out.println(title);			// 检测收录 - 米扑代理
	}

	
	// Socks5代理爬取网页
	public static void getSocksProxy() {
		HtmlUnitDriver driver = new HtmlUnitDriver(true);	// enable javascript
		
		// 方式1
		driver.setSocksProxy(proxySocks.split(":")[0], Integer.parseInt(proxySocks.split(":")[1]));			// proxySocks = "183.239.240.138:1080"
		
		// 方式2
		driver.setSocksProxy(proxySocks.split(":")[0], Integer.parseInt(proxySocks.split(":")[1]), null);	// proxySocks = "183.239.240.138:1080"
		
		driver.get(mimvpUrl);
		
		String html = driver.getPageSource();
		System.out.println(html);
		String title = driver.getTitle();
		System.out.println(title);			// 检测收录 - 米扑代理
	}

	
	// 代理需要用户名和密码
	public static void getAuthProxy() {
		HtmlUnitDriver driver = null;
		
		final String proxyUser = "mimvp-user";
        final String proxyPass = "mimvp-pwd";
        
		Proxy proxy = new Proxy();
		proxy.setHttpProxy(proxyUri);	

		// 设置代理的用户名和密码
		DesiredCapabilities capabilities = DesiredCapabilities.htmlUnit();
		capabilities.setCapability(CapabilityType.PROXY, proxy);
		capabilities.setJavascriptEnabled(true);
		capabilities.setPlatform(Platform.WIN8_1);
		driver = new HtmlUnitDriver(capabilities) {
			@Override
			protected WebClient modifyWebClient(WebClient client) {
				DefaultCredentialsProvider creds = new DefaultCredentialsProvider();
				creds.addCredentials(proxyUser, proxyPass);
				client.setCredentialsProvider(creds);
				return client;
			}
		};
		driver.setJavascriptEnabled(true);	// enable javascript
		driver.get(mimvpUrl);
		String title = driver.getTitle();
		System.out.println(title);			// 检测收录 - 米扑代理
	}

	
	// 进行百度搜索
	public static void getBaiduSearch(String keyword) {
		final String url = "http://www.baidu.com";
		WebDriver driver = new HtmlUnitDriver(false);
		driver.get(url);
		driver.findElement(By.id("kw")).sendKeys(keyword);
		Actions action = new Actions(driver);
		action.sendKeys(Keys.ENTER).perform();
		String html = driver.getPageSource();
		System.out.println(html);
	}
}
