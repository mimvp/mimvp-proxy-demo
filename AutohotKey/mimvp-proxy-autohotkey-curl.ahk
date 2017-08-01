; AutohotKey 支持 http
;
; 米扑代理示例：
; http://proxy.mimvp.com/demo2.php
; 
; 米扑代理购买：
; http://proxy.mimvp.com
; 
; mimvp.com
; 2016-11-29

URL := "http://proxy.mimvp.com/exist.php"
RESULT_FILE = "result_curl.txt"

Runcurl = curl.exe "%URL%" -x 138.68.165.154:3128 -o "%RESULT_FILE%"
;Runcurl = curl.exe "%URL%" -x user:password@proxyhost:port -o "%RESULT_FILE%"
Runwait, %comspec% /c %RunCurl%, , Hide