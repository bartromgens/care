# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groupaccount', '__first__'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAccountInvite',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('isAccepted', models.BooleanField(default=False)),
                ('isDeclined', models.BooleanField(default=False)),
                ('createdDateAndTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('groupAccount', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('invitee', models.ForeignKey(to='userprofile.UserProfile', related_name='invitee')),
                ('inviter', models.ForeignKey(to='userprofile.UserProfile', related_name='inviter')),
            ],
        ),
    ]
