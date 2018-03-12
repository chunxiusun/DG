#while(true); do

#ps -ef | grep add_feature | awk '{print $2}' | xargs kill -9
for i in {0..4} 
do
    echo $i
    nohup python -u ranker_1vN.py ../addfeature/feature/feature_$i.txt 2>&1 1>$i.log &
done

#sleep 600 
#done
