#!/bin/bash

cd ..

python manage.py schemamigration userprofile --auto
python manage.py migrate userprofile

python manage.py schemamigration groupaccount --auto
python manage.py migrate groupaccount

python manage.py schemamigration transaction --auto
python manage.py migrate transaction

python manage.py schemamigration transactionreal --auto
python manage.py migrate transactionreal

python manage.py schemamigration groupaccountinvite --auto
python manage.py migrate groupaccountinvite

