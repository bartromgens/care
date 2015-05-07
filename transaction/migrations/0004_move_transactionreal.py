# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groupaccount', '0002_auto_20150505_1143'),
        ('userprofile', '0002_auto_20150505_1314'),
        ('transaction', '0003_auto_20150505_1459'),
        ('transactionreal', '0004_empty'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='TransactionReal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('comment', models.CharField(max_length=200)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('group_account', models.ForeignKey(to='groupaccount.GroupAccount')),
                ('receiver', models.ForeignKey(to='userprofile.UserProfile', related_name='receiver')),
                ('sender', models.ForeignKey(to='userprofile.UserProfile', related_name='sender')),
            ],
        ),
        migrations.AlterField(
            model_name='modification',
            name='transaction_real',
            field=models.ForeignKey(to='transaction.TransactionReal', blank=True, null=True),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]