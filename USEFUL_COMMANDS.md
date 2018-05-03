# Useful Commands

### Replace in files

* `find ./ -iname "*.md" -type f | xargs sed -i 's/width=\([0-9]\+\)/style="width: \1px"/g'`
  * before: `<img src="media/15248055719429.jpg" width=600 />`
  * after: `<img src="media/15248055719429.jpg" style="width:600px" />`
