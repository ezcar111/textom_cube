#!/bin/bash

serv_list=(

        "210.91.154.134"
        "210.91.154.135"
        "210.91.154.136"
        "210.91.154.137"
        "210.91.154.152"
        "210.91.154.153"
        "210.91.154.154"
        "210.91.154.155"
        "210.91.154.164"
        "210.91.154.166"
        "210.91.154.175"
        "210.91.154.176"
        "210.91.154.177"
        "210.91.154.178"

)

for (( i = 0 ; i < ${#serv_list[@]} ; i++ )) ; do
        serv_addr=${serv_list[$i]}
        nohup ssh root@$serv_addr /home/theimc/incubate/textom-cube/restart.sh &
done
#nohup ssh root@10.0.0.3 /home/theimc/incubate/earthling-cube-textom/restart.sh &
#nohup ssh root@10.0.0.4 /home/theimc/incubate/earthling-cube-textom/restart.sh &

#&&
#ssh root@10.0.0.4 /home/theimc/incubate/earthling-cube-textom/restart.sh &&
#ssh root@10.0.0.5 /home/theimc/incubate/earthling-cube-textom/restart.sh &&
#ssh root@10.0.0.6 /home/theimc/incubate/earthling-cube-textom/restart.sh &&
#ssh root@10.0.0.7 /home/theimc/incubate/earthling-cube-textom/restart.sh &&
#ssh root@10.0.0.8 /home/theimc/incubate/earthling-cube-textom/restart.sh &&
#ssh root@10.0.0.9 /home/theimc/incubate/earthling-cube-textom/restart.sh &&
#ssh root@10.0.0.10 /home/theimc/incubate/earthling-cube-textom/restart.sh &&
#ssh root@10.0.0.11 /home/theimc/incubate/earthling-cube-textom/restart.sh