#!/bin/bash

filehash=$(cat filehash)

eventhash=$(md5sum /var/log/auth.log | awk '{print $1}')

if [[ "$filehash" = "$eventhash" ]]
then
        echo "Equal"
else
        echo "Not Equal"
        echo $(md5sum /var/log/auth.log | awk '{print $1}') > filehash

        todaysDate=$(date -I)
        today=$(date +"%b %e")

        cat /var/log/auth.log | grep -e "$(date +'%b %e')" | grep -i "accepted\|failed" > /home/nitesh/authlogs/$todaysDate.txt
        python3 /home/nitesh/scripts/loguploader.py

fi