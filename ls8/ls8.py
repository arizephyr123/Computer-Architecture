#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    print('Missing second argument.')
    print('Usage: python3 ls8.py <second_file_name.py>\n')
    sys.exit()

else:
    try:
        cpu = CPU()
        cpu.load(sys.argv[1])
        cpu.run()

    except FileNotFoundError:
        print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
