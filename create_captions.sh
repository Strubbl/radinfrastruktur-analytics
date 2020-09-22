#!/bin/bash
set -eux
searchpath=$1
for i in $searchpath/*.png
do
  f=$(basename -- "$i")
  caption_filename="${i%.*}.txt"
  echo "${f%.*}" > "$caption_filename"
  sed -i "s/_/ /g" "$caption_filename"
done
