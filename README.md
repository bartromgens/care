Care 
====
#### Computer automated remote exchange

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
- Python 3.x
- Django 1.6
- South 0.8.3
- django-bootstrap3 4.11.0
- django-cron 0.3.4
- django-registration-redux 1.1

Installation
------------
#### Create a virtualenv
Create a virtual enviroment with python 3.x,
```bash
$ virtualenv -p /usr/bin/python3.x [virtualenvdir]
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
Copy `./base/user_settings_example.py` to `./base/user_settings.py` and change the placeholders in user_settings.py with your personal settings. 

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

