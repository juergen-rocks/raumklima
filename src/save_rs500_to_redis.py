#!/usr/bin/env python3

"""
Collect Data and save to Redis DB
"""
import warnings
from save_rs500_to_backend import fetch_and_save


if __name__ == "__main__":
    warnings.warn(
        "'save_rs500_to_redis.py' will be removed soon. Use 'save_rs500_to_backend.py' instead.",
        DeprecationWarning,
    )
    fetch_and_save()
