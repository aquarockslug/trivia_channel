#!/bin/bash

# convert images into videos with an empty audio track
cd slides || exit
for f in *a.png; do
	ffmpeg -v quiet -stats -y -loop 1 -i "$f" -i $2 -c copy -map 0:v:0 -map 1:a:0 -c:v libx264 -pix_fmt yuv420p -t 10 -vf fade=type=in:duration=1,fade=type=out:duration=1:start_time=9,scale=1920:1080 -y ../combine/$f.mpeg
	rm $f
done

echo Creating answer slides:

for f in *b.png; do
	ffmpeg -v quiet -stats -y -loop 1 -i "$f" -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 5 -c:v libx264 -t 5 -pix_fmt yuv420p -vf fade=type=in:duration=1,scale=1920:1080 -y ../combine/$f.mpeg
	rm $f
done

ffmpeg -v quiet -stats -y -loop 1 -i title.png -f lavfi -i anullsrc=channel_layout=5.1:sample_rate=48000 -t 3 -c:v libx264 -t 3 -pix_fmt yuv420p -vf scale=1920:1080 -y ../combine/a_title.png.mpeg
cd ..

cd combine || exit

# sort and combine
CONCAT=""
for f in *.mpeg; do CONCAT="$CONCAT$f|"; done
sort "$CONCAT"
ffmpeg -v quiet -stats -y -i "concat:${CONCAT::-1}" -c copy "../output/$1.mp4"
echo "\n$CONCAT\nCreated $1.mp4 in output folder"
