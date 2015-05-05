# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAccount',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('number', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupSetting',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('notification_lower_limit', models.IntegerField(default=-100)),
                ('notification_lower_limit_interval', models.ForeignKey(to='userprofile.NotificationInterval', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='groupaccount',
            name='settings',
            field=models.ForeignKey(to='groupaccount.GroupSetting', null=True, blank=True),
        ),
    ]
