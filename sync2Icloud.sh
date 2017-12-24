#! /bin/bash

projectName="computer-science-learning"

sourcePath="~/workspace/"${projectName}

destinationPath="~/Library/Mobile\ Documents/iCloud~com~coderforart~iOS~MWeb/Documents/"


# Sync computer-science-learning to iCould Mweb
rsync -arve --delete \
  --delete-excluded \
  --exclude=node_modules \
  --exclude=book.json \
  --exclude=.DS_Store \
  --exclude=_book \
  --exclude=etc \
  --exclude=\.git* \
  ${sourcePath} \
  ${destinationPath}
