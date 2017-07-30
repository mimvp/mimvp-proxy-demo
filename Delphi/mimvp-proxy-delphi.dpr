# Delphi 支持 http
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
# 
# 米扑代理购买：
# http://proxy.mimvp.com
# 
# mimvp.com
# 2016-11-25


interface
    uses
        Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
        Dialogs, StdCtrls, IDHTTP;

    type
        TForm1 = class(TForm)
            Button1: TButton;
            procedure Button1Click(Sender: TObject);
        private
            { Private declarations }
        public
            { Public declarations }
        end;

    var
        Form1: TForm1;

    implementation

    {$R * .dfm}

    procedure TForm1.Button1Click(Sender: TObject);
    const
        // 要访问的目标页面
        mimvp_url = "http://proxy.mimvp.com/exist.php"
        mimvp_url2 = "https://proxy.mimvp.com/exist.php"
        mimvp_url3 = "https://apps.bdimg.com/libs/jquery-i18n/1.1.1/jquery.i18n.min.js"

        // 代理服务器
        proxy_ip = '138.68.165.154';
        proxy_port = 3128;
        
    var
        IDHTTP1 : TIDHTTP;
    begin
        Application.ProcessMessages;
        IDHTTP1 : = TIDHTTP.Create(nil);
        with IDHTTP1 do
        begin
            AllowCookies : = True;
            HandleRedirects : = True;
            ProxyParams.BasicAuthentication : = True;
            ProxyParams.ProxyServer : = proxy_ip;
            ProxyParams.ProxyPort : = proxy_port;
#             ProxyParams.ProxyUsername : = 'mimvp-user';
#             ProxyParams.ProxyPassword : = 'mimvp-pass';
            
            Request.Method : = 'GET';
            Request.Accept : = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8';
            Request.AcceptEncoding : = 'gzip, deflate, sdch';
            Request.AcceptLanguage : = 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4';
            Request.Connection : = 'keep-alive';
            Request.UserAgent : = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36';
            IDHTTP1.Get(mimvp_url);
        end;
    end;
end.   