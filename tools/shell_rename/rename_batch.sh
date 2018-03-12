#!/bin/bash

count=0

function getdir(){
    for element in `ls $1`
    do
        dir_or_file=$1"/"$element
        if [ -d $dir_or_file ]
        then
            #echo $element
            count=0
            file_name=$element
            getdir $dir_or_file $file_name
        else
            #echo $2
            let count+=1
            echo $2_$count.txt
            mv $dir_or_file $1"/"$2_$count.txt
        fi
    done
}

root_dir="/home/dell/python/sun/tools/shell_rename/rename_test/"
getdir $root_dir ""
