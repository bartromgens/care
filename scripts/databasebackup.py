#! /usr/bin/python

import shutil

from datetime import datetime

now = datetime.now()
nowStr = now.strftime('%Y%m%d')
shutil.copy('../care.sqlite', '../backup/' + nowStr + 'care.sqlite')