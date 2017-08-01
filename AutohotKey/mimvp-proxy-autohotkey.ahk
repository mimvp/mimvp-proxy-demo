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


MIMVP_PROXY_NOAUTH := 2
MIMVP_PROXY_AUTH := 1

;~ 代理服务器
proxy_http := "138.68.165.154:3128"

;~ 要访问的目标页面
mimvp_url := "http://proxy.mimvp.com/exist.php"
mimvp_url2 = "https://proxy.mimvp.com/exist.php"

whr := ComObjCreate("WinHttp.WinHttpRequest.5.1")
whr.SetTimeouts(30000,30000,30000,30000) 			;~ Set timeouts to 30 seconds

whr.Open("GET", mimvp_url, true)
whr.SetRequestHeader("User-Agent", "curl/7.41.0")	;~ 模拟curl的ua，方便测试


;~ 设置代理服务器
whr.SetProxy(MIMVP_PROXY_NOAUTH, proxy_http)

;~ 设置代理隧道验证信息
;whr.SetCredentials('mimvp-user', 'mimvp-pass', MIMVP_PROXY_AUTH)

whr.Send()
whr.WaitForResponse()

MsgBox % whr.ResponseText  ; 输入到消息框，网页内容太长则显示不完整


; 打开对话框选择文件，写入完整的网页内容
FileSelectFile, resultName, S16,, Create a new file:
if (resultName = "")
	return
	
outFile := FileOpen(resultName , "w" , "utf-8")
if !IsObject(outFile)
{
	MsgBox , 不能打开文件: %resultName%
	return 
}
outFile.write(whr.ResponseText)
outFile.Close()
    