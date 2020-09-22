#!/bin/bash
set -eux
filename='munich_suburbs.txt'
while read line; do
  python munich_suburbs.py "$line"
done < $filename

