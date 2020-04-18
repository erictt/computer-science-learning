#! /bin/sh

hexo generate
git add .
git commit -m "new updates"
git push -u origin master
