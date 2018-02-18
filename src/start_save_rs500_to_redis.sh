#!/bin/bash

cd "$(dirname "$0")"

. ../venv/bin/activate
./save_rs500_to_redis.py
