#!/bin/bash

# convert to video
for f in slides/*a.jpg; do ffmpeg -y -loop 1 -i $f -t 10 $f.mpeg; done;
for f in slides/*b.jpg; do ffmpeg -y -loop 1 -i $f -t 5 $f.mpeg; done;
ffmpeg -y -loop 1 -i slides/title.jpg -t 3 slides/aa_title.jpg.mpeg

# combine slides 
cd slides 
CONCAT = ""
for f in *.jpg.mpeg; do CONCAT="$CONCAT$f|"; done
sort $CONCAT
ffmpeg -i "concat:${CONCAT::-1}" -c copy ../output.mpeg
