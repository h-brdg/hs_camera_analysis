#!/usr/bin/env_python3

"""
Returns the path

"""

import os

def find_mount_point():
    mp_path = os.path.abspath(os.getcwd())
    while not os.path.ismount(mp_path):
        mp_path = os.path.dirname(mp_path)
    return mp_path

if __name__ == "__main__":
    print(find_mount_point())
