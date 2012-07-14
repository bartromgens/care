#!/usr/bin/bash
# ssh bartromgens@bartromgens.webfactional.com
# ~/webapps/care/apache2/bin/restart
# python2.7 manage.py collectstatic
scp -r ../. bartromgens@bartromgens.webfactional.com:~/webapps/care/care/
scp ../webfaction/*.py bartromgens@bartromgens.webfactional.com:~/webapps/care/care/base/
scp -r ../static/. bartromgens@bartromgens.webfactional.com:~/webapps/care/care/staticfiles
