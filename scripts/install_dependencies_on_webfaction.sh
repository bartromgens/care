#!/usr/bin/env bash

PYTHONPATH=$HOME/webapps/care_0_3/lib/python3.4 easy_install-3.4 --install-dir=$HOME/webapps/care_0_3/lib/python3.4 --script-dir=$HOME/webapps/care_0_3/bin `cat requirements.txt`