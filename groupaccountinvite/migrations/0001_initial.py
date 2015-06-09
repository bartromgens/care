# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groupaccount', '0002_auto_20150609_2202'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAccountInvite',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('isAccepted', models.BooleanField(default=False)),
                ('isDeclined', models.BooleanField(default=False)),
                ('createdDateAndTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('group_account', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('invitee', models.ForeignKey(to='userprofile.UserProfile', related_name='invitee')),
                ('inviter', models.ForeignKey(to='userprofile.UserProfile', related_name='inviter')),
            ],
        ),
    ]
