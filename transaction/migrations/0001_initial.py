# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '__first__'),
        ('groupaccount', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('user', models.ForeignKey(blank=True, to='userprofile.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('what', models.CharField(max_length=24)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('buyer', models.ForeignKey(to='userprofile.UserProfile', related_name='buyer')),
                ('consumers', models.ManyToManyField(related_name='consumers', to='userprofile.UserProfile')),
                ('groupAccount', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('modifications', models.ManyToManyField(blank=True, to='transaction.Modification')),
            ],
        ),
    ]
