#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

file = None

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = 'examples/print8.ls8'

cpu = CPU()

cpu.load(file)
cpu.run()