#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

os.chdir("source/_posts")
files = [x for x in list(os.walk('.'))[0][2] if re.match(r'^\d{4}-\d{2}-\d{2}-.+?\.md$', x)]
for file in files:
    createDate = file[0:10]
    os.system("sed -i '2 adate: " + createDate + "' " + file)
    updateDate = str(os.popen('git log --pretty=format:"%ad" --date=short -1 ' + file).read())
    os.system("sed -i '3 aupdated: " + updateDate + "' " + file)
