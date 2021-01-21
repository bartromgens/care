# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groupaccount', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationInterval',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('days', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('displayname', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\S.*\\S$|^\\S$|^$', 'This field cannot start or end with spaces.')])),
                ('firstname', models.CharField(max_length=100, blank=True)),
                ('lastname', models.CharField(max_length=100, blank=True)),
                ('showTableView', models.BooleanField(default=False)),
                ('group_accounts', models.ManyToManyField(to='groupaccount.GroupAccount', blank=True)),
                ('historyEmailInterval', models.ForeignKey(to='userprofile.NotificationInterval', null=True, on_delete=models.SET_NULL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
