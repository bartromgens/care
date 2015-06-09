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
            name='Modification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('what', models.CharField(max_length=24)),
                ('comment', models.CharField(max_length=200, blank=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('buyer', models.ForeignKey(to='userprofile.UserProfile', related_name='buyer')),
                ('consumers', models.ManyToManyField(related_name='consumers', to='userprofile.UserProfile')),
                ('group_account', models.ForeignKey(to='groupaccount.GroupAccount')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionReal',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('comment', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('group_account', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('receiver', models.ForeignKey(to='userprofile.UserProfile', related_name='receiver')),
                ('sender', models.ForeignKey(to='userprofile.UserProfile', related_name='sender')),
            ],
        ),
        migrations.AddField(
            model_name='modification',
            name='transaction',
            field=models.ForeignKey(to='transaction.Transaction', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='modification',
            name='transaction_real',
            field=models.ForeignKey(to='transaction.TransactionReal', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='modification',
            name='user',
            field=models.ForeignKey(to='userprofile.UserProfile', blank=True),
        ),
    ]
