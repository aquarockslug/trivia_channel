#!/bin/bash

cd combine || exit

# sort and combine
CONCAT=""
for f in *.mpeg; do CONCAT="$CONCAT$f|"; done
sort $CONCAT
ffmpeg -v quiet -stats -y -i "concat:${CONCAT::-1}" -c copy "../output/$1.mp4"
#echo "\n$CONCAT\nCreated $1.mp4 in output folder"
