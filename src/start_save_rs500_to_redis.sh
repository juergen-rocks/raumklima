#!/bin/bash

cd "$(dirname "$0")"

echo "DEPRECATION NOTICE: This script will go away soon! Use 'start_save_rs500_to_backend.sh' instead!"

poetry run python save_rs500_to_backend.py
