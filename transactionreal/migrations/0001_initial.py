# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groupaccount', '__first__'),
        ('userprofile', '__first__'),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionReal',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('comment', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('groupAccount', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('modifications', models.ManyToManyField(to='transaction.Modification', blank=True)),
                ('receiver', models.ForeignKey(related_name='receiver', to='userprofile.UserProfile')),
                ('sender', models.ForeignKey(related_name='sender', to='userprofile.UserProfile')),
            ],
        ),
    ]
