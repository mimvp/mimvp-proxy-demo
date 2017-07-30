#!/usr/bin/env perl 
#
# Perl 支持 http、https
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2017-03-28


use CGI;
use strict;
use LWP::UserAgent;


our %proxy_http = ("http", "http://138.68.165.154:3128");
our %proxy_https = ("https", "https://113.106.94.213:80");
our %proxy_connect = ("https", "connect://173.233.55.118:443");

our $mimvp_url = "http://proxy.mimvp.com/exist.php";
our $mimvp_url2 = "https://proxy.mimvp.com/exist.php";



## http 
sub test_http {
	my ($url, %proxy) = @_;
	
	print "proxy  : $proxy{'http'}\n";
	print "https  : $proxy{'https'}\n";
	print "url : $url\n";
	
	my $browser = LWP::UserAgent->new(ssl_opts => { verify_hostname => 0 });
	$browser->env_proxy();
	
# 	# 设置的代理格式
# 	$browser->proxy('http', 'http://138.68.165.154:3128');  
# 	$browser->proxy(['http','ftp'], 'http://138.68.165.154:3128');  
	$browser->proxy(%proxy);
	$browser->timeout(30);
	$browser->agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36');
	
	my $response = $browser->get($url);  				# 爬取的网址
	my $is_success = $response->is_success();			# 1
	my $content_type = $response->content_type();		# text/html
	my $content = $response->content();					# 网页正文
	my $content_length = length($content);				# 网页正文长度
	
	print "$is_success\n";
	print "$content_type\n";
	print "$content_length\n";
	print "$content\n";
}



## https (NO Success)
## error info : LWP::Protocol::https::Socket: SSL connect attempt failed because of handshake problems SSL wants a read first at /System/Library/Perl/Extras/5.18/LWP/Protocol/http.pm line 51.
sub test_https {
	my ($url, %proxy) = @_;
	
	print "proxy  : $proxy{'http'}\n";
	print "https  : $proxy{'https'}\n";
	print "url : $url\n";
	
	BEGIN {
		$ENV{HTTPS_PROXY} = 'https://173.233.55.118:443'; 
# 		$ENV{HTTPS_PROXY_USERNAME} = <username>; 
# 		$ENV{HTTPS_PROXY_PASSWORD} = <password>; 
		$ENV{HTTPS_DEBUG} = 1;
		$ENV{PERL_LWP_SSL_VERIFY_HOSTNAME} = 0;
	}
	
	my $browser = LWP::UserAgent->new(ssl_opts => { verify_hostname => 0 });
	$browser->env_proxy();
	
# 	# 设置的代理格式
# 	$browser->proxy(%proxy);	# NO USE
	$browser->timeout(30);
	$browser->agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36');
	
	my $req = new HTTP::Request('GET', $url);			# 爬取的网址
	my $response = $browser->request($req);
	
	my $is_success = $response->is_success();			# 1
	my $content_type = $response->content_type();		# text/html
	my $content = $response->content();					# 网页正文
	my $content_length = length($content);				# 网页正文长度
	
	print "$is_success\n";
	print "$content_type\n";
	print "$content_length\n";
	print "$content\n";
}



## https (connect)
## 1. download LWP-Protocol-connect (wget http://search.cpan.org/CPAN/authors/id/B/BE/BENNING/LWP-Protocol-connect-6.09.tar.gz)
## 2. tar zxvf LWP-Protocol-connect-6.09.tar.gz 
##    cd LWP-Protocol-connect-6.09
##    perl Makefile.PL
##    make
##    sudo make install
sub test_connect {
	my ($url, %proxy) = @_;
	
	print "proxy  : $proxy{'http'}\n";
	print "https  : $proxy{'https'}\n";
	print "url : $url\n";
	
	my $browser = LWP::UserAgent->new();
	$browser->env_proxy();
	
# 	# 设置的代理格式
# 	$browser->proxy('https', 'connect://173.233.55.118:443'); 
	$browser->proxy(%proxy);
	$browser->timeout(30);
	$browser->agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36');
	
# 	my $req = new HTTP::Request('GET', $url);
# 	my $response = $browser->request($req);
	my $response = $browser->get($url);  				# 爬取的网址
	my $is_success = $response->is_success();			# 1
	my $content_type = $response->content_type();		# text/html
	my $content = $response->content();					# 网页正文
	my $content_length = length($content);				# 网页正文长度
	
	print "$is_success\n";
	print "$content_type\n";
	print "$content_length\n";
	print "$content\n";
}


test_http($mimvp_url, %proxy_http);			# http
test_https($mimvp_url2, %proxy_https);		# https (NO Success)
test_connect($mimvp_url2, %proxy_connect);	# https (connect)



## 执行命令
## perl -d mimvp-proxy-perl.pl | grep '<font color="red">'





# ## 普通变量
# $num = 2066;             	# 整型
# $name = "mimvp.com";      	# 字符串
# $salary = 1000000.52;     	# 浮点数
# 
# print "num = $num\n";			# 2066
# print "name = $name\n";			# mimvp.com
# print "salary = $salary\n";		# 1000000.52
# 
# 
# ## 数组变量
# @num_array = (20, 30, 40);             
# @name_array = ("proxy.mimvp.com", "domain.mimvp.com", "money.mimvp.com");
# 
# print "\$num_array : @num_array\n";					# 20 30 40
# print "\$num_array[0] = $num_array[0]\n";			# 20
# print "\$num_array[2] = $num_array[2]\n";			# 40
# print "\$num_array[-1] = $num_array[-1]\n";			# 40
# print "\$name_array[1] = $name_array[1]\n";			# domain.mimvp.com
# print "\$name_array[-1] = $name_array[-1]\n";		# money.mimvp.com
# 
# 
# ## 哈希变量
# %data_dict = ('proxy', 20, 'domain', 30, 'money', 40);
# 
# print "\$data_dict{'proxy'} = $data_dict{'proxy'}\n";		# 20
# print "\$data_dict{'domain'} = $data_dict{'domain'}\n";		# 30
# print "\$data_dict{'money'} = $data_dict{'money'}\n";		# 40
# 
# 
# ## 
# @name_array = ('taobao', 'tencent', 'baidu', 'mimvp');
# 
# @copy_array = @name_array; 		# 复制数组
# $array_size = @copy_array;   	# 返回数组元素个数
# 
# print "copy_array : @copy_array\n";		# taobao tencent baidu mimvp
# print "array_size : $array_size\n";		# 4






# my $mimvp = "mimvp.com";
# print "$mimvp\n";				# mimvp.com
# 
# myFunction();
# print "$mimvp\n";				# mimvp.com
# 
# sub myFunction {
# 	print "$mimvp\n";			# mimvp.com
# 	
# 	my $mimvp = "mimvp.com in myFunction";
# 	print "$mimvp\n";			# mimvp.com in myFunction
# 	mySub();
# }
# 
# sub mySub {
# 	print "$mimvp\n";			# mimvp.com
# 	
# 	my $mimvp = "mimvp.com in mySub";
# 	print "$mimvp\n";			# mimvp.com in mySub
# }


