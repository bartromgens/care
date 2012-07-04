#!/usr/bin/bash
# ssh bartromgens@bartromgens.webfactional.com
# ~/webapps/care/apache2/bin/restart
scp -r ../. bartromgens@bartromgens.webfactional.com:~/webapps/care/care/
scp ../webfaction/*.py bartromgens@bartromgens.webfactional.com:~/webapps/care/care/base/
scp ../static/style.css bartromgens@bartromgens.webfactional.com:~/webapps/static/
