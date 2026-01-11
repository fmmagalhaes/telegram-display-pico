#!/bin/bash
# Run the bot locally with mock hardware modules

# MicroPython doesn't use PYTHONPATH, so we add mock to sys.path in Python
micropython -c "
import sys
sys.path.insert(0, 'mock')
exec(open('main.py').read())
"
