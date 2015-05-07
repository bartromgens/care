# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionreal', '0003_remove_transactionreal_modifications'),
    ]

    database_operations = [
        migrations.AlterModelTable('TransactionReal', 'transaction_transactionreal')
    ]

    state_operations = [
        migrations.DeleteModel('TransactionReal')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
