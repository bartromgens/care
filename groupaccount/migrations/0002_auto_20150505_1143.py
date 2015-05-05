# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
        ('groupaccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsetting',
            name='notification_lower_limit_interval',
            field=models.ForeignKey(to='userprofile.NotificationInterval', null=True),
        ),
        migrations.AddField(
            model_name='groupaccount',
            name='settings',
            field=models.ForeignKey(blank=True, to='groupaccount.GroupSetting', null=True),
        ),
    ]
