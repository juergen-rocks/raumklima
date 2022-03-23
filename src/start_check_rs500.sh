#!/bin/bash

cd "$(dirname "$0")"

poetry run check_rs500.py $@
