#! /bin/bash

sourcePath="non-path"
while [ ! -d $sourcePath ]; do
  if [ ! $sourcePath = 'non-path' ]; then
    echo "Directory ($sourcePath) doesn't exist"
  fi
  read -p "Project Name (Under Path ~/workspace/) [Default: computer-science-learning]: " projectName
  projectName=${projectName:-computer-science-learning}
  sourcePath=~/workspace/${projectName}
done

# Sync computer-science-learning to iCould Mweb
rsync -arve --delete \
  --delete-excluded \
  --exclude=node_modules \
  --exclude=book.json \
  --exclude=.DS_Store \
  --exclude=_book \
  --exclude=etc \
  --exclude=\.git* \
  --exclude=algorithms-1/programming \
  --exclude=algorithms-1/algs4 \
  --exclude=sync2Icloud.sh \
  --exclude=stanford-machine-learning/ex* \
  --exclude=laff-linear-algebra/LAFF-2.0xM \
  $sourcePath \
  ~/Library/Mobile\ Documents/iCloud~com~coderforart~iOS~MWeb/Documents/
