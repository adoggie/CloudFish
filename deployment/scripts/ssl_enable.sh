#!/usr/bin/env bash
pwd=$(cd `dirname $0`;pwd)
nginx_cfg=$pwd/../nginx/nginx_docker.conf
js_file=$pwd/../moca/src/web/static/js/message/message.js

sed -e "s/#ssl on;/ssl on;/g" $nginx_cfg > /tmp/nginx.conf ; cat /tmp/nginx.conf > $nginx_cfg
#sed -e "s/ws:/wss:/g" $js_file > /tmp/message.js ; cat /tmp/message.js > $js_file