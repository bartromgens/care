# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionreal', '0003_remove_transactionreal_modifications'),
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
            field=models.ForeignKey(to='transactionreal.TransactionReal', blank=True, null=True),
        ),
    ]
