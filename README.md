# care
[![Build Status](https://travis-ci.org/bartromgens/care.svg?branch=master)](https://travis-ci.org/bartromgens/care)
#### Computer Automated Remote Exchange

Share expenses with friends in this Django and Bootstrap based web application.

Features
------------------
- Responsive web interface
- Share expenses between multiple friends
- Register real transactions between friends
- Keep track of your balance within a group
- Create groups
- Invite friends to group
- Periodic transaction history email
- Notification when balance is too low
- Modify shares and transactions
- Recurring shares
- Group statistics

## Dependencies
- Python 3.4+
- Django 1.11
- see `requirements.txt`

## Installation

#### Create a virtualenv
Create a virtual enviroment with Python 3,
```bash
$ virtualenv -p /usr/bin/python3 env
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
