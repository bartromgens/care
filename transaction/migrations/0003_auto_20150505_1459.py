# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20150505_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='modifications',
        ),
        migrations.AddField(
            model_name='modification',
            name='transaction',
            field=models.ForeignKey(to='transaction.Transaction', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='modification',
            name='transaction_real',
            field=models.ForeignKey(to='transaction.TransactionReal', blank=True, null=True),
        ),
    ]
