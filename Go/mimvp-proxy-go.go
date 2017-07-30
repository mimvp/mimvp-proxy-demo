/**
* go 支持 http、socks5
*
* 米扑代理示例：
* http://proxy.mimvp.com/demo2.php
*
* 米扑代理购买：
* http://proxy.mimvp.com
*
* mimvp.com
* 2017.6.20
 */

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"

	"golang.org/x/net/proxy"
)

// http（方法1）
func main_1(proxy_uri string, mimvp_url string) {
	proxy := func(_ *http.Request) (*url.URL, error) {
		return url.Parse(proxy_uri)
	}
	transport := &http.Transport{Proxy: proxy}
	client := &http.Client{Transport: transport}
	resp, err := client.Get(mimvp_url)
	if err != nil {
		fmt.Println("error : ", err)
		return
	} else {
		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Printf("%s\n", body)
	}
}

// http（方法2）
func main_2(proxy_uri string, mimvp_url string) {
	url_i := url.URL{}
	url_proxy, _ := url_i.Parse(proxy_uri)
	transport := &http.Transport{Proxy: http.ProxyURL(url_proxy)}
	client := http.Client{Transport: transport}
	resp, err := client.Get(mimvp_url)
	if err != nil {
		log.Fatalln(err)
	} else {
		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Printf("%s\n", body)
	}
}

// config environment varable
func main_22(proxy_uri string, mimvp_url string) {
	// url_i := url.URL{}
	// url_proxy, _ := url_i.Parse("https://127.0.0.1:9743")
	os.Setenv("HTTP_PROXY", "http://125.77.25.124:80")
	os.Setenv("HTTPS_PROXY", "https://210.209.89.100:8081")
	c := http.Client{ /* Transport: &http.Transport{ // Proxy: http.ProxyURL(url_proxy)} */ }
	resp, err := c.Get("http://mimvp.com")
	if err != nil {
		log.Fatalln(err)
	} else {
		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Printf("%s\n", body)
	}
}

// 指定代理ip
func getTransportFieldURL(proxy_addr *string) (transport *http.Transport) {
	url_i := url.URL{}
	url_proxy, _ := url_i.Parse(*proxy_addr)
	transport = &http.Transport{Proxy: http.ProxyURL(url_proxy)}
	return
}

// 从环境变量$http_proxy或$HTTP_PROXY中获取HTTP代理地址
// Linux 设置代理环境变量命令：
// http_proxy=http://125.77.25.124:80
// https_proxy=https://210.209.89.100:8081
func getTransportFromEnvironment() (transport *http.Transport) {
	transport = &http.Transport{Proxy: http.ProxyFromEnvironment}
	return
}

func fetch(mimvp_url, proxy_uri *string) (html string) {
	transport := getTransportFieldURL(proxy_uri)
	client := &http.Client{Transport: transport}
	req, err := http.NewRequest("GET", *mimvp_url, nil)
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
	if err != nil {
		log.Fatal(err.Error())
	}
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err.Error())
	}
	if resp.StatusCode == 200 {
		robots, err := ioutil.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			log.Fatal(err.Error())
		}
		html = string(robots)
	} else {
		html = ""
	}
	return
}

// http（方法3）
func main_3(proxy_uri string, mimvp_url string) {
	html := fetch(&mimvp_url, &proxy_uri)
	fmt.Println(html)
}

// socks5
// 1. download https://github.com/golang/net
// 2. unzip and move to /usr/local/go/src/golang.org/x/net/
// 3. import ( "golang.org/x/net/proxy" )
func main_socks5(proxy_socks string, mimvp_url string) {
	dialer, err := proxy.SOCKS5("tcp", proxy_socks, nil, proxy.Direct)
	if err != nil {
		fmt.Println(os.Stderr, "can't connect to socks5 proxy:", err)
		os.Exit(1)
	}

	// setup a http client
	//	transport := &http.Transport{}
	//	transport.Dial = dialer.Dial
	transport := &http.Transport{Dial: dialer.Dial}
	client := &http.Client{Transport: transport}

	resp, err := client.Get(mimvp_url)
	if err != nil {
		log.Fatalln(err)
	} else {
		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Printf("%s\n", body)
	}
}

func main() {
	// http
	proxy_uri := "http://125.77.25.124:80"
	mimvp_url := "http://proxy.mimvp.com/exist.php"
	main_1(proxy_uri, mimvp_url)
	main_2(proxy_uri, mimvp_url)
	main_3(proxy_uri, mimvp_url)

	// socks5
	proxy_socks := "175.138.65.244:1080"
	main_socks5(proxy_socks, mimvp_url)
}

// 执行命令：
// $ go build mimvp-proxy-go.go
// $ ./mimvp-proxy-go
