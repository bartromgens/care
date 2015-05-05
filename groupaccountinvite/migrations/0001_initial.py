# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
        ('groupaccount', '0002_auto_20150505_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAccountInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('isAccepted', models.BooleanField(default=False)),
                ('isDeclined', models.BooleanField(default=False)),
                ('createdDateAndTime', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('groupAccount', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('invitee', models.ForeignKey(to='userprofile.UserProfile', related_name='invitee')),
                ('inviter', models.ForeignKey(to='userprofile.UserProfile', related_name='inviter')),
            ],
        ),
    ]
