/**
 * Selenum FirefoxDriver 支持 http、socks5
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

import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.firefox.FirefoxProfile;

public class MimvpProxy_FirefoxDriver {

	final static String proxyUri = "103.35.171.77:8080";				// 代理服务器（HTTP, HTTPS）
	final static String proxySocks = "50.63.167.102:18628";				// 代理服务器（Socks5）
	final static String mimvpUrl = "http://proxy.mimvp.com/exist.php";	// 爬取网址
	
//	final static String firefoxBin = "D:/Program Files/Mozilla Firefox/firefox.exe";			// Windows
//	final static String firefoxBin = "/usr/bin/firefox-bin";									// Linux
	final static String firefoxBin = "/Applications/Firefox.app/Contents/MacOS/firefox-bin";	// Mac

	public static void main(String[] args) {
		getNoProxy();
		getHttpProxy();
		getSocksProxy();
	}

	// 不用代理爬取网页
	public static void getNoProxy() {
//		System.setProperty("webdriver.firefox.bin", firefoxBin);	// 不设置也可以
		
		FirefoxProfile profile = new FirefoxProfile();
        
        // 启动Firefox，抓取网页后，再关闭Firefox
        FirefoxDriver driver = new FirefoxDriver(profile);
        driver.get(mimvpUrl);
		String title = driver.getTitle();
		System.out.println(title);			// 检测收录 - 米扑代理
		driver.quit();
		driver.close();
	}

	// HTTP和HTTPS代理爬取网页
	public static void getHttpProxy() {
		FirefoxProfile profile = new FirefoxProfile();
		
		// 设置代理
		profile.setPreference("network.proxy.type", 1);		// 0 - 不用代理； 1 - 使用代理
		profile.setPreference("network.proxy.http", proxyUri.split(":")[0]);
        profile.setPreference("network.proxy.http_port", Integer.parseInt(proxyUri.split(":")[1]));
        profile.setPreference("network.proxy.ssl", proxyUri.split(":")[0]);
        profile.setPreference("network.proxy.ssl_port", Integer.parseInt(proxyUri.split(":")[1]));
        profile.setPreference("network.proxy.no_proxies_on", "localhost");
        
//        // 代理设置用户名和密码，无密码的代理无需配置
//        profile.setPreference("username", "mimvp-user");
//        profile.setPreference("password", "mimvp-pwd");

        FirefoxDriver driver = new FirefoxDriver(profile);
        driver.get(mimvpUrl);
		String title = driver.getTitle();
		System.out.println(title);			// 检测收录 - 米扑代理
		driver.close();
	}

	// Socks5代理爬取网页
	public static void getSocksProxy() {
		FirefoxProfile profile = new FirefoxProfile();
		
		// 设置代理
		profile.setPreference("network.proxy.type", 1);		// 0 - 不用代理； 1 - 使用代理
		profile.setPreference("network.proxy.socks", proxySocks.split(":")[0]);
	    profile.setPreference("network.proxy.socks_port", Integer.parseInt(proxySocks.split(":")[1]));
        profile.setPreference("network.proxy.no_proxies_on", "localhost");

        FirefoxDriver driver = new FirefoxDriver(profile);
        driver.get(mimvpUrl);
		String title = driver.getTitle();
		System.out.println(title);			// 检测收录 - 米扑代理
		driver.close();
	}
}
