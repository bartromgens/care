# Generated by Django 2.2.17 on 2021-01-21 18:53

import datetime
from functools import wraps
from django.db import migrations, models
import django.db.models.deletion


def set_last_modified_for(model, schema_editor):
    db_alias = schema_editor.connection.alias
    rows = model.objects.using(db_alias).all()

    for row in rows:
        last_mod_date = row.date
        if row.modifications.exists():
            last_mod_date = row.modifications.latest("date").date
        row.last_modified = last_mod_date
        row.save()


def set_last_modified(apps, schema_editor):
    for model_name in ("Transaction", "TransactionRecurring", "TransactionReal"):
        model = apps.get_model("transaction", model_name)
        set_last_modified_for(model, schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ("transaction", "0004_related_modifications"),
    ]

    operations = [
        # Create the fields with current date
        migrations.AddField(
            model_name="transaction",
            name="last_modified",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime.now, editable=False
            ),
        ),
        migrations.AddField(
            model_name="transactionreal",
            name="last_modified",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime.now, editable=False
            ),
        ),
        migrations.AddField(
            model_name="transactionrecurring",
            name="last_modified",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime.now, editable=False
            ),
        ),
        # Update the dates to the correct last_mod date
        migrations.RunPython(set_last_modified, migrations.RunPython.noop),
    ]
