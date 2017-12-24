#! /bin/bash

# projectName=computer-science-learning
while [ x$projectName = "x" ]; do
  read -p "Project Name (Under Path ~/workspace/) : " projectName
done

sourcePath=~/workspace/${projectName}

# Sync computer-science-learning to iCould Mweb
rsync -arve --delete \
  --delete-excluded \
  --exclude=node_modules \
  --exclude=book.json \
  --exclude=.DS_Store \
  --exclude=_book \
  --exclude=etc \
  --exclude=\.git* \
  $sourcePath \
  ~/Library/Mobile\ Documents/iCloud~com~coderforart~iOS~MWeb/Documents/
