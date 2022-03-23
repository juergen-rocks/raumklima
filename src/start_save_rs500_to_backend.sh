#!/bin/bash

cd "$(dirname "$0")"

poetry run save_rs500_to_backend.py
