#!/bin/bash
for f in slides/g*.jpg; do ffmpeg -loop 1 -f image2 -i $f -t 10 $f.mp4; done;
for f in slides/a*.jpg; do ffmpeg -loop 1 -f image2 -i $f -t 5 $f.mp4; done;
ffmpeg slides/title.jpg -loop 1 -f image2 -i $f -t 5 title.mp4
