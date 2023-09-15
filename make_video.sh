#!/bin/bash

# convert images into video with empty audio track
for f in slides/*a.png; do ffmpeg -y -loop 1 -i $f -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 10 -c:v libx264 -t 10 -pix_fmt yuv420p -vf scale=1920:1080 -y $f.mpeg; done;
for f in slides/*b.png; do ffmpeg -y -loop 1 -i $f -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 5 -c:v libx264 -t 5 -pix_fmt yuv420p -vf scale=1920:1080 -y $f.mpeg; done;
ffmpeg -y -loop 1 -i slides/title.png -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 3 -c:v libx264 -t 3 -pix_fmt yuv420p -vf scale=1920:1080 -y slides/a_title.png.mpeg

cd slides

# add fade effect
# for f in *a.png.mpeg; do ffmpeg -i $f -vf fade=type=in:duration=1,fade=type=out:duration=1:start_time=9 $f.mpeg; rm $f; done;

# combine guess slides with music 
for f in *a.png.mpeg; do ffmpeg -i $f -i $2 -c copy -map 0:v:0 -map 1:a:0 -y $f.mpeg; rm $f; done;

# sort and combine
CONCAT = ""
for f in *.mpeg; do CONCAT="$CONCAT$f|"; done;
sort $CONCAT
ffmpeg -i "concat:${CONCAT::-1}" -c copy "../output/$1.mpeg"
ffmpeg -i "../output/$1.mpeg" "../output/$1.mp4"
