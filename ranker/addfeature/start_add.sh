#while(true); do

#ps -ef | grep add_feature | awk '{print $2}' | xargs kill -9
for i in {1..60} 
do
    echo $i
    nohup python add_feature.py  ./feature/feature_$i.txt 2>&1 1>$i.log &
done

#sleep 600 
#done
