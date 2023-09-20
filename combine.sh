#!/bin/bash

# sort and combine
CONCAT=""
for f in combine/*.png.mpeg; do CONCAT="$CONCAT$f|"; done;
sort $CONCAT
ffmpeg -i "concat:${CONCAT::-1}" -c copy -y "output/output.mpeg"
#ffmpeg -i "../output/output.mpeg" "output/output.mp4"
echo ${CONCAT::-1}

if [ 22 -ge 21 ]
then
echo "ge true"
else
echo "ge false"
fi

