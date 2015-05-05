# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactionreal', '0002_auto_20150505_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionreal',
            name='modifications',
        ),
    ]
