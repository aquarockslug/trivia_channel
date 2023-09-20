#!/bin/bash

# converting images into videos with an empty audio track
echo Creating guess slides...
cd slides
for f in *a.png; do ffmpeg -y -loop 1 -i $f -i $2 -c copy -map 0:v:0 -map 1:a:0 -c:v libx264 -pix_fmt yuv420p -t 10 -vf fade=type=in:duration=1,fade=type=out:duration=1:start_time=9,scale=1920:1080 -y ../combine/$f.mpeg; echo +; done;

for f in *b.png; do ffmpeg -y -loop 1 -i $f -i $2 -c copy -map 0:v:0 -map 1:a:0 -c:v libx264 -pix_fmt yuv420p -t 5 -vf fade=type=in:duration=1,scale=1920:1080 -y ../combine/$f.mpeg; echo +; done;
cd .. 

# sort and combine
echo Creating 
cd combine
CONCAT=""
for f in *.mpeg; do CONCAT="$CONCAT$f|"; done;
sort $CONCAT
ffmpeg -i "concat:${CONCAT::-1}" -c copy "../output/$1.mp4"
cd ..
