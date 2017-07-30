#!/bin/bash
#
# http 支持 http、https
#
# 米扑代理示例：
# http://proxy.mimvp.com/demo2.php
#
# 米扑代理购买：
# http://proxy.mimvp.com
#
# mimvp.com
# 2015-11-10


# http代理格式 		--proxy http:IP:Port
# https代理格式 		--proxy https:IP:Port


$ http --help
usage: http [--json] [--form] [--pretty {all,colors,format,none}]
            [--style STYLE] [--print WHAT] [--headers] [--body] [--verbose]
            [--all] [--history-print WHAT] [--stream] [--output FILE]
            [--download] [--continue]
            [--session SESSION_NAME_OR_PATH | --session-read-only SESSION_NAME_OR_PATH]
            [--auth USER[:PASS]] [--auth-type {basic,digest}]
            [--proxy PROTOCOL:PROXY_URL] [--follow]
            [--max-redirects MAX_REDIRECTS] [--timeout SECONDS]
            [--check-status] [--verify VERIFY]
            [--ssl {ssl2.3,ssl3,tls1,tls1.1,tls1.2}] [--cert CERT]
            [--cert-key CERT_KEY] [--ignore-stdin] [--help] [--version]
            [--traceback] [--default-scheme DEFAULT_SCHEME] [--debug]
            [METHOD] URL [REQUEST_ITEM [REQUEST_ITEM ...]]
            
# http
http --proxy "http:217.107.197.174:8081" http://proxy.mimvp.com/exist.php | grep '<font color="red">'

# https
http --verify no --proxy "https:46.105.214.133:3128" https://proxy.mimvp.com/exist.php | grep '<font color="red">'
