#!/bin/bash
while :
do
    var1=`ps -ef | grep 'python3 cube-assistant.py' | wc | awk '{print $1}'`
    if [ $var1 -gt 1 ]
    then
        echo "RUNNING"
    else
        echo "INACTIVAE"
        source bin/activate && nohup python3 cube-assistant.py &
    fi
    sleep 5
done
