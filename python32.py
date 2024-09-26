#!/usr/bin/env python3
### chap13/python32.py
import subprocess
import sys

from rewrite import rewrite_emsg

def main():
    # We don't fall into the interactive Python
    # interpreter. We expect an input script.
    if len(sys.argv) < 2:
        sys.exit('[python32]: Please specify an input script')

    # Launch input script as a subprocess
    sys.argv[0] = 'python3'
    p = subprocess.run(sys.argv, stderr=subprocess.PIPE)

    # Convert the bytes to a string
    e = p.stderr.decode('utf-8')

    if len(e) != 0:
        rewrite_emsg(e)

if __name__ == '__main__':
    main()
