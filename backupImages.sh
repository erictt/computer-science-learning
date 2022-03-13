#!/bin/bash

images=$(\grep -oh "https:\/\/i\.imgur\.com\/.*\.[jpgnif]*" -rn ./notes/ | sed "s/[0-9]*\:https\:\/\/i\.\imgur\.com\///g" | sort | uniq)
downloaded=$(find ./images/ -name "*.[jpgpnif]*" | sed "s/.*\/\///g" | sort | uniq)
prefix="https://i.imgur.com/"

count=0
skip=0

for i in $images; do
  exist=$(echo $downloaded | grep $i)
  if [[ "$exist" == "" ]]; then
    # echo "$count: wget $prefix$i -O ./images/$i"
    wget $prefix$i -O ./images/$i
    count=$((count+1))
  else
    # echo "skip: $i"
    skip=$((skip+1))
  fi
done

echo "Total skipped: $skip, total downloaded: $count"
