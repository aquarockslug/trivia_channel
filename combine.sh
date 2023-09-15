#!/bin/bash

# sort and combine
CONCAT = ""
for f in slides/*.mpeg; do CONCAT="$CONCAT$f|"; done;
sort $CONCAT
ffmpeg -i "concat:${CONCAT::-1}" -c copy "output/output.mpeg"
#ffmpeg -i "../output/output.mpeg" "output/output.mp4"
echo $CONCAT
