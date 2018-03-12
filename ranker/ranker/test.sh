#/bin/bash

rm Latency
rm Accuracy
rm QPS


for i in {0..49}
do
   cat $i.log |grep "Rankered Latency"|tail -n 1 >> Latency
   cat $i.log |grep "Rankered Accuracy"|tail -n 1 >> Accuracy
   cat $i.log |grep "Rankered QPS"|tail -n 1 >> QPS

done

   cat Latency | awk '{t=t+$3} END {print t/NR}'
   cat Accuracy | awk '{c=c+$3} END {print c/NR}'
   cat QPS | awk '{q=q+$3} END {print q}'
