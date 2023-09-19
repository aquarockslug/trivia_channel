#!/bin/bash

# convert images into video with empty audio track
cd slides
for f in *a.png; do ffmpeg -y -loop 1 -i $f -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 10 -c:v libx264 -t 10 -pix_fmt yuv420p -vf scale=1920:1080 -y ../fade/$f.mpeg; done;

for f in *b.png; do ffmpeg -y -loop 1 -i $f -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 5 -c:v libx264 -t 5 -pix_fmt yuv420p -vf scale=1920:1080 -y ../combine/$f.mpeg; done;

ffmpeg -y -loop 1 -i title.png -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 3 -c:v libx264 -t 3 -pix_fmt yuv420p -vf scale=1920:1080 -y ../combine/a_title.png.mpeg

# add fade effect
cd slides
for f in *a.png.mpeg; do ffmpeg -i $f -vf fade=type=in:duration=1,fade=type=out:duration=1:start_time=9 ../fade/$f; rm $f; done;
cd ..

# combine guess slides with music 
cd fade
for f in *a.png.mpeg; do ffmpeg -i $f -i $2 -c copy -map 0:v:0 -map 1:a:0 -y ../combine/$f; rm $f; done;
cd ..

# sort and combine
cd combine
CONCAT = ""
for f in *.png.mpeg; do CONCAT="$CONCAT$f|"; done;
sort $CONCAT
ffmpeg -i "concat:${CONCAT::-1}" -c copy "../output/$1.mpeg"

# convert to mp4
ffmpeg -i "../output/$1.mpeg" "../output/$1.mp4"
