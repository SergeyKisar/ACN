#!/bin/bash

set -x

USER="root"
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

#log_file olt-reboot_$(date '+%x-%R').log
exp_internal 1
set timeout 2

spawn ssh $USER@$H
expect \"*(yes/no)?*\" {send \"yes\r\"}
expect \"password:\" {send \"$PASSWD\r\"}

expect \"*>\"
send \"enable\r\"
expect \"*>\"
send \"show time\r\"
expect \"*>\"
send \"show device\r\"
expect \"*>\"
send \"show version\r\"
expect \"*>\"
send \"reboot\r\"
expect \"Are you sure to reboot system? (y/n):\" {send \"y\r\"}
expect \"*>\"
expect eof
"

expect -c "$COMM" > $H.log

done

mkdir -p ~/olt-reboot_$DATE
mv ~/172.16* ~/olt-reboot_$DATE
