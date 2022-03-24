#!/bin/bash

cd "$(dirname "$0")"

poetry run python check_rs500.py $@
