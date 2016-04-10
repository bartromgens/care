Care 
====
#### Computer Automated Remote Exchange
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/bartromgens/care/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/bartromgens/care/?branch=master) [![Dependency Status](https://gemnasium.com/badges/github.com/bartromgens/care.svg)](https://gemnasium.com/github.com/bartromgens/care)

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
#### Configure user_settings.py
Copy `./base/user_settings_example.py` to `./base/user_settings.py` and change the placeholders in user_settings.py with your local settings. 

#### Create database
Create initial database migrations for the following apps:
- userprofile
- groupaccount
- transaction
- transactionreal
- groupaccountinvite
```bash
$ python manage.py schemamigration <appname> --initial
```
migrate all apps,
```bash
$ manage.py migrate <appname>
```

Run syncdb and create a Django root user,
```bash
$ python manage.py syncdb
```

#### Test run
Run test server,
```bash
$ python manage.py runserver 127.0.0.1:8000
```
#### Create userprofile
Create a userprofile for the root user you just created,
- Visit `http://127.0.0.1:8000/admin` and login with the root account
- Create a new userprofile and link it to the root user


Webfaction (Django hosting)
------------
##### Install dependencies
see requirements.txt for required modules
```bash
$ PYTHONPATH=$HOME/webapps/care/lib/python3.3 easy_install-3.3 --install-dir=$HOME/webapps/care/lib/python3.3 --script-dir=$HOME/webapps/care/bin django-bootstrap3
```

##### Collect staticfiles
```bash
$ python3.3 manage.py collectstatic
```

#####  Check error log
```bash
$ less ~/logs/user/error_care.log
```
##### Apache restart
```bash
$ ~/webapps/care/apache2/bin/restart
```

##### Cronjob (python)
```
*/05 * * * * cd /home/bartromgens/webapps/care/care/ && PYTHONPATH=$HOME/webapps/care/lib/python3.3 /usr/local/bin/python3.3 manage.py runcrons >> $HOME/logs/user/cron.log 2>&1
```
