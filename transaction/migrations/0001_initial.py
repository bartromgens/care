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
            name='Modification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('user', models.ForeignKey(blank=True, to='userprofile.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('what', models.CharField(max_length=24)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('buyer', models.ForeignKey(to='userprofile.UserProfile', related_name='buyer')),
                ('consumers', models.ManyToManyField(to='userprofile.UserProfile', related_name='consumers')),
                ('groupAccount', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('modifications', models.ManyToManyField(blank=True, to='transaction.Modification')),
            ],
        ),
    ]
