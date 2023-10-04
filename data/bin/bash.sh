#!/bin/bash
# get data code
name=$1
# reads=$2
pwd=$(pwd)
# basedir=$(dirname $pwd)

find $pwd -type f -name "*.html" | while read -r i ; do
  total_seq=$(grep -Pzo '(?s)<td>Total Sequences<\/td>.*<td>Sequences flagged as poor quality<\/td>' "$i" | grep -oaE '<td>Total Sequences<\/td><td>[0-9-]+<\/td>' | grep -oE '[0-9]+') &&
  max_seq=$(grep -Pzo '(?s)<td>Sequence length<\/td>.*<td>%GC<\/td>' "$i" | grep -oaE '<td>Sequence length<\/td><td>[0-9-]+<\/td>' | grep -oE '[0-9]+' | sort -n | tail -1) &&
  name_seq=$(grep -Pzo '(?s)<td>Filename<\/td>.*<td>File type<\/td>'  "$i" | awk -F'</?td>' '{print $4}') && 
  adapter_seq=$(grep -oP 'alt="\K[^"]*(?="/>Adapter)' "$i")&&
  echo "${name_seq}  ${max_seq} ${total_seq} ${adapter_seq}"  >> ${name}_output.txt 
done
awk '!seen[$0]++' ${name}_output.txt > ${name}_output_clear.txt
# sed '/R2/d' output_awk.txt > output_awk_remove_lap.txt

