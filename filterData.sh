#!/bin/bash

needPrint=false
str=""
while IFS=',' read -ra line || [[ -n "$line" ]]; do
    if [ ${line[0]} == ${line[1]} ]; then
	needPrint=true
    elif [ ${line[0]} != ${line[1]} ]; then
	if [[ ${line[1]} =~ 市$  ]]; then
	    needPrint=false
	fi
    fi
    
    if [ $needPrint == true ]; then
	echo ${line[0]},${line[1]}
    fi
done < data.out



