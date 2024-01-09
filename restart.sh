#!/bin/bash

pkill -9 -f cube-assistant.py
#pkill -9 -f /home/theimc/incubate/earthling-cube-textom/restart.sh
cd /home/theimc/incubate/textom-cube
source bin/activate
python3 cube-serialize.py && python3 cube-assistant.py 

