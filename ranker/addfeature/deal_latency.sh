#/bin/bash

for i in {0..49}
do
   cat $i.log |grep "Request Latency"|tail -n 1 >> Latency
   cat $i.log |grep "Successful added"|tail -n 1 >> Add

done

   cat Latency |awk '{t=t+$3} END {print t/NR}'
