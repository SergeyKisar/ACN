#!/bin/bash

set -x

USER="admin"
PASSWD="admin"
DATE=$(date '+%x-%R')

HOSTS="
172.16.0.101
"

for H in $HOSTS

do

expect << EOF > $H.log
set timeout 2
spawn ssh $USER@$H
expect {
    "*(yes/no)*" {
        send "yes\r"
        exp_continue
    }
    "*password:*" {
        send "$PASSWD\r"
        exp_continue
    }
    "*>" {
        send "enable\r"
        exp_continue
    }
}
send "show saved-config\r"
expect {
    -re {--More.*\( Press 'Q' to quit \).*} {
        send "1"
        exp_continue
    }
    "*>"
}
send -- "logout\r"
expect "*>"

EOF

sed -i '/Unknown command:/d' $H.log
sed -i '/--More .* Press '\''Q'\'' to quit/d' $H.log

done

# mkdir olt-show-saved-config_$DATE
# mv ./172.16* ./olt-show-saved-config_$DATE
