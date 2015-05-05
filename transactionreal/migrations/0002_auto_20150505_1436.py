# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionreal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionreal',
            old_name='groupAccount',
            new_name='group_account',
        ),
    ]
