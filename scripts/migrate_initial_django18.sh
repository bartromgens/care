#!/usr/bin/env bash

cd ..
git checkout v0.2.2 
python3.4 manage.py migrate --fake-initial
git checkout v0.2.3 
python3.4 manage.py migrate
git checkout v0.2.4 
python3.4 manage.py migrate
git checkout v0.2.5 
python3.4 manage.py migrate
git checkout v0.2.6
python3.4 manage.py migrate --fake-initial
git checkout v0.2.7
python3.4 manage.py migrate --fake-initial