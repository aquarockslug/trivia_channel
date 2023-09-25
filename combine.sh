#!/bin/bash

cd combine || exit

# sort and combine
CONCAT=""
for f in *.mpeg; do CONCAT="$CONCAT$f|"; done
sort "$CONCAT"
ffmpeg -v quiet -stats -y -i "concat:${CONCAT::-1}" -vf "scale=1920:1080" -c copy "../output/$1.mp4"
ffmpeg -y -i "../output/$1.mp4" -vframes 1 "../output/$1_thumb.png"
