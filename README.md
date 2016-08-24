Care 
====
#### Computer Automated Remote Exchange
[![Build Status](https://travis-ci.org/bartromgens/care.svg?branch=master)](https://travis-ci.org/bartromgens/care) [![Dependency Status](https://gemnasium.com/badges/github.com/bartromgens/care.svg)](https://gemnasium.com/github.com/bartromgens/care) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/bartromgens/care/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/bartromgens/care/?branch=master)

Share expenses with friends in this Django and Bootstrap based web application.

Features
------------------
- Web interface for desktop, tablet and mobile
- Share expenses between multiple friends
- Register real transactions between friends
- Keep track of your balance within a group
- Create groups
- Invite friends to group
- Periodic transaction history email
- Notification when balance is too low
- Modify shares and transactions

Dependencies
-----------
- Python 3.3+
- Django 1.9
- see `requirements.txt`

Installation
------------
#### Create a virtualenv
Create a virtual enviroment with python 3.x,
```bash
$ virtualenv -p /usr/bin/python3.x env
```
Activate the enviroment,
```bash
$ source ./env/bin/activate
```
#### Install dependencies
Install the required python modules (with activated virtual env),
```bash
$ pip install -r requirements.txt
```
#### Create local_settings.py
Run `create_local_settings.py`,
```bash
$ python create_local_settings.py
```

#### Create database
Create initial database,
```bash
$ manage.py migrate
```

Create a superuser,
```bash
$ python manage.py createsuperuser
```

#### Test run
Run test server,
```bash
$ python manage.py runserver
```
#### Create userprofile
Create a userprofile for the root user you just created,
- Visit `http://127.0.0.1:8000/admin` and login with the root account
- Create a new userprofile and link it to the root user


Webfaction (Django hosting)
------------
##### Set project PYTHONPATH
```bash
$ PYTHONPATH=$HOME/webapps/<projectname>/lib/python3.4
```

##### Install dependencies
Install dependencies,
```bash
$ pip3.4 install --target=$HOME/webapps/<projectname>/lib/python3.4 -r requirements.txt
```

##### Collect staticfiles
```bash
$ python3.4 manage.py collectstatic
```

#####  Check error log
```bash
$ less ~/logs/user/error_care.log
```
##### Apache restart
```bash
$ ~/webapps/<projectname>/apache2/bin/restart
```

##### Cronjob (python)
```
*/05 * * * * cd /home/bartromgens/webapps/<projectname>/care/ && PYTHONPATH=$HOME/webapps/<projectname>/lib/python3.4 /usr/local/bin/python3.4 manage.py runcrons >> $HOME/logs/user/cron.log 2>&1
```
