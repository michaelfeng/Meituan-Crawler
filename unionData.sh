#!/bin/bash

while IFS='' read -r city || [[ -n "$line" ]]; do
    while IFS='' read -r area || [[ -n "$line" ]]; do
	echo "$city,$area"
    done < GB2260.txt
done < pureCity.txt

#awk '{ getline b < "GB2260.txt"; print $0, b}' pureCity.txt

