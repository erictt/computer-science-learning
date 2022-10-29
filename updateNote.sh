#!/bin/sh

hexo clean

hexo generate 

cp ./CNAME ./docs/

git add . && git commit -m "update notes" && git push


