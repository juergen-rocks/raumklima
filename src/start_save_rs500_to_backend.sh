#!/bin/bash

cd "$(dirname "$0")"

poetry run python save_rs500_to_backend.py
