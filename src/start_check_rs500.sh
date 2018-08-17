#!/bin/bash

cd "$(dirname "$0")"

. ../venv/bin/activate
./check_rs500.py $@
