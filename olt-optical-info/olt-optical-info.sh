#!/bin/bash

set -x

USER="admin"
PASSWD="admin"
DATE=$(date '+%Y-%m-%d')

HOSTS="
172.16.0.101
172.16.0.102
172.16.0.103
172.16.0.104
172.16.0.105
172.16.0.106
172.16.0.107
172.16.0.108
172.16.2.101
172.16.2.102
172.16.2.103
172.16.2.104
172.16.3.101
172.16.3.102
172.16.3.103
172.16.3.104
172.16.4.101
172.16.4.102
172.16.4.103
172.16.5.101
172.16.5.102
172.16.5.103
172.16.5.104
172.16.6.101
172.16.6.102
172.16.6.103
172.16.6.104
172.16.6.105
172.16.6.106
172.16.7.101
172.16.7.102
172.16.8.101
172.16.8.102
172.16.8.103
172.16.8.104
172.16.8.105
172.16.8.106
172.16.8.107
172.16.9.101
172.16.9.102
172.16.9.103
172.16.10.101
172.16.10.102
172.16.11.101
"

for H in $HOSTS
do

COMM="

#log_file olt-optical-info_$(date '+%x-%R').log
exp_internal 1
set timeout 2

spawn ssh $USER@$H
expect \"*(yes/no)?*\" {send \"yes\r\"}
expect \"password:\" {send \"$PASSWD\r\"}

expect \"*>\"
send \"enable\r\"
expect \"*>\"
send \"config\r\"
expect \"*>\"
send \"show time\r\"
expect \"*>\"
send \"show device\r\"
expect \"*>\"
send \"show version\r\"
expect \"*>\"
send \"interface epon 0/0\r\"
expect \"*>\"
send \"show ont optical-info 1 all\r\"
expect \"*>\"
send \"show ont optical-info 2 all\r\"
expect \"*>\"
send \"show ont optical-info 3 all\r\"
expect \"*>\"
send \"show ont optical-info 4 all\r\"
expect \"*>\"
send \"show ont optical-info 5 all\r\"
expect \"*>\"
send \"show ont optical-info 6 all\r\"
expect \"*>\"
send \"show ont optical-info 7 all\r\"
expect \"*>\"
send \"show ont optical-info 8 all\r\"
expect \"*>\"
send \"show ont optical-info 9 all\r\"
expect \"*>\"
send \"show ont optical-info 10 all\r\"
expect \"*>\"
send \"show ont optical-info 11 all\r\"
expect \"*>\"
send \"show ont optical-info 12 all\r\"
expect \"*>\"
send \"show ont optical-info 13 all\r\"
expect \"*>\"
send \"show ont optical-info 14 all\r\"
expect \"*>\"
send \"show ont optical-info 15 all\r\"
expect \"*>\"
send \"show ont optical-info 16 all\r\"
expect \"*>\"
send \"exit\r\"
expect \"*>\"
send \"logout\r\"
expect \"*>\"

expect eof
"

expect -c "$COMM" > $H.log

done

mkdir -p ~/_optical-info/olt-optical-info_$DATE
mv ~/172.16* ~/_optical-info/olt-optical-info_$DATE
