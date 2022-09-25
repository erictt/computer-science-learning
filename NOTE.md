# NOTE

## HEXO

* one for all: `hexo generate && git add . && git commit -m "update notes" && git push`

## replace markdown image format to html format

* e.g. replace ![](https://i.imgur.com/xxx.png) to <img src="https://i.imgur.com/xxxx.png" style="width: 500px" />                                                                                           │
* `sed 's/\!\[\](\(https:[\/\.0-9a-zA-Z]*\))/<img src="\1" style="width: 500px" \/\>/' ./files.md`
