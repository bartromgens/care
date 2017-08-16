## Webfaction Intallation (Django hosting)

##### Set project PYTHONPATH
```bash
$ PYTHONPATH=$HOME/webapps/<projectname>/lib/python3.x
```

##### Install dependencies
Install dependencies,
```bash
$ pip3.4 install --target=$HOME/webapps/<projectname>/lib/python3.x -r requirements.txt
```

##### Collect staticfiles
```bash
$ python3.x manage.py collectstatic
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
*/05 * * * * cd /home/<username>/webapps/<projectname>/care/ && PYTHONPATH=$HOME/webapps/<projectname>/lib/python3.4 /usr/local/bin/python3.4 manage.py runcrons >> $HOME/logs/user/cron.log 2>&1
```
